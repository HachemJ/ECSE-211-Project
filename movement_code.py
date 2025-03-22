from threading import Thread
import brickpi3
import threading
import time

# Initialize BrickPi3 instance
BP = brickpi3.BrickPi3()

LEFT_MOTOR = BP.PORT_C
RIGHT_MOTOR = BP.PORT_D

def move(power, duration):
    BP.set_motor_power(LEFT_MOTOR, -power)
    BP.set_motor_power(RIGHT_MOTOR, -power)
    time.sleep(2)
    stop_all_movement()
    
def turn(dps, direction):
    if direction == "left":
        BP.set_motor_dps(LEFT_MOTOR, -dps)
        BP.set_motor_dps(RIGHT_MOTOR, dps)
    else:
        BP.set_motor_dps(LEFT_MOTOR, dps)
        BP.set_motor_dps(RIGHT_MOTOR, -dps)
    time.sleep(10)
    stop_all_movement()
    
def stop_all_movement():
    BP.set_motor_power(LEFT_MOTOR, 0)
    BP.set_motor_power(RIGHT_MOTOR, 0)
    print("Emergency stop triggered")
     
#Testing movement
#move(50, 5)
             
#Testing turn left
turn(90, "left")
    
# def sleepMe(x):
#     print(f"Thread {x} going to sleep for 2 seconds.")
#     time.sleep(2)
#     print(f"Thread {x} is active now.")
#     
# for x in range(10):
#     th = Thread(target=sleepMe, args=(x, ))
#     th.start()
#     print(f"Current Thread count: {threading.active_count()}")