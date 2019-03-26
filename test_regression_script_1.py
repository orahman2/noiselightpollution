import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import json
import numpy as np
import math

noise_data = json.load(open("noise_array_2012.json"))

data_lists = [
    json.load(open("lgvs_2012.json")),
    json.load(open("all_hgvs_2012.json")),
    json.load(open("cars_and_taxis_2012.json")),
    json.load(open("two_wheeled_motor_vehicles_2012.json")),
    json.load(open("buses_and_coaches_2012.json")),
    json.load(open("traffic_array_2012.json"))
]

# for index in range(0,data_lists):


for data_list in data_lists:
    # data_list = np.polyfit(np.sqrt(data_list), noise_data, 1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(data_list, noise_data)
    print("slope: %f    intercept: %f" % (slope, intercept))
    print("r-squared: %f" % r_value**2)
    print("p value: %f" % p_value)
    # try:
    #   print(np.polyfit(np.log(data_list), noise_data, 1))
    # except:
    #   print("NUMPY NO WORK")
    
    popt, pcov = curve_fit(lambda t,a,b: a+b*np.log10(t), data_list, noise_data, absolute_sigma=True)
    print(popt)
    # print(pcov)
    curvex=np.linspace(min(data_list), max(data_list))
    p1 = popt[0]
    p2 = popt[1]
    curvey=(lambda x,c,m: m*np.log10(x)+c)(curvex,p1,p2)

    # plot data
    plt.plot(data_list,noise_data,'x',label = 'Xsaved')
    plt.plot(curvex,curvey,'r', linewidth=2, label = 'Model')

    # ********** LINE OF BEST FIT **********
    # plt.plot(np.unique(data_list), np.poly1d(np.polyfit(data_list, noise_data, 1))(np.unique(data_list)), label = "model")

    # plt.show()
    # plt.plot(np.array(data_list, dtype=np.float64), np.array(noise_data, dtype=np.float64), 'o', label='original data')
    # plt.plot(np.array(data_list, dtype=np.float64), intercept + slope*np.array(data_list, dtype=np.float64), 'r', label='fitted line')
    # plt.xlabel('Log(Daily Average Traffic)', fontsize=18)
    # plt.ylabel('Noise (dB)', fontsize=16)
    plt.legend()
    plt.show()

    print()
    print()
    print()