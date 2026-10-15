
# Based on demo.py
# Kevin McAleer
# test the nRF24L01 modules to send and receive data
# Watch this video for more information about that library https://www.youtube.com/watch?v=aP8rSN-1eT0

from nrf24l01 import NRF24L01
from ssd1306 import SSD1306_I2C
from machine import SPI, Pin, I2C
from time import sleep
import utime
import struct

#Configuration des Ports pour le uCompute V1.x
_I2C_SDA = 20 # définition de Data du I2C(0) (GP20)
_I2C_SCL = 21 # définition de SCL du I2C(0) (GP21)
_Boutons = 26 # définition du port analogue des boutons (GP26)
_SPI1_SCK = 14 # SPI1_shared Clock
_SPI1_MOSI = 15 # SPI1_shared MOSI
_SPI1_MISO = 12 # SPI1_shared MISO
_Led_System = 25 # définition du port  del systeme (GP25)
#---------------------------------
#Module uCompute NRF24L01
_NRF_24L01_CSN = 8 # chip select not
_NRF_24L01_CE = 10 # chip enable


# RF_SETUP register
_NRF24l01_POWER_0 = const(0x00)  # -18 dBm
_NRF24l01_POWER_1 = const(0x02)  # -12 dBm
_NRF24l01_POWER_2 = const(0x04)  # -6 dBm
_NRF24l01_POWER_3 = const(0x06)  # 0 dBm
_NRF24l01_SPEED_1M = const(0x00)
_NRF24l01_SPEED_2M = const(0x08)
_NRF24l01_SPEED_250K = const(0x20)

#Parametre de communication du module NRF24L01
#---------------------------------
payload_size = 20
_NRF24l01_Channel = 1
_NRF24l01_Power = _NRF24l01_POWER_3
_NRF24l01_Speed = _NRF24l01_SPEED_1M

# Define the channel or 'pipes' the radios use.
# switch round the pipes depending if this is a sender or receiver pico

#role = "send"
role = "receive"

if role == "send":
    send_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xd2\xf0\xf0\xf0\xf0"
else:
    send_pipe = b"\xd2\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xe1\xf0\xf0\xf0\xf0"

#---------------------------------

#
# Début de l'initialisation 
#

#Initialisation des IOs
System_LED = Pin(_Led_System,Pin.OUT)
BTN_Analogue = machine.ADC(_Boutons) #Diviseur de tension des boutons


#initialisation du bus I2C
i2c=I2C(0,sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
# -----------------------------------
# Choisir la résolution du OLED
#
screen_width = 128
screen_height = 64
oled = SSD1306_I2C(screen_width, screen_height, i2c)
#oled = SSD1306_I2C(128, 32, i2c)
#------------------------------------
#gestion de la sortie STDOUT sur l'ecran LCD
TTY_Pointer=0
WrapScreen= int(screen_height/10)  # nombre de ligne avant de wrapper sur l'écran /10 si charactere 8x8
TTY = ['']*WrapScreen# creation d'une matrice pour emuler un TTY

def PrintTTY(texte):
#------------------------------------------------------------------------------------
# Fonctions permettant d'utiliser le display comme un TTY pour afficher les logs
# et de scroller automatiquement
#------------------------------------------------------------------------------------
    global TTY_Pointer # en utilisant une variable global, cela permet d'initialiser une seule fois la variable. Il y a surement une facon plus elegante, pour garder l'etat d'une variable locale dans une fonction. 
    
    if TTY_Pointer < WrapScreen:
        TTY[TTY_Pointer]=texte[:15] # je limite le texte a la largeur de l'ecran
        TTY_Pointer+=1
    else: #  dans le cas ou je suis a la derniere ligne de l'ecran, je decale vers le haut
        for i in range(WrapScreen-1):
            TTY[i] = TTY[i+1] # je decale vers le haut
        TTY[TTY_Pointer-1]=texte[:15] # je limite le texte a la largeur de l'ecran
# j'affiche le texte sur l'ecran 
    oled.fill(0)
    for i in range(TTY_Pointer):
        line_ptr=i*10
        oled.text(TTY[i],0,line_ptr)
    oled.show() # render display
    
def WaitInputKey():
    while BTN_Analogue.read_u16()>64000: # attend any key
        utime.sleep(.05)

def SplashScreen():
    oled.fill(0)
    oled.text('----------------', 0, 0)
    if role == "send":
        oled.text('NRF24L01', 10, 10)
        oled.text('SENDER', 50, 20)
    else:
        oled.text('NRF24L01', 10, 10)
        oled.text('RECEIVER', 50, 20)
        
    oled.text('----------------', 0, 30)
    oled.text('[Press AnyKey]', 5, 50)
    oled.show()
    
def flash_led(times:int=None):
    ''' Flashed the built in LED the number of times defined in the times parameter '''
    for _ in range(times):
        System_LED(1)
        sleep(0.01)
        System_LED(0)
        sleep(0.01)
        
def setup_NRF24l01():
    print("Initialising the nRF24L0+ Module")
    csn = Pin(_NRF_24L01_CSN, mode=Pin.OUT, value=1)  # chip select not
    ce  = Pin(_NRF_24L01_CE, mode=Pin.OUT, value=0)  # chip enable
    spi = SPI(1, baudrate=20000000, sck=Pin(_SPI1_SCK), mosi=Pin(_SPI1_MOSI), miso=Pin(_SPI1_MISO))
    nrf = NRF24L01(spi, csn, ce,channel=_NRF24l01_Channel, payload_size=payload_size)
    nrf.set_power_speed(_NRF24l01_Power, _NRF24l01_Speed)  # Best for point to point links
    nrf.open_tx_pipe(send_pipe)
    nrf.open_rx_pipe(1, receive_pipe)
    nrf.start_listening()
    return nrf



def send(nrf, msg):
    # On ajoute le \n directement à la fin de la chaîne complète
    full_msg = msg + "\n"
    print("Sending message:", full_msg.strip())
    PrintTTY("Send: "+ msg)
    
    nrf.stop_listening()
    try:
        # On encode et on envoie TOUT le texte d'un seul coup (max 32 caractères)
        nrf.send(full_msg.encode())
        flash_led(1)
    except OSError:
        print(role, "Sorry message not sent")
        oled.fill(0)
        oled.text('Sorry message:', 10, 10)
        oled.text('not sent', 30, 20)
        oled.show()
    nrf.start_listening()


# main code loop
#--------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#--------------------------------------------------------------------------------------------------------------------------------------------------
flash_led(1)
SplashScreen()
#WaitInputKey()
utime.sleep(1)
try:
    nrf = setup_NRF24l01()
except OSError:
    print("NRF24l01 not found")
    COMM_LOST(1)
    oled.fill(0)
    oled.text('err Comm. Module', 0, 0)
    oled.text('-----------------', 0, 10)
    oled.text("nRF24L0+", 25, 30)
    oled.text("not found", 20, 40)
    oled.show()
    while True: # puisqu'il y a une erreure, je boucle en infini car cela ne sert a rien de continuer
        utime.sleep(0.1)
# Flush screen        
oled.fill(0)
oled.show()

nrf.start_listening()
msg_string = ""
if role == "receive":
    PrintTTY("Waiting")
    PrintTTY("------------")
    
while True:
    if role == "send":
        send(nrf, "Hello")
        utime.sleep(0.1) # Petite pause pour laisser le temps au récepteur
        send(nrf, "Test")
        utime.sleep(0.5)

    else:
        # Check for Messages
        if nrf.any():
            package = nrf.recv()
            # On décode directement le paquet entier reçu
            msg = package.decode() 
            flash_led(1)
        
            # On vérifie si notre caractère de fin \n est présent dans le bloc reçu
            if "\n" in msg:
                # On nettoie les espaces/sauts de ligne pour l'affichage
                clean_msg = msg.strip(" \n\r\t\x00")
                print("full message:", clean_msg)
                PrintTTY("MSG:" + clean_msg)
