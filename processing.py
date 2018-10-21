import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from models import Stop, Vehicle
from database import get_cur
import re
import json
cur = get_cur()




#This gets all the vehicles and puts them into an array of objects.
def populate_vehicles(cur):
    cur.execute("SELECT * FROM rapidsubset;")
    vehicles = []
    vehicles_table = cur.fetchall()
    for vehicles_row in vehicles_table:
        vehicle = Vehicle(vehicles_row)
        vehicles.append(vehicle)
    return vehicles

def get_stops_on_route(cur, vehicle):
    stops_on_route = []
    stops = []
    cur.execute("SELECT * FROM stops;")
    stops_table = cur.fetchall()
    for stops_row in stops_table:
        stop = Stop(stops_row)
        stops.append(stop)
        
    for stop in stops:
        for route in stop.json_routes:
            # print(stop_route)
            if vehicle.route_id == route:
                stops_on_route.append(stop)

    
    return stops_on_route
            

# Now we have a list of the stops for the route the vehicle is on
# Geom is at stop[2]
def get_distance_from_stop(cur, vehicle, stop):
   
    sql_string = """
                SELECT ST_Distance('{vehicle_location}'::geography, '{stop_location}'::geography)
                """.format(vehicle_location=vehicle.loc, stop_location=stop.geom)
    cur.execute(sql_string)
    return cur.fetchall()[0]


vehicles = populate_vehicles(cur)
vehicle_map = {}
for vehicle in vehicles:
    vehicle_map[vehicle] = []
    stops = get_stops_on_route(cur, vehicle)
    for stop in stops:
        vehicle_map[vehicle].append(get_distance_from_stop(cur, vehicle, stop))
    print("cycled!")    
    








