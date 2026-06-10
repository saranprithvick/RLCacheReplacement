import argparse

from experiments.experiment import compare_policies
from experiments.runner import format_stats
from experiments.reporting import (
    print_quick_summary,
    workload_dimension,
    workload_name,
)
from experiments.trace_loader import list_benchmark_traces, load_trace


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run LRU vs RL-LRU on the benchmark suite "
            "(single cache size, terminal output)."
        )
    )

    parser.add_argument(
        "--cache-size",
        type=int,
        default=4,
        help="Cache capacity (default: 4).",
    )

    parser.add_argument(
        "--train-episodes",
        type=int,
        default=50,
        help="RL training episodes before evaluation (default: 50).",
    )

    parser.add_argument(
        "--trace",
        type=str,
        default=None,
        help="Run a single trace file instead of the full benchmark suite.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-access simulator logs.",
    )

    return parser.parse_args()


def resolve_traces(trace_arg):
    if trace_arg:
        return [(trace_arg.split("/")[-1], load_trace(trace_arg))]

    return [
        (path.name, load_trace(path))
        for path in list_benchmark_traces()
    ]


def print_header():
    print("\n===== BENCHMARK RUN =====")
    print("Suite   : workloads/benchmark/")
    print("Policies: LRU (1 pass) vs RL-LRU (train then 1 eval pass)")


def print_result(result):
    print(f"\nWorkload   : {workload_name(result['trace'])}")
    print(f"Dimension  : {workload_dimension(result['trace'])}")
    print(f"Length     : {result['trace_length']} accesses")
    print(f"Cache size : {result['cache_size']}")
    print(f"RL training: {result['train_episodes']} episodes")
    print(f"LRU        : {format_stats(result['lru'])}")
    print(f"RL-LRU     : {format_stats(result['rl_lru'])}")

    sign = "+" if result["delta_hit_rate"] >= 0 else ""
    print(
        f"Delta      : {sign}{result['delta_hit_rate']:.2%} "
        f"(RL-LRU hit rate vs LRU)"
    )


def print_sanity_notes(results):
    print("\n===== SANITY CHECKS =====")
    print(
        "• stable_working_set should beat thrashing_cache_plus_one on LRU."
    )
    print("• RL-LRU may be worse than LRU — that is expected early on.")

    lru_by_trace = {
        r["trace"]: r["lru"]["hit_rate"]
        for r in results
        if r["cache_size"] == results[0]["cache_size"]
    }

    stable = "stable_working_set.txt"
    thrash = "thrashing_cache_plus_one.txt"

    if stable in lru_by_trace and thrash in lru_by_trace:
        stable_hit = lru_by_trace[stable]
        thrash_hit = lru_by_trace[thrash]

        if stable_hit > thrash_hit:
            print(
                f"✓ LRU on stable working set ({stable_hit:.1%}) beats "
                f"thrashing ({thrash_hit:.1%})."
            )
        else:
            print(
                "✗ Stable working set should beat thrashing — "
                "review benchmark traces."
            )


def main():
    args = parse_args()

    traces = resolve_traces(args.trace)

    if not traces:
        raise SystemExit(
            "No benchmark traces found. Run: "
            "PYTHONPATH=. python3 workloads/benchmark/generate.py"
        )

    print_header()

    results = []

    for trace_name, trace in traces:
        result = compare_policies(
            trace_name,
            trace,
            cache_size=args.cache_size,
            train_episodes=args.train_episodes,
            verbose=args.verbose,
        )
        print_result(result)
        results.append(result)

    print_quick_summary(results)
    print_sanity_notes(results)


if __name__ == "__main__":
    main()
