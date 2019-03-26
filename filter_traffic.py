import json
from sys import argv

script, year = argv

london_traffic = json.load(open("london_traffic.geojson"))
london_traffic['features'] = [x for x in london_traffic['features'] if x['properties']['year'] == int(year)]

json.dump(london_traffic, open(f"london_traffic_{year}.geojson", "w"))