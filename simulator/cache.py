from simulator.cache_line import CacheLine
from rl.history_table import HistoryTable


class Cache:
    def __init__(self, size, policy):

        self.size = size
        self.policy = policy

        self.lines = {}
        self.access_frequency = {}

        self.hits = 0
        self.misses = 0
        self.evictions = 0

        self.recent_hit = {}

        # Q-Learning bookkeeping
        self.last_state = None
        self.last_action = None

        self.history_table = HistoryTable()

    def build_state(self, victim):

        freq = self.access_frequency.get(victim, 0)

        if freq <= 1:
            frequency_bucket = 0

        elif freq <= 3:
            frequency_bucket = 1

        else:
            frequency_bucket = 2

        recent_hit_bucket = self.recent_hit.get(victim, 0)

        return (
            frequency_bucket,
            recent_hit_bucket
        )

    def access(self, block):

        self.access_frequency[block] = (
            self.access_frequency.get(block, 0) + 1
        )

        # ------------------------------------
        # Reward generation (June 4 Step 5)
        # ------------------------------------

        if self.last_state is not None and self.last_action is not None:

            if self.history_table.was_evicted(block):

                reward = -1

            else:

                reward = +1

            self.policy.agent.update(
                self.last_state,
                self.last_action,
                reward,
                self.last_state
            )

        # ------------------------------------
        # HIT
        # ------------------------------------

        if block in self.lines:

            self.hits += 1

            self.recent_hit[block] = 1

            self.policy.access(block)

            print(
                f"{block:>2} -> HIT   "
                f"Cache={list(self.lines.keys())}"
            )

            return

        # ------------------------------------
        # MISS
        # ------------------------------------

        self.misses += 1

        if len(self.lines) >= self.size:

            victim = self.policy.victim()

            state = self.build_state(victim)

            action = self.policy.agent.choose_action(
                state
            )

            decision = action.name

            # Store for future Q-update
            self.last_state = state
            self.last_action = action

            print(
                f"Victim={victim}",
                f"State={state}",
                f"Action={decision}",
            )

            if decision == "EVICT":

                self.history_table.add(victim)

                del self.lines[victim]

                if victim in self.recent_hit:
                    del self.recent_hit[victim]

                self.policy.remove(victim)

                self.evictions += 1

                print(
                    f"{block:>2} -> MISS    "
                    f"Evict={victim}"
                )

            else:

                # Give victim second chance

                self.policy.remove(victim)

                self.policy.insert(victim)

                victim = self.policy.victim()

                self.history_table.add(victim)

                del self.lines[victim]

                if victim in self.recent_hit:
                    del self.recent_hit[victim]

                self.policy.remove(victim)

                self.evictions += 1

                print(
                    f"{block:>2} -> MISS    "
                    f"SecondChance "
                    f"Evict={victim}"
                )

        else:

            print(
                f"{block:>2} -> MISS"
            )

        self.lines[block] = CacheLine(block)

        self.recent_hit[block] = 0

        self.policy.insert(block)

    def get_stats(self):

        total = self.hits + self.misses

        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "hit_rate": round(self.hits / total, 4),
            "miss_rate": round(self.misses / total, 4)
        }

    def print_stats(self):

        stats = self.get_stats()

        print("\n ===== RESULTS =====")

        print(f"Hits      : {stats['hits']}")
        print(f"Misses    : {stats['misses']}")
        print(f"Evictions : {stats['evictions']}")
        print(f"Hit Rate  : {stats['hit_rate']:.2%}")
        print(f"Miss Rate : {stats['miss_rate']:.2%}")