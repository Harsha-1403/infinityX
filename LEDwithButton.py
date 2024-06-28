from gpiozero import LED, Button
from time import sleep

green = LED(7)
red = LED(8)
blue = LED(11)
lock_sensor_handle = Button(26)
lock_sensor_inflow = Button(20)

#yellowWire --> down lock
#orangeWire --> upper lock


while True:
    if lock_sensor_handle.is_pressed:
        red.on()
        green.off()
        blue.off()
        sleep(3)
    if lock_sensor_inflow.is_pressed:
        red.off()
        green.on()
        blue.off()
        sleep(3)
    if lock_sensor_inflow.is_pressed and lock_sensor_handle.is_pressed:
        red.off()
        green.off()
        blue.on()
        sleep(3)
  

