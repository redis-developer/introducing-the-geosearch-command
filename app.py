from flask import Flask
from flask import jsonify
import redis
from fastkml import kml

STATIONS_KEY = "stations"

redis_client = redis.Redis(decode_responses = True)

app = Flask(__name__)

@app.route("/api/search/byradius/<latitude>/<longitude>/<radius>/<radius_unit>")
def search_by_radius(latitude, longitude, radius, radius_unit):
    # http://localhost:5000/api/search/byradius/37.7589057/-122.3757349/10/mi
    results = redis_client.execute_command(f"geosearch {STATIONS_KEY} fromlonlat {longitude} {latitude} byradius {radius} {radius_unit} withcoord")
    response = [{"name": item[0], "location": { "latitude": item[1][1], "longitude": item[1][0]}} for item in results]
    return jsonify(response)

@app.route("/api/search/byrect/<latitude>/<longitude>/<box_width>/<box_height>/<box_unit>")
def search_by_rectangle(latitude, longitude, box_width, box_height, box_unit):
    results = redis_client.execute_command(f"geosearch {STATIONS_KEY} fromlonlat {longitude} {latitude} bybox ")
    return "TODO"

@app.route("/")
def homepage():
    return "TODO"
