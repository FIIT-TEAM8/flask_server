import os

API_VERSION = "v2"

# API parameters
# /search endpoint
API_SEARCH_QUERY = "q"
API_SEARCH_FROM = "from"
API_SEARCH_TO = "to"
API_SEARCH_LOCALE = "locale"


# environmental variables
MONGO_INITDB_ROOT_USERNAME = str(os.environ['MONGO_INITDB_ROOT_USERNAME'] or 'root')
MONGO_INITDB_ROOT_PASSWORD = str(os.environ['MONGO_INITDB_ROOT_PASSWORD'] or 'password')