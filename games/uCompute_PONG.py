#------------------------------------------------
#  Pong game 240x240 ST7789 SPI LCD
#  JPMICHON  05/2023
#  
#------------------------------------------------
import uos

from machine import I2C, Pin, SPI, PWM
import st7789 as st7789
import framebuf2
import utime

# Variables pour le jeux
BALL_SIZE = 6 # 2X2 pixels
BALL_SPEED_init = 4 # permet d'accelerer la balle
PAD_WIDTH = 25 # largeur de la palette
PAD_HEIGHT = 2
PAD_STEP =10
HALF_PAD_WIDTH = int(PAD_WIDTH / 2)
HALF_PAD_HEIGHT = int(PAD_HEIGHT / 2)

# Configuration des pins
_Buzzer = 11 # définition du port pour le buzzer (GP9)
_ST7789_SCK = 2 # définition de la pin Clock du ST7789 (GP2) SPI0
_ST7789_MOSI = 3 # définition de la pin MOSI du ST7789 (GP3) SPI0
_ST7789_RESET = 4 # définition de la pin Reset du ST7789 (GP4)
_ST7789_DC = 5 # définition de la pinSelect du ST7789 (GP5)
_ST7789_BL = 6 # définition de la pinBacklit du ST7789 (GP6)
_Boutons = 26 # définition du port analogue des boutons (GP26)
BTN_Analogue = machine.ADC(_Boutons) #Diviseur de tension des boutons

# set landscape screen
screen_width = 240
screen_height = 240
screen_rotation = 1
# #Creation du frame buffer meme taille que l'écran
buffer = bytearray(screen_width * screen_height * 2)
fbuf = framebuf2.FrameBuffer(buffer, screen_width, screen_height, framebuf2.RGB565)

spi0 = machine.SPI(0,20000000,sck=machine.Pin(_ST7789_SCK,machine.Pin.OUT),mosi=machine.Pin(_ST7789_MOSI,machine.Pin.OUT), polarity=1,phase=1)
display = st7789.ST7789(spi0,screen_width,screen_height,reset=Pin(_ST7789_RESET, Pin.OUT),dc=Pin(_ST7789_DC, Pin.OUT),backlight=Pin(_ST7789_BL, Pin.OUT),rotation=screen_rotation)
print(spi0)


NOTES = {
    'DO4': 262, 'RE4': 294, 'MI4': 330, 'FA4': 349, 'SOL4': 392, 'LA4': 440, 'SI4': 494,
    'DO5': 523, 'RE5': 587, 'MI5': 659, 'FA5': 698, 'SOL5': 784, 'LA5': 880, 'SI5': 988,
    'DO6': 1047, 'RE6': 1175, 'MI6': 1319, 'SILENCE': 0}
   
def play_game_start():
    buzzer = PWM(Pin(_Buzzer))
    partition = ['DO5', 'MI5', 'SOL5', 'DO5', 'PAUSE', 'DO6']
    tempos = [0.10, 0.10, 0.10, 0.15, 0.05, 0.35]
    for note, duree in zip(partition, tempos):
        frequence = 0 if note == 'PAUSE' else NOTES[note]
        if frequence == 0:
            buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            buzzer.freq(frequence)
            buzzer.duty_u16(32768)
            utime.sleep(duree)
        buzzer.duty_u16(0)
        utime.sleep(0.01)
    buzzer.deinit()
    
def play_game_over():
    buzzer = PWM(Pin(_Buzzer))
    partition = ['MI5', 'RE5', 'DO5', 'SI4', 'PAUSE', 'LA4']
    tempos = [0.15, 0.15, 0.15, 0.25, 0.10, 0.60]
    for note, duree in zip(partition, tempos):
        frequence = 0 if note == 'PAUSE' else NOTES[note]
        if frequence == 0:
            buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            buzzer.freq(frequence)
            buzzer.duty_u16(32768)
            utime.sleep(duree)
        buzzer.duty_u16(0)
        utime.sleep(0.02)
    buzzer.deinit()

def play_Collision_hit():
    buzzer = PWM(Pin(_Buzzer))
    buzzer.freq(NOTES['SOL5'])
    buzzer.duty_u16(16384)
    utime.sleep(0.05)
    buzzer.deinit()


def Read_Keys():
    _read = BTN_Analogue.read_u16()
    _KeyPress='null'
    if _read < 7000: #Droite
        _KeyPress='Droite'
    elif _read < 12000: #Select
        _KeyPress='select'
    elif _read < 16000: # Gauche
        _KeyPress='Gauche'          
    #print(str(_read)) #pour le debuggage affiche la lecture de la clé dans la console    
    return _KeyPress #+str(_read) 

def WaitInputKey():
    # Boucle TANT QUE la valeur est inférieure au seuil
    while BTN_Analogue.read_u16() > 40000:
        utime.sleep(0.01)
        
#Splash Screen
fbuf.fill(st7789.BLACK) # efface l'écran
fbuf.rect(0, 0, screen_width, screen_height, st7789.BLUE)
fbuf.fill_rect(10, 10, screen_width-20, 100, st7789.BLUE)
fbuf.fill_rect(15, 15, screen_width-30, 90, st7789.GREEN)
fbuf.large_text("uCompute", 60, 30, 2, st7789.BLUE)
fbuf.large_text("-PONG-", 70, 70,2,  st7789.WHITE)
fbuf.large_text("[ANY KEY]", 50, 200,2,  st7789.GREEN)
display.blit_buffer(buffer, 0, 0, screen_width, screen_height)

WaitInputKey() # boucle en attendant que la touche START soit enfoncer
play_game_start()    
fbuf.fill(st7789.BLACK) # efface l'écran
display.blit_buffer(buffer, 0, 0, screen_width, screen_height)
utime.sleep(.2)

x=120 # set la valeur initial de la position du curseur
# Lance la balle a partir du centre
ball_x = int(screen_width / 2)
ball_y = int(screen_height / 2)
# Initialise le mouvement de la balle
ball_x_dir = 1
ball_y_dir = 1
score=0
GameOver=False
BALL_SPEED=2
while GameOver==False: #Boucle infini
    tempokey=Read_Keys()
    if tempokey=='Droite':
        if x < (screen_width - PAD_WIDTH):  
            x=x+PAD_STEP
    if tempokey=='Gauche':
        if x > (PAD_STEP-PAD_WIDTH/2): 
            x=x-PAD_STEP
    fbuf.fill_rect(0,  235, 240, 3, st7789.BLACK) # efface la palette 
    fbuf.fill_rect(x,  235, PAD_WIDTH, PAD_HEIGHT, st7789.WHITE) # dessine la palette
    fbuf.fill_rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE, st7789.BLUE)
    display.blit_buffer(buffer, 0, 0, screen_width, screen_height)
    # Déplacement de la balle
    fbuf.fill_rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE, st7789.BLACK) #efface la balle
    
    ball_x = ball_x + (ball_x_dir*BALL_SPEED)
    ball_y = ball_y + (ball_y_dir*BALL_SPEED)
    
    # Détection des collisions avec les parois et fait rebondir la balle
    if ball_y < 0:
        play_Collision_hit()
        ball_y_dir = 1
    if ball_x > screen_width - 3:
        play_Collision_hit()
        ball_x_dir = -1
    if ball_x  < 0:
        play_Collision_hit()
        ball_x_dir = 1
    # Détection de la palette
    if ball_y > 235: # si la balle est au niveau de la palette, je valide s'il y a collision
        if ball_x > x and ball_x < (x+PAD_WIDTH): # si vrai, la palette a touché la balle
            play_Collision_hit()
            ball_y_dir = -1
            ball_y = ball_y-2
            score=score+1  # j'incrémente le score a chaque rebond sur la palette
        else:
            GameOver=True # partie fini
            
    BALL_SPEED = (score//10)+BALL_SPEED_init # a chaque tranche de 10, la balle augmente la vitesse de la balle         
    
    
# si j'arrive ici c'est que la partie est fini
fbuf.fill(st7789.BLACK) # efface l'écran
display.blit_buffer(buffer, 0, 0, screen_width, screen_height)
fbuf.large_text("Game Over", 60, 70, 2, st7789.BLUE, st7789.BLACK)
fbuf.large_text("Score: " +str(score),70,120, 2, st7789.YELLOW, st7789.BLACK)
display.blit_buffer(buffer, 0, 0, screen_width, screen_height)
play_game_over()