import sys
import time
from enum import Enum
import pygame
from pygame.locals import *
from Board import *


SCREEN_WIDTH = BLOCK_WIDTH * SIZE
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE


class GameStatus(Enum):
    readied = 1,
    started = 2,
    over = 3,
    win = 4


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Mine Sweeper')

    font = pygame.font.Font('resources/a.TTF', SIZE * 2)  # 得分的字体
    fwidth, fheight = font.size('999')
    font_color = (40, 40, 200)

    img0 = pygame.image.load('resources/0.bmp').convert()
    img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
    img1 = pygame.image.load('resources/1.bmp').convert()
    img1 = pygame.transform.smoothscale(img1, (SIZE, SIZE))
    img2 = pygame.image.load('resources/2.bmp').convert()
    img2 = pygame.transform.smoothscale(img2, (SIZE, SIZE))
    img3 = pygame.image.load('resources/3.bmp').convert()
    img3 = pygame.transform.smoothscale(img3, (SIZE, SIZE))
    img4 = pygame.image.load('resources/4.bmp').convert()
    img4 = pygame.transform.smoothscale(img4, (SIZE, SIZE))
    img5 = pygame.image.load('resources/5.bmp').convert()
    img5 = pygame.transform.smoothscale(img5, (SIZE, SIZE))
    img6 = pygame.image.load('resources/6.bmp').convert()
    img6 = pygame.transform.smoothscale(img6, (SIZE, SIZE))
    img7 = pygame.image.load('resources/7.bmp').convert()
    img7 = pygame.transform.smoothscale(img7, (SIZE, SIZE))
    img8 = pygame.image.load('resources/8.bmp').convert()
    img8 = pygame.transform.smoothscale(img8, (SIZE, SIZE))
    img_blank = pygame.image.load('resources/blank.bmp').convert()
    img_blank = pygame.transform.smoothscale(img_blank, (SIZE, SIZE))
    img_flag = pygame.image.load('resources/flag.bmp').convert()
    img_flag = pygame.transform.smoothscale(img_flag, (SIZE, SIZE))
    img_ask = pygame.image.load('resources/ask.bmp').convert()
    img_ask = pygame.transform.smoothscale(img_ask, (SIZE, SIZE))
    img_mine = pygame.image.load('resources/mine.bmp').convert()
    img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
    img_blood = pygame.image.load('resources/blood.bmp').convert()
    img_blood = pygame.transform.smoothscale(img_blood, (SIZE, SIZE))
    img_error = pygame.image.load('resources/error.bmp').convert()
    img_error = pygame.transform.smoothscale(img_error, (SIZE, SIZE))
    face_size = int(SIZE * 1.25)
    img_face_fail = pygame.image.load('resources/face_fail.bmp').convert()
    img_face_fail = pygame.transform.smoothscale(img_face_fail, (face_size, face_size))
    img_face_normal = pygame.image.load('resources/face_normal.bmp').convert()
    img_face_normal = pygame.transform.smoothscale(img_face_normal, (face_size, face_size))
    img_face_success = pygame.image.load('resources/face_success.bmp').convert()
    img_face_success = pygame.transform.smoothscale(img_face_success, (face_size, face_size))
    face_pos_x = (SCREEN_WIDTH - face_size) // 2
    face_pos_y = (SIZE * 2 - face_size) // 2

    img_dict = {
        0: img0,
        1: img1,
        2: img2,
        3: img3,
        4: img4,
        5: img5,
        6: img6,
        7: img7,
        8: img8
    }

    bg_color = (225, 225, 225)

    block = MineCell()
    game_status = GameStatus.readied
    start_time = None   # 开始时间
    elapsed_time = 0    # 耗时

    while True:
        screen.fill(bg_color)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2
                b1, b2, b3 = pygame.mouse.get_pressed()
                if game_status == GameStatus.started:
                    if b1 and b3:
                        mine = block.get_mine(x, y)
                        if mine.status == CellStatus.clicked:
                            if not block.double_mouse_button_down(x, y):
                                game_status = GameStatus.over
            elif event.type == MOUSEBUTTONUP:
                if face_pos_x <= mouse_x <= face_pos_x + face_size \
                        and face_pos_y <= mouse_y <= face_pos_y + face_size:
                    game_status = GameStatus.readied
                    block = MineCell()
                    start_time = time.time()
                    elapsed_time = 0
                    continue

                if game_status == GameStatus.readied:
                    game_status = GameStatus.started
                    start_time = time.time()
                    elapsed_time = 0

                if game_status == GameStatus.started:
                    if x < 0 or y < 0:
                        continue
                    mine = block.get_mine(x, y)
                    if b1 and not b3:       # 按鼠标左键
                        if mine.status == CellStatus.normal:
                            if not block.open_mine(x, y):
                                game_status = GameStatus.over
                    elif not b1 and b3:     # 按鼠标右键
                        if mine.status == CellStatus.normal:
                            mine.status = CellStatus.flag
                        elif mine.status == CellStatus.flag:
                            mine.status = CellStatus.ask
                        elif mine.status == CellStatus.ask:
                            mine.status = CellStatus.normal
                    elif b1 and b3:
                        if mine.status == CellStatus.double:
                            block.double_mouse_button_up(x, y)

        flag_count = 0
        opened_count = 0

        for row in block.cell:
            for mine in row:
                pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                if mine.status == CellStatus.clicked:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                    opened_count += 1
                elif mine.status == CellStatus.double:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                elif mine.status == CellStatus.bomb:
                    screen.blit(img_blood, pos)
                elif mine.status == CellStatus.flag:
                    screen.blit(img_flag, pos)
                    flag_count += 1
                elif mine.status == CellStatus.ask:
                    screen.blit(img_ask, pos)
                elif mine.status == CellStatus.hint:
                    screen.blit(img0, pos)
                elif game_status == GameStatus.over and mine.value:
                    screen.blit(img_mine, pos)
                elif mine.value == 0 and mine.status == CellStatus.flag:
                    screen.blit(img_error, pos)
                elif mine.status == CellStatus.normal:
                    screen.blit(img_blank, pos)

        print_text(screen, font, 30, (SIZE * 2 - fheight) // 2 - 2, '%02d' % (MINE_COUNT - flag_count), font_color)
        if game_status == GameStatus.started:
            elapsed_time = int(time.time() - start_time)
        print_text(screen, font, SCREEN_WIDTH - fwidth - 30,
                   (SIZE * 2 - fheight) // 2 - 2, '%03d' % elapsed_time, font_color)

        if flag_count + opened_count == BLOCK_WIDTH * BLOCK_HEIGHT:
            game_status = GameStatus.win

        if game_status == GameStatus.over:
            screen.blit(img_face_fail, (face_pos_x, face_pos_y))
        elif game_status == GameStatus.win:
            screen.blit(img_face_success, (face_pos_x, face_pos_y))
        else:
            screen.blit(img_face_normal, (face_pos_x, face_pos_y))

        pygame.display.update()


if __name__ == '__main__':
    main()
