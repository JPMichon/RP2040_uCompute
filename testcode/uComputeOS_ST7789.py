# -----------------------------------------------------------------------------
#  RP2040 uCompute - uComputeOS
#  Copyright (c) 2026 JP Michon
#  
#  Ce programme et le matériel associé sont protégés par la licence :
#  Creative Commons Attribution - Pas d'Utilisation Commerciale - 
#  Partage dans les Mêmes Conditions 4.0 International (CC BY-NC-SA 4.0)
# -----------------------------------------------------------------------------
# uComputeOS ST7789 Version
# Identification de la version du PCB pour la configuration des IOs

# ---------------------------------------------------------
from machine import I2C, Pin, SPI, PWM
import st7789 as st7789
import time
import sys
import framebuf2
import sdcard
import os

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

# --- INITIALISATION ---
BTN_Analogue = machine.ADC(_Boutons) #Diviseur de tension des boutons
# set landscape screen
screen_width = 240
screen_height = 240
screen_rotation = 1
spi = SPI(0,baudrate=60000000,polarity=1,phase=1,bits=8,firstbit=SPI.MSB,sck=Pin(_ST7789_SCK),mosi=Pin(_ST7789_MOSI))
display = st7789.ST7789(spi,screen_width,screen_height,reset=Pin(_ST7789_RESET, Pin.OUT),dc=Pin(_ST7789_DC, Pin.OUT),backlight=Pin(_ST7789_BL, Pin.OUT),rotation=screen_rotation)
# Lecteur MicroSD (SPI)
spi = SPI(1, sck=Pin(_SPI1_SCK), mosi=Pin(_SPI1_MOSI), miso=Pin(_SPI1_MISO))

# Initialisation du FrameBuffer
# FrameBuffer needs 2 bytes for every RGB565 pixel
buffer_width = 240
buffer_height = 240
buffer = bytearray(buffer_width * buffer_height * 2)
fbuf = framebuf2.FrameBuffer(buffer, buffer_width, buffer_height, framebuf2.RGB565)
fbuf.fill(st7789.WHITE)

try:
    sd = sdcard.SDCard(spi, Pin(_MicroSD_Select))
except Exception:
    sd = None
    print("No SD Card detected")
    

# --- FONCTIONS ---
def sd_available():
    if sd is None:
        return False
    try:
        os.mount(sd, "/sd")
        os.umount("/sd")
        return True
    except OSError as e:
        return e.args[0] == 17  # Déjà monté (EEXIST)
    except Exception:
        return False

def draw_header(title):
    fbuf.fill(st7789.BLACK) # Efface l'écran (le framefuffer)
    fbuf.large_text(title, 35, 10, 2, st7789.GREENYELLOW)
    fbuf.rect(1, 1, 239, 30, st7789.GREENYELLOW, False ) # boite Vide

def splash_screen():
    info = os.statvfs('/')
    # Extraction des valeurs numériques du tuple (AJOUTER LES CORCHETS [])
    taille_bloc = info[0]   # Taille du bloc (ex: 4096)
    blocs_totaux = info[2]  # Nombre total de blocs
    blocs_libres = info[3]  # Nombre de blocs libres
    Flashtotal = (blocs_totaux * taille_bloc) / 1024
    Flashlibre = (blocs_libres * taille_bloc) / 1024
    
    fbuf.fill(st7789.BLACK) # Efface l'écran (le framefuffer)
    fbuf.large_text('uCompute OS', 35, 10, 2, st7789.GREENYELLOW)
    fbuf.rect(1, 1, 239, 30, st7789.GREENYELLOW, False ) # boite Vide
    fbuf.large_text(f"{os.uname().machine}", 0, 40, 1, st7789.GREENYELLOW)
    #fbuf.large_text("RP2040 @ " + str(int((machine.freq()/1000000))) + " Mhz", 10, 40, 1, st7789.GREENYELLOW)
    fbuf.large_text("Firmware:", 4, 60, 1, st7789.GREENYELLOW)
    fbuf.large_text((str(os.uname().release)[:30]), 20, 70, 1, st7789.GREENYELLOW)
    fbuf.large_text((str(os.uname().version)[:30]), 20, 80, 1, st7789.GREENYELLOW)
    fbuf.large_text("Flash:", 4, 100, 1, st7789.GREENYELLOW)
    fbuf.large_text(f"Free:{Flashlibre:.0f}/{Flashtotal:.0f} KB", 20, 110, 1, st7789.GREENYELLOW)
    display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)
    fbuf.large_text('Navigation',40, 190, 2, st7789.GREENYELLOW)
    fbuf.line(1, 210, 239, 210, st7789.GREENYELLOW) # ligne
    fbuf.large_text('FLASH',5, 220, 2, st7789.GREENYELLOW)
    if sd_disponible:
        fbuf.large_text('SD',200, 220, 2, st7789.GREENYELLOW)
    display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)

def read_keys():
    _read = BTN_Analogue.read_u16()
    _KeyPress='null'
    if _read < 7000: #Down
        _KeyPress='up'
    elif _read < 12000: #Select
        _KeyPress='select'
    elif _read < 16000: # Up
        _KeyPress='down'
    #print(str(_read))
    return _KeyPress   

def afficher_menu():
    draw_header("uCompute OS")
    Fichier_affichage=8
    if not files:
        fbuf.large_text("Aucun script .py",30, 100, 2, st7789.GREENYELLOW)
        #oled.text("Aucun script .py", 0, 20)
    else:
        start_idx = (selected_index // Fichier_affichage) * Fichier_affichage
        for i in range(start_idx, min(start_idx + Fichier_affichage, len(files))):
            prefix = "> " if i == selected_index else "  "
            fbuf.large_text(prefix + files[i][:14],0, 40 + (i % Fichier_affichage) * 20, 2, st7789.GREENYELLOW)
            #oled.text(prefix + files[i][:14], 0, 15 + (i % 5) * 10)
    fbuf.line(1, 210, 239, 210, st7789.GREENYELLOW) # ligne
    fbuf.triangle( 5, 220, 20, 220, 12, 230, st7789.GREENYELLOW, True)
    fbuf.large_text('Select',75, 220, 2, st7789.GREENYELLOW)
    fbuf.triangle( 215, 230, 230, 230, 222, 220, st7789.GREENYELLOW, True)
    display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)
    
def copier_fichier(source, destination):
    try:
        with open(source, "rb") as f_src:
            with open(destination, "wb") as f_dest:
                while True:
                    bloc = f_src.read(512)
                    if not bloc: break
                    f_dest.write(bloc)
        return True
    except Exception as e:
        print(f"Erreur copie: {e}")
        return False
    
def selected_file(nom_fichier):
    draw_header("uCompute OS")
    fbuf.large_text(nom_fichier[:16],30, 100, 2, st7789.GREENYELLOW)
    fbuf.line(1, 210, 239, 210, st7789.GREENYELLOW) # ligne
    fbuf.large_text("EXEC" ,100, 220, 2, st7789.GREENYELLOW)
    fbuf.large_text("RET" ,190, 220, 2, st7789.GREENYELLOW)
    if storage == "FLASH":
        fichier_source, fichier_dest = f"/{nom_fichier}", f"/sd/{nom_fichier}"
        fbuf.large_text('CP>SD',5, 220, 2, st7789.GREENYELLOW)
        
    else:
        fichier_source, fichier_dest = f"/sd/{nom_fichier}", f"/{nom_fichier}"
        fbuf.large_text("CP>\ " ,5, 220, 2, st7789.GREENYELLOW)
        
    display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)
    time.sleep(0.5)
    
    while True:
        key = read_keys()
        if key == 'down' and sd_disponible:
            draw_header("uCompute OS")
            fbuf.large_text("Copie de...",20, 80, 2, st7789.GREENYELLOW)
            fbuf.large_text(nom_fichier[:16],30, 100, 2, st7789.GREENYELLOW)
            display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)
            
            if copier_fichier(fichier_source, fichier_dest):
                fbuf.large_text("Done !",30, 140, 2, st7789.GREENYELLOW)
            else:
                fbuf.large_text("Echec copie!",30, 140, 2, st7789.RED)
            display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)    
            time.sleep(2)
            break
        
        elif key == 'up':
            break
        
        elif key == 'select':    
            try:
                with open(fichier_source, "r") as f:
                    draw_header("uCompute OS")
                    fbuf.large_text("Execution de...",20, 80, 2, st7789.GREENYELLOW)
                    fbuf.large_text(nom_fichier[:16],30, 100, 2, st7789.GREENYELLOW)
                    display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)
                    time.sleep(0.5)
                    code = f.read()
                    exec(code, globals())
            except Exception as e:
                fbuf.fill(st7789.BLACK) # Efface l'écran (le framefuffer)
                fbuf.large_text("ERREUR :",10, 140, 2, st7789.RED)
                fbuf.large_text(str(e)[:24],30, 160, 1, st7789.RED)
                display.blit_buffer(buffer, 0, 0, buffer_width, buffer_height)
                time.sleep(3)
            break
        time.sleep_ms(50)

# --- BOUCLE PRINCIPALE ---
sd_disponible = sd_available()
splash_screen()

# Choix de l'espace de stockage
storage = None
while storage is None:
    key_input = read_keys()
    if key_input == 'down':
        storage = "FLASH"
        files = [f for f in os.listdir("/") if f.endswith(".py")]
    elif key_input == 'up' and sd_disponible:
        storage = "SD"
        os.mount(sd, "/sd")
        files = [f for f in os.listdir("/sd") if f.endswith(".py")]
    time.sleep_ms(50)

files.sort()
selected_index = 0
afficher_menu()

# Boucle de navigation du menu
while True:
    key_input = read_keys()
    
    if key_input == 'up' and files:
        selected_index = (selected_index - 1) % len(files)
        afficher_menu()
        time.sleep_ms(100)  # Anti-rebond/ralentisseur de défilement
        
    elif key_input == 'down' and files:
        selected_index = (selected_index + 1) % len(files)
        afficher_menu()
        time.sleep_ms(100)
        
    elif key_input == 'select' and files:
        selected_file(files[selected_index])
        afficher_menu()  # Réaffiche le menu après action
        time.sleep_ms(100)
        
    time.sleep_ms(10)
