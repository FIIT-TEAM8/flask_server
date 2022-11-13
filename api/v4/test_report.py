import unittest
from unittest import mock
from flask import Flask
import json

app = Flask(__name__)

from api.v4.search_routes import api_v4
app.register_blueprint(api_v4, name="api_v4")

class TestArchiveRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_no_ids(self):
        response = self.app.get('api/v4/report')
        assert response.data.decode("utf-8")  == "Invalid input, please provide 'ids' parameter"

if __name__ == "__main__":
    unittest.main()