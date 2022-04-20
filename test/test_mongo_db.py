import unittest
from bson.objectid import ObjectId
import sys
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import api.v4.db_connector as database


class TestMongo(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMongo, self).__init__(*args, **kwargs)
        self.db = database.Database

 
    # loads sample html file to string
    def load_html(self):
        with open('sample_html.txt', 'r', encoding='utf8') as file:
            html = file.read()        
        return html


    # removes '\n' and '\r' from html
    def prepare_html(self, html):
        html = html.replace('\r', '')
        html = html.replace('\n', '')
        

    # test if database returns articles correcty
    def test_find_article(self):
        html = self.load_html()
        document = {
            'title': 'British man extradited to US on movie piracy charges | TheHill - The Hill',
            'published': 'Wed, 01 Sep 2021 07:00:00 GMT',
            'link': 'https://thehill.com/regulation/court-battles/570410-british-man-extradited-to-us-on-movie-piracy-charges',
            'region': 'gb',
            'language': 'en',
            'html': html
        }

        self.db.initialize()
        article_id = '619106033a5566fa48e9ac23'
        article = self.db.find_one('articles', {'_id': ObjectId(article_id)})

        article['html'] = self.prepare_html(article['html'])
        document['html'] = self.prepare_html(document['html'])

        self.assertEqual(document['title'], article['title'])
        self.assertEqual(document['published'], article['published'])
        self.assertEqual(document['link'], article['link'])
        self.assertEqual(document['region'], article['region'])
        self.assertEqual(document['language'], article['language'])
        self.assertEqual(document['html'], article['html'])


    # test if database returns keywords correcty
    def test_find_keywords(self):
        case_one = {
            'link': 'https://thehill.com/regulation/court-battles/570410-british-man-extradited-to-us-on-movie-piracy-charges',
            'keywords': ['Pirating']
        }
        case_two = {
            'link': 'https://www.newsweek.com/us-unable-reach-third-migrant-kids-released-amid-fears-they-were-forced-labor-1625225',
            'keywords': ['Forced Labor', 'Child Exploitation']
        }

        self.db.initialize()
        keywords_one = self.db.find_one('crimemaps', {'link': case_one['link']}, {'keywords': 1, '_id': 0})
        keywords_two = self.db.find_one('crimemaps', {'link': case_two['link']}, {'keywords': 1, '_id': 0})

        self.assertEqual(case_one['keywords'], keywords_one['keywords'])
        self.assertEqual(case_two['keywords'], keywords_two['keywords'])



# # runs all tests
# if __name__ == '__main__':
#     unittest.main()
