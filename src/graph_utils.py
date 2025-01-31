import networkx as nx


def remove_isolated_vertices(G: nx.Graph):
    """Removes isolated vertices from graph G."""
    isolated = list(nx.isolates(G))
    G.remove_nodes_from(isolated)


def is_vertex_cover(G: nx.Graph, cover_set) -> bool:
    """
    Checks if cover_set is a valid vertex cover for G.
    Returns True if every edge has at least one endpoint in cover_set.
    """
    covered_edges = 0
    total_edges = G.number_of_edges()
    cover_set = set(cover_set)

    for (u, v) in G.edges():
        if (u in cover_set) or (v in cover_set):
            covered_edges += 1
    return (covered_edges == total_edges)