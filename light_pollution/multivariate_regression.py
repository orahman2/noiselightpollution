# Script to perform multivariate regression
# Input: Traffic points enriched with all the parameters to be considered
# Output: results of multivariate regression

from pandas import DataFrame
from sklearn import linear_model
import statsmodels.api as sm
import time
import json
import matplotlib.pyplot as plt
import math
from sys import argv
from scipy import stats
import numpy as np

outlier_keys = [
    'buses_and_coaches',
    'cars_and_taxis',
    'distance_to_closest_tube_station',
    'people_at_closest_tube_station',
    'two_wheeled_motor_vehicles'
]

useful_keys = [
    "pedal_cycles",
    "two_wheeled_motor_vehicles",
    "cars_and_taxis",
    "buses_and_coaches",
    "lgvs",
    "population",
    "distance_to_closest_tube_station",
    "people_at_closest_tube_station",
    "distance_to_closest_airport",
    "distance_to_london",
    'light_pollution'
]

traffic_dict = {}
keys_to_remove = set()

# Remove outliers from dataset
def find_outliers(dictionary):
    keys_to_remove = set()

    # Use the interquartile method modified using 5*range
    for key in outlier_keys:
        array_to_clean = dictionary[key]
        q1, q3 = np.percentile(sorted(array_to_clean),[25,75])

        iqr = q3 - q1   
        lower_bound = q1 -(5 * iqr)
        upper_bound = q3 +(5 * iqr)
        
        keys_to_remove.update([
            x for x in range(0,len(array_to_clean)) if
            lower_bound > array_to_clean[x] or
            array_to_clean[x] > upper_bound
        ])
    return keys_to_remove

# script, opt = argv

traffic_data = json.load(open('data/traffic/full_traffic_data.geojson'))

# Remove keys from all traffic data
def remove_keys(set_of_keys):
    keys_to_remove = list(set_of_keys)
    keys_to_remove.sort()
    keys_to_remove.reverse()

    for key_to_remove in keys_to_remove:
        del traffic_data['features'][key_to_remove]
        for key in traffic_dict.keys():
            del traffic_dict[key][key_to_remove]

# Iterate through each key and separate each property out into arrays
for useful_key in useful_keys:
    array_for_useful_key = []
    
    for traffic_point_index in range(0, len(traffic_data['features'])):
        traffic_point = traffic_data['features'][traffic_point_index]

        # Try and access the property
        # If property doesn't exist, flag that index as to be removed
        try:
            array_for_useful_key.append(traffic_point['properties'][useful_key])
        except Exception as e:
            keys_to_remove.add(traffic_point_index)
            array_for_useful_key.append(0)
    traffic_dict[useful_key] = array_for_useful_key

remove_keys(keys_to_remove)
remove_keys(find_outliers(traffic_dict))

# Specify axes
df = DataFrame(traffic_dict, columns=useful_keys)
useful_keys.remove('light_pollution')
X = df[useful_keys]
Y = df['light_pollution']

# Perform regression with sklearn
regr = linear_model.LinearRegression()
regr.fit(X, Y)

print('Intercept: \n', regr.intercept_)
coefs = regr.coef_
print('Coefficients: \n', coefs)

# with statsmodels
X = sm.add_constant(X)  # adding a constant

model = sm.OLS(Y, X).fit()
# predictions = model.predict(X)

print_model = model.summary()
print(print_model)
