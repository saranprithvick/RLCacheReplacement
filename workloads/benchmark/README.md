# Benchmark Suite

Five workloads covering the main dimensions cache replacement policies are evaluated on.
Designed for a default **4-way** cache; use `generate.py` to regenerate traces.

| File | Dimension | What it tests |
|------|-----------|---------------|
| `stable_working_set.txt` | Recency | Same small set reused continuously; working set fits in cache |
| `thrashing_cache_plus_one.txt` | Thrashing | 5 blocks in a loop vs 4-way cache; continuous eviction/reload |
| `hot_set_scan.txt` | Pollution resistance | Hot A–D blocks mixed with a one-time cold scan |
| `zipfian.txt` | Frequency / popularity | Zipfian skew — few blocks accessed much more often |
| `phase_shift.txt` | Adaptation over time | Hot set shifts from A–D to W–Z mid-trace |

Regenerate:

```bash
PYTHONPATH=. python3 workloads/benchmark/generate.py
```
