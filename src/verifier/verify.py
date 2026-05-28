import json
import networkx as nx


def read_graph6(g6: str):
    return nx.from_graph6_bytes(g6.encode())


def compute_invariants(G):
    degrees = dict(G.degree())

    return {
        "density": nx.density(G),
        "rad": nx.radius(G) if nx.is_connected(G) else None,
        "diam": nx.diameter(G) if nx.is_connected(G) else None,
        "n": G.number_of_nodes(),
        "m": G.number_of_edges(),
        "avg": sum(degrees.values()) / G.number_of_nodes(),
        "delta": min(degrees.values()),
        "Delta": max(degrees.values()),
    }


def verify_counterexample(conjecture, G):
    inv = compute_invariants(G)

    left = inv[conjecture["left_invariant"]]
    right = eval(conjecture["right_expression"], {}, inv)

    violated = left > right if conjecture["relation"] == "<=" else left < right

    return {
        "conjecture_id": conjecture["id"],
        "left_value": left,
        "right_value": right,
        "violated": violated,
        "invariants": inv,
    }


if __name__ == "__main__":
    with open("data/false_conjectures/HDR-002.json") as f:
        conjecture = json.load(f)

    g6 = conjecture["known_counterexample"]["value"]
    G = read_graph6(g6)

    print(verify_counterexample(conjecture, G))