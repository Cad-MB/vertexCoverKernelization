import networkx as nx
from networkx.algorithms import bipartite

def maximal_matching(G: nx.Graph):
    """
    Finds a maximal matching in G greedily.
    Returns list of (u,v) edges in the matching.
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

def build_bipartite_subgraph(G: nx.Graph, matched_vertices: set, unmatched: set):
    """
    Builds bipartite subgraph from matched and unmatched vertices.
    matched_vertices will be part 0, unmatched will be part 1.
    Only keeps edges between the two parts.
    """
    B = nx.Graph()
    B.add_nodes_from(matched_vertices, bipartite=0)
    B.add_nodes_from(unmatched, bipartite=1)
    for u in matched_vertices:
        for v in G[u]:
            if v in unmatched:
                B.add_edge(u, v)
    return B

def crown_decomposition(G: nx.Graph, k: int):
    """
    Attempts to find crown decomposition (C, H, R) of graph G.
    Returns (C, H, is_no_instance) where:
    - C is the crown (independent set)
    - H is the head
    - is_no_instance is True if definitely no k-vertex cover exists
    """
    M = maximal_matching(G)
    if len(M) > k:
        return None, None, True

    matched_vertices = set()
    for (u, v) in M:
        matched_vertices.add(u)
        matched_vertices.add(v)

    unmatched = set(G.nodes()) - matched_vertices

    B = build_bipartite_subgraph(G, matched_vertices, unmatched)

    match_dict = {}
    try:
        for component in nx.connected_components(B):
            sub = B.subgraph(component)
            if not sub.nodes():
                continue
            top, _ = bipartite.sets(sub)
            matching_sub = bipartite.maximum_matching(sub, top_nodes=top)
            match_dict.update(matching_sub)
    except nx.AmbiguousSolution:
        pass

    for x in unmatched:
        neigh = set(B[x])
        if len(neigh) == 0:
            C = {x}
            H = set()
            return C, H, False

    return None, None, False