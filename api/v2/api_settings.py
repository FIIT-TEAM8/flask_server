import os

API_VERSION = "v2"

# API parameters
# /search endpoint
API_SEARCH_QUERY = "q"
API_SEARCH_FROM = "from"
API_SEARCH_TO = "to"
API_SEARCH_LOCALE = "locale"


# environmental variables
MONGO_SERVER_URL = str(os.environ['MONGO_SERVER_URL'] or localhost)
MONGO_SERVER_PORT = str(os.environ['MONGO_SERVER_PORT'] or 27017)
MONGO_USER = str(os.environ['MONGO_USER'] or 'root')
MONGO_PASSWORD = str(os.environ['MONGO_PASSWORD'] or 'password')
MONGO_DB = str(os.environ['MONGO_DB'] or 'admin')
