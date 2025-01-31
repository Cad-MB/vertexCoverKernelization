import networkx as nx
from .graph_utils import remove_isolated_vertices
from .reduction_rules import high_degree_rule
from .crown_decomp import crown_decomposition


def crown_reduction(G: nx.Graph, k: int):
    """
    Applies crown reduction rules iteratively until either:
    - Graph size <= 3k (kernel found)
    - No more reductions possible
    - Definitely no k-vertex cover exists
    """
    G = G.copy()
    while True:
        remove_isolated_vertices(G)
        k = high_degree_rule(G, k)
        if k < 0:
            return None, 0, True

        if G.number_of_nodes() <= 3 * k:
            return G, k, False

        C, H, no_inst = crown_decomposition(G, k)
        if no_inst:
            return None, 0, True
        if C is None:
            return G, k, False

        G.remove_nodes_from(C)
        k -= len(H)
        if k < 0:
            return None, 0, True


def kernel_vertex_cover_crown(G: nx.Graph, k: int):
    """
    Main kernelization function.
    Returns (kernel_graph, new_k, no_instance).
    """
    return crown_reduction(G, k)