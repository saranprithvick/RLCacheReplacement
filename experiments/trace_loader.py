from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = PROJECT_ROOT / "workloads" / "benchmark"


def load_trace(path):
    trace_path = Path(path)

    if not trace_path.is_absolute():
        trace_path = PROJECT_ROOT / trace_path

    with open(trace_path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def list_benchmark_traces():
    if not BENCHMARK_DIR.exists():
        return []

    return sorted(BENCHMARK_DIR.glob("*.txt"))


def benchmark_catalog():
    return {
        "stable_working_set.txt": {
            "dimension": "Recency",
            "description": "Stable working set that fits in cache",
        },
        "thrashing_cache_plus_one.txt": {
            "dimension": "Thrashing",
            "description": "Working set one block larger than cache",
        },
        "hot_set_scan.txt": {
            "dimension": "Pollution resistance",
            "description": "Hot set mixed with one-time scan",
        },
        "zipfian.txt": {
            "dimension": "Frequency / popularity",
            "description": "Zipfian skewed access distribution",
        },
        "phase_shift.txt": {
            "dimension": "Adaptation",
            "description": "Hot set changes between phases",
        },
    }


def trace_label(filename):
    meta = benchmark_catalog().get(filename, {})
    dimension = meta.get("dimension")

    if dimension:
        return f"{filename} ({dimension})"

    return filename
