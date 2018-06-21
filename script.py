
import networkx as nx 

path = './data/graph.p'
G = nx.read_gpickle(path)

properties = [
    "entity", 
    "prenom", 
    "nom", 
    "date_naissance", 
    "telephone", 
    "numero_piece_identite", 
    "pays", 
    "pays_code", 
    "code_postal"]

if __name__ == "__main__":
    for (s, t) in G.edges():
        transactions = G[s][t]["transactions"]
        don = G.node[s]
        ben = G.node[t]
        for transaction in transactions:
            for typ in ["don", "ben"]:
                for prop in properties:
                    p = "%s_%s" % (typ, prop)
                    transaction[p] = (don[prop] if typ == "don" else ben[prop])
        G[s][t]["transactions"] = transactions
    nx.write_gpickle(G, path)
