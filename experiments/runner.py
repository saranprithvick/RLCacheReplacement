from policies.lru import LRUPolicy
from policies.rl_lru import RLLRUPolicy
from rl.agent import QLearningAgent
from simulator.cache import Cache


def run_lru(trace, cache_size, verbose=False):
    cache = Cache(
        size=cache_size,
        policy=LRUPolicy(),
        verbose=verbose,
    )

    for block in trace:
        cache.access(block)

    return cache.get_stats()


def run_rl_lru(
    trace,
    cache_size,
    train_episodes=50,
    eval_epsilon=0.0,
    alpha=0.1,
    gamma=0.9,
    train_epsilon=0.1,
    verbose=False,
):
    agent = QLearningAgent(
        alpha=alpha,
        gamma=gamma,
        epsilon=train_epsilon,
    )

    for _ in range(train_episodes):
        policy = RLLRUPolicy(agent)
        cache = Cache(
            size=cache_size,
            policy=policy,
            verbose=False,
        )

        for block in trace:
            cache.access(block)

    agent.epsilon = eval_epsilon

    policy = RLLRUPolicy(agent)
    cache = Cache(
        size=cache_size,
        policy=policy,
        verbose=verbose,
    )

    for block in trace:
        cache.access(block)

    return {
        "stats": cache.get_stats(),
        "q_table": serialize_q_table(agent.q_table),
    }


def serialize_q_table(q_table):
    serialized = {}

    for state, values in q_table.items():
        serialized[str(state)] = {
            "EVICT": round(values[0], 4),
            "KEEP": round(values[1], 4),
        }

    return serialized


def format_stats(stats):
    return (
        f"hits={stats['hits']} "
        f"misses={stats['misses']} "
        f"evictions={stats['evictions']} "
        f"hit_rate={stats['hit_rate']:.2%} "
        f"miss_rate={stats['miss_rate']:.2%}"
    )
