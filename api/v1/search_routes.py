from flask import Blueprint
import api.v1.api_settings as api_settings
from flask import request
from random import randint

# /v1/search/
search_api = Blueprint("search_routes", __name__, url_prefix="/" + api_settings.API_VERSION + "/search")


@search_api.route("/")
def search():
    query = request.args.get(api_settings.API_SEARCH_QUERY, default=None, type=str)
    search_from = request.args.get(api_settings.API_SEARCH_FROM, default="", type=str)
    search_to = request.args.get(api_settings.API_SEARCH_TO, default="", type=str)
    locale = request.args.get(api_settings.API_SEARCH_LOCALE, default="", type=str)
    if query is None:
        return "Invalid input, please provide 'q' parameter", 400
    f = open("sample_lipsum.txt")
    articles = []
    art_body = f.read()
    art_count = randint(5, 10)
    for i in range(0, art_count):
        article = {
            "link": "https://thispersondoesnotexist.com/",
            "published": "2020-01-01",
            "locale": "en-gb",
            "title": "Sample article number " + str(i),
            "body": art_body
        }
        articles.append(article)

    response = {
        "query": query,
        "search_from": search_from,
        "search_to": search_to,
        "locale": locale,
        "result_count": art_count,
        "results": articles
    }

    return response

