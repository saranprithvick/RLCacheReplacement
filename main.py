from simulator.cache import Cache
from policies.lru import LRUPolicy
from rl.agent import RLAgent
from policies.rl_lru import (
    RLLRUPolicy
)


def load_trace(path):

    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

trace = [
    "A",
    "B",
    "C",
    "D",
    "A",
    "B",
    "E",
    "A",
    "B",
    "C",
    "D",
    "E"
]

def main():

    # trace = load_trace(
    #     "workloads/synthetic/trace_1.txt"
    # )
    agent = RLAgent()

    policy = RLLRUPolicy(
        agent
    )

    cache = Cache(
        size=4,
        policy=LRUPolicy()
    )

    for block in trace:
        cache.access(block)

    cache.print_stats()


if __name__ == "__main__":
    main()