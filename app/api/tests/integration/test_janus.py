from unittest import TestCase
from ...janus import JanusClient, es_fuzzy_string_query


class JanusTestCase(TestCase):

    def setUp(self):
        self.janus_host = "127.0.0.1"

    def test_es_fuzzy_string_query(self):
        """ it should returns a fuzzy string query """
        tokens = ["quikc", "brwn", "foks"]
        str_query = es_fuzzy_string_query(tokens)
        self.assertEqual(str_query, "quikc~ brwn~ foks~")

    def test_get_neighbors(self):
        with JanusClient(self.janus_host) as janus:
            neighbors = janus.get_neighbors('19336')
            self.assertEqual(len(neighbors), 7)
            node = neighbors[0]
            expected_attributes = [
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
                'out_degree_weighted'
            ]
            for attr in expected_attributes:
                self.assertIn(attr, node.keys())

    def test_get_links(self):
        with JanusClient(self.janus_host) as janus:
            links = janus.get_links('19336')
            self.assertEqual(len(links), 8)
            link = links[0]
            expected_attributes = [
                'source',
                'target',
                'date_operation',
                'valeur_euro'
            ]
            for attr in expected_attributes:
                self.assertIn(attr, link.keys())

    def test_search(self):
        with JanusClient(self.janus_host) as janus:
            search_results = janus.search('John')
            self.assertEqual(len(search_results), 10)
            search_result = search_results[0]
            self.assertIn('entity', search_result)
            self.assertIn('prenom_nom', search_result)
            self.assertIn('prenom', search_result)
            self.assertIn('nom', search_result)
            self.assertIn('code_postal', search_result)
            self.assertIn('pays_code', search_result)
            self.assertIn('numero_piece_identite', search_result)
            self.assertIn('degree', search_result)