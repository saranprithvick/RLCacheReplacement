| workload | dimension | cache_size | policy | episodes | hits | misses | evictions | hit_rate | miss_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stable_working_set | Recency | 2 | LRU | 1 | 0 | 80 | 78 | 0.0 | 1.0 |
| stable_working_set | Recency | 2 | RL-LRU | 50 | 22 | 58 | 56 | 0.275 | 0.725 |
| stable_working_set | Recency | 4 | LRU | 1 | 76 | 4 | 0 | 0.95 | 0.05 |
| stable_working_set | Recency | 4 | RL-LRU | 50 | 76 | 4 | 0 | 0.95 | 0.05 |
| stable_working_set | Recency | 8 | LRU | 1 | 76 | 4 | 0 | 0.95 | 0.05 |
| stable_working_set | Recency | 8 | RL-LRU | 50 | 76 | 4 | 0 | 0.95 | 0.05 |
| thrashing_cache_plus_one | Thrashing | 2 | LRU | 1 | 0 | 100 | 98 | 0.0 | 1.0 |
| thrashing_cache_plus_one | Thrashing | 2 | RL-LRU | 50 | 20 | 80 | 78 | 0.2 | 0.8 |
| thrashing_cache_plus_one | Thrashing | 4 | LRU | 1 | 0 | 100 | 96 | 0.0 | 1.0 |
| thrashing_cache_plus_one | Thrashing | 4 | RL-LRU | 50 | 48 | 52 | 48 | 0.48 | 0.52 |
| thrashing_cache_plus_one | Thrashing | 8 | LRU | 1 | 95 | 5 | 0 | 0.95 | 0.05 |
| thrashing_cache_plus_one | Thrashing | 8 | RL-LRU | 50 | 95 | 5 | 0 | 0.95 | 0.05 |
| hot_set_scan | Pollution resistance | 2 | LRU | 1 | 0 | 100 | 98 | 0.0 | 1.0 |
| hot_set_scan | Pollution resistance | 2 | RL-LRU | 50 | 21 | 79 | 77 | 0.21 | 0.79 |
| hot_set_scan | Pollution resistance | 4 | LRU | 1 | 72 | 28 | 24 | 0.72 | 0.28 |
| hot_set_scan | Pollution resistance | 4 | RL-LRU | 50 | 72 | 28 | 24 | 0.72 | 0.28 |
| hot_set_scan | Pollution resistance | 8 | LRU | 1 | 72 | 28 | 20 | 0.72 | 0.28 |
| hot_set_scan | Pollution resistance | 8 | RL-LRU | 50 | 72 | 28 | 20 | 0.72 | 0.28 |
| zipfian | Frequency / popularity | 2 | LRU | 1 | 79 | 121 | 119 | 0.395 | 0.605 |
| zipfian | Frequency / popularity | 2 | RL-LRU | 50 | 86 | 114 | 112 | 0.43 | 0.57 |
| zipfian | Frequency / popularity | 4 | LRU | 1 | 127 | 73 | 69 | 0.635 | 0.365 |
| zipfian | Frequency / popularity | 4 | RL-LRU | 50 | 128 | 72 | 68 | 0.64 | 0.36 |
| zipfian | Frequency / popularity | 8 | LRU | 1 | 175 | 25 | 17 | 0.875 | 0.125 |
| zipfian | Frequency / popularity | 8 | RL-LRU | 50 | 171 | 29 | 21 | 0.855 | 0.145 |
| phase_shift | Adaptation | 2 | LRU | 1 | 0 | 80 | 78 | 0.0 | 1.0 |
| phase_shift | Adaptation | 2 | RL-LRU | 50 | 8 | 72 | 70 | 0.1 | 0.9 |
| phase_shift | Adaptation | 4 | LRU | 1 | 72 | 8 | 4 | 0.9 | 0.1 |
| phase_shift | Adaptation | 4 | RL-LRU | 50 | 72 | 8 | 4 | 0.9 | 0.1 |
| phase_shift | Adaptation | 8 | LRU | 1 | 72 | 8 | 0 | 0.9 | 0.1 |
| phase_shift | Adaptation | 8 | RL-LRU | 50 | 72 | 8 | 0 | 0.9 | 0.1 |
