#------------------------------------------------
#  Breakout (Casse-briques) game 240x240 ST7789 SPI LCD
#------------------------------------------------
import uos
from machine import I2C, Pin, SPI, PWM, ADC
import st7789 as st7789
import framebuf2
import utime
import random

# Configuration de l'écran et des pins
_ST7789_SCK = 2 
_ST7789_MOSI = 3 
_ST7789_RESET = 4 
_ST7789_DC = 5 
_ST7789_BL = 6 
_Boutons = 26
_Buzzer = 11 # définition du port pour le buzzer (GP11)

BTN_Analogue = ADC(_Boutons)

screen_width = 240
screen_height = 240
screen_rotation = 1

buffer = bytearray(screen_width * screen_height * 2)
fbuf = framebuf2.FrameBuffer(buffer, screen_width, screen_height, framebuf2.RGB565)

spi0 = SPI(0, 20000000, sck=Pin(_ST7789_SCK, Pin.OUT), mosi=Pin(_ST7789_MOSI, Pin.OUT), polarity=1, phase=1)
display = st7789.ST7789(spi0, screen_width, screen_height, reset=Pin(_ST7789_RESET, Pin.OUT), dc=Pin(_ST7789_DC, Pin.OUT), backlight=Pin(_ST7789_BL, Pin.OUT), rotation=screen_rotation)

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

def play_brick_hit():
    buzzer = PWM(Pin(_Buzzer))
    buzzer.freq(NOTES['SOL5'])
    buzzer.duty_u16(16384)
    utime.sleep(0.05)
    buzzer.deinit()


# Variables du jeu
BALL_SIZE = 6
PAD_WIDTH = 40  # Élargi pour rendre le jeu plus accessible
PAD_HEIGHT = 6
PAD_Y = 220     # Position verticale fixe de la raquette

# Structure des briques
BRICK_ROWS = 4
BRICK_COLS = 6
BRICK_WIDTH = 36
BRICK_HEIGHT = 10
BRICK_GAP = 3
BRICK_START_Y = 40
BRICK_START_X = (screen_width - ((BRICK_COLS * BRICK_WIDTH) + ((BRICK_COLS - 1) * BRICK_GAP))) // 2

# Couleurs des lignes de briques
BRICK_COLORS = [st7789.RED, st7789.YELLOW, st7789.GREEN, st7789.BLUE]

def WaitInputKey():
    # Boucle TANT QUE la valeur est inférieure au seuil
    while BTN_Analogue.read_u16() > 40000:
        utime.sleep(0.1)

def Read_Keys():
    _read = BTN_Analogue.read_u16()
    if _read < 7000:
        return 'Droite'
    elif _read < 12000:
        return 'select'
    elif _read < 16000:
        return 'Gauche'
    return 'null'

def splashScreen():
    fbuf.fill(st7789.BLACK) # efface l'écran
    fbuf.rect(0, 0, screen_width, screen_height, st7789.BLUE)
    fbuf.fill_rect(10, 10, screen_width-20, 100, st7789.BLUE)
    fbuf.fill_rect(15, 15, screen_width-30, 90, st7789.GREEN)
    fbuf.large_text("uCompute", 60, 30, 2, st7789.BLUE)
    fbuf.large_text("-Breakout-", 40, 70, 2,  st7789.BLACK)
    fbuf.large_text("[ANY KEY]", 50, 200, 2,  st7789.GREEN)
    display.blit_buffer(buffer, 0, 0, screen_width, screen_height)

def init_game():
    global ball_x, ball_y, ball_dx, ball_dy, pad_x, bricks, score, game_over
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_dx = random.choice([-5, 5])
    ball_dy = -5
    pad_x = (screen_width - PAD_WIDTH) // 2
    score = 0
    game_over = False
    
    # Création de la matrice de briques [x, y, couleur, actif(1/0)]
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            bx = BRICK_START_X + col * (BRICK_WIDTH + BRICK_GAP)
            by = BRICK_START_Y + row * (BRICK_HEIGHT + BRICK_GAP)
            bricks.append([bx, by, BRICK_COLORS[row % len(BRICK_COLORS)], 1])

# Initialisation du premier round
splashScreen()
play_game_start()
WaitInputKey()
init_game()

# Boucle principale
while True:
    fbuf.fill(st7789.BLACK)
    
    if not game_over:
        # 1. Lecture des entrées
        key = Read_Keys()
        if key == 'Gauche' and pad_x > 0:
            pad_x -= 6
        elif key == 'Droite' and pad_x < (screen_width - PAD_WIDTH):
            pad_x += 6
            
        # 2. Mise à jour de la bille
        ball_x += ball_dx
        ball_y += ball_dy
        
        # Collisions avec les murs latéraux
        if ball_x <= 0 or ball_x >= (screen_width - BALL_SIZE):
            ball_dx = -ball_dx
        # Collision avec le plafond
        if ball_y <= 20: # Laisse de la place pour le score
            ball_dy = -ball_dy
            
        # Collision avec la raquette
        if ball_dy > 0: # La bille descend
            if (ball_y + BALL_SIZE >= PAD_Y) and (ball_y <= PAD_Y + PAD_HEIGHT):
                if (ball_x + BALL_SIZE >= pad_x) and (ball_x <= pad_x + PAD_WIDTH):
                    ball_dy = -ball_dy
                    # Calcul du point d'impact pour modifier l'angle
                    hit_pos = (ball_x + (BALL_SIZE // 2)) - (pad_x + (PAD_WIDTH // 2))
                    ball_dx = int(hit_pos / 4)
                    if ball_dx == 0:
                        ball_dx = 1 if random.random() > 0.5 else -1

        # Collision avec les briques
        bricks_left = False
        for b in bricks:
            if b[3] == 1: # Si la brique est active
                bricks_left = True
                # Vérification de la collision AABB
                if (ball_x + BALL_SIZE >= b[0] and ball_x <= b[0] + BRICK_WIDTH and
                    ball_y + BALL_SIZE >= b[1] and ball_y <= b[1] + BRICK_HEIGHT):
                    
                    b[3] = 0 # Désactiver la brique
                    ball_dy = -ball_dy # Rebond vertical
                    score += 10
                    play_brick_hit()
                    break # Gère une seule collision par frame
                    
        # Condition de victoire (plus de briques)
        if not bricks_left:
            init_game() # Relance une partie ou augmente la difficulté
            
        # Condition de défaite (bille sous la raquette)
        if ball_y > screen_height:
            game_over = True

        # 3. Dessin des éléments
        # Dessin du score
        fbuf.text("SCORE: " + str(score), 10, 5, st7789.WHITE)
        
        # Dessin de la raquette
        fbuf.fill_rect(pad_x, PAD_Y, PAD_WIDTH, PAD_HEIGHT, st7789.WHITE)
        
        # Dessin de la bille
        fbuf.fill_rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE, st7789.WHITE)
        
        # Dessin des briques
        for b in bricks:
            if b[3] == 1:
                fbuf.fill_rect(b[0], b[1], BRICK_WIDTH, BRICK_HEIGHT, b[2])
                
    else:
        # Écran de Game Over
        fbuf.large_text("GAME OVER", 50, 70, 2, st7789.RED)
        fbuf.large_text("Score: " + str(score), 45, 120, 2, st7789.WHITE)
        fbuf.large_text("[ANY KEY]", 50, 200, 2,  st7789.GREEN)
        display.blit_buffer(buffer, 0, 0, screen_width, screen_height)
        play_game_over()
        WaitInputKey()
        init_game()

    # Envoi du framebuffer à l'écran
    display.blit_buffer(buffer, 0, 0, screen_width, screen_height)
    utime.sleep_ms(15)
