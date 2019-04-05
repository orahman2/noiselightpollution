# Script to convert json file to geojson file
# Input: json file
# Output: geojson file

from geojson import Point, Feature, FeatureCollection, dump
from sys import argv
import json

script, filename = argv

data_file = json.load(open(filename))

# For each feature, extracts longitude/latitude and adds data as properties
features = []
for data in data_file['data']:
   longitude = float(data['longitude'])
   latitude = float(data['latitude'])
   point = Point((longitude, latitude))
   features.append(Feature(geometry=point, properties=data))

feature_collection = FeatureCollection(features)
new_filename = filename.split(".")[0] + '.geojson'
with open(new_filename, 'w') as f:
   dump(feature_collection, f)