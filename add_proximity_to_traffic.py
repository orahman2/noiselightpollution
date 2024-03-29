# Script to add tube and airport data to traffic points
# Input: London road traffic data, transport data
# Output: transport-enriched traffic data

import json
import util
from shapely.geometry import Point
import time
import constants

tube_station_data = json.load(open("data/london_tube_coordinates.json"))
traffic_data = json.load(open('data/traffic/traffic_data_with_noise_and_population.geojson'))

# Iterate through traffic points and enrich the data set
for traffic_feature in traffic_data['features']:

    # Add closest tube station's distance and traffic
    closest_tube_station = sorted(
        tube_station_data,
        key=lambda tube_obj: util.get_distance_to_place(traffic_feature, tube_obj)
    )[0]
    distance_to_closest_tube = util.get_distance_to_place(traffic_feature, closest_tube_station)
    traffic_feature['properties']['distance_to_closest_tube_station'] = distance_to_closest_tube
    traffic_feature['properties']['people_at_closest_tube_station'] = closest_tube_station['people_count']

    # Add distance to closest airport
    closest_airport = sorted(
        constants.airport_coordinates,
        key=lambda airport_obj: util.get_distance_to_place(traffic_feature, airport_obj)
    )[0]
    distance_to_closest_airport = util.get_distance_to_place(traffic_feature, closest_airport)
    traffic_feature['properties']['distance_to_closest_airport'] = distance_to_closest_airport

    # Add distance to central london
    distance_to_london = util.get_distance_to_place(traffic_feature, {'location':[51.5074, -0.1278]})
    traffic_feature['properties']['distance_to_london'] = distance_to_london

json.dump(traffic_data, open('data/traffic/traffic_data_with_noise_and_population_and_proximity.geojson', 'w'))