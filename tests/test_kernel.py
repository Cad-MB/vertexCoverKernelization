import unittest
import networkx as nx
from src.kernel import crown_reduction, kernel_vertex_cover_crown


class TestKernel(unittest.TestCase):
    """
    Suite de tests unitaires pour les fonctions de réduction et de kernelization
    du problème du Vertex Cover.
    """

    def test_crown_reduction_empty(self):
        """
        Vérifie que la réduction en couronne fonctionne correctement sur un graphe vide.
        - L'instance ne doit pas être déclarée invalide.
        - La valeur de k ne doit pas être modifiée.
        - Le graphe réduit doit rester vide.
        """
        g = nx.Graph()
        ker_g, ker_k, no_inst = crown_reduction(g, 2)
        self.assertFalse(no_inst)
        self.assertEqual(ker_k, 2)
        self.assertEqual(len(ker_g.nodes()), 0)

    def test_crown_reduction_path(self):
        """
        Vérifie la réduction en couronne sur un graphe en chemin.
        - L'instance ne doit pas être invalide.
        - Le nombre de sommets après réduction doit être ≤ 3k.
        """
        g = nx.path_graph(5)
        ker_g, ker_k, no_inst = crown_reduction(g, 2)
        self.assertFalse(no_inst)
        self.assertLessEqual(len(ker_g.nodes()), 3 * ker_k)

    def test_crown_reduction_complete(self):
        """
        Vérifie la réduction en couronne sur un graphe complet.
        - Un graphe complet avec plus d'arêtes que k ne peut pas être réduit à un kernel.
        - L'instance doit être déclarée invalide.
        """
        g = nx.complete_graph(5)
        ker_g, ker_k, no_inst = crown_reduction(g, 2)
        self.assertTrue(no_inst)

    def test_kernel_vertex_cover_crown(self):
        """
        Vérifie la kernelization du Vertex Cover en appliquant la réduction en couronne.
        - Test sur un graphe mixte contenant un triangle, une arête isolée et des sommets isolés.
        - L'instance ne doit pas être déclarée invalide.
        - Le graphe réduit doit respecter la borne 3k.
        """
        g = nx.Graph()
        g.add_edges_from([(1, 2), (2, 3), (1, 3)])  # Triangle
        g.add_edge(4, 5)  # Arête isolée
        g.add_nodes_from([6, 7])  # Sommets isolés

        ker_g, ker_k, no_inst = kernel_vertex_cover_crown(g, 2)
        self.assertFalse(no_inst)
        self.assertTrue(ker_g.number_of_nodes() <= 3 * ker_k)

    def test_crown_reduction_star(self):
        """
        Vérifie la réduction en couronne sur un graphe en étoile.
        - L'instance ne doit pas être invalide.
        - Le graphe réduit ne doit contenir au plus qu'un seul sommet.
        """
        g = nx.star_graph(7)
        ker_g, ker_k, no_inst = crown_reduction(g, 2)
        self.assertFalse(no_inst)
        self.assertLessEqual(ker_g.number_of_nodes(), 1)

    def test_kernel_on_cycle(self):
        """
        Vérifie la kernelization sur un graphe cyclique.
        - L'instance ne doit pas être invalide.
        - Le graphe réduit doit contenir au plus 3k sommets.
        """
        g = nx.cycle_graph(6)
        ker_g, ker_k, no_inst = kernel_vertex_cover_crown(g, 3)
        self.assertFalse(no_inst)
        self.assertLessEqual(ker_g.number_of_nodes(), 9)
