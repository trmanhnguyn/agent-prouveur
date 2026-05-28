import networkx as nx


def read_graph6(graph6_string: str):
    return nx.from_graph6_bytes(graph6_string.encode())


def graph_info(G):
    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": nx.density(G),
        "connected": nx.is_connected(G),
        "radius": nx.radius(G) if nx.is_connected(G) else None,
        "diameter": nx.diameter(G) if nx.is_connected(G) else None,
        "average_degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
    }


if __name__ == "__main__":
    g6 = "M~~~~zz|~^z~n~^~_"
    G = read_graph6(g6)
    print(graph_info(G))