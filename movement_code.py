from threading import Thread
import brickpi3
import threading
import time
import math

# Initialize BrickPi3 instance
BP = brickpi3.BrickPi3()

RIGHT_WHEEL = BP.PORT_D #The motor connected to the port D
LEFT_WHEEL = BP.PORT_C #The motor connected to the port C
WHEEL_RADIUS = 2.1 #In cm
CIRCUMFERENCE = 2 * math.pi * WHEEL_RADIUS #2*pi*r

#Stop movement
def stop_all_movement():
    BP.set_motor_power(RIGHT_WHEEL, 0)
    BP.set_motor_power(LEFT_WHEEL, 0)
    print("Emergency stop triggered")

#Moving
def move(speed, duration, direction):
    if direction == "forward":
        BP.set_motor_dps(LEFT_WHEEL, -speed)
        BP.set_motor_dps(RIGHT_WHEEL, -speed)
    else:
        BP.set_motor_dps(LEFT_WHEEL, speed)
        BP.set_motor_dps(RIGHT_WHEEL, speed)
    time.sleep(duration)
    stop_all_movement()
    
#Turning
def turn(dps, duration, direction):
    if direction == "right":
        BP.set_motor_dps(RIGHT_WHEEL, -dps)
        BP.set_motor_dps(LEFT_WHEEL, -0.1*dps)
        time.sleep(duration)
    elif direction == "left":
        BP.set_motor_dps(RIGHT_WHEEL, -0.1*dps)
        BP.set_motor_dps(LEFT_WHEEL, -dps)
        time.sleep(duration)
    stop_all_movement()

#TEST TURNIN
# def turn_alternative(dps, direction):
#     if direction == "left":
#         BP.set_motor_dps(RIGHT_WHEEL, -dps)
#         BP.set_motor_dps(LEFT_WHEEL, dps)
#         time.sleep(1)
#     else:
#         BP.set_motor_dps(RIGHT_WHEEL, dps)
#         BP.set_motor_dps(LEFT_WHEEL, -dps)
#         time.sleep(1)
#     
#     stop_all_movement()
      
    
#THE PERFECT TRY
# move(260, 5, "forward")
# turn(264, "right")
# move(260, 5.9, "forward")
# turn(263, "left")
#     

stop_all_movement()
    
# turn_alternative(263, "right")
# #move(150,2)
# turn_alternative(263, "right")
# #move(150,2)
# turn_alternative(263, "right")
# 
# turn_alternative(263, "right")


#Test:
#stop_all_movement()

#turn(360, "left")
     
###
###Testing movement
###
#one full rotation
#move_forward(360, 1)
#
#two full rotations
#move_forward(720, 1)
#stop_all_movement()    
             
             
 
 
 
 
 
 
 
 
 
##This is for threading
# def sleepMe(x):
#     print(f"Thread {x} going to sleep for 2 seconds.")
#     time.sleep(2)
#     print(f"Thread {x} is active now.")
#     
# for x in range(10):
#     th = Thread(target=sleepMe, args=(x, ))
#     th.start()
#     print(f"Current Thread count: {threading.active_count()}")