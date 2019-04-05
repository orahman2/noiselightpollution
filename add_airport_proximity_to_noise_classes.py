# Script to produce files that can be used to perform linear regression
# Input: London road noise data
# Output: London road noise data enriched with 'distance to closest airport' value

import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import constants
import random
import util

noise_data = json.load(open("data/noise/road_lden_london.geojson"))

# Extract polygons from geo-encoded noise data
polygon_list = util.get_polygon_list(noise_data)

for noise_polygon_index in range(0,len(polygon_list)):
    # access the noise data and associated polygon
    feature = noise_data['features'][noise_polygon_index]
    noise_polygon = polygon_list[noise_polygon_index]

    # Calculate and add distance between point and closest airport
    # Choose method depending on whether geographic object is polygon
    # or mutlipolygon
    if isinstance(noise_polygon, MultiPolygon):
        feature['properties']['distance_to_airport'] = min([
            min([
                noise_multipolygon.exterior.distance(point) 
                for point in constants.airport_points])
            for noise_multipolygon in noise_polygon
        ])

    else:
        feature['properties']['distance_to_airport'] = min([
            noise_polygon.exterior.distance(point) 
            for point in constants.airport_points
        ])
    # Add noise class to polygon
    feature['properties']['noise'] = util.get_random_value(feature["properties"]["NoiseClass"])

output = open('.data/noise/noise_data_with_airport_proximity.geojson', 'w')
json.dump(noise_data, output)
