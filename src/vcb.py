import networkx as nx


def vcb_recursive(G: nx.Graph, k: int) -> bool:
    """
    Algorithme récursif de branchement pour le problème du Vertex Cover.
    Détermine si le graphe G possède une couverture de sommets de taille ≤ k.

    Paramètres
    ----------
    G : nx.Graph
        Le graphe d'entrée.
    k : int
        Taille maximale autorisée du vertex cover.

    Retourne
    --------
    bool
        True si un vertex cover de taille ≤ k existe, False sinon.
    """
    # Si k devient négatif, il est impossible d'avoir une couverture valide
    if k < 0:
        return False

    # Si le graphe n'a plus d'arêtes, alors tout ensemble de sommets est un vertex cover
    if G.number_of_edges() == 0:
        return True

    # Si k est nul mais qu'il reste des arêtes, alors aucun vertex cover valide n'existe
    if k == 0:
        return G.number_of_edges() == 0

    # Sélection d'une arête (u, v) arbitraire
    u, v = next(iter(G.edges()))

    # Première branche : Suppression du sommet u et exploration avec k-1
    g1 = G.copy()
    g1.remove_node(u)
    if vcb_recursive(g1, k - 1):
        return True

    # Deuxième branche : Suppression du sommet v et exploration avec k-1
    g2 = G.copy()
    g2.remove_node(v)

    return vcb_recursive(g2, k - 1)
