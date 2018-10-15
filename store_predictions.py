from database import get_cur
import requests
import random 
from time import sleep

base_url = "https://api.actransit.org/transit/stops/{}/predictions/?token=03398D26A0BBF79AF14C6351C6ADFF77"

cur = get_cur()

def get_stop_id():
    cur.execute("SELECT stop_id FROM stops;")
    stops = cur.fetchall()
    stop = random.choice(stops)
    return stop[0]


def get_prediction_data(stop_id):
    r = requests.get(base_url.format(stop_id))
    predictions = r.json()
    return predictions

def submit_prediction_data(predictions):

    for prediction in predictions:
        print(prediction)

        stop_id = prediction['StopId']
        trip_id = prediction['TripId']
        vehicle_id = prediction['VehicleId']
        route_name = prediction['RouteName']
        predicted_delay = prediction['PredictedDelayInSeconds']
        predicted_departure = prediction['PredictedDeparture']
        prediction_datetime = prediction['PredictionDateTime']

        sql_string=  """
        INSERT INTO predictions VALUES ('{stop_id}', '{trip_id}', '{vehicle_id}', '{route_name}', '{predicted_delay}',
                                        '{predicted_departure}', '{prediction_datetime}');

        """.format(
            stop_id=stop_id,
            trip_id=trip_id,
            vehicle_id=vehicle_id,
            route_name=route_name,
            predicted_delay=predicted_delay,
            predicted_departure=predicted_departure,
            prediction_datetime=prediction_datetime
        )

        cur.execute(sql_string)


truth = True

while(truth):
    stop_id = get_stop_id()
    try:
        predictions = get_prediction_data(stop_id)
        submit_prediction_data(predictions)

    except:
        print("no prediction or malformed data")
    sleep(3)
