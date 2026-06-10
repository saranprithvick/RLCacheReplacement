from experiments.runner import run_lru, run_rl_lru


def compare_policies(
    trace_name,
    trace,
    cache_size,
    train_episodes=50,
    verbose=False,
):
    lru_stats = run_lru(
        trace,
        cache_size=cache_size,
        verbose=verbose,
    )

    rl_result = run_rl_lru(
        trace,
        cache_size=cache_size,
        train_episodes=train_episodes,
        verbose=verbose,
    )
    rl_stats = rl_result["stats"]

    delta = round(
        rl_stats["hit_rate"] - lru_stats["hit_rate"],
        4,
    )

    return {
        "trace": trace_name,
        "trace_length": len(trace),
        "cache_size": cache_size,
        "train_episodes": train_episodes,
        "lru": lru_stats,
        "rl_lru": rl_stats,
        "delta_hit_rate": delta,
        "q_table": rl_result["q_table"],
    }


def policy_rows(result, timestamp):
    rows = []

    for policy_name, stats, episodes in [
        ("LRU", result["lru"], 1),
        ("RL-LRU", result["rl_lru"], result["train_episodes"]),
    ]:
        rows.append(
            {
                "timestamp": timestamp,
                "trace": result["trace"],
                "trace_length": result["trace_length"],
                "cache_size": result["cache_size"],
                "policy": policy_name,
                "episodes": episodes,
                "hits": stats["hits"],
                "misses": stats["misses"],
                "evictions": stats["evictions"],
                "hit_rate": stats["hit_rate"],
                "miss_rate": stats["miss_rate"],
            }
        )

    return rows
