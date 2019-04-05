import math
import random
import time
from shapely.geometry import shape, GeometryCollection
import constants

# Calculates geospatial distance, based on the following post
# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def distance(lat1, lon1, lat2, lon2):
    p = math.pi/180
    a = 0.5 - math.cos((lat2 - lat1) * p)/2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 12742 * math.asin(math.sqrt(a))

# Calls distance method from a geojson perspective
def get_distance_to_place(traffic_feature, place):
    y1 = traffic_feature['geometry']['coordinates'][0]
    x1 = traffic_feature['geometry']['coordinates'][1]
    x2 = place['location'][0]
    y2 = place['location'][1]
    return distance(x1, y1, x2, y2)

# Gets random noise value between given range
def get_random_value(noise_range):
    start_int = constants.discrete_continuous_map[noise_range]
    if start_int == 0 or start_int == 750:
        return random.randint(start_int, start_int + 549)/10
    return random.randint(start_int, start_int + 49)/10

# Convert geometry collection to list of features
def get_polygon_list(feature_list):
    return GeometryCollection([
    shape(feature["geometry"]).buffer(0)
    for feature
    in feature_list['features']
    ]).geoms