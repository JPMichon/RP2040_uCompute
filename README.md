# RP2040_Ucompute
Plateforme de développement basé sur un RP2040

Projet d'utilisation de création d'un PI Pico sur stéroïde.
L'objectif est de créer une platine de développement IoT à faible coût et versatile.
taille: 96mm x 42mm

Caractéristique:

- RP2040 
- LCD 1.3" 240x240 IPS ST7789
- EEPROM I2C (optionel)
- Bornier pour néopixel
- 1 Connecteur JST pour des modules I2C
- 3 boutons pour l'interface utilisateur (relié ADC0)
- SIP pour prototypage (10 IOs).
- Port USB (USB Mini-B)
- Fusible PTC
- Piezo
- Port MicroSD
- QSPI flash en boitier SOP8 permettant de choisir la taille (2meg - 16meg)
- DEL connecté au port standard GP25
- support pour un module Ethernet W5500
- Trous de montage 3mm
<BR>
#Configuration des Ports pour le uCompute V1.x
- _MicroSD_Detect = 7 # détection de la présence d'une carte MicroSD (GP7)
- _MicroSD_Select = 13 # définition de la pin Select du SDCARD (GP13)
- _W5500_Select = 8 # définition de la pin Select du W5500 (GP8)
- _W5500_Reset = 10 # définition de la pin Reset du W5500 (GP10)
- _SPI1_SCK = 14 # SPI1_shared Clock
- _SPI1_MOSI = 15 # SPI1_shared MOSI
- _SPI1_MISO = 12 # SPI1_shared MISO
- _ST7789_SCK = 2 # définition de la pin Clock du ST7789 (GP2) SPI0
- _ST7789_MOSI = 3 # définition de la pin MOSI du ST7789 (GP3) SPI0
- _ST7789_RESET = 4 # définition de la pin Reset du ST7789 (GP4)
- _ST7789_DC = 5 # définition de la pinSelect du ST7789 (GP5)
- _ST7789_BL = 6 # définition de la pinBacklit du ST7789 (GP6)
- _Led_System = 25 # définition du port  del systeme (GP25)
- _I2C_SDA = 20 # définition de Data du I2C(0) (GP20)
- _I2C_SCL = 21 # définition de SCL du I2C(0) (GP21)
- _Buzzer = 11 # définition du  buzzer (GP11)
- _NeoPixel = 23 # définition du port NeoPixel (GP23)
- _NeoPixel_nbr = 8 # nombre de neopixel sur le port
- _EEPROM_ADDR = 0x50 # adresse du eeprom
_Boutons = 26 # définition du port analogue des boutons (GP26)
_UART = 0 # UART par defaut
_TX_PIN = 0 # TX Pin (GP0)
_RX_PIN = 1 # TX Pin (GP1)
<img width="1110" height="470" alt="image" src="https://github.com/user-attachments/assets/91428e7b-5c0c-451a-8e28-290e433af26a" />
