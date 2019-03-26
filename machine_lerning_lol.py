# Import function to create training and test set splits
from sklearn.model_selection import train_test_split
# Import function to automatically create polynomial features! 
from sklearn.preprocessing import PolynomialFeatures
# Import Linear Regression and a regularized regression function
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
# Finally, import function to make a machine learning pipeline
from sklearn.pipeline import make_pipeline

from pandas import DataFrame
from sklearn import linear_model
import statsmodels.api as sm
import time
import json
import matplotlib.pyplot as plt
import math
import numpy as np

useful_keys = ['cars_and_taxis','buses_and_coaches', 'lgvs', 'hgvs_6_articulated_axle', 'all_hgvs', 'all_motor_vehicles', 'population', 'distance_to_closest_tube_station', 'people_at_closest_tube_station', 'distance_to_closest_airport','noise']
traffic_data = json.load(open('traffic_data_with_noise_and_population_and_proximity.geojson'))

traffic_dict = {}
keys_to_remove = set()

for useful_key in useful_keys:
    array_for_useful_key = []
    for traffic_point_index in range(0, len(traffic_data['features'])):
        traffic_point = traffic_data['features'][traffic_point_index]
        try:
            array_for_useful_key.append(traffic_point['properties'][useful_key])
        except:
            keys_to_remove.add(traffic_point_index)
            array_for_useful_key.append(0)
    traffic_dict[useful_key] = array_for_useful_key

keys_to_remove = list(keys_to_remove)
keys_to_remove.sort()
keys_to_remove.reverse()

for key_to_remove in keys_to_remove:
    del traffic_data['features'][key_to_remove]
    for key in traffic_dict.keys():
        del traffic_dict[key][key_to_remove]

useful_keys.remove('noise')

for useful_key in useful_keys:
    array_for_useful_key = []
    for traffic_point in traffic_data['features']:
        try:
            array_for_useful_key.append(math.log(traffic_point['properties'][useful_key]))
        except:
            array_for_useful_key.append(0)
    traffic_dict[useful_key+'_log'] = array_for_useful_key

for useful_key in useful_keys:
    array_for_useful_key = []
    for traffic_point in traffic_data['features']:
        array_for_useful_key.append(math.sqrt(traffic_point['properties'][useful_key]))
    traffic_dict[useful_key+'_sqrt'] = array_for_useful_key

# temp_array = []
# for x in useful_keys:

# useful_keys.extend([useful_key+'_log' for useful_key in useful_keys])
# useful_keys.extend([useful_key+'_sqrt' for useful_key in useful_keys])
useful_keys.append('noise')

df = DataFrame(traffic_dict,columns=useful_keys)

# Alpha (regularization strength) of LASSO regression
lasso_eps = 0.0001
lasso_nalpha=20
lasso_iter=5000
# Min and max degree of polynomials features to consider
degree_min = 2
degree_max = 8
# Test/train split
X_train, X_test, y_train, y_test = train_test_split(df['noise'], df['cars_and_taxis'],test_size=0.33)
# Make a pipeline model with polynomial transformation and LASSO regression with cross-validation, run it for increasing degree of polynomial (complexity of the model)
for degree in range(degree_min,degree_max+1):
    model = make_pipeline(PolynomialFeatures(degree, interaction_only=False), LassoCV(eps=lasso_eps,n_alphas=lasso_nalpha,max_iter=lasso_iter, normalize=True,cv=5))
    model.fit(X_train,y_train)
    test_pred = np.array(model.predict(X_test))
    RMSE=np.sqrt(np.sum(np.square(test_pred-y_test)))
    test_score = model.score(X_test,y_test)