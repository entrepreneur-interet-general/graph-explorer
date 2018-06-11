# -*- coding: utf-8 -*-

import networkx as nx

def expand(G, H, n):
    """
    Given a graph G, a subgraph H of G, and a node 'n' in H,
    returns a new subgraph containing all nodes in H and 
    neighbors of 'n' in G 
    :param G: a networkx graph  
    :param H: a subgraph of G 
    :param n: a node around which to expand the subgraph 
    """
    neighbors = nx.all_neighbors(G, n)
    all_nodes = set(H.nodes()).union(set(neighbors)).union(set([n]))
    return G.subgraph(all_nodes)


def collapse(G, n):
    """
    Given a graph G and a node 'n' in G,
    remove all leaf nodes in G amongst 'n' neigbors 
    """
    neighbors = G.neighbors(n)
    degrees = nx.degree(G, neighbors)
    leafs = [node for (node, degree) in degrees if degree == 1]
    G.remove_nodes_from(leafs)
    return G 