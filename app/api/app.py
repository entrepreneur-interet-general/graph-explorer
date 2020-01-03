# -*- coding: utf-8 -*-
import json
import os
from collections import OrderedDict

from flask import Flask, request, send_from_directory, jsonify, \
    send_file, redirect

from .janus import JanusClient
from .elastic import ElasticsearchProxy

# Get the current working directory
cwd = os.getcwd()

# Path to the static folder
static_folder = os.path.join(cwd, 'local')

# Path to index.html
index_html_file = os.path.join(cwd, 'index.html')


def create_app(conf):
    """ Application factory """
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(conf)
    return app

config = os.environ.get('CONFIG', 'api.config.Production')
application = create_app(config)


@application.route("/")
def home():
    return send_file(index_html_file)


@application.route('/search')
def search():
    """ Returns the top 10 nodes fuzzyily matching the `text`
        on attribute `prenomnom`.
        We make use of JanusGraph direct index queries
        https://docs.janusgraph.org/latest/direct-index-query.html
        :param search_term: The pattern we are searching
        :returns: the search suggestions
    """
    prenom_nom = request.args["prenom_nom"]
    search_results = []
    if prenom_nom:
        janus_host = application.config['JANUS_HOST']
        with JanusClient(janus_host) as janus:
            search_results = janus.search(prenom_nom)
    return jsonify(search_results)


@application.route('/neighbors')
def get_neighbors():
    """ Returns the subgraph containing `node` and its neighbors
        :param node: the node in the center of neighbors
        :returns: the subgraph of node and its neighbors
    """
    entity = request.args["node"]
    janus_host = application.config['JANUS_HOST']
    with JanusClient(janus_host) as janus:
        # Get all neighbors nodes
        nodes = janus.get_neighbors(entity)
        # Get all links between the nodes and its neighbors
        links = janus.get_links(entity)
        subgraph = {
            "nodes": nodes,
            "links": links
        }
    return jsonify(subgraph)


def to_ordered_dict(transaction):
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
    row = OrderedDict()
    for column in columns:
        row[column] = transaction[column]
    return row


@application.route('/transactions', methods=["POST"])
def get_transactions():
    """ Returns all the transactions that occurs between a set of entities """
    es_host = application.config['ELASTICSEARCH_HOST']
    es = ElasticsearchProxy(es_host)
    entities = request.get_json()['data']['entities']
    transactions = es.get_transactions(entities)
    transactions = [to_ordered_dict(t) for t in transactions]
    return jsonify(transactions)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
