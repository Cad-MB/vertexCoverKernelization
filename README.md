# k-Vertex Cover Kernelization

Une implémentation de la kernelization par décomposition en couronne pour le problème du k-Vertex Cover, basée sur l'algorithme décrit dans Cygan et al. "Parameterized Algorithms".

## Caractéristiques

- Implémentation de la décomposition en couronne
- Kernelization avec borne garantie de 3k sommets
- Intégration de l'algorithme de Hopcroft-Karp via NetworkX
- Générateur d'instances de test
- Suite de benchmarks complète
- Tests unitaires extensifs

## Prérequis

```bash
Python 3.8+
networkx 3.4.2
matplotlib 3.10.0
pandas 2.2.3
seaborn 0.13.2
numpy 2.2.2
scipy 1.15.1
```

## Installation

```bash
git clone https://github.com/yourusername/vertex-cover-kernelization.git
cd vertex-cover-kernelization
pip install -r requirements.txt
```

## Utilisation

### Mode démonstration simple
```bash
python main.py --mode demo
```

### Test sur graphe aléatoire
```bash
python main.py --mode random --n 50 --k 12
```

### Lancer les benchmarks
```bash
python main.py --mode benchmark
```

## Structure du projet

```
.
├── src/
│   ├── __init__.py
│   ├── graph_utils.py      # Opérations de base sur les graphes
│   ├── reduction_rules.py  # Règles de réduction
│   ├── crown_decomp.py    # Algorithme de décomposition en couronne
│   ├── kernel.py          # Kernelization principale
│   ├── vcb.py            # Algorithme de branchement VCB
│   └── generators.py      # Générateurs de graphes tests
├── docs/
├── tests/
│   ├── __init__.py
│   ├── test_graph_utils.py
│   ├── test_reduction_rules.py
│   ├── test_crown_decomp.py
│   ├── test_kernel.py
│   └── test_vcb.py
├── benchmark/
│   └── benchmark.py       # Scripts de benchmark
│   └── benchmark_results_full.csv
│   └── benchmark_results_full.png
├── main.py               # Point d'entrée principal
├── requirements.txt
└── README.md
```

## Tests

Pour exécuter tous les tests :
```bash
python -m unittest discover tests
```

Pour un test spécifique :
```bash
python -m unittest tests/test_kernel.py
```

## Benchmarks

Les benchmarks mesurent :
- Temps d'exécution comparatif (kernel+VCB vs VCB seul)
- Taille du kernel vs borne théorique
- Ratio de réduction
- Impact de la densité du graphe

Les résultats sont sauvegardés sous forme de graphiques dans le dossier `benchmark/`.

## Exemples de résultats

```python
# Exemple d'utilisation du code
import networkx as nx
from src.kernel import kernel_vertex_cover_crown
from src.vcb import vcb_recursive

# Créer un graphe
G = nx.Graph([(1, 2), (2, 3), (1, 3), (3, 4)])
k = 2

# Appliquer la kernelization
ker_G, ker_k, no_inst = kernel_vertex_cover_crown(G, k)
if not no_inst:
    result = vcb_recursive(ker_G, ker_k)
    print(f"Vertex cover de taille {k} existe: {result}")
```

## Références

- Cygan, M. et al. (2016). Parameterized Algorithms. Springer.


## Auteur

- https://github.com/Cad-MB

## Encadrement

- Prof. Claire Hanen (https://www.lip6.fr/actualite/personnes-fiche.php?ident=P41)