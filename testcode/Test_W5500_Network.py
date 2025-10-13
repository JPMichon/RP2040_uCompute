#source: https://github.com/Wiznet/RP2040-HAT-MicroPython
# Pico firmware disponible a ce lien: https://github.com/Wiznet/RP2040-HAT-MicroPython/releases
from usocket import socket
from machine import Pin,SPI
import network
import time

led = Pin(25, Pin.OUT)
_W5500_Select = 8 # définition du  Select du W5500 (GP8)
_W5500_Reset = 10 # définition du  Reset du W5500 (GP10)
_SPI1_SCK = 14 # SPI1_shared Clock
_SPI1_MOSI = 15 # SPI1_shared MOSI
_SPI1_MISO = 12 # SPI1_shared MISO

#W5x00 chip init
def w5x00_init():
    spi=SPI(1,2_000_000, mosi=Pin(_SPI1_MOSI),miso=Pin(_SPI1_MISO),sck=Pin(_SPI1_SCK))
    nic = network.WIZNET5K(spi,Pin(_W5500_Select),Pin(_W5500_Reset)) #spi,cs,reset pin
    nic.active(True)
#   nic.ifconfig(('192.168.1.6','255.255.255.0','192.168.1.1','8.8.8.8'))
    nic.ifconfig('dhcp')
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
    print(nic.ifconfig())
        
def main():
    w5x00_init()

    while True:
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)

if __name__ == "__main__":
    main()