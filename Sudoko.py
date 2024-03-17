# imports
import pygame
from box import square
from matrix import Matrix
from threading import Thread
from pygame_gui.elements import UIButton
from pygame_gui import UI_BUTTON_PRESSED,UIManager







clock = pygame.time.Clock()
# init
pygame.init()
#global params
WIDTH, HEIGHT = 540, 540
BACKGROUND_COLOR = 'white'
run = True
POS = 1
blocks = []
FOCUSED = None
grey = (160, 160, 160)

cond = False

# window
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(BACKGROUND_COLOR)
pygame.display.set_caption('Sudoku')

# input config
numbers = str(list(range(1, 10)))
keypad = [f'[{i}]' for i in numbers]

# sudoku object
sudoko = Matrix()

# grid
BLOCK_SIZE = 60
BLOCKS = [[square(window, (i*BLOCK_SIZE, j*BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE),
                  value=sudoko.sudoko[i, j]) for i in range(9)] for j in range(9)]


# return clicked position to index in the matrix


def pos_to_index(pos):
    return (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)


def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(window, 'black', (i*3*60, 0), (i*3*60, HEIGHT), (4))
        pygame.draw.line(window, 'black', (0, i*3*60), (WIDTH, i*3*60), (4))


def draw():
    # draw boxes
    for row in BLOCKS:
        for col in row:
            col.draw()
    # draw lines
    for i in range(1, 3):
        pygame.draw.line(window, 'black', (i*3*60, 0),
                         (i*3*60, HEIGHT), (4))
        pygame.draw.line(window, 'black', (0, i*3*60),
                         (WIDTH, i*3*60), (4))


def on_click_change(pos):

    # COLOR AND VALUE

    global FOCUSED, POS, grey, blocks
    if POS == -1:
        return
    POS = pos

    for block in blocks:
        if BLOCKS[block[0], block[1]].color != "white":
            BLOCKS[block[0], block[1]].color = "white"
    # try:
    #     if FOCUSED.box_color != "white":
    #         FOCUSED.box_color = "white"
    # except:
    #     pass

    index = pos_to_index(pos)
    # mouse gets position inversed
    FOCUSED = BLOCKS[index[1]][index[0]]
    blocks = sudoko.get_same_value(FOCUSED.value)
    if not len(blocks):

        FOCUSED.border_color = (100, 100, 100)

    else:
        for block in blocks:
            BLOCKS[block[0], block[1]].border_color = (100, 100, 100)

    #FOCUSED.border_color = (100, 100, 100)

    return

manager = UIManager((800, 600), 'data/themes/quick_theme.json')

hello_button = UIButton((350, 280), 'Hello')



# Threa
Threads = {"filling_Thread": {"Thread": Thread(
    target=sudoko.fill, args=[BLOCKS]), "status": 0}}

while (run):

    keys = pygame.key.get_pressed()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
            break
        # HANDLING INPUTS
        if event.type == pygame.KEYDOWN:
            # CLOSE
            if event.key == pygame.K_ESCAPE:
                run = False
                break
            # DELETE
            if event.key == pygame.K_BACKSPACE:
                if FOCUSED:
                    idx = pos_to_index(FOCUSED.position)
                    sudoko.set_value(idx, 0)
                    FOCUSED.value = 0
                    FOCUSED.box_color = grey
                    FOCUSED.wrong = 0
                    POS = 1 

            # INSERT
            pressed = pygame.key.name(event.key)
            if (pressed in numbers or pressed in keypad) & (POS != -1):
                if FOCUSED:
                    if len(pressed) > 1:
                        pressed = pressed[1]
                    pressed = int(pressed)
                    idx = pos_to_index(FOCUSED.position)
                    FOCUSED.value = pressed
                    sudoko.set_value(idx, pressed)
                    if not sudoko.check_value_valid(idx, pressed, FOCUSED):
                        POS = -1

            if (event.key == pygame.K_SPACE) and (not Threads["filling_Thread"]["status"]):
                Threads["filling_Thread"]["Thread"].start()
                Threads["filling_Thread"]["status"] = 1

    # movement
    if FOCUSED:
        if keys[pygame.K_RIGHT]:
            r, c = FOCUSED.position
            on_click_change((((r+BLOCK_SIZE) % 540), c))
        if keys[pygame.K_LEFT]:
            r, c = FOCUSED.position
            on_click_change((((r-BLOCK_SIZE) % 540), c))
        if keys[pygame.K_UP]: 
            r, c = FOCUSED.position
            on_click_change((r, ((c-BLOCK_SIZE) % 540)))
        if keys[pygame.K_DOWN]:
            r, c = FOCUSED.position
            on_click_change((r, ((c+BLOCK_SIZE) % 540)))

    # MOUSE
    if (pygame.mouse.get_pressed()[0]):

        on_click_change(pygame.mouse.get_pos())

    draw()
    clock.tick(60)
    pygame.display.update()


pygame.quit()
