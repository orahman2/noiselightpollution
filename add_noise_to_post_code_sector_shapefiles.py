import json

london_post_code_sectors_geojson = json.load(open("london_sectors.geojson"))
london_post_code_sectors_population = json.load(open("london_population_data_by_post_code_sectors.json"))

postcode_population_map = {}

new_geojson = json.loads('{"type":"FeatureCollection", "features": []}')

# print(london_post_code_sectors_population[0]['postcode'])
# print(london_post_code_sectors_geojson['features'][0]['properties']['name'])

for obj in london_post_code_sectors_population:
    postcode = obj['postcode']
    population = obj['population']
    postcode_population_map[postcode] = population

missing_data_count = 0

for obj in london_post_code_sectors_geojson['features']:
    postcode = obj['properties']['name']
    if postcode_population_map.__contains__(postcode):
        obj['properties']['population'] = postcode_population_map[postcode]
        new_geojson['features'].append(obj)

output = open('lodon_post_code_sector_population.geojson', 'w')
json.dump(new_geojson, output)