from flask import Blueprint
from flask.json import jsonify
from math import ceil
import api.v3.api_settings as api_settings
from flask import request
from elasticsearch import Elasticsearch
from bson.objectid import ObjectId
from .db_connector import Database


# number of articles returned by elasticsearch
SIZE = 20

# /v3/search/
search_api = Blueprint("search_routes", __name__, url_prefix="/" + api_settings.API_VERSION + "/search")

es = Elasticsearch(hosts=[
    {"host": api_settings.ELASTIC_SERVER_URL}
])

# get ids from elasticsearch results
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
    page_num = request.args.get(api_settings.API_PAGE_NUM, default=1, type=int)

    if query is None:
        return "Invalid input, please provide 'q' parameter", 400

    if page_num <= 0:
        page_num = 1

    body = {
        "from": page_num * SIZE - SIZE,
        "size": SIZE,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["text"]
            }
        }
    }

    resp = es.search(index="articles_index", doc_type="_doc", body=body)
    total_results = resp['hits']['total']['value']
    total_pages = int(ceil(total_results/SIZE))

    article_ids = get_ids(resp)
    per_page = len(article_ids)

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
        #"result_count": len(article_ids),
        "page_num": page_num,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_results": total_results,
        "results": articles
    }

    return jsonify(response)