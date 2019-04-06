# Performs linear regression
# Input: Various independent variable arrays and noise pollution
# Output: Graph showing regression output

import matplotlib.pyplot as plt
from scipy import stats
import json
import numpy as np

noise_data = json.load(open("data/noise/noise_array_2012.json"))

data_lists = [
    json.load(open("data/traffic/lgvs_2012.json")),
    json.load(open("data/traffic/all_hgvs_2012.json")),
    json.load(open("data/traffic/cars_and_taxis_2012.json")),
    json.load(open("data/traffic/two_wheeled_motor_vehicles_2012.json")),
    json.load(open("data/traffic/buses_and_coaches_2012.json")),
    json.load(open("data/traffic/traffic_array_2012.json"))
]

for data_list in data_lists:
    slope, intercept, r_value, p_value, std_err = stats.linregress(data_list, noise_data)
    print("slope: %f    intercept: %f" % (slope, intercept))
    print("r-squared: %f" % r_value**2)
    print(f"standard error: {std_err}")

    plt.plot(np.array(data_list, dtype=np.float64), np.array(noise_data, dtype=np.float64), 'o', label='original data')
    plt.plot(np.array(data_list, dtype=np.float64), intercept + slope*np.array(data_list, dtype=np.float64), 'r', label='fitted line')
    plt.xlabel('Daily Average Traffic', fontsize=18)
    plt.ylabel('Noise (dB)', fontsize=16)
    plt.legend()
    plt.show()