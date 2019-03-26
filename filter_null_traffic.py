import json

traffic_data = json.load(open("traffic_data_with_noise_class.json"))

print(len(traffic_data["features"]))

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

print(len(geojson["features"]))

output = open('filtered_traffic_data_with_noise_class_nonull.json', 'w')
json.dump(geojson, output)
