import csv
import json
reader = csv.reader(open(r"open_pubs_london.csv"),delimiter=',')

tube_coordinates = []

for row in list(reader):
    lat = row[6]
    lon = row[7]
    
    try:
        tube_coordinates.append((float(lat),float(lon)))
    except:
        print(f"{lat},{lon}")

output = open('london_pubs_data.json', 'w')
json.dump(tube_coordinates, output)