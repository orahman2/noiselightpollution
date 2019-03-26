import csv
import json
from json import JSONEncoder

reader = csv.reader(open(r"London stations.csv"),delimiter=',')
analytics = json.load(open('london_tube_analytics.json'))

tube_coordinates = []
class TubeObj(object):
    def __init__(self, people_count, location):
        self.people_count = people_count
        self.location = location

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

counter = 0
tube_coordinates_list = list(reader)[1:]
for row in tube_coordinates_list:
    counter += 1
    station_name = row[0]
    if station_name in analytics:
        tube_coordinates.append(TubeObj(analytics[station_name], (float(row[3]),float(row[4]))))

print(len(tube_coordinates_list))
print(counter)

output = open('london_tube_coordinates.json', 'w')
json.dump(MyEncoder().encode(tube_coordinates), output)