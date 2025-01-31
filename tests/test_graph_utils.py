import unittest
import networkx as nx
from src.graph_utils import remove_isolated_vertices, is_vertex_cover

class TestGraphUtils(unittest.TestCase):
    def test_remove_isolated_vertices(self):
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3, 4])
        G.add_edge(1, 2)
        remove_isolated_vertices(G)
        self.assertEqual(set(G.nodes()), {1, 2})

    def test_is_vertex_cover_empty(self):
        G = nx.Graph()
        self.assertTrue(is_vertex_cover(G, set()))

    def test_is_vertex_cover_complete(self):
        G = nx.complete_graph(3)
        self.assertTrue(is_vertex_cover(G, {0, 1}))
        self.assertFalse(is_vertex_cover(G, {0}))