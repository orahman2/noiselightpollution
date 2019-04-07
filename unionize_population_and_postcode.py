# Script to geoencode population data
# Input: London borough sector geoencoded files, population data
# Output: Geoencoded borough sector level data

import json
import util

london_post_code_sectors_geojson = json.load(open("data/london_sectors.geojson"))
london_post_code_sectors_population = json.load(open("data/population/london_population_data_by_post_code_sectors.json"))

postcode_population_map = {}
new_geojson = json.loads('{"type":"FeatureCollection", "features": []}')

for obj in london_post_code_sectors_population:
    postcode = obj['postcode']
    population = obj['population']
    postcode_population_map[postcode] = population

for obj in london_post_code_sectors_geojson['features']:
    postcode = obj['properties']['name']
    if postcode in postcode_population_map:
        obj['properties']['population'] = postcode_population_map[postcode]
        new_geojson['features'].append(obj)

output = open('data/population/london_post_code_sector_population.geojson', 'w')
json.dump(new_geojson, output)