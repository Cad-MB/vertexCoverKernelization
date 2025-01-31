# src/reduction.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module 'reduction' :
Contient les fonctions de réduction pour le k-Vertex Cover :
- remove_isolated_vertices
- high_degree_rule
- crown_decomposition + crown_reduction
- kernel_vertex_cover_crown
"""

import networkx as nx
from networkx.algorithms import bipartite
import random

def remove_isolated_vertices(G: nx.Graph):
    """
    Supprime les sommets isolés (degré 0).
    """
    isolated = list(nx.isolates(G))
    G.remove_nodes_from(isolated)


def high_degree_rule(G: nx.Graph, k: int) -> int:
    """
    Règle : si un sommet a un degré > k, il doit être dans le vertex cover.
    On le retire et on décrémente k.
    """
    degs = dict(G.degree())
    changed = True
    while changed:
        changed = False
        for v in list(G.nodes()):
            if degs[v] > k:
                G.remove_node(v)
                k -= 1
                changed = True
                break
        if changed:
            degs = dict(G.degree())
    return k


def maximal_matching(G: nx.Graph):
    """
    Trouve un couplage glouton maximal (non-maximum).
    """
    M = []
    used = set()
    for u in G.nodes():
        if u not in used:
            for v in G.neighbors(u):
                if v not in used:
                    M.append((u, v))
                    used.add(u)
                    used.add(v)
                    break
    return M


def build_bipartite_subgraph(G: nx.Graph, matched: set, unmatched: set):
    """
    Construit un sous-graphe biparti entre matched et unmatched.
    """
    B = nx.Graph()
    B.add_nodes_from(matched, bipartite=0)
    B.add_nodes_from(unmatched, bipartite=1)
    for u in matched:
        for v in G[u]:
            if v in unmatched:
                B.add_edge(u, v)
    return B


def crown_decomposition(G: nx.Graph, k: int):
    """
    Tente de trouver (C, H, R) via la décomposition en couronne.
    Retourne (C, H, no_instance).
    """
    M = maximal_matching(G)
    if len(M) > k:
        return None, None, True  # pas de VC <= k

    matched = set()
    for (u, v) in M:
        matched.add(u)
        matched.add(v)

    unmatched = set(G.nodes()) - matched
    B = build_bipartite_subgraph(G, matched, unmatched)

    # Cherche un unmatched isolé dans B => couronne triviale
    for x in unmatched:
        neigh = set(B[x])
        if len(neigh) == 0:
            return {x}, set(), False

    # Sinon pas trouvé => None
    return None, None, False


def crown_reduction(G: nx.Graph, k: int):
    """
    Applique itérativement :
     - remove_isolated_vertices
     - high_degree_rule
     - si |V| <= 3k => stop
     - crown_decomposition => si trouvé => supprime C, k -= |H|
    Retourne (kernel_graph, new_k, no_instance).
    """
    G = G.copy()
    while True:
        remove_isolated_vertices(G)
        k = high_degree_rule(G, k)
        if k < 0:
            return None, 0, True

        if G.number_of_nodes() <= 3*k:
            return G, k, False

        C, H, no_inst = crown_decomposition(G, k)
        if no_inst:
            return None, 0, True
        if C is None:
            # pas de couronne => stop
            return G, k, False
        # Réduction
        G.remove_nodes_from(C)
        k -= len(H)
        if k < 0:
            return None, 0, True


def kernel_vertex_cover_crown(G: nx.Graph, k: int):
    """
    Kernel principal :
    Retourne (kernel, new_k, no_instance).
    """
    return crown_reduction(G, k)
