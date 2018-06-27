# -*- coding: utf-8 -*-

import json
from flask import Flask, request, send_from_directory, jsonify, send_file
import networkx as nx


app = Flask(__name__, static_folder="local")

# Dummy graph
G = nx.read_gpickle('./data/graph.p')
for n in G:
    G.node[n]["degree"] = G.degree(n)
    G.node[n]["in_degree"] = G.in_degree(n, "valeur_euro")
    G.node[n]["out_degree"] = G.out_degree(n, "valeur_euro")

@app.route("/")
def home():
    return send_file('index.html')


@app.route('/dist/<path:path>')
def send_static(path):
    return send_from_directory('dist', path)


@app.route('/neighbors')
def get_neighbors():
    """ Returns the subgraph containing `node` and its neighbors 
        :param node: the node in the center of neighbors
        :returns: the subgraph of node and its neighbors
    """
    node = request.args.get("node")
    node = int(node)
    neighbors = nx.all_neighbors(G, node)
    neighbors = list(neighbors)
    neighbors.append(node)
    H = G.subgraph(neighbors)
    data = nx.node_link_data(H)
    return jsonify(data)


@app.route('/search')
def search():
    """ Search for a specific name containing pattern "pattern" in graph "dataset" 
        and returns top 10 suggestions 
        :param search_term: The pattern we are searching 
        :param filters: A list of filters 
    """
    search_term = request.args.get("search_term")
    data = []
    if search_term:
        search_term = search_term.lower()
        nodes = [G.node[n] for n in G]
        # TODO apply filter
        # match if contains substring 
        data = [node for node in nodes if search_term in node['prenom_nom'].lower()][:10]
    return jsonify(data)
