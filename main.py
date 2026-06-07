from simulator.cache import Cache
from rl.agent import QLearningAgent
from policies.rl_lru import RLLRUPolicy


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

    episodes = 50

    agent = QLearningAgent(
        alpha=0.1,
        gamma=0.9,
        epsilon=0.1
    )

    for episode in range(episodes):

        policy = RLLRUPolicy(agent)

        cache = Cache(
            size=4,
            policy=policy
        )

        for block in trace:
            cache.access(block)

        if (episode + 1) % 10 == 0:
            print(
                f"Episode {episode + 1} completed"
            )

    print("\n===== FINAL RESULTS =====")
    cache.print_stats()

    print("\n===== Q TABLE =====")

    for state, values in sorted(agent.q_table.items()):

        print(
            f"{state} -> "
            f"EVICT={values[0]:.3f} "
            f"KEEP={values[1]:.3f}"
        )


if __name__ == "__main__":
    main()