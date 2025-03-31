#!/usr/bin/env python3

"""
This test is used to collect data from the ultrasonic sensor.
Press touch sensor once to collect data and another time to stop it.
It must be run on the robot.
"""

from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from time import sleep


US_SENSOR_DATA_FILE = "/home/pi/ecse211/ECSE-211-Project/US_DATA_3x2_TRIAL1"

print("Program start.\nWaiting for sensors to turn on...")

TOUCH_SENSOR = TouchSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)


wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")


def collect_continuous_us_data():
    "Collect continuous data from the ultrasonic sensor between two button presses."
    output_file = open(US_SENSOR_DATA_FILE, "w")
    
    while True: #infinite loop
        is_pressed = False #initially touch sensor not pressed
        
        if TOUCH_SENSOR.is_pressed(): #when pressed first time, capture data
            print("Touch sensor is pressed")
            is_pressed = True
            sleep(1) #delay needed
            
        while is_pressed:
            us_data = US_SENSOR.get_value()
            print(us_data)
            if us_data is not None:
                output_file.write(f"{us_data}\n")
            if TOUCH_SENSOR.is_pressed(): #when pressed second time, stop program
                print("Done collecting")
                return
            
if __name__ == "__main__":
    collect_continuous_us_data()

