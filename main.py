"""
Project entry point.

  python main.py              → quick LRU vs RL-LRU run (benchmark suite)
  python main.py compare ...  → systematic grid + CSV export
  python main.py analyze ...  → tables, plots, observations (Day 08)
"""

import sys

from experiments.analyze import main as analyze_main
from experiments.compare import main as compare_main
from experiments.run import main as run_main


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        sys.argv.pop(1)
        compare_main()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "analyze":
        sys.argv.pop(1)
        analyze_main()
        return

    run_main()


if __name__ == "__main__":
    main()
