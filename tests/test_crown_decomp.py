import unittest
import networkx as nx
from src.crown_decomp import (maximal_matching, build_bipartite_subgraph,
                            crown_decomposition)

class TestCrownDecomp(unittest.TestCase):
    def test_maximal_matching_empty(self):
        G = nx.Graph()
        M = maximal_matching(G)
        self.assertEqual(M, [])

    def test_maximal_matching_path(self):
        G = nx.path_graph(4)  # 0-1-2-3
        M = maximal_matching(G)
        self.assertEqual(len(M), 2)
        edges = set(map(frozenset, M))
        possible = {frozenset([0, 1]), frozenset([2, 3])}
        self.assertEqual(edges, possible)

    def test_build_bipartite(self):
        G = nx.Graph([(1, 2), (2, 3), (3, 4)])
        matched = {1, 2}
        unmatched = {3, 4}
        B = build_bipartite_subgraph(G, matched, unmatched)
        self.assertEqual(len(B.edges()), 1)  # Only edge (2,3) connects matched to unmatched
        self.assertTrue(nx.is_bipartite(B))

    def test_crown_decomposition_small(self):
        G = nx.path_graph(3)  # Simple path 0-1-2
        C, H, no_inst = crown_decomposition(G, 2)
        self.assertFalse(no_inst)
        if C is not None:
            self.assertTrue(nx.is_independent_set(G, C))

    def test_maximal_matching_complete_graph(self):
        G = nx.complete_graph(6)
        M = maximal_matching(G)
        self.assertEqual(len(M), 3)  # Un couplage maximal contient n/2 arêtes

    def test_maximal_matching_disconnected(self):
        G = nx.Graph()
        G.add_edges_from([(1, 2), (3, 4), (5, 6)])
        M = maximal_matching(G)
        self.assertEqual(len(M), 3)

    def test_build_bipartite_empty_matched(self):
        G = nx.Graph([(1, 2), (2, 3)])
        B = build_bipartite_subgraph(G, set(), {1, 2, 3})
        self.assertEqual(len(B.edges()), 0)

    def test_crown_decomposition_no_crown(self):
        G = nx.complete_graph(4)
        C, H, no_inst = crown_decomposition(G, 2)
        self.assertIsNone(C)
        self.assertIsNone(H)

    def test_crown_decomposition_isolated_vertex(self):
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3])
        G.add_edge(1, 2)
        C, H, no_inst = crown_decomposition(G, 1)
        self.assertEqual(C, {3})
        self.assertEqual(H, set())
