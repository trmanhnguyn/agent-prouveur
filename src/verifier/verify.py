import json
import itertools
import networkx as nx


def read_graph6(g6: str):
    return nx.from_graph6_bytes(g6.encode())


def domination_number(G):
    """
    Compute the domination number gamma(G) by brute force.
    This is only suitable for small graphs.
    """
    nodes = list(G.nodes())

    for r in range(1, len(nodes) + 1):
        for subset in itertools.combinations(nodes, r):
            dominated = set(subset)

            for node in subset:
                dominated.update(G.neighbors(node))

            if len(dominated) == len(nodes):
                return r

    return len(nodes)


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
        "kappa": nx.node_connectivity(G) if nx.is_connected(G) else 0,
        "edge_kappa": nx.edge_connectivity(G) if nx.is_connected(G) else 0,
        "gamma": domination_number(G),
    }


def verify_counterexample(conjecture, G):
    inv = compute_invariants(G)

    left_invariant = conjecture["left_invariant"]

    if left_invariant not in inv:
        return {
            "conjecture_id": conjecture["id"],
            "error": f"Unsupported invariant: {left_invariant}",
            "violated": False,
            "invariants": inv,
        }

    left = inv[left_invariant]
    right = eval(conjecture["right_expression"], {}, inv)

    if conjecture["relation"] == "<=":
        violated = left > right
    elif conjecture["relation"] == ">=":
        violated = left < right
    else:
        raise ValueError(f"Unsupported relation: {conjecture['relation']}")

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