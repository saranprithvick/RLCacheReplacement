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

        # Ghost Cache: bounded eviction history
        # sized at 2x cache capacity
        self.history_table = HistoryTable(
            capacity=2 * size
        )

    def _is_rl_policy(self):

        return hasattr(self.policy, "agent")

    def _reward_expired(self, expired, current_state):
        """Issue a positive reward for a block that expired
        from the history table without being re-requested.
        This means the eviction was a good decision."""

        if expired is None:
            return

        if not self._is_rl_policy():
            return

        _expired_block, (exp_state, exp_action) = expired

        if exp_state is None:
            return

        bootstrap_state = (
            current_state
            if current_state is not None
            else exp_state
        )

        self.policy.agent.update(
            exp_state,
            exp_action,
            +1,
            bootstrap_state,
        )

    def _reward_near_miss(self, meta, current_state):
        """Issue a negative reward for a block that was
        re-requested while still in the history table.
        This means the eviction was premature."""

        if meta is None:
            return

        if not self._is_rl_policy():
            return

        near_state, near_action = meta

        if near_state is None:
            return

        bootstrap_state = (
            current_state
            if current_state is not None
            else near_state
        )

        self.policy.agent.update(
            near_state,
            near_action,
            -1,
            bootstrap_state,
        )

    def _log(self, message):

        if self.verbose:
            print(message)

    def access(self, block):

        self.access_frequency[block] = (
            self.access_frequency.get(block, 0) + 1
        )

        is_hit = block in self.lines

        # ----------------------------------
        # HIT
        # ----------------------------------

        if is_hit:

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

        # Check if this missed block is in the
        # ghost cache (near-miss detection)
        near_miss_meta = self.history_table.remove(
            block
        )

        if len(self.lines) >= self.size:

            # ----------------------------------
            # RL-LRU PATH
            # ----------------------------------

            if self._is_rl_policy():

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

                # Resolve the near-miss penalty using
                # the current state as bootstrap
                self._reward_near_miss(
                    near_miss_meta, state
                )

                victim = candidate["block"]

                self._log(
                    f"Candidate={victim} "
                    f"State={state} "
                    f"Action={action.name}"
                )

                # -------------------------
                # EVICT
                # -------------------------

                if action.name == "EVICT":

                    expired = self.history_table.add(
                        victim, state, action
                    )

                    # Reward the expired block
                    # (it was never re-requested)
                    self._reward_expired(expired, state)

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

                    expired = self.history_table.add(
                        victim, state, action
                    )

                    # Reward the expired block
                    self._reward_expired(expired, state)

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

            # Cache not full yet, resolve any
            # near-miss from the ghost cache
            if self._is_rl_policy():
                self._reward_near_miss(
                    near_miss_meta, None
                )

            self._log(f"{block:>2} -> MISS")

        # ----------------------------------
        # Insert New Block
        # ----------------------------------

        self.lines[block] = CacheLine(block)

        self.recent_hit[block] = 0

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
