# src/graph_gen.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module 'graph_gen' :
Contient des fonctions utilitaires pour générer des graphes aléatoires
et vérifier un vertex cover.
"""

import networkx as nx
import random

def generate_random_graph(n: int, m: int) -> nx.Graph:
    """
    Génére un graphe aléatoire G(n,m) uniformément.
    """
    return nx.gnm_random_graph(n, m, seed=None)


def generate_vertex_cover_graph(n: int, k: int, edge_prob: float = 0.5) -> nx.Graph:
    """
    Génère un graphe avec un cover imposé de taille k (avec forte prob).
    """
    G = nx.Graph()
    G.add_nodes_from(range(n))
    cover = set(random.sample(range(n), min(k, n)))
    for i in range(n):
        for j in range(i+1, n):
            if (i in cover) or (j in cover):
                if random.random() < edge_prob:
                    G.add_edge(i, j)
    return G


def is_vertex_cover(G: nx.Graph, cover_set) -> bool:
    """
    Vérifie si cover_set couvre toutes les arêtes de G.
    """
    c = set(cover_set)
    for (u, v) in G.edges():
        if u not in c and v not in c:
            return False
    return True
