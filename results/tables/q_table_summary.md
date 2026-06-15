# Learned Q-Table Summary

| Workload | Dimension | Cache | State | EVICT | KEEP | Preferred |
| --- | --- | --- | --- | --- | --- | --- |
| hot_set_scan | Pollution resistance | 2 | (0, 0) | -2.2577 | -1.9573 | KEEP |
| hot_set_scan | Pollution resistance | 2 | (1, 0) | -5.4213 | -5.1229 | KEEP |
| hot_set_scan | Pollution resistance | 2 | (1, 1) | -1.7252 | -1.3057 | KEEP |
| hot_set_scan | Pollution resistance | 2 | (2, 0) | -5.5256 | -3.1071 | KEEP |
| hot_set_scan | Pollution resistance | 2 | (2, 1) | -5.1643 | -5.4538 | EVICT |
| hot_set_scan | Pollution resistance | 4 | (0, 0) | 9.6519 | 8.5401 | EVICT |
| hot_set_scan | Pollution resistance | 4 | (2, 0) | 2.7408 | 0.0 | EVICT |
| hot_set_scan | Pollution resistance | 4 | (2, 1) | 9.5778 | 6.7663 | EVICT |
| hot_set_scan | Pollution resistance | 8 | (0, 0) | 0.0 | -0.1 | EVICT |
| hot_set_scan | Pollution resistance | 8 | (2, 1) | -0.9995 | -0.9994 | KEEP |
| phase_shift | Adaptation | 2 | (0, 0) | -8.6193 | -8.6365 | EVICT |
| phase_shift | Adaptation | 2 | (1, 0) | -8.7625 | -8.7945 | EVICT |
| phase_shift | Adaptation | 2 | (1, 1) | -7.4895 | -7.5342 | EVICT |
| phase_shift | Adaptation | 2 | (2, 0) | -8.8878 | -8.8807 | KEEP |
| phase_shift | Adaptation | 2 | (2, 1) | -8.3593 | -8.3641 | EVICT |
| phase_shift | Adaptation | 4 | (0, 0) | -0.4387 | -0.3439 | KEEP |
| phase_shift | Adaptation | 4 | (2, 1) | 0.0 | -0.3917 | EVICT |
| phase_shift | Adaptation | 8 | — | — | — | — |
| stable_working_set | Recency | 2 | (0, 0) | -8.2703 | -8.3064 | EVICT |
| stable_working_set | Recency | 2 | (1, 0) | -9.3779 | -9.3832 | EVICT |
| stable_working_set | Recency | 2 | (1, 1) | -7.9082 | -7.9003 | KEEP |
| stable_working_set | Recency | 2 | (2, 0) | -9.9512 | -9.9511 | KEEP |
| stable_working_set | Recency | 2 | (2, 1) | -9.7293 | -9.7298 | EVICT |
| stable_working_set | Recency | 4 | — | — | — | — |
| stable_working_set | Recency | 8 | — | — | — | — |
| thrashing_cache_plus_one | Thrashing | 2 | (0, 0) | -9.3142 | -9.1581 | KEEP |
| thrashing_cache_plus_one | Thrashing | 2 | (1, 0) | -9.7898 | -9.8128 | EVICT |
| thrashing_cache_plus_one | Thrashing | 2 | (1, 1) | -7.6101 | -7.4513 | KEEP |
| thrashing_cache_plus_one | Thrashing | 2 | (2, 0) | -9.9024 | -9.9049 | EVICT |
| thrashing_cache_plus_one | Thrashing | 2 | (2, 1) | -9.7588 | -9.7881 | EVICT |
| thrashing_cache_plus_one | Thrashing | 4 | (0, 0) | -7.7782 | -7.6605 | KEEP |
| thrashing_cache_plus_one | Thrashing | 4 | (1, 0) | -8.6256 | -8.7562 | EVICT |
| thrashing_cache_plus_one | Thrashing | 4 | (1, 1) | -7.3793 | -7.4867 | EVICT |
| thrashing_cache_plus_one | Thrashing | 4 | (2, 0) | -9.9908 | -9.9909 | EVICT |
| thrashing_cache_plus_one | Thrashing | 4 | (2, 1) | -9.9901 | -9.9902 | EVICT |
| thrashing_cache_plus_one | Thrashing | 8 | — | — | — | — |
| zipfian | Frequency / popularity | 2 | (0, 0) | -1.8008 | -2.421 | EVICT |
| zipfian | Frequency / popularity | 2 | (1, 0) | -2.0341 | -2.4309 | EVICT |
| zipfian | Frequency / popularity | 2 | (1, 1) | -2.5453 | -2.8053 | EVICT |
| zipfian | Frequency / popularity | 2 | (2, 0) | -2.0415 | -2.7732 | EVICT |
| zipfian | Frequency / popularity | 2 | (2, 1) | -2.7336 | -2.8408 | EVICT |
| zipfian | Frequency / popularity | 4 | (0, 0) | -9.7068 | -9.6854 | KEEP |
| zipfian | Frequency / popularity | 4 | (1, 0) | -9.7362 | -9.7253 | KEEP |
| zipfian | Frequency / popularity | 4 | (1, 1) | -9.6242 | -9.6399 | EVICT |
| zipfian | Frequency / popularity | 4 | (2, 0) | -9.776 | -9.7762 | EVICT |
| zipfian | Frequency / popularity | 4 | (2, 1) | -9.7712 | -9.7709 | KEEP |
| zipfian | Frequency / popularity | 8 | (0, 0) | -6.2197 | -6.3383 | EVICT |
| zipfian | Frequency / popularity | 8 | (1, 1) | -7.0577 | -7.1129 | EVICT |
| zipfian | Frequency / popularity | 8 | (2, 0) | -7.3286 | -7.2969 | KEEP |
| zipfian | Frequency / popularity | 8 | (2, 1) | -7.3651 | -7.3555 | KEEP |
