import networkx as nx


def remove_isolated_vertices(G: nx.Graph):
    """
    Supprime les sommets isolés du graphe G.

    Un sommet est considéré comme isolé s'il n'a aucune arête incidente.
    """
    isolated = list(nx.isolates(G))  # Identifie les sommets isolés
    G.remove_nodes_from(isolated)  # Supprime ces sommets du graphe


def is_vertex_cover(G: nx.Graph, cover_set) -> bool:
    """
    Vérifie si un ensemble de sommets donné constitue un vertex cover valide pour G.

    Un vertex cover est un sous-ensemble de sommets tel que chaque arête du graphe
    a au moins une de ses extrémités dans cet ensemble.

    Paramètres
    ----------
    G : nx.Graph
        Graphe sur lequel la vérification est effectuée.
    cover_set : iterable
        Ensemble de sommets candidats pour être un vertex cover.

    Retourne
    --------
    bool
        True si cover_set est un vertex cover valide, False sinon.
    """
    covered_edges = 0
    total_edges = G.number_of_edges()
    cover_set = set(cover_set)  # Conversion en ensemble pour accès rapide

    for (u, v) in G.edges():
        if (u in cover_set) or (v in cover_set):  # Vérifie si l'arête est couverte
            covered_edges += 1

    return covered_edges == total_edges
