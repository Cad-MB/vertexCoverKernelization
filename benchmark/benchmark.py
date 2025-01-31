#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de comparaison des temps d'exécution entre:
- (Kernelization + VCB) sur un noyau de taille <= 3k
- VCB seul (sans prétraitement Crown Decomposition)

Instances générées aléatoirement, on précise la méthode de génération:
  -> generate_vertex_cover_graph() :
      * on choisit aléatoirement k sommets pour faire un "cover imposé"
      * les arêtes ont une certaine probabilité d'exister si elles touchent ce cover
  -> (optionnel) generate_random_graph() : un G(n,m) purement aléatoire

La bibliothèque NetworkX est utilisée pour construire et manipuler les graphes.
"""

import time
import random
import pandas as pd
import matplotlib.pyplot as plt

from src.crown_vc import generate_vertex_cover_graph, vcb_recursive, kernel_vertex_cover_crown


# Si vous avez un package src/:
# from src.crown_vc import generate_vertex_cover_graph, vcb_recursive, kernel_vertex_cover_crown
# Sinon, si crown_vc.py est dans le même dossier:

def benchmark_random_graphs(n_values, k_values, edge_prob=0.1, nb_runs=3):
    """
    Pour chaque (n, k), on génère un graphe "vertex-cover-likely" via generate_vertex_cover_graph,
    puis on mesure le temps d'exécution de:
      (1) kernel + vcb sur le kernel
      (2) vcb seul (sans kernel)

    On effectue nb_runs répétitions et on moyenne les temps.

    Paramètres
    ----------
    n_values : list of int
        Liste des tailles de graphes (nombre de sommets) à tester
    k_values : list of int
        Liste des paramètres k à tester
    edge_prob : float
        Probabilité d'ajouter une arête entre les sommets éligibles dans generate_vertex_cover_graph
    nb_runs : int
        Nombre de répétitions pour chaque (n, k) afin de moyenner les temps

    Retourne
    --------
    df : pd.DataFrame
        Un DataFrame contenant les colonnes:
           "n", "k", "Time (Kernel+VCB)", "Time (VCB alone)"

    Remarques
    ---------
    - La fonction generate_vertex_cover_graph(n, k, edge_prob) crée un graphe
      qui a de fortes chances (mais pas certitude) d'avoir un VC <= k.
    - Vous pouvez aussi tester d'autres méthodes (p.ex. generate_random_graph(n, m)).
    """
    results = []
    for n in n_values:
        for k in k_values:
            # Si k > n, tester n'a pas de sens. On peut ignorer ou continuer.
            if k > n:
                continue

            total_ker_time = 0.0
            total_vcb_time = 0.0

            for _ in range(nb_runs):
                # Générez un graphe aléatoire
                G = generate_vertex_cover_graph(n, k, edge_prob=edge_prob)

                # Mesure temps: Kernelization + VCB
                start = time.time()
                ker_G, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
                if not no_inst:
                    _ = vcb_recursive(ker_G, ker_k)
                end = time.time()
                total_ker_time += (end - start)

                # Mesure temps: VCB seul
                start = time.time()
                _ = vcb_recursive(G, k)
                end = time.time()
                total_vcb_time += (end - start)

            # Moyennes
            avg_ker = total_ker_time / nb_runs
            avg_vcb = total_vcb_time / nb_runs
            results.append((n, k, avg_ker, avg_vcb))

    df = pd.DataFrame(results, columns=["n", "k", "Time (Kernel+VCB)", "Time (VCB alone)"])
    return df


def main():
    """
    Exemple : on compare sur n dans [50, 100, 150, 200]
              k dans [5, 10, 15, 20]
    On trace ensuite le temps d'exécution pour k=10.
    """
    random.seed(42)  # Optionnel, pour reproductibilité
    n_values = [50, 100, 150, 200]
    k_values = [5, 10, 15, 20]

    # Lancement du benchmark
    df = benchmark_random_graphs(n_values, k_values, edge_prob=0.05, nb_runs=3)
    print("Résultats :\n", df)

    # Ex: tracer pour k=10
    df_k10 = df[df["k"] == 10]
    plt.figure(figsize=(8, 5))
    plt.plot(df_k10["n"], df_k10["Time (Kernel+VCB)"], 'o-', label="Kernel + VCB")
    plt.plot(df_k10["n"], df_k10["Time (VCB alone)"], 'o-', label="VCB seul")
    plt.xlabel("Nombre de sommets (n)")
    plt.ylabel("Temps moyen (s)")
    plt.title("Comparaison temps pour k=10 (nb_runs=3)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
