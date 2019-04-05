# Performs logarithmic regression
# Input: Various independent variable arrays and noise pollution
# Output: Graph showing regression output

import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import json
import numpy as np
import math

noise_data = json.load(open("data/noise/noise_array_2012.json"))

data_lists = [
    json.load(open("data/lgvs_2012.json")),
    json.load(open("data/all_hgvs_2012.json")),
    json.load(open("data/cars_and_taxis_2012.json")),
    json.load(open("data/two_wheeled_motor_vehicles_2012.json")),
    json.load(open("data/buses_and_coaches_2012.json")),
    json.load(open("data/traffic/traffic_array_2012.json"))
]

for data_list in data_lists:
    slope, intercept, r_value, p_value, std_err = stats.linregress(data_list, noise_data)
    print("slope: %f    intercept: %f" % (slope, intercept))
    print("r-squared: %f" % r_value**2)
    print("p value: %f" % p_value)
    
    popt, pcov = curve_fit(lambda t,a,b: a+b*np.log10(t), data_list, noise_data, absolute_sigma=True)
    print(popt)
    curvex=np.linspace(min(data_list), max(data_list))
    p1 = popt[0]
    p2 = popt[1]
    curvey=(lambda x,c,m: m*np.log10(x)+c)(curvex,p1,p2)

    # plot data
    plt.plot(data_list,noise_data,'x',label = 'Xsaved')
    plt.plot(curvex,curvey,'r', linewidth=2, label = 'Model')

    plt.legend()
    plt.show()