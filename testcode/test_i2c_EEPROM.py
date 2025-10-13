# source pour la partie du code et de la librairie EEPROM
# https://github.com/shivasiddharth/Raspberry-Pi-Pico/blob/main/Micropython/Examples/EEPROM/demo.py
#
from machine import I2C, Pin
import EEPROM_CAT24C256 #For 32bit or 4KB EEPROM library. Change this according to your library name.


i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=200000)

#
#
# scan du bus I2C
#
print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
#-------------------------------------------
# Registre des adresses i2c  
# 0x38  = AHT10/AHT20 temperature+humidity sensor
# 0x3c  = OLED SSD1306
# 0x50  = EEPROM
#
#------------------------------------------    
i2caddr=0x50 #Set the I2C address of your EEPROM.
#
eeprom = EEPROM_CAT24C256.CAT24C256(i2c,i2caddr)


# # Read and print 32Bytes starting from memory address 0
print(eeprom.read(0, 32))


# # Read and print entire EEPROM. This demo is constructed for a 4KB EEPROM, hence 4096.
# print(eeprom.read(0,4096))

# # Write String to memory address 0
# eeprom.write(0, 'Test string')

# # Wipe the EEPROM
# eeprom.wipe()

# # Write multiple pages (Bytes per page are EEPROM dependent. This demo is constructed for an EEPROM with 32Bytes per page specification. Please check the datasheet for your EEPROM)
# eeprom.write(0, b'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# # Read multiple pages (Bytes per page are EEPROM dependent. This demo is constructed for an EEPROM with 32Bytes per page specification. Please check the datasheet for your EEPROM)
# eeprom.read(0,64)

# # Mutliple page writes (fill pages 0 and 1 with test data)
# # Write is performed in two steps, "0" x 32 in the first page, then "1" x 32 in the next page
# # Memory address was at the start of a page boundary so each write is a full 32 byte page write
# # This demo is constructed for an EEPROM with 32 Bytes per page specification. Please check the datasheet for your EEPROM
#eeprom.write(0, b'0000000000000000000000000000000011111111111111111111111111111111')

# # Partial page writes
# # Write some bytes spanning two pages, not starting at a page boundary
# # Write is performed in two steps, "abc" in the first page then "def" in the next page
# # This demo is constructed for an EEPROM with 32 Bytes per page specification. Please check the datasheet for your EEPROM
# eeprom.write(29, b'abcdef')
# eeprom.read(0,64)