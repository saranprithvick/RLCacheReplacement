"""
Generate the five-workload benchmark suite.

Run from project root:
  PYTHONPATH=. python3 workloads/benchmark/generate.py
"""

import random
from pathlib import Path


BENCHMARK_DIR = Path(__file__).resolve().parent
ZIPF_SEED = 42


def write_trace(name, blocks):
    path = BENCHMARK_DIR / name
    path.write_text("\n".join(blocks) + "\n")
    return path


def stable_working_set(repeats=20):
    """Recency: working set fits in a 4-way cache."""
    blocks = ["A", "B", "C", "D"]
    trace = blocks * repeats
    return write_trace("stable_working_set.txt", trace)


def thrashing_cache_plus_one(repeats=20):
    """Thrashing: working set is one block larger than a 4-way cache."""
    blocks = ["A", "B", "C", "D", "E"]
    trace = blocks * repeats
    return write_trace("thrashing_cache_plus_one.txt", trace)


def hot_set_scan(hot_rounds=8):
    """Pollution: hot set mixed with a one-time cold scan."""
    hot = ["A", "B", "C", "D"]
    trace = []

    for _ in range(hot_rounds):
        trace.extend(hot)
        trace.extend(hot)

    scan = [f"S{i:02d}" for i in range(1, 21)]
    trace.extend(scan)

    for _ in range(4):
        trace.extend(hot)

    return write_trace("hot_set_scan.txt", trace)


def zipfian_accesses(n=200, num_blocks=10, exponent=1.2):
    """Frequency: Zipfian popularity over block IDs."""
    rng = random.Random(ZIPF_SEED)
    blocks = [chr(ord("A") + i) for i in range(num_blocks)]
    weights = [1.0 / (rank ** exponent) for rank in range(1, num_blocks + 1)]
    trace = rng.choices(blocks, weights=weights, k=n)
    return write_trace("zipfian.txt", trace)


def phase_shift(phase_len=40):
    """Adaptation: hot set changes between phases."""
    phase_a = ["A", "B", "C", "D"]
    phase_b = ["W", "X", "Y", "Z"]
    trace = phase_a * (phase_len // len(phase_a))
    trace += phase_b * (phase_len // len(phase_b))
    return write_trace("phase_shift.txt", trace)


def main():
    paths = [
        stable_working_set(),
        thrashing_cache_plus_one(),
        hot_set_scan(),
        zipfian_accesses(),
        phase_shift(),
    ]

    print("Benchmark traces written:")
    for path in paths:
        lines = path.read_text().strip().splitlines()
        print(f"  {path.name:<30} {len(lines):>4} accesses")


if __name__ == "__main__":
    main()
