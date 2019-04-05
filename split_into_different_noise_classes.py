# Merges important traffic data with noise data for linear regression
# Input: noise-enriched traffic data and traffic data
# Output: traffic data with noise and all consdiered attributes extracted

import json

traffic_data = json.load(open("filtered_traffic_data_with_noise_class_nonull.json"))
original_traffic_data = json.load(open("traffic_data.json"))

for traffic_index in range(0, len(traffic_data["features"])):
    # Gather counts of various vehicles
    lgvs_count = original_traffic_data[traffic_index]["lgvs"]
    buses_and_coaches_count = original_traffic_data[traffic_index]["buses_and_coaches"]
    two_wheeled_motor_vehicles_count = original_traffic_data[traffic_index]["two_wheeled_motor_vehicles"]
    all_hgvs_count = original_traffic_data[traffic_index]["all_hgvs"]
    cars_and_taxis_count = original_traffic_data[traffic_index]["cars_and_taxis"]

    # Enrich traffic data with various counts
    traffic_data["features"][traffic_index]["lgvs"] = lgvs_count
    traffic_data["features"][traffic_index]["buses_and_coaches"] = buses_and_coaches_count
    traffic_data["features"][traffic_index]["two_wheeled_motor_vehicles"] = two_wheeled_motor_vehicles_count
    traffic_data["features"][traffic_index]["all_hgvs"] = all_hgvs_count
    traffic_data["features"][traffic_index]["cars_and_taxis"] = cars_and_taxis_count

output = open('traffic_data_enriched.json', 'w')
json.dump(traffic_data, output)
