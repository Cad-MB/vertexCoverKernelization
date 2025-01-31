# tests/test_fpt.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests unitaires pour l'algorithme FPT 'vcb_recursive'.
On peut tester plusieurs cas : random, petit graphe, etc.
"""

import unittest
import networkx as nx
import random

from src.fpt import vcb_recursive

class TestFPT(unittest.TestCase):

    def test_vcb_small_random(self):
        """Petit test sur un graphe aléatoire."""
        random.seed(42)
        G = nx.gnm_random_graph(6, 8)
        # On ne sait pas la taille min du VC,
        # on vérifie juste que vcb_recursive ne plante pas.
        res = vcb_recursive(G, 3)
        self.assertIn(res, [True, False])

    def test_vcb_no_edges(self):
        """Graphe sans arêtes => VCB doit renvoyer True si k>=0."""
        G = nx.Graph()
        G.add_nodes_from(range(5))
        # 0 edges
        self.assertTrue(vcb_recursive(G, 0))
        self.assertTrue(vcb_recursive(G, 2))

    def test_vcb_complete_graph(self):
        """K4 => cover min=3 => on teste vcb pour k=2 et k=3."""
        G = nx.complete_graph(4)
        # si k=2 => impossible => vcb => False
        self.assertFalse(vcb_recursive(G, 2))
        # si k=3 => possible => True
        self.assertTrue(vcb_recursive(G, 3))

    def test_vcb_line_graph(self):
        """Ligne à 5 sommets => cover min=2."""
        G = nx.Graph()
        G.add_edges_from([(1,2),(2,3),(3,4),(4,5)])
        # min cover=2 (ex: {2,4})
        self.assertTrue(vcb_recursive(G, 2))
        # si k=1 => insuffisant => False
        self.assertFalse(vcb_recursive(G, 1))

if __name__ == "__main__":
    unittest.main()
