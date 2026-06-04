import csv
import json
from pathlib import Path

from src.mcp_invalidator.server import invalidate

CONJECTURES = [
    "HDR-001",
    "HDR-002",
    "HDR-003",
    "HDR-004",
    "HDR-005",
]

MAX_ITERATIONS = 20000
MAX_ATTEMPTS = 5

RESULTS_CSV = Path("results/verification_results.csv")
RESULTS_JSON = Path("results/report.json")
COUNTEREXAMPLE_DIR = Path("data/counterexamples")


def run_with_retries(conjecture_id: str) -> dict:
    """
    Run the invalidator several times because local search is stochastic.
    Stop as soon as a counterexample is found.
    """
    best_result = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Attempt {attempt}/{MAX_ATTEMPTS} for {conjecture_id}")

        result = invalidate(
            conjecture_id,
            max_iterations=MAX_ITERATIONS,
        )

        best_result = result

        if result.get("status") == "counterexample_found":
            print(f"Counterexample found for {conjecture_id}")
            break

    return best_result or {
        "status": "error",
        "conjecture_id": conjecture_id,
        "message": "No result returned by invalidator",
    }


def save_counterexample(conjecture_id: str, graph6: str | None) -> str:
    """
    Save a graph6 counterexample into data/counterexamples.
    """
    if not graph6:
        return ""

    COUNTEREXAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    path = COUNTEREXAMPLE_DIR / f"{conjecture_id}.g6"
    path.write_text(graph6, encoding="utf-8")

    return str(path)


def build_row(conjecture_id: str, result: dict) -> dict:
    """
    Convert one invalidator result into a CSV row.
    """
    verification = result.get("result") or {}
    invariants = verification.get("invariants") or {}

    graph6 = result.get("graph6")
    counterexample_file = save_counterexample(conjecture_id, graph6)

    return {
        "id": conjecture_id,
        "status": result.get("status"),
        "iteration": result.get("iteration"),
        "graph6": graph6,
        "counterexample_file": counterexample_file,
        "left_value": verification.get("left_value"),
        "right_value": verification.get("right_value"),
        "violated": verification.get("violated"),
        "n": invariants.get("n"),
        "m": invariants.get("m"),
        "density": invariants.get("density"),
        "rad": invariants.get("rad"),
        "diam": invariants.get("diam"),
        "avg": invariants.get("avg"),
        "delta": invariants.get("delta"),
        "Delta": invariants.get("Delta"),
    }


def main() -> None:
    RESULTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    COUNTEREXAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    report = {}

    for conjecture_id in CONJECTURES:
        print("=" * 60)
        print(f"Running {conjecture_id}")

        result = run_with_retries(conjecture_id)
        row = build_row(conjecture_id, result)

        rows.append(row)

        report[conjecture_id] = {
            "status": result.get("status"),
            "iteration": result.get("iteration"),
            "graph6": result.get("graph6"),
            "counterexample_file": row.get("counterexample_file"),
            "verification": result.get("result") or {},
        }

    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    RESULTS_JSON.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 60)
    print(f"CSV results saved to {RESULTS_CSV}")
    print(f"JSON report saved to {RESULTS_JSON}")


if __name__ == "__main__":
    main()