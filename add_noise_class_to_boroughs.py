# Script to add noise classes to borough sector level population data for linear regression
# Input: London road noise data, population data
# Output: Pollution data segregated by year

import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
import random
import util
import time

population_data = json.load(open("data/population/london_post_code_sector_population.geojson"))
noise_data = json.load(open("data/noise/road_lden_london.json"))

def build_polygon_noise_list():
    polygon_list = util.get_polygon_list(noise_data)
    return [
        [
            polygon_list[polygon_list_index],
            util.get_random_value(noise_data['features'][polygon_list_index]["properties"]["NoiseClass"])
        ]
        for polygon_list_index in range(0, len(polygon_list))
    ]

def build_polygon_population_list():
    polygon_list = util.get_polygon_list(population_data)
    return [
        [
            polygon_list[polygon_list_index],
            population_data['features'][polygon_list_index]["properties"]['name'],
            population_data['features'][polygon_list_index]["properties"]['population']
        ]
        for polygon_list_index in range(0, len(polygon_list))
    ]

polygon_noise_list = build_polygon_noise_list()
polygon_population_list = build_polygon_population_list()

# Cycle through every borough sector to calculate its noise level
for population_list_index in range(0, len(polygon_population_list)):

    population_list = polygon_population_list[population_list_index]
    population_polygon = population_list[0]

    borough_sector_area = population_polygon.area
    running_noise = 0

    # Check if an intersection exists between the nosie polygon and borough sector
    # If it does, add that noise to running total
    for noise_list in polygon_noise_list:
        print('ayo naya')
        noise_polygon = noise_list[0]
        noise = noise_list[1]
        intersected_polygon = population_polygon.intersection(noise_polygon)
        if not intersected_polygon.is_empty:
            running_noise += noise/intersected_polygon.area

    # Add running noise to borough sector
    population_data['features'][population_list_index]['properties']['noise'] = running_noise

output = open('data/population/population_data_with_noise', 'w')
json.dump(population_data, output)