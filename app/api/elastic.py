
from elasticsearch import Elasticsearch


class ElasticsearchProxy():

    def __init__(self, es_host):
        self.es = Elasticsearch(
            es_host,
            timeout=120,
            max_retries=10,
            retry_on_timeout=True)

    def get_transactions(self, entities):
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
        results = self.es.search(index='transactions', body=query)
        transactions = [hit['_source'] for hit in results['hits']['hits']]
        return transactions
