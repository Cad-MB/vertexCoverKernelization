import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from src.generators import generate_vertex_cover_graph
from src.kernel import kernel_vertex_cover_crown
from src.vcb import vcb_recursive


def benchmark_instance(G, k, edge_density):
    """Benchmark détaillé avec métriques supplémentaires."""
    results = {
        "n": G.number_of_nodes(),
        "m": G.number_of_edges(),
        "k": k,
        "density": edge_density,
        "k_n_ratio": k / G.number_of_nodes()
    }

    # Kernel + VCB
    start = time.time()
    ker_G, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
    ker_time = time.time() - start

    if not no_inst and ker_G:
        vcb_start = time.time()
        vcb_ker_result = vcb_recursive(ker_G, ker_k)
        ker_vcb_time = time.time() - vcb_start

        results.update({
            "kernel_size": ker_G.number_of_nodes(),
            "kernel_edges": ker_G.number_of_edges(),
            "kernel_density": ker_G.number_of_edges() / (ker_G.number_of_nodes() * (ker_G.number_of_nodes() - 1) / 2),
            "kernel_time": ker_time,
            "kernel_vcb_time": ker_vcb_time,
            "total_ker_time": ker_time + ker_vcb_time,
            "reduction_ratio": 1 - (ker_G.number_of_nodes() / G.number_of_nodes()),
            "edge_reduction_ratio": 1 - (ker_G.number_of_edges() / G.number_of_edges()),
            "kernel_success": vcb_ker_result
        })
    else:
        results.update({
            "kernel_size": 0,
            "kernel_edges": 0,
            "kernel_density": 0,
            "kernel_time": ker_time,
            "kernel_vcb_time": 0,
            "total_ker_time": ker_time,
            "reduction_ratio": 0,
            "edge_reduction_ratio": 0,
            "kernel_success": False
        })

    # VCB seul
    start = time.time()
    vcb_result = vcb_recursive(G, k)
    vcb_time = time.time() - start

    results.update({
        "vcb_time": vcb_time,
        "vcb_success": vcb_result,
        "speedup": vcb_time / results["total_ker_time"] if results["total_ker_time"] > 0 else 0
    })

    return results


def run_comprehensive_benchmarks(test_configs, edge_probs=[0.1, 0.3, 0.5], samples=5):
    """Exécute une série complète de tests."""
    all_results = []
    total_tests = len(test_configs) * len(edge_probs) * samples * 2  # *2 pour random et guaranteed
    current = 0

    for config in test_configs:
        n, k = config["n"], config["k"]
        print(f"\nConfiguration: n={n}, k={k}")

        for edge_prob in edge_probs:
            print(f"Edge probability: {edge_prob}")
            for i in range(samples):
                current += 2
                print(f"Sample {i + 1}/{samples} (Progress: {current}/{total_tests})")

                # Test standard
                G = generate_vertex_cover_graph(n, k, edge_prob)
                results = benchmark_instance(G, k, edge_prob)
                results.update({"type": "random"})
                all_results.append(results)

                # Test avec VC garanti
                G = generate_vertex_cover_graph(n, k, edge_prob, guaranteed_vc=True)
                results = benchmark_instance(G, k, edge_prob)
                results.update({"type": "guaranteed_vc"})
                all_results.append(results)

    return pd.DataFrame(all_results)


def compute_confidence_intervals(df, column, confidence=0.95):
    """Calcule les intervalles de confiance pour une colonne."""
    grouped = df.groupby(['n', 'type', 'density'])
    intervals = grouped[column].agg(lambda x: stats.t.interval(confidence,
                                                               len(x) - 1,
                                                               loc=np.mean(x),
                                                               scale=stats.sem(x)))
    return intervals


def main():
    """Programme principal avec configurations étendues."""
    test_configs = [
        {"n": 30, "k": 8},
        {"n": 50, "k": 12},
        {"n": 70, "k": 15},
        {"n": 90, "k": 20},
        {"n": 110, "k": 25},
        {"n": 130, "k": 30}
    ]

    # Exécution des benchmarks
    results_df = run_comprehensive_benchmarks(test_configs)

    # Sauvegarde détaillée
    results_df.to_csv("benchmark_detailed.csv", index=False)

    # Analyse statistique
    print("\nStatistiques par type et densité:")
    stats_df = results_df.groupby(['type', 'density'])[['reduction_ratio', 'speedup']].describe()
    print(stats_df)

    # Intervalles de confiance
    ci_reduction = compute_confidence_intervals(results_df, 'reduction_ratio')
    ci_speedup = compute_confidence_intervals(results_df, 'speedup')
    print("\nIntervalles de confiance (réduction):")
    print(ci_reduction)
    print("\nIntervalles de confiance (speedup):")
    print(ci_speedup)

    # Impact de la densité
    density_impact = results_df.groupby(['density', 'type']).agg({
        'reduction_ratio': ['mean', 'std'],
        'speedup': ['mean', 'std'],
        'kernel_success': 'mean',
        'vcb_success': 'mean'
    })
    print("\nImpact de la densité:")
    print(density_impact)

    # Ajout des visualisations détaillées
    plot_detailed_results(results_df)

def plot_detailed_results(df, output_dir="."):
    """Crée toutes les visualisations nécessaires."""

    # 1. Temps d'exécution par densité
    plt.figure(figsize=(10, 6))
    for density in df['density'].unique():
        data = df[df['density'] == density]
        plt.plot(data['n'], data['total_ker_time'],
                 label=f'Kernel+VCB (d={density:.1f})')
        plt.plot(data['n'], data['vcb_time'],
                 label=f'VCB (d={density:.1f})')
    plt.xlabel('Nombre de sommets (n)')
    plt.ylabel('Temps (s)')
    plt.title('Temps d\'exécution par densité')
    plt.legend()
    plt.savefig(f'{output_dir}/exec_time_density.png')
    plt.close()

    # 2. Qualité du kernel
    plt.figure(figsize=(10, 6))
    for type_g in df['type'].unique():
        data = df[df['type'] == type_g]
        plt.scatter(data['k_n_ratio'], data['reduction_ratio'],
                    label=f'Type: {type_g}', alpha=0.6)
    plt.xlabel('Ratio k/n')
    plt.ylabel('Ratio de réduction')
    plt.title('Qualité du kernel vs ratio k/n')
    plt.legend()
    plt.savefig(f'{output_dir}/kernel_quality.png')
    plt.close()

    # 3. Impact de la densité
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    densities = sorted(df['density'].unique())
    types = df['type'].unique()

    for type_g in types:
        means = [df[(df['density'] == d) & (df['type'] == type_g)]['reduction_ratio'].mean()
                 for d in densities]
        ax1.plot(densities, means, 'o-', label=type_g)
    ax1.set_xlabel('Densité')
    ax1.set_ylabel('Ratio moyen de réduction')
    ax1.set_title('Impact de la densité sur la réduction')
    ax1.legend()

    for type_g in types:
        success = [df[(df['density'] == d) & (df['type'] == type_g)]['kernel_success'].mean()
                   for d in densities]
        ax2.plot(densities, success, 'o-', label=type_g)
    ax2.set_xlabel('Densité')
    ax2.set_ylabel('Taux de succès')
    ax2.set_title('Impact de la densité sur le succès')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(f'{output_dir}/density_impact.png')
    plt.close()

    # 4. Distributions des temps
    plt.figure(figsize=(10, 6))
    violin_data = []
    labels = []
    for density in densities:
        for type_g in types:
            data = df[(df['density'] == density) & (df['type'] == type_g)]
            violin_data.append(data['speedup'])
            labels.append(f'{type_g}\nd={density:.1f}')

    plt.violinplot(violin_data, showmeans=True)
    plt.xticks(range(1, len(labels) + 1), labels, rotation=45)
    plt.ylabel('Speedup')
    plt.title('Distribution des speedups par configuration')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/speedup_dist.png')
    plt.close()

if __name__ == "__main__":
    main()