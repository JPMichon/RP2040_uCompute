#--------------------------------------------------------
#test le led sur GP25
#
#
#                                  JP Michon 03/2023
#--------------------------------------------------------
from machine import Pin
from time import sleep

import utime

GP25_led = Pin(25,Pin.OUT) # led GP25


# Tous les leds eteints.
GP25_led.value(0) # led GP25


while True:
    GP25_led.toggle()
    utime.sleep(1)
    