from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/api/search/byradius")
def search_by_radius():
    return "TODO"

@app.route("/api/search/byrect")
def search_by_rectangle():
    return "TODO"

@app.route("/")
def homepage():
    return "TODO"
