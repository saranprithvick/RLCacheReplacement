from simulator.cache import Cache
from policies.lru import LRUPolicy

def test_lru():

    trace = [
        'A','B','C','D',
        'A','B',
        'E',
        'A','B',
        'C','D','E'
    ]

    cache = Cache(
        size = 4,
        policy = LRUPolicy()
    )

    for block in trace:
        cache.access(block)

    stats = cache.get_stats()

    assert stats["hits"] == 4
    assert stats["misses"] == 8
    assert stats["evictions"] == 4

    print("\n Test Passed !")

if __name__ == "__main__":
    test_lru()