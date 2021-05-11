import redis
from fastkml import kml

STATIONS_KEY = "stations"

redis_client = redis.Redis(decode_responses = True)

doc = open("stations.kml", "r").read()
stations_kml = kml.KML()
stations_kml.from_string(doc)

features = list(stations_kml.features())
stations = list(features[0].features())

pipeline = redis_client.pipeline(transaction=False)
pipeline.delete(STATIONS_KEY)

for station in stations:
    pipeline.geoadd(STATIONS_KEY, station.geometry.x, station.geometry.y, station.name)

pipeline.zcard(STATIONS_KEY)
responses = pipeline.execute()

print(f"Loaded {responses[len(responses) -1]} stations.")