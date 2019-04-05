# Script to filter London traffic by year
# Input: Year query term, traffic dataset
# Output: london-only population by post codes

import json
from sys import argv

script, year = argv

london_traffic = json.load(open("data/traffic/london_traffic.geojson"))
london_traffic['features'] = [x for x in london_traffic['features'] if x['properties']['year'] == int(year)]

json.dump(london_traffic, open(f"data/traffic/london_traffic_{year}.geojson", "w"))