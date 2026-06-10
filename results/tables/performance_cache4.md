| workload | dimension | cache_size | lru_hit_rate | rl_hit_rate | delta_hit_rate | winner |
| --- | --- | --- | --- | --- | --- | --- |
| stable_working_set | Recency | 4 | 0.95 | 0.95 | +0.0000 | tie |
| thrashing_cache_plus_one | Thrashing | 4 | 0.0 | 0.48 | +0.4800 | RL-LRU |
| hot_set_scan | Pollution resistance | 4 | 0.72 | 0.72 | +0.0000 | tie |
| zipfian | Frequency / popularity | 4 | 0.635 | 0.64 | +0.0050 | RL-LRU |
| phase_shift | Adaptation | 4 | 0.9 | 0.9 | +0.0000 | tie |
