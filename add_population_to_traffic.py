# Script to add populatin data to traffic
# Input: London road traffic data, population data
# Output: Pollution-enriched traffic data

import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
import random
import util
import time

population_data = json.load(open("data/population/london_post_code_sector_population.geojson"))
traffic_data = json.load(open("data/traffic/london_traffic_2012.geojson"))

def build_polygon_population_list():
    polygon_list = util.get_polygon_list(population_data)
    return [
        [
            polygon_list[polygon_list_index],
            population_data['features'][polygon_list_index]["properties"]['population']
        ]
        for polygon_list_index in range(0, len(polygon_list))
    ]

polygon_population_list = build_polygon_population_list()

for traffic_obj in traffic_data['features']:
    traffic_point = Point(traffic_obj['geometry']['coordinates'])

    for population_list_index in range(0, len(polygon_population_list)):
        population_list = polygon_population_list[population_list_index]
        population_polygon = population_list[0]

        if population_polygon.contains(traffic_point):
            traffic_obj['properties']['population'] = population_list[1]
            break

output = open('data/traffic/traffic_data_with_population.geojson', 'w')
json.dump(traffic_data, output)