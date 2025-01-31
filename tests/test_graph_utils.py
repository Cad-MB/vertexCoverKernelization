import unittest
import networkx as nx
from src.graph_utils import remove_isolated_vertices, is_vertex_cover


class TestGraphUtils(unittest.TestCase):
    """
    Suite de tests unitaires pour les fonctions utilitaires sur les graphes.
    """

    def test_remove_isolated_vertices(self):
        """
        Vérifie que la suppression des sommets isolés fonctionne correctement.
        Après suppression, seuls les sommets connectés par une arête doivent rester.
        """
        g = nx.Graph()
        g.add_nodes_from([1, 2, 3, 4])  # Ajout de sommets isolés
        g.add_edge(1, 2)  # Seuls 1 et 2 sont connectés

        remove_isolated_vertices(g)

        # Seuls les sommets 1 et 2 doivent rester après suppression des isolés
        self.assertEqual(set(g.nodes()), {1, 2})

    def test_is_vertex_cover_empty(self):
        """
        Vérifie qu'un ensemble vide est un vertex cover valide pour un graphe vide.
        """
        g = nx.Graph()
        self.assertTrue(is_vertex_cover(g, set()))

    def test_is_vertex_cover_complete(self):
        """
        Vérifie le fonctionnement de la vérification du vertex cover sur un graphe complet.
        - Un ensemble de deux sommets doit couvrir un graphe complet de 3 sommets.
        - Un seul sommet ne suffit pas à couvrir toutes les arêtes.
        """
        g = nx.complete_graph(3)

        # {0, 1} doit être un vertex cover valide
        self.assertTrue(is_vertex_cover(g, {0, 1}))

        # {0} seul ne couvre pas toutes les arêtes du graphe complet
        self.assertFalse(is_vertex_cover(g, {0}))
