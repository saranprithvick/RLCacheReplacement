import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

from experiments.analyze import save_q_table_from_compare_results
from experiments.experiment import compare_policies, policy_rows
from experiments.reporting import print_comparison_summary
from experiments.trace_loader import (
    PROJECT_ROOT,
    list_benchmark_traces,
    load_trace,
)

RESULTS_DIR = PROJECT_ROOT / "results" / "csv"
CSV_FIELDS = [
    "timestamp",
    "trace",
    "trace_length",
    "cache_size",
    "policy",
    "episodes",
    "hits",
    "misses",
    "evictions",
    "hit_rate",
    "miss_rate",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Systematic LRU vs RL-LRU comparison: "
            "vary cache size and traces, write CSV results."
        )
    )

    parser.add_argument(
        "--cache-sizes",
        type=int,
        nargs="+",
        default=[2, 4, 8],
        help="Cache sizes to evaluate (default: 2 4 8).",
    )

    parser.add_argument(
        "--train-episodes",
        type=int,
        default=50,
        help="RL training episodes before each eval pass (default: 50).",
    )

    parser.add_argument(
        "--trace",
        type=str,
        default=None,
        help="Evaluate a single trace instead of the full benchmark suite.",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="CSV output path (default: results/csv/comparison_<timestamp>.csv).",
    )

    return parser.parse_args()


def resolve_traces(trace_arg):
    if trace_arg:
        return [(trace_arg.split("/")[-1], load_trace(trace_arg))]

    return [
        (path.name, load_trace(path))
        for path in list_benchmark_traces()
    ]


def default_output_path():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return RESULTS_DIR / f"comparison_{stamp}.csv"


def write_csv(rows, output_path):
    output_path = Path(output_path)

    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def print_header(cache_sizes, train_episodes, trace_count):
    print("\n===== BENCHMARK COMPARISON (DAY 07) =====")
    print(f"Suite        : workloads/benchmark/ ({trace_count} traces)")
    print(f"Cache sizes  : {cache_sizes}")
    print(f"RL training  : {train_episodes} episodes per RL-LRU run")
    print("Output       : one CSV row per (trace, cache_size, policy)")


def main():
    args = parse_args()
    traces = resolve_traces(args.trace)

    if not traces:
        raise SystemExit(
            "No benchmark traces found. Run: "
            "PYTHONPATH=. python3 workloads/benchmark/generate.py"
        )

    timestamp = datetime.now(timezone.utc).isoformat()
    output_path = Path(args.output) if args.output else default_output_path()

    print_header(
        cache_sizes=args.cache_sizes,
        train_episodes=args.train_episodes,
        trace_count=len(traces),
    )

    csv_rows = []
    comparison_results = []

    for trace_name, trace in traces:
        for cache_size in args.cache_sizes:
            result = compare_policies(
                trace_name,
                trace,
                cache_size=cache_size,
                train_episodes=args.train_episodes,
                verbose=False,
            )
            comparison_results.append(result)
            csv_rows.extend(policy_rows(result, timestamp))

    output_file = write_csv(csv_rows, output_path)
    save_q_table_from_compare_results(comparison_results)

    print_comparison_summary(
        comparison_results,
        title="BENCHMARK COMPARISON SUMMARY",
    )
    print(f"\nCSV written to: {output_file}")
    print(f"Total rows    : {len(csv_rows)}")


if __name__ == "__main__":
    main()
