import json

data = []

for traffic_data_num in ["region_6",78,80,83,123,128,135]:
    data.extend(json.load(open("traffic_data_" + str(traffic_data_num) + ".json"))['data'])

ouput = open("combined_traffic_data.json", "w")
json.dump({"data": data}, ouput)