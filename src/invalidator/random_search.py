import json
import random
import networkx as nx
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.verifier.verify import verify_counterexample


def random_connected_graph():
    n = random.randint(5, 20)
    p = random.uniform(0.1, 0.9)

    G = nx.gnp_random_graph(n, p)

    if nx.is_connected(G):
        return G

    return None


if __name__ == "__main__":
    with open("data/false_conjectures/HDR-001.json") as f:
        conjecture = json.load(f)

    for i in range(5000):
        G = random_connected_graph()

        if G is None:
            continue

        result = verify_counterexample(conjecture, G)

        if result["violated"]:
            print("COUNTEREXAMPLE FOUND")
            print("iteration:", i)
            print(result)
            g6 = nx.to_graph6_bytes(G, header=False).decode().strip()
            print("graph6:", g6)
            break
    else:
        print("No counterexample found")