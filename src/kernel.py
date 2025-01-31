import networkx as nx
from .graph_utils import remove_isolated_vertices
from .reduction_rules import high_degree_rule
from .crown_decomp import crown_decomposition


def crown_reduction(g: nx.Graph, k: int):
    """
    Applique la réduction par décomposition en couronne de manière itérative jusqu'à ce que :
    - La taille du graphe soit ≤ 3k (noyau trouvé).
    - Aucune réduction supplémentaire ne soit possible.
    - Il soit établi qu'aucune couverture de sommets de taille k n'existe.

    Paramètres
    ----------
    G : nx.Graph
        Graphe d'entrée sur lequel les réductions sont appliquées.
    k : int
        Paramètre indiquant la taille maximale du vertex cover recherché.

    Retourne
    --------
    tuple (nx.Graph ou None, int, bool)
        - Le graphe réduit si un noyau est trouvé, sinon None.
        - La nouvelle valeur de k après réduction.
        - Un booléen indiquant si l'instance est invalide (aucun vertex cover de taille ≤ k).
    """
    g = g.copy()  # Copie pour éviter de modifier l'original
    while True:
        remove_isolated_vertices(g)  # Suppression des sommets isolés
        k = high_degree_rule(g, k)  # Application de la règle des sommets de haut degré

        if k < 0:
            return None, 0, True  # Impossible de trouver une couverture valide

        if g.number_of_nodes() <= 3 * k:
            return g, k, False  # Noyau obtenu

        # Décomposition en couronne
        c, h, no_inst = crown_decomposition(g, k)

        if no_inst:
            return None, 0, True  # Aucune solution possible
        if c is None:
            return g, k, False  # Aucune réduction supplémentaire possible

        # Suppression des sommets de la couronne et ajustement de k
        g.remove_nodes_from(c)
        k -= len(h)

        if k < 0:
            return None, 0, True  # Instance invalide après réduction


def kernel_vertex_cover_crown(G: nx.Graph, k: int):
    """
    Fonction principale de kernelization pour le problème du vertex cover.

    Paramètres
    ----------
    G : nx.Graph
        Graphe d'entrée.
    k : int
        Taille maximale du vertex cover recherché.

    Retourne
    --------
    tuple (nx.Graph ou None, int, bool)
        - Le graphe réduit après kernelization, ou None si l'instance est invalide.
        - La nouvelle valeur de k après les réductions.
        - Un booléen indiquant si aucun vertex cover de taille ≤ k n'existe.
    """
    return crown_reduction(G, k)
