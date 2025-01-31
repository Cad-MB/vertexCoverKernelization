# src/fpt.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module 'fpt' :
Contient l'algorithme de branchement (VCB) pour décider si un vertex cover <= k
existe dans un graphe.
"""

import networkx as nx

def vcb_recursive(G: nx.Graph, k: int) -> bool:
    """
    Algorithme VCB (variante branch & reduce).
    - k < 0 => False
    - plus d'arêtes => True
    - k=0 => True ssi pas d'arêtes
    - Sinon, on choisit une arête (u, v), on tente d'inclure u puis v.
    """
    if k < 0:
        return False
    if G.number_of_edges() == 0:
        return True
    if k == 0:
        # possible ssi pas d'arêtes
        return (G.number_of_edges() == 0)

    # On prend une arête
    (u, v) = next(iter(G.edges()))

    # Branch sur u
    G1 = G.copy()
    G1.remove_node(u)
    if vcb_recursive(G1, k - 1):
        return True

    # Branch sur v
    G2 = G.copy()
    G2.remove_node(v)
    return vcb_recursive(G2, k - 1)
