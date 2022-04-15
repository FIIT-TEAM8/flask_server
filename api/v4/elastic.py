import requests
import json
import os
import api.v4.api_settings as api_settings


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
    def build_query(self, query, keywords, regions, search_from, search_to, page_num, size):
        
        # load default body of query withou any filters
        with open('default_query.json', encoding='utf8') as file:
            self.body = json.load(file)
      
        # replace placeholder values
        self.body['from'] = self.body['from'].replace('$from', str(page_num * size - size))
        self.body['size'] = self.body['size'].replace('$size', str(size))
        self.body['query']['bool']['must'][0]['match']['html']['query'] = self.body['query']['bool']['must'][0]['match']['html']['query'].replace('$query', query)

        # add crime keywords filter
        if keywords:
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
            if search_to:
                year_to = search_to[:4]
                date_filter["range"]["published"]["lte"] = year_to

            self.body["query"]["bool"]["must"].append(date_filter)


    # build query then search
    def search(self, query, keywords, regions, search_from, search_to, page_num, size):
        self.build_query(query, keywords, regions, search_from, search_to, page_num, size)
        headers = {}
        response = requests.get(api_settings.ES_SEARCH_STRING, 
            headers=headers, 
            json=self.body, 
            verify=False, 
            auth=(api_settings.ES_USER, api_settings.ES_PASSWORD))
        return response.json()