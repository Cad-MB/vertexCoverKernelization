import networkx as nx


def vcb_recursive(G: nx.Graph, k: int) -> bool:
    """
    Vertex Cover Branch algorithm.
    Returns True if G has a vertex cover of size <= k.
    """
    if k < 0:
        return False
    if G.number_of_edges() == 0:
        return True
    if k == 0:
        return (G.number_of_edges() == 0)

    u, v = next(iter(G.edges()))

    G1 = G.copy()
    G1.remove_node(u)
    if vcb_recursive(G1, k - 1):
        return True

    G2 = G.copy()
    G2.remove_node(v)
    return vcb_recursive(G2, k - 1)
