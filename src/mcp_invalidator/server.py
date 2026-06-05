import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.invalidator.local_search import invalidate_conjecture


mcp = FastMCP("Graph Conjecture Invalidator")


@mcp.tool()
def invalidate(
    conjecture_id: str,
    max_iterations: int = 20000,
    mutation_strategy: str = "mixed",
) -> dict:
    """
    Try to find a counterexample for a graph theory conjecture.

    Args:
        conjecture_id: Example "HDR-001"
        max_iterations: Maximum number of local search iterations
        mutation_strategy:
            - "edge_only": only add/remove edges
            - "structured": only structured mutations
            - "mixed": edge + structured mutations

    Returns:
        A dictionary containing the status, counterexample if found, and verification result.
    """
    conjecture_path = f"data/false_conjectures/{conjecture_id}.json"

    if not Path(conjecture_path).exists():
        return {
            "status": "error",
            "message": f"Conjecture file not found: {conjecture_path}",
        }

    return invalidate_conjecture(
        conjecture_path=conjecture_path,
        max_iterations=max_iterations,
        mutation_strategy=mutation_strategy,
    )


if __name__ == "__main__":
    mcp.run()