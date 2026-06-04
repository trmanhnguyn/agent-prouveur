import csv
import json
from pathlib import Path

from src.mcp_invalidator.server import invalidate

CONJECTURES = [
    "HDR-001",
    "HDR-002",
]

RESULTS_CSV = Path("results/verification_results.csv")
RESULTS_JSON = Path("results/report.json")
COUNTEREXAMPLE_DIR = Path("data/counterexamples")


def main():
    RESULTS_CSV.parent.mkdir(exist_ok=True)
    COUNTEREXAMPLE_DIR.mkdir(exist_ok=True)

    rows = []
    report = {}

    for conjecture_id in CONJECTURES:
        print(f"Running {conjecture_id}...")

        result = invalidate(conjecture_id, max_iterations=20000)

        verification = result.get("result", {})
        invariants = verification.get("invariants", {})

        graph6 = result.get("graph6")

        if graph6:
            g6_path = COUNTEREXAMPLE_DIR / f"{conjecture_id}.g6"
            g6_path.write_text(graph6, encoding="utf-8")
        else:
            g6_path = ""

        row = {
            "id": conjecture_id,
            "status": result.get("status"),
            "iteration": result.get("iteration"),
            "graph6": graph6,
            "counterexample_file": str(g6_path),
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

        rows.append(row)

        report[conjecture_id] = {
            "status": result.get("status"),
            "iteration": result.get("iteration"),
            "graph6": graph6,
            "counterexample_file": str(g6_path),
            "verification": verification,
        }

    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    RESULTS_JSON.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"CSV results saved to {RESULTS_CSV}")
    print(f"JSON report saved to {RESULTS_JSON}")


if __name__ == "__main__":
    main()