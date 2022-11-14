import unittest
from unittest import mock
from flask import Flask
import json

app = Flask(__name__)

elasticResponse = {
    "hits": {
        "total": {
            "value": 1
        },
        "hits": [
            {
                "_source": {
                    "html": "test html"
                },
                "_id": "864257bh4ec0b85j6er83751"
            }
        ]
    }
}

serverResponse = {
    "query": "test",
    "search_from": "",
    "search_to": "",
    "page_num": 1,
    "per_page": 1,
    "total_pages": 1,
    "total_results": 1,
    "results": [
        {
            '_id': '864257bh4ec0b85j6er83751',
            'preview': 'Article preview is currently not supported.'
        }
    ]
}

elasticAdvancedResponse = {
    "hits": {
        "total": {
            "value": 1
        },
        "hits": [
            {
                "_source": {
                    "html": "test html"
                },
                "_id": "864257bh4ec0b85j6er83751"
            }
        ]
    }
}

serverAdvancedResponse = {
    "query": "test",
    "search_from": "2020-01-01",
    "search_to": "2021-01-01",
    "page_num": 2,
    "per_page": 1,
    "total_pages": 1,
    "total_results": 1,
    "results": [
        {
            '_id': '864257bh4ec0b85j6er83751',
            'preview': 'Article preview is currently not supported.'
        }
    ]
}

from api.v4.search_routes import api_v4
app.register_blueprint(api_v4, name="api_v4")

class TestSearchRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_no_query(self):
        response = self.app.get('api/v4/search')
        assert response.data.decode("utf-8")  == "Invalid input, please provide 'q' parameter"
    

    @mock.patch("api.v4.search_routes.Elastic.check_connection", return_value=200)
    @mock.patch("api.v4.search_routes.Elastic.search", return_value=elasticResponse)
    def test_search(self, conn, response):
        response = self.app.get('api/v4/search?q=test')
        resp_json = response.data.decode('utf8').replace("'", '"')
        resp_data = json.loads(resp_json)

        print(resp_data)

        assert resp_data == serverResponse


    @mock.patch("api.v4.search_routes.Elastic.check_connection", return_value=200)
    @mock.patch("api.v4.search_routes.Elastic.search", return_value=elasticAdvancedResponse)
    def test_advanced_search(self, conn, response):
        response = self.app.get('api/v4/search?q=test&regions=[sk, hu, it]&keywords=[Bomb Threat, Murder]&from=2020-01-01&to=2021-01-01&page=2&size=10')
        resp_json = response.data.decode('utf8').replace("'", '"')
        resp_data = json.loads(resp_json)

        print(resp_data)

        assert resp_data == serverAdvancedResponse

if __name__ == "__main__":
    unittest.main()