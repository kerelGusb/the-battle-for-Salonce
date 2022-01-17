import os
import sys

import pygame
import pygame_gui
import csv
import sqlite3

from sprites import Background, MainCharacter

pygame.init()

SIZE = WIDTH, HEIGHT = 800, 600
MUSIC_VOLUME = SOUND_VOLUME = 0.5
CUR_SAVE = "save_1"
LEVEL_OPENED = 1

con = sqlite3.connect("data/game_data.db")
cur = con.cursor()

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


def load_music(name):
    pygame.mixer.music.load("data/sounds/" + name)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)


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
    load_music("menu.wav")

    screen.fill(pygame.Color("black"))
    start_bg = load_image("start_bg_2.jpg")
    screen.blit(start_bg, (0, 0))

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
    time_delta = clock.tick(60) / 1000
    while True:
        screen.blit(start_bg, (0, 0))
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
                screen.blit(start_bg, (0, 0))
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                load_sound("button_hover_2.mp3")
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


def draw_planets(images, sizes):
    screen.blit(images[0], sizes[0])
    screen.blit(images[1], sizes[1])
    screen.blit(images[2], sizes[2])
    screen.blit(images[3], sizes[3])
    screen.blit(images[4], sizes[4])
    screen.blit(images[5], sizes[5])
    screen.blit(images[6], sizes[6])
    screen.blit(images[7], sizes[7])
    screen.blit(images[8], sizes[8])
    screen.blit(images[9], sizes[9])


def draw_image_square(image, coords):
    square = pygame.Surface(tuple(map(lambda x: x + 4, image.get_size())))
    square.fill(pygame.Color("red"))
    new_coords = tuple(map(lambda x: x - 2, coords))
    screen.blit(square, new_coords)


def select_level_menu():
    global LEVEL_OPENED

    bg = load_image("start_bg_without_logo.jpg")
    screen.blit(bg, (0, 0))
    pliton_im = load_image("pliton.png")
    if LEVEL_OPENED > 1:
        teptune_im = load_image("Teptune.png")
    else:
        teptune_im = load_image("Teptune_locked.png")
    if LEVEL_OPENED > 2:
        buran_im = load_image("Buran.png")
    else:
        buran_im = load_image("Buran_locked.png")
    if LEVEL_OPENED > 3:
        maturne_im = load_image("Maturne.png")
    else:
        maturne_im = load_image("Maturne_locked.png")
    if LEVEL_OPENED > 4:
        jupater_im = load_image("Jupater.png")
    else:
        jupater_im = load_image("Jupater_locked.png")
    if LEVEL_OPENED > 5:
        mors_im = load_image("mors.png")
    else:
        mors_im = load_image("mors_locked.png")
    if LEVEL_OPENED > 6:
        kemlya_im = load_image("Kemlya.png")
    else:
        kemlya_im = load_image("Kemlya_locked.png")
    if LEVEL_OPENED > 7:
        veneda_im = load_image("veneda.png")
    else:
        veneda_im = load_image("veneda_locked.png")
    if LEVEL_OPENED > 8:
        merciry_im = load_image("merciry.png")
    else:
        merciry_im = load_image("merciry_locked.png")
    if LEVEL_OPENED > 9:
        salonce_im = load_image("salonce.png")
    else:
        salonce_im = load_image("salonce_locked.png")

    planets = ["Плитон", "Тептун", "Буран", "Матурн", "Юпатер",
               "Морс", "Кемля", "Венеда", "Меркирий", "Салонце (финал)"]
    planet_images = [pliton_im, teptune_im, buran_im, maturne_im, jupater_im,
                     mors_im, kemlya_im, veneda_im, merciry_im, salonce_im]
    planet_images_coords = [(50, 50), (50, 200), (50, 350), (185, 50), (200, 200),
                            (200, 350), (350, 50), (350, 200), (350, 350), (515, 325)]

    planet_choose = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=planets,
        starting_option=planets[LEVEL_OPENED - 1],
        relative_rect=pygame.Rect((500, 50), (200, 50)),
        manager=manager
    )
    choosen_planet = "Плитон"
    start_level = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((60, 500), (310, 60)),
        text='Запустить уровень',
        manager=manager
    )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((430, 500), (310, 60)),
        text='Вернуться в меню',
        manager=manager
    )
    elements = [start_level, planet_choose, exit_to_menu_btn]

    time_delta = clock.tick(60) / 1000
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                load_sound("button_clicked.mp3")
                if event.ui_element == exit_to_menu_btn:
                    kill_elements(elements)
                    return
                if event.ui_element == start_level:
                    hide_elements(elements)
                    game_process(choosen_planet)
                    load_music("menu.wav")
                    show_elements(elements)
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                load_sound("button_hover_2.mp3")
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                choosen_planet = event.text
                if planets.index(choosen_planet) <= LEVEL_OPENED - 1:
                    start_level.enable()
                else:
                    start_level.disable()
            manager.process_events(event)
        manager.update(time_delta)

        cur_p_index = planets.index(choosen_planet)
        cur_p_image = planet_images[cur_p_index]
        cur_p_coords = planet_images_coords[cur_p_index]
        screen.blit(bg, (0, 0))
        draw_image_square(cur_p_image, cur_p_coords)
        draw_planets(planet_images, planet_images_coords)

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
    time_delta = clock.tick(60) / 1000
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                load_sound("button_clicked.mp3")
                if event.ui_element in elements:
                    if event.ui_element != exit_to_menu_btn:
                        temp_save = save_to_file[event.ui_element]
                        pygame_gui.windows.UIConfirmationDialog(
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
                        LEVEL_OPENED = int(list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1][1])
            manager.process_events(event)
        manager.update(time_delta)
        screen.blit(bg, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()


def parameters():
    global MUSIC_VOLUME
    global SOUND_VOLUME

    bg = load_image("start_bg_without_logo.jpg")
    screen.blit(bg, (0, 0))
    label_1 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((60, 25), (310, 50)),
        text="Громкость музыки:",
        manager=manager
    )
    label_2 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((60, 105), (310, 50)),
        text="Громкость звуков:",
        manager=manager
    )
    music_volume_scr_bar = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((430, 25), (310, 50)),
        start_value=pygame.mixer.music.get_volume() * 100,
        value_range=(0, 100),
        click_increment=2,
        manager=manager
    )
    sound_volume_scr_bar = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((430, 105), (310, 50)),
        start_value=SOUND_VOLUME * 100,
        value_range=(0, 100),
        click_increment=2,
        manager=manager
    )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((245, 185), (310, 60)),
        text='Вернуться в меню',
        manager=manager
    )
    elements = [label_1, label_2, music_volume_scr_bar,
                sound_volume_scr_bar, exit_to_menu_btn]
    time_delta = clock.tick(60) / 1000
    while True:
        MUSIC_VOLUME = music_volume_scr_bar.get_current_value() / 100
        SOUND_VOLUME = sound_volume_scr_bar.get_current_value() / 100
        pygame.mixer.music.set_volume(MUSIC_VOLUME)

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
        screen.blit(bg, (0, 0))
        clock.tick(30)
        manager.draw_ui(screen)
        pygame.display.update()


def stat_menu():
    global CUR_SAVE

    bg = load_image("start_bg_without_logo.jpg")
    screen.blit(bg, (0, 0))

    with open(f'data/saves/{CUR_SAVE}.csv', encoding="utf8") as csvfile:
        settings = list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1:]
        label_level_opened = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((70, 40), (295, 60)),
            text=f"Уровней пройдено: {int(settings[0][1]) - 1}",
            manager=manager
        )
        label_killed_ships = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((435, 40), (295, 60)),
            text=f"Кораблей убито: {settings[1][1]}",
            manager=manager
        )
        label_shots_value = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((70, 160), (295, 60)),
            text=f"Выстрелов сделано: {settings[2][1]}",
            manager=manager
        )
        label_accuracy = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((435, 160), (295, 60)),
            text=f"Точность: {settings[3][1]}%",
            manager=manager
        )
        label_bonus_value = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((70, 280), (295, 60)),
            text=f"Бонусов активировано: {settings[4][1]}",
            manager=manager
        )
        label_points_value = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((435, 280), (295, 60)),
            text=f"Очков получено: {settings[5][1]}",
            manager=manager
        )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((245, 500), (310, 60)),
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


def game_process(level):
    load_music("battle.wav")
    level_to_bg = {"Плитон": "pliton_bg.png",
                   "Тептун": "teptune_bg.png",
                   "Буран": "buran_bg.png",
                   "Матурн": "maturne_bg.png",
                   "Юпатер": "jupater_bg.png",
                   "Морс": "mors_bg.png",
                   "Кемля": "kemlya_bg.png",
                   "Венеда": "veneda_bg.png",
                   "Меркирий": "merciry_bg.png",
                   "Салонце (финал)": "salonce_bg.png"}
    all_sprites = pygame.sprite.Group()
    Background(load_image(level_to_bg[level]), all_sprites)
    main_char = MainCharacter(load_image("new_hero_ic_loop.png"), 4, 30, 255, 8, all_sprites)
    is_back_to_menu = False
    while True:
        if is_back_to_menu:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    main_char.move_to_up = True
                if event.key == pygame.K_DOWN:
                    main_char.move_to_down = True
                if event.key == pygame.K_LEFT:
                    main_char.move_to_left = True
                if event.key == pygame.K_RIGHT:
                    main_char.move_to_right = True
                if event.key == pygame.K_ESCAPE:
                    is_back_to_menu = pause_menu()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    main_char.move_to_up = False
                if event.key == pygame.K_DOWN:
                    main_char.move_to_down = False
                if event.key == pygame.K_LEFT:
                    main_char.move_to_left = False
                if event.key == pygame.K_RIGHT:
                    main_char.move_to_right = False
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.update()


def pause_menu():
    bg = load_image("start_bg_without_logo.jpg")
    screen.blit(bg, (0, 0))

    back_to_game_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((250, 160), (300, 80)),
        text="Вернуться в игру", manager=manager
    )
    settings_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((250, 255), (300, 80)),
        text="Параметры", manager=manager
    )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((250, 350), (300, 80)),
        text="Выйти в меню", manager=manager
    )
    elements = [back_to_game_btn, settings_btn, exit_to_menu_btn]
    while True:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                load_sound("button_hover_2.mp3")
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                load_sound("button_clicked.mp3")
                if event.ui_element == back_to_game_btn:
                    kill_elements(elements)
                    return False
                if event.ui_element == settings_btn:
                    hide_elements(elements)
                    parameters()
                    show_elements(elements)
                if event.ui_element == exit_to_menu_btn:
                    kill_elements(elements)
                    return True
            manager.process_events(event)
        manager.update(time_delta)
        screen.blit(bg, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()


if __name__ == "__main__":
    start_menu()
    terminate()
