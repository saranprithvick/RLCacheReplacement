from enum import Enum

class Action(Enum):
    EVICT = 0
    KEEP = 1

class RLAgent:

    def choose_action(self,state):
        
        recency_bucket = state["recency_bucket"]
        frequency_bucket = state["frequency_bucket"]

        if(frequency_bucket == 2):
            return Action.KEEP
        
        return Action.EVICT