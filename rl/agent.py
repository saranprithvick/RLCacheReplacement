import random
from collections import defaultdict
from enum import Enum


class Action(Enum):
    EVICT = 0
    KEEP = 1


class QLearningAgent:

    def __init__(
        self,
        alpha=0.1,
        gamma=0.9,
        epsilon=0.1
    ):

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.q_table = defaultdict(
            lambda: [0.0, 0.0]
        )

    def choose_action(self, state):

        if random.random() < self.epsilon:

            return random.choice(
                list(Action)
            )

        q_values = self.q_table[state]

        if q_values[0] >= q_values[1]:
            return Action.EVICT

        return Action.KEEP

    def update(
        self,
        state,
        action,
        reward,
        next_state
    ):

        action_idx = action.value

        current_q = (
            self.q_table[state]
            [action_idx]
        )

        max_next_q = max(
            self.q_table[next_state]
        )

        new_q = current_q + (
            self.alpha
            * (
                reward
                + self.gamma
                * max_next_q
                - current_q
            )
        )

        self.q_table[state][
            action_idx
        ] = new_q