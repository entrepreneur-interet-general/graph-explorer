from unittest import TestCase, mock
import json

from app import application, es_fuzzy_string_query

INDEX_HTML_FILE_PATH = 'index.html'
BUILD_JS_FILE_PATH = 'local/build.js'


class GraphExplorerTestCase(TestCase):

    def setUp(self):
        # creates a test client
        application.config.from_object('config.Development')
        self.app = application.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        """ it should return 200 OK status code """
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        result.close()

    def test_home_data(self):
        """ it should return the content of index.html """
        result = self.app.get('/')
        html = result.data
        with open(INDEX_HTML_FILE_PATH, 'rb') as html_file:
            expected_html = html_file.read()
            self.assertEqual(html, expected_html)
        result.close()

    def test_build_js_status_code(self):
        """ it should return the file local/build.js """
        result = self.app.get(BUILD_JS_FILE_PATH)
        self.assertEqual(result.status_code, 200)
        result.close()

    def test_build_js_data(self):
        """ it should return the content of local/build.js """
        result = self.app.get(BUILD_JS_FILE_PATH)
        js = result.data
        with open(BUILD_JS_FILE_PATH, 'rb') as build_js_file:
            expected_js = build_js_file.read()
            self.assertEqual(js, expected_js)
        result.close()

    def test_es_fuzzy_string_query(self):
        """ it should returns a fuzzy string query """
        tokens = ["quikc", "brwn", "foks"]
        str_query = es_fuzzy_string_query(tokens)
        self.assertEqual(str_query, "quikc~ brwn~ foks~")

    def test_search(self):
        """ it should returns the search suggestions """
        result = self.app.get('/search?text=Amanda')
        print(json.loads(result.data))

    @mock.patch('app.ElasticsearchClient')
    def test_get_transactions(self, ElasticsearchClient_mock):
        """ it should return all the transactions between a set of entites """
        es_mock = mock.Mock()
        ElasticsearchClient_mock.return_value.__enter__.return_value = es_mock
        es_response = {
            'hits': {
                'total': 3,
                'max_score': 2.0,
                'hits': [
                    {
                        '_index': 'transactions',
                        '_type': 'doc',
                        '_id': '-XKAgWYBECkQq3Nc5G3V',
                        '_score': 2.0,
                        '_source': {
                            'don_nom': 'Walker',
                            'don_numero_piece_identite': 'JMTTF6GT91',
                            'ben_date_naissance': '2006-12-08',
                            'date_operation': '1983-02-26',
                            'ben_numero_piece_identite': 'T38OBM7SJL',
                            'path': '/workspace/logstash/data/transactions.csv',
                            'ben_pays_code': 'FR',
                            'don_pays_code': 'FR',
                            'ben_pays': 'France',
                            'don_date_naissance': '1988-01-10',
                            '@version': '1',
                            'host': '97af5f0dcc11',
                            'ben_code_postal': '62747',
                            'ben_prenom': 'Jill',
                            'don_telephone': '973-483-5114x6508',
                            'don_id': '3df9bca8bc4294bebce2b9d879a3f681',
                            'ben_entity_id': '19336',
                            'ben_telephone': '876-399-2828x519',
                            'don_prenom': 'Amanda',
                            'don_pays': 'France',
                            'don_entity_id': '19976',
                            'ben_nom': 'Sanchez',
                            'ben_id': '2fe5a1b77fdd7de1c4caaee37d325a95',
                            '@timestamp': '2018-10-17T10:09:59.391Z',
                            'valeur_euro': '3000.0',
                            'don_code_postal': '45417'
                        }
                    }
                ]
            }
        }
        es_mock.search.return_value = es_response

        data = {'data': {'entities': ['19336', '19976']}}
        result = self.app.post(
            '/transactions',
            data=json.dumps(data),
            content_type='application/json')

        transactions = [
            {
                "date_operation": "1983-02-26",
                "valeur_euro": "3000.0",
                "don_id": "3df9bca8bc4294bebce2b9d879a3f681",
                "don_entity_id": "19976",
                "don_prenom": "Amanda",
                "don_nom": "Walker",
                "don_date_naissance": "1988-01-10",
                "don_telephone": "973-483-5114x6508",
                "don_numero_piece_identite": "JMTTF6GT91",
                "don_pays": "France",
                "don_pays_code": "FR",
                "don_code_postal": "45417",
                "ben_id": "2fe5a1b77fdd7de1c4caaee37d325a95",
                "ben_entity_id": "19336",
                "ben_prenom": "Jill",
                "ben_nom": "Sanchez",
                "ben_date_naissance": "2006-12-08",
                "ben_telephone": "876-399-2828x519",
                "ben_numero_piece_identite": "T38OBM7SJL",
                "ben_pays": "France",
                "ben_pays_code": "FR",
                "ben_code_postal": "62747"
            }
        ]
        self.assertEqual(json.loads(result.data), transactions)

    @mock.patch('app.JanusClient')
    def test_get_neighbors(self, JanusClient_mock):
        """ it should return all the neighbors of an entity in the graph """
        result = self.app.get('/neighbors?node=19336')
        janus_mock = mock.Mock()
        JanusClient_mock.return_value.__enter__.return_value = janus_mock
        janus_mock.submit.return_value.next.return_value = [
            {'code_postal': ['62747'], 'star': [True], 'degree': [6], 'out_degree_weighted': [2000.0], 'nom': ['Sanchez'], 'in_degree_weighted': [34000.0], 'numero_piece_identite': ['T38OBM7SJL'], 'prenomnom': ['Jill Sanchez'], 'pays_code': ['FR'], 'prenom': ['Jill'], 'entity': ['19336'], 'date_naissance': ['2006-12-08'], 'pays': ['France']},
            {'code_postal': ['49608'], 'star': [False], 'degree': [2], 'out_degree_weighted': [10500.0], 'nom': ['Compton'], 'in_degree_weighted': [0.0], 'numero_piece_identite': ['A5ER1EO06J'], 'prenomnom': ['Victoria Compton'], 'pays_code': ['DE'], 'prenom': ['Victoria'], 'entity': ['24534'], 'date_naissance': ['1982-11-27'], 'pays': ['Allemagne']}]

        nodes = []

        links = [{'source': '19336', 'target': '19976', 'date_operation': '1983-02-26', 'valeur_euro': 2000.0}, {'source': '29496', 'target': '19336', 'date_operation': '2016-10-05', 'valeur_euro': 5500.0}, {'source': '19335', 'target': '19336', 'date_operation': '1998-09-09', 'valeur_euro': 5000.0}, {'source': '18581', 'target': '19336', 'date_operation': '2017-04-10', 'valeur_euro': 5500.0}, {'source': '22628', 'target': '19336', 'date_operation': '1995-03-28', 'valeur_euro': 5000.0}, {'source': '24534', 'target': '19336', 'date_operation': '1970-10-30', 'valeur_euro': 5000.0}, {'source': '19976', 'target': '19336', 'date_operation': '1983-02-24', 'valeur_euro': 5000.0}, {'source': '19976', 'target': '19336', 'date_operation': '1983-02-26', 'valeur_euro': 3000.0}]

        expected_neighbors = {
            'links': [
                {'date_operation': '2016-10-05', 'source': '29496', 'target': '19336', 'valeur_euro': 5500.0}
            ],
            'nodes': [
                {'code_postal': '62747', 'date_naissance': '2006-12-08', 'degree': 6, 'entity': '19336', 'in_degree_weighted': 34000.0, 'nom': 'Sanchez', 'numero_piece_identite': 'T38OBM7SJL', 'out_degree_weighted': 2000.0, 'pays': 'France', 'pays_code': 'FR', 'prenom': 'Jill', 'prenom_nom': 'Jill Sanchez', 'star': True},
                {'code_postal': '45417', 'date_naissance': '1988-01-10', 'degree': 4, 'entity': '19976', 'in_degree_weighted': 2000.0, 'nom': 'Walker', 'numero_piece_identite': 'JMTTF6GT91', 'out_degree_weighted': 23500.0, 'pays': 'France', 'pays_code': 'FR', 'prenom': 'Amanda', 'prenom_nom': 'Amanda Walker', 'star': False},
                {'code_postal': '84901', 'date_naissance': '2014-06-15', 'degree': 3, 'entity': '29496', 'in_degree_weighted': 0.0, 'nom': 'Pratt', 'numero_piece_identite': '31K2C6SBFY', 'out_degree_weighted': 20500.0, 'pays': 'France', 'pays_code': 'FR', 'prenom': 'Michael', 'prenom_nom': 'Michael Pratt', 'star': False},
                {'code_postal': '1903', 'date_naissance': '2012-10-22', 'degree': 2, 'entity': '19335', 'in_degree_weighted': 0.0, 'nom': 'Schaefer', 'numero_piece_identite': 'RXZYAKHYL2', 'out_degree_weighted': 10000.0, 'pays': 'Italie', 'pays_code': 'IT', 'prenom': 'Austin', 'prenom_nom': 'Austin Schaefer', 'star': False},
                {'code_postal': '84733', 'date_naissance': '2013-03-04', 'degree': 3, 'entity': '18581', 'in_degree_weighted': 0.0, 'nom': 'Gibson', 'numero_piece_identite': 'B1ASSPNQ67', 'out_degree_weighted': 16000.0, 'pays': 'France', 'pays_code': 'FR', 'prenom': 'Jennifer', 'prenom_nom': 'Jennifer Gibson', 'star': False},
                {'code_postal': '50085', 'date_naissance': '2017-06-29', 'degree': 3, 'entity': '22628', 'in_degree_weighted': 0.0, 'nom': 'Horton', 'numero_piece_identite': '8C1GUDO4QM', 'out_degree_weighted': 20500.0, 'pays': 'France', 'pays_code': 'FR', 'prenom': 'Christina', 'prenom_nom': 'Christina Horton', 'star': False},
                {'code_postal': '49608', 'date_naissance': '1982-11-27', 'degree': 2, 'entity': '24534', 'in_degree_weighted': 0.0, 'nom': 'Compton', 'numero_piece_identite': 'A5ER1EO06J', 'out_degree_weighted': 10500.0, 'pays': 'Allemagne', 'pays_code': 'DE', 'prenom': 'Victoria', 'prenom_nom': 'Victoria Compton', 'star': False}
                ]
        }
        #print(json.loads(result.data))


    def test_query(self):
        query = "g.V().has('entity', '19336').project('entity', 'prenomnom').by('entity').by('prenomnom')"
        from app import JanusClient
        with JanusClient() as janus_client:
            response = janus_client.submit(query).all().result()
            print(response)