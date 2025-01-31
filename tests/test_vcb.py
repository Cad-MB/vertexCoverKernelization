import unittest
import networkx as nx
from src.vcb import vcb_recursive


class TestVCB(unittest.TestCase):
    """
    Suite de tests unitaires pour l'algorithme récursif de Vertex Cover Branching (VCB).
    """

    def test_vcb_empty(self):
        """
        Vérifie le comportement de l'algorithme sur un graphe vide.
        - Un graphe sans arêtes possède toujours un vertex cover de taille 0.
        - L'algorithme doit aussi accepter toute valeur de k ≥ 0.
        """
        g = nx.Graph()
        self.assertTrue(vcb_recursive(g, 0))
        self.assertTrue(vcb_recursive(g, 1))

    def test_vcb_single_edge(self):
        """
        Vérifie le fonctionnement sur un graphe avec une seule arête.
        - Un vertex cover de taille 0 est impossible.
        - Un vertex cover de taille 1 est toujours suffisant.
        """
        g = nx.Graph([(0, 1)])
        self.assertFalse(vcb_recursive(g, 0))
        self.assertTrue(vcb_recursive(g, 1))

    def test_vcb_triangle(self):
        """
        Vérifie le comportement sur un graphe formant un triangle (clique de 3 sommets).
        - Un seul sommet ne peut pas couvrir toutes les arêtes.
        - Deux sommets suffisent pour couvrir toutes les arêtes.
        """
        g = nx.Graph([(0, 1), (1, 2), (0, 2)])
        self.assertFalse(vcb_recursive(g, 1))
        self.assertTrue(vcb_recursive(g, 2))

    def test_vcb_path(self):
        """
        Vérifie le fonctionnement sur un graphe en chemin de 4 sommets.
        - Un vertex cover de taille 2 est suffisant.
        - Un vertex cover de taille 1 est insuffisant.
        """
        g = nx.path_graph(4)
        self.assertTrue(vcb_recursive(g, 2))
        self.assertFalse(vcb_recursive(g, 1))

    def test_vcb_cycle(self):
        """
        Vérifie le comportement sur un graphe cyclique.
        - Un cycle de n sommets nécessite au moins ⌈n/2⌉ sommets dans le vertex cover.
        """
        g = nx.cycle_graph(6)
        self.assertFalse(vcb_recursive(g, 2))  # ⌈6/2⌉ = 3 nécessaire
        self.assertTrue(vcb_recursive(g, 3))

    def test_vcb_bipartite(self):
        """
        Vérifie le fonctionnement sur un graphe biparti complet.
        - Un graphe K_{3,4} a un vertex cover de taille 3.
        - Un vertex cover de taille 2 est insuffisant.
        """
        g = nx.complete_bipartite_graph(3, 4)
        self.assertTrue(vcb_recursive(g, 3))
        self.assertFalse(vcb_recursive(g, 2))

    def test_vcb_disconnected(self):
        """
        Vérifie le comportement sur un graphe composé de plusieurs composantes déconnectées.
        - Un vertex cover doit couvrir toutes les arêtes de chaque composante.
        - Un k trop petit ne permet pas de couvrir toutes les arêtes.
        """
        g = nx.Graph()
        g.add_edges_from([(1, 2), (3, 4), (5, 6)])
        self.assertTrue(vcb_recursive(g, 3))  # Chaque arête requiert au moins un sommet dans le cover
        self.assertFalse(vcb_recursive(g, 2))  # 2 sommets ne suffisent pas pour 3 arêtes
