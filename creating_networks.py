# Adult

connections_df = pd.read_csv('connections.csv') 
neurons_df = pd.read_csv('neurons.csv') 
classification_df = pd.read_csv('classification.csv')

# finding unique connections and their weights
final_connections_df = connections_df.groupby(['pre_root_id', 'post_root_id'])['syn_count'].sum().reset_index()

ids_sorted = sorted(neurons_df['root_id']) # the ids look sorted but still for confirmation I am sorting 'em

# renumbering the body IDs for better readability 
neurons_renumbered_dict = {}
for index, root_id in enumerate(ids_sorted):
    neurons_renumbered_dict[root_id] = index

neurons_renumbered_reverse_dict = {v:k for k,v in neurons_renumbered_dict.items()}

# storing neuron information
neuron_details = {}
for row in classification_df[['root_id', 'flow', 'super_class', 'class', 'sub_class', 'cell_type', 'hemibrain_type', 'hemilineage', 'side', 'nerve']].values:
    neuron_id = row[0]
    neuron_details[neuron_id] = {'flow':row[1], 'super_class':row[2], 'class':row[3], 'sub_class':row[4], 'cell_type':row[5], 'hemibrain_type':row[6], 'hemilineage':row[7], 'side':row[8], 'nerve':row[9]}

# building the network
final_connections_dict = final_connections_df.to_dict('records')

for row in final_connections_dict:
    row['pre_root_id'] = neurons_renumbered_dict.get(row['pre_root_id'])
    row['post_root_id'] = neurons_renumbered_dict.get(row['post_root_id'])

connections = final_connections_df_renumbered[['pre_root_id', 'post_root_id']].values

fly_graph = nx.DiGraph()
fly_graph.add_edges_from(list(connections))

#############################################################################################

# larva

all_all_connectivity_matrix_df = pd.read_csv("all-all_connectivity_matrix.csv", index_col=0)
all_all_connectivity_matrix = all_all_connectivity_matrix_df.to_numpy()

relabeling_nodes_dictionary = {}
for index, nodeid in enumerate(all_all_connectivity_matrix_df):
    relabeling_nodes_dictionary[index] = nodeid

# binarizing
all_all_connectivity_matrix_nothreshold = np.array(all_all_connectivity_matrix, copy=True)  
for i in range(len(all_all_connectivity_matrix_nothreshold)):
    for j in range(len(all_all_connectivity_matrix_nothreshold[0])):
        if all_all_connectivity_matrix_nothreshold[i][j] != 0:
            all_all_connectivity_matrix_nothreshold[i][j] = 1

G = nx.from_numpy_array(all_all_connectivity_matrix_nothreshold, create_using=nx.DiGraph)
G = nx.relabel_nodes(G, relabeling_nodes_dictionary)

# neuron information

df_neuron_details = pd.read_csv(r"D:\PRATEEK\LarvalConnectome_Data\science.add9330_data_s2.csv")

neuron_details = {}
for row in df_neuron_details[['left_id', 'right_id', 'celltype', 'additional_annotations', 'level_7_cluster']].values:
    if row[0].isdigit() == True:
        neuron_details[row[0]] = {'celltype':row[2], 'additional_annotations':row[3], 'level_7_cluster':row[4]}
    if row[1].isdigit() == True:
        neuron_details[row[1]] = {'celltype':row[2], 'additional_annotations':row[3], 'level_7_cluster':row[4]}