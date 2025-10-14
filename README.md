# RP2040_UCompute
Plateforme de développement basé sur un RP2040
taille: 96mm x 42mm
<BR>
<img width="573" height="281" alt="image" src="https://github.com/user-attachments/assets/853fa8fa-20b1-4d21-8bcf-28d7ebb2a3ee" />


## Caractéristiques:

- RP2040 
- LCD 1.3" 240x240 IPS ST7789
- EEPROM I2C (optionel)
- Bornier pour néopixel
- 1 Connecteur JST pour des modules I2C
- 3 boutons pour l'interface utilisateur (relié ADC0)
- SIP pour prototypage (8 IOs).
- Port USB (USB Mini-B)
- Fusible PTC (500ma)
- Piezo
- Port MicroSD
- QSPI flash en boitier SOP8 permettant de choisir la taille (2meg - 16meg)
- DEL connecté au port standard GP25
- support pour un module Ethernet W5500
- Trous de montage 3mm
<BR>
[!TIP] 
 le module W5500 requière environ 200ma, assurez vous d'avoir une alimentation conséquente.<BR><BR>

## Répertoires:
  Firmware: Firmware compilé en fonction des différentes configuration du SPI <BR>
  Hardware: Schématique, Gerber <BR>
  TestCode: Code Python servant d'exemple d'utilisation des différentes fonctionnalitées <BR>

## Assignation des IOs

```Python
_MicroSD_Detect = 7 # détection de la présence d'une carte MicroSD (GP7) <BR>
_MicroSD_Select = 13 # définition de la pin Select du SDCARD (GP13) <BR>
_W5500_Select = 8 # définition de la pin Select du W5500 (GP8) <BR>
_W5500_Reset = 10 # définition de la pin Reset du W5500 (GP10) <BR>
_SPI1_SCK = 14 # SPI1_shared Clock <BR>
_SPI1_MOSI = 15 # SPI1_shared MOSI <BR>
_SPI1_MISO = 12 # SPI1_shared MISO <BR>
_ST7789_SCK = 2 # définition de la pin Clock du ST7789 (GP2) SPI0 <BR>
_ST7789_MOSI = 3 # définition de la pin MOSI du ST7789 (GP3) SPI0 <BR>
_ST7789_RESET = 4 # définition de la pin Reset du ST7789 (GP4) <BR>
_ST7789_DC = 5 # définition de la pinSelect du ST7789 (GP5) <BR>
_ST7789_BL = 6 # définition de la pinBacklit du ST7789 (GP6) <BR>
_Led_System = 25 # définition du port  del systeme (GP25) <BR>
_I2C_SDA = 20 # définition de Data du I2C(0) (GP20) <BR>
_I2C_SCL = 21 # définition de SCL du I2C(0) (GP21) <BR>
_Buzzer = 11 # définition du  buzzer (GP11) <BR>
_NeoPixel = 23 # définition du port NeoPixel (GP23) <BR>
_EEPROM_ADDR = 0x50 # adresse du eeprom <BR>
_Boutons = 26 # définition du port analogue des boutons (GP26) <BR>
_UART = 0 # UART par defaut <BR>
_TX_PIN = 0 # TX Pin (GP0) <BR>
_RX_PIN = 1 # TX Pin (GP1) <BR>
```

## Rendu 3D
<img width="1110" height="470" alt="image" src="https://github.com/user-attachments/assets/91428e7b-5c0c-451a-8e28-290e433af26a" /><BR>
## BOM
Rev 1.2: 
<img width="1707" height="962" alt="image" src="https://github.com/user-attachments/assets/d4e758f1-466e-432b-9660-30dd6cbc7dc9" /><BR>

## Révision
Rev 1.1: Release candidat. <BR>
Rev 1.2: Corrections; ajout d'une diode de protection entre le 5v du port USB et le header du Neopixel et une seconde diode sur la ligne DO du Neopixel.<BR><BR>
## Références:
https://github.com/Wiznet/RP2040-HAT-MicroPython/blob/main/Ethernet%20Example%20Getting%20Started%20%5BMicropython%5D.md
https://github.com/Wiznet/RP2040-HAT-MicroPython/tree/main/examples
https://docs.micropython.org/en/latest/rp2/quickref.html

