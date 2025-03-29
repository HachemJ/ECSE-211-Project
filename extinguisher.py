import brickpi3
import time
from utils.brick import Motor

EXTINGUISHER_MOTOR = Motor("B")

def drop_cube():
  
    for i in range(2):
        EXTINGUISHER_MOTOR.set_dps(-600)
        time.sleep(0.25)
        
        EXTINGUISHER_MOTOR.set_dps(150)
        time.sleep(1)
        
    EXTINGUISHER_MOTOR.set_power(0)
    print("I ran")

def stop():
    EXTINGUISHER_MOTOR.set_power(0)
    
    
drop_cube()
#stop()