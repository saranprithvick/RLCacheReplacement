# RL-Based LRU Cache Replacement

Prototype simulator comparing **traditional LRU** with **RL-guided LRU** (Q-learning + second-chance eviction), inspired by paper 2's next-attempt approach.

## Prerequisites

- Python 3.8+
- `matplotlib` for plots (Day 08): `pip install -r requirements.txt`

All commands below assume you are in the project root:

```bash
cd "/path/to/RL_Cache_Replacement"
```

## Why `PYTHONPATH=.`?

Imports use top-level packages (`experiments`, `simulator`, `policies`, `rl`). Setting `PYTHONPATH=.` tells Python to treat the project root as the module search path so those imports resolve correctly.

## Benchmark suite

Five workloads in `workloads/benchmark/` cover the main replacement-policy dimensions:

| File | Dimension |
|------|-----------|
| `stable_working_set.txt` | Recency — working set fits in cache |
| `thrashing_cache_plus_one.txt` | Thrashing — working set is cache+1 |
| `hot_set_scan.txt` | Pollution resistance — hot set + cold scan |
| `zipfian.txt` | Frequency / popularity — Zipfian skew |
| `phase_shift.txt` | Adaptation — hot set changes mid-trace |

Regenerate traces:

```bash
PYTHONPATH=. python3 workloads/benchmark/generate.py
```

## Run tests

```bash
PYTHONPATH=. python3 tests/test_lru.py
PYTHONPATH=. python3 tests/test_rl_lru.py
```

## Quick experiment (terminal output)

Compare LRU vs RL-LRU on the full benchmark suite (default cache size: 4).

```bash
PYTHONPATH=. python3 main.py
```

**Options:**

```bash
PYTHONPATH=. python3 main.py --cache-size 8
PYTHONPATH=. python3 main.py --train-episodes 100
PYTHONPATH=. python3 main.py --trace workloads/benchmark/zipfian.txt
PYTHONPATH=. python3 main.py --trace workloads/benchmark/stable_working_set.txt --verbose
```

## Systematic comparison + CSV

Run the benchmark grid (5 traces × cache sizes 2/4/8 × LRU vs RL-LRU):

```bash
PYTHONPATH=. python3 main.py compare
```

Write to a fixed CSV path:

```bash
PYTHONPATH=. python3 main.py compare --output results/csv/benchmark_comparison.csv
```

**Options:**

```bash
PYTHONPATH=. python3 main.py compare --cache-sizes 4 8
PYTHONPATH=. python3 main.py compare --trace workloads/benchmark/phase_shift.txt
```

## Generate tables, plots, and observations (Day 08)

Requires a comparison CSV first (see above). Then:

```bash
PYTHONPATH=. python3 main.py analyze
```

**Outputs:**

| Output | Location |
|--------|----------|
| Performance table | `results/tables/performance.csv` / `.md` |
| Δ hit rate table | `results/tables/improvement_delta.csv` / `.md` |
| Cache-4 summary | `results/tables/performance_cache4.csv` / `.md` |
| Win/loss/tie counts | `results/tables/summary_win_loss.md` |
| Q-table summary | `results/tables/q_table_summary.md` + `.json` |
| Written observations | `OBSERVATIONS.md` (also `results/OBSERVATIONS.md`) |
| Plots | `plots/figures/*.png` |

**Plots generated:** hit rate vs workload, hit rate vs dimension, hit rate vs cache size, delta bar chart, delta heatmap, Q-table summary.

```bash
PYTHONPATH=. python3 main.py analyze --csv results/csv/benchmark_comparison.csv
```

## Full pipeline

```bash
pip install -r requirements.txt
PYTHONPATH=. python3 workloads/benchmark/generate.py
PYTHONPATH=. python3 main.py compare --output results/csv/benchmark_comparison.csv
PYTHONPATH=. python3 main.py analyze
```

## Project layout

```
policies/              LRU and RL-LRU replacement policies
rl/                    Q-learning agent and eviction history
simulator/             Cache simulator
experiments/           Runners, comparison, and analysis scripts
workloads/benchmark/   Benchmark traces + generate.py
results/csv/           Raw experiment CSV
results/tables/        Exported tables + Q-table JSON
OBSERVATIONS.md        Experiment analysis (root + results/)
plots/figures/         Generated plots
tests/                 Unit tests
main.py                Entry point (`run`, `compare`, or `analyze`)
```
