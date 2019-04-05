# Script to add pub data to noise data for linear regression
# Input: Noise data, pub data
# Output: transport-enriched noise data

import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import random
import util

noise_data = json.load(open("data/noise/road_lden_london.json"))
pub_data = json.load(open("data/london_pubs_data.json"))
polygon_list = util.get_polygon_list(noise_data)

for noise_polygon_index in range(0,len(polygon_list)):
    noise_polygon = polygon_list[noise_polygon_index]
    feature = noise_data['features'][noise_polygon_index]
    
    # Check if station lies in the noise polygon
    stations_in_polygon = [
        1 
        for tube_obj in pub_data
        if noise_polygon.contains(Point(tube_obj[0],tube_obj[1]))
    ]
    feature['properties']['distance_to_tube'] = (sum(stations_in_polygon)/len(stations_in_polygon)
        if len(stations_in_polygon) != 0
        else 0
    )
    feature['properties']['noise'] = util.get_random_value(feature["properties"]["NoiseClass"])

output = open('data/noise/noise_data_with_tube_proximity.geojson', 'w')
json.dump(noise_data, output)