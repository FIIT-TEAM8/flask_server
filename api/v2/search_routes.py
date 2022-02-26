from flask import Blueprint
from flask.json import jsonify
import api.v2.api_settings as api_settings
from flask import request
from elasticsearch import Elasticsearch
from bson.objectid import ObjectId
from .db_connector import Database


# /v2/search/
search_api = Blueprint("search_routes", __name__, url_prefix="/" + api_settings.API_VERSION + "/search")

es = Elasticsearch(hosts=[
    {"host": api_settings.ELASTIC_SERVER_URL}
])

def get_ids(result):
    ids = []

    for res in result["hits"]["hits"]:
        ids.append(res["_id"])

    return ids


@search_api.route("/", methods=['GET'])
def search():
    query = request.args.get(api_settings.API_SEARCH_QUERY, default=None, type=str)
    search_from = request.args.get(api_settings.API_SEARCH_FROM, default="", type=str)
    search_to = request.args.get(api_settings.API_SEARCH_TO, default="", type=str)
    locale = request.args.get(api_settings.API_SEARCH_LOCALE, default="", type=str)

    if query is None:
        return "Invalid input, please provide 'q' parameter", 400

    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["text"]
            }
        }
    }

    resp = es.search(index="articles_index", doc_type="_doc", body=body, size=10)

    article_ids = get_ids(resp)
    Database.initialize()

    articles = []

    for id in article_ids:
        # finds article document in articles collection by id
        article = Database.find_one('articles', {'_id': ObjectId(id)})
        article['body'] = article.pop('html')

        # finds crime keywords in crimemaps collection by article's link
        crime_keywords = Database.find_one('crimemaps', {'link': article['link']}, {'keywords': 1, '_id': 0})
        article.update(crime_keywords)
        articles.append(article)

    response = {
        "query": query,
        "search_from": search_from,
        "search_to": search_to,
        "locale": locale,
        "result_count": len(article_ids),
        "results": articles
    }

    return jsonify(response)
