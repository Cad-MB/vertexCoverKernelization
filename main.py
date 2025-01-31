# main.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple d'utilisation du module crown_vc :
1) Création d'un petit graphe
2) Kernelization + test
3) VCB direct
"""

import networkx as nx
from src.crown_vc import (
    kernel_vertex_cover_crown,
    vcb_recursive
)

if __name__ == "__main__":
    # Exemple
    G_ex = nx.Graph()
    edges_ex = [(1,2),(2,3),(3,4),(2,4),(4,5)]
    G_ex.add_edges_from(edges_ex)
    K = 2

    print("Graphe exemple =", G_ex.edges())
    ker_graph, ker_k, no_inst = kernel_vertex_cover_crown(G_ex, K)
    if no_inst:
        print("Réponse : NON (pas de vertex cover de taille <= K).")
    else:
        print("Graphe réduit (kernel) :", ker_graph.nodes(), ker_graph.edges())
        print("Nouveau k :", ker_k)
        vcb_res = vcb_recursive(ker_graph, ker_k)
        print("=> Test VCB sur kernel :", vcb_res)

    direct_res = vcb_recursive(G_ex, K)
    print("=> Test VCB sans kernel :", direct_res)