import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from database import get_cur

cur = get_cur()
base_url = "https://api.actransit.org/transit/gtfsrt/vehicles/?token=369BB8F6542E51FF57BC06577AFE829C"

feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get(base_url)
feed.ParseFromString(response.content)

for entity in feed.entity:
    print(entity)
    break