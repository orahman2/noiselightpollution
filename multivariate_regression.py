from pandas import DataFrame
from sklearn import linear_model
import statsmodels.api as sm
import time
import json
import matplotlib.pyplot as plt
import math
from sys import argv

script, opt = argv

type_of_noise = opt
if type_of_noise not in ['day', 'night', 'avg']:
    raise ValueError('invalid noise option')
type_of_noise = 'road_noise_' + type_of_noise

useful_keys = ['cars_and_taxis','two_wheeled_motor_vehicles','buses_and_coaches', 'lgvs',type_of_noise]
traffic_data = json.load(open('traffic_data_with_noise_and_population_and_proximity.geojson'))

traffic_dict = {}
keys_to_remove = set()

# useful_keys.remove('distance_to_closest_tube_station')
# useful_keys.remove('people_at_closest_tube_station')
array_for_useful_key = []
# for traffic_point_index in range(0, len(traffic_data['features'])):
#         traffic_point = traffic_data['features'][traffic_point_index]
#         try:
#             array_for_useful_key.append(traffic_point['properties']['people_at_closest_tube_station']/traffic_point['properties']['distance_to_closest_tube_station'])
#         except:
#             keys_to_remove.add(traffic_point_index)
#             array_for_useful_key.append(0)
# traffic_dict['tube_distance_and_popularity'] = array_for_useful_key

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

useful_keys.remove(type_of_noise)

# for useful_key in useful_keys:
#     array_for_useful_key = []
#     for traffic_point in traffic_data['features']:
#         try:
#             array_for_useful_key.append(math.log(traffic_point['properties'][useful_key]))
#         except:
#             array_for_useful_key.append(0)
#     traffic_dict[useful_key+'_log'] = array_for_useful_key

# for useful_key in useful_keys:
#     array_for_useful_key = []
#     for traffic_point in traffic_data['features']:
#         array_for_useful_key.append(math.sqrt(traffic_point['properties'][useful_key]))
#     traffic_dict[useful_key+'_sqrt'] = array_for_useful_key

# temp_array = []
# for x in useful_keys:

# useful_keys.extend([useful_key+'_log' for useful_key in useful_keys])
# useful_keys.extend([useful_key+'_sqrt' for useful_key in useful_keys])
useful_keys.append(type_of_noise)
# useful_keys.append('tube_distance_and_popularity')

df = DataFrame(traffic_dict,columns=useful_keys)
useful_keys.remove(type_of_noise)
# for useful_key in useful_keys:
#     try:
#         plt.scatter(df[useful_key], df[type_of_noise], color='red')
#         plt.title('type_of_noise Vs ' +useful_key, fontsize=14)
#         plt.xlabel(useful_key, fontsize=14)
#         plt.ylabel(type_of_noise, fontsize=14)
#         plt.grid(True)
#         plt.show()
#     except:
#         print(useful_key)
# summary = []
# with open('your_file.txt', 'w') as f:
#     for key in useful_keys:
#         print(key)
#         X = df[[key]]
#         Y = df[type_of_noise]
        
#         # with sklearn
#         regr = linear_model.LinearRegression()
#         regr.fit(X, Y)

#         print('Intercept: \n', regr.intercept_)
#         print('Coefficients: \n', regr.coef_)


#         # # prediction with sklearn
#         # New_Interest_Rate = 2.75
#         # New_Unemployment_Rate = 5.3
#         # print ('Predicted Stock Index Price: \n', regr.predict([[New_Interest_Rate ,New_Unemployment_Rate]]))


#         # with statsmodels
#         X = sm.add_constant(X) # adding a constant
        
#         model = sm.OLS(Y, X).fit()
#         # predictions = model.predict(X) 
        
#         print_model = model.summary()
#         f.write("%s\n%s\n\n" % (key,print_model))
#         print(print_model)

X = df[useful_keys]
Y = df[type_of_noise]
 
# with sklearn
regr = linear_model.LinearRegression()
regr.fit(X, Y)

print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)


# # prediction with sklearn
# New_Interest_Rate = 2.75
# New_Unemployment_Rate = 5.3
# print ('Predicted Stock Index Price: \n', regr.predict([[New_Interest_Rate ,New_Unemployment_Rate]]))


# with statsmodels
X = sm.add_constant(X) # adding a constant
 
model = sm.OLS(Y, X).fit()
# predictions = model.predict(X) 
 
print_model = model.summary()
print(print_model)