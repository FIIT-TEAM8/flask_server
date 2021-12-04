from flask import Flask
from api.v1.search_routes import search_api as search_api_v1
from api.v2.search_routes import search_api as search_api_v2
from api.v2.json_encoder import MyEncoder

app = Flask(__name__)

app.register_blueprint(search_api_v1, name="search_api_v1")
app.register_blueprint(search_api_v2, name="search_api_v2")
app.json_encoder = MyEncoder


@app.route("/")
def root():
    return "<h1>/v2/search - entrypoint for searching</h1>"


if __name__ == '__main__':
    app.run()