import os
import sys

import pygame
import pygame_gui
import csv


pygame.init()

FPS = 30
SIZE = WIDTH, HEIGHT = 800, 600
SOUND_VOLUME = 0.75
CUR_SAVE = "save_1"
LEVEL_OPENED = 1

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Битва за Салонце")

clock = pygame.time.Clock()

manager = pygame_gui.UIManager(SIZE)


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
    pygame.mixer.music.load("data/sounds/menu.wav")
    pygame.mixer.music.set_volume(0.75)
    pygame.mixer.music.play(-1)

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
                    upload_game_menu("load")
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


def upload_game_menu(mode):
    global CUR_SAVE
    global LEVEL_OPENED

    bg = load_image("start_bg_without_logo.jpg")
    screen.blit(bg, (0, 0))

    load_1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 20), (300, 75)),
        text='Слот сохранения 1', manager=manager
    )
    load_2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 120), (300, 75)),
        text='Слот сохранения 2', manager=manager
    )
    load_3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 220), (300, 75)),
        text='Слот сохранения 3', manager=manager
    )
    load_4 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 320), (300, 75)),
        text='Слот сохранения 4', manager=manager
    )
    load_5 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 420), (300, 75)),
        text='Слот сохранения 5', manager=manager
    )
    load_6 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 20), (300, 75)),
        text='Слот сохранения 6', manager=manager
    )
    load_7 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 120), (300, 75)),
        text='Слот сохранения 7', manager=manager
    )
    load_8 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 220), (300, 75)),
        text='Слот сохранения 8', manager=manager
    )
    load_9 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 320), (300, 75)),
        text='Слот сохранения 9', manager=manager
    )
    load_10 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 420), (300, 75)),
        text='Слот сохранения 10', manager=manager
    )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((250, 520), (300, 60)),
        text='Вернуться в меню', manager=manager
    )
    elements = [load_1, load_2, load_3, load_4, load_5,
                load_6, load_7, load_8, load_9, load_10, exit_to_menu_btn]
    save_to_file = {load_1: 'save_1',
                    load_2: 'save_2',
                    load_3: 'save_3',
                    load_4: 'save_4',
                    load_5: 'save_5',
                    load_6: 'save_6',
                    load_7: 'save_7',
                    load_8: 'save_8',
                    load_9: 'save_9',
                    load_10: 'save_10'}
    temp_save = "save_1"
    while True:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in elements:
                    load_sound("button_clicked.mp3")
                    if event.ui_element != exit_to_menu_btn:
                        temp_save = save_to_file[event.ui_element]
                        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((250, 200), (300, 200)),
                            manager=manager,
                            window_title="Подтверждение",
                            action_long_desc=f"Загрузить сохранение {temp_save.split('_')[1]}?",
                            action_short_name='OK',
                            blocking=True
                        )
                if event.ui_element == exit_to_menu_btn:
                    kill_elements(elements)
                    return
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                if event.ui_element in elements:
                    load_sound("button_hover_2.mp3")
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                CUR_SAVE = temp_save
                with open(f'data/saves/{CUR_SAVE}.csv', encoding="utf8") as csvfile:
                    if mode == "load":
                        LEVEL_OPENED = list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1][1]
            manager.process_events(event)
        manager.update(time_delta)
        screen.blit(bg, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()


def select_level_menu():
    pass


def parameters():
    global SOUND_VOLUME

    bg = load_image("start_bg_without_logo.jpg")
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
    elements = [label_1, label_2, music_volume_scr_bar,
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
                    kill_elements(elements)
                    return
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                if event.ui_element == exit_to_menu_btn:
                    load_sound("button_hover_2.mp3")
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


def stat_menu():
    global CUR_SAVE

    bg = load_image("start_bg_without_logo.jpg")
    screen.blit(bg, (0, 0))

    with open(f'data/saves/{CUR_SAVE}.csv', encoding="utf8") as csvfile:
        settings = list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1:]
        label_level_opened = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((35, 35), (220, 50)),
            text=f"Пройденных уровней: {int(settings[0][1]) - 1}",
            manager=manager
        )
        label_killed_ships = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((290, 35), (220, 50)),
            text=f"Убитых кораблей: {settings[1][1]}",
            manager=manager
        )
        label_shots_value = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((545, 35), (220, 50)),
            text=f"Выстрелов сделано: {settings[2][1]}",
            manager=manager
        )
        label_accuracy = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((35, 120), (220, 50)),
            text=f"Точность: {settings[3][1]}%",
            manager=manager
        )
        label_bonus_value = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((290, 120), (220, 50)),
            text=f"Подобранных бонусов: {settings[4][1]}",
            manager=manager
        )
        label_points_value = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((545, 120), (220, 50)),
            text=f"Полученных очков: {settings[5][1]}",
            manager=manager
        )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 540), (250, 50)),
        text='Вернуться в меню',
        manager=manager
    )
    elements = [label_level_opened, label_killed_ships, label_shots_value,
                label_accuracy, label_bonus_value, label_points_value, exit_to_menu_btn]
    while True:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                load_sound("button_clicked.mp3")
                if event.ui_element == exit_to_menu_btn:
                    kill_elements(elements)
                    return
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                load_sound("button_hover_2.mp3")
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


start_menu()
terminate()
