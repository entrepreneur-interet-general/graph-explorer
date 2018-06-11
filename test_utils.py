# -*- coding: utf-8 -*-

from unittest import TestCase
import networkx as nx 

from utils import expand, collapse

class UtilsTestCase(TestCase):
    
    def test_expand(self):
        """ it should expand a subgraph around a node """
        G = nx.Graph()
        edges = [
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (5, 6),
            (5, 7),
            (5, 8),
            (6, 9)
        ]
        G.add_edges_from(edges)
        H_1 = G.subgraph([1])
        H_2 = expand(G, H_1, 1)
        self.assertListEqual(list(H_2.nodes()), [1, 2, 3, 4, 5])
        H_3 = expand(G, H_2, 5)
        self.assertListEqual(list(H_3.nodes()), [1, 2, 3, 4, 5, 6, 7, 8])


    def test_collapse(self):
        G = nx.Graph()
        edges = [
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (5, 6),
            (5, 7),
            (5, 8),
            (6, 9)
        ]
        G.add_edges_from(edges)
        G_2 = collapse(G, 5)
        self.assertListEqual(list(G_2.nodes()), [1, 2, 3, 4, 5, 6, 9])

        

