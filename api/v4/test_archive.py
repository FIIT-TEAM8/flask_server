import unittest
from unittest import mock
from flask import Flask
import json

app = Flask(__name__)

databaseResponse = {
      "_id": "6239b1eddf4b7decb33fbaf2",
      "html": "scraped html",
      "keywords":["Assassination"],
      "language":"en",
      "link": "https://test.com/",
      "published": "2020-01-01",
      "region":"gb",
      "title": "Sample article number 0"
    }

serverResponse =  {
  "article": 
    {
      "_id": "6239b1eddf4b7decb33fbaf2",
      "html": "scraped html",
      "keywords":["Assassination"],
      "language":"en",
      "link": "https://test.com/",
      "published": "2020-01-01",
      "region":"gb",
      "title": "Sample article number 0"
    }
}

from api.v4.search_routes import api_v4
app.register_blueprint(api_v4, name="api_v4")

class TestArchiveRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_no_link(self):
        response = self.app.get('api/v4/archive')
        assert response.data.decode("utf-8")  == "Invalid input, please provide 'link' parameter"

    @mock.patch("api.v4.search_routes.Database.find_one", return_value=databaseResponse)
    def test_archive(self, article):
        response = self.app.get('api/v4/archive?link=https://www.test.com/')
        resp_json = response.data.decode('utf8').replace("'", '"')
        resp_data = json.loads(resp_json)

        print(resp_data)

        assert resp_data == serverResponse


    @mock.patch("api.v4.search_routes.Database.find_one", return_value=None)
    def test_archive_article_doesnt_exist(self, article):
        response = self.app.get('api/v4/archive?link=https://www.test.com/')
        response = response.data.decode("utf-8") 

        assert response == "Article does not exist"

if __name__ == "__main__":
    unittest.main()