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
