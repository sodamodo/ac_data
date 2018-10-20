import requests
import psycopg2
from google.transit import gtfs_realtime_pb2
from database import get_cur
import re
import json
cur = get_cur()

cur.execute(
    """
    SELECT * FROM stops LIMIT 100;
    """

)

stops_list = cur.fetchall()
# print(stops_list)

for stop in stops_list:
    stop_id = stop[3]
    route_set = stop[5]
    
    route_array = route_set.split(" ")
    # master_array.append(master_array[1].split(" "))
    for n in route_array:
        if n.isdigit() == False:
            route_array.remove(n)

    print("array of numbered routes", route_array)
    print("string of json route number arrays for SQL insertion", json.dumps(route_array))



    # num_only = m.group(0)
    # # print("route list string with no letters: ", num_only)
    # route_array = num_only.split(" ")
    # if ''  in route_array:
    #     route_array.remove('')
    # if len(route_array) > 1:
    #     print("this route array has multiple", route_array)
    

# routes_list = cur.fetchall()

# for i in routes_list:
#     route_set = i[0]
#     m = re.search('\d*\s*', route_set)
#     num_only =  
# print(routes_list)

# WITH (SELECT * FROM vehicles_copy WHERE id = '2ddd9b66-8975-4830-8328-c2195620162d') AS vehicle 

# SELECT * FROM routes WHERE 