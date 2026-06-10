from simulator.cache import Cache
from rl.agent import QLearningAgent, Action
from policies.rl_lru import RLLRUPolicy


def _make_cache(agent, size=4):
    return Cache(
        size=size,
        policy=RLLRUPolicy(agent),
        verbose=False,
    )


def _warm_cache(cache):
    for block in ["A", "B", "C", "D", "A", "B"]:
        cache.access(block)


def test_evict_action_removes_lru_candidate():
    agent = QLearningAgent(epsilon=0.0)
    state = (0, 0)
    agent.q_table[state] = [10.0, 0.0]

    cache = _make_cache(agent)
    _warm_cache(cache)

    cache.access("E")

    assert "C" not in cache.lines
    assert "E" in cache.lines
    assert cache.pending_victim == "C"
    assert cache.pending_action == Action.EVICT


def test_keep_action_gives_second_chance():
    agent = QLearningAgent(epsilon=0.0)
    state = (0, 0)
    agent.q_table[state] = [0.0, 10.0]

    cache = _make_cache(agent)
    _warm_cache(cache)

    cache.access("E")

    assert "C" in cache.lines
    assert "D" not in cache.lines
    assert "E" in cache.lines
    assert cache.pending_victim == "D"
    assert cache.pending_action == Action.KEEP


def test_reward_negative_when_evicted_block_is_referenced():
    agent = QLearningAgent(
        alpha=1.0,
        gamma=0.0,
        epsilon=0.0,
    )
    state = (0, 0)
    agent.q_table[state] = [10.0, 0.0]

    cache = _make_cache(agent)
    _warm_cache(cache)

    cache.access("E")
    assert cache.pending_victim == "C"

    cache.access("C")

    assert agent.q_table[state][Action.EVICT.value] == -1.0
    assert cache.pending_victim is not None


def test_reward_positive_when_other_block_hits():
    agent = QLearningAgent(
        alpha=1.0,
        gamma=0.0,
        epsilon=0.0,
    )
    state = (0, 0)
    agent.q_table[state] = [10.0, 0.0]

    cache = _make_cache(agent)
    _warm_cache(cache)

    cache.access("E")

    cache.access("A")

    assert agent.q_table[state][Action.EVICT.value] == 1.0
    assert cache.pending_state is None


def test_history_table_clears_on_reinsert():
    agent = QLearningAgent(epsilon=0.0)
    state = (0, 0)
    agent.q_table[state] = [10.0, 0.0]

    cache = _make_cache(agent)
    _warm_cache(cache)

    cache.access("E")
    assert cache.history_table.was_evicted("C")

    cache.access("C")
    assert not cache.history_table.was_evicted("C")


if __name__ == "__main__":
    test_evict_action_removes_lru_candidate()
    test_keep_action_gives_second_chance()
    test_reward_negative_when_evicted_block_is_referenced()
    test_reward_positive_when_other_block_hits()
    test_history_table_clears_on_reinsert()
    print("\nAll RL-LRU tests passed!")
