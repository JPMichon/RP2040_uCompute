# ---------------------------------------------------------
# uCompute Digital Rain for ST7789
# ---------------------------------------------------------
from machine import I2C, Pin, SPI, PWM
import st7789 as st7789
import time
import framebuf2
import random

# ---------------------------------------------------------------
# uCompute standard pin
_SSD1306_ADDR = 0x3C
_Buzzer = 11 # définition du  buzzer (GP11)
_MicroSD_Detect = 7 # détection de la présence d'une carte MicroSD (GP7)
_MicroSD_Select = 13 # définition de la pin Select du SDCARD (GP13)
_SPI1_SCK = 14 # SPI1_shared Clock
_SPI1_MOSI = 15 # SPI1_shared MOSI
_SPI1_MISO = 12 # SPI1_shared MISO
_Led_System = 25 # définition du port  del systeme (GP25)
_I2C_SDA = 20 # définition de Data du I2C(0) (GP20)
_I2C_SCL = 21 # définition de SCL du I2C(0) (GP21)
_Boutons = 26 # définition du port analogue des boutons (GP26)
_ST7789_SCK = 2 # définition de la pin Clock du ST7789 (GP2) SPI0
_ST7789_MOSI = 3 # définition de la pin MOSI du ST7789 (GP3) SPI0
_ST7789_RESET = 4 # définition de la pin Reset du ST7789 (GP4)
_ST7789_DC = 5 # définition de la pinSelect du ST7789 (GP5)
_ST7789_BL = 6 # définition de la pinBacklit du ST7789 (GP6)

# Configuration de l'écran ST7789 (SPI)
screen_width = 240
screen_height = 240
screen_rotation = 1

spi = SPI(0, baudrate=20000000, polarity=1, phase=1, bits=8, firstbit=SPI.MSB, sck=Pin(_ST7789_SCK), mosi=Pin(_ST7789_MOSI))
display = st7789.ST7789(
    spi,
    screen_width,
    screen_height,
    reset=Pin(_ST7789_RESET, Pin.OUT),
    dc=Pin(_ST7789_DC, Pin.OUT),
    backlight=Pin(_ST7789_BL, Pin.OUT),
    rotation=screen_rotation
)

# Définition des couleurs en format RGB565 (16 bits)
GREEN_DARK  = st7789.GREEN 
GREEN_MID   = st7789.GREENYELLOW   
WHITE       = st7789.WHITE  
BLACK       = st7789.BLACK  

# Initialisation du FrameBuffer
buffer_width = screen_width
buffer_height = screen_height
buffer = bytearray(buffer_width * buffer_height * 2)
fbuf = framebuf2.FrameBuffer(buffer, buffer_width, buffer_height, framebuf2.RGB565)

# Splash screen 
fbuf.fill(BLACK) 
fbuf.large_text('Booting', 60, 100, 2, GREEN_DARK)
display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)
time.sleep(1)

# Paramètres de l'animation Matrix adaptés à la résolution 240x240
FONT_WIDTH = 8    
FONT_HEIGHT = 8   
COLS = buffer_width // FONT_WIDTH  # Donne 30 colonnes

CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ*#$@%&+-=<>:?"

# Initialisation des pistes de gouttes
y_positions = [random.randint(-FONT_HEIGHT * 6, 0) for _ in range(COLS)]
speeds = [random.randint(4, 8) for _ in range(COLS)] 

# Boucle principale d'animation
while True:
    fbuf.fill(BLACK) 
    
    for col in range(COLS):
        x_pos = col * FONT_WIDTH
        y_pos = y_positions[col]
        
        if y_pos >= 0:
            # Caractère du haut (Vert sombre)
            if y_pos - (FONT_HEIGHT * 2) < buffer_height:
                char_top = random.choice(CHARS)
                fbuf.text(char_top, x_pos, y_pos - (FONT_HEIGHT * 2), GREEN_DARK)
                
            # Caractère du milieu (Vert intermédiaire)
            if y_pos - FONT_HEIGHT < buffer_height:
                char_mid = random.choice(CHARS)
                fbuf.text(char_mid, x_pos, y_pos - FONT_HEIGHT, GREEN_MID)
                
            # La tête de la goutte (Blanc)
            if y_pos < buffer_height:
                char_lead = random.choice(CHARS)
                fbuf.text(char_lead, x_pos, y_pos, WHITE)
        
        # Fait descendre la goutte
        y_positions[col] += speeds[col]
        
        # Réinitialisation en haut
        if y_positions[col] >= screen_height + (FONT_HEIGHT * 2):
            y_positions[col] = random.randint(-FONT_HEIGHT * 6, 0)
            speeds[col] = random.randint(4, 8)
            
    # Rafraîchissement complet de l'affichage via le buffer
    display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)
    
    time.sleep(0.01)
