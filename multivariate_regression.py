# Script to perform multivariate regression
# Input: Traffic points enriched with all the parameters to be considered
# Output: results of multivariate regression
# Based on example provided by data to fish: https://datatofish.com/multiple-linear-regression-python/

from pandas import DataFrame
from sklearn import linear_model
from sklearn.metrics import r2_score
import statsmodels.api as sm
import time
import json
import matplotlib.pyplot as plt
import math
from sys import argv
from scipy import stats
import numpy as np
import constants

script, opt = argv

type_of_noise = opt
pollution = constants.getPollutionObject(type_of_noise)

outlier_keys = pollution.outlier_keys
useful_keys = pollution.useful_keys
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

traffic_data = json.load(open(pollution.filepath))

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
df = DataFrame(traffic_dict ,columns=useful_keys)
# df = DataFrame(traffic_dict ,columns=useful_keys)
useful_keys.remove(pollution.type_of_pollution)
X = df[useful_keys]
Y = df[pollution.type_of_pollution]

# Perform regression
regr = linear_model.LinearRegression()
regr.fit(X, Y)

# Record outputs
print('Intercept: \n', regr.intercept_)
coefs = regr.coef_
print('Coefficients: \n', coefs)

X = sm.add_constant(X) # adding a constant
 
model = sm.OLS(Y, X).fit()

print_model = model.summary()
print(print_model)