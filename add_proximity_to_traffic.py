import json
import util
from shapely.geometry import Point
import time

tube_station_data = json.load(open("london_tube_coordinates.json"))

airport_coordinates = [
    {'location':[51.4700, -0.4543]},
    {'location':[51.1537, -0.1821]},
    {'location':[51.8763, -0.3717]},
    {'location':[51.5048, 0.0495]},
    {'location':[51.8860, 0.2389]}
]

traffic_data = json.load(open('traffic_data_with_noise_and_population.geojson'))

def get_distance_to_place(traffic_feature, place):
    y1 = traffic_feature['geometry']['coordinates'][0]
    x1 = traffic_feature['geometry']['coordinates'][1]
    x2 = place['location'][0]
    y2 = place['location'][1]
    return util.distance(x1, y1, x2, y2)
counnerrrr = 0
num_of_feats = len(traffic_data['features'])
for traffic_feature in traffic_data['features']:
    counnerrrr+=1
    closest_tube_station = sorted(tube_station_data, key=lambda tube_obj: get_distance_to_place(traffic_feature, tube_obj))[0]
    distance_to_closest_tube = get_distance_to_place(traffic_feature, closest_tube_station)
    traffic_feature['properties']['distance_to_closest_tube_station'] = distance_to_closest_tube
    traffic_feature['properties']['people_at_closest_tube_station'] = closest_tube_station['people_count']

    closest_airport = sorted(airport_coordinates, key=lambda airport_obj: get_distance_to_place(traffic_feature, airport_obj))[0]
    distance_to_closest_airport = get_distance_to_place(traffic_feature, closest_airport)
    traffic_feature['properties']['distance_to_closest_airport'] = distance_to_closest_airport

    distance_to_london = get_distance_to_place(traffic_feature, {'location':[51.5074, -0.1278]})
    traffic_feature['properties']['distance_to_london'] = distance_to_london
    
    print(f"{counnerrrr} of {num_of_feats} is {(100*counnerrrr)/num_of_feats}%")

json.dump(traffic_data, open('traffic_data_with_noise_and_population_and_proximity.geojson', 'w'))