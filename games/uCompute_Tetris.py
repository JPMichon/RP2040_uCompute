#------------------------------------------------
#  Tetris Game 240x240 ST7789 SPI LCD
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
_Buzzer = 11 

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

def play_block_hit():
    buzzer = PWM(Pin(_Buzzer))
    buzzer.freq(NOTES['SOL5'])
    buzzer.duty_u16(16384)
    utime.sleep(0.05)
    buzzer.deinit()

def WaitInputKey():
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
    fbuf.fill(st7789.BLACK)
    fbuf.rect(0, 0, screen_width, screen_height, st7789.BLUE)
    fbuf.fill_rect(10, 10, screen_width-20, 100, st7789.BLUE)
    fbuf.fill_rect(15, 15, screen_width-30, 90, st7789.RED)
    fbuf.large_text("uCompute", 60, 30, 2, st7789.BLUE)
    fbuf.large_text("-TETRIS-", 50, 70, 2,  st7789.BLACK)
    fbuf.large_text("[ANY KEY]", 50, 200, 2,  st7789.GREEN)
    display.blit_buffer(buffer, 0, 0, screen_width, screen_height)

# Dimensions de la grille de Tetris
GRID_COLS = 10
GRID_ROWS = 20
BLOCK_SIZE = 10  # 10x10 pixels par bloc
GRID_X_OFFSET = (screen_width - (GRID_COLS * BLOCK_SIZE)) // 2  # Centrage horizontal
GRID_Y_OFFSET = 20

# Formes des Tetrominos (Matrice 4x4)
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1], [1, 1]], # O
    [[1, 1, 0], [0, 1, 1]], # Z
    [[0, 1, 1], [1, 1, 0]]  # S
]

SHAPE_COLORS = [st7789.CYAN, st7789.MAGENTA, st7789.WHITE, st7789.BLUE, st7789.YELLOW, st7789.RED, st7789.GREEN]

def rotate_shape(shape):
    # Rotation anti-horaire/horaire d'une matrice 2D
    return [list(x) for x in zip(*shape[::-1])]

def check_collision(grid, shape, offset_x, offset_y):
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val:
                grid_x = offset_x + c
                grid_y = offset_y + r
                if grid_x < 0 or grid_x >= GRID_COLS or grid_y >= GRID_ROWS:
                    return True
                if grid_y >= 0 and grid[grid_y][grid_x] != st7789.BLACK:
                    return True
    return False

def merge_shape(grid, shape, offset_x, offset_y, color):
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val and (offset_y + r) >= 0:
                grid[offset_y + r][offset_x + c] = color

def clear_lines(grid):
    global score
    lines_cleared = 0
    new_grid = [row for row in grid if any(block == st7789.BLACK for block in row)]
    lines_cleared = GRID_ROWS - len(new_grid)
    
    # Remplir le haut avec de nouvelles lignes vides
    for _ in range(lines_cleared):
        new_grid.insert(0, [st7789.BLACK] * GRID_COLS)
        
    if lines_cleared > 0:
        score += lines_cleared * 100
        play_block_hit()
        
    return new_grid

def new_piece():
    global current_shape, current_color, piece_x, piece_y
    idx = random.randint(0, len(SHAPES) - 1)
    current_shape = SHAPES[idx]
    current_color = SHAPE_COLORS[idx]
    piece_x = GRID_COLS // 2 - len(current_shape[0]) // 2
    piece_y = -len(current_shape)

def init_game():
    global grid, score, game_over, fall_speed, last_fall_time
    grid = [[st7789.BLACK] * GRID_COLS for _ in range(GRID_ROWS)]
    score = 0
    game_over = False
    fall_speed = 700 # Millisecondes entre chaque descente
    last_fall_time = utime.ticks_ms()
    new_piece()

# Démarrage
splashScreen()
play_game_start()
WaitInputKey()
init_game()

# Variables pour éviter le spam des boutons
last_key_time = utime.ticks_ms()

while True:
    fbuf.fill(st7789.BLACK)
    current_time = utime.ticks_ms()
    
    if not game_over:
        # 1. Gestion des entrées utilisateur (avec anti-rebond léger)
        if utime.ticks_diff(current_time, last_key_time) > 150:
            key = Read_Keys()
            if key == 'Gauche':
                if not check_collision(grid, current_shape, piece_x - 1, piece_y):
                    piece_x -= 1
                last_key_time = current_time
            elif key == 'Droite':
                if not check_collision(grid, current_shape, piece_x + 1, piece_y):
                    piece_x += 1
                last_key_time = current_time
            elif key == 'select':
                rotated = rotate_shape(current_shape)
                if not check_collision(grid, rotated, piece_x, piece_y):
                    current_shape = rotated
                last_key_time = current_time

        # 2. Gestion de la gravité (Chute de la pièce)
        if utime.ticks_diff(current_time, last_fall_time) > fall_speed:
            if not check_collision(grid, current_shape, piece_x, piece_y + 1):
                piece_y += 1
            else:
                # La pièce se pose
                if piece_y < 0:
                    # Si elle se bloque hors de l'écran, fin de partie
                    game_over = True
                else:
                    merge_shape(grid, current_shape, piece_x, piece_y, current_color)
                    grid = clear_lines(grid)
                    new_piece()
            last_fall_time = current_time

        # 3. Rendu visuel du jeu
        # Interface et Score
        fbuf.text("SCORE: " + str(score), 10, 5, st7789.WHITE)
        fbuf.rect(GRID_X_OFFSET - 2, GRID_Y_OFFSET - 2, (GRID_COLS * BLOCK_SIZE) + 4, (GRID_ROWS * BLOCK_SIZE) + 4, st7789.BLUE)

        # Dessin de la grille stockée
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if grid[r][c] != st7789.BLACK:
                    fbuf.fill_rect(GRID_X_OFFSET + (c * BLOCK_SIZE), GRID_Y_OFFSET + (r * BLOCK_SIZE), BLOCK_SIZE - 1, BLOCK_SIZE - 1, grid[r][c])

        # Dessin de la pièce active en mouvement
        for r, row in enumerate(current_shape):
            for c, val in enumerate(row):
                if val and (piece_y + r) >= 0:
                    fbuf.fill_rect(GRID_X_OFFSET + ((piece_x + c) * BLOCK_SIZE), GRID_Y_OFFSET + ((piece_y + r) * BLOCK_SIZE), BLOCK_SIZE - 1, BLOCK_SIZE - 1, current_color)

    else:
        # Écran de fin de partie (Game Over)
        fbuf.large_text("GAME OVER", 50, 70, 2, st7789.RED)
        fbuf.large_text("Score: " + str(score), 45, 120, 2, st7789.WHITE)
        fbuf.large_text("[ANY KEY]", 50, 200, 2,  st7789.GREEN)
        display.blit_buffer(buffer, 0, 0, screen_width, screen_height)
        play_game_over()
        WaitInputKey()
        init_game()

    # Rafraîchissement de l'écran matériel
    display.blit_buffer(buffer, 0, 0, screen_width, screen_height)
    utime.sleep_ms(20)
