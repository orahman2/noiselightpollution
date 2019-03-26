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
population = []

counter = 0

def transform_to_logged_val(input_val):
    return math.log10(input_val) if input_val is not 0 else input_val
    # return input_val

for feature in traffic_data["features"]:
    noise.append(feature["properties"]["noise"])
    population.append(feature["properties"][field_name])

slope, intercept, r_value, p_value, std_err = stats.linregress(population, noise)
print("slope: %f    intercept: %f" % (slope, intercept))
print("r-squared: %f" % r_value**2)

plt.plot(np.array(population, dtype=np.float64), np.array(noise, dtype=np.float64), 'o', label='original data')
plt.plot(np.array(population, dtype=np.float64), intercept + slope*np.array(population, dtype=np.float64), 'r', label='fitted line')
plt.xlabel(field_name, fontsize=18)
plt.ylabel('Noise (dB)', fontsize=16)
plt.legend()
plt.show()