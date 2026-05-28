import json
import random
import sys
from pathlib import Path

import networkx as nx

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.verifier.verify import verify_counterexample


def violation_score(result):
    return result["left_value"] - result["right_value"]


def mutate_graph(G):
    H = G.copy()
    nodes = list(H.nodes())

    u, v = random.sample(nodes, 2)

    if H.has_edge(u, v):
        H.remove_edge(u, v)
    else:
        H.add_edge(u, v)

    return H


def initial_connected_graph(n=10, p=0.4):
    while True:
        G = nx.gnp_random_graph(n, p)
        if nx.is_connected(G):
            return G


if __name__ == "__main__":
    with open("data/false_conjectures/HDR-001.json") as f:
        conjecture = json.load(f)

    G = initial_connected_graph(n=10, p=0.8)
    best_result = verify_counterexample(conjecture, G)
    best_score = violation_score(best_result)

    for i in range(20000):
        candidate = mutate_graph(G)

        if not nx.is_connected(candidate):
            continue

        result = verify_counterexample(conjecture, candidate)
        score = violation_score(result)

        if score > best_score:
            G = candidate
            best_score = score
            best_result = result

        if result["violated"]:
            print("COUNTEREXAMPLE FOUND")
            print("iteration:", i)
            print(result)
            g6 = nx.to_graph6_bytes(candidate, header=False).decode().strip()
            print("graph6:", g6)
            break
    else:
        print("No counterexample found")
        print("best score:", best_score)
        print(best_result)