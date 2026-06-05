import json
import random
import sys
from pathlib import Path

import networkx as nx

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.verifier.verify import verify_counterexample


def violation_score(result):
    """
    Score used by the local search.

    For conjectures of the form left <= right:
        violation means left > right, so score = left - right.

    For conjectures of the form left >= right:
        violation means left < right, so score = right - left.

    A positive score means that the conjecture is violated.
    """
    left = result["left_value"]
    right = result["right_value"]

    conjecture_relation = result.get("relation")

    if conjecture_relation == ">=":
        return right - left

    return left - right


def edge_mutation(G):
    """
    Simple mutation:
    add or remove one edge.
    """
    H = G.copy()
    nodes = list(H.nodes())

    if len(nodes) < 2:
        return H

    u, v = random.sample(nodes, 2)

    if H.has_edge(u, v):
        H.remove_edge(u, v)
    else:
        H.add_edge(u, v)

    return H


def add_vertex_mutation(G):
    """
    Add one new vertex and connect it to existing vertices.
    """
    H = G.copy()

    if H.number_of_nodes() == 0:
        H.add_node(0)
        return H

    new_node = max(H.nodes()) + 1
    H.add_node(new_node)

    existing_nodes = [node for node in H.nodes() if node != new_node]
    k = min(3, len(existing_nodes))

    neighbors = random.sample(existing_nodes, k)

    for v in neighbors:
        H.add_edge(new_node, v)

    return H


def remove_vertex_mutation(G):
    """
    Remove one vertex, if the graph remains large enough.
    """
    H = G.copy()

    if H.number_of_nodes() <= 3:
        return H

    node = random.choice(list(H.nodes()))
    H.remove_node(node)

    return H


def add_clique_mutation(G):
    """
    Select a small set of vertices and add all missing edges between them.
    """
    H = G.copy()
    nodes = list(H.nodes())

    if len(nodes) < 3:
        return H

    clique_size = random.randint(3, min(5, len(nodes)))
    selected_nodes = random.sample(nodes, clique_size)

    for i in range(len(selected_nodes)):
        for j in range(i + 1, len(selected_nodes)):
            H.add_edge(selected_nodes[i], selected_nodes[j])

    return H


def add_path_mutation(G):
    """
    Select a set of vertices and connect them as a path.
    """
    H = G.copy()
    nodes = list(H.nodes())

    if len(nodes) < 3:
        return H

    path_size = random.randint(3, min(6, len(nodes)))
    selected_nodes = random.sample(nodes, path_size)

    for i in range(len(selected_nodes) - 1):
        H.add_edge(selected_nodes[i], selected_nodes[i + 1])

    return H


def add_star_mutation(G):
    """
    Select one center vertex and add several new leaves connected to it.
    """
    H = G.copy()

    if H.number_of_nodes() == 0:
        H.add_node(0)
        return H

    center = random.choice(list(H.nodes()))
    number_of_leaves = random.randint(2, 5)

    for _ in range(number_of_leaves):
        new_node = max(H.nodes()) + 1
        H.add_node(new_node)
        H.add_edge(center, new_node)

    return H


def mutate_graph(G, mutation_strategy="mixed"):
    """
    Apply one mutation.

    mutation_strategy:
    - edge_only: only add/remove one edge
    - structured: only structured mutations
    - mixed: edge + structured mutations
    """
    if mutation_strategy == "edge_only":
        mutations = [edge_mutation]

    elif mutation_strategy == "structured":
        mutations = [
            add_vertex_mutation,
            remove_vertex_mutation,
            add_clique_mutation,
            add_path_mutation,
            add_star_mutation,
        ]

    else:
        mutations = [
            edge_mutation,
            add_vertex_mutation,
            remove_vertex_mutation,
            add_clique_mutation,
            add_path_mutation,
            add_star_mutation,
        ]

    mutation = random.choice(mutations)
    return mutation(G)


def initial_connected_graph(n=10, p=0.4):
    """
    Generate a connected random graph.
    """
    while True:
        G = nx.gnp_random_graph(n, p)
        if nx.is_connected(G):
            return G


def invalidate_conjecture(
    conjecture_path: str,
    max_iterations: int = 20000,
    mutation_strategy: str = "mixed",
):
    with open(conjecture_path) as f:
        conjecture = json.load(f)

    G = initial_connected_graph(n=5, p=0.8)

    best_result = verify_counterexample(conjecture, G)
    best_result["relation"] = conjecture["relation"]
    best_score = violation_score(best_result)

    for i in range(max_iterations):
        candidate = mutate_graph(G, mutation_strategy=mutation_strategy)

        if not nx.is_connected(candidate):
            continue

        result = verify_counterexample(conjecture, candidate)
        result["relation"] = conjecture["relation"]
        score = violation_score(result)

        if score > best_score:
            G = candidate
            best_score = score
            best_result = result

        if result["violated"]:
            g6 = nx.to_graph6_bytes(
                candidate,
                header=False,
            ).decode().strip()

            return {
                "status": "counterexample_found",
                "iteration": i,
                "conjecture_id": result["conjecture_id"],
                "graph6": g6,
                "mutation_strategy": mutation_strategy,
                "result": result,
            }

    return {
        "status": "no_counterexample_found",
        "conjecture_id": conjecture["id"],
        "mutation_strategy": mutation_strategy,
        "best_score": best_score,
        "best_result": best_result,
    }


if __name__ == "__main__":
    result = invalidate_conjecture(
        "data/false_conjectures/HDR-001.json",
        mutation_strategy="mixed",
    )

    print(result)