#-----------------------------------------------------------------------------------------
#Programme de diagnostique scanner le bus I2C sur le PICO FUN BOARD V1.0
#
#
#                                  JP Michon 01/2023
#-----------------------------------------------------------------------------------------
import machine
import utime
import ahtx0

sdaPIN=20
sclPIN=21
    
#initialisation du protocole        
i2c = machine.I2C(0, scl=machine.Pin(sclPIN), sda=machine.Pin(sdaPIN), freq=200000)
print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))

# test de lecture du capteur ATH20

sensorAHT20 = ahtx0.AHT10(i2c)

print("Temperature: %0.2f C" % sensorAHT20.temperature)
print("Humidity: %0.2f %%" % sensorAHT20.relative_humidity)
