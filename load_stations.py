import os

from redis import ResponseError
from fastkml import kml
from redisearch import Client, IndexDefinition, TextField


STATIONS_KEY = "stations"

SCHEMA = (
    TextField("City"),
)
client = Client("idx:stations", host=os.environ.get("REDIS_HOST",
                                                    default="localhost"))

definition = IndexDefinition(prefix=['station:'])

try:
    client.info()
except ResponseError:
    client.create_index(SCHEMA, definition=definition)

doc = open("stations.kml", "r").read()
stations_kml = kml.KML()
stations_kml.from_string(doc)

features = list(stations_kml.features())
stations = list(features[0].features())

pipeline = client.redis.pipeline(transaction=False)
pipeline.delete(STATIONS_KEY)

for station in stations:
    extended_data = station.extended_data
    sd = extended_data.elements[0]
    station_data = {x["name"]: x["value"] for x in sd.data}

    station_key = f"station:{str(station.name).lower()}"
    pipeline.hmset(station_key, station_data)
    pipeline.geoadd(STATIONS_KEY, station.geometry.x,
                    station.geometry.y, station.name)

pipeline.zcard(STATIONS_KEY)
responses = pipeline.execute()

print(f"Loaded {responses[len(responses) -1]} stations.")
