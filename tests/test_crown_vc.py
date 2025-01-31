import unittest
import networkx as nx

from src.crown_vc import kernel_vertex_cover_crown, is_vertex_cover


class TestCrownVC(unittest.TestCase):

    def test_empty_graph(self):
        """Graphe vide : aucun sommet, aucun edge => kernel trivial."""
        G = nx.Graph()
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        # Le graphe réduit doit rester vide, k ne change pas, pas de "no_instance"
        self.assertEqual(len(ker_graph.nodes()), 0)
        self.assertEqual(len(ker_graph.edges()), 0)
        self.assertEqual(ker_k, 2)
        self.assertFalse(no_inst)

    def test_isolated_vertices(self):
        """Graphe avec 3 sommets isolés => aucun edge => kernel trivial."""
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3])
        k = 1
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        # Tous les sommets étant isolés, on obtient un graphe réduit vide
        self.assertEqual(len(ker_graph.nodes()), 0)
        self.assertEqual(len(ker_graph.edges()), 0)
        self.assertEqual(ker_k, 1)
        self.assertFalse(no_inst)

    def test_simple_triangle(self):
        """Graphe triangle (3 sommets) => cover min = 2."""
        G = nx.Graph()
        edges = [(1, 2), (2, 3), (1, 3)]
        G.add_edges_from(edges)
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        # Vertex cover minimal = 2 ; la réduction ne devrait pas conclure "no" ni trop réduire
        self.assertFalse(no_inst)
        # On peut s'attendre à un kernel de taille <= 3k = 6 (k=2 => 6)
        self.assertTrue(len(ker_graph.nodes()) <= 6)
        # Vérifier que la couverture est correcte
        self.assertTrue(is_vertex_cover(G, ker_graph.nodes()))

    def test_line_graph(self):
        """
        Graphe en ligne de 5 sommets : 1-2-3-4-5
        Un vertex cover de taille 2 suffit : par exemple {2,4}.
        """
        G = nx.Graph()
        G.add_edges_from(nx.utils.pairwise([1, 2, 3, 4, 5]))  # edges = (1,2), (2,3), (3,4), (4,5)
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        # On attend un kernel avec <= 3*k=6 sommets => correct
        self.assertTrue(len(ker_graph.nodes()) <= 6)
        # Vérifier que la couverture est correcte
        self.assertTrue(is_vertex_cover(G, ker_graph.nodes()))
        self.assertTrue(ker_k >= 2)

    def test_disconnected_components(self):
        """Graphe à 2 composantes, dont l'une est déjà 'grosse', on vérifie la réduction."""
        G = nx.Graph()
        # composante 1 : triangle
        G.add_edges_from([(1, 2), (2, 3), (1, 3)])
        # composante 2 : un simple edge
        G.add_edge(4, 5)
        # composante 3 : 2 sommets isolés
        G.add_node(6)
        G.add_node(7)

        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        # Le kernel doit contenir au plus 3k=6 sommets (mais initialement 7, avec les isolés retirés)
        self.assertTrue(len(ker_graph.nodes()) <= 6)
        # Vérifier que la couverture est correcte
        self.assertTrue(is_vertex_cover(G, ker_graph.nodes()))

    def test_insufficient_k(self):
        """
        Graphe complet K4 => Le vertex cover min = 3.
        Si on donne k=2, on ne peut pas couvrir K4 => no_instance doit être True.
        """
        G = nx.complete_graph(4)  # K4
        k = 2
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertTrue(no_inst)

    def test_sufficient_k(self):
        """
        Graphe complet K4 => Le vertex cover min = 3.
        Si on donne k=3, on peut couvrir K4 => no_instance doit être False.
        """
        G = nx.complete_graph(4)  # K4
        k = 3
        ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
        self.assertFalse(no_inst)
        # kernel <= 3*k=9 sommets => correct
        self.assertTrue(len(ker_graph.nodes()) <= 9)
        # Vérifier que la couverture est correcte
        self.assertTrue(is_vertex_cover(G, ker_graph.nodes()))
        self.assertTrue(ker_k >= 3)


if __name__ == "__main__":
    unittest.main()
