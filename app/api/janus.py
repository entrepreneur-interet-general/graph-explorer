from gremlin_python.driver import client
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import (
    DriverRemoteConnection
)


def es_fuzzy_string_query(tokens):
    """
    Returns a string query used to search nodes fuzzily
    based on a list of tokens
    See: https://www.elastic.co/guide/en/elasticsearch/reference/
    current/query-dsl-query-string-query.html#_fuzziness
        :param tokens: a list of tokens f
    """
    return " ".join(["%s~" % t for t in tokens])
    return 'v.prenomnom:%s' % values


class JanusProxy():
    """
    JanusProxy implements some methods to query the graph
    It uses Gremlin Python language variant:
    http://tinkerpop.apache.org/docs/3.3.4/reference/#gremlin-python
    for traversals and Gremlin-Python driver for JanusGraph
    Direct Index Query:
    http://tinkerpop.apache.org/docs/3.3.4/reference/#connecting-via-python
    """

    def __init__(self, janus_host):
        janus_server_url = 'ws://%s:8182/gremlin' % janus_host
        # low level client for JanusGraph specific queries not part of Gremlin
        graph = Graph()
        self.connection = DriverRemoteConnection(janus_server_url, 'g')
        self.g = graph.traversal().withRemote(self.connection)

    def get_neighbors(self, entity):
        """
        Returns all the neighbors of a node
            :param entity: the entity id of a vertex
            :returns: a list of neighbors attributes
        """

        # find the node identified by `entity`
        traversal = self.g.V().has('entity', entity)

        # find the neighbors of this node
        traversal = traversal.bothE().bothV().dedup()

        # calculates extra attributes
        traversal = traversal \
            .property('degree', __.both().dedup().count()) \
            .property('in_degree_weighted',
                      __.inE().values('valeur_euro').sum()) \
            .property('out_degree_weighted',
                      __.outE().values('valeur_euro').sum())

        # select only specific attributes
        traversal = traversal.project(
            'entity',
            'prenom',
            'nom',
            'prenom_nom',
            'date_naissance',
            'pays_code',
            'code_postal',
            'numero_piece_identite',
            'star',
            'degree',
            'in_degree_weighted',
            'out_degree_weighted') \
            .by('entity') \
            .by('prenom') \
            .by('nom') \
            .by('prenomnom') \
            .by('date_naissance') \
            .by('pays_code') \
            .by('code_postal') \
            .by('numero_piece_identite') \
            .by('star') \
            .by('degree') \
            .by('in_degree_weighted') \
            .by('out_degree_weighted')

        neighbors = traversal.toList()
        return neighbors

    def get_links(self, entity):
        """
        Returns the list of edges of the vertex, both
        inbound and outbound
            :param entity: the entity id of a vertex
        """

        # find the node identified by `entity`
        traversal = self.g.V().has('entity', entity)

        # traverse both inbound and outbound edges
        traversal = traversal.bothE()

        # select attributes on edges
        traversal = traversal \
            .as_('source', 'target', 'date_operation', 'valeur_euro') \
            .select('source', 'target', 'date_operation', 'valeur_euro')\
            .by(__.outV().values('entity'))\
            .by(__.inV().values('entity'))\
            .by('date_operation')\
            .by('valeur_euro')

        links = traversal.toList()
        return links

    def search(self, prenom_nom):
        """
        Search all nodes which attribute `prenomnom` matches the query
            :param prenom_nom: the text query
        """
        tokens = prenom_nom.strip().split()
        str_query = es_fuzzy_string_query(tokens)
        # Use JanusGraph direct index query
        # https://docs.janusgraph.org/latest/direct-index-query.html
        query = "graph.indexQuery('vertexByPrenomNom', 'v.prenomnom:%s')\
            .limit(10).vertices()" % str_query
        client = self.connection._client
        vertices_and_score = client.submit(query).all().result()
        vertices = [v["element"] for v in vertices_and_score]
        search_results = []
        if vertices:
            # find all the matching vertices
            traversal = self.g.V(vertices)
            # add the attribute `degree` on each vertex
            traversal = traversal.property('degree', __.both().dedup().count())
            # select attributes
            traversal = traversal \
                .project(
                    'entity',
                    'prenom_nom',
                    'prenom',
                    'nom',
                    'code_postal',
                    'pays_code',
                    'numero_piece_identite',
                    'degree') \
                .by('entity') \
                .by('prenomnom') \
                .by('prenom') \
                .by('nom') \
                .by('code_postal') \
                .by('pays_code') \
                .by('numero_piece_identite') \
                .by('degree')
            search_results.extend(traversal.toList())
        return search_results

    def close(self):
        self.connection.close()


class JanusClient():
    """
    Context manager to get a JanusGraph proxy
    and ensure resources are closed
    """
    def __init__(self, janus_host):
        self.janus_host = janus_host

    def __enter__(self):
        self.proxy = JanusProxy(self.janus_host)
        return self.proxy

    def __exit__(self, *args):
        self.proxy.close()
