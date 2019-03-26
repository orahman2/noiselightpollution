#! usr/bin/env python

from sys import argv
from os.path import exists
import simplejson as json 

script, in_file, out_file = argv

data = json.load(open(in_file))

geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry" : {
            "type": "Point",
            "coordinates": [float(obj["geometry"]["coordinates"][0]), float(obj["geometry"]["coordinates"][1])],
            },
        "properties" : obj["properties"],
     } for obj in data["features"] if obj["properties"]["year"] == 2012]
}


output = open(out_file, 'w')
json.dump(geojson, output)

# print geojson