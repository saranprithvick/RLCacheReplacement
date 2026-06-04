from rl.agent import Action


class RLLRUPolicy:

    def __init__(self, agent):
        self.agent = agent

    def select_victim(self, cache_lines):

        """
        cache_lines:
        [
            {
                "block": "A",
                "frequency": 5
            },
            ...
        ]

        LRU block is index 0
        """

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

        recency_bucket = 0

        frequency_bucket = self.get_frequency_bucket(
            candidate["frequency"]
        )

        return {
            "recency_bucket": recency_bucket,
            "frequency_bucket": frequency_bucket
        }

    def get_frequency_bucket(self, freq):

        if freq <= 1:
            return 0

        elif freq <= 3:
            return 1

        return 2