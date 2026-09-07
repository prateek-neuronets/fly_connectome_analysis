import numpy as np


def find_rcc_indeg(realgraph, randomgraph, threshold):

    # REAL NETWORK
    neuron_indeg = dict(realgraph.in_degree)
    neurons_with_indeg_greater_than_threshold = {k for k,v in neuron_indeg.items() if v > threshold}

    number_direct_edges = sum(1 for (a,b) in set(map(tuple, realgraph.edges())) if a in neurons_with_indeg_greater_than_threshold and b in neurons_with_indeg_greater_than_threshold)
    number_possible_direct_edges = (len(neurons_with_indeg_greater_than_threshold)*(len(neurons_with_indeg_greater_than_threshold)-1)) #n*(n-1)

    # RANDOM NETWORK
    neuron_indeg_RAN = dict(randomgraph.in_degree)
    neurons_with_indeg_greater_than_threshold_random = {k for k,v in neuron_indeg_RAN.items() if v > threshold}

    number_direct_edges_random = sum(1 for (a,b) in set(map(tuple, randomgraph.edges())) if a in neurons_with_indeg_greater_than_threshold_random and b in neurons_with_indeg_greater_than_threshold_random)
    number_possible_direct_edges_random = (len(neurons_with_indeg_greater_than_threshold_random)*(len(neurons_with_indeg_greater_than_threshold_random)-1))

    if len(neurons_with_indeg_greater_than_threshold) == 0 or len(neurons_with_indeg_greater_than_threshold) == 1:
        normalized_rcc = 1
    else:
        rcc = round(number_direct_edges/number_possible_direct_edges, 5)
        random_rcc = round(number_direct_edges_random/number_possible_direct_edges_random, 5)
        if random_rcc == 0:
            normalized_rcc = 1 #to avoid zero division error
        else:
            normalized_rcc = round(rcc/random_rcc, 5)

    return normalized_rcc


def calculate_rcc_indeg(graph, list_of_random_graphs):

    real_in_degrees = sorted(list(set((dict(graph.in_degree).values()))))

    # Initialize an empty numpy array with the appropriate dimensions
    n_graphs = len(list_of_random_graphs)
    n_degrees = len(real_in_degrees)
    rcc_values_entire = np.zeros((n_graphs, n_degrees))

    # Fill in the array with the rcc values
    for i, rg in enumerate(list_of_random_graphs):
        for j, deg in enumerate(real_in_degrees):
            val = find_rcc_indeg(graph, rg, deg)
            rcc_values_entire[i, j] = val

    rcc_values_entire.mean(axis=0) # finding mean of rcc value for a degree across all random graphs (along the column in the matrix)

    avg_normalized_rcc = {}
    for i, rcc in enumerate(rcc_values_entire.mean(axis=0)):
        avg_normalized_rcc[real_in_degrees[i]] = rcc

    return avg_normalized_rcc