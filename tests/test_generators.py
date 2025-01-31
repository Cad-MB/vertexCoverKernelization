import unittest

from src.generators import generate_vertex_cover_graph
from src.kernel import kernel_vertex_cover_crown
from src.vcb import vcb_recursive


class TestGraphGeneration(unittest.TestCase):
    """
    Suite de tests unitaires pour la génération et la réduction de graphes
    dans le cadre du problème du Vertex Cover.
    """

    def test_kernel_exact_bounds(self):
        """
        Vérifie que la borne 3k est bien respectée après la kernelization.
        Un graphe réduit doit contenir au plus 3k sommets.
        """
        for _ in range(5):
            g = generate_vertex_cover_graph(20, 5, edge_prob=0.7)
            ker_g, ker_k, no_inst = kernel_vertex_cover_crown(g, 5)
            if not no_inst and ker_g:
                self.assertLessEqual(ker_g.number_of_nodes(), 3 * ker_k)

    def test_guaranteed_vc_property(self):
        """
        Vérifie que la génération d'un graphe avec un vertex cover garanti
        respecte bien la taille k spécifiée.
        """
        for n, k in [(20, 5), (30, 8), (40, 10)]:
            g = generate_vertex_cover_graph(n, k, guaranteed_vc=True)
            has_vc = vcb_recursive(g, k)
            self.assertTrue(has_vc)

    def test_edge_probability(self):
        """
        Vérifie que la probabilité d'ajout d'arêtes est respectée dans une
        marge d'erreur raisonnable.
        """
        n, k = 30, 5
        for prob in [0.1, 0.3, 0.5]:
            g = generate_vertex_cover_graph(n, k, edge_prob=prob)
            density = 2 * g.number_of_edges() / (n * (n - 1))
            self.assertLess(abs(density - prob), 0.4)

    def test_generator_minimal_edges(self):
        """
        Vérifie la génération d'un graphe avec très peu d'arêtes.
        S'assure qu'aucun sommet ne dépasse un degré maximal fixé.
        """
        g = generate_vertex_cover_graph(10, 1, edge_prob=0.1)
        max_degree = max(dict(g.degree()).values())
        self.assertLess(max_degree, 10)

    def test_generator_extremes(self):
        """
        Vérifie les cas limites de la génération de graphes :
        - Un graphe avec k = n devrait toujours avoir une couverture valide.
        - Un graphe avec très peu d'arêtes ne doit pas en contenir plus que n.
        """
        g = generate_vertex_cover_graph(5, 5, edge_prob=0.1)
        self.assertTrue(vcb_recursive(g, 5))

        g = generate_vertex_cover_graph(10, 3, edge_prob=0.01)
        self.assertLess(g.number_of_edges(), 10)
