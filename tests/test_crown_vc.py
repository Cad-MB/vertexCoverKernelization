#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests unitaires pour la réduction par décomposition en couronne (k-Vertex Cover)
et l'algorithme VCB associé.
"""

import unittest
import networkx as nx

from src.crown_vc import kernel_vertex_cover_crown, vcb_recursive


class TestCrownVC(unittest.TestCase):

    def test_empty_graph(self):
        """Graphe vide : pas d'arêtes => tout cover convient => kernel trivial."""
        G = nx.Graph()
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst, "Graphe vide => pas de contradiction (no_inst=False).")
        # Le graphe réduit devrait être vide
        self.assertEqual(len(ker_graph.nodes()), 0)
        self.assertEqual(len(ker_graph.edges()), 0)
        self.assertEqual(ker_k, k)

        # Vérif algo VCB
        self.assertTrue(vcb_recursive(G, k))

    def test_isolated_vertices(self):
        """Graphe avec 3 sommets isolés => aucun edge => kernel trivial."""
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3])
        k = 1
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        self.assertEqual(ker_graph.number_of_nodes(), 0)
        self.assertEqual(ker_k, 1)
        self.assertTrue(vcb_recursive(G, k))

    def test_triangle_cover_2(self):
        """Triangle complet => cover min = 2. On teste k=2."""
        G = nx.Graph()
        edges = [(1, 2), (2, 3), (1, 3)]
        G.add_edges_from(edges)
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        # Le kernel doit être de taille <= 3*k = 6.
        self.assertLessEqual(ker_graph.number_of_nodes(), 6)
        # Contrôle final via VCB
        self.assertTrue(vcb_recursive(ker_graph, ker_k))
        # On vérifie par brute force que la cover est de taille 2 possible
        # => l'algo VCB doit renvoyer True
        self.assertTrue(vcb_recursive(G, k))

    def test_line_graph_cover(self):
        """Graphe en ligne de 5 sommets (1-2-3-4-5). Un cover de taille 2 (ex: {2,4})."""
        G = nx.Graph()
        G.add_edges_from([(1,2),(2,3),(3,4),(4,5)])
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        self.assertTrue(ker_graph.number_of_nodes() <= 3*k)
        self.assertTrue(vcb_recursive(G, k))

    def test_disconnected_components(self):
        """Graphe avec composante triangle + composante arête + isolés."""
        G = nx.Graph()
        # Triangle
        G.add_edges_from([(1, 2), (2, 3), (1, 3)])
        # Simple arête
        G.add_edge(4, 5)
        # Isolés
        G.add_node(6)
        G.add_node(7)
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        self.assertTrue(ker_graph.number_of_nodes() <= 3*k)

    def test_insufficient_k(self):
        """K4 complet => cover min = 3. Si k=2 => NO-instance."""
        G = nx.complete_graph(4)
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertTrue(no_inst)

    def test_sufficient_k(self):
        """K4 complet => cover min = 3. Si k=3 => OK."""
        G = nx.complete_graph(4)
        k = 3
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        self.assertTrue(ker_graph.number_of_nodes() <= 3*k)
        # Vérif que c'est faisable
        self.assertTrue(vcb_recursive(ker_graph, ker_k))

    def test_vcb_random_small(self):
        """Petit test sur un graphe aléatoire."""
        import random
        random.seed(42)
        G = nx.gnm_random_graph(6, 8)
        # On ne sait pas a priori la taille min du cover
        # On teste juste que l'algo VCB s'exécute (pas un test strict).
        self.assertIn(vcb_recursive(G, 3), [True, False])


if __name__ == "__main__":
    unittest.main()
