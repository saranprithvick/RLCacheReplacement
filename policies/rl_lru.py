from rl.agent import Action
from policies.lru import LRUPolicy


class RLLRUPolicy:

    def __init__(self, agent):

        self.agent = agent

        # Internal LRU policy
        self.lru = LRUPolicy()

    # ------------------
    # LRU Interface
    # ------------------

    def access(self, block):
        self.lru.access(block)

    def insert(self, block):
        self.lru.insert(block)

    def remove(self, block):
        self.lru.remove(block)

    def victim(self):
        return self.lru.victim()

    # ------------------
    # RL Logic
    # ------------------

    def select_victim(self, cache_lines):

        candidate = cache_lines[0]

        state = self.build_state(
            candidate,
            cache_lines
        )

        action = self.agent.choose_action(state)

        return candidate, state, action

    def build_state(
        self,
        candidate,
        cache_lines
    ):

        frequency_bucket = self.get_frequency_bucket(
            candidate["frequency"]
        )

        recent_hit_bucket = candidate["recent_hit"]

        # IMPORTANT:
        # tuple, not dict
        return (
            frequency_bucket,
            recent_hit_bucket
        )

    def get_frequency_bucket(self, freq):

        if freq <= 1:
            return 0

        elif freq <= 3:
            return 1

        return 2