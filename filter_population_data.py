# Script to extract London postcodes from population data
# Input: Population by post code, london post codes
# Output: london-only population by post codes

import csv
import json
from json import JSONEncoder

london_post_code_prefixes = json.load(open("data/london_post_code_areas.json"))
reader = csv.reader(open(r"data/population/population_data_by_post_code_sectors.csv"),delimiter=',')

# Population object
class PopulationByPostcode(object):
    def __init__(self, postcode, population):
        self.postcode = postcode
        self.population = population

# Class to make postcode list encodable 
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

postcodes = []

# Iterate through each row to check if post code starts with london prefix
for row in reader:
    for prefix in london_post_code_prefixes:
        postcode = row[1]
        postcode_starts_with_london_prefix = postcode.startswith(prefix)
        char_after_prefix_is_not_number = postcode[len(prefix)].isdigit()

        # If it does start with a London post code prefix, append to array
        if postcode_starts_with_london_prefix and char_after_prefix_is_not_number:
            postcodes.append(PopulationByPostcode(postcode, float(row[-1])))
            break

output = open('data/population/london_population_data_by_post_code_sectors.json', 'w')
json.dump(MyEncoder().encode(postcodes), output)