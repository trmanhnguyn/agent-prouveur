import csv
from pathlib import Path

from src.mcp_invalidator.server import invalidate

CONJECTURES = ["HDR-001", "HDR-002", "HDR-003", "HDR-004", "HDR-005"]
STRATEGIES = ["edge_only", "mixed"]

MAX_ITERATIONS = 20000
MAX_ATTEMPTS = 5

RESULTS_PATH = Path("results/mutation_comparison.csv")


def run_attempts(conjecture_id: str, strategy: str) -> dict:
    best_result = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"{conjecture_id} | {strategy} | attempt {attempt}/{MAX_ATTEMPTS}")

        result = invalidate(
            conjecture_id,
            max_iterations=MAX_ITERATIONS,
            mutation_strategy=strategy,
        )

        best_result = result

        if result.get("status") == "counterexample_found":
            result["attempt"] = attempt
            return result

    best_result["attempt"] = MAX_ATTEMPTS
    return best_result


def main():
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for conjecture_id in CONJECTURES:
        for strategy in STRATEGIES:
            result = run_attempts(conjecture_id, strategy)

            rows.append({
                "conjecture_id": conjecture_id,
                "strategy": strategy,
                "status": result.get("status"),
                "attempt": result.get("attempt"),
                "iteration": result.get("iteration"),
                "best_score": result.get("best_score"),
                "graph6": result.get("graph6"),
            })

    with RESULTS_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Comparison saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()