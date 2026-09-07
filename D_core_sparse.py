import pandas as pd
import networkx as nx
import numpy as np
import pickle
import itertools
from multiprocessing import Pool
import time
from scipy.sparse import csr_matrix

start = time.time()

def Trim_sparse(directed_graph, k, l): # k --> in-degree and l --> out-degree
    nodesarray = np.array(directed_graph.nodes())
    sparsematrix = nx.to_scipy_sparse_array(directed_graph) 
    recursion = True

    while recursion==True and sparsematrix.shape[0] != 0:

        in_degrees = sparsematrix.sum(axis=0)
        out_degrees = sparsematrix.sum(axis=1)
        
        # Identify nodes with in-degree less than k, and out-degree less than l
        indices_to_delete_cols = np.where(in_degrees < k)[0]
        indices_to_delete_rows = np.where(out_degrees < l)[0]
        
        indices_to_delete = np.union1d(indices_to_delete_cols, indices_to_delete_rows)
        
        mask  = np.ones(sparsematrix.shape[0], dtype=bool)
        
        mask[indices_to_delete] = False

        sparsematrix = sparsematrix[:, mask][mask]
        nodesarray = nodesarray[mask]

        if len(indices_to_delete) == 0:
            recursion=False
          
    return sparsematrix, nodesarray

k_l_pairs = list(itertools.product(range(50), range(48))) # obtained via trial and error

def decomposition(graph, pairs_of_kandl):
    all_Dcores_nodes = {}
    Dcores_matrix = np.zeros((50, 48))
    for k, l in pairs_of_kandl:
        trimmed = Trim(graph, k, l)
        all_Dcores_nodes['({}, {})'.format(k, l)] = trimmed[1]
        Dcores_matrix[k][l] += trimmed[0].shape[0]
    return all_Dcores_nodes, Dcores_matrix

pool = Pool()
result = pool.apply(decomposition, args=(fly_graph, k_l_pairs))
pool.close()