import networkx as nx 

G = nx.MultiDiGraph()

# Dummy transactions 
transactions = []
with open("./data/transactions.csv", 'r') as f:
    columns = f.readline().rstrip().split(',')
    rows = [line.rstrip().split(',') for line in f.readlines()]
    for row in rows:
        transaction = dict(zip(columns, row))
        transactions.append(transaction)



def get_or_create(n):
    entity = int(n['entity'])
    if G.has_node(entity):
        return G.node[entity]
    else:
        G.add_node(entity, **n)
        return G.node[entity]
        # node = G.node[entity]
        # for _property in n.keys():
        #     node[_property] = n[_property]
        # return node


don_columns = [c for c in columns if c.startswith('don')]
ben_columns = [c for c in columns if c.startswith('ben')]

for transaction in transactions:
    don = dict([(c.split("don_")[1], transaction[c]) for c in don_columns])
    don['entity'] = int(don['entity'])
    don_node = get_or_create(don)
    ben = dict([(c.split("ben_")[1], transaction[c]) for c in ben_columns])
    ben['entity'] = int(ben['entity'])
    ben_node = get_or_create(ben) 
    link = {
        "date_operation": transaction["date_operation"],
        "valeur_euro": float(transaction["valeur_euro"])
    }
    don_entity = int(don_node['entity'])
    ben_entity = int(ben_node['entity'])
    G.add_edge(don_entity, ben_entity, **link)


for n in G.nodes():
    prenom = G.node[n]['prenom']
    nom = G.node[n]['nom']
    G.node[n]['prenom_nom'] = "%s %s" % (prenom, nom)
    G.node[n]['degree'] = G.degree(n)
    G.node[n]['in_degree_weighted'] = G.in_degree(n, weight="valeur_euro")
    G.node[n]['out_degree_weighted'] = G.out_degree(n, weight="valeur_euro")

nx.write_gpickle(G, './data/graph.p')