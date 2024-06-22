from servo_serial import *
duty = 0.5
port = "/dev/ttyUSB0"
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
import numpy as np
pos = 0

with TMotorManager_servo_serial(port='/dev/ttyUSB0', baud=961200, motor_params={'Curr_max': 15.0, 'Curr_min': -15.0, 'GEAR_RATIO': 9, 'Kt': 0.115, 'NUM_POLE_PAIRS': 21, 'P_max': 58.85, 'P_min': -58.85, 'Temp_max': 40.0, 'Type': 'AK80-9', 'V_max': 20.0, 'V_min': -20.0}, max_mosfett_temp=50) as dev:
        loop = SoftRealtimeLoop(dt=0.005, report=True, fade=0.0)
        dev.set_zero_position()
        dev.update()
        dev.enter_position_control()
        for t in loop:
            pos = 2*np.sin(t)
            dev.set_output_angle_radians(pos)
            dev.update()
            print(f"\r {dev}", end='')

        
