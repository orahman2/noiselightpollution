import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
import random
import util
import time

population_data = json.load(open("lodon_post_code_sector_population.geojson"))
noise_data = json.load(open("road_lden_london.json"))

def build_polygon_noise_list():
    features = noise_data["features"]
    polygon_list = GeometryCollection([
        shape(feature["geometry"]).buffer(0)
        for feature
        in features
        ]).geoms

    polygon_noise_list = []

    for polygon_list_index in range(0, len(polygon_list)):
        temp_obj = [
            polygon_list[polygon_list_index],
            util.get_random_value(util.discrete_continuous_map[features[polygon_list_index]["properties"]["NoiseClass"]])
            ]
        polygon_noise_list.append(temp_obj)

    return polygon_noise_list

polygon_noise_list = build_polygon_noise_list()

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
            features[polygon_list_index]["properties"]['name'],
            features[polygon_list_index]["properties"]['population']
            ]
        polygon_population_list.append(temp_obj)

    return polygon_population_list

polygon_population_list = build_polygon_population_list()

total_iterations = len(polygon_population_list)*len(polygon_noise_list)
lowest = 0

for population_list_index in range(0, len(polygon_population_list)):
    population_list = polygon_population_list[population_list_index]
    population_polygon = population_list[0]

    borough_sector_area = population_polygon.area
    running_noise = 0

    for noise_list in polygon_noise_list:
        noise_polygon = noise_list[0]
        noise = noise_list[1]
        intersected_polygon = population_polygon.intersection(noise_polygon)
        if not intersected_polygon.is_empty:
            running_noise += noise

    population_data['features'][population_list_index]['properties']['noise'] = running_noise

output = open('population_data_with_noise', 'w')
json.dump(population_data, output)