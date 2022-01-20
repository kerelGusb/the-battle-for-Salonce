import sys

import pygame
import pygame_gui
import csv
import sqlite3
import random


from sprites import ALL_SPRITES, PLAYER_BULLET, ALIEN_SPRITES, HEARTS
from sprites import Background, MainCharacter, Enemy, Boss, MainCharBullet, Heart, Battery
from sprites import load_image


pygame.init()

con = sqlite3.connect("data/game_data.db")
cur = con.cursor()

SIZE = WIDTH, HEIGHT = 800, 600
MUSIC_VOLUME = SOUND_VOLUME = 0.5
CUR_SAVE = cur.execute("""SELECT save_index FROM game_saves WHERE is_running = 'True'""").fetchone()[0]
with open(f'data/saves/{CUR_SAVE}.csv', encoding="utf8") as csvfile:
    LEVEL_OPENED = int(list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1][1])
LEVEL_COMPLETED = LEVEL_OPENED - 1

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Битва за Салонце")

clock = pygame.time.Clock()

manager = pygame_gui.UIManager(SIZE)


def terminate():
    pygame.quit()
    sys.exit()


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
    textbox_1 = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((550, 329), (225, 150)),
        html_text="Управление:<br>Клавиши стрелок - перемещение<br>F - выстрел из пушки<br>ESC - пауза",
        manager=manager
    )
    textbox_2 = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((25, 329), (225, 150)),
        html_text=f"На Салонечную систему<br>напали захватчики,<br>и только вы "
                  f"можете их <br>остановить!",
        manager=manager
    )
    elements = [start_game_btn, upload_game_btn, stat_btn, settings_btn, exit_game_btn, textbox_1, textbox_2]
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
                    upload_game_menu()
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


def check_planet_open():
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
    planet_images = [pliton_im, teptune_im, buran_im, maturne_im, jupater_im,
                     mors_im, kemlya_im, veneda_im, merciry_im, salonce_im]
    return planet_images


def select_level_menu():
    global LEVEL_OPENED
    global LEVEL_COMPLETED

    bg = load_image("start_bg_without_logo.jpg")
    screen.blit(bg, (0, 0))

    planets = ["Плитон", "Тептун", "Буран", "Матурн", "Юпатер",
               "Морс", "Кемля", "Венеда", "Меркирий", "Салонце (финал)"]
    planet_images_coords = [(50, 50), (50, 200), (50, 350), (185, 50), (200, 200),
                            (200, 350), (350, 50), (350, 200), (350, 350), (515, 325)]
    choosen_planet = "Плитон"
    planet_choose = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=planets,
        starting_option=choosen_planet,
        relative_rect=pygame.Rect((500, 50), (200, 50)),
        manager=manager
    )
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
                    cur_choosen_planet = choosen_planet
                    do_next_level, do_return_to_menu, do_repeat_level = game_process(cur_choosen_planet, planets)
                    while not do_return_to_menu:
                        LEVEL_OPENED = LEVEL_COMPLETED + 1
                        if do_next_level:
                            cur_choosen_planet = planets[planets.index(cur_choosen_planet) + 1]
                            do_next_level, do_return_to_menu, do_repeat_level = \
                                game_process(cur_choosen_planet, planets)
                        elif do_repeat_level:
                            do_next_level, do_return_to_menu, do_repeat_level = \
                                game_process(cur_choosen_planet, planets)
                    LEVEL_OPENED = LEVEL_COMPLETED + 1

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

        planet_images = check_planet_open()

        cur_p_index = planets.index(choosen_planet)
        cur_p_image = planet_images[cur_p_index]
        cur_p_coords = planet_images_coords[cur_p_index]
        screen.blit(bg, (0, 0))
        draw_image_square(cur_p_image, cur_p_coords)
        draw_planets(planet_images, planet_images_coords)

        manager.draw_ui(screen)
        pygame.display.update()


def upload_game_menu():
    global CUR_SAVE
    global LEVEL_OPENED

    bg = load_image("start_bg_without_logo.jpg")
    screen.blit(bg, (0, 0))

    save_names = cur.execute("""SELECT save_name FROM game_saves""").fetchall()

    load_1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 20), (300, 75)),
        text=save_names[0][0], manager=manager
    )
    load_2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 120), (300, 75)),
        text=save_names[1][0], manager=manager
    )
    load_3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 220), (300, 75)),
        text=save_names[2][0], manager=manager
    )
    load_4 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 320), (300, 75)),
        text=save_names[3][0], manager=manager
    )
    load_5 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 420), (300, 75)),
        text=save_names[4][0], manager=manager
    )
    load_6 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 20), (300, 75)),
        text=save_names[5][0], manager=manager
    )
    load_7 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 120), (300, 75)),
        text=save_names[6][0], manager=manager
    )
    load_8 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 220), (300, 75)),
        text=save_names[7][0], manager=manager
    )
    load_9 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 320), (300, 75)),
        text=save_names[8][0], manager=manager
    )
    load_10 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 420), (300, 75)),
        text=save_names[9][0], manager=manager
    )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 515), (300, 65)),
        text='Вернуться в меню', manager=manager
    )
    label_1 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, 515), (300, 65)),
        text=f'Текущее сохранение: {CUR_SAVE.split("_")[1]}', manager=manager
    )
    elements = [load_1, load_2, load_3, load_4, load_5,
                load_6, load_7, load_8, load_9, load_10, exit_to_menu_btn, label_1]
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
    temp_save = CUR_SAVE
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
                cur.execute(f"""UPDATE game_saves SET is_running = 'False' WHERE save_index = '{CUR_SAVE}'""")
                CUR_SAVE = temp_save
                cur.execute(f"""UPDATE game_saves SET is_running = 'True' WHERE save_index = '{CUR_SAVE}'""")
                con.commit()
                with open(f'data/saves/{CUR_SAVE}.csv', encoding="utf8") as csvfile:
                    LEVEL_OPENED = int(list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1][1])
                label_1.set_text(f'Текущее сохранение: {CUR_SAVE.split("_")[1]}')
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
    global LEVEL_OPENED

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
            text=f"Точность: {int(float(settings[3][1]) * 100)}%",
            manager=manager
        )
        label_good_shots_value = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((70, 280), (295, 60)),
            text=f"Выстрелов попало: {settings[4][1]}",
            manager=manager
        )
        label_points_value = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((435, 280), (295, 60)),
            text=f"Очков получено: {settings[5][1]}",
            manager=manager
        )
    delete_save_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((245, 400), (310, 60)),
        text=f'Обнулить сохранение {CUR_SAVE.split("_")[1]}',
        manager=manager
    )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((245, 500), (310, 60)),
        text='Вернуться в меню',
        manager=manager
    )
    elements = [label_level_opened, label_killed_ships, label_shots_value,
                label_accuracy, label_good_shots_value, label_points_value, exit_to_menu_btn, delete_save_btn]
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
                if event.ui_element == delete_save_btn:
                    pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((250, 200), (300, 200)),
                        manager=manager,
                        window_title="Подтверждение",
                        action_long_desc=f"Обнулить сохранение {CUR_SAVE.split('_')[1]}?",
                        action_short_name='OK',
                        blocking=True
                    )
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                load_sound("button_hover_2.mp3")
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                with open(f'data/saves/{CUR_SAVE}.csv', 'w', newline='') as csvfile:
                    csvfile.truncate()
                    writer = csv.writer(
                        csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(['set_name', 'value'])
                    writer.writerow(['levels_opened', 1])
                    label_level_opened.set_text("Уровней пройдено: 0")
                    writer.writerow(['killed_ships', 0])
                    label_killed_ships.set_text("Кораблей убито: 0")
                    writer.writerow(['shots_value', 0])
                    label_shots_value.set_text("Выстрелов сделано: 0")
                    writer.writerow(['accuracy', 1])
                    label_accuracy.set_text("Точность: 100%")
                    writer.writerow(['good_shots_value', 0])
                    label_good_shots_value.set_text("Выстрелов попало: 0")
                    writer.writerow(['points_value', 0])
                    label_points_value.set_text("Очков получено: 0")
                    LEVEL_OPENED = 1
            manager.process_events(event)
        manager.update(time_delta)
        screen.blit(bg, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()


def game_process(level, planets):
    global LEVEL_COMPLETED
    load_music("battle.wav")
    # характеристики уровней: название файла фона, радиус выбора времени спавна врагов,
    # убитых врагов для появления босса, кол-во hp у врагов, кол-во hp у босса,
    # время на восстановление 1 заряда батареи
    level_parameters = {
                        "Плитон": ["pliton_bg.png", (1000, 3000), 10, 50, 500, 1000],
                        "Тептун": ["teptune_bg.png", (900, 2500), 12, 50, 600, 930],
                        "Буран": ["buran_bg.png", (800, 2000), 14, 50, 700, 860],
                        "Матурн": ["maturne_bg.png", (700, 1700), 16, 50, 800, 790],
                        "Юпатер": ["jupater_bg.png", (650, 1500), 18, 50, 900, 720],
                        "Морс": ["mors_bg.png", (600, 1300), 20, 100, 1000, 650],
                        "Кемля": ["kemlya_bg.png", (550, 1100), 22, 100, 1100, 580],
                        "Венеда": ["veneda_bg.png", (500, 1000), 24, 100, 1200, 510],
                        "Меркирий": ["merciry_bg.png", (450, 900), 26, 100, 1300, 440],
                        "Салонце (финал)": ["salonce_bg.png", (400, 800), 28, 100, 1500, 370]
                        }
    enemy_ic_elems = {"enemy_ic_loop_1_16.png": 16,
                      "enemy_ic_loop_2_6.png": 6,
                      "enemy_ic_loop_3_4.png": 4}
    cur_lvl_par = level_parameters[level]
    Background(load_image(cur_lvl_par[0]), ALL_SPRITES)
    main_char = MainCharacter("new_hero_ic_loop_hit_2.png", 4, 30, 255, 10, [102, 43], ALL_SPRITES)
    Heart(main_char, 0, (5, 5), ALL_SPRITES, HEARTS)
    Heart(main_char, 50, (40, 5), ALL_SPRITES, HEARTS)
    Heart(main_char, 100, (75, 5), ALL_SPRITES, HEARTS)
    bat = Battery(cur_lvl_par[5], (5, 541), ALL_SPRITES)
    enemies = []
    is_back_to_menu = False
    is_next_lvl = False
    is_repeat_lvl = False
    boss_arrived = False
    boss = None
    death_time = "вакашок"
    boss_death_time = "абалдуй"
    enemy_spawn_ticks = pygame.time.get_ticks()
    time_distance = random.randint(*cur_lvl_par[1])
    points = 0
    player_shots = 0
    player_good_shots = 0
    killed_enemies = 0
    while True:
        if is_next_lvl:
            for sprite in ALL_SPRITES.sprites():
                sprite.kill()
            return True, False, False
        if is_back_to_menu:
            for sprite in ALL_SPRITES.sprites():
                sprite.kill()
            return False, True, False
        if is_repeat_lvl:
            for sprite in ALL_SPRITES.sprites():
                sprite.kill()
            return False, False, True
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
                if event.key == pygame.K_f:
                    if bat.charge > 0:
                        load_sound("shot_sound.wav")
                        MainCharBullet("bullet_player.png", 4,
                                       *main_char.shot_bullet_pos, 15, ALL_SPRITES, PLAYER_BULLET)
                        player_shots += 1
                        bat.charge -= 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    main_char.move_to_up = False
                if event.key == pygame.K_DOWN:
                    main_char.move_to_down = False
                if event.key == pygame.K_LEFT:
                    main_char.move_to_left = False
                if event.key == pygame.K_RIGHT:
                    main_char.move_to_right = False
        if time_distance < (pygame.time.get_ticks() - enemy_spawn_ticks):
            rand_enemy_ic_name = random.choice(["enemy_ic_loop_1_16.png",
                                                "enemy_ic_loop_2_6.png",
                                                "enemy_ic_loop_3_4.png"])
            enemy_ic = load_image(rand_enemy_ic_name)
            enemy = Enemy(rand_enemy_ic_name, enemy_ic_elems[rand_enemy_ic_name], 800,
                          random.randint(0, 600 - enemy_ic.get_height()),
                          random.randint(8, 16), [-20, enemy_ic.get_height() // 2 - 2],
                          cur_lvl_par[3], ALL_SPRITES, ALIEN_SPRITES)
            enemies.append(enemy)
            time_distance = random.randint(*cur_lvl_par[1])
            enemy_spawn_ticks = pygame.time.get_ticks()
        alive_enemies = []
        for enemy in enemies:
            if not enemy.alive():
                if enemy.was_killed:
                    killed_enemies += 1
                    player_good_shots += enemy.got_shot
                    points += 100
            else:
                alive_enemies.append(enemy)
        enemies = alive_enemies
        if killed_enemies >= cur_lvl_par[2] and not boss_arrived:
            pass
            boss = Boss(planets.index(level) + 1, cur_lvl_par[4], ALL_SPRITES, ALIEN_SPRITES)
            boss_arrived = True
        if main_char.is_dead:
            if main_char.alive():
                main_char.kill()
                death_time = pygame.time.get_ticks()
            if death_time != "вакашок":
                if pygame.time.get_ticks() - death_time > 1250:
                    is_next_lvl, is_back_to_menu, is_repeat_lvl = game_end(level, False, points,
                                                                           player_shots, killed_enemies)
        if boss:
            if boss.is_dead:
                if boss.alive():
                    boss.kill()
                    boss_death_time = pygame.time.get_ticks()
                if boss_death_time != "абалдуй":
                    if pygame.time.get_ticks() - boss_death_time > 1250:
                        player_good_shots += boss.got_shot
                        if planets.index(level) == LEVEL_COMPLETED:
                            LEVEL_COMPLETED += 1
                        change_save(killed_enemies, player_shots, player_good_shots, points)
                        is_next_lvl, is_back_to_menu, is_repeat_lvl = game_end(level, True, points,
                                                                               player_shots, killed_enemies)
        ALL_SPRITES.draw(screen)
        ALL_SPRITES.update()
        pygame.display.update()


def change_save(killed_ships, shots_value, good_shots_value, points_value):
    data = []
    with open(f'data/saves/{CUR_SAVE}.csv', 'r', newline='') as csvfile:
        reader = list(csv.reader(csvfile, delimiter=';', quotechar='"'))[1:]
        for elem in reader:
            data.append(elem[1])
    with open(f'data/saves/{CUR_SAVE}.csv', 'w', newline='') as csvfile:
        csvfile.truncate()
        writer = csv.writer(
            csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['set_name', 'value'])
        writer.writerow(['levels_opened', LEVEL_COMPLETED + 1])
        writer.writerow(['killed_ships', killed_ships + int(data[1])])
        writer.writerow(['shots_value', shots_value + int(data[2])])
        writer.writerow(['accuracy', round((good_shots_value + float(data[4])) / (shots_value + float(data[2])), 2)])
        writer.writerow(['good_shots_value', good_shots_value + int(data[4])])
        writer.writerow(['points_value', points_value + int(data[5])])


def game_end(level, is_player_won,
             player_points, player_shots, killed_enemies):
    load_music("level_end.mp3")
    if is_player_won:
        bg = load_image("you_won_bg.png")
    else:
        bg = load_image("game_over_bg.png")
    screen.blit(bg, (0, 0))

    label_1 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((40, 175), (340, 90)),
        text=f"Убитых врагов: {killed_enemies}",
        manager=manager
    )
    label_2 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((40, 280), (340, 90)),
        text=f"Выстрелов сделано: {player_shots}",
        manager=manager
    )
    label_3 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((40, 385), (340, 90)),
        text=f"Получено очков: {player_points}",
        manager=manager
    )

    next_lvl_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((420, 175), (340, 90)),
        text="Следующий уровень", manager=manager
    )
    return_lvl_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((420, 175), (340, 90)),
        text="Повторить попытку", manager=manager
    )
    settings_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((420, 280), (340, 90)),
        text="Параметры", manager=manager
    )
    exit_to_lvls_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((420, 385), (340, 90)),
        text="Выйти в меню", manager=manager
    )
    if level == "Салонце (финал)":
        next_lvl_btn.disable()
    if is_player_won:
        return_lvl_btn.hide()
    else:
        next_lvl_btn.hide()
    elements = [label_1, label_2, label_3, next_lvl_btn,
                return_lvl_btn, settings_btn, exit_to_lvls_btn]
    while True:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                load_sound("button_hover_2.mp3")
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                load_sound("button_clicked.mp3")
                if event.ui_element == next_lvl_btn:  # перейти на след. уровень
                    kill_elements(elements)
                    return True, False, False
                if event.ui_element == return_lvl_btn:
                    kill_elements(elements)
                    return False, False, True
                if event.ui_element == settings_btn:
                    hide_elements(elements)
                    parameters()
                    show_elements(elements)
                if event.ui_element == exit_to_lvls_btn:  # перейти в меню
                    kill_elements(elements)
                    return False, True, False
            manager.process_events(event)
        manager.update(time_delta)
        screen.blit(bg, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()


def pause_menu():
    bg = load_image("pause_bg.jpg")
    screen.blit(bg, (0, 0))

    back_to_game_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((220, 175), (340, 90)),
        text="Вернуться в игру", manager=manager
    )
    settings_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((220, 280), (340, 90)),
        text="Параметры", manager=manager
    )
    exit_to_menu_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((220, 385), (340, 90)),
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
