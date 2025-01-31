# tests/test_reduction.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests unitaires centrés sur la réduction/kernélisation via crown decomposition.
Ici, on se focalise sur 'kernel_vertex_cover_crown' et les règles associées.
"""

import unittest
import networkx as nx

from src.reduction import kernel_vertex_cover_crown
from src.fpt import vcb_recursive  # on l'importe éventuellement pour vérifier le kernel

class TestCrownReduction(unittest.TestCase):

    def test_empty_graph(self):
        """Graphe vide => kernel trivial, no_instance=False."""
        G = nx.Graph()
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        self.assertEqual(ker_graph.number_of_nodes(), 0)
        self.assertEqual(ker_graph.number_of_edges(), 0)
        self.assertEqual(ker_k, 2)
        # Vérification via VCB (optionnel)
        self.assertTrue(vcb_recursive(G, k))

    def test_isolated_vertices(self):
        """3 sommets isolés => kernel trivial."""
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3])
        k = 1
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        self.assertEqual(ker_graph.number_of_nodes(), 0)
        self.assertEqual(ker_k, 1)
        self.assertTrue(vcb_recursive(G, k))

    def test_triangle_cover_2(self):
        """Triangle complet => cover min=2 => on teste k=2."""
        G = nx.Graph()
        edges = [(1,2),(2,3),(1,3)]
        G.add_edges_from(edges)
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        # Le kernel doit être de taille <= 3*k
        self.assertLessEqual(ker_graph.number_of_nodes(), 6)
        # Vérification via VCB
        self.assertTrue(vcb_recursive(ker_graph, ker_k))

    def test_line_graph_cover(self):
        """Graphe en ligne (5 sommets) => on teste la réduction."""
        G = nx.Graph()
        G.add_edges_from([(1,2),(2,3),(3,4),(4,5)])
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        self.assertTrue(ker_graph.number_of_nodes() <= 3*k)
        self.assertTrue(vcb_recursive(G, k))

    def test_disconnected_components(self):
        """Graphe avec composante triangle + arête + isolés => on teste le kernel."""
        G = nx.Graph()
        G.add_edges_from([(1,2),(2,3),(1,3)])
        G.add_edge(4,5)
        G.add_node(6)
        G.add_node(7)
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        self.assertTrue(ker_graph.number_of_nodes() <= 3*k)

    def test_insufficient_k(self):
        """K4 => cover min=3. Si k=2 => no_instance=True."""
        G = nx.complete_graph(4)
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertTrue(no_inst)

    def test_sufficient_k(self):
        """K4 => cover min=3, k=3 => OK."""
        G = nx.complete_graph(4)
        k = 3
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        self.assertTrue(ker_graph.number_of_nodes() <= 3*k)
        self.assertTrue(vcb_recursive(ker_graph, ker_k))


if __name__ == "__main__":
    unittest.main()
