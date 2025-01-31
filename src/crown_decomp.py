import networkx as nx
from networkx.algorithms import bipartite


def maximal_matching(G: nx.Graph):
    """
    Détermine un couplage maximal dans le graphe G en utilisant une approche gloutonne.
    Renvoie une liste d'arêtes (u, v) représentant le couplage trouvé.
    """
    m = []  # Liste des arêtes du couplage maximal
    used = set()  # Ensemble des sommets déjà appariés

    for u in G.nodes():
        if u not in used:
            for v in G.neighbors(u):
                if v not in used:
                    m.append((u, v))  # Ajout de l'arête au couplage
                    used.add(u)
                    used.add(v)
                    break  # On arrête après avoir trouvé une correspondance pour U.
    return m


def build_bipartite_subgraph(G: nx.Graph, matched_vertices: set, unmatched: set):
    """
    Construit un sous-graphe biparti à partir des sommets appariés et non appariés.
    - Les sommets appariés forment la première partie (0).
    - Les sommets non appariés constituent la seconde partie (1).
    Seules les arêtes reliant ces deux ensembles sont conservées.
    """
    b = nx.Graph()
    b.add_nodes_from(matched_vertices, bipartite=0)
    b.add_nodes_from(unmatched, bipartite=1)

    # Ajout des arêtes entre les sommets appariés et les non appariés
    for u in matched_vertices:
        for v in G[u]:
            if v in unmatched:
                b.add_edge(u, v)

    return b


def crown_decomposition(G: nx.Graph, k: int):
    """
    Tente de trouver une décomposition en couronne (C, H, R) du graphe G.
    Retourne un triplet (C, H, is_no_instance) où :
    - C'est l'ensemble couronne (un ensemble indépendant de sommets).
    - H est la tête de la couronne.
    - is_no_instance est un booléen indiquant si l'on peut conclure qu'aucune couverture de sommets de taille k n'existe.
    """
    m = maximal_matching(G)

    # Si le couplage contient plus de k arêtes, alors il est impossible d'obtenir une couverture de taille k
    if len(m) > k:
        return None, None, True

    matched_vertices = set()

    # Extraction des sommets appariés dans le couplage
    for (u, v) in m:
        matched_vertices.add(u)
        matched_vertices.add(v)

    # Les sommets restants sont ceux qui ne sont pas couplés
    unmatched = set(G.nodes()) - matched_vertices

    # Construction du sous-graphe biparti entre sommets appariés et non appariés
    b = build_bipartite_subgraph(G, matched_vertices, unmatched)

    match_dict = {}

    try:
        for component in nx.connected_components(b):
            sub = b.subgraph(component)
            if not sub.nodes():
                continue
            top, _ = bipartite.sets(sub)
            matching_sub = bipartite.maximum_matching(sub, top_nodes=top)
            match_dict.update(matching_sub)
    except nx.AmbiguousSolution:
        pass  # Si la bipartition est ambiguë, on ignore cette exception

    # Vérification de l'existence d'un sommet non apparié avec un voisinage vide
    for x in unmatched:
        neigh = set(b[x])
        if len(neigh) == 0:
            c = {x}  # Candidat pour l'ensemble couronne
            h = set()  # La tête de la couronne est vide.
            return c, h, False

    return None, None, False
