# -*- coding: utf-8 -*-
import json
import os
from collections import OrderedDict

from flask import Flask, request, send_from_directory, jsonify, send_file
from elasticsearch import Elasticsearch
from gremlin_python.driver import client


def create_app(conf):
    """ Application factory """
    app = Flask(__name__, static_folder="local")
    app.config.from_object(conf)
    return app

config = os.environ.get('CONFIG', 'config.Production')
application = create_app(config)


class JanusClient():
    """
    Context manager to get a JanusGraph client
    and ensure it is closed after usage
    """
    def __enter__(self):
        janus_host = application.config['JANUS_HOST']
        janus_server_url = 'ws://%s:8182/gremlin' % janus_host
        self.client = client.Client(janus_server_url, 'g')
        return self.client

    def __exit__(self, *args):
        self.client.close()


class ElasticsearchClient():
    """ Context manager to get an Elasticsearch client """
    def __enter__(self):
        es_host = application.config['ELASTICSEARCH_HOST']
        es = Elasticsearch(
            es_host,
            timeout=120,
            max_retries=10,
            retry_on_timeout=True)
        return es

    def __exit__(self, *args):
        pass


def format_properties(vp):
    """
    Format properties from the output of a valueMap() step
    http://tinkerpop.apache.org/docs/3.3.4/reference/#valuemap-step
    {"entity": [12568]} => {"entity": 12568}
    """
    for k in vp.keys():
        p = vp[k]
        if len(p) >= 1:
            vp[k] = p[0]
    vp['prenom_nom'] = vp['prenomnom']
    del vp['prenomnom']
    return vp


def es_fuzzy_string_query(tokens):
    """
    Returns a string query used to query nodes fuzzily
    based on a list of tokens
    See: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#_fuzziness
    """
    return " ".join(["%s~" % t for t in tokens])
    return 'v.prenomnom:%s' % values


@application.route("/")
def home():
    return send_file('index.html')


@application.route("/test")
def test():
    return 'test'


@application.route('/search')
def search():
    """ Returns the top 10 nodes fuzzyily matching the `text`
        on attribute `prenomnom`.
        We make use of JanusGraph direct index queries
        https://docs.janusgraph.org/latest/direct-index-query.html
        :param search_term: The pattern we are searching
        :returns: the search suggestions
    """
    text = request.args.get("text")
    matches = []
    if text:
        with JanusClient() as janus_client:
            tokens = text.strip().split()
            str_query = es_fuzzy_string_query(tokens)
            query = "graph.indexQuery('vertexByPrenomNom', 'v.prenomnom:%s')\
                .limit(10).vertices()" % str_query
            vertices = janus_client.submit(query).all().result()
            elements = [v["element"].id for v in vertices]
            if elements:
                query = "g.V(%s).property('degree', __.both().dedup().count())\
                    .valueMap()" % elements
                properties = janus_client.submit(query).all().result()
                matches = [format_properties(p) for p in properties]

    return jsonify(matches)


@application.route('/neighbors')
def get_neighbors():
    """ Returns the subgraph containing `node` and its neighbors
        :param node: the node in the center of neighbors
        :returns: the subgraph of node and its neighbors
    """
    entity = request.args.get("node")
    with JanusClient() as janus_client:
        # Get all neighbors nodes
        query = "g.V().has('entity', '%s')\
            .bothE()\
            .bothV()\
            .dedup()\
            .property('degree', __.both().dedup().count())\
            .property('in_degree_weighted', \
                __.inE().values('valeur_euro').sum())\
            .property('out_degree_weighted', \
                __.outE().values('valeur_euro').sum())\
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


@application.route('/transactions', methods=["POST"])
def get_transactions():
    """ Returns all the transactions that occurs between entities """
    with ElasticsearchClient() as es:
        entities = request.get_json()['data']['entities']
        query = {
            'size': 200,
            'query': {
                'bool': {
                    'must': [
                        {'terms': {'ben_entity_id': entities}},
                        {'terms': {'don_entity_id': entities}}
                    ]
                }
            }
        }
        results = es.search(index='transactions', body=query)
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
            row = OrderedDict()
            for column in columns:
                row[column] = transaction[column]
            rows.append(row)

        return json.dumps(rows)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
