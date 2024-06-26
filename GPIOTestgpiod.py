import gpiod
from time import sleep
LED_PIN = 17
BUTTON_PIN = 10
BUTTONB_PIN = 9
chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(LED_PIN)
button_line = chip.get_line(BUTTON_PIN)
buttonb_line = chip.get_line(BUTTONB_PIN)
led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
button_line.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)
buttonb_line.request(consumer="ButtonB", type=gpiod.LINE_REQ_DIR_IN)
try:
   while True:
       button_state = button_line.get_value()
       buttonb_state = buttonb_line.get_value()
       if button_state == 1 and buttonb_state == 0:
           led_line.set_value(1)
           sleep(0.35)
           led_line.set_value(0)
       else:
           led_line.set_value(0)
finally:
   led_line.release()
button_line.release()
exit()
