import json
from flask import Flask, request, send_from_directory
import networkx as nx


app = Flask(__name__, static_folder="local/static")

# Dummy datasets 
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
    
@app.route("/")
def home():
    return app.send_static_file('index.html')


@app.route('/local/static/<path:path>')
def send_static(path):
    return send_from_directory('local/static', path)


@app.route('/datasets')
def get_datasets():
    """  Returns a list of all available datasets
    """
    data = [ { "id": k, "name": v["name"]} for (k, v) in datasets.items() ]
    return json.dumps(data)


@app.route('/connected_component')
def network():
    """ Returns the connected component of node "id" in graph "dataset" (undirected)
        :param id: The id of the central node 
        :param dataset: The graph we are interested in
    """

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

@app.route('/search')
def search():
    """ Search for a specific name containing pattern "pattern" in graph "dataset" 
        and returns top 5 suggestions 
        :param pattern: The pattern we are searching 
        :param dataset: The graph we are interested in
    """
    pattern = request.args["pattern"]
    data = []
    if pattern:
        pattern = pattern.lower()
        dataset_id = request.args["dataset"]
        dataset = datasets[dataset_id]
        G = dataset["graph"]
        nodes = [G.node[n] for n in G]
        # match if contains substring 
        data = [node for node in nodes if pattern in node['prenom_nom'].lower()][:5]
    return json.dumps(data)
