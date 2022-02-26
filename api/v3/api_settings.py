import os

API_VERSION = "v3"

# API parameters
# /search endpoint
API_SEARCH_QUERY = "q"
API_SEARCH_FROM = "from"
API_SEARCH_TO = "to"
API_SEARCH_LOCALE = "locale"
API_PAGE_NUM = "page"

# environmental variables
MONGO_SERVER_URL = str(os.environ['MONGO_SERVER_URL'] or 'localhost')
MONGO_SERVER_PORT = str(os.environ['MONGO_SERVER_PORT'] or 27017)
MONGO_USER = str(os.environ['MONGO_USER'] or 'root')
MONGO_PASSWORD = str(os.environ['MONGO_PASSWORD'] or 'password')
MONGO_DB = str(os.environ['MONGO_DB'] or 'admin')

ELASTIC_SERVER_URL = str(os.environ['ELASTIC_SERVER_URL'] or 'localhost')