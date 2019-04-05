# Script to write noise and traffic data to arrays for linear regression
# Input: unionized traffic and noise data
# Output: arrays written to memroy

import json
import math

traffic_data = json.load(open("data/traffic/filtered_traffic_data_with_noise_class_discrete.json"))

noise = []
traffic = []
lgvs = []
all_hgvs = []
cars_and_taxis = []
two_wheeled_motor_vehicles = []
buses_and_coaches = []

def transform_to_logged_val(input_val):
    return input_val

for feature in traffic_data["features"]:
    noise.append(feature["noise_class"])
    lgvs.append(transform_to_logged_val(feature["properties"]["lgvs"]))
    all_hgvs.append(transform_to_logged_val(feature["properties"]["all_hgvs"]))
    cars_and_taxis.append(transform_to_logged_val(feature["properties"]["cars_and_taxis"]))
    two_wheeled_motor_vehicles.append(transform_to_logged_val(feature["properties"]["two_wheeled_motor_vehicles"]))
    buses_and_coaches.append(transform_to_logged_val(feature["properties"]["buses_and_coaches"]))
    traffic.append(transform_to_logged_val(feature["properties"]["all_motor_vehicles"]))

output = open('data/noise/noise_array_2012.json', 'w')
print(len(noise))
json.dump(noise, output)

output = open('data/traffic/traffic_array_2012.json', 'w')
print(len(traffic))
json.dump(traffic, output)

output = open('data/traffic/lgvs_2012.json', 'w')
print(len(lgvs))
json.dump(lgvs, output)

output = open('data/traffic/all_hgvs_2012.json', 'w')
print(len(all_hgvs))
json.dump(all_hgvs, output)

output = open('data/traffic/cars_and_taxis_2012.json', 'w')
print(len(cars_and_taxis))
json.dump(cars_and_taxis, output)

output = open('data/traffic/two_wheeled_motor_vehicles_2012.json', 'w')
print(len(two_wheeled_motor_vehicles))
json.dump(two_wheeled_motor_vehicles, output)

output = open('data/traffic/buses_and_coaches_2012.json', 'w')
print(len(buses_and_coaches))
json.dump(buses_and_coaches, output)