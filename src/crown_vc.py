#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implémentation de la réduction via décomposition en couronne (Crown Decomposition)
pour le problème k-Vertex Cover, basée sur les références :

- Cygan et al, "Parameterized Algorithms", Springer, 2015, Chapitre Kernelization (pages 26 à 29)
- TD Kernels Exercice 4
- Hopcroft et Karp pour le couplage biparti
- Lemme de la couronne (Crown Lemma) permettant d'obtenir un kernel de taille <= 3k.

Objectif : obtenir un kernel de taille au plus 3k pour k-Vertex Cover, puis comparer
avec l'algorithme de branchement (VCB) sans réduction préalable.

Copyright : projet étudiant 2025
"""

import networkx as nx
from networkx.algorithms import bipartite
import random
import time


def remove_isolated_vertices(G: nx.Graph):
    """
    Supprime les sommets isolés du graphe G, c.-à-d. ceux de degré 0.
    Réduction : un sommet isolé n'a pas d'arêtes à couvrir -> il peut être éliminé sans impacter la couverture.
    """
    isolated = list(nx.isolates(G))
    G.remove_nodes_from(isolated)


def high_degree_rule(G: nx.Graph, k: int):
    """
    Réduction : si un sommet v a un degré strictement supérieur à k, alors pour couvrir toutes les arêtes incidentes à v,
    v doit appartenir au vertex cover. On enlève donc v du graphe et on décrémente k de 1.
    
    Paramètres
    ----------
    G : nx.Graph
        Le graphe dans lequel on applique la réduction.
    k : int
        Le paramètre du vertex cover.

    Retourne
    --------
    new_k : int
        La nouvelle valeur du paramètre k après application de la règle.
    """
    degs = dict(G.degree())
    changed = True
    while changed:
        changed = False
        for v in list(G.nodes()):
            if degs[v] > k:
                # v doit être dans le cover
                G.remove_node(v)
                k -= 1
                changed = True
                break
        if changed:
            degs = dict(G.degree())
    return k


def maximal_matching(G: nx.Graph):
    """
    Trouve un couplage maximal glouton dans G (pas nécessairement maximum).
    Utilisé dans la fonction crown_decomposition (pour comparer avec le paramètre).

    Paramètres
    ----------
    G : nx.Graph
        Le graphe.
    
    Retourne
    --------
    M : list of (u, v)
        Liste d'arêtes formant un couplage (chaque sommet apparaît au plus une fois).
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


def build_bipartite_subgraph(G: nx.Graph, matched_vertices: set, unmatched: set):
    """
    Construit un sous-graphe biparti B à partir des sommets matched et unmatched.
    matched sera une des parts (part 0) et unmatched l'autre (part 1).

    Arêtes : on ne garde que celles qui relient un sommet matched à un sommet unmatched dans G.

    Paramètres
    ----------
    G : nx.Graph
        Le graphe original.
    matched_vertices : set
        Sommets appariés dans le couplage (partie "top").
    unmatched : set
        Sommets non appariés (partie "bottom").

    Retourne
    --------
    B : nx.Graph
        Le sous-graphe biparti construit.
    """
    B = nx.Graph()
    B.add_nodes_from(matched_vertices, bipartite=0)
    B.add_nodes_from(unmatched, bipartite=1)
    for u in matched_vertices:
        for v in G[u]:
            if v in unmatched:
                B.add_edge(u, v)
    return B


def crown_decomposition(G: nx.Graph, k: int):
    """
    Tente de trouver une décomposition en couronne (C, H, R) du graphe G pour le paramètre k.

    Étapes :
    1) On calcule un couplage maximal (non nécessairement maximum) M dans G (fonction maximal_matching).
    2) Si |M| > k, alors on a déjà un couplage > k => "NO-instance" (pas de cover <= k).
    3) On sépare matched = {u, v pour (u, v) in M}, unmatched = autres sommets.
    4) On construit un biparti B en séparant matched vs unmatched.
    5) On cherche un couplage maximum (Hopcroft-Karp) dans B. 
       - S'il y a un sommet x in unmatched n'ayant pas de voisins => petite couronne triviale (C={x}, H=vide).
         (car x isolé dans B => x stable dans G, etc.)
       - Sinon, on essaye d'identifier un sous-ensemble C et H satisfaisant la définition de la couronne.

    Pour simplifier, on se base sur l'hypothèse que si un unmatched est "peu connecté", on peut construire (C,H).
    Dans la pratique, on renvoie (None,None,False) si on ne la trouve pas.

    Paramètres
    ----------
    G : nx.Graph
        Le graphe.
    k : int
        Le paramètre.

    Retourne
    --------
    (C, H, no_instance) : (set or None, set or None, bool)
        - C, H = la couronne trouvée, ou None, None si aucune trouvée
        - no_instance = True si on conclut directement "pas de cover de taille <= k".
    """
    # 1) Couplage "maximal" (glouton)
    M = maximal_matching(G)
    if len(M) > k:
        # si couplage > k, alors impossible d'avoir un vertex cover de taille k
        return None, None, True

    matched_vertices = set()
    for (u, v) in M:
        matched_vertices.add(u)
        matched_vertices.add(v)

    unmatched = set(G.nodes()) - matched_vertices

    # 2) Construire le biparti B (pour Hopcroft-Karp)
    B = build_bipartite_subgraph(G, matched_vertices, unmatched)

    # 3) Essayer un couplage maximum dans B
    #    on utilise networkx.algorithms.bipartite.maximum_matching
    #    besoin de l'ensemble top_nodes => matched_vertices
    match_dict = {}
    try:
        # On travaille par composantes connectées de B (sinon hopcroft_karp() l'exige)
        for component in nx.connected_components(B):
            sub = B.subgraph(component)
            if not sub.nodes():
                continue
            # bipartite.sets(sub) peut lever AmbiguousSolution si le sous-graphe n'est pas biparti
            top, _ = bipartite.sets(sub)
            matching_sub = bipartite.maximum_matching(sub, top_nodes=top)
            match_dict.update(matching_sub)
    except nx.AmbiguousSolution:
        pass  # on ignore la situation ambiguë

    # 4) Chercher si un unmatched x n'a pas de voisins dans B => cas simple : C={x}, H=voisins(x).
    #    Puis on aura R = tous les autres.
    #    => c'est déjà une crown decomposition : C stable, arcs seulement C->H, etc.
    for x in unmatched:
        neigh = set(B[x])
        if len(neigh) == 0:
            # x n'a pas de voisins => x est un sommet "isolé" du côté unmatched
            C = {x}
            H = set()
            R = set(G.nodes()) - C - H
            # On a C stable, pas d'arête vers R, trivialement.
            # H=vide => couplage saturant H => couplage de taille 0, c'est ok.
            return C, H, False

    # Si on ne trouve pas de couronne évidente, on rend None, None
    return None, None, False


def crown_reduction(G: nx.Graph, k: int):
    """
    Applique itérativement les règles de réduction sur G, pour produire un kernel ou
    conclure NO-instance.

    Règles appliquées à chaque étape :
      1) remove_isolated_vertices
      2) high_degree_rule (si sommet deg > k)
      3) si nb_sommets <= 3*k => on arrête et on rend le graphe
      4) crown_decomposition => si trouvé couronne C,H :
            on supprime C du graphe
            on décrémente k de |H|
         si couplage > k => NO-instance

    Paramètres
    ----------
    G : nx.Graph
        Le graphe d'entrée.
    k : int
        Le paramètre du vertex cover.

    Retourne
    --------
    (kernel_graph, new_k, no_instance) :
        kernel_graph : nx.Graph or None
        new_k : int
        no_instance : bool
    """
    G = G.copy()
    while True:
        # 1) remove isolated
        remove_isolated_vertices(G)

        # 2) high_degree_rule
        k = high_degree_rule(G, k)
        if k < 0:
            return None, 0, True

        # 3) si |V| <= 3*k => on arrête
        if G.number_of_nodes() <= 3 * k:
            return G, k, False

        # 4) crown_decomposition
        C, H, no_inst = crown_decomposition(G, k)
        if no_inst:
            return None, 0, True
        if C is None:
            # aucune couronne trouvée => on arrête
            return G, k, False
        # Sinon, on a trouvé une couronne -> on réduit
        G.remove_nodes_from(C)
        k -= len(H)
        if k < 0:
            return None, 0, True


def kernel_vertex_cover_crown(G: nx.Graph, k: int):
    """
    Fonction principale de Kernelization : 
    Retourne le kernel (graphe réduit) de taille <= 3k et la nouvelle valeur de k,
    ou conclut "no_instance".

    Paramètres
    ----------
    G : nx.Graph
        Graphe d'entrée.
    k : int
        Paramètre du vertex cover.

    Retourne
    --------
    (kernel_graph, new_k, no_instance):
        kernel_graph : nx.Graph or None
            Le graphe réduit (kernel).
        new_k : int
            Le nouveau paramètre.
        no_instance : bool
            Indique si on conclut directement que la réponse est NON.
    """
    return crown_reduction(G, k)


def vcb_recursive(G: nx.Graph, k: int) -> bool:
    """
    Algorithme récursif VCB (branch & reduce) pour décider si le graphe G a un vertex cover
    de taille <= k.

    - Cas de base : k=0 => cover possible ssi pas d'arêtes
    - Sinon, on prend une arête (u, v) au hasard.
        * On tente en incluant u dans le cover (=> on supprime u du graphe et on appelle récursivement).
        * Sinon, on tente en incluant v.
      Si l'un aboutit, on renvoie True.

    Complexité ~ O(2^k * (n + m)) en pire cas, ce qui est FPT.

    Paramètres
    ----------
    G : nx.Graph
        Le graphe
    k : int
        Paramètre

    Retourne
    --------
    bool
        True si un VC de taille <= k existe, False sinon.
    """
    if k < 0:
        return False
    if G.number_of_edges() == 0:
        # plus d'arêtes => plus besoin de couvrir
        return True
    if k == 0:
        # s'il reste des arêtes => pas possible
        return (G.number_of_edges() == 0)

    # Choisir une arête
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


def generate_random_graph(n: int, m: int) -> nx.Graph:
    """
    Génère un graphe aléatoire avec n sommets et m arêtes (distribuées uniformément au hasard).
    Utilise la fonction gnm_random_graph de NetworkX.

    Paramètres
    ----------
    n : int
        Nombre de sommets
    m : int
        Nombre d'arêtes

    Retourne
    --------
    G : nx.Graph
        Le graphe généré
    """
    G = nx.gnm_random_graph(n, m, seed=None)
    return G


def generate_vertex_cover_graph(n: int, k: int, edge_prob: float = 0.5) -> nx.Graph:
    """
    Génère un graphe aléatoire ayant (avec forte probabilité) un vertex cover de taille <= k.
    Pour cela, on choisit aléatoirement k sommets qui seront notre "cover imposé", et
    on n'ajoute des arêtes que si elles touchent (au moins) un de ces sommets, 
    ou éventuellement entre les sommets du cover lui-même (selon edge_prob).

    Paramètres
    ----------
    n : int
        Nombre total de sommets
    k : int
        Taille du cover souhaité
    edge_prob : float
        Probabilité d'ajouter une arête entre deux sommets autorisés.

    Retourne
    --------
    G : nx.Graph
        Graphe généré
    """
    G = nx.Graph()
    G.add_nodes_from(range(n))
    cover = set(random.sample(range(n), min(k, n)))  # on choisit k sommets au hasard
    # Ajoute des arêtes tant que (u, v) a au moins un sommet dans cover
    # ou (u, v) tous deux dans cover
    nodes = list(range(n))
    for i in range(n):
        for j in range(i+1, n):
            if (i in cover) or (j in cover):
                # On met une arête avec prob edge_prob
                if random.random() < edge_prob:
                    G.add_edge(i, j)
    return G


def is_vertex_cover(G: nx.Graph, cover_set) -> bool:
    """
    Vérifie si cover_set est un vertex cover du graphe G.
    i.e. pour toute arête (u, v), u in cover_set ou v in cover_set.

    Paramètres
    ----------
    G : nx.Graph
        Le graphe
    cover_set : iterable
        Ensemble de sommets supposé couvrir G

    Retourne
    --------
    bool
        True si c'est effectivement un vertex cover, False sinon
    """
    covered_edges = 0
    total_edges = G.number_of_edges()
    cover_set = set(cover_set)

    # Comptons les arêtes couvertes
    for (u, v) in G.edges():
        if (u in cover_set) or (v in cover_set):
            covered_edges += 1
    return (covered_edges == total_edges)


if __name__ == "__main__":
    # Exemple d'utilisation : Kernelisation + test direct.

    # Petit graphe d'exemple
    G_ex = nx.Graph()
    edges_ex = [(1, 2), (2, 3), (3, 4), (2, 4), (4, 5)]
    G_ex.add_edges_from(edges_ex)
    K = 2

    print("Graphe exemple =", G_ex.edges())
    ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G_ex, K)
    if no_inst:
        print("Réponse : NON (pas de vertex cover de taille <= K).")
    else:
        print("Graphe réduit (kernel) :", ker_graph.nodes(), ker_graph.edges())
        print("Nouveau k :", ker_k)
        # On applique l'algo VCB sur le kernel
        vcb_res = vcb_recursive(ker_graph, ker_k)
        print("=> Test VCB sur kernel :", vcb_res)

    # On applique l'algo VCB sans kernel
    direct_res = vcb_recursive(G_ex, K)
    print("=> Test VCB sans kernel :", direct_res)
