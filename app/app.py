# -*- coding: utf-8 -*-
import json

from flask import Flask, request, send_from_directory, jsonify, send_file
from elasticsearch import Elasticsearch
from gremlin_python import statics 
from gremlin_python.structure.graph import Graph 
from gremlin_python.process.graph_traversal import __ 
from gremlin_python.process.strategies import * 
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection 
from gremlin_python.driver import client 

import time 

application = Flask(__name__, static_folder="local")

# Set special config based on environment 
if application.config['ENV'] == 'development':
    application.config.from_object('config.DevelopmentConfig')
else:
    application.config.from_object('config.ProductionConfig')

es_host = application.config['ELASTICSEARCH_HOST']
es = Elasticsearch(es_host, timeout=120, max_retries=10, retry_on_timeout=True)
index = 'transactions'

janus_host = application.config['JANUS_HOST']
janus_server_url = 'ws://%s:8182/gremlin' % janus_host
statics.load_statics(globals())
graph = Graph()
connection = DriverRemoteConnection(janus_server_url, 'g')
g = graph.traversal().withRemote(connection)

# # Create a low level client for Janus graph specific queries 
janus_client = client.Client(janus_server_url, 'g')


@application.route("/")
def home():
    return send_file('index.html')


@application.route('/dist/<path:path>')
def send_static(path):
    return send_from_directory('dist', path)


@application.route('/transactions', methods=["POST"])
def get_transactions():
    """ Returns all the transactions of a given entity """
    entities = request.get_json()['data']['entities']
    query = {
        'size': 200,
        'query': {
            'bool': {
                'must': [
                    { 'terms': { 'ben_entity_id': entities } },
                    { 'terms': { 'don_entity_id': entities } }
                ]
            }
        }
    }
    results = es.search(index=index, body=query)
    transactions = [hit['_source'] for hit in results['hits']['hits']]
    columns = [
        'date_operation',
        'valeur_euro',
        'don_id',
        'don_entity_id',
        'don_prenom',
        'don_nom',
        'don_date_naissance',
        'don_telephone',
        'don_numero_piece_identite',
        'don_pays',
        'don_pays_code',
        'don_code_postal',
        'ben_id',
        'ben_entity_id',
        'ben_prenom',
        'ben_nom',
        'ben_date_naissance',
        'ben_telephone',
        'ben_numero_piece_identite',
        'ben_pays',
        'ben_pays_code',
        'ben_code_postal',
    ]

    rows = []
    for transaction in transactions:
        row = { k: v for (k, v) in transaction.items() if k in columns }
        rows.append(row)

    return jsonify(rows)

def format_properties(vp):
    for k in vp.keys():
        p = vp[k]
        if len(p) >= 1:
            vp[k] = p[0]
    vp['prenom_nom'] = vp['prenomnom']
    del vp['prenomnom']
    return vp

@application.route('/neighbors')
def get_neighbors():
    """ Returns the subgraph containing `node` and its neighbors 
        :param node: the node in the center of neighbors
        :returns: the subgraph of node and its neighbors
    """
    entity = request.args.get("node")
    if entity:
        # Get all neighbors nodes
        query = "g.V().has('entity', '%s')\
            .bothE()\
            .bothV()\
            .dedup()\
            .property('degree', __.both().dedup().count())\
            .property('in_degree_weighted', __.inE().values('valeur_euro').sum())\
            .property('out_degree_weighted', __.outE().values('valeur_euro').sum())\
            .valueMap()" % entity
        nodes = janus_client.submit(query).next()
        nodes = [format_properties(n) for n in nodes]
        # Get all links between the nodes and its neighbors 
        query = "g.V().has('entity', %s)\
            .bothE()\
            .as('source', 'target', 'date_operation', 'valeur_euro')\
            .select('source', 'target', 'date_operation', 'valeur_euro')\
            .by(__.outV().values('entity'))\
            .by(__.inV().values('entity'))\
            .by('date_operation')\
            .by('valeur_euro')" % entity
        links = janus_client.submit(query).next()
        subgraph = {
            "nodes": nodes,
            "links": links
        }
    return jsonify(subgraph)


@application.route('/search')
def search():
    """ Search for a specific name containing pattern "pattern" in graph "dataset" 
        and returns top 10 suggestions 
        :param search_term: The pattern we are searching 
        :param filters: A list of filters 
    """
    search_term = request.args.get("search_term")
    matches = []
    if search_term:
        query = "g.V().has('prenomnom', textContainsFuzzy('%s'))\
            .property('degree', __.both().dedup().count())\
            .order().by('degree', decr)\
            .limit(10).valueMap()" % search_term
        vertices = janus_client.submit(query).all().result() 
        # vertices properties are array like {"entity": [12568]},
        # format them to {"entity": 12568}
        matches = [format_properties(vp) for vp in vertices]

    return jsonify(matches)


if __name__ == "__main__":
    application.run(host='0.0.0.0')