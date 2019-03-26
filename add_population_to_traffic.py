import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
import random
import util
import time

population_data = json.load(open("lodon_post_code_sector_population.geojson"))
traffic_data = json.load(open("london_traffic_2012.geojson"))

def build_polygon_population_list():
    features = population_data["features"]
    polygon_list = GeometryCollection([
        shape(feature["geometry"]).buffer(0)
        for feature
        in features
        ]).geoms

    polygon_population_list = []

    for polygon_list_index in range(0, len(polygon_list)):
        temp_obj = [
            polygon_list[polygon_list_index],
            features[polygon_list_index]["properties"]['population']
            ]
        polygon_population_list.append(temp_obj)

    return polygon_population_list

polygon_population_list = build_polygon_population_list()

for traffic_obj in traffic_data['features']:
    traffic_point = Point(traffic_obj['geometry']['coordinates'])

    for population_list_index in range(0, len(polygon_population_list)):
        population_list = polygon_population_list[population_list_index]
        population_polygon = population_list[0]

        if population_polygon.contains(traffic_point):
            traffic_obj['properties']['population'] = population_list[1]
            break

output = open('traffic_data_with_population.geojson', 'w')
json.dump(traffic_data, output)