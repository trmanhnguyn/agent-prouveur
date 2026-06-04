import re
import json
from pathlib import Path

from src.mcp_invalidator.server import invalidate
from src.verifier.verify import read_graph6, verify_counterexample


CONJECTURE_DIR = Path("data/false_conjectures")
REPORT_DIR = Path("results/agent_reports")


def extract_conjecture_id(user_query: str) -> str | None:
    match = re.search(r"HDR-\d{3}", user_query.upper())
    if match:
        return match.group(0)
    return None


def load_conjecture(conjecture_id: str) -> dict:
    path = CONJECTURE_DIR / f"{conjecture_id}.json"

    if not path.exists():
        raise FileNotFoundError(f"Conjecture file not found: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def verify_known_counterexample(conjecture_id: str) -> dict:
    conjecture = load_conjecture(conjecture_id)

    g6 = conjecture["known_counterexample"]["value"]
    G = read_graph6(g6)

    return verify_counterexample(conjecture, G)


def generate_summary(conjecture_id: str, result: dict) -> str:
    status = result.get("status")

    if status == "counterexample_found":
        verification = result.get("result", {})
        invariants = verification.get("invariants", {})

        return f"""
Agent report for {conjecture_id}

Status: counterexample found.

The invalidator found a graph encoded in graph6 format:

{result.get("graph6")}

The independent verifier computed:

left_value = {verification.get("left_value")}
right_value = {verification.get("right_value")}
violated = {verification.get("violated")}

Graph invariants:
{json.dumps(invariants, indent=2)}

Conclusion:
The conjecture is invalidated because the generated graph satisfies the graph class constraints and violates the inequality.
""".strip()

    return f"""
Agent report for {conjecture_id}

Status: no counterexample found.

The invalidator did not find a counterexample within the current search budget.

Important:
This does not prove that the conjecture is true. It only means that no violating graph was found during the heuristic search.
""".strip()


def handle_query(user_query: str) -> str:
    conjecture_id = extract_conjecture_id(user_query)

    if conjecture_id is None:
        return "Please provide a conjecture ID, for example: HDR-001."

    result = invalidate(conjecture_id, max_iterations=20000)

    summary = generate_summary(conjecture_id, result)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"{conjecture_id}_agent_report.txt"
    report_path.write_text(summary, encoding="utf-8")

    return summary


def main():
    print("Minimal LLM-style agent for graph conjecture invalidation")
    print("Example: Try to invalidate HDR-001")
    print("Type 'exit' to quit.")

    while True:
        query = input("\n> ")

        if query.lower() in {"exit", "quit"}:
            break

        try:
            answer = handle_query(query)
            print("\n" + answer)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()