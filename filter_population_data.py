import csv
import json
from json import JSONEncoder

london_post_code_prefixes = json.load(open("london_post_code_areas.json"))
reader = csv.reader(open(r"population_data_by_post_code_sectors.csv"),delimiter=',')

class PopulationByPostcode(object):
    def __init__(self, postcode, population):
        self.postcode = postcode
        self.population = population

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

postcodes = []
counter = 0
for row in reader:
    for prefix in london_post_code_prefixes:
        postcode = row[1]
        postcode_starts_with_london_prefix = postcode.startswith(prefix)
        char_after_prefix_is_not_number = postcode[len(prefix)].isdigit()
        if postcode_starts_with_london_prefix and char_after_prefix_is_not_number:
            counter += 1
            postcodes.append(PopulationByPostcode(postcode, float(row[-1])))
            break

print(counter)

output = open('london_population_data_by_post_code_sectors.json', 'w')
json.dump(MyEncoder().encode(postcodes), output)