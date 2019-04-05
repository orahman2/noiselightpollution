# Performs logarithmic regression
# Input: The json file in question
# Output: Graph showing regression output

import json
import math
import matplotlib.pyplot as plt
from scipy import stats
import json
import numpy as np
from sys import argv

script, file_name, field_name = argv
traffic_data = json.load(open(file_name))

noise = []
parameter_list = []

# Convert to logarithmic input
def transform_to_logged_val(input_val):
    return math.log10(input_val) if input_val is not 0 else input_val

# Convert input to 1 dimensional list
for feature in traffic_data["features"]:
    noise.append(feature["properties"]["noise"])
    parameter_list.append(feature["properties"][field_name])

# Print result and plot graph
slope, intercept, r_value, p_value, std_err = stats.linregress(parameter_list, noise)
print("slope: %f    intercept: %f" % (slope, intercept))
print("r-squared: %f" % r_value**2)

plt.plot(np.array(parameter_list, dtype=np.float64), np.array(noise, dtype=np.float64), 'o', label='original data')
plt.plot(np.array(parameter_list, dtype=np.float64), intercept + slope*np.array(parameter_list, dtype=np.float64), 'r', label='fitted line')
plt.xlabel(field_name, fontsize=18)
plt.ylabel('Noise (dB)', fontsize=16)
plt.legend()
plt.show()