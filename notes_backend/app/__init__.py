import os
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp
from .services import init_db

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["API_TITLE"] = "My Flask API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Ensure DB path is configurable by env variable
app.config["NOTES_DB_PATH"] = os.environ.get("NOTES_DB_PATH", "notes.db")

api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(notes_blp)

# Initialize the database when the app starts.
with app.app_context():
    init_db()
