import unittest
from unittest import mock
from flask import Flask
import json

app = Flask(__name__)

elasticResponse = [
    {
        "found": True,
        "_id": "6239b1eddf4b7decb33fbaf2",
        "_source": {
            "_id": "6239b1eddf4b7decb33fbaf2",
            "html": "scraped html",
            "keywords":["Assassination"],
            "language":"en",
            "link": "https://thispersondoesnotexist.com/",
            "published": "2020-01-01",
            "region":"gb",
            "title": "Sample article number 0"
        }
    },
    {
        "found": True,
        "_id": "206239b1ecdf4b7decb33fbaee",
        "_source": {
            "_id": "206239b1ecdf4b7decb33fbaee",
            "html": "scraped html",
            "keywords":["Assassination", "Murder"],
            "language":"en",
            "link": "https://thispersondoesnotexist.com/",
            "published": "2020-01-01",
            "region":"gb",
            "title": "Sample article number 1"
        }
    }
]

articleNotFoundElasticResponse = [
    {
        "found": False,
        "_id": "",
        "_source": {
        }
    }
]

serverResponse = {
  "results": [
    {
      "_id": "6239b1eddf4b7decb33fbaf2",
      "html": "scraped html",
      "keywords":["Assassination"],
      "language":"en",
      "link": "https://thispersondoesnotexist.com/",
      "published": "2020-01-01",
      "region":"gb",
      "title": "Sample article number 0"
    },
    {
      "_id": "206239b1ecdf4b7decb33fbaee",
      "html": "scraped html",
      "keywords":["Assassination", "Murder"],
      "language":"en",
      "link": "https://thispersondoesnotexist.com/",
      "published": "2020-01-01",
      "region":"gb",
      "title": "Sample article number 1"
    }
  ]
}


from api.v4.search_routes import api_v4
app.register_blueprint(api_v4, name="api_v4")

class TestReportRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()


    def test_no_ids(self):
        response = self.app.get('api/v4/report')
        assert response.data.decode("utf-8")  == "Invalid input, please provide 'ids' parameter"
        

    @mock.patch("api.v4.search_routes.Elastic.search_by_ids", return_value=elasticResponse)
    def test_report(self, response):
        response = self.app.get('api/v4/report?ids=[6239b1eddf4b7decb33fbaf2, 206239b1ecdf4b7decb33fbaee]')
        resp_json = response.data.decode('utf8').replace("'", '"')
        resp_data = json.loads(resp_json)

        print(resp_data)

        assert resp_data == serverResponse


    @mock.patch("api.v4.search_routes.Elastic.search_by_ids", return_value=articleNotFoundElasticResponse)
    def test_report_article_not_found(self, response):
        response = self.app.get('api/v4/report?ids=[6239b1eddf4b7decb33fbaf2]')

        assert response.data.decode("utf-8") == "Article with id {doc['_id']} does not exist"

if __name__ == "__main__":
    unittest.main()