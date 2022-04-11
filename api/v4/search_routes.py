from flask import Blueprint
from flask.json import jsonify
from math import ceil
import api.v4.api_settings as api_settings
from flask import request
from bson.objectid import ObjectId
from .db_connector import Database
from .elastic import Elastic

# link: https://ew.com/recap/limitless-season-1-episode-12/  https://www.bbc.com/news/world-middle-east-35219693
# ids=[6239b1eddf4b7decb33fbaf2, 6239b1ecdf4b7decb33fbaee, 6239b1ecdf4b7decb33fbae4]

# max and deafult numbers of articles returned by elasticsearch
MAX_SIZE = 20
DEFAULT_SIZE = 10

# /v4/search/
api_v4 = Blueprint("search_routes", __name__, url_prefix="/" + api_settings.API_VERSION)

elastic = Elastic()

# check if number of articles to be returned is valid 
def check_size_validity(size):
    
    if size >= MAX_SIZE:
        size = MAX_SIZE

    elif size <= 0:
        size = DEFAULT_SIZE

    return size


# transforms string of filter parametes from request to list
def string_to_list(params_str):

    # check if filter is used
    if not params_str:
        return None
    # transform keywords string into list
    elif params_str[0] == '[' and params_str[len(params_str) - 1] == ']':
        params_str = params_str[1:-1]
        params_list = params_str.split(',')
        params_list = [item.lstrip() for item in params_list]
        return params_list
    else:
        return None


# main function for searching
@api_v4.route("/search", methods=['GET'])
def search():
    
    query = request.args.get(api_settings.API_SEARCH_QUERY, default=None, type=str)
    search_from = request.args.get(api_settings.API_SEARCH_FROM, default="", type=str)
    search_to = request.args.get(api_settings.API_SEARCH_TO, default="", type=str)
    page_num = request.args.get(api_settings.API_PAGE_NUM, default=1, type=int)
    size = request.args.get(api_settings.API_PAGE_SIZE, default=DEFAULT_SIZE, type=int)
    keywords = request.args.get(api_settings.API_KEYWORDS, default="", type=str)
    regions = request.args.get(api_settings.API_REGIONS, default="", type=str)

    if query is None:
        return "Invalid input, please provide 'q' parameter", 400

    if elastic.check_connection() is None:
        return "Can't connect to Elasticsearch", 503

    if page_num <= 0:
        page_num = 1

    size = check_size_validity(size)
    keywords_list = string_to_list(keywords)
    regions_list = string_to_list(regions)

    resp = elastic.search(query, keywords_list, regions_list, page_num, size)
    total_results = resp['hits']['total']['value']
    total_pages = int(ceil(total_results/size))
    article_ids = elastic.get_ids(resp)
    per_page = len(article_ids)

    Database.initialize()

    articles = []

    for id in article_ids:
        # finds article document in articles collection by id and remove html field
        article = Database.find_one('articles', {'_id': ObjectId(id)})
        article.pop('html')
        articles.append(article) 
        
    response = {
        "query": query,
        "search_from": search_from,
        "search_to": search_to,
        "page_num": page_num,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_results": total_results,
        "results": articles
    }

    return jsonify(response)


# get article by url from mongo db
@api_v4.route("/archive", methods=['GET'])
def get_article_by_link():
    link = request.args.get(api_settings.API_LINK, default=None, type=str)

    if link is None:
        return "Invalid input, please provide 'link' parameter", 400
    
    Database.initialize()
    article = Database.find_one('articles', {'link': link})
        
    response = {
        "article": article
    }

    return jsonify(response)


# get articles by ids from mongo db
@api_v4.route("/report", methods=['GET'])
def get_article_by_id():
    ids = request.args.get(api_settings.API_IDS, default=None, type=str)

    if ids is None:
        return "Invalid input, please provide 'ids' parameter", 400

    article_ids = string_to_list(ids)
    Database.initialize()
    articles = []

    for id in article_ids:
        # finds article document in articles collection by id
        article = Database.find_one('articles', {'_id': ObjectId(id)})
        articles.append(article) 
        
    response = {
        "results": articles
    }

    return jsonify(response)