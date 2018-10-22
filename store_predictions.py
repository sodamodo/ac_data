from database import get_cur
import requests
import random 
from time import sleep
import csv
from models import Stop, Prediction
from ast import literal_eval
from time import sleep

base_url = "https://api.actransit.org/transit/stops/{}/predictions/?token=78A6470DBD59DB9CDFBF9427A4443A2E"

cur = get_cur()

def get_prediction_data(stop_id):
    r = requests.get(base_url.format(stop_id))
    prediction_list = []
    predictions = r.content

    if r.status_code == '404' or r.content == b'':
        return None
    else:
        
        predictions = predictions.decode("utf-8")
        predictions = literal_eval(predictions)
        for prediction in predictions:
            if type(prediction) != dict:
                continue
            else:
                prediction_list.append(list(prediction.values()))
        return prediction_list 

def submit_prediction_data(prediction):

        sql_string=  """
        INSERT INTO predictions VALUES ('{stop_id}', '{trip_id}', '{vehicle_id}', '{route_name}', '{predicted_delay}',
                                        '{predicted_departure}', '{prediction_datetime}');

        """.format(
            stop_id=prediction.stop_id,
            trip_id=prediction.trip_id,
            vehicle_id=prediction.vehicle_id,
            route_name=prediction.route_name,
            predicted_delay=prediction.predicted_delay,
            predicted_departure=prediction.predicted_departure,
            prediction_datetime=prediction.prediction_datetime
        )

        cur.execute(sql_string)

#This is confusing with get_stops_on_route, need to rename to be less confusing 
def get_stops_for_route(cur, stops, route):
    stops_on_route = []
    for stop in stops:
        for stop_route in stop.json_routes:
            if stop_route == route:
                stops_on_route.append(stop)
    return stops_on_route

truth = True
stops = []
stops_file = open("stops.csv", "r")
stops_table = csv.reader(stops_file, delimiter=',')
for stops_row in stops_table:
    stop = Stop(stops_row)
    stops.append(stop)
while (truth):
    predictions = []
    stop_list = get_stops_for_route(cur, stops, '72')
    for stop in stop_list:
        if get_prediction_data(stop.stop_id) == None:
            continue
        else:
            prediction_data = get_prediction_data(stop.stop_id)
            if type(prediction_data == list):
                try:
                    for prediction in prediction_data:
                        print("type of prediction list...", type(prediction))
                        predictions.append(Prediction(prediction))
                except:
                    continue
    sleep(30)
    print("cycled!")

# truth = True

# while(truth):
#     stop_id = get_stop_id()
#     try:
#         predictions = get_prediction_data(stop_id)
#         submit_prediction_data(predictions)

#     except:
#         print("no prediction or malformed data")
#     sleep(3)