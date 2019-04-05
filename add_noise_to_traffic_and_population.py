# Script to add noise data of different kinds to traffic points
# Input: Noise and traffic data
# Output: Noise-enriched traffic data

import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
import random
import util
import time
noise_data_prefix = "data/noise/"
noise_data = {
        'road_noise_avg': json.load(open(f"{noise_data_prefix}road_lden_london.geojson")),
        'road_noise_day': json.load(open(f"{noise_data_prefix}road_laeq_16h_latlong.geojson")),
        'road_noise_night': json.load(open(f"{noise_data_prefix}road_laeq_16h_latlong.geojson")),
        'rail_noise_avg': json.load(open(f"{noise_data_prefix}rail_lden_latlong.geojson")),
        'rail_noise_day': json.load(open(f"{noise_data_prefix}rail_laeq_16h_latlong.geojson")),
        'rail_noise_night': json.load(open(f"{noise_data_prefix}rail_laeq_16h_latlong.geojson"))
    }
    
traffic_data = json.load(open("data/traffic/traffic_data_with_population.geojson"))

def build_polygon_noise_list(noise_objects):
    polygon_list = util.get_polygon_list(noise_objects)
    return [
        [
            polygon_list[polygon_list_index],
            util.get_random_value(noise_objects['features'][polygon_list_index]["properties"]["NoiseClass"])
        ]
        for polygon_list_index in range(0, len(polygon_list))
    ]
        
noise_objects_dict = { x:build_polygon_noise_list(noise_data[x]) for x in noise_data.keys() }

# Iterate through each traffic point to add all noise classes to it
for traffic_obj in traffic_data['features']:
    traffic_point = Point(traffic_obj['geometry']['coordinates'])

    for noise_object_type in noise_objects_dict.keys():
        noise_object_list = noise_objects_dict[noise_object_type]
        
        for noise_list_index in range(0, len(noise_object_list)):
            
            noise_list = noise_object_list[noise_list_index]
            noise_polygon = noise_list[0]
            print('ayo homie')

            if noise_polygon.contains(traffic_point):
                traffic_obj['properties'][noise_object_type] = noise_list[1]
                break

output = open('data/traffic/traffic_data_with_noise_and_population.geojson', 'w')
json.dump(traffic_data, output)