from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flasgger import Swagger
from .api.docs.config import swagger_config, template

load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('app.config.Config')
db = SQLAlchemy(app)

Swagger(app, config=swagger_config, template=template)

from app.api.routes.randObject import bp, url_prefix
app.register_blueprint(bp, url_prefix=url_prefix)
