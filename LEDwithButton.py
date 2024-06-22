from gpiozero import LED, Button
from time import sleep

led = LED(24)
lock_sensor_handle = Button(10)
lock_sensor_inflow = Button(9)

while True:
    if lock_sensor_handle.is_pressed or lock_sensor_inflow.is_pressed:
        led.on()
        sleep(0.35)
        led.off()
        sleep(0.35)
        led.close()
        break
