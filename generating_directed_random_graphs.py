import networkx as nx

def generate_random_graphs(graph, n_random):
    
    random_graphs = []
    percentage_common_edges = []

    for i in range(n_random):

        ranG = graph.copy()
        nx.directed_edge_swap(
            ranG, nswap=500000, max_tries=800000
        )  # increasing swaps to 12 million and tries to 20 million doesn't give much better result: it's much slower and the percentage of common edges doesn't decrease

        random_graphs.append(ranG)

        common_edges = set(graph.edges()) & set(ranG.edges())
        percentage_common_edges.append(
            (len(common_edges) / len(set(ranG.edges()))) * 100
        )

    return random_graphs, percentage_common_edges