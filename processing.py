import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from models import Stop, Vehicle
from database import get_cur
import re
import json
import csv
from collections import defaultdict
from geopy.distance import vincenty
from shapely import wkb

cur = get_cur()

stops = []
stops_file = open("stops.csv", "r")
stops_table = csv.reader(stops_file, delimiter=',')
for stops_row in stops_table:
    stop = Stop(stops_row)
    stops.append(stop)

#This gets all the vehicles and puts them into an array of objects.
def populate_vehicles(cur):
    cur.execute("SELECT * FROM rapidsubset LIMIT 100;")
    vehicles = []
    vehicles_table = cur.fetchall()
    for vehicles_row in vehicles_table:
        vehicle = Vehicle(vehicles_row)
        vehicles.append(vehicle)
    return vehicles

def get_stops_on_route(cur, vehicle, stops):
    stops_on_route = []
    for stop in stops:
        
        for route in stop.json_routes:
            if vehicle.route_id == route:
                stops_on_route.append(stop)

    
    return stops_on_route
            

# Now we have a list of the stops for the route the vehicle is on
# Geom is at stop[2]
def get_distance_from_stop(cur, vehicle, stop):
   
    
    vehicle_point = wkb.loads(vehicle.loc, hex=True)
    stop_point = wkb.loads(stop.geom, hex=True)
    distance = vincenty((vehicle_point.y, vehicle_point.x), (stop_point.y, stop_point.x)).m

    # sql_string = """
    #             SELECT ST_Distance('{vehicle_location}'::geography, '{stop_location}'::geography)
    #             """.format(vehicle_location=vehicle.loc, stop_location=stop.geom)
    # cur.execute(sql_string)
    # distance = cur.fetchall()[0]
    # print("distance: ", distance)
    return distance
    


vehicles = populate_vehicles(cur)
# vehicle_map = defaultdict(list)
vehicle_map = {}
for vehicle in vehicles:
    distance_list = []
    stops_on_route = get_stops_on_route(cur, vehicle, stops)
    for stop in stops_on_route:
        distance_list.append(get_distance_from_stop(cur, vehicle, stop))
        vehicle_map[vehicle] = min(distance_list)
        # print("distance stop<-->vehicle", dist)
        
    sorted_by_value = sorted(vehicle_map.items(), key=lambda kv: kv[1])
    print(sorted_by_value)








