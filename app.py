import os
from dotenv import load_dotenv
if os.path.exists("./.env"):
    load_dotenv()
from flask import Flask
from api.v1.search_routes import search_api as search_api_v1
from api.v4.metadata_routes import metadata_v4 as metadata_api_v4
from api.v4.search_routes import api_v4
from api.v2.json_encoder import MyEncoder
from dotenv import load_dotenv
from requests.packages import urllib3
from flask_cors import CORS
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


app = Flask(__name__)

app.register_blueprint(search_api_v1, name="search_api_v1")
app.register_blueprint(api_v4, name="api_v4")
app.register_blueprint(metadata_api_v4, name="metada_api_v4")

app.json_encoder = MyEncoder

if (not os.getenv('PRODUCTION')):
    print('RUNNING IN DEVELOPMENT ENV...')
    cors = CORS(app, supports_credentials=True)
else:
    cors = CORS(app, resources={
    r"/*": {
        "origins": ["https://adversea.com", "www.adversea.com", "https://www.adversea.com"]
        }
    })



@app.route("/")
def root():
    return "<h1>/api/v4/search - entrypoint for searching</h1>"


if __name__ == '__main__':
    app.run()
