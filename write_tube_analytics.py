import csv
import json
reader = csv.reader(open(r"tube_analytics.csv"),delimiter=',')

tube_coordinates = {}

for row in list(reader)[1:]:
    if row[3] == 'London':
        print('hi')
        tube_coordinates[row[2]] = (float(row[15].strip().replace(',', '')))

output = open('london_tube_analytics.json', 'w')
json.dump(tube_coordinates, output)