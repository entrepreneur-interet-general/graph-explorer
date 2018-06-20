import networkx as nx
from faker import Faker 
import random 

fake = Faker()
G = nx.read_gpickle('./data/graph.p')

codes = {
    "FRANCE": "FR",
    "SERBIE": "RS",
}

def numero_piece_identite():
    chrs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    chrs_list = list(chrs)
    random.shuffle(chrs_list)
    return ''.join(chrs_list[:10])

def create_node(entity, country, country_code):
    node = {
        "entity": entity,
        "pays": country,
        "pays_code": country_code,
        "code_postal": "69120",
        "prenom": fake.first_name(),
        "nom": fake.last_name(),
        "date_naissance": fake.date(pattern="%Y-%m-%d", end_datetime="-15y"),
        "telephone": fake.phone_number(),
        "numero_piece_identite": numero_piece_identite()
    }
    node["prenom_nom"] = "%s %s" % (node["prenom"], node["nom"])
    return node 

if __name__ == '__main__':
    entities_fr = range(36000, 36003)
    entities_rs = range(36004, 36007)

    for entity in entities_fr:            
        attrs = create_node(entity, "FRANCE", codes["FRANCE"])
        print(attrs["prenom_nom"])
        G.add_node(entity, **attrs)

    for entity in entities_rs:
        attrs = create_node(entity, "SERBIE", codes["SERBIE"])
        if entity == 36006:
            attrs["star"] = True
        G.add_node(entity, **attrs)
    # create links between nodes 
    links = [
        {"source": 36000, "target": 36004},
        {"source": 36000, "target": 36005},
        {"source": 36001, "target": 36004},
        {"source": 36001, "target": 36005},
        {"source": 36001, "target": 36006},
        {"source": 36002, "target": 36005},
        {"source": 36002, "target": 36006},
    ]

    for link in links:
        transactions = []
        total = 0
        for i in range(1, random.randint(2, 15)):
            ve = random.randint(1000, 3000)
            transactions.append({"valeur_euro": ve})
            total += ve
        G.add_edge(link["source"], link["target"], valeur_euro=total, transactions=transactions)



    nx.write_gpickle(G, './data/graph.p')
    
