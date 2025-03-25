#!/usr/bin/env python3
"""
    This file will allow for detecting the colors:
    - yellow --> tile
    - red --> fire
    - green --> furniture
    - None will be outputted if no match (should have same consequences as yellow)
    - **NOTE**: middle of color sensor light must touch the green sticker! Or else, detects yellow background :/
    - Specific values generated thru calculating 95% confidence interval
"""

from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor
from time import sleep

COLOR_SENSOR = EV3ColorSensor(1) #Testing Purposes  
Touch_Sensor = TouchSensor(2)

#Retrieves RGB Values when Touch Sensor pressed (touch sensor used for testing purposes)
def get_rgb_values():
    "Collect color sensor data."
    try:
        print("Touch Sensor is pressed... collecting rgb")
        rgb_values = COLOR_SENSOR.get_rgb()
        if rgb_values is not None:
            print(rgb_values)
            return rgb_values
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
        
def detect_color(r, g, b):    
    #Normalized RGB Values
    r_norm = r/(r+g+b)
    g_norm = g/(r+g+b)
    b_norm = b/(r+g+b)
    
    #Red: Extinguish Fire
    if r >= 1.7*g and r >= 4*b:
     return "red"

    #Yellow (just like None)
    elif ((0.3 <= r_norm <= 0.7) and (0.26 <= g_norm <= 0.53) and (0.01 <= b_norm <= 0.11)):
        #if overlap with green normalized range
        if ((0.25 <= r_norm <= 0.65) and (0.31 <= g_norm <= 0.66) and (0.03 <= b_norm <= 0.11)):
            #green if green value superior
            if(r_norm <= g_norm):
                return "green"
            #or else, yellow
            else:
                return "yellow"
        else:
            return "yellow"
        
    #Green: Move away
    elif ((0.25 <= r_norm <= 0.65) and (0.31 <= g_norm <= 0.66) and (0.03 <= b_norm <= 0.11)):
        return "green"
    
    # If no match, None
    else:
        return None

    
if __name__ == "__main__":
    while True:
        if Touch_Sensor.is_pressed():
            r, g, b = get_rgb_values()
            print(detect_color(r, g, b))
        sleep(0.2)
    