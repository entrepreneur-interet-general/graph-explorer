from unittest import TestCase, mock
import json

from ...app import application

INDEX_HTML_FILE_PATH = 'index.html'
BUILD_JS_FILE_PATH = 'local/build.js'


class GraphExplorerTestCase(TestCase):

    def setUp(self):
        # creates a test client
        application.config.from_object('api.config.Development')
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

    def test_search_empty_prenom_nom(self):
        """ it should return empty search results """
        result = self.app.get('/search?prenom_nom=')
        self.assertEqual(json.loads(result.data), [])

    @mock.patch('api.app.ElasticsearchProxy')
    def test_get_transactions(self, es_proxy):
        """ it should order fields in rows """
        es = mock.Mock()
        es_proxy.return_value = es
        es.get_transactions.return_value = [
            {
                "date_operation": "1983-02-26",
                "valeur_euro": "3000.0",
                "don_id": "3df9bca8bc4294bebce2b9d879a3f681",
                "don_entity_id": "19976",
                "ben_entity_id": "19336",
                "ben_prenom": "Jill",
                "don_nom": "Walker",
                "don_date_naissance": "1988-01-10",
                "don_telephone": "973-483-5114x6508",
                "don_code_postal": "45417",
                "don_prenom": "Amanda",
                "ben_date_naissance": "2006-12-08",
                "don_pays": "France",
                "don_numero_piece_identite": "JMTTF6GT91",
                "ben_id": "2fe5a1b77fdd7de1c4caaee37d325a95",
                "ben_nom": "Sanchez",
                "ben_telephone": "876-399-2828x519",
                "ben_numero_piece_identite": "T38OBM7SJL",
                "ben_pays": "France",
                "ben_pays_code": "FR",
                "don_pays_code": "FR",
                "ben_code_postal": "62747"}
        ]
        data = {
            'data': {
                'entities': ['19336', '19976']
            }
        }
        result = self.app.post('/transactions', json=data)
        transactions = json.loads(result.data)
        expected_columns = [
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
        self.assertEqual(len(transactions), 1)
        self.assertEqual(list(transactions[0].keys()), expected_columns)