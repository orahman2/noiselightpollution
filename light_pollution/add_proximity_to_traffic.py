# Script to add transport and proximity based data to traffic file
# Input: Tube coordinates and light pollution-enriched traffic data
# Output: Enrich traffic data with tube coordinates

import json
import util
from shapely.geometry import Point
import time
import constants

tube_station_data = json.load(open("data/london_tube_coordinates.json"))
traffic_data = json.load(open('data/light/light_pollution_with_traffic.geojson'))

for traffic_feature in traffic_data['features']:
    # Get closest tube station and calculate distance
    # Enrich data with calculated distance and number of people
    closest_tube_station = sorted(
        tube_station_data,
        key=lambda tube_obj: util.get_distance_to_place(traffic_feature, tube_obj)
    )[0]
    distance_to_closest_tube = util.get_distance_to_place(traffic_feature, closest_tube_station)
    traffic_feature['properties']['distance_to_closest_tube_station'] = distance_to_closest_tube
    traffic_feature['properties']['people_at_closest_tube_station'] = closest_tube_station['people_count']

    # Enrich data with airport and central London distance
    closest_airport = sorted(
        constants.airport_coordinates,
        key=lambda airport_obj: util.get_distance_to_place(traffic_feature, airport_obj)
    )[0]
    distance_to_closest_airport = util.get_distance_to_place(traffic_feature, closest_airport)
    traffic_feature['properties']['distance_to_closest_airport'] = distance_to_closest_airport
    
    traffic_feature['properties']['distance_to_london'] = util.get_distance_to_place(traffic_feature, {'location': [51.5074, -0.1278]})

json.dump(traffic_data, open('data/traffic/traffic_data_with_light_and_population_and_proximity.geojson', 'w'))