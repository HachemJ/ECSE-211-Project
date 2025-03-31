#!/usr/bin/env python3
"""
    This file will allow for detecting the colors:
    - yellow --> tile
    - red --> fire
    - green --> furniture
    - None will be outputted if no match (should have same consequences as yellow)
    - **NOTE**: middle of color sensor light must touch the green sticker! Or else, detects yellow background :/
    - Specific values generated thru calculating 95% confidence interval
    
    This file will allow also for color sensor arm control.
"""

from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, Motor
from time import sleep

import brickpi3
import threading

BP = brickpi3.BrickPi3()
ARM_MOTOR = Motor("D")

#This is for dropping the cube
EXTINGUISHER_MOTOR = Motor("A")

#TESTING NAVIGATION IN THE SAME CODE TYPE SHIT
RIGHT_MOTOR = Motor("B") #RIGHT_WHEEL
LEFT_MOTOR = Motor("C") #LEFT_WHEEL


COLOR_SENSOR = EV3ColorSensor(1) #Testing Purposes  
Touch_Sensor = TouchSensor(2)

def stop():
    RIGHT_MOTOR.set_power(0)
    LEFT_MOTOR.set_power(0)

#Retrieves RGB Values when Touch Sensor pressed (touch sensor used for testing purposes)
def get_rgb_values():
    "Collect color sensor data."
    try:
        #print("Touch Sensor is pressed... collecting rgb")
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

#DROPPING THE CUBE
def drop_cube():
  
    EXTINGUISHER_MOTOR.set_dps(-600)
    sleep(0.3)
        
    EXTINGUISHER_MOTOR.set_dps(240)
    sleep(1)
        
    EXTINGUISHER_MOTOR.set_power(0)
    print("I ran")
 
#reset_arm_position
def reset_arm_position(quarter, increment):
    if quarter == "1st":
        ARM_MOTOR.set_dps(-80)
        sleep(0.2*increment)
    elif quarter == "2nd":
        ARM_MOTOR.set_dps(-80)
        sleep(0.2*(6-increment))
    elif quarter == "3rd":
        ARM_MOTOR.set_dps(80)
        sleep(0.2*increment)
    else:
        ARM_MOTOR.set_dps(80)
        sleep(0.2*(6-increment))

#Turning : forward
def turn(dps, duration, direction):
    if direction == "right":
        RIGHT_MOTOR.set_dps(-dps)
        LEFT_MOTOR.set_dps(-0.1*dps)
        sleep(duration)
    elif direction == "left":
        RIGHT_MOTOR.set_dps(-0.1*dps)
        LEFT_MOTOR.set_dps(-dps)
        sleep(duration)
        
#Turning : backwards
def turn_reverse(dps, duration, direction, i):
    if direction == "right":
        RIGHT_MOTOR.set_dps(dps)
        LEFT_MOTOR.set_dps(0.1*dps)
        sleep(duration)
        move_backwards(150/(7 - i), 1)
    elif direction == "left":
        RIGHT_MOTOR.set_dps(0.1*dps)
        LEFT_MOTOR.set_dps(dps)
        sleep(duration)
        move_backwards(150/i, 1)
        
        
def turn_based_on_quarter_and_increment(quarter, i):
    if quarter == "1st":
        turn(24*i, 1, "left")
        move(150/i, 1)
    elif quarter == "2nd":
        turn(24*i, 1, "left")
        move(150/(7 - i), 1) #worried about division by zero
    elif quarter == "3rd":
        turn(24*i, 1, "right")
        move(150/i, 1)
    else:
        turn(24*i, 1, "right")
        move(150/(7 - i), 1)
            
    
def turn_reverse_based_on_quarter_and_increment(quarter, i):
    if quarter == "1st":
        turn_reverse(24*i, 1, "left", i)
        move(150/i, 1)
    elif quarter == "2nd":
        turn_reverse(24*i, 1, "left", i)
        move(150/(7 - i), 1) #worried about division by zero
    elif quarter == "3rd":
        turn_reverse(24*i, 1, "right", i)
        move(150/i, 1)
    else:
        turn_reverse(24*i, 1, "right", i)
        move(150/(7 - i), 1)
        

        
def move(speed, duration):
    
    LEFT_MOTOR.set_dps(-speed)
    RIGHT_MOTOR.set_dps(-speed)
    sleep(duration)
    
    LEFT_MOTOR.set_power(0)
    RIGHT_MOTOR.set_power(0)
    
def move_backwards(speed, duration):
    
    LEFT_MOTOR.set_dps(speed)
    RIGHT_MOTOR.set_dps(speed)
    sleep(duration)
    
    LEFT_MOTOR.set_power(0)
    RIGHT_MOTOR.set_power(0)
        
def move_robot_based_on_quarter_and_increment(quarter, increment):
    if quarter == "2nd" or quarter == "4th":
        increment = 6 - increment
        
    if quarter == "1st" or quarter == "2nd":
        direction = "left"
    else:
        direction = "right"
        
    angle = 16*increment
    turn_based_on_quarter_and_increment(quarter, increment) #6th increment
    
    stop()
    
    drop_cube()
    
    turn_reverse_based_on_quarter_and_increment(quarter, increment) #6th increment
    #turn_reverse(145, 1, direction)
    stop()
    #turn(23, 1, direction) #1st increment
    #move(150, 1)
    
    #drop_cube()
    
    reset_arm_position(quarter, increment)
    
    ARM_MOTOR.set_power(0)
    
def move_arm(found_sticker):
    while found_sticker:
        for i in range(1, 7):
            ARM_MOTOR.set_dps(80)
            sleep(0.2)
            rgb = get_rgb_values()
            color_detected = detect_color(rgb[0],rgb[1],rgb[2])
            if color_detected == "red":
                print("1st quarter " + str(i))
                ARM_MOTOR.set_power(0)
                found_sticker = False
                move_robot_based_on_quarter_and_increment("1st", i)
                return
            print(color_detected)
        for i in range(1, 7):
            ARM_MOTOR.set_dps(-80)
            sleep(0.2)
            rgb = get_rgb_values()
            color_detected = detect_color(rgb[0],rgb[1],rgb[2])
            if color_detected == "red":
                print("2nd quarter " + str(i))
                ARM_MOTOR.set_power(0)
                found_sticker = False
                move_robot_based_on_quarter_and_increment("2nd", i)
                return
            print(color_detected)
            
        for i in range(1, 7):
            ARM_MOTOR.set_dps(-80)
            sleep(0.2)
            rgb = get_rgb_values()
            color_detected = detect_color(rgb[0],rgb[1],rgb[2])
            if color_detected == "red":
                print("3rd quarter " + str(i))
                ARM_MOTOR.set_power(0)
                found_sticker = False
                move_robot_based_on_quarter_and_increment("3rd", i)
                return
            print(color_detected)
            
        for i in range(1, 7):
            ARM_MOTOR.set_dps(80)
            sleep(0.2)
            rgb = get_rgb_values()
            color_detected = detect_color(rgb[0],rgb[1],rgb[2])
            if color_detected == "red":
                print("4th quarter " + str(i))
                ARM_MOTOR.set_power(0)
                found_sticker = False
                move_robot_based_on_quarter_and_increment("4th", i)
                return
            print(color_detected)

#turn(145, 1, "left")
#stop()
#move_robot_based_on_quarter_and_increment("1st", 6)
    
#The two functions we called for testing
move_arm(True)
#sleep(2)
#move_arm(True)
#move(260,3)





#stop()
#ARM_MOTOR.set_power(0)
    
#drop_cube()

    

#we just need to worry about 1st and 3rd quarters logic

#if __name__ == "__main__":
    #move_arm()
#     while True:
#         if Touch_Sensor.is_pressed():
#             r, g, b = get_rgb_values()
#             print(detect_color(r, g, b))
#         sleep(0.2)
    