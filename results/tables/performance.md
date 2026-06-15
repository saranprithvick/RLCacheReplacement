| workload | dimension | cache_size | policy | episodes | hits | misses | evictions | hit_rate | miss_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stable_working_set | Recency | 2 | LRU | 1 | 0 | 80 | 78 | 0.0 | 1.0 |
| stable_working_set | Recency | 2 | RL-LRU | 50 | 13 | 67 | 65 | 0.1625 | 0.8375 |
| stable_working_set | Recency | 4 | LRU | 1 | 76 | 4 | 0 | 0.95 | 0.05 |
| stable_working_set | Recency | 4 | RL-LRU | 50 | 76 | 4 | 0 | 0.95 | 0.05 |
| stable_working_set | Recency | 8 | LRU | 1 | 76 | 4 | 0 | 0.95 | 0.05 |
| stable_working_set | Recency | 8 | RL-LRU | 50 | 76 | 4 | 0 | 0.95 | 0.05 |
| thrashing_cache_plus_one | Thrashing | 2 | LRU | 1 | 0 | 100 | 98 | 0.0 | 1.0 |
| thrashing_cache_plus_one | Thrashing | 2 | RL-LRU | 50 | 16 | 84 | 82 | 0.16 | 0.84 |
| thrashing_cache_plus_one | Thrashing | 4 | LRU | 1 | 0 | 100 | 96 | 0.0 | 1.0 |
| thrashing_cache_plus_one | Thrashing | 4 | RL-LRU | 50 | 28 | 72 | 68 | 0.28 | 0.72 |
| thrashing_cache_plus_one | Thrashing | 8 | LRU | 1 | 95 | 5 | 0 | 0.95 | 0.05 |
| thrashing_cache_plus_one | Thrashing | 8 | RL-LRU | 50 | 95 | 5 | 0 | 0.95 | 0.05 |
| hot_set_scan | Pollution resistance | 2 | LRU | 1 | 0 | 100 | 98 | 0.0 | 1.0 |
| hot_set_scan | Pollution resistance | 2 | RL-LRU | 50 | 18 | 82 | 80 | 0.18 | 0.82 |
| hot_set_scan | Pollution resistance | 4 | LRU | 1 | 72 | 28 | 24 | 0.72 | 0.28 |
| hot_set_scan | Pollution resistance | 4 | RL-LRU | 50 | 72 | 28 | 24 | 0.72 | 0.28 |
| hot_set_scan | Pollution resistance | 8 | LRU | 1 | 72 | 28 | 20 | 0.72 | 0.28 |
| hot_set_scan | Pollution resistance | 8 | RL-LRU | 50 | 74 | 26 | 18 | 0.74 | 0.26 |
| zipfian | Frequency / popularity | 2 | LRU | 1 | 79 | 121 | 119 | 0.395 | 0.605 |
| zipfian | Frequency / popularity | 2 | RL-LRU | 50 | 86 | 114 | 112 | 0.43 | 0.57 |
| zipfian | Frequency / popularity | 4 | LRU | 1 | 127 | 73 | 69 | 0.635 | 0.365 |
| zipfian | Frequency / popularity | 4 | RL-LRU | 50 | 119 | 81 | 77 | 0.595 | 0.405 |
| zipfian | Frequency / popularity | 8 | LRU | 1 | 175 | 25 | 17 | 0.875 | 0.125 |
| zipfian | Frequency / popularity | 8 | RL-LRU | 50 | 174 | 26 | 18 | 0.87 | 0.13 |
| phase_shift | Adaptation | 2 | LRU | 1 | 0 | 80 | 78 | 0.0 | 1.0 |
| phase_shift | Adaptation | 2 | RL-LRU | 50 | 10 | 70 | 68 | 0.125 | 0.875 |
| phase_shift | Adaptation | 4 | LRU | 1 | 72 | 8 | 4 | 0.9 | 0.1 |
| phase_shift | Adaptation | 4 | RL-LRU | 50 | 72 | 8 | 4 | 0.9 | 0.1 |
| phase_shift | Adaptation | 8 | LRU | 1 | 72 | 8 | 0 | 0.9 | 0.1 |
| phase_shift | Adaptation | 8 | RL-LRU | 50 | 72 | 8 | 0 | 0.9 | 0.1 |
