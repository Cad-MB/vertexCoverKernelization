import random
import networkx as nx


def generate_random_graph(n: int, m: int) -> nx.Graph:
    """
    Generates random graph with n vertices and m edges.
    Uses NetworkX's G(n,m) random graph model.
    """
    return nx.gnm_random_graph(n, m, seed=None)


def generate_vertex_cover_graph(n: int, k: int, edge_prob: float = 0.5, guaranteed_vc: bool = False) -> nx.Graph:
    """
    Génère un graphe aléatoire ayant (avec forte probabilité) un vertex cover de taille <= k.
    Si guaranteed_vc=True, force la construction pour garantir un vertex-cover de taille k.

    Parameters
    ----------
    n : int
        Nombre total de sommets
    k : int
        Taille du cover souhaité
    edge_prob : float
        Probabilité d'ajouter une arête entre deux sommets autorisés
    guaranteed_vc : bool
        Si True, garantit un vertex-cover de taille k
    """
    G = nx.Graph()
    G.add_nodes_from(range(n))

    # Choisir k sommets qui formeront le cover
    cover = set(random.sample(range(n), min(k, n)))

    if guaranteed_vc:
        # Pour garantir que cover est un vertex-cover minimal:
        # 1. Ajout d'arêtes entre sommets hors cover et sommets du cover
        non_cover = set(range(n)) - cover
        for u in non_cover:
            # Chaque sommet hors cover doit être relié à au moins un sommet du cover
            v = random.choice(list(cover))
            G.add_edge(u, v)

            # Ajouter d'autres arêtes aléatoirement
            for v in cover:
                if random.random() < edge_prob:
                    G.add_edge(u, v)
    else:
        # Version originale: arêtes aléatoires touchant le cover
        nodes = list(range(n))
        for i in range(n):
            for j in range(i + 1, n):
                if (i in cover) or (j in cover):
                    if random.random() < edge_prob:
                        G.add_edge(i, j)

    return G