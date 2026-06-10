from experiments.trace_loader import benchmark_catalog


def workload_name(filename):
    return filename.replace(".txt", "")


def workload_dimension(filename):
    meta = benchmark_catalog().get(filename, {})
    return meta.get("dimension", "—")


def _pct(value):
    return f"{value * 100:6.1f}%"


def _delta(value):
    sign = "+" if value >= 0 else "-"
    return f"{sign}{abs(value) * 100:5.1f}%"


def _divider(width):
    return "-" * width


def print_comparison_summary(results, title="COMPARISON SUMMARY"):
    workload_w = 28
    dimension_w = 24
    size_w = 4
    pct_w = 8
    delta_w = 9
    note_w = 5

    total_w = (
        workload_w
        + dimension_w
        + size_w
        + pct_w * 2
        + delta_w
        + note_w
        + 6
    )

    print(f"\n===== {title} =====")
    print(
        f"{'Workload':<{workload_w}} "
        f"{'Dimension':<{dimension_w}} "
        f"{'Size':>{size_w}} "
        f"{'LRU':>{pct_w}} "
        f"{'RL-LRU':>{pct_w}} "
        f"{'Delta':>{delta_w}} "
        f"{'Note':>{note_w}}"
    )
    print(_divider(total_w))

    rl_better = 0
    lru_better = 0
    tied = 0

    for result in results:
        delta = result["delta_hit_rate"]

        if delta > 0:
            note = "RL"
            rl_better += 1
        elif delta < 0:
            note = "LRU"
            lru_better += 1
        else:
            note = "tie"
            tied += 1

        print(
            f"{workload_name(result['trace']):<{workload_w}} "
            f"{workload_dimension(result['trace']):<{dimension_w}} "
            f"{result['cache_size']:>{size_w}} "
            f"{_pct(result['lru']['hit_rate']):>{pct_w}} "
            f"{_pct(result['rl_lru']['hit_rate']):>{pct_w}} "
            f"{_delta(delta):>{delta_w}} "
            f"{note:>{note_w}}"
        )

    print(_divider(total_w))
    print(
        f"{'Totals':<{workload_w}} "
        f"{'':<{dimension_w}} "
        f"{'':>{size_w}} "
        f"{'':>{pct_w}} "
        f"{'':>{pct_w}} "
        f"{'':>{delta_w}} "
        f"{'':>{note_w}}"
    )
    print(
        f"  RL-LRU better: {rl_better}   "
        f"LRU better: {lru_better}   "
        f"Tied: {tied}"
    )


def print_quick_summary(results):
    workload_w = 28
    pct_w = 8
    delta_w = 9
    total_w = workload_w + 24 + 4 + pct_w * 2 + delta_w + 4

    print("\n===== SUMMARY =====")
    print(
        f"{'Workload':<{workload_w}} "
        f"{'Dimension':<24} "
        f"{'Size':>4} "
        f"{'LRU':>{pct_w}} "
        f"{'RL-LRU':>{pct_w}} "
        f"{'Delta':>{delta_w}}"
    )
    print(_divider(total_w))

    for result in results:
        print(
            f"{workload_name(result['trace']):<{workload_w}} "
            f"{workload_dimension(result['trace']):<24} "
            f"{result['cache_size']:>4} "
            f"{_pct(result['lru']['hit_rate']):>{pct_w}} "
            f"{_pct(result['rl_lru']['hit_rate']):>{pct_w}} "
            f"{_delta(result['delta_hit_rate']):>{delta_w}}"
        )

    print(_divider(total_w))
