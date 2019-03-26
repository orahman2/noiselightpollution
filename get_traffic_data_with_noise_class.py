#! usr/bin/env python

from sys import argv
from os.path import exists
import simplejson as json 
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
script, out_file = argv

counter = 0

traffic_data = json.load(open("traffic_data_geo_clean.geojson"))
noise_data = json.load(open("road_lden_london.json"))

def build_polygon_noise_list():
    features = noise_data["features"]
    print(features[0])
    polygon_list = GeometryCollection([
        shape(feature["geometry"]).buffer(0)
        for feature
        in features
        ]).geoms

    polygon_noise_list = []

    for polygon_list_index in range(0, len(polygon_list)):
        temp_obj = [
            polygon_list[polygon_list_index],
            features[polygon_list_index]["properties"]["NoiseClass"]
            ]
        polygon_noise_list.append(temp_obj)

    return polygon_noise_list

polygon_noise_list = build_polygon_noise_list()

def get_noise_class(point_x_cor, point_y_cor):
    counter += 1
    print(counter)
    point = Point(point_x_cor, point_y_cor)

    for entry in polygon_noise_list:
        if entry[0].contains(point):
            return entry[1]
    return None

geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry" : {
            "type": "Point",
            "coordinates": [obj["geometry"]["coordinates"][0], obj["geometry"]["coordinates"][1]],
            },
        "properties" : obj["properties"],
        "noise_class": get_noise_class(obj["geometry"]["coordinates"][0], obj["geometry"]["coordinates"][1])
     } for obj in traffic_data["features"]]
}


output = open(out_file, 'w')
json.dump(geojson, output)

# print geojson