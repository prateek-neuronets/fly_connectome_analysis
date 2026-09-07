import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


def get_frontier_Dcore_connections(nodes_of_frontier_Dcores_sorted, fly_graph, neuron_details, neurons_renumbered_reverse_dict):
    
    # Takes nodes of frontier D-cores sorted by neuron type and node ID
    connections_of_nodes_of_frontier_Dcores_sorted = {}
    for node in nodes_of_frontier_Dcores_sorted:
        connections_of_nodes_of_frontier_Dcores_sorted[node] = {}
        preds = fly_graph.predecessors(node)
        succs = fly_graph.successors(node)
        
        l = []
        for neighbor in preds:
            d = neuron_details.get(neurons_renumbered_reverse_dict[neighbor], 'NA')
            if d != 'NA' and pd.isna(d['class']) == False: # if neuron type information exist AND the class is not nan (because not all neurons' class is known)
                typ = d['class']
            else:
                typ = 'NA'
                
            l.append(typ)
        preds_types = dict(Counter(l))

        l = []
        for neighbor in succs:
            d = neuron_details.get(neurons_renumbered_reverse_dict[neighbor], 'NA')
            if d != 'NA' and pd.isna(d['class']) == False:
                typ = d['class']
            else:
                typ = 'NA'
            l.append(typ)
        succs_types = dict(Counter(l))

        connections_of_nodes_of_frontier_Dcores_sorted[node]['predecessors'] = preds_types
        connections_of_nodes_of_frontier_Dcores_sorted[node]['successors'] = succs_types
        
    return connections_of_nodes_of_frontier_Dcores_sorted

def plot_frontier_Dcore_predecessors(connections_of_nodes_of_frontier_Dcores_sorted, classes, classes_colors): # similar for successors

    predecessors = {typ:[] for typ in classes}
    for node in connections_of_nodes_of_frontier_Dcores_sorted:
        for typ in classes:
            val = connections_of_nodes_of_frontier_Dcores_sorted[node]['predecessors'].get(typ, 0)
            predecessors[typ].append(val)

    predecessors_matrix = np.array(list(predecessors.values())).transpose()

    predecessors_matrix_normalized_averaged = np.array([list(np.mean((predecessors_matrix[:2] / np.sum(predecessors_matrix[:2], axis = 1)[:, np.newaxis]), axis = 0)),
                 list(np.mean((predecessors_matrix[2:124] / np.sum(predecessors_matrix[2:124], axis = 1)[:, np.newaxis]), axis = 0)),
                 list(np.mean((predecessors_matrix[124:198] / np.sum(predecessors_matrix[124:198], axis = 1)[:, np.newaxis]), axis = 0))])

    width = 0.5 
    fig, ax = plt.subplots(figsize = (10,10), dpi = 1000)
    bottom = np.zeros(3)

    dcore_node_types = ['ALIN', 'ALLN', 'ALPN']
    for idx, count in enumerate(predecessors_matrix_normalized_averaged.transpose()):
        typ = classes[idx]
        bar = ax.bar(dcore_node_types, count, width, label=typ, color=classes_colors[typ], bottom=bottom)
        bottom += count
          
    ax.set_xlabel('Neuron Type', fontsize = 40)
    ax.set_ylabel('Counts', fontsize = 40)

    ax.tick_params(labelsize = 40, length=10, width = 2, pad = 15)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.xticks(fontsize=40)
    plt.yticks(fontsize=40)

    plt.show()

# similarly for the larva