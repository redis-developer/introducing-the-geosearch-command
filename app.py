import redis
import os

from flask import Flask
from flask import jsonify
from flask import render_template
from fastkml import kml

STATIONS_KEY = "stations"

redis_client = redis.Redis(host = os.environ.get("REDIS_HOST",
    default="localhost"), decode_responses = True)

app = Flask(__name__)

def transform_geosearch_response(response):
    return [{"name": item[0], "location": { "latitude": item[1][1], "longitude": item[1][0]}} for item in response]

@app.route("/api/search/byradius/<latitude>/<longitude>/<radius>/<radius_unit>")
def search_by_radius(latitude, longitude, radius, radius_unit):
    # http://localhost:5000/api/search/byradius/37.7589057/-122.3757349/10/mi
    results = redis_client.execute_command(f"geosearch {STATIONS_KEY} fromlonlat {longitude} {latitude} byradius {radius} {radius_unit} withcoord")
    return jsonify(transform_geosearch_response(results))

@app.route("/api/search/bybox/<latitude>/<longitude>/<box_width>/<box_height>/<box_unit>")
def search_by_box(latitude, longitude, box_width, box_height, box_unit):
    # http://localhost:5000/api/search/bybox/37.7589057/-122.3757349/5/10/mi
    results = redis_client.execute_command(f"geosearch {STATIONS_KEY} fromlonlat {longitude} {latitude} bybox {box_width} {box_height} {box_unit} withcoord")
    return jsonify(transform_geosearch_response(results))

@app.route("/")
def homepage():
    return render_template("homepage.html")
