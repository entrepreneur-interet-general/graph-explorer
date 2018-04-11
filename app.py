import json
from flask import Flask, request, send_from_directory
import networkx as nx


app = Flask(__name__, static_folder="local/static")

# build the graph
graph_path = "./data/graph.p"
G = nx.read_gpickle(graph_path)
G_undirected = G.to_undirected()

# compute degree, in_degree (weighted) and out_degree (weighted)
for n in G:
    G.node[n]["degree"] = G.degree(n)
    G.node[n]["in_degree"] = G.in_degree(n, "valeur_euro")
    G.node[n]["out_degree"] = G.out_degree(n, "valeur_euro")


# compute top beneficiaries en top_donneurs
top_30_beneficiaries = sorted(
    [G.node[n] for n in G], reverse=True, key=lambda x: x["in_degree"])[:30]

top_30_donneurs = sorted(
    [G.node[n] for n in G], reverse=True, key=lambda x: x["out_degree"])[:30]


@app.route("/")
def home():
    return app.send_static_file('index.html')


@app.route('/local/static/<path:path>')
def send_static(path):
    return send_from_directory('local/static', path)


@app.route('/draw_network')
def draw_network():

    node = int(request.args.get("id"))

    shortest_path = nx.shortest_path(G_undirected, target=node)
    connected_component = G.subgraph(shortest_path.keys())

    # Output
    data = nx.node_link_data(connected_component)

    return json.dumps({"status": "ok", "data": data})


@app.route('/top_beneficiaries')
def get_top_beneficiaries():
    return json.dumps(top_30_beneficiaries)


@app.route('/top_donneurs')
def get_top_donneurs():
    return json.dumps(top_30_donneurs)
