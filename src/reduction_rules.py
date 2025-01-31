import networkx as nx


def high_degree_rule(G: nx.Graph, k: int) -> int:
    """
    Applies high degree reduction rule: if vertex v has degree > k,
    it must be in any k-vertex cover, so remove it and decrement k.

    Parameters
    ----------
    G : nx.Graph
        Input graph (modified in place)
    k : int
        Current parameter value

    Returns
    -------
    new_k : int
        Updated parameter value after reductions
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