# Script to set minimal noise for areas of london where data wasn't provided
# Input: Noise data
# Output: Non-null noise data

import json

traffic_data = json.load(open("data/traffic/traffic_data_with_noise_class.json"))

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
        "noise_class": obj["noise_class"] if obj["noise_class"] is not None else "<=54.9"
     } for obj in traffic_data["features"]]
}

output = open('data/filtered_traffic_data_with_noise_class_nonull.json', 'w')
json.dump(geojson, output)
