import json
from shapely.geometry import Point, shape, GeometryCollection
from shapely.geometry.polygon import Polygon
import random
import util
import time

noise_data = {
        'road_noise_avg': json.load(open("road_lden_london.geojson")),
        'road_noise_day': json.load(open("road_laeq_16h_latlong.geojson")),
        'road_noise_night': json.load(open("road_laeq_16h_latlong.geojson")),
        'rail_noise_avg': json.load(open("rail_lden_latlong.geojson")),
        'rail_noise_day': json.load(open("rail_laeq_16h_latlong.geojson")),
        'rail_noise_night': json.load(open("rail_laeq_16h_latlong.geojson"))
    }

progress_milestones = [5*x for x in range(0,21)]
    
traffic_data = json.load(open("traffic_data_with_population.geojson"))

def build_polygon_noise_list(noise_objects):
    features = noise_objects["features"]
    polygon_list = GeometryCollection([
        shape(feature["geometry"]).buffer(0)
        for feature
        in features
        ]).geoms

    polygon_noise_list = []

    for polygon_list_index in range(0, len(polygon_list)):
        temp_obj = [
            polygon_list[polygon_list_index],
            util.get_random_value(features[polygon_list_index]["properties"]["NoiseClass"])
            ]
        polygon_noise_list.append(temp_obj)

    return polygon_noise_list

noise_objects_dict = { x:build_polygon_noise_list(noise_data[x]) for x in noise_data.keys() }

total_iterations = len(traffic_data['features'])*sum([len(x) for x in noise_objects_dict.values()])
print(f"number of total iterations is {total_iterations}")

counter = 0
for traffic_obj in traffic_data['features']:
    traffic_point = Point(traffic_obj['geometry']['coordinates'])

    for noise_object_type in noise_objects_dict.keys():
        noise_object_list = noise_objects_dict[noise_object_type]
        
        for noise_list_index in range(0, len(noise_object_list)):

            counter+=1
            progress = 100*counter/total_iterations
            if round(progress) in progress_milestones:
                progress_milestones.remove(round(progress))
                print(f"iteration {counter} out of {total_iterations}. Current progress is {round(progress,2)}%")
            
            noise_list = noise_object_list[noise_list_index]
            noise_polygon = noise_list[0]

            if noise_polygon.contains(traffic_point):
                traffic_obj['properties'][noise_object_type] = noise_list[1]
                break

output = open('traffic_data_with_noise_and_population.geojson', 'w')
json.dump(traffic_data, output)