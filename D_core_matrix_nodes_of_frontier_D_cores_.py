import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def find_frontier_cores(all_Dcores_nodes):

    frontier_cells = []
    for key in all_Dcores_nodes:
        k, l = [int(x) for x in re.findall('\d+', key)]
        parent = set(all_Dcores_nodes[key])
        l_plus1 = f'({k}, {l+1})'
        k_plus1 = f'({k+1}, {l})'

        if len(parent) > 0:
            if (l_plus1 in all_Dcores_nodes.keys() and len(all_Dcores_nodes[l_plus1]) == 0) or (k_plus1 in all_Dcores_nodes.keys() and len(all_Dcores_nodes[k_plus1]) == 0):
                frontier_cells.append(key)

    nodes_of_frontier_Dcores = set()
    for key in frontier_cells:
        nodes_of_frontier_Dcores.update(set(all_Dcores_nodes[key]))

    return frontier_cells, nodes_of_frontier_Dcores

def plot_Dcores_matrix(Dcores_matrix, frontier_cells):

    set_of_frontier_cells = set(frontier_cells)

    # Define the value ranges and corresponding colors
    value_ranges = [(0, 0, 'white'), (0, 10, 'darkblue'), (11, 20, 'blue'),
                    (21, 30, 'lightblue'), (31, 40, 'green'), (41, 50, 'lightgreen'), (51, 60, 'yellow'),
                    (61, 70, 'orange'), (71, 80, 'red'), (81, 90, 'crimson'), (91, np.inf, 'brown')]

    # Create a colormap with custom colors
    colors = [color for _, _, color in value_ranges]
    cmap = ListedColormap(colors)

    # Define the color mapping function
    def map_value_to_color(value):

        if value == 0:
            return 0 #zeroth index

        percentage = int(round((value/124891)*100, 0))
        for low, high, color in value_ranges[1:]:
            if low <= percentage <= high:
                return colors.index(color)

    # Apply the custom color mapping to each cell in the matrix
    mapped_matrix = np.vectorize(map_value_to_color)(Dcores_matrix)

    fig, ax = plt.subplots(figsize=(10,10), dpi=1000)

    # Plot the matrix with the custom colormap
    im = ax.imshow(mapped_matrix, cmap=cmap)

    # Create a colorbar with the value labels
    cbar = plt.colorbar(im, ticks=range(len(colors)), fraction=0.048, pad=0.05)
    cbar.set_ticklabels([f'{low}-{high}' if high != np.inf else f'>{low}' for low, high, _ in value_ranges])
    cbar.ax.tick_params(labelsize=20)

    # add cell boundaries
    for i in range(len(mapped_matrix)):
        for j in range(len(mapped_matrix[0])):
            if mapped_matrix[i][j] != 0:
                plt.plot([j - 0.5, j + 0.5], [i + 0.5, i + 0.5], color='black', linewidth=0.5)
                plt.plot([j + 0.5, j + 0.5], [i - 0.5, i + 0.5], color='black', linewidth=0.5)
                if f'({i}, {j})' in set_of_frontier_cells:
                    plt.plot([j - 0.4, j + 0.4], [i + 0.4, i - 0.4], color='white', linewidth=1.25)

    # Set ticks and tick labels at intervals of 5
    plt.xticks(np.arange(0, mapped_matrix.shape[1], 10))
    plt.yticks(np.arange(0, mapped_matrix.shape[0], 10))

    ax.set_xlabel('l', fontsize=40)
    ax.set_ylabel('k', fontsize=40)
    ax.tick_params(axis='both', which='major', labelsize=40, length=10, width=2)

    plt.show()