import unittest
import networkx as nx
from src.reduction_rules import high_degree_rule

class TestReductionRules(unittest.TestCase):
    def test_high_degree_empty(self):
        G = nx.Graph()
        k = high_degree_rule(G, 2)
        self.assertEqual(k, 2)
        self.assertEqual(len(G.nodes()), 0)

    def test_high_degree_star(self):
        G = nx.star_graph(5)  # Center vertex degree 5
        k = high_degree_rule(G, 3)
        self.assertEqual(k, 2)  # k decremented by 1
        self.assertEqual(len(G.nodes()), 5)  # Center removed

    def test_high_degree_complete(self):
        G = nx.complete_graph(4)
        k = high_degree_rule(G, 2)
        self.assertEqual(k, -2)  # All vertices removed
        self.assertEqual(len(G.nodes()), 0)

    def test_high_degree_chain_reaction(self):
        """Test de réduction en chaîne avec attente correcte"""
        G = nx.Graph()
        G.add_edges_from([(1,2), (2,3), (3,4), (1,3), (2,4), (1,4)])
        k = high_degree_rule(G, 2)
        self.assertEqual(k, -2)  # k devient négatif car trop de sommets de haut degré