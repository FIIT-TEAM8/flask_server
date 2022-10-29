from flask import Blueprint
import api.v4.api_settings as api_settings
from .elastic import Elastic
from .db_connector import Database
import json

metadata_v4 = Blueprint("stats_routes", __name__, url_prefix="/api/" + api_settings.API_VERSION)


KEYWORDS_CATEGORIES = "static/en_keyword_categories.json"
LANGUAGE_MAPPINGS = "static/language_code_mapping.json"
REGION_MAPPINGS = "static/region_code_maping.json"
KEYWORDS_TRANSLATION = "static/en_keyword_translation.json"


def human_readable_bytes(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"



@metadata_v4.route("/stats/", methods=["GET"])
def get_stats():
    elastic = Elastic()
    mongo = Database
    mongo.initialize()
    resp = {}
    es_stats = elastic.get_elastic_stats()
    mongo_stats = {"count": mongo.DATABASE["articles"].count_documents({}), 
            "size": mongo.DATABASE.command("dbstats")["dataSize"]}
    mongo_stats["size"] = human_readable_bytes(mongo_stats["size"])
    es_stats["size"] = human_readable_bytes(es_stats["size"])
    resp["elasticsearch"] = es_stats
    resp["mongo"] = mongo_stats
    return resp, 200

@metadata_v4.route("/keyword_categories/", defaults={"category":"all"}, methods=["GET"])
@metadata_v4.route("/keyword_categories/<string:category>", methods=["GET"])
def get_keyword_categories(category):
    categories_data = json.load(open(KEYWORDS_CATEGORIES, encoding="utf-8"))
    if category == "all":
        return categories_data
    if category not in categories_data:
        return "This category does not exist", 404
    
    return {category: categories_data[category]}

@metadata_v4.route("/keyword_translation/", defaults={"keyword":"all"}, methods=["GET"])
@metadata_v4.route("/keyword_translation/<string:keyword>", methods=["GET"])
def get_keyword_translation(keyword):
    keywords_data = json.load(open(KEYWORDS_TRANSLATION, encoding="utf-8"))
    if keyword == "all":
        return keywords_data
    if keyword not in keywords_data:
        return "This keyword does not exist", 404
    
    return {keyword: keywords_data[keyword]}

@metadata_v4.route("/language_mapping/", methods=["GET"])
def get_language_code_mappings():
    return json.load(open(LANGUAGE_MAPPINGS, encoding="utf-8"))

@metadata_v4.route("/region_mapping/", methods=["GET"])
def get_region_code_mappings():
    return json.load(open(REGION_MAPPINGS, encoding="utf-8"))

