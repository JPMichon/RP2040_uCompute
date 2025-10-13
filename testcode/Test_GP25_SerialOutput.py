from machine import UART, Pin
import time
import utime

GP25_led = Pin(25,Pin.OUT) # led GP25
GP25_led.value(0) # led GP25

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters


uart.write(b'Boot\n\r')

while True:
    GP25_led.toggle()
    uart.write(b'GP25 toggle\n\r')
    utime.sleep(1)