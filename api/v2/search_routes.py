from flask import Blueprint
import api.v2.api_settings as api_settings
from flask import request
from elasticsearch import Elasticsearch

# /v2/search/
search_api = Blueprint("search_routes", __name__, url_prefix="/" + api_settings.API_VERSION + "/search")

# es = Elasticsearch('https://team08-21.studenti.fiit.stuba.sk/es01/')

es = Elasticsearch(hosts=[
    {"host":'es01'}
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

    articles_ids = get_ids(resp)

    response = {
        "query": query,
        "articles_ids": articles_ids
    }

    return response