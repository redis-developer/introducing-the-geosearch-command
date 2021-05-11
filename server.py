from flask import Flask
from flask import jsonify
import redis
from fastkml import kml

STATIONS_KEY = "stations"

redis_client = redis.Redis(decode_responses = True)

app = Flask(__name__)

@app.route("/api/search/byradius/<latitude>/<longitude>/<radius>/<radius_unit>")
def search_by_radius(latitude, longitude, radius, radius_unit):
    return "TODO"

@app.route("/api/search/byrect/<latitude>/<longitude>/<box_width>/<box_height>/<box_unit>")
def search_by_rectangle(latitude, longitude, box_width, box_height, box_unit):
    return "TODO"

@app.route("/")
def homepage():
    return "TODO"
