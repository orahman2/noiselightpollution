import json
import random

traffic_data = json.load(open("traffic_data_enriched.json"))

print(len(traffic_data["features"]))

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
        "noise_class": get_random_value(discrete_continuous_map[obj["noise_class"]])
     } for obj in traffic_data["features"]]
}

# print(geojson['features'])

output = open('filtered_traffic_data_with_noise_class_discrete.json', 'w')
json.dump(geojson, output)
