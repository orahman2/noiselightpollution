import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import random
import sys

noise_data = json.load(open("road_lden_london.json"))
# tube_station_coordiates = [Point(coordinate[0], coordinate[1]) for coordinate in json.load(open("london_tube_coordinates.json"))]
tube_station_data = json.load(open("london_tube_coordinates.json"))

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

tube_stations_found = []
counter = 0
for noise_polygon_index in range(0,len(polygon_list)):
    progress = noise_polygon_index/len(polygon_list)
    counter += 1
    if counter%1000 == 0.0:
        print(progress)
    noise_polygon = polygon_list[noise_polygon_index]
    feature = noise_data['features'][noise_polygon_index]
    
    people_in_polygon = []
    
    for tube_obj in tube_station_data:
        lat = tube_obj['location'][1]
        lon = tube_obj['location'][0]
        lat_lon_str = f"{lat},{lon}"
        point = Point(lat, lon)
        if (not lat_lon_str in people_in_polygon) and noise_polygon.contains(point):
            people_in_polygon.append(tube_obj['people_count'])
        else:
            if not isinstance(noise_polygon, MultiPolygon):
                distance_to_station = noise_polygon.exterior.distance(point)
                people_in_polygon.append(tube_obj['people_count']/(50*distance_to_station))
            else:
                distance_to_station = min([noise_multipolygon.exterior.distance(point) for noise_multipolygon in noise_polygon])
                people_in_polygon.append(tube_obj['people_count']/(50*distance_to_station))
    # if len(people_in_polygon) == 0:
        # if isinstance(noise_polygon, MultiPolygon):
        #     # feature['properties']['distance_to_tube'] = min([min([noise_multipolygon.exterior.distance(point) for point in tube_station_coordiates]) for noise_multipolygon in noise_polygon])
        #     feature['properties']['distance_to_tube'] = max([max([tube_obj['people_count']/noise_multipolygon.exterior.distance(Point(tube_obj['location'][0], tube_obj['location'][1])) for tube_obj in tube_station_data]) for noise_multipolygon in noise_polygon])
        # else:
        #     # feature['properties']['distance_to_tube'] = min([noise_polygon.exterior.distance(point) for point in tube_station_coordiates])
        #     feature['properties']['distance_to_tube'] = max([tube_obj['people_count']/noise_polygon.exterior.distance(Point(tube_obj['location'][0], tube_obj['location'][1])) for tube_obj in tube_station_data])
        # feature['properties']['distance_to_tube'] = 0¸
    # else:
    feature['properties']['people_count'] = sum(people_in_polygon) if len(people_in_polygon) != 0 else 0
    feature['properties']['noise'] = get_random_value(discrete_continuous_map[feature["properties"]["NoiseClass"]])

output = open('noise_data_with_tube_proximityo.geojson', 'w')
json.dump(noise_data, output)
