import unittest
import requests

class TestV2SearchRoutes(unittest.TestCase):
    API_URL = "https://team08-21.studenti.fiit.stuba.sk/api/v2"
    SEARCH_URL = "{}/search/?q=murder".format(API_URL)
    SEARCH_URL_NO_QUERY = "{}/search/".format(API_URL)

    # test if api works correctly
    def test_connection(self):
        r = requests.get(self.SEARCH_URL)

        query = r.json()["query"]
        results = r.json()["results"]

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 6)
        self.assertEqual(query, "murder")
        self.assertTrue(results)
    
    # test if there is 400 status code, when no query is given
    def test_no_query(self):
        r = requests.get(self.SEARCH_URL_NO_QUERY)

        self.assertEqual(r.status_code, 400)




