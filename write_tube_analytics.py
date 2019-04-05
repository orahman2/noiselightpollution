# Script to read tube data from csv and write as json file
# Input: tube analytics csv
# Output: tube analytics json

import csv
import json
reader = csv.reader(open(r"data/tube_analytics.csv"),delimiter=',')

tube_coordinates = {}
# Check if station is in london. if so, normalize text and process
for row in list(reader)[1:]:
    if row[3] == 'London':
        tube_coordinates[row[2]] = (float(row[15].strip().replace(',', '')))

output = open('data/london_tube_analytics.json', 'w')
json.dump(tube_coordinates, output)