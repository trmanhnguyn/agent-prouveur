import networkx as nx
import matplotlib.pyplot as plt

# Lecture du graphe au format graph6
G = nx.read_graph6("data/counterexamples/HDR-001.g6")

# Position des sommets
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(4,4))

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=1800,
    font_size=14,
    width=2
)

plt.title("Contre-exemple HDR-001")

plt.tight_layout()

plt.savefig("HDR001.png", dpi=300)

print("Image enregistrée : HDR001.png")

plt.show()