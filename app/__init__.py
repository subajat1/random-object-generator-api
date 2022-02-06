from flask import Flask, jsonify


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('app.config.Config')


@app.route("/")
def hello_world():
    return jsonify(app='random-object-generator')
