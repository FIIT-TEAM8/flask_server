import requests
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
    def build_query(self, query, keywords, regions, page_num, size):
        
        # default body of query withou any filters
        self.body = {
            # pagination
            "from": page_num * size - size,
            "size": size,
            "query": {
                "bool": {
                    "must": [
                        # match main query in article itself
                        {
                            "match": {
                                "html": {
                                    "query": query,
                                    "operator": "and"
                                }
                            }
                        },
                    ]
                }
            }
        }

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
        

    # build query then search
    def search(self, query, keywords, regions, page_num, size):
        self.build_query(query, keywords, regions, page_num, size)
        headers = {}
        response = requests.get(api_settings.ES_SEARCH_STRING, 
            headers=headers, 
            json=self.body, 
            verify=False, 
            auth=(api_settings.ES_USER, api_settings.ES_PASSWORD))
        return response.json()