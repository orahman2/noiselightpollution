# Script to consolidate all London-related traffic data
# Input: london-related data sets individually
# Output: combined data set

import json

data = []

for traffic_data_num in ["region_6","local_authority_78","local_authority_80","local_authority_83",'local_authority_123',"local_authority_128","local_authority_135"]:
    data.extend(json.load(open("data/traffic/traffic_data_" + str(traffic_data_num) + ".json"))['data'])

ouput = open("data/traffic/combined_traffic_data.json", "w")
json.dump({"data": data}, ouput)