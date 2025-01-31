import random

import networkx as nx


def generate_random_graph(n: int, m: int) -> nx.Graph:
    """
    Génère un graphe aléatoire de n sommets et m arêtes.
    Utilise le modèle G(n, m) de NetworkX pour créer un graphe aléatoire avec un nombre
    d'arêtes fixe.

    Paramètres
    ----------
    n : int
        Nombre total de sommets dans le graphe.
    m : int
        Nombre total d'arêtes à inclure dans le graphe.

    Retourne
    --------
    nx.Graph
        Un graphe aléatoire non orienté contenant n sommets et m arêtes.
    """
    return nx.gnm_random_graph(n, m, seed=None)


def generate_vertex_cover_graph(n: int, k: int, edge_prob: float = 0.5, guaranteed_vc: bool = False) -> nx.Graph:
    """
    Génère un graphe aléatoire ayant (avec forte probabilité) un vertex cover de taille ≤ k.
    Si `guaranteed_vc` est activé, la structure du graphe est modifiée pour assurer l'existence
    d'un vertex cover de taille exactement k.

    Paramètres
    ----------
    n : int
        Nombre total de sommets dans le graphe.
    k : int
        Taille maximale du vertex cover souhaité.
    edge_prob : float, optionnel (par défaut 0.5)
        Probabilité d'ajouter une arête entre deux sommets admissibles.
    guaranteed_vc : bool, optionnel (par défaut False)
        Si True, assure la construction d'un vertex cover de taille k en forçant les connexions.

    Retourne
    --------
    nx.Graph
        Un graphe non orienté généré selon les critères spécifiés.
    """
    g = nx.Graph()
    g.add_nodes_from(range(n))

    # Sélection aléatoire de k sommets qui formeront le vertex cover
    cover = set(random.sample(range(n), min(k, n)))

    if guaranteed_vc:
        # Assurer que le vertex cover est bien de taille k :
        # 1. Chaque sommet hors du cover est connecté à au moins un sommet du cover.
        non_cover = set(range(n)) - cover
        for u in non_cover:
            # Connexion obligatoire à un sommet du cover pour garantir un recouvrement
            v = random.choice(list(cover))
            g.add_edge(u, v)

            # Ajout d'arêtes supplémentaires aléatoires entre le sommet hors cover et d'autres sommets du cover
            for v in cover:
                if random.random() < edge_prob:
                    g.add_edge(u, v)
    else:
        # Version sans garantie stricte du vertex cover : arêtes générées de manière aléatoire
        list(range(n))
        for i in range(n):
            for j in range(i + 1, n):
                # On favorise les connexions impliquant des sommets du vertex cover
                if (i in cover) or (j in cover):
                    if random.random() < edge_prob:
                        g.add_edge(i, j)

    return g
