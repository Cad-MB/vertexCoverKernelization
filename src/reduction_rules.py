import networkx as nx


def high_degree_rule(G: nx.Graph, k: int) -> int:
    """
    Applique la règle de réduction des sommets de haut degré :
    - Si un sommet v a un degré strictement supérieur à k, il doit obligatoirement
      appartenir à toute couverture de sommets de taille k.
    - Il est donc supprimé du graphe et k est décrémenté.

    Paramètres
    ----------
    G : nx.Graph
        Graphe d'entrée (modifié en place).
    k : int
        Valeur actuelle du paramètre k (taille maximale du vertex cover).

    Retourne
    --------
    new_k : int
        Nouvelle valeur de k après l'application des réductions.
    """
    degs = dict(G.degree())  # Dictionnaire des degrés des sommets
    changed = True  # Indicateur pour suivre les modifications

    while changed:
        changed = False
        for v in list(G.nodes()):
            if degs[v] > k:  # Si un sommet a un degré > k, il doit être dans le vertex cover
                G.remove_node(v)  # Suppression du sommet
                k -= 1  # Ajustement du paramètre k
                changed = True
                break  # Redémarrer l'itération après modification

        if changed:
            degs = dict(G.degree())  # Mise à jour des degrés après suppression

    return k
