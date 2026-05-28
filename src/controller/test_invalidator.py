import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.invalidator.local_search import invalidate_conjecture


if __name__ == "__main__":
    result = invalidate_conjecture(
        conjecture_path="data/false_conjectures/HDR-001.json",
        max_iterations=20000,
    )

    print("=== INVALIDATOR RESULT ===")
    print(result)