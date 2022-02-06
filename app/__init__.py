from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('app.config.Config')
db = SQLAlchemy(app)


@app.route("/")
def hello_world():
    return jsonify(app='random-object-generator')

from app.api.routes.randObject import bp, url_prefix
app.register_blueprint(bp, url_prefix=url_prefix)
