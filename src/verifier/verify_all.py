import csv
import json
from pathlib import Path
from verify import read_graph6, verify_counterexample


DATA_DIR = Path("data/false_conjectures")
RESULTS_DIR = Path("results")
OUTPUT_FILE = RESULTS_DIR / "verification_results.csv"


if __name__ == "__main__":
    RESULTS_DIR.mkdir(exist_ok=True)

    rows = []

    for file_path in DATA_DIR.glob("*.json"):
        with open(file_path) as f:
            conjecture = json.load(f)

        g6 = conjecture["known_counterexample"]["value"]
        G = read_graph6(g6)

        result = verify_counterexample(conjecture, G)

        rows.append({
            "id": result["conjecture_id"],
            "left_value": result["left_value"],
            "right_value": result["right_value"],
            "violated": result["violated"],
            "n": result["invariants"]["n"],
            "m": result["invariants"]["m"],
            "density": result["invariants"]["density"],
            "rad": result["invariants"]["rad"],
            "diam": result["invariants"]["diam"],
            "avg": result["invariants"]["avg"],
            "delta": result["invariants"]["delta"],
            "Delta": result["invariants"]["Delta"],
        })

    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Results saved to {OUTPUT_FILE}")