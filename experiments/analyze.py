import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from experiments.reporting import workload_dimension, workload_name
from experiments.trace_loader import PROJECT_ROOT, benchmark_catalog

RESULTS_DIR = PROJECT_ROOT / "results"
CSV_DIR = RESULTS_DIR / "csv"
TABLES_DIR = RESULTS_DIR / "tables"
PLOTS_DIR = PROJECT_ROOT / "plots" / "figures"
OBSERVATIONS_PATH = RESULTS_DIR / "OBSERVATIONS.md"
ROOT_OBSERVATIONS_PATH = PROJECT_ROOT / "OBSERVATIONS.md"
Q_TABLE_PATH = RESULTS_DIR / "tables" / "q_table_summary.json"

WORKLOAD_ORDER = list(benchmark_catalog().keys())
PRIMARY_CACHE_SIZE = 4


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Day-08 tables, plots, and observations."
    )

    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Comparison CSV (default: latest results/csv/benchmark_comparison.csv or newest comparison_*.csv).",
    )

    parser.add_argument(
        "--primary-cache-size",
        type=int,
        default=PRIMARY_CACHE_SIZE,
        help="Cache size for primary workload plots (default: 4).",
    )

    return parser.parse_args()


def resolve_csv_path(csv_arg):
    if csv_arg:
        path = Path(csv_arg)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path

    fixed = CSV_DIR / "benchmark_comparison.csv"
    if fixed.exists():
        return fixed

    candidates = sorted(CSV_DIR.glob("comparison_*.csv"))
    if candidates:
        return candidates[-1]

    raise SystemExit(
        "No comparison CSV found. Run: "
        "PYTHONPATH=. python3 main.py compare "
        "--output results/csv/benchmark_comparison.csv"
    )


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def workload_sort_key(trace):
    if trace in WORKLOAD_ORDER:
        return WORKLOAD_ORDER.index(trace)

    return len(WORKLOAD_ORDER)


def pivot_results(rows):
    grouped = defaultdict(dict)

    for row in rows:
        key = (row["trace"], int(row["cache_size"]))
        grouped[key][row["policy"]] = row

    comparisons = []

    for (trace, cache_size), policies in sorted(
        grouped.items(),
        key=lambda item: (workload_sort_key(item[0][0]), item[0][1]),
    ):
        lru = policies.get("LRU")
        rl = policies.get("RL-LRU")

        if not lru or not rl:
            continue

        comparisons.append(
            {
                "trace": trace,
                "cache_size": cache_size,
                "trace_length": int(lru["trace_length"]),
                "dimension": workload_dimension(trace),
                "lru": lru,
                "rl_lru": rl,
                "delta_hit_rate": round(
                    float(rl["hit_rate"]) - float(lru["hit_rate"]),
                    4,
                ),
            }
        )

    return comparisons


def write_csv_table(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_table(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

    path.write_text("\n".join(lines) + "\n")


def export_performance_tables(comparisons):
    perf_rows = []
    delta_rows = []
    perf_cs4_rows = []
    summary_rows = []

    rl_better = 0
    lru_better = 0
    tied = 0

    for item in comparisons:
        for policy_key, label in [("lru", "LRU"), ("rl_lru", "RL-LRU")]:
            stats = item[policy_key]
            perf_rows.append(
                {
                    "workload": workload_name(item["trace"]),
                    "dimension": item["dimension"],
                    "cache_size": item["cache_size"],
                    "policy": label,
                    "episodes": stats["episodes"],
                    "hits": stats["hits"],
                    "misses": stats["misses"],
                    "evictions": stats["evictions"],
                    "hit_rate": stats["hit_rate"],
                    "miss_rate": stats["miss_rate"],
                }
            )

        delta = item["delta_hit_rate"]
        if delta > 0:
            winner = "RL-LRU"
            rl_better += 1
        elif delta < 0:
            winner = "LRU"
            lru_better += 1
        else:
            winner = "tie"
            tied += 1

        delta_row = {
            "workload": workload_name(item["trace"]),
            "dimension": item["dimension"],
            "cache_size": item["cache_size"],
            "lru_hit_rate": item["lru"]["hit_rate"],
            "rl_hit_rate": item["rl_lru"]["hit_rate"],
            "delta_hit_rate": f"{delta:+.4f}",
            "winner": winner,
        }
        delta_rows.append(delta_row)

        if item["cache_size"] == PRIMARY_CACHE_SIZE:
            perf_cs4_rows.append(delta_row)

    summary_rows = [
        {"metric": "RL-LRU better", "count": rl_better},
        {"metric": "LRU better", "count": lru_better},
        {"metric": "Tied", "count": tied},
    ]

    perf_fields = [
        "workload",
        "dimension",
        "cache_size",
        "policy",
        "episodes",
        "hits",
        "misses",
        "evictions",
        "hit_rate",
        "miss_rate",
    ]
    delta_fields = [
        "workload",
        "dimension",
        "cache_size",
        "lru_hit_rate",
        "rl_hit_rate",
        "delta_hit_rate",
        "winner",
    ]

    write_csv_table(TABLES_DIR / "performance.csv", perf_fields, perf_rows)
    write_csv_table(TABLES_DIR / "improvement_delta.csv", delta_fields, delta_rows)
    write_csv_table(
        TABLES_DIR / "performance_cache4.csv",
        delta_fields,
        perf_cs4_rows,
    )
    write_csv_table(TABLES_DIR / "summary_win_loss.csv", ["metric", "count"], summary_rows)

    write_markdown_table(
        TABLES_DIR / "performance.md",
        perf_fields,
        [[row[field] for field in perf_fields] for row in perf_rows],
    )
    write_markdown_table(
        TABLES_DIR / "improvement_delta.md",
        delta_fields,
        [[row[field] for field in delta_fields] for row in delta_rows],
    )
    write_markdown_table(
        TABLES_DIR / "performance_cache4.md",
        delta_fields,
        [[row[field] for field in delta_fields] for row in perf_cs4_rows],
    )
    write_markdown_table(
        TABLES_DIR / "summary_win_loss.md",
        ["metric", "count"],
        [[row["metric"], row["count"]] for row in summary_rows],
    )

    return {
        "rl_better": rl_better,
        "lru_better": lru_better,
        "tied": tied,
        "perf_cs4": perf_cs4_rows,
        "all_comparisons": comparisons,
    }


def export_q_table_summary(comparison_results_from_compare=None):
    q_rows = []

    if comparison_results_from_compare:
        source = comparison_results_from_compare
    elif Q_TABLE_PATH.exists():
        return json.loads(Q_TABLE_PATH.read_text())
    else:
        return []

    for result in source:
        q_rows.append(
            {
                "workload": workload_name(result["trace"]),
                "dimension": workload_dimension(result["trace"]),
                "cache_size": result["cache_size"],
                "q_table": result.get("q_table", {}),
            }
        )

    Q_TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    Q_TABLE_PATH.write_text(json.dumps(q_rows, indent=2))

    md_lines = [
        "# Learned Q-Table Summary",
        "",
        "| Workload | Dimension | Cache | State | EVICT | KEEP | Preferred |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for entry in q_rows:
        if not entry["q_table"]:
            md_lines.append(
                f"| {entry['workload']} | {entry['dimension']} | "
                f"{entry['cache_size']} | — | — | — | — |"
            )
            continue

        for state, values in sorted(entry["q_table"].items()):
            preferred = (
                "KEEP"
                if values["KEEP"] > values["EVICT"]
                else "EVICT"
                if values["EVICT"] > values["KEEP"]
                else "tie"
            )
            md_lines.append(
                f"| {entry['workload']} | {entry['dimension']} | "
                f"{entry['cache_size']} | {state} | {values['EVICT']} | "
                f"{values['KEEP']} | {preferred} |"
            )

    (TABLES_DIR / "q_table_summary.md").write_text(
        "\n".join(md_lines) + "\n"
    )

    return q_rows


def write_observations(summary, comparisons):
    cs4 = [c for c in comparisons if c["cache_size"] == PRIMARY_CACHE_SIZE]
    rl_wins = [c for c in cs4 if c["delta_hit_rate"] > 0]
    lru_wins = [c for c in cs4 if c["delta_hit_rate"] < 0]
    ties = [c for c in cs4 if c["delta_hit_rate"] == 0]

    small_cache_noise = [
        c
        for c in comparisons
        if c["cache_size"] < PRIMARY_CACHE_SIZE and c["delta_hit_rate"] > 0
    ]

    lines = [
        "# Experiment Observations",
        "",
        "## Overall (all cache sizes)",
        "",
        f"- RL-LRU better: **{summary['rl_better']}** configurations",
        f"- LRU better: **{summary['lru_better']}** configurations",
        f"- Tied: **{summary['tied']}** configurations",
        "",
        f"## Primary analysis (cache size = {PRIMARY_CACHE_SIZE})",
        "",
        "### Where RL-LRU helps",
        "",
    ]

    if rl_wins:
        for item in rl_wins:
            lines.append(
                f"- **{workload_name(item['trace'])}** "
                f"({item['dimension']}): "
                f"{float(item['lru']['hit_rate']):.1%} → "
                f"{float(item['rl_lru']['hit_rate']):.1%} "
                f"(Δ {item['delta_hit_rate']:+.1%})"
            )
    else:
        lines.append("- No RL-LRU wins at the primary cache size.")

    lines.extend(["", "### Where LRU is better", ""])

    if lru_wins:
        for item in lru_wins:
            lines.append(
                f"- **{workload_name(item['trace'])}** "
                f"({item['dimension']}): "
                f"RL-LRU underperforms by {abs(item['delta_hit_rate']):.1%}"
            )
    else:
        lines.append("- LRU does not beat RL-LRU at the primary cache size.")

    lines.extend(["", "### Ties", ""])

    if ties:
        for item in ties:
            lines.append(
                f"- **{workload_name(item['trace'])}** "
                f"({item['dimension']}): identical hit rate"
            )
    else:
        lines.append("- No exact ties at the primary cache size.")

    lines.extend(
        [
            "",
            "## Anomalies",
            "",
        ]
    )

    if small_cache_noise:
        lines.append(
            "- **Small cache (size < 4):** RL-LRU often looks better than LRU, "
            "but the benchmark suite was designed around a 4-way cache. "
            "Treat size-2 results as noisy."
        )

    thrash_cs4 = next(
        (
            c
            for c in cs4
            if c["trace"] == "thrashing_cache_plus_one.txt"
        ),
        None,
    )
    if thrash_cs4 and thrash_cs4["delta_hit_rate"] > 0:
        lines.append(
            "- **Thrashing @ cache 4:** LRU hit rate is 0% (expected for a "
            "cache+1 loop), while RL-LRU improves via second-chance decisions. "
            "Worth discussing as the most interesting RL case."
        )

    lines.extend(
        [
            "",
            "## Takeaways for the meeting",
            "",
            "- RL-LRU is built as a layer on top of LRU, not a replacement.",
            "- Gains are workload-dependent; many benchmarks tie at cache size 4.",
            "- The Q-table summary shows which states learned to EVICT vs KEEP.",
            "- Professors care more about *when* RL helps than always beating LRU.",
            "",
        ]
    )

    content = "\n".join(lines)

    OBSERVATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    OBSERVATIONS_PATH.write_text(content)
    ROOT_OBSERVATIONS_PATH.write_text(content)


def plot_results(comparisons, primary_cache_size):
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise SystemExit(
            "matplotlib is required for plots. Install with: pip install matplotlib"
        ) from exc

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    ordered_traces = sorted(
        {item["trace"] for item in comparisons},
        key=workload_sort_key,
    )
    labels = [workload_name(t) for t in ordered_traces]
    dimensions = [workload_dimension(t) for t in ordered_traces]
    x = np.arange(len(ordered_traces))
    width = 0.36

    cs4_items = {
        item["trace"]: item
        for item in comparisons
        if item["cache_size"] == primary_cache_size
    }

    # 1. Hit rate vs workload @ primary cache size
    lru_vals = [float(cs4_items[t]["lru"]["hit_rate"]) * 100 for t in ordered_traces]
    rl_vals = [float(cs4_items[t]["rl_lru"]["hit_rate"]) * 100 for t in ordered_traces]

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x - width / 2, lru_vals, width, label="LRU")
    ax.bar(x + width / 2, rl_vals, width, label="RL-LRU")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylabel("Hit rate (%)")
    ax.set_title(f"Hit Rate vs Workload (cache size = {primary_cache_size})")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "hit_rate_vs_workload.png", dpi=160)
    plt.close(fig)

    # 1b. Hit rate vs benchmark dimension @ primary cache size
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width / 2, lru_vals, width, label="LRU")
    ax.bar(x + width / 2, rl_vals, width, label="RL-LRU")
    ax.set_xticks(x)
    ax.set_xticklabels(dimensions, rotation=15, ha="right")
    ax.set_ylabel("Hit rate (%)")
    ax.set_title(f"Hit Rate vs Benchmark Dimension (cache size = {primary_cache_size})")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "hit_rate_vs_dimension.png", dpi=160)
    plt.close(fig)

    # 2. Hit rate vs cache size (line plot per workload)
    cache_sizes = sorted({item["cache_size"] for item in comparisons})
    fig, ax = plt.subplots(figsize=(9, 5))

    for trace in ordered_traces:
        by_size = {
            item["cache_size"]: item
            for item in comparisons
            if item["trace"] == trace
        }
        lru_line = [
            float(by_size[size]["lru"]["hit_rate"]) * 100
            for size in cache_sizes
        ]
        rl_line = [
            float(by_size[size]["rl_lru"]["hit_rate"]) * 100
            for size in cache_sizes
        ]
        name = workload_name(trace)
        ax.plot(cache_sizes, lru_line, marker="o", linestyle="--", label=f"{name} LRU")
        ax.plot(cache_sizes, rl_line, marker="o", label=f"{name} RL-LRU")

    ax.set_xlabel("Cache size")
    ax.set_ylabel("Hit rate (%)")
    ax.set_title("Hit Rate vs Cache Size")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "hit_rate_vs_cache_size.png", dpi=160)
    plt.close(fig)

    # 3. Delta bar chart @ primary cache size
    deltas = [
        cs4_items[t]["delta_hit_rate"] * 100 for t in ordered_traces
    ]
    colors = ["#2ca02c" if d > 0 else "#d62728" if d < 0 else "#9e9e9e" for d in deltas]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x, deltas, color=colors)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylabel("Δ hit rate (RL-LRU − LRU) (pp)")
    ax.set_title(f"Improvement Delta (cache size = {primary_cache_size})")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "delta_hit_rate.png", dpi=160)
    plt.close(fig)

    # 4. Delta heatmap (workload × cache size)
    heatmap = np.zeros((len(ordered_traces), len(cache_sizes)))
    for i, trace in enumerate(ordered_traces):
        for j, size in enumerate(cache_sizes):
            item = next(
                c
                for c in comparisons
                if c["trace"] == trace and c["cache_size"] == size
            )
            heatmap[i, j] = item["delta_hit_rate"] * 100

    fig, ax = plt.subplots(figsize=(8, 5))
    image = ax.imshow(heatmap, aspect="auto", cmap="RdYlGn", vmin=-10, vmax=50)
    ax.set_xticks(range(len(cache_sizes)))
    ax.set_xticklabels(cache_sizes)
    ax.set_yticks(range(len(ordered_traces)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Cache size")
    ax.set_title("Δ Hit Rate Heatmap (RL-LRU − LRU, pp)")
    fig.colorbar(image, ax=ax)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "delta_heatmap.png", dpi=160)
    plt.close(fig)

    # 5. Q-table summary chart @ primary cache size
    if Q_TABLE_PATH.exists():
        q_rows = json.loads(Q_TABLE_PATH.read_text())
        q_cs4 = [
            row
            for row in q_rows
            if row["cache_size"] == primary_cache_size and row["q_table"]
        ]

        if q_cs4:
            fig, ax = plt.subplots(figsize=(10, 5))
            chart_labels = []
            evict_vals = []
            keep_vals = []

            for entry in q_cs4:
                for state, values in sorted(entry["q_table"].items()):
                    chart_labels.append(f"{entry['workload']}\n{state}")
                    evict_vals.append(values["EVICT"])
                    keep_vals.append(values["KEEP"])

            xq = np.arange(len(chart_labels))
            ax.bar(xq - width / 2, evict_vals, width, label="Q(EVICT)")
            ax.bar(xq + width / 2, keep_vals, width, label="Q(KEEP)")
            ax.set_xticks(xq)
            ax.set_xticklabels(chart_labels, rotation=25, ha="right", fontsize=8)
            ax.set_ylabel("Q-value")
            ax.set_title(
                f"Learned Q-Table Summary (cache size = {primary_cache_size})"
            )
            ax.legend()
            ax.grid(axis="y", alpha=0.3)
            fig.tight_layout()
            fig.savefig(PLOTS_DIR / "q_table_summary.png", dpi=160)
            plt.close(fig)


def save_q_table_from_compare_results(results):
    export_q_table_summary(comparison_results_from_compare=results)


def run_analysis(csv_path, primary_cache_size, comparison_results=None):
    rows = load_rows(csv_path)
    comparisons = pivot_results(rows)
    summary = export_performance_tables(comparisons)

    if comparison_results is None:
        export_q_table_summary()
    else:
        export_q_table_summary(comparison_results)

    write_observations(summary, comparisons)
    plot_results(comparisons, primary_cache_size)

    return {
        "csv": csv_path,
        "tables_dir": TABLES_DIR,
        "plots_dir": PLOTS_DIR,
        "observations": ROOT_OBSERVATIONS_PATH,
    }


def main():
    args = parse_args()
    csv_path = resolve_csv_path(args.csv)
    outputs = run_analysis(csv_path, args.primary_cache_size)

    print("\n===== DAY 08 — ARTIFACT GENERATION =====")
    print(f"Source CSV : {outputs['csv']}")
    print(f"Tables     : {outputs['tables_dir']}")
    print(f"Plots      : {outputs['plots_dir']}")
    print(f"Notes      : {outputs['observations']}")
    print("\nGenerated plots:")
    for path in sorted(outputs["plots_dir"].glob("*.png")):
        print(f"  - {path.name}")


if __name__ == "__main__":
    main()
