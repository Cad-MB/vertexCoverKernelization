import unittest
import networkx as nx
from src.reduction_rules import high_degree_rule


class TestReductionRules(unittest.TestCase):
    """
    Suite de tests unitaires pour les règles de réduction appliquées au problème du Vertex Cover.
    """

    def test_high_degree_empty(self):
        """
        Vérifie le comportement de la règle des sommets de haut degré sur un graphe vide.
        - La valeur de k ne doit pas être modifiée.
        - Le graphe doit rester vide après l'application de la règle.
        """
        g = nx.Graph()
        k = high_degree_rule(g, 2)
        self.assertEqual(k, 2)
        self.assertEqual(len(list(g.nodes())), 0)  # Vérification du nombre de sommets

    def test_high_degree_star(self):
        """
        Vérifie la règle des sommets de haut degré sur un graphe en étoile.
        - Le centre de l'étoile (degré > k) doit être supprimé.
        - La valeur de k doit être mise à jour en conséquence.
        - Le graphe doit conserver le bon nombre de sommets après réduction.
        """
        g = nx.star_graph(5)  # Un sommet central connecté à 5 feuilles
        k = high_degree_rule(g, 3)
        self.assertEqual(k, 2)
        self.assertEqual(len(set(g.nodes())), 5)  # Vérification de la taille du graphe

    def test_high_degree_complete(self):
        """
        Vérifie la règle des sommets de haut degré sur un graphe complet.
        - Tous les sommets ont un degré > k, ils doivent donc être supprimés.
        - La valeur de k doit devenir négative après suppression.
        - Le graphe doit être complètement vidé.
        """
        g = nx.complete_graph(4)  # Graphe complet à 4 sommets
        k = high_degree_rule(g, 2)
        self.assertEqual(k, -2)
        self.assertEqual(len(list(g.nodes())), 0)  # Vérification que le graphe est vide

    def test_high_degree_chain_reaction(self):
        """
        Vérifie l'effet de la règle de haut degré sur un graphe où la suppression
        d'un sommet entraîne des suppressions en cascade.
        - La suppression des sommets doit être correctement gérée.
        - La valeur de k doit être mise à jour en conséquence.
        """
        g = nx.Graph()
        g.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 3), (2, 4), (1, 4)])  # Graphe dense
        k = high_degree_rule(g, 2)
        self.assertEqual(k, -2)  # Vérification que la suppression a bien été appliquée