#!/usr/bin/env python3

"""
This file is used to plot RGB data collected from the color sensor.
It should be run on your computer, not on the robot.

Before running this script for the first time, you must install the dependencies
as explained in the README.md file.
"""

from ast import literal_eval
from math import sqrt, e, pi
from statistics import mean, stdev

from matplotlib import pyplot as plt
import numpy as np

COLOR_SENSOR_DATA_FILE = r"data\colorSensor\Yellow(2cm).csv"

def gaussian(x, values):
    """Return a Gaussian distribution for the given values."""
    mean_all = mean(values)
    st_dev = stdev(values)
    
    # Prevent division by zero
    if st_dev == 0:
        return np.zeros_like(x)
    
    return (1 / (st_dev * sqrt(2 * pi))) * np.exp(-((x - mean_all) ** 2) / (2 * st_dev ** 2))

def confidence_range(mean, st_dev, n=2):  #95% confidence interval
    return (mean - n * st_dev, mean + n * st_dev)

red, green, blue = [], [], []
with open(COLOR_SENSOR_DATA_FILE, "r") as f:
    for line in f.readlines():
        r, g, b = literal_eval(line)  # Convert string to 3 floats
        
        ### UNIT-VECTOR METHOD ###
        # denominator = sqrt(r ** 2 + g ** 2 + b ** 2)
        
        ### RATIO METHOD ###
        denominator = r + g + b
        
        red.append(r / denominator)
        green.append(g / denominator)
        blue.append(b / denominator)

# Mean and standard deviation for each color
mean_r, st_dev_r = mean(red), stdev(red)
mean_g, st_dev_g = mean(green), stdev(green)
mean_b, st_dev_b = mean(blue), stdev(blue)

# 95% confidence interval
red_range = confidence_range(mean_r, st_dev_r, n=2)
green_range = confidence_range(mean_g, st_dev_g, n=2)
blue_range = confidence_range(mean_b, st_dev_b, n=2)

# Print stats
print(f"Red: Mean = {mean_r:.4f}, Std Dev = {st_dev_r:.4f}, Range (95%) = {red_range}")
print(f"Green: Mean = {mean_g:.4f}, Std Dev = {st_dev_g:.4f}, Range (95%) = {green_range}")
print(f"Blue: Mean = {mean_b:.4f}, Std Dev = {st_dev_b:.4f}, Range (95%) = {blue_range}")

# Plot Gaussian distributions
x_values = np.linspace(0, 1, 255)  # 255 evenly spaced values between 0 and 1
plt.plot(x_values, gaussian(x_values, red), color="r", label="Red")
plt.plot(x_values, gaussian(x_values, green), color="g", label="Green")
plt.plot(x_values, gaussian(x_values, blue), color="b", label="Blue")

plt.xlabel("Normalized intensity value")
plt.ylabel("Normalized intensity PDF by color")
plt.legend()
plt.show()