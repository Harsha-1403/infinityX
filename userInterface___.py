
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from TMotorCANControl.servo_serial import *
from tkinter import *

duty = 0.5
port = "/dev/ttyUSB0"

with TMotorManager_servo_serial(port = port, baud=961200, motor_params={'Curr_max': 15.0, 'Curr_min': -15.0, 'GEAR_RATIO': 9, 'Kt': 0.115, 'NUM_POLE_PAIRS': 21, 'P_max': 58.85, 'P_min': -58.85, 'Temp_max': 40.0, 'Type': 'AK80-9', 'V_max': 20.0, 'V_min': -20.0}, max_mosfett_temp=50)
deviceInfo.__enter__()


total_time = 20  # Total time for the triangle wave (in seconds)
max_rpm = -580*21   # Maximum RPM for the motor + is for putting into bp - is for pulling out
# for putting in it takes 21s and pulling out takes 21.5-22s with speed at 580*21
acceleration_time = total_time/3   # Time for acceleration (in seconds)
max_rpm_time = 2*acceleration_time
deceleration_time = total_time - max_rpm_time  # Time for deceleration (in seconds)

acceleration_rate = max_rpm / acceleration_time
deceleration_rate = max_rpm / deceleration_time

deviceInfo.enter_velocity_control()                                                                            
start_time = time.time()

while True:
    current_time = time.time() - start_time

    if current_time < acceleration_time:
        # Acceleration phase
        motor_speed = acceleration_rate * current_time
        deviceInfo.comm_set_speed_ERPM(float(motor_speed))
        deviceInfo.update()
    elif current_time > acceleration_time and current_time < max_rpm_time:
        # full speed phase
        motor_speed = max_rpm
        deviceInfo.comm_set_speed_ERPM(float(motor_speed))
        deviceInfo.update()
    elif current_time < total_time and current_time > max_rpm_time :
        # Deceleration phase
        motor_speed = max_rpm - deceleration_rate * (current_time - max_rpm_time)
        deviceInfo.comm_set_speed_ERPM(float(motor_speed))
        deviceInfo.update()
    else:
        # End of the triangle wave
        motor_speed = 0
        deviceInfo.comm_set_speed_ERPM(float(motor_speed))
        deviceInfo.update()
        break

    deviceInfo.update()

    # Read and display d-axis current
    current_daxis = deviceInfo.get_current_bus_amps()
    print("I/P Current (Amps):", current_daxis)


    time.sleep(0.1) 
