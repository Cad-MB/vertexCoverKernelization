"""
Implémentation de la réduction via décomposition en couronne (Crown Decomposition)
pour le problème k-Vertex Cover, basée sur les références :

- Cygan et al, "Parameterized Algorithms", Springer, 2015, Chapitre Kernelization (pages 26 à 29)
- TD Kernels Exercice 4
- Hopcroft et Karp pour le couplage maximum biparti

Objectif : obtenir un kernel de taille au plus 3k pour k-Vertex Cover.
"""

import networkx as nx
import time
import random
from networkx.algorithms import bipartite


def remove_isolated_vertices(G):
    """
    Supprime les sommets isolés du graphe G.
    """
    isolated = list(nx.isolates(G))
    G.remove_nodes_from(isolated)

def high_degree_rule(G, k):
    degs = dict(G.degree())
    changed = True
    while changed:
        changed = False
        for v in list(G.nodes()):
            if degs[v] > k:
                print(f"Suppression sommet {v} (degré {degs[v]}), décrémentation de k ({k} -> {k-1})")
                G.remove_node(v)
                k -= 1
                changed = True
                break
        if changed:
            degs = dict(G.degree())
    return k

def maximal_matching(G):
    """
    Trouve un couplage maximal dans G en utilisant une approche gloutonne.
    """
    M = []
    used = set()
    for u in G.nodes():
        if u not in used:
            for v in G.neighbors(u):
                if v not in used:
                    M.append((u, v))
                    used.add(u)
                    used.add(v)
                    break
    return M


def build_bipartite_subgraph(G, matched, unmatched):
    """
    Construit un sous-graphe biparti B à partir des sommets matcheés et non matcheés.
    """
    B = nx.Graph()
    B.add_nodes_from(matched, bipartite=0)
    B.add_nodes_from(unmatched, bipartite=1)
    for u in matched:
        for v in G[u]:
            if v in unmatched:
                B.add_edge(u, v)
    return B


def crown_decomposition(G, k):
    M = maximal_matching(G)
    if len(M) > k:
        return None, None, True  # "NO-instance"

    matched_vertices = set()
    for (u, v) in M:
        matched_vertices.add(u)
        matched_vertices.add(v)

    unmatched = set(G.nodes()) - matched_vertices
    B = build_bipartite_subgraph(G, matched_vertices, unmatched)

    match_dict = {}
    for component in nx.connected_components(B):
        subgraph = B.subgraph(component)
        if len(subgraph.nodes()) == 0:
            continue
        try:
            top_nodes, _ = bipartite.sets(subgraph)
            matching = bipartite.maximum_matching(subgraph, top_nodes=top_nodes)
            match_dict.update(matching)
        except nx.AmbiguousSolution:
            continue

    for x in unmatched:
        neigh = set(B[x])
        if len(neigh) < 1:  # Cas simple de couronne
            C = {x}
            H = neigh
            R = set(G.nodes()) - C - H
            print(f"Décomposition couronne trouvée : C={C}, H={H}, R={R}")
            return C, H, False

    print("Aucune décomposition couronne trouvée.")
    return None, None, False

def crown_reduction(G, k):
    while True:
        print(f"Avant réduction : {len(G.nodes())} sommets, {len(G.edges())} arêtes, k = {k}")

        remove_isolated_vertices(G)
        k = high_degree_rule(G, k)

        if k < 0:
            return None, 0, True

        if G.number_of_nodes() <= 3 * k:
            return G, k, False

        C, H, no_instance = crown_decomposition(G, k)

        if no_instance:
            return None, 0, True
        if C is None:
            return G, k, False

        print(f"Suppression de {len(C)} sommets du kernel")

        G.remove_nodes_from(C)
        k -= len(H)

def kernel_vertex_cover_crown(G, k):
    """
    Applique la réduction de couronne sur G avec le paramètre k.
    Retourne le graphe kernelisé, le nouveau k, et un indicateur de "NO-instance".
    """
    G = G.copy()
    kernel_graph, new_k, no_instance = crown_reduction(G, k)
    return kernel_graph, new_k, no_instance


def vcb_recursive(G, k):
    """
    Algorithme récursif pour le Vertex Cover basé sur l'énumération des couplages.
    Retourne True si un vertex cover de taille ≤k existe, sinon False.
    """
    if k == 0:
        return len(G.edges()) == 0
    if len(G.edges()) == 0:
        return True

    # Choisir une arête (u, v)
    u, v = next(iter(G.edges()))

    # Brancher sur l'inclusion de u
    G1 = G.copy()
    G1.remove_node(u)
    if vcb_recursive(G1, k - 1):
        return True

    # Brancher sur l'inclusion de v
    G2 = G.copy()
    G2.remove_node(v)
    return vcb_recursive(G2, k - 1)

import time
import random


def generate_random_graph(n, m):
    """
    Génère un graphe aléatoire avec n sommets et m arêtes.
    """
    G = nx.gnm_random_graph(n, m)
    return G


def generate_vertex_cover_graph(n, k, edge_prob=0.5):
    """
    Génère un graphe aléatoire avec un vertex cover de taille ≤k.
    """
    G = nx.Graph()
    vertex_cover = set(random.sample(range(n), k))
    non_cover = set(range(n)) - vertex_cover
    # Ajoute des arêtes uniquement entre cover et non-cover ou entre cover et cover
    for u in range(n):
        for v in range(u + 1, n):
            if u in vertex_cover or v in vertex_cover:
                if random.random() < edge_prob:
                    G.add_edge(u, v)
    return G

def is_vertex_cover(G, cover_set):
    """
    Vérifie si cover_set est un vertex cover valide du graphe G.
    Un vertex cover doit couvrir toutes les arêtes du graphe.
    """
    covered_edges = set()
    for v in cover_set:
        for neighbor in G.neighbors(v):
            covered_edges.add(frozenset((v, neighbor)))

    return len(covered_edges) == len(G.edges())

if __name__ == "__main__":
    # Exemple d'utilisation de la réduction de kernel
    G_ex = nx.Graph()
    edges_ex = [(1, 2), (2, 3), (3, 4), (2, 4), (4, 5)]
    G_ex.add_edges_from(edges_ex)
    K = 2

    ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G_ex, K)
    if no_inst:
        print("Réponse : NON (pas de vertex cover de taille ≤ k).")
    else:
        print("Graphe réduit :", ker_graph.nodes(), ker_graph.edges())
        print("Nouveau k :", ker_k)

    # Comparaison des algorithmes
    import matplotlib.pyplot as plt

    # Paramètres pour les tests
    num_tests = 10
    sizes = [50, 100, 150, 200, 250, 300]
    k_values = [5, 10, 15, 20]

    results_kernel = []
    results_vcb = []

    for n in sizes:
        for k in k_values:
            if k > n:
                continue
            # Génération aléatoire
            G = generate_vertex_cover_graph(n, k, edge_prob=0.1)

            # Mesure temps de kernelization + VCB
            start = time.time()
            ker_G, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
            if not no_inst:
                vcb_result = vcb_recursive(ker_G, ker_k)
            else:
                vcb_result = False
            end = time.time()
            time_kernel = end - start
            results_kernel.append((n, k, time_kernel))

            # Mesure temps de VCB sans kernelization
            start = time.time()
            vcb_result_no_kernel = vcb_recursive(G, k)
            end = time.time()
            time_vcb = end - start
            results_vcb.append((n, k, time_vcb))

    # Affichage des résultats (simple exemple)
    import pandas as pd

    df_kernel = pd.DataFrame(results_kernel, columns=['n', 'k', 'Time Kernel + VCB'])
    df_vcb = pd.DataFrame(results_vcb, columns=['n', 'k', 'Time VCB'])

    # Moyennes par taille et k
    mean_kernel = df_kernel.groupby(['n', 'k']).mean().reset_index()
    mean_vcb = df_vcb.groupby(['n', 'k']).mean().reset_index()

    # Tracé pour un k fixe
    fixed_k = 10
    subset_kernel = mean_kernel[mean_kernel['k'] == fixed_k]
    subset_vcb = mean_vcb[mean_vcb['k'] == fixed_k]

    plt.figure(figsize=(10, 6))
    plt.plot(subset_kernel['n'], subset_kernel['Time Kernel + VCB'], label='Kernel + VCB')
    plt.plot(subset_vcb['n'], subset_vcb['Time VCB'], label='VCB Sans Kernel')
    plt.xlabel('Nombre de sommets (n)')
    plt.ylabel('Temps (s)')
    plt.title(f'Comparaison des temps pour k={fixed_k}')
    plt.legend()
    plt.show()