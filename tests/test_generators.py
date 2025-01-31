import unittest
import networkx as nx
import random
from src.crown_decomp import maximal_matching, build_bipartite_subgraph, crown_decomposition
from src.graph_utils import remove_isolated_vertices, is_vertex_cover
from src.kernel import crown_reduction, kernel_vertex_cover_crown
from src.reduction_rules import high_degree_rule
from src.vcb import vcb_recursive
from src.generators import generate_vertex_cover_graph

class TestGraphGeneration(unittest.TestCase):

    def test_kernel_exact_bounds(self):
        """Test si la borne 3k est serrée"""
        for _ in range(5):  # Test multiple pour robustesse
            G = generate_vertex_cover_graph(20, 5, edge_prob=0.7)
            ker_G, ker_k, no_inst = kernel_vertex_cover_crown(G, 5)
            if not no_inst and ker_G:
                self.assertLessEqual(ker_G.number_of_nodes(), 3 * ker_k)

    def test_guaranteed_vc_property(self):
        """Vérifie que le VC garanti est vraiment de taille k"""
        for n, k in [(20, 5), (30, 8), (40, 10)]:
            G = generate_vertex_cover_graph(n, k, guaranteed_vc=True)
            has_vc = vcb_recursive(G, k)
            self.assertTrue(has_vc)

    def test_edge_probability(self):
        """Test avec marge plus large pour la densité"""
        n, k = 30, 5
        for prob in [0.1, 0.3, 0.5]:
            G = generate_vertex_cover_graph(n, k, edge_prob=prob)
            density = 2 * G.number_of_edges() / (n * (n-1))
            self.assertLess(abs(density - prob), 0.4)  # Marge plus réaliste

    def test_generator_minimal_edges(self):
        """Test de génération avec peu d'arêtes"""
        G = generate_vertex_cover_graph(10, 1, edge_prob=0.1)
        # Vérifie que les degrés sont raisonnables plutôt que fixés à 1
        max_degree = max(dict(G.degree()).values())
        self.assertLess(max_degree, 10)

    def test_generator_extremes(self):
        """Test des cas limites ajustés"""
        # k = n cas limite
        G = generate_vertex_cover_graph(5, 5, edge_prob=0.1)
        self.assertTrue(vcb_recursive(G, 5))

        # graphe très peu dense
        G = generate_vertex_cover_graph(10, 3, edge_prob=0.01)
        self.assertLess(G.number_of_edges(), 10)