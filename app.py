import json
from flask import Flask, request, send_from_directory
import networkx as nx


app = Flask(__name__, static_folder="local/static")

datasets = {
    "dataset_1": {
        "name": "Dataset 1",
        "graph_path": "./data/graph.p" 
    },
    "dataset_2": {
        "name": "Dataset 2",
        "graph_path": "./data/graph.p"
    },
    "dataset_3": {
        "name": "Dataset 3",
        "graph_path": "./data/graph.p"
    }
}

for k, dataset in datasets.items():
    G = nx.read_gpickle(dataset["graph_path"])
    for n in G:
        G.node[n]["degree"] = G.degree(n)
        G.node[n]["in_degree"] = G.in_degree(n, "valeur_euro")
        G.node[n]["out_degree"] = G.out_degree(n, "valeur_euro")

    dataset["graph"] = G 
    
    dataset["top_30_beneficiaries"] = sorted(
        [G.node[n] for n in G], reverse=True, key=lambda x: x["in_degree"])[:30]

    dataset["top_30_donneurs"] = sorted(
        [G.node[n] for n in G], reverse=True, key=lambda x: x["out_degree"])[:30]
        

@app.route("/")
def home():
    return app.send_static_file('index.html')


@app.route('/local/static/<path:path>')
def send_static(path):
    return send_from_directory('local/static', path)

@app.route('/datasets')
def get_datasets():
    data = [ { "id": k, "name": v["name"]} for (k, v) in datasets.items() ]
    return json.dumps(data)

@app.route('/draw_network')
def draw_network():

    node = int(request.args["id"])
    dataset_id = request.args["dataset"]
    dataset = datasets[dataset_id]
    G = dataset["graph"]
    G_undirected = G.to_undirected()

    shortest_path = nx.shortest_path(G_undirected, target=node)
    connected_component = G.subgraph(shortest_path.keys())

    # Output
    data = nx.node_link_data(connected_component)

    return json.dumps({"status": "ok", "data": data})


@app.route('/top_beneficiaries')
def get_top_beneficiaries():
    dataset = request.args.get("dataset")
    top_30_beneficiaries = datasets[dataset]["top_30_beneficiaries"]
    return json.dumps(top_30_beneficiaries)


@app.route('/top_donneurs')
def get_top_donneurs():
    dataset = request.args.get("dataset")
    top_30_donneurs = datasets[dataset]["top_30_donneurs"]
    return json.dumps(top_30_donneurs)
