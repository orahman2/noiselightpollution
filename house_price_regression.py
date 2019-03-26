import json
from shapely.geometry import Point, GeometryCollection
from shapely.geometry.polygon import Polygon
import random
import fiona

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

inner_london_boroughs = ['Lambeth', 'Southwark', 'Kensington and Chelsea', 'Westminster', 'City of London']

noise_data = json.load(open("road_lden_london.json"))
shapes = fiona.open("statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp")
shapes_iter = iter(shapes)
current_shape = next(shapes_iter)

borough_shape_dict = {}

from shapely.geometry import shape
for current_shape in shapes:
    shp_geom = shape(current_shape['geometry'])
    borough_name = current_shape['properties']['NAME']
    print(borough_name)
    if not borough_name in inner_london_boroughs:
        borough_shape_dict[borough_name] = shp_geom

polygon_list = GeometryCollection([
    shape(feature["geometry"]).buffer(0)
    for feature
    in noise_data["features"]
    ]).geoms

noise_features = noise_data['features']
    
for polygon_list_index in range(0, len(polygon_list)):
    polygon = polygon_list[polygon_list_index]
    noise_class = noise_features[polygon_list_index]['properties']['NoiseClass']
    for borough_name in borough_shape_dict.keys:
        if borough_shape_dict[borough_name].contains(polygon):
            print('hi')

json.dump(shapes, 'boroughs_with_average_noise.json')