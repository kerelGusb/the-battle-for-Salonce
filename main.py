import os
import sys

import pygame
import pygame_gui

from select_lvl import select_level_menu


pygame.init()

FPS = 30
SIZE = WIDTH, HEIGHT = 800, 600
COLOR = "black"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Битва за Салонце")

clock = pygame.time.Clock()

manager = pygame_gui.UIManager(SIZE)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def start_menu():
    screen.fill(pygame.Color("black"))
    start_logo = load_image("start_bg.jpg")
    screen.blit(start_logo, (0, 0))
    start_game_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 275), (250, 50)),
        text='Начать игру',
        manager=manager
    )
    upload_game_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 327), (250, 50)),
        text='Загрузить игру',
        manager=manager
    )
    stat_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 379), (250, 50)),
        text='Статистика',
        manager=manager
    )
    settings_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 431), (250, 50)),
        text='Параметры',
        manager=manager
    )
    exit_game_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 483), (250, 50)),
        text='Выйти из игры',
        manager=manager
    )
    while True:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_game_btn:
                    select_level_menu()
                elif event.ui_element == upload_game_btn:
                    upload_game_menu()
                elif event.ui_element == stat_btn:
                    stat_menu()
                elif event.ui_element == settings_btn:
                    parameters()
                elif event.ui_element == exit_game_btn:
                    terminate()
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


def upload_game_menu():
    pass


def parameters():
    pass


def stat_menu():
    pass


start_menu()
terminate()
