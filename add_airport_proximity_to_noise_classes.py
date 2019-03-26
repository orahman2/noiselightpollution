import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import random

noise_data = json.load(open("road_lden_london.json"))
airport_coordinates = [
    Point(-0.4543, 51.4700),
    Point(-0.1821, 51.1537),
    Point(-0.3717, 51.8763),
    Point(0.0495, 51.5048),
    Point(0.2389, 51.8860)
]

polygon_list = GeometryCollection([
    shape(feature["geometry"]).buffer(0)
    for feature
    in noise_data['features']
    ]).geoms

def get_random_value(start_int):
    if start_int == 0 or start_int == 750:
        return random.randint(start_int, start_int + 549)/10
    return random.randint(start_int, start_int + 49)/10
    
discrete_continuous_map = {
    '<=54.9' : 0,
    '55.0-59.9' : 550,
    '60.0-64.9' : 600,
    '65.0-69.9' : 650,
    '70.0-74.9' : 700,
    '>=75.0' : 750
}

for noise_polygon_index in range(0,len(polygon_list)):
    noise_polygon = polygon_list[noise_polygon_index]
    feature = noise_data['features'][noise_polygon_index]
    if isinstance(noise_polygon, MultiPolygon):
        feature['properties']['distance_to_airport'] = min([min([noise_multipolygon.exterior.distance(point) for point in airport_coordinates]) for noise_multipolygon in noise_polygon])
    else:
        rep_point = noise_polygon.representative_point()
        print(f" distance between {airport_coordinates[0]} and {noise_polygon.representative_point()} is {noise_polygon.exterior.distance(airport_coordinates[0])}")
        feature['properties']['distance_to_airport'] = min([noise_polygon.exterior.distance(point) for point in airport_coordinates])
    feature['properties']['noise'] = get_random_value(discrete_continuous_map[feature["properties"]["NoiseClass"]])

output = open('noise_data_with_airport_proximity.geojson', 'w')
json.dump(noise_data, output)
