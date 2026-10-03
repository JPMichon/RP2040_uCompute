from machine import UART,Pin, SPI
import time
import utime
import struct
import st7789 as st7789
import framebuf2
from SECRET import _SSID, _WifiPWD


#Configuration des Ports pour le uCompute V1.x
_MicroSD_Detect = 7 # détection de la présence d'une carte MicroSD (GP7)
_MicroSD_Select = 13 # définition de la pin Select du SDCARD (GP13)
_SPI1_SCK = 14 # SPI1_shared Clock
_SPI1_MOSI = 15 # SPI1_shared MOSI
_SPI1_MISO = 12 # SPI1_shared MISO
_ST7789_SCK = 2 # définition de la pin Clock du ST7789 (GP2) SPI0
_ST7789_MOSI = 3 # définition de la pin MOSI du ST7789 (GP3) SPI0
_ST7789_RESET = 4 # définition de la pin Reset du ST7789 (GP4)
_ST7789_DC = 5 # définition de la pinSelect du ST7789 (GP5)
_ST7789_BL = 6 # définition de la pinBacklit du ST7789 (GP6)

_Led_System = 25 # définition du port  del systeme (GP25)
_I2C_SDA = 20 # définition de Data du I2C(0) (GP20)
_I2C_SCL = 21 # définition de SCL du I2C(0) (GP21)
_Buzzer = 11 # définition du  buzzer (GP11)
_NeoPixel = 23 # définition du port NeoPixel (GP23)
_NeoPixel_nbr = 8 # nombre de neopixel sur le port
_EEPROM_ADDR = 0x50 # adresse du eeprom
_Boutons = 26 # définition du port analogue des boutons (GP26)

_NTPServer="pool.ntp.org"
_timeout = 2000 # 5 secondes
ESP01_EN = Pin(12,Pin.OUT) # ESP01 Enable
ESP01_RST = Pin(10,Pin.OUT) # ESP01 Reset

# set landscape screen
screen_width = 240
screen_height = 240
screen_rotation = 1
_Debugverbose=False

# Initialize UART on Pico
uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))

# Initialisation du LCD
spi = SPI(0,baudrate=40000000,polarity=1,phase=1,bits=8,firstbit=SPI.MSB,sck=Pin(_ST7789_SCK),mosi=Pin(_ST7789_MOSI))
display = st7789.ST7789(spi,screen_width,screen_height,reset=Pin(_ST7789_RESET, Pin.OUT),dc=Pin(_ST7789_DC, Pin.OUT),backlight=Pin(_ST7789_BL, Pin.OUT),rotation=screen_rotation)

# Initialisation du FrameBuffer
# FrameBuffer needs 2 bytes for every RGB565 pixel
buffer_width = 240
buffer_height = 240
buffer = bytearray(buffer_width * buffer_height * 2)
fbuf = framebuf2.FrameBuffer(buffer, buffer_width, buffer_height, framebuf2.RGB565)
fbuf.fill(st7789.BLACK)
display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)

def _init_esp12f():
    #active le ESP01 en resettant le ESP01 et en activant la pin enable
    ESP01_RST.value(0)  # reset
    utime.sleep(1.0) # reset 1sec
    ESP01_RST.value(1)  # reset
    utime.sleep(.5)
    ESP01_EN.value(1) # enable ESP01
    
def _Wait_ESP_Rsp(uart=uart, timeout=3000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    try:
            return resp.decode()
    except UnicodeError:
            print("Except!")
            #print(resp)
        
def _send_at(cmd, back='OK', timeout=2000):
    uart.write(cmd)
    print("CMD: "+cmd)
    utime.sleep_ms(timeout)
    toto=_Wait_ESP_Rsp(uart, timeout)
    #print("test:",toto)


            
             
#---------------------------------------------------------------------
# code principale
#
fbuf.fill(st7789.WHITE) # Efface l'écran (le framefuffer)
fbuf.large_text("NTP CLOCK", 10, 20, 3, st7789.BLUE)
display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height) # render display

#prepare le ESP12f
print ("Initialisation du ESP12f")
fbuf.large_text("Initialisation du ESP12f", 10, 80, 1, st7789.BLACK)
display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height) # render display
_init_esp12f()
if _send_at('AT\r\n'):
    print("OK")
_send_at('AT+GMR\r\n')
_send_at('AT+CWMODE=1\r\n', timeout=2000)
fbuf.large_text("Done ", 10, 90, 1, st7789.BLACK)
display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height) # render display
fbuf.large_text("Connexion Wifi: "+_SSID, 10, 100, 1, st7789.BLACK)
display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height) # render display
print("Connexion au WiFi...")
if _send_at('AT+CWJAP="' + _SSID + '","' + _WifiPWD + '"\r\n',timeout=4000):
    print("Connecté !")
uart.write('AT+CIFSR\r\n')
IP=_Wait_ESP_Rsp(uart, 2000)
print(IP.split('"')[1])
fbuf.large_text("IP: "+ IP.split('"')[1], 10, 110, 1, st7789.BLACK)
display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height) # render display
print("Connexion au serveur NTP")
if _send_at('AT+CIPSTART="UDP","'+_NTPServer+'",123\r\n'):
   print("Connecté !")
# si la connection est reussi, j'affiche le NTP server au LCD   
fbuf.large_text("Connexion a: "+_NTPServer, 10, 120, 1, st7789.BLACK)
display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height) # render display

print("Envoi la requete")
_send_at('AT+CIPSEND=48\r\n')    
ntp_request = b'\x1b' + 47 * b'\0'  
uart.write(ntp_request) 

utime.sleep(3) # Attendre la réponse
raw = uart.read()

if raw:
    # On cherche le début des données après les deux points ':' du +IPD,48:
    try:
        data_start = raw.find(b':') + 1
        response = raw[data_start:]
        
        # Les secondes commencent à l'octet 40 de la réponse utile
        seconds_bytes = response[40:44]
        
        if len(seconds_bytes) == 4:
            t = struct.unpack(">I", seconds_bytes)[0]

            TIME1970 = 2208988800
            t -= TIME1970
            t -= 5 * 3600  # GMT-5

            tm = time.localtime(t)
            print("Heure récupérée : {:02d}:{:02d}:{:02d}".format(tm[3], tm[4], tm[5]))
        else:
            print("Erreur : Paquet NTP incomplet")
    except Exception as e:
        print("Erreur lors de l'extraction :", e)
else:
    print("Erreur : Aucune donnée reçue de l'UART")
tm = time.localtime(t)
heure_str = "{:02d}:{:02d}:{:02d}".format(tm[3], tm[4], tm[5])
date_str = "{:04d}-{:02d}-{:02d}".format(tm[0], tm[1], tm[2])

print("Heure GMT:", heure_str)

while True:
    tm = time.localtime()
    heure_str = "{:02d}:{:02d}:{:02d}".format(tm[3], tm[4], tm[5])
    date_str = "{:04d}-{:02d}-{:02d}".format(tm[0], tm[1], tm[2])
    fbuf.fill(st7789.WHITE) # Efface l'écran (le framefuffer)
    fbuf.large_text("NTP CLOCK", 10, 20, 3, st7789.BLUE)
    fbuf.large_text(_NTPServer, 10, 45, 2, st7789.GREEN)
    fbuf.large_text(date_str, 10, 100, 2, st7789.GREEN)
    fbuf.large_text(heure_str, 25, 140, 3, st7789.RED)
    display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height) # render display
    utime.sleep(.1) 