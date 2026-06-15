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
    """EVICT action should remove the LRU candidate."""
    agent = QLearningAgent(epsilon=0.0)
    state = (0, 0)
    agent.q_table[state] = [10.0, 0.0]

    cache = _make_cache(agent)
    _warm_cache(cache)

    cache.access("E")

    assert "C" not in cache.lines
    assert "E" in cache.lines
    # C should now be in the ghost cache
    assert cache.history_table.was_evicted("C")


def test_keep_action_gives_second_chance():
    """KEEP action should protect the LRU candidate
    and evict the next-oldest block instead."""
    agent = QLearningAgent(epsilon=0.0)
    state = (0, 0)
    agent.q_table[state] = [0.0, 10.0]

    cache = _make_cache(agent)
    _warm_cache(cache)

    cache.access("E")

    assert "C" in cache.lines
    assert "D" not in cache.lines
    assert "E" in cache.lines
    # D should be in the ghost cache (not C)
    assert cache.history_table.was_evicted("D")
    assert not cache.history_table.was_evicted("C")


def test_near_miss_penalty():
    """When an evicted block is re-requested while
    still in the ghost cache, issue a -1 penalty."""
    agent = QLearningAgent(
        alpha=1.0,
        gamma=0.0,
        epsilon=0.0,
    )
    state = (0, 0)
    agent.q_table[state] = [10.0, 0.0]

    cache = _make_cache(agent)
    _warm_cache(cache)

    # Evict C
    cache.access("E")
    assert cache.history_table.was_evicted("C")

    # Request C again — near-miss in ghost cache
    cache.access("C")

    # The agent should have been penalized
    assert agent.q_table[state][Action.EVICT.value] == -1.0
    # C should no longer be in the ghost cache
    assert not cache.history_table.was_evicted("C")


def test_expiration_reward():
    """When a block expires from the ghost cache
    (never re-requested), issue a +1 reward."""
    agent = QLearningAgent(
        alpha=1.0,
        gamma=0.0,
        epsilon=0.0,
    )
    state = (0, 0)
    agent.q_table[state] = [0.0, 0.0]

    # Use a small cache (size=2) so the ghost cache
    # capacity is 2*2=4, easier to overflow.
    cache = _make_cache(agent, size=2)

    # Fill cache: [A, B]
    cache.access("A")
    cache.access("B")

    # Miss C -> evict A (LRU), ghost = {A}
    cache.access("C")
    assert cache.history_table.was_evicted("A")

    # Miss D -> evict B, ghost = {A, B}
    cache.access("D")

    # Miss E -> evict C, ghost = {A, B, C}
    cache.access("E")

    # Miss F -> evict D, ghost = {A, B, C, D}
    cache.access("F")

    # Ghost is now at capacity (4).
    # Next eviction should expire A from the ghost
    # and trigger a +1 reward for A's eviction.
    q_before = agent.q_table[state][Action.EVICT.value]

    cache.access("G")

    # A should have expired and been rewarded
    assert not cache.history_table.was_evicted("A")

    q_after = agent.q_table[state][Action.EVICT.value]
    assert q_after > q_before, (
        f"Expected positive reward update: "
        f"q_before={q_before}, q_after={q_after}"
    )


def test_history_table_clears_on_reinsert():
    """When an evicted block is re-inserted into the
    cache, it should be removed from the ghost cache."""
    agent = QLearningAgent(epsilon=0.0)
    state = (0, 0)
    agent.q_table[state] = [10.0, 0.0]

    cache = _make_cache(agent)
    _warm_cache(cache)

    cache.access("E")
    assert cache.history_table.was_evicted("C")

    # C is re-requested (miss), gets re-inserted
    cache.access("C")
    assert not cache.history_table.was_evicted("C")


def test_ghost_cache_capacity():
    """Ghost cache should not exceed 2x cache size."""
    agent = QLearningAgent(epsilon=0.0)
    state = (0, 0)
    agent.q_table[state] = [10.0, 0.0]

    cache = _make_cache(agent, size=2)

    # Fill cache
    cache.access("A")
    cache.access("B")

    # Cause evictions to fill ghost cache
    unique_blocks = ["C", "D", "E", "F", "G", "H", "I"]
    for b in unique_blocks:
        cache.access(b)

    # Ghost cache should never exceed capacity (2*2=4)
    assert len(cache.history_table.evicted) <= 4, (
        f"Ghost cache size {len(cache.history_table.evicted)} "
        f"exceeds capacity 4"
    )


if __name__ == "__main__":
    test_evict_action_removes_lru_candidate()
    test_keep_action_gives_second_chance()
    test_near_miss_penalty()
    test_expiration_reward()
    test_history_table_clears_on_reinsert()
    test_ghost_cache_capacity()
    print("\nAll RL-LRU tests passed!")
