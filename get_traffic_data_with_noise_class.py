# Script to add noise to traffic
# Input: Noise class and traffic
# Output: noise-enriched traffic data

from sys import argv
from os.path import exists
import simplejson as json 
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
import util

script, out_file = argv

traffic_data = json.load(open("data/traffic/traffic_data_geo_clean.geojson"))
noise_data = json.load(open("data/noise/road_lden_london.json"))

def build_polygon_noise_list():
    polygon_list = util.get_polygon_list(noise_data)
    return [
        [
            polygon_list[polygon_list_index],
            noise_data["features"][polygon_list_index]["properties"]["NoiseClass"]
        ]
        for polygon_list_index in range(0, len(polygon_list))
    ]

polygon_noise_list = build_polygon_noise_list()

# Return noise class for point if it exists
def get_noise_class(point_x_cor, point_y_cor):
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