import unittest
import networkx as nx
from src.kernel import crown_reduction, kernel_vertex_cover_crown


class TestKernel(unittest.TestCase):
    def test_crown_reduction_empty(self):
        G = nx.Graph()
        ker_G, ker_k, no_inst = crown_reduction(G, 2)
        self.assertFalse(no_inst)
        self.assertEqual(ker_k, 2)
        self.assertEqual(len(ker_G.nodes()), 0)

    def test_crown_reduction_path(self):
        G = nx.path_graph(5)
        ker_G, ker_k, no_inst = crown_reduction(G, 2)
        self.assertFalse(no_inst)
        self.assertLessEqual(len(ker_G.nodes()), 3 * ker_k)

    def test_crown_reduction_complete(self):
        G = nx.complete_graph(5)
        ker_G, ker_k, no_inst = crown_reduction(G, 2)
        self.assertTrue(no_inst)  # No VC of size 2 possible

    def test_kernel_vertex_cover_crown(self):
        # Test cases from original test file
        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3), (1, 3)])  # Triangle
        G.add_edge(4, 5)  # Extra edge
        G.add_nodes_from([6, 7])  # Isolated vertices

        ker_G, ker_k, no_inst = kernel_vertex_cover_crown(G, 2)
        self.assertFalse(no_inst)
        self.assertTrue(ker_G.number_of_nodes() <= 3 * ker_k)

    def test_crown_reduction_star(self):
        G = nx.star_graph(7)  # Centre + 7 feuilles
        ker_G, ker_k, no_inst = crown_reduction(G, 2)
        self.assertFalse(no_inst)
        self.assertLessEqual(ker_G.number_of_nodes(), 1)

    def test_kernel_on_cycle(self):
        G = nx.cycle_graph(6)
        ker_G, ker_k, no_inst = kernel_vertex_cover_crown(G, 3)
        self.assertFalse(no_inst)
        self.assertLessEqual(ker_G.number_of_nodes(), 9)  # 3*k

