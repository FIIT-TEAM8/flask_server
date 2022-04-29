import requests
import json
import os
import api.v4.api_settings as api_settings


FIRST_YEAR = 2000
LAST_YEAR = 2100


def load_keywords(categories):
    
    keywords = []

    # load json containg all categories and their keywords
    with open('static/en_keyword_categories.json', encoding='utf8') as file:
        keywords_file = json.load(file)

    for cat in categories:
        cat_keywords = keywords_file[cat]
        keywords.extend(cat_keywords)

    return keywords


# handle elasticsearch through requests library
class Elastic:
    def __init__(self):
        pass

    
    # test request to check connection
    def check_connection(self):
        try:
            response = requests.get("{protocol}://{host}:{port}/".format(
                    protocol=api_settings.ES_PROTOCOL,
                    host=api_settings.ES_HOST,
                    port=api_settings.ES_PORT
                ),
                verify=False, 
                auth=(api_settings.ES_USER, api_settings.ES_PASSWORD))
            
            if response.status_code == 200:
                return True
            return None

        except Exception as e:
            return None


    # get ids from elasticsearch results
    def get_ids(self, results):
        ids = []

        for res in results["hits"]["hits"]:
            ids.append(res["_id"])

        return ids
    

    # builds elasticsearch query with or without filters
    def build_query(self, query, categories, regions, search_from, search_to, page_num, size):
        
        # load default body of query withou any filters
        with open('default_query.json', encoding='utf8') as file:
            self.body = json.load(file)
      
        # replace placeholder values
        self.body['from'] = self.body['from'].replace('$from', str(page_num * size - size))
        self.body['size'] = self.body['size'].replace('$size', str(size))
        self.body['query']['bool']['must'][0]['match_phrase']['html'] = self.body['query']['bool']['must'][0]['match_phrase']['html'].replace('$query', query)

        # add crime keywords filter
        if categories:
            keywords = load_keywords(categories)
            keywords_filter = {
                "terms": {
                    "keywords.keyword": keywords
                }
            }
            self.body["query"]["bool"]["must"].append(keywords_filter)
        
        # add regions filter
        if regions:
            regions_filter = {
                "terms": {
                    "region": regions
                }
            }
            self.body["query"]["bool"]["must"].append(regions_filter)
        
        # add filtering by date
        if search_from or search_to:
            date_filter = { 
                "range": {
                    "published": {
                    }
                }
            }
            if search_from:
                year_from = search_from[:4]
                date_filter["range"]["published"]["gte"] = year_from
                if not search_to:
                    date_filter["range"]["published"]["lte"] = LAST_YEAR

            if search_to:
                year_to = search_to[:4]
                date_filter["range"]["published"]["lte"] = year_to
                if not search_from:
                    date_filter["range"]["published"]["gte"] = FIRST_YEAR

            self.body["query"]["bool"]["must"].append(date_filter)


    # build query then search
    def search(self, query, categories, regions, search_from, search_to, page_num, size):
        self.build_query(query, categories, regions, search_from, search_to, page_num, size)
        headers = {}
        response = requests.get(api_settings.ES_SEARCH_STRING, 
            headers=headers, 
            json=self.body, 
            verify=False, 
            auth=(api_settings.ES_USER, api_settings.ES_PASSWORD))
        return response.json()
    

    def get_elastic_stats(self):
        es_url = "{protocol}://{host}:{port}/{index}/".format(
            protocol=api_settings.ES_PROTOCOL,
            host=api_settings.ES_HOST,
            port=api_settings.ES_PORT,
            index=api_settings.ELASTIC_INDEX_NAME)
        num_of_articles = requests.get(es_url + "_count", verify=False, auth=(api_settings.ES_USER, api_settings.ES_PASSWORD)).json()["count"]
        index_size = requests.get(es_url + "_stats/store", verify=False, auth=(api_settings.ES_USER, api_settings.ES_PASSWORD)).json()["_all"]["total"]["store"]["size_in_bytes"]
        return {"count": num_of_articles, "size": index_size}


