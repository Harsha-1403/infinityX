import gpiod
import time
LED_PIN = 24
BUTTON1_PIN = 9
BUTTON2_PIN = 10
chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(LED_PIN)
button1_line = chip.get_line(BUTTON1_PIN)
button2_line = chip.get_line(BUTTON2_PIN)
led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
button1_line.request(consumer="Button1", type=gpiod.LINE_REQ_DIR_IN)
button2_line.request(consumer="Button2", type=gpiod.LINE_REQ_DIR_IN)
try:
   while True:
       button1_state = button1_line.get_value()
       button2_state = button2_line.get_value()
       if button1_state == 1 and button2_state == 1:
           led_line.set_value(1)
           time.sleep(0.35)
           led_line.set_value(0)
       else:
           led_line.set_value(0)
finally:
   led_line.release()
button1_line.release()
button2_line.release()
