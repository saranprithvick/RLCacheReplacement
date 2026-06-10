# Learned Q-Table Summary

| Workload | Dimension | Cache | State | EVICT | KEEP | Preferred |
| --- | --- | --- | --- | --- | --- | --- |
| hot_set_scan | Pollution resistance | 2 | (0, 0) | 9.6518 | 8.9996 | EVICT |
| hot_set_scan | Pollution resistance | 2 | (1, 0) | 9.7381 | 8.1797 | EVICT |
| hot_set_scan | Pollution resistance | 2 | (2, 0) | 9.1762 | 10.0 | KEEP |
| hot_set_scan | Pollution resistance | 2 | (2, 1) | 9.8507 | 2.2949 | EVICT |
| hot_set_scan | Pollution resistance | 4 | (0, 0) | 9.9966 | 8.1286 | EVICT |
| hot_set_scan | Pollution resistance | 4 | (2, 0) | 2.4894 | 0.0 | EVICT |
| hot_set_scan | Pollution resistance | 4 | (2, 1) | 9.9676 | 4.6585 | EVICT |
| hot_set_scan | Pollution resistance | 8 | (0, 0) | 9.9809 | 9.7682 | EVICT |
| hot_set_scan | Pollution resistance | 8 | (2, 1) | 9.9425 | 4.8132 | EVICT |
| phase_shift | Adaptation | 2 | (0, 0) | 9.5079 | 6.8137 | EVICT |
| phase_shift | Adaptation | 2 | (1, 0) | 9.6892 | 8.6495 | EVICT |
| phase_shift | Adaptation | 2 | (1, 1) | 0.8887 | 0.0 | EVICT |
| phase_shift | Adaptation | 2 | (2, 0) | 9.122 | 10.0 | KEEP |
| phase_shift | Adaptation | 2 | (2, 1) | 8.2794 | 0.0 | EVICT |
| phase_shift | Adaptation | 4 | (0, 0) | 1.4137 | 0.0 | EVICT |
| phase_shift | Adaptation | 4 | (2, 1) | 8.315 | 2.0265 | EVICT |
| phase_shift | Adaptation | 8 | — | — | — | — |
| stable_working_set | Recency | 2 | (0, 0) | 9.5542 | 3.6566 | EVICT |
| stable_working_set | Recency | 2 | (1, 0) | 9.5641 | 8.041 | EVICT |
| stable_working_set | Recency | 2 | (1, 1) | 0.7334 | 0.0 | EVICT |
| stable_working_set | Recency | 2 | (2, 0) | 9.1843 | 10.0 | KEEP |
| stable_working_set | Recency | 2 | (2, 1) | 9.6447 | 3.2063 | EVICT |
| stable_working_set | Recency | 4 | — | — | — | — |
| stable_working_set | Recency | 8 | — | — | — | — |
| thrashing_cache_plus_one | Thrashing | 2 | (0, 0) | 9.9762 | 7.8625 | EVICT |
| thrashing_cache_plus_one | Thrashing | 2 | (1, 0) | 9.9993 | 8.5374 | EVICT |
| thrashing_cache_plus_one | Thrashing | 2 | (2, 0) | 9.5292 | 10.0 | KEEP |
| thrashing_cache_plus_one | Thrashing | 2 | (2, 1) | 9.6904 | 0.0 | EVICT |
| thrashing_cache_plus_one | Thrashing | 4 | (0, 0) | 0.559 | 7.8076 | KEEP |
| thrashing_cache_plus_one | Thrashing | 4 | (1, 0) | 1.7077 | 9.1037 | KEEP |
| thrashing_cache_plus_one | Thrashing | 4 | (1, 1) | 4.8005 | 0.3157 | EVICT |
| thrashing_cache_plus_one | Thrashing | 4 | (2, 0) | 6.5148 | 10.0 | KEEP |
| thrashing_cache_plus_one | Thrashing | 4 | (2, 1) | 5.8785 | 8.633 | KEEP |
| thrashing_cache_plus_one | Thrashing | 8 | — | — | — | — |
| zipfian | Frequency / popularity | 2 | (0, 0) | 7.43 | 6.4546 | EVICT |
| zipfian | Frequency / popularity | 2 | (1, 0) | 8.149 | 6.2682 | EVICT |
| zipfian | Frequency / popularity | 2 | (1, 1) | 6.8495 | 2.7269 | EVICT |
| zipfian | Frequency / popularity | 2 | (2, 0) | 7.786 | 7.1042 | EVICT |
| zipfian | Frequency / popularity | 2 | (2, 1) | 7.3984 | 8.1755 | KEEP |
| zipfian | Frequency / popularity | 4 | (0, 0) | 4.5333 | 8.6097 | KEEP |
| zipfian | Frequency / popularity | 4 | (1, 0) | 8.766 | 5.1606 | EVICT |
| zipfian | Frequency / popularity | 4 | (1, 1) | 7.3018 | 8.492 | KEEP |
| zipfian | Frequency / popularity | 4 | (2, 0) | 8.668 | 8.4132 | EVICT |
| zipfian | Frequency / popularity | 4 | (2, 1) | 7.9517 | 8.1908 | KEEP |
| zipfian | Frequency / popularity | 8 | (0, 0) | 2.6724 | 6.9249 | KEEP |
| zipfian | Frequency / popularity | 8 | (1, 1) | 2.9743 | 6.2191 | KEEP |
| zipfian | Frequency / popularity | 8 | (2, 0) | 5.1498 | 7.0018 | KEEP |
| zipfian | Frequency / popularity | 8 | (2, 1) | 6.6331 | 4.4528 | EVICT |
