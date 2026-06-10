from simulator.cache_line import CacheLine
from rl.history_table import HistoryTable


class Cache:

    def __init__(self, size, policy, verbose=True):

        self.size = size
        self.policy = policy
        self.verbose = verbose

        self.lines = {}
        self.access_frequency = {}

        self.hits = 0
        self.misses = 0
        self.evictions = 0

        self.recent_hit = {}

        # Q-learning bookkeeping
        self.pending_state = None
        self.pending_action = None
        self.pending_victim = None

        self.history_table = HistoryTable()

    def _log(self, message):

        if self.verbose:
            print(message)

    def _resolve_pending_transition(self, block, next_state=None):

        if not hasattr(self.policy, "agent"):
            return

        if self.pending_state is None:
            return

        if block == self.pending_victim:
            reward = -1
        else:
            reward = +1

        bootstrap_state = (
            next_state
            if next_state is not None
            else self.pending_state
        )

        self.policy.agent.update(
            self.pending_state,
            self.pending_action,
            reward,
            bootstrap_state,
        )

        self.pending_state = None
        self.pending_action = None
        self.pending_victim = None

    def access(self, block):

        self.access_frequency[block] = (
            self.access_frequency.get(block, 0) + 1
        )

        is_hit = block in self.lines

        # ----------------------------------
        # HIT
        # ----------------------------------

        if is_hit:

            self._resolve_pending_transition(block)

            self.hits += 1

            self.recent_hit[block] = 1

            self.policy.access(block)

            self._log(
                f"{block:>2} -> HIT   "
                f"Cache={list(self.lines.keys())}"
            )

            return

        # ----------------------------------
        # MISS
        # ----------------------------------

        self.misses += 1

        next_state = None

        if len(self.lines) >= self.size:

            # ----------------------------------
            # RL-LRU PATH
            # ----------------------------------

            if hasattr(self.policy, "agent"):

                cache_lines = []

                for block_name in self.policy.lru.order:

                    cache_lines.append(
                        {
                            "block": block_name,
                            "frequency": self.access_frequency.get(
                                block_name, 0
                            ),
                            "recent_hit": self.recent_hit.get(
                                block_name, 0
                            ),
                        }
                    )

                candidate, state, action = (
                    self.policy.select_victim(cache_lines)
                )

                next_state = state

                self._resolve_pending_transition(
                    block,
                    next_state=next_state,
                )

                victim = candidate["block"]

                self.pending_state = state
                self.pending_action = action

                self._log(
                    f"Candidate={victim} "
                    f"State={state} "
                    f"Action={action.name}"
                )

                # -------------------------
                # EVICT
                # -------------------------

                if action.name == "EVICT":

                    self.pending_victim = victim

                    self.history_table.add(victim)

                    del self.lines[victim]

                    self.recent_hit.pop(victim, None)

                    self.policy.remove(victim)

                    self.evictions += 1

                    self._log(
                        f"{block:>2} -> MISS    "
                        f"Evict={victim}"
                    )

                # -------------------------
                # KEEP
                # -------------------------

                else:

                    protected = victim

                    self.policy.remove(protected)
                    self.policy.insert(protected)

                    victim = self.policy.victim()

                    self.pending_victim = victim

                    self.history_table.add(victim)

                    del self.lines[victim]

                    self.recent_hit.pop(victim, None)

                    self.policy.remove(victim)

                    self.evictions += 1

                    self._log(
                        f"{block:>2} -> MISS    "
                        f"SecondChance "
                        f"Evict={victim}"
                    )

            # ----------------------------------
            # PURE LRU PATH
            # ----------------------------------

            else:

                victim = self.policy.victim()

                del self.lines[victim]

                self.policy.remove(victim)

                self.evictions += 1

                self._log(
                    f"{block:>2} -> MISS    "
                    f"Evict={victim}"
                )

        else:

            self._resolve_pending_transition(block)

            self._log(f"{block:>2} -> MISS")

        # ----------------------------------
        # Insert New Block
        # ----------------------------------

        self.lines[block] = CacheLine(block)

        self.recent_hit[block] = 0

        self.history_table.remove(block)

        self.policy.insert(block)

    def get_stats(self):

        total = self.hits + self.misses

        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "hit_rate": round(
                self.hits / total,
                4
            ),
            "miss_rate": round(
                self.misses / total,
                4
            ),
        }

    def print_stats(self):

        stats = self.get_stats()

        print("\n===== RESULTS =====")

        print(
            f"Hits      : {stats['hits']}"
        )

        print(
            f"Misses    : {stats['misses']}"
        )

        print(
            f"Evictions : {stats['evictions']}"
        )

        print(
            f"Hit Rate  : "
            f"{stats['hit_rate']:.2%}"
        )

        print(
            f"Miss Rate : "
            f"{stats['miss_rate']:.2%}"
        )
