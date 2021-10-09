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

@app.route("/api/position/<station_name>")
def search_by_station_name(station_name):
    stations = redis_client.geopos(STATIONS_KEY, station_name)
    station = stations[0]
    if not station:
        raise ResourceNotFound(message=f"The station named {station_name} could not be found")
    latitude, longitude = station
    return jsonify({"name": station_name, "location": {"latitude": latitude, "longitude": longitude}})

class ResourceNotFound(Exception):

    def __init__(self, message):
        super().__init__()
        self.detail = message
        self.code = 404
        self.title = "Not found"

    def to_dict(self):
        return self.__dict__

@app.errorhandler(ResourceNotFound)
def resource_not_found(e):
    return jsonify(e.to_dict())

@app.route("/")
def homepage():
    return render_template("homepage.html")
