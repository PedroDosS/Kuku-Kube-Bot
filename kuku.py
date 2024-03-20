from PIL import ImageGrab
from PIL import Image
import pyautogui
import mouse
import time
import sys

pyautogui.FAILSAFE = False

# This is the coordinates of the game screen. They are (x1, y1, x2, y2) of the top-left and bottom-right corners of the board
game_screen = (708, 290, 1211, 789)

# These is the location of the start and play again buttons on the screen
start_pos = (850, 250)
reset_pos = (950, 550)

# These are the sizes of the boards. i.e., The first board is 2x2, the second 3x3, the third 4x4, etc
# After the 16th board, they are always 9x9
board_size = [2, 3, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 8]

click_count = 0

# Finds the differently colored pixel and clicks it
def click_pixel():

    global click_count

    # Takes a screenshot and loads it
    im = ImageGrab.grab(bbox = game_screen)
    im_width, im_height = im.size
    pixels = im.load()

    board_size = calc_board_size()

    tile_size = im.width / board_size

    # Finds the color of each tile
    colors = []
    for j in range(board_size):
        for i in range(board_size):
            tile_x, tile_y = get_tile_pos(i, j, tile_size)
            colors.append(pixels[tile_x - game_screen[0], tile_y - game_screen [1]])


    if not (colors[0] == colors[1]): # If the first two colors don't match, one of them must be the different one
        if colors[0] == colors[2]: # If tile 0 is the same as tile 2, it must be that tile 1 is different
            click(get_tile_pos(1, 0, tile_size))
        else: # Otherwise, it is tile 1 that's different
            click(get_tile_pos(0, 0, tile_size))
    else:
        for i in range(pow(board_size,2)): # Looks through the colors, clicks the different one
            if not(colors[i] == colors[0]):

                x = i % board_size
                y = i // board_size

                click(get_tile_pos(x, y, tile_size))

                break;

    click_count += 1


# Clicks a coordinate on the screen
def click(pos):
    pyautogui.mouseDown(x = pos[0], y = pos[1], _pause = False)
    pyautogui.mouseUp()

# Finds the screen position of a tile
def get_tile_pos(x, y, tile_size):
    half_tile_size = tile_size / 2
    return ((x * tile_size) + half_tile_size + game_screen[0], (y * tile_size) + half_tile_size + game_screen[1])

# Returns the size of the board
# The boards are NxN, where N is 2, 3, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 8
# After the 16th board, the following are all 9x9
def calc_board_size():
    global click_count

    if click_count < len(board_size):
        return board_size[click_count]
    else:
        return 9

# Detects if the game has already been played. If so, it hits the reset button. Otherwise, it hits the start button
if ImageGrab.grab(bbox = game_screen).load()[0, 0] == (167, 67, 67): # (167, 67, 67) is the color of the end screen
    click(reset_pos)
else:
    click(start_pos)

time_start = time.time()
time_now = time.time()

# The program will automatically stop after 65 seconds
# You can also hold the right mouse button to exit
while not mouse.is_pressed(button='right'):
    click_pixel()

    print((time.time() - time_now) * 1000)
    time_now = time.time()

    # Automatically stops the program after 65 seconds
    if time.time() - time_start > 65:
        break




