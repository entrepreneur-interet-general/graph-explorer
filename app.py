# -*- coding: utf-8 -*-

import json
from flask import Flask, request, send_from_directory, jsonify
import networkx as nx

from utils import expand, collapse

app = Flask(__name__, static_folder="dist")

# Dummy graph
G = nx.read_gpickle('./data/graph.p')
for n in G:
    G.node[n]["degree"] = G.degree(n)
    G.node[n]["in_degree"] = G.in_degree(n, "valeur_euro")
    G.node[n]["out_degree"] = G.out_degree(n, "valeur_euro")

# Dummy countries 
countries = [
    {"code": "GE", "name": "Allemagne"},
    {"code": "IT", "name": "Italie"}
]

# Dummy departments
departments = [
    {"code": "07", "name": "Ardèche"},
    {"code": "42", "name": "Loire"}
]
    
@app.route("/")
def home():
    return app.send_static_file('index.html')


@app.route('/dist/<path:path>')
def send_static(path):
    return send_from_directory('dist', path)


@app.route('/countries')
def get_countries():
    """  Returns a list of countries
    """
    return jsonify(countries)


@app.route('/departments')
def get_departments():
    """  Returns a list of departments
    """
    return jsonify(departments)

@app.route('/subgraph', methods=["POST"])
def get_subgraph():
    """ Returns the subgraph for a given set of nodes 
        :param nodes: a list of nodes 
        :param expand: a node around which to expand the graph 
        :param collapse: a node around which to collapse the graph  
    """
    payload = request.get_json()
    nodes = payload.get("nodes", [])
    expand_node = payload.get("expand_node")
    collapse_node = payload.get("collapse_node")
    H = G.subgraph(nodes)
    if expand_node:
        H = expand(G, H, expand_node)
    if collapse_node:
        H = nx.Graph(H) # create a copy
        H = collapse(H, collapse_node)
    data = nx.node_link_data(H)
    return json.dumps({"status": "ok", "data": data})

@app.route('/search')
def search():
    """ Search for a specific name containing pattern "pattern" in graph "dataset" 
        and returns top 5 suggestions 
        :param search_term: The pattern we are searching 
        :param filters: A list of filters 
    """
    search_term = request.args["search_term"]
    data = []
    if search_term:
        search_term = search_term.lower()
        nodes = [G.node[n] for n in G]
        # TODO apply filter
        # match if contains substring 
        data = [node for node in nodes if search_term in node['prenom_nom'].lower()][:10]
    return json.dumps(data)
