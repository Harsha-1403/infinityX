from servo_serial import TMotorManager_servo_serial
from gpiozero import Button
import time
import numpy as np

# Define step size and initial position
step_size = 0.015  # Adjust step size as needed
pos = 0
s = Button(8)

motor_handle_params = {
    'Curr_max': 15.0, 
    'Curr_min': -15.0, 
    'GEAR_RATIO': 9, 
    'Kt': 0.115, 
    'NUM_POLE_PAIRS': 21,
    'P_max': 58.85, 
    'P_min': -58.85, 
    'Temp_max': 40.0, 
    'Type': 'HandleMotor', 
    'V_max': 20.0, 
    'V_min': -20.0
}

step_size = 0.015  # Adjust step size as needed
pos = 0
with TMotorManager_servo_serial(port='/dev/ttyUSB_HANDLE', baud=961200, motor_params=motor_handle_params, max_mosfett_temp=50) as dev:
    dev.set_zero_position()
    dev.update()
    dev.enter_position_control()

    # Main control loop
    start_time = time.time()  # Record start time
    while True:
        # Calculate current time
        current_time = time.time()
        
        # Increment position by step size
        pos += step_size
        print(pos)
        # Set position
        dev.set_output_angle_radians(pos)
        dev.update()
        time.sleep(0.5)
        # Check button press
        if s.is_pressed:
            continue  # Continue loop if button not pressed
        else:
            break  # Exit loop if button pressed
        
        # Print device information
        print(f"\r {dev}", end='')

        # Add a small delay to control the speed of movement
        # You might need to adjust the delay based on your motor's speed and step size
          # Example delay, adjust as needed
        
        # Check if the elapsed time has exceeded a certain threshold (e.g., 2 seconds)
        #if current_time - start_time >= 2:
            #break  # Exit loop after a certain duration

print("Loop ended.")
