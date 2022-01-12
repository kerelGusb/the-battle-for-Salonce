import os
import sys

import pygame
import pygame_gui

from select_lvl import select_level_menu


pygame.init()

FPS = 30
SIZE = WIDTH, HEIGHT = 800, 600
COLOR = "black"
SOUND_VOLUME = 0.75
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Битва за Салонце")

clock = pygame.time.Clock()

manager = pygame_gui.UIManager(SIZE)

pygame.mixer.music.load("data/sounds/menu.wav")
pygame.mixer.music.set_volume(0.75)
pygame.mixer.music.play(-1)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data/images', name)
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


def load_sound(name):
    sound = pygame.mixer.Sound("data/sounds/" + name)
    sound.play()
    sound.set_volume(SOUND_VOLUME)


def hide_elements(elems):
    for elem in elems:
        elem.hide()


def show_elements(elems):
    for elem in elems:
        elem.show()


def kill_elements(elems):
    for elem in elems:
        elem.hide()
        elem.kill()


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
    elements = [start_game_btn, upload_game_btn, stat_btn, settings_btn, exit_game_btn]
    while True:
        screen.blit(start_logo, (0, 0))
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                load_sound("button_clicked.mp3")
                hide_elements(elements)
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
                show_elements(elements)
                screen.blit(start_logo, (0, 0))
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                load_sound("button_hover_2.mp3")
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


def upload_game_menu():
    pass


def parameters():
    global SOUND_VOLUME

    bg = load_image("start_bg_without_logo.jpg")
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    label_1 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((25, 25), (250, 50)),
        text="Громкость музыки:",
        manager=manager
    )
    label_2 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((25, 80), (250, 50)),
        text="Громкость звуков:",
        manager=manager
    )
    music_volume_scr_bar = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((280, 25), (250, 50)),
        start_value=pygame.mixer.music.get_volume() * 100,
        value_range=(0, 100),
        click_increment=5,
        manager=manager
    )
    sound_volume_scr_bar = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((280, 80), (250, 50)),
        start_value=SOUND_VOLUME * 100,
        value_range=(0, 100),
        click_increment=5,
        manager=manager
    )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 540), (250, 50)),
        text='Вернуться в меню',
        manager=manager
    )
    settings_elements = [label_1, label_2, music_volume_scr_bar,
                         sound_volume_scr_bar, exit_to_menu_btn]
    while True:
        music_volume = music_volume_scr_bar.get_current_value()
        SOUND_VOLUME = sound_volume_scr_bar.get_current_value() / 100
        pygame.mixer.music.set_volume(music_volume / 100)

        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_to_menu_btn:
                    load_sound("button_clicked.mp3")
                    kill_elements(settings_elements)
                    return
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                if event.ui_element == exit_to_menu_btn:
                    load_sound("button_hover_2.mp3")
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


def stat_menu():
    pass


start_menu()
terminate()
