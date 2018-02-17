import cv2
from base64 import b64decode
import numpy as np
import pickle
from skimage.measure import compare_ssim as ssim
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from Board import Board
from unscrabble import legal_plays
from lexicon import lexicon


def get_rack(driver):
    try:
        letter_img_div = driver.find_element_by_id('wwf-letters')
    except NoSuchElementException:
        wait_and_switch_frame('_2u_i', driver)
        letter_img_div = driver.find_element_by_id('wwf-letters')
    letter_images = letter_img_div.find_elements_by_tag_name('a')
    img_b64 = [im.find_element_by_xpath('./span/span')
                 .value_of_css_property('background-image')
                 .split(',')[1][:-2]
               for im in letter_images if im.is_displayed()]
    with open('rack.pkl', 'rb') as f:
        rack_dict = pickle.load(f)
    return ''.join([rack_dict[b64] for b64 in img_b64])


def best_match(tile, tile_dict):
    ssimD = {k: ssim(tile, v) for k, v in tile_dict.items()}
    return max(ssimD, key=ssimD.get)


def wait_and_switch_frame(my_class, driver):
    wait = WebDriverWait(driver, 15)
    ready = EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME,
                                                       my_class))
    wait.until(ready)


def b64tocv2(stro):
    # https://stackoverflow.com/questions/33754935
    nparr = np.fromstring(b64decode(stro), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def canvas_b64(driver):
    canvas = driver.find_element_by_id('wwf-renderer-canvas')
    js = 'return arguments[0].toDataURL(\'image/png\').substring(21);'
    return driver.execute_script(js, canvas)


def get_board(driver):
    def split():
        imgwidth = im.shape[0]
        tile_size = int(imgwidth / 11)
        return [[im[y * tile_size: (y + 1) * tile_size,
                 x * tile_size: (x + 1) * tile_size]
                for x in range(0, 11)]
                for y in range(0, 11)]
    im = b64tocv2(canvas_b64(driver))
    tiles = split()
    tiles = [[tile[5: tile.shape[1] - 5, 5: tile.shape[0] - 5] for tile in row]
             for row in tiles]
    bc = []
    for row in tiles:
        bc_row = []
        for image in row:
            image[np.where((image == [255, 255, 255]).all(axis=2))] = [0, 0, 0]
            top_right = image[3:22, image.shape[0] - 20:image.shape[0]]
            black = np.array([0, 0, 0])
            light_black = np.array([20, 30, 60])
            in_black = cv2.inRange(top_right, black, light_black)
            black_count = cv2.countNonZero(in_black)
            bc_row.append(black_count)
        bc.append(bc_row)

    tiles = [[cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) for im in row]
             for row in tiles]

    with open('lookup.pkl', 'rb') as f:
        tile_dict = pickle.load(f)

    board_string = [[best_match(tile, tile_dict) for tile in row]
                    for row in tiles]
    for i, row in enumerate(board_string):
        for j, key in enumerate(row):
            if bc[i][j] < 8 and key not in ('TL', 'DL', 'DW', 'TW', '_', 'CE'):
                board_string[i][j] = key + '.'
    print_board = [['|{}|'.format(t) if len(t) == 2
                    else '|{} |'.format(t)
                   for t in row]
                   for row in board_string]
    for row in print_board:
        print(' '.join(row) + '\n')
    return board_string


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    chro = webdriver.Chrome(chrome_options=options)
    chro.maximize_window()
    chro.get('https://www.messenger.com/')
    input('Press enter when it\'s your turn')
    wait_and_switch_frame('_2u_i', chro)

    with open('board.txt', 'r') as f:
        if canvas_b64(chro) == f.read():
            rack = get_rack(chro)
            board = Board(get_board(chro))
            all_plays = legal_plays(board, rack, lexicon)
            print('Top ten plays: ', all_plays[0:10])
            best_play = all_plays[0:1]
            print('\n', 'BEST PLAY:', best_play, '\n')
            input('Press enter when it\'s your turn')

    while True:
        rack = get_rack(chro)
        print(rack)
        board = Board(get_board(chro))
        all_plays = legal_plays(board, rack, lexicon)
        print('Top ten plays: ', all_plays[0:10])
        best_play = all_plays[0:1]
        print('\n', 'BEST PLAY:', best_play, '\n')
        input('Press enter when it\'s your turn')
