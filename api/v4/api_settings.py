import os

API_VERSION = "v4"

# API parameters
# /search endpoint
API_SEARCH_QUERY = "q"
API_SEARCH_FROM = "from"
API_SEARCH_TO = "to"
API_PAGE_NUM = "page"
API_PAGE_SIZE = "size"
API_KEYWORDS = "keywords"
API_REGIONS = "regions"

# /archive endpoint
API_LINK = "link"

# /pdf report endpoint
API_IDS = "ids"

# environmental variables
MONGO_SERVER_URL = str(os.environ['MONGO_SERVER_URL'] or 'localhost')
MONGO_SERVER_PORT = str(os.environ['MONGO_SERVER_PORT'] or 27017)
MONGO_USER = str(os.environ['MONGO_USER'] or 'root')
MONGO_PASSWORD = str(os.environ['MONGO_PASSWORD'] or 'password')
# NOTE: switch db name to "ams" when custom mongo_db image is used
MONGO_DB = str(os.environ['MONGO_DB'] or 'ams')

ES_HOST = str(os.environ['ES_HOST'] or 'localhost')
ES_PORT = str(os.environ['ES_PORT'] or 9200)
ES_USER = str(os.environ['ES_USER'] or 'root')
ES_PASSWORD = str(os.environ['ES_PASSWORD'] or '123')
ELASTIC_INDEX_NAME = str(os.environ['ELASTIC_INDEX_NAME'] or 'main')
ES_PROTOCOL="https"


ES_CONNECTION_STRING = "{protocol}://{username}:{password}@{host}:{port}/".format(
    protocol=ES_PROTOCOL,
    username=ES_USER,
    password=ES_PASSWORD,
    host=ES_HOST,
    port=ES_PORT
)

ES_SEARCH_STRING = "{protocol}://{host}:{port}/{index}/_search".format(
    protocol=ES_PROTOCOL,
    host=ES_HOST,
    port=ES_PORT,
    index=ELASTIC_INDEX_NAME
    )