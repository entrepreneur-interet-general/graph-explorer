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
time.sleep(120)

app = Flask(__name__, static_folder="local")

es_host = 'elasticsearch'
es = Elasticsearch(es_host, timeout=120, max_retries=10, retry_on_timeout=True)
index = 'transactions'

janus_host = 'janus'
janus_server_url = 'ws://%s:8182/gremlin' % janus_host
statics.load_statics(globals())
graph = Graph()
connection = DriverRemoteConnection(janus_server_url, 'g')
g = graph.traversal().withRemote(connection)

# # Create a low level client for Janus graph specific queries 
janus_client = client.Client(janus_server_url, 'g')


@app.route("/")
def home():
    return send_file('index.html')


@app.route('/dist/<path:path>')
def send_static(path):
    return send_from_directory('dist', path)


@app.route('/transactions')
def get_transactions():
    """ Returns all the transactions of a given entity """
    entity = request.args.get("node")
    query = {
        'size': 200,
        'query': {
            'bool': {
                'should': [
                    { 'term': { 'ben_entity_id': entity } },
                    { 'term': { 'don_entity_id': entity } }
                ]
            }
        }
    }
    results = es.search(index=index, body=query)
    transactions = [hit['_source'] for hit in results['hits']['hits']]
    columns = [
        'date_operation',
        'valeur_euro',
        'don_entity_id',
        'don_prenom',
        'don_nom',
        'don_date_naissance',
        'don_telephone',
        'don_numero_piece_identite',
        'don_pays',
        'don_pays_code',
        'don_code_postal',
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
        row = [transaction.get(column) for column in columns]
        rows.append(row)

    response = {'columns': columns, 'rows': rows}
    return jsonify(response)

def format_properties(vp):
    for k in vp.keys():
        p = vp[k]
        if len(p) >= 1:
            vp[k] = p[0]
    vp['prenom_nom'] = vp['prenomnom']
    del vp['prenomnom']
    return vp

@app.route('/neighbors')
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


@app.route('/search')
def search():
    """ Search for a specific name containing pattern "pattern" in graph "dataset" 
        and returns top 10 suggestions 
        :param search_term: The pattern we are searching 
        :param filters: A list of filters 
    """
    search_term = request.args.get("search_term")
    matches = []
    if search_term:
        query = "g.V().has('prenomnom', textContainsFuzzy('%s')).limit(10).valueMap()" % search_term
        vertices = janus_client.submit(query).all().result() 
        # vertices properties are array like {"entity": [12568]},
        # format them to {"entity": 12568}
        matches = [format_properties(vp) for vp in vertices]

    return jsonify(matches)
