from flask import Flask
from flask import jsonify
import redis
from fastkml import kml

STATIONS_KEY = "stations"

redis_client = redis.Redis(decode_responses = True)

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
