import unittest
import requests
from unittest import mock
from flask import Flask
import json

app = Flask(__name__)

foundArticle = {
    "page_num": 1,
    "per_page": 10,
    "query": "test",
    "results": [
        {
            "_id": "864257bh4ec0b85j6er83751",
            "keywords": ["test"],
            "language": "sk",
            "link": ["www.test.com"],
            "preview": "preview",
            "published": ["Sun, 06 Nov 2022 16:34:20 GMT"],
            "region": "sk",
            "title": ["Test"],
        }
    ],
    "search_from": "",
    "search_to": "",
    "total_pages": 1,
    "total_results": 1,
}


article_test = {
    "hits": {
        "total": {
            "value": 1
        },
        "hits": [
            {
                "_source": {
                    "html": "sdfsdf"
                },
                "_id": "864257bh4ec0b85j6er83751"
            }
        ]
    }
}

from api.v4.search_routes import api_v4
app.register_blueprint(api_v4, name="api_v4")

from api.v4.search_routes import search


class TestClassIWantToTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_health(self):
        rv = self.app.get('api/v4/search')
        assert rv.data.decode("utf-8")  == "Invalid input, please provide 'q' parameter"
    

    @mock.patch("api.v4.search_routes.Elastic.check_connection", return_value=200)
    @mock.patch("api.v4.search_routes.Elastic.search", return_value=article_test)
    def test_conn(self, lol, art):
        rv = self.app.get('api/v4/search?q=murder')
        my_json = rv.data.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        print(data["results"][0]["_id"])

        assert data["results"][0]["_id"] == article_test["hits"]["hits"][0]["_id"]

if __name__ == "__main__":
    unittest.main()