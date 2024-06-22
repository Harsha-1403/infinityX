from gpiozero import Button, LED
from time import sleep
from servo_serial import *

# Define GPIO pins
lock_sensor_handle = Button(16)
lock_sensor_inflow = Button(26)
plate_open = LED(22)
plate_close = LED(23)
actuator_up = LED(17)
actuator_down = LED(27)
handle_unlock = LED(24)
red_led = LED(4)
green_led = LED(5)
blue_led = LED(6)

# Motor configurations
motor_handle_params = {'Curr_max': 15.0, 'Curr_min': -15.0, 'GEAR_RATIO': 9, 'Kt': 0.115, 'NUM_POLE_PAIRS': 21,
                       'P_max': 58.85, 'P_min': -58.85, 'Temp_max': 40.0, 'Type': 'HandleMotor', 'V_max': 20.0, 'V_min': -20.0}
motor_inflow_params = {'Curr_max': 15.0, 'Curr_min': -15.0, 'GEAR_RATIO': 9, 'Kt': 0.115, 'NUM_POLE_PAIRS': 21,
                       'P_max': 58.85, 'P_min': -58.85, 'Temp_max': 40.0, 'Type': 'InflowMotor', 'V_max': 20.0, 'V_min': -20.0}
motor_outflow_params = {'Curr_max': 15.0, 'Curr_min': -15.0, 'GEAR_RATIO': 9, 'Kt': 0.115, 'NUM_POLE_PAIRS': 21,
                        'P_max': 58.85, 'P_min': -58.85, 'Temp_max': 40.0, 'Type': 'OutflowMotor', 'V_max': 20.0, 'V_min': -20.0}

#function to get white led
def white():
	red_led.on()
	green_led.on()
	blue_led.on()
	
#function to get red led
def red():
	red_led.on()
	green_led.off()
	blue_led.off()

#function to get green led
def green():
	red_led.off()
	green_led.on()
	blue_led.off()

# Function to open the plates
def open_plates():
    plate_open.on()
    sleep(2.1)  # Adjust as needed
    plate_open.off()

# Function to open the plates
def open_plates():
    plate_open.on()
    sleep(2.1)  # Adjust as needed
    plate_open.off()

# Function to close the plates
def close_plates():
    plate_close.on()
    sleep(2.2)  # Adjust as needed
    plate_close.off()
    
# Function to unlock the handle
def unlock_handle():
    handle_unlock.on()
    sleep(0.3)
    handle_unlock.off()

# Function to handle the motor rotation with a timeout
def run_motor_with_timeout(motor, target_speed, timeout):
    motor.comm_set_speed_ERPM(float(target_speed))
    motor.update()
    motor_torque = motor.get_motor_torque_newton_meters()
    print("Motor Torque (Nm):", motor_torque)
    runcount = 0

    while runcount < timeout*5000:
        motor.comm_set_speed_ERPM(float(target_speed))
        motor.update()
        motor_torque = motor.get_motor_torque_newton_meters()
        print("Motor Torque (Nm):", motor_torque)
        runcount += 1

    motor.comm_set_speed_ERPM(0)
    motor.update()
    sleep(0.25)
    var = 0
    runcount = 0

# Function to control the actuator
def control_actuator(led, duration):
    led.on()
    sleep(duration)
    led.off()

# Function to stop the motor when torque is below the threshold
def stop_motor_on_low_torque(motor, target_speed, timeout, torque_threshold, delay=4.0):
    motor.comm_set_speed_ERPM(float(target_speed))
    motor.update()
    runcount=0
    count = 0
    var = 0

    while runcount < timeout*5000:
        motor.comm_set_speed_ERPM(float(target_speed))
        motor.update()
        motor_torque = motor.get_motor_torque_newton_meters()
        count += 1
        runcount += 1
        print("Motor Torque (Nm):", motor_torque)
        if count > 42750:
            target_speed = 2000
        if 42750 < count < 142750 and -1 < motor_torque < 1 and motor_torque != 0:
            var = 1
            break
        if var == 1:
            break

    motor.comm_set_speed_ERPM(0)
    motor.update()
    var = 0
    count = 0

# Initialize motors
with TMotorManager_servo_serial(port='/dev/ttyUSB_HANDLE', baud=961200, motor_params={'Curr_max': 15.0, 'Curr_min': -15.0, 'GEAR_RATIO': 9, 'Kt': 0.115, 'NUM_POLE_PAIRS': 21, 'P_max': 58.85, 'P_min': -58.85, 'Temp_max': 40.0, 'Type': 'AK80-9', 'V_max': 20.0, 'V_min': -20.0}) as motorh:
    with TMotorManager_servo_serial(port='/dev/ttyUSB_BOTTOM', baud=961200, motor_params=motor_inflow_params, max_mosfett_temp=50) as motor_inflow:
        with TMotorManager_servo_serial(port='/dev/ttyUSB_TOP', baud=961200, motor_params=motor_outflow_params, max_mosfett_temp=50) as motor_outflow:
            count=0
            sleep(0.30)
            while (True):
                white()
                if (count==0):
                    control_actuator(actuator_down, duration=2.3)

                    # Wait for both lock buttons to be pressed
                    print("Waiting for lock buttons to be pressed...")
                    while not (lock_sensor_handle.is_pressed and lock_sensor_inflow.is_pressed):
                        sleep(0.25)

                    print("Both lock buttons pressed. Opening plates...")
                    red()
                    open_plates()
                    sleep(0.75)

                    print("Running handle motor...")
                    sleep(0.25)
                    motorh.comm_set_speed_ERPM(float(-7500))
                    motorh.update()
                    motor_torque = motorh.get_motor_torque_newton_meters()
                    print("Motor Torque (Nm):", motor_torque)
                    runcount = 0

                    while runcount < 6*5000:
                        motorh.comm_set_speed_ERPM(float(-7500))
                        motorh.update()
                        motor_torque = motorh.get_motor_torque_newton_meters()
                        print("Motor Torque (Nm):", motor_torque)
                        runcount += 1

                    motorh.comm_set_speed_ERPM(0)
                    motorh.update()
                    sleep(0.25)
                    var = 0
                    runcount = 0
                    sleep(0.75)

                    # Run inflow motor
                    sleep(0.5)
                    print("Running inflow motor...")
                    sleep(0.1)
                    run_motor_with_timeout(motor_inflow, target_speed=-15000, timeout=9.75)
                    sleep(0.25)
                    control_actuator(actuator_up, duration=2.3)
                    sleep(0.25)

                    # Move the actuator to UP position
                    control_actuator(actuator_up, duration=2.2)
                    sleep(0.75)

                    # Run outflow motor for 5.5 seconds
                    print("Running outflow motor...")
                    run_motor_with_timeout(motor_outflow, target_speed=10250, timeout=14.75)
                    sleep(1.75)

                    # Run handle motor until torque is below 1
                    print("Running handle motor until torque is below 1...")
                    stop_motor_on_low_torque(motorh, target_speed=5000, timeout=20, torque_threshold=5.0)
                    sleep(1.75)

                    # Close plates
                    print("Closing plates...")
                    close_plates()
                    green()
                    
                    # Unlock the handle
                    unlock_handle()
                    sleep(3.5)
                    unlock_handle()
                    sleep(15)
                    count = count+1

                elif count%2!=0:
                    control_actuator(actuator_up, duration=2.3)

                    # Wait for both lock buttons to be pressed
                    print("Waiting for lock buttons to be pressed...")
                    while not (lock_sensor_handle.is_pressed and lock_sensor_inflow.is_pressed):
                        sleep(0.25)

                    print("Both lock buttons pressed. Opening plates...")
                    red()
                    open_plates()
                    sleep(0.75)

                    print("Running handle motor...")
                    sleep(0.25)
                    motorh.comm_set_speed_ERPM(float(-7500))
                    motorh.update()
                    motor_torque = motorh.get_motor_torque_newton_meters()
                    print("Motor Torque (Nm):", motor_torque)
                    runcount = 0

                    while runcount < 6*5000:
                        motorh.comm_set_speed_ERPM(float(-7500))
                        motorh.update()
                        motor_torque = motorh.get_motor_torque_newton_meters()
                        print("Motor Torque (Nm):", motor_torque)
                        runcount += 1

                    motorh.comm_set_speed_ERPM(0)
                    motorh.update()
                    sleep(0.25)
                    var = 0
                    runcount = 0
                    sleep(0.75)

                    # Run inflow motor
                    sleep(0.5)
                    print("Running inflow motor...")
                    sleep(0.1)
                    run_motor_with_timeout(motor_outflow, target_speed=-15000, timeout=9.75)
                    sleep(0.25)
                    control_actuator(actuator_down, duration=2.3)
                    sleep(0.25)

                    # Move the actuator to UP position
                    control_actuator(actuator_down, duration=2.2)
                    sleep(0.75)

                    # Run outflow motor for 5.5 seconds
                    print("Running outflow motor...")
                    run_motor_with_timeout(motor_inflow, target_speed=10250, timeout=14.75)
                    sleep(1.75)

                    # Run handle motor until torque is below 1
                    print("Running handle motor until torque is below 1...")
                    stop_motor_on_low_torque(motorh, target_speed=5000, timeout=20, torque_threshold=5.0)
                    sleep(1.75)

                    # Close plates
                    print("Closing plates...")
                    close_plates()
                    green()
                    
                    # Unlock the handle
                    unlock_handle()
                    sleep(3.5)
                    unlock_handle()
                    sleep(15)
                    count=count+1

                else:
                    sleep(0.30)
                    control_actuator(actuator_down, duration=2.3)

                    # Wait for both lock buttons to be pressed
                    print("Waiting for lock buttons to be pressed...")
                    while not (lock_sensor_handle.is_pressed and lock_sensor_inflow.is_pressed):
                        sleep(0.25)

                    print("Both lock buttons pressed. Opening plates...")
                    red()
                    open_plates()
                    sleep(0.75)

                    print("Running handle motor...")
                    sleep(0.25)
                    motorh.comm_set_speed_ERPM(float(-7500))
                    motorh.update()
                    motor_torque = motorh.get_motor_torque_newton_meters()
                    print("Motor Torque (Nm):", motor_torque)
                    runcount = 0

                    while runcount < 6*5000:
                        motorh.comm_set_speed_ERPM(float(-7500))
                        motorh.update()
                        motor_torque = motorh.get_motor_torque_newton_meters()
                        print("Motor Torque (Nm):", motor_torque)
                        runcount += 1

                    motorh.comm_set_speed_ERPM(0)
                    motorh.update()
                    sleep(0.25)
                    var = 0
                    runcount = 0
                    sleep(0.75)

                    # Run inflow motor
                    sleep(0.5)
                    print("Running inflow motor...")
                    sleep(0.1)
                    run_motor_with_timeout(motor_inflow, target_speed=-15000, timeout=9.75)
                    sleep(0.25)
                    control_actuator(actuator_up, duration=2.3)
                    sleep(0.25)

                    # Move the actuator to UP position
                    control_actuator(actuator_up, duration=2.2)
                    sleep(0.75)

                    # Run outflow motor for 5.5 seconds
                    print("Running outflow motor...")
                    run_motor_with_timeout(motor_outflow, target_speed=10250, timeout=14.75)
                    sleep(1.75)

                    # Run handle motor until torque is below 1
                    print("Running handle motor until torque is below 1...")
                    stop_motor_on_low_torque(motorh, target_speed=5000, timeout=20, torque_threshold=5.0)
                    sleep(1.75)

                    # Close plates
                    print("Closing plates...")
                    close_plates()
                    green()
                    
                    # Unlock the handle
                    unlock_handle()
                    sleep(3.5)
                    unlock_handle()
                    sleep(15)
                    count = count+1
