# Experiment Observations

## Overall (all cache sizes)

- RL-LRU better: **7** configurations
- LRU better: **1** configurations
- Tied: **7** configurations

## Primary analysis (cache size = 4)

### Where RL-LRU helps

- **thrashing_cache_plus_one** (Thrashing): 0.0% → 48.0% (Δ +48.0%)
- **zipfian** (Frequency / popularity): 63.5% → 64.0% (Δ +0.5%)

### Where LRU is better

- LRU does not beat RL-LRU at the primary cache size.

### Ties

- **stable_working_set** (Recency): identical hit rate
- **hot_set_scan** (Pollution resistance): identical hit rate
- **phase_shift** (Adaptation): identical hit rate

## Anomalies

- **Small cache (size < 4):** RL-LRU often looks better than LRU, but the benchmark suite was designed around a 4-way cache. Treat size-2 results as noisy.
- **Thrashing @ cache 4:** LRU hit rate is 0% (expected for a cache+1 loop), while RL-LRU improves via second-chance decisions. Worth discussing as the most interesting RL case.

## Takeaways for the meeting

- RL-LRU is built as a layer on top of LRU, not a replacement.
- Gains are workload-dependent; many benchmarks tie at cache size 4.
- The Q-table summary shows which states learned to EVICT vs KEEP.
- Professors care more about *when* RL helps than always beating LRU.
