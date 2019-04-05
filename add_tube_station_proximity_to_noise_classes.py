# Script to add noise data to tube data for linear regression
# Input: London noise data, tube data
# Output: transport-enriched noise data

import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import random
import sys
import util

noise_data = json.load(open("data/noise/road_lden_london.json"))
tube_station_data = json.load(open("data/london_tube_coordinates.json"))

polygon_list = util.get_polygon_list(noise_data)

tube_stations_found = []

for noise_polygon_index in range(0,len(polygon_list)):
    progress = noise_polygon_index/len(polygon_list)

    noise_polygon = polygon_list[noise_polygon_index]
    feature = noise_data['features'][noise_polygon_index]
    
    people_in_polygon = []
    
    for tube_obj in tube_station_data:
        lat = tube_obj['location'][1]
        lon = tube_obj['location'][0]
        lat_lon_str = f"{lat},{lon}"
        point = Point(lat, lon)

        # Check if data has been cached
        if (not lat_lon_str in people_in_polygon) and noise_polygon.contains(point):
            people_in_polygon.append(tube_obj['people_count'])
        else:
            # Check whether geographic feature is polygon or multipolygon
            # Add tube traffic divided by proximity
            if not isinstance(noise_polygon, MultiPolygon):
                distance_to_station = noise_polygon.exterior.distance(point)
                people_in_polygon.append(tube_obj['people_count']/(50*distance_to_station))
            else:
                distance_to_station = min([
                    noise_multipolygon.exterior.distance(point)
                    for noise_multipolygon in noise_polygon
                ])
                people_in_polygon.append(tube_obj['people_count']/(50*distance_to_station))
    
    # Add all people inside the polygon 
    # and people outside the polygon divided by their distance to the polygon
    feature['properties']['people_count'] = sum(people_in_polygon) if len(people_in_polygon) != 0 else 0
    feature['properties']['noise'] = util.get_random_value(feature["properties"]["NoiseClass"])

output = open('data/noise/noise_data_with_tube_proximityo.geojson', 'w')
json.dump(noise_data, output)
