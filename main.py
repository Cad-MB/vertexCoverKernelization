#!/usr/bin/env python3
"""
Point d'entrée principal pour le projet k-Vertex Cover Kernelization.
Permet de :
1. Lancer un exemple simple
2. Exécuter les benchmarks
3. Générer des graphes tests
4. Démontrer l'utilisation des différentes fonctionnalités
"""

import argparse
import networkx as nx
import time

from src.kernel import kernel_vertex_cover_crown
from src.vcb import vcb_recursive
from src.generators import generate_vertex_cover_graph
from benchmark.benchmark import run_comprehensive_benchmarks, plot_detailed_results


def demo_simple_example():
    """Démontre l'utilisation sur un petit exemple."""
    global vcb_result
    print("\nDémonstration sur un petit graphe:")
    # Créer un petit graphe exemple (triangle + arête)
    g = nx.Graph()
    g.add_edges_from([(1, 2), (2, 3), (1, 3), (3, 4)])
    k = 2

    print(f"Graphe initial: {g.number_of_nodes()} sommets, {g.number_of_edges()} arêtes")

    # Test Kernel + VCB
    start = time.time()
    ker_g, ker_k, no_inst = kernel_vertex_cover_crown(g, k)
    if not no_inst:
        vcb_result = vcb_recursive(ker_g, ker_k)
    ker_time = time.time() - start

    print(f"\nKernel + VCB:")
    print(f"- Temps: {ker_time:.3f}s")
    if not no_inst:
        print(f"- Taille kernel: {ker_g.number_of_nodes()} sommets")
        print(f"- Résultat: {'Oui' if vcb_result else 'Non'}")
    else:
        print("- Pas de vertex cover de taille k possible")

    # Test VCB seul
    start = time.time()
    vcb_result = vcb_recursive(g, k)
    vcb_time = time.time() - start

    print(f"\nVCB seul:")
    print(f"- Temps: {vcb_time:.3f}s")
    print(f"- Résultat: {'Oui' if vcb_result else 'Non'}")


def demo_random_graph(n=30, k=8):
    """Démontre l'utilisation sur un graphe aléatoire."""
    global vcb_result
    print(f"\nDémonstration sur un graphe aléatoire (n={n}, k={k}):")
    g = generate_vertex_cover_graph(n, k, edge_prob=0.3)
    print(f"Graphe généré: {g.number_of_nodes()} sommets, {g.number_of_edges()} arêtes")

    # Test avec kernel
    start = time.time()
    ker_g, ker_k, no_inst = kernel_vertex_cover_crown(g, k)
    if not no_inst:
        vcb_result = vcb_recursive(ker_g, ker_k)
    ker_time = time.time() - start

    print(f"\nKernel + VCB:")
    print(f"- Temps: {ker_time:.3f}s")
    if not no_inst:
        print(f"- Taille kernel: {ker_g.number_of_nodes()} sommets")
        print(f"- Résultat: {'Oui' if vcb_result else 'Non'}")
    else:
        print("- Pas de vertex cover de taille k possible")


def run_benchmarks():
    """Lance les benchmarks complets."""
    print("\nLancement des benchmarks...")

    test_configs = [
        {"n": 30, "k": 8},
        {"n": 50, "k": 12},
        {"n": 70, "k": 15}
    ]

    results_df = run_comprehensive_benchmarks(test_configs)
    plot_detailed_results(results_df)
    print("Benchmarks terminés. Résultats sauvegardés.")


def main():
    parser = argparse.ArgumentParser(description="k-Vertex Cover Kernelization Demo")
    parser.add_argument('--mode', choices=['demo', 'random', 'benchmark'],
                        default='demo', help='Mode d\'exécution')
    parser.add_argument('--n', type=int, default=30,
                        help='Nombre de sommets pour le graphe aléatoire')
    parser.add_argument('--k', type=int, default=8,
                        help='Paramètre k pour le vertex cover')

    args = parser.parse_args()

    if args.mode == 'demo':
        demo_simple_example()
    elif args.mode == 'random':
        demo_random_graph(args.n, args.k)
    else:
        run_benchmarks()


if __name__ == "__main__":
    main()