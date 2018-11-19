from unittest import TestCase
from ...elastic import ElasticsearchProxy


class ElasticTestCase(TestCase):

    def setUp(self):
        self.es_host = '127.0.0.1'

    def test_get_transactions(self):
        es = ElasticsearchProxy(self.es_host)
        transactions = es.get_transactions(['19336', '19976'])
        self.assertEqual(len(transactions), 3)
