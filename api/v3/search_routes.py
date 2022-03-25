from ast import keyword
from email.policy import default
from flask import Blueprint
from flask.json import jsonify
from math import ceil
import api.v3.api_settings as api_settings
from flask import request
from elasticsearch import Elasticsearch
from bson.objectid import ObjectId
from .db_connector import Database


# max and deafult numbers of articles returned by elasticsearch
MAX_SIZE = 20
DEFAULT_SIZE = 10

# /v3/search/
search_api = Blueprint("search_routes", __name__, url_prefix="/" + api_settings.API_VERSION + "/search")

es = Elasticsearch(host=api_settings.ES_CONNECTION_STRING, verify_certs=False)

# get ids from elasticsearch results
def get_ids(result):
    ids = []

    for res in result["hits"]["hits"]:
        ids.append(res["_id"])

    return ids


# check if number of articles to be returned is valid 
def check_size_validity(size):
    
    if size >= MAX_SIZE:
        size = MAX_SIZE

    elif size <= 0:
        size = DEFAULT_SIZE

    return size


# transforms keywords string to list
def keywords_to_list(keywords):

    # check if keywords are used
    if not keywords:
        return None
    # transform keywords string into list
    elif keywords[0] == '[' and keywords[len(keywords) - 1] == ']':
        keywords = keywords[1:-1]
        wordlist = keywords.split(',')
        wordlist = [item.lstrip() for item in wordlist]
        return wordlist
    else:
        return None


# builds elasticsearch query with or without filters
def build_query(query, keywords, page_num, size):
    body = {
        # pagination
        "from": page_num * size - size,
        "size": size,
        # match query in article text
        "query": {
            "match": {
                "text": {
                    "query": query,
                    "operator": "and"
                }
            }
        }
    }
    return body


@search_api.route("/", methods=['GET'])
def search():
    query = request.args.get(api_settings.API_SEARCH_QUERY, default=None, type=str)
    search_from = request.args.get(api_settings.API_SEARCH_FROM, default="", type=str)
    search_to = request.args.get(api_settings.API_SEARCH_TO, default="", type=str)
    locale = request.args.get(api_settings.API_SEARCH_LOCALE, default="", type=str)
    page_num = request.args.get(api_settings.API_PAGE_NUM, default=1, type=int)
    size = request.args.get(api_settings.API_PAGE_SIZE, default=DEFAULT_SIZE, type=int)
    keywords = request.args.get(api_settings.API_KEYWORDS, default="", type=str)

    if query is None:
        return "Invalid input, please provide 'q' parameter", 400

    if page_num <= 0:
        page_num = 1

    size = check_size_validity(size)
    keywords_list = keywords_to_list(keywords)

    body = build_query(query, keywords_list, page_num, size)

    # body = {
    #     # pagination
    #     "from": page_num * size - size,
    #     "size": size,
    #     # match query in article text
    #     "filtered": {
    #         "query": {
    #             "match": { "html": query },
    #             "operator": "and"
    #             },
    #         # match results with at least one keyword from the list
    #         "filter": {
    #             "terms": {
    #                 "keywords": keywords_list
    #             }
    #         }
    #     }
    # }

    resp = es.search(index="articles_index", doc_type="_doc", body=body)
    total_results = resp['hits']['total']['value']
    total_pages = int(ceil(total_results/size))
    article_ids = get_ids(resp)
    per_page = len(article_ids)

    Database.initialize()

    articles = []

    for id in article_ids:
        # finds article document in articles collection by id
        article = Database.find_one('articles', {'_id': ObjectId(id)})
        #article = Database.find_one('articles', {'_id': id})
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
        "page_num": page_num,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_results": total_results,
        "results": articles
    }

    return jsonify(response)