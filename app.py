import redis
from redisearch import Client
import os
from operator import attrgetter

from flask import Flask
from flask import jsonify
from flask import render_template
from fastkml import kml

STATIONS_KEY = "stations"

client = Client("idx:stations", host=os.environ.get("REDIS_HOST",
                                                    default="localhost"))


app = Flask(__name__)


class ResourceNotFound(Exception):

    def __init__(self, message):
        super().__init__()
        self.detail = message
        self.code = 404
        self.title = "Not found"

    def to_dict(self):
        return self.__dict__


def transform_geosearch_response(response):
    return [{"name": item[0], "location": {"latitude": item[1][1], "longitude": item[1][0]}} for item in response]


@app.route("/api/search/byradius/<latitude>/<longitude>/<radius>/<radius_unit>")
def search_by_radius(latitude, longitude, radius, radius_unit):
    # http://localhost:5000/api/search/byradius/37.7589057/-122.3757349/10/mi
    results = client.redis.execute_command(
        f"geosearch {STATIONS_KEY} fromlonlat {longitude} {latitude} byradius {radius} {radius_unit} withcoord")
    return jsonify(transform_geosearch_response(results))


@app.route("/api/search/bybox/<latitude>/<longitude>/<box_width>/<box_height>/<box_unit>")
def search_by_box(latitude, longitude, box_width, box_height, box_unit):
    # http://localhost:5000/api/search/bybox/37.7589057/-122.3757349/5/10/mi
    results = client.redis.execute_command(
        f"geosearch {STATIONS_KEY} fromlonlat {longitude} {latitude} bybox {box_width} {box_height} {box_unit} withcoord")
    return jsonify(transform_geosearch_response(results))


@app.route("/api/position/<station_name>")
def search_by_station_name(station_name):
    stations = client.redis.geopos(STATIONS_KEY, station_name)
    station = stations[0]
    if not station:
        raise ResourceNotFound(
            message=f"The station named {station_name} could not be found")
    latitude, longitude = station
    return jsonify({"name": station_name, "location": {"latitude": latitude, "longitude": longitude}})


@app.route("/api/distance/<first_station_name>/<second_station_name>/<distance_unit>")
def compute_distance(first_station_name: str, second_station_name: str, distance_unit: str = "km"):
    first_station = client.redis.geopos(STATIONS_KEY, first_station_name)
    if not first_station:
        raise ResourceNotFound(
            message=f"Station named {first_station_name} not found")
    second_station = client.redis.geopos(STATIONS_KEY, second_station_name)
    if not second_station:
        raise ResourceNotFound(
            message=f"Station named {first_station_name} not found")
    if distance_unit not in ["m", "km", "mi", "ft"]:
        return jsonify({"message": f"Invalid unit provided {distance_unit}"})
    try:
        distance = client.redis.geodist(
            STATIONS_KEY, first_station_name, second_station_name, distance_unit)
        return jsonify({"first station": first_station_name, "second station": second_station_name, "units": distance_unit, "distance": distance})
    except Exception as e:
        raise ResourceNotFound(message=f"Error Occured {e}")


@app.route("/api/search/bycity/<city_name>")
def search_by_city_name(city_name: str):
    res = client.search(city_name)
    output = []
    for i in range(res.total-1):
        station = res.docs[i]
        latitude, longitude, Field_1, City = attrgetter('Lat', 'Long', 'Field_1', 'City')(station)
        output.append({"name": Field_1, "city": City, "location": {
                      "latitude": latitude, "longitude": longitude}})
    return jsonify(output)


@app.errorhandler(ResourceNotFound)
def resource_not_found(e):
    return jsonify(e.to_dict())


@app.route("/")
def homepage():
    return render_template("homepage.html")
