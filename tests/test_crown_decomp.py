import unittest
import networkx as nx
from src.crown_decomp import (
    maximal_matching, build_bipartite_subgraph, crown_decomposition
)


class TestCrownDecomp(unittest.TestCase):
    """
    Suite de tests unitaires pour les fonctions de la décomposition en couronne.
    """

    def test_maximal_matching_empty(self):
        """
        Vérifie que l'algorithme de couplage maximal fonctionne correctement
        sur un graphe vide (résultat attendu : liste vide).
        """
        g = nx.Graph()
        m = maximal_matching(g)
        self.assertEqual(m, [])

    def test_maximal_matching_path(self):
        """
        Vérifie que le couplage maximal est correct pour un graphe en chemin.
        Un chemin de 4 sommets devrait avoir un couplage de 2 arêtes.
        """
        g = nx.path_graph(4)
        m = maximal_matching(g)
        self.assertEqual(len(m), 2)
        edges = set(map(frozenset, m))
        possible = {frozenset([0, 1]), frozenset([2, 3])}
        self.assertEqual(edges, possible)

    def test_build_bipartite(self):
        """
        Teste la construction d'un sous-graphe biparti à partir des sommets appariés et non appariés.
        Vérifie que le graphe obtenu est bien biparti et contient le bon nombre d'arêtes.
        """
        g = nx.Graph([(1, 2), (2, 3), (3, 4)])
        matched = {1, 2}
        unmatched = {3, 4}
        b = build_bipartite_subgraph(g, matched, unmatched)
        self.assertEqual(len(b.edges()), 1)
        self.assertTrue(nx.is_bipartite(b))

    def test_crown_decomposition_small(self):
        """
        Vérifie la décomposition en couronne pour un petit graphe en chemin.
        Le graphe étant réduit, on s'assure que l'instance n'est pas triviale (no_inst=False).
        """
        g = nx.path_graph(3)
        c, h, no_inst = crown_decomposition(g, 2)
        self.assertFalse(no_inst)
        if c is not None:
            self.assertTrue(nx.is_independent_set(g, c))

    def test_maximal_matching_complete_graph(self):
        """
        Vérifie que le couplage maximal est correct pour un graphe complet de 6 sommets.
        Un graphe complet de 6 sommets doit avoir un couplage de 3 arêtes.
        """
        g = nx.complete_graph(6)
        m = maximal_matching(g)
        self.assertEqual(len(m), 3)

    def test_maximal_matching_disconnected(self):
        """
        Vérifie que l'algorithme de couplage maximal fonctionne correctement
        sur un graphe composé de plusieurs composantes connexes indépendantes.
        """
        g = nx.Graph()
        g.add_edges_from([(1, 2), (3, 4), (5, 6)])
        m = maximal_matching(g)
        self.assertEqual(len(m), 3)

    def test_build_bipartite_empty_matched(self):
        """
        Vérifie la construction d'un sous-graphe biparti lorsque l'ensemble des sommets appariés est vide.
        Le graphe résultant ne doit contenir aucune arête.
        """
        g = nx.Graph([(1, 2), (2, 3)])
        b = build_bipartite_subgraph(g, set(), {1, 2, 3})
        self.assertEqual(len(b.edges()), 0)

    def test_crown_decomposition_no_crown(self):
        """
        Vérifie le comportement de la décomposition en couronne lorsqu'aucune couronne n'est détectée.
        Un graphe complet ne devrait pas permettre une telle décomposition.
        """
        g = nx.complete_graph(4)
        c, h, no_inst = crown_decomposition(g, 2)
        self.assertIsNone(c)
        self.assertIsNone(h)

    def test_crown_decomposition_isolated_vertex(self):
        """
        Vérifie que la décomposition en couronne identifie correctement un sommet isolé.
        Un sommet sans arête devrait être détecté comme une couronne de taille 1.
        """
        g = nx.Graph()
        g.add_nodes_from([1, 2, 3])
        g.add_edge(1, 2)
        c, h, no_inst = crown_decomposition(g, 1)
        self.assertEqual(c, {3})
        self.assertEqual(h, set())
