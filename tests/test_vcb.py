import unittest
import networkx as nx
from src.vcb import vcb_recursive

class TestVCB(unittest.TestCase):
    def test_vcb_empty(self):
        G = nx.Graph()
        self.assertTrue(vcb_recursive(G, 0))
        self.assertTrue(vcb_recursive(G, 1))

    def test_vcb_single_edge(self):
        G = nx.Graph([(0, 1)])
        self.assertFalse(vcb_recursive(G, 0))
        self.assertTrue(vcb_recursive(G, 1))

    def test_vcb_triangle(self):
        G = nx.Graph([(0, 1), (1, 2), (0, 2)])
        self.assertFalse(vcb_recursive(G, 1))
        self.assertTrue(vcb_recursive(G, 2))

    def test_vcb_path(self):
        G = nx.path_graph(4)  # 0-1-2-3
        self.assertTrue(vcb_recursive(G, 2))  # {1,2} is a cover
        self.assertFalse(vcb_recursive(G, 1))

    def test_vcb_cycle(self):
        """Test sur un cycle, qui requiert n/2 sommets"""
        G = nx.cycle_graph(6)
        self.assertFalse(vcb_recursive(G, 2))
        self.assertTrue(vcb_recursive(G, 3))

    def test_vcb_bipartite(self):
        """Test sur un graphe biparti complet"""
        G = nx.complete_bipartite_graph(3, 4)
        self.assertTrue(vcb_recursive(G, 3))
        self.assertFalse(vcb_recursive(G, 2))

    def test_vcb_disconnected(self):
        """Test sur graphe avec composantes déconnectées"""
        G = nx.Graph()
        G.add_edges_from([(1, 2), (3, 4), (5, 6)])
        self.assertTrue(vcb_recursive(G, 3))
        self.assertFalse(vcb_recursive(G, 2))