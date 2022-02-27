"""module codé par Bastien (@BLASTUHQ) TG5, contenant des fonctions pour
les menus du jeu Tetris. Repassage du code par Solène, (@periergeia)."""


import pygame
try:
    from constant import LANG, COLOR
    from diego import GameStrings, post_request
    from gameplay import gameplay
    from solene import RadioButton
    from useful import get_font_size, loop_starter_pack, Button, Button2, Text
except ModuleNotFoundError:
    from modules.constant import LANG, COLOR
    from modules.diego import GameStrings, post_request
    from modules.gameplay import gameplay
    from modules.solene import RadioButton
    from modules.useful import get_font_size, loop_starter_pack, Button, Button2, Text


game_strings = GameStrings(LANG)


def create_main_menu(window):
    logo = pygame.image.load('./image/logo.jpg').convert_alpha()
    logo_height = window.get_height() // 4
    logo_size = (round(340 * logo_height / 153), logo_height)
    logo_to_display = pygame.transform.scale(logo, logo_size)
    logo_pos = (window.get_width() - logo_size[0]) // 2, round(window.get_height() * 0.15)

    window_w = window.get_width()
    
    play_button = Button(window, (logo_pos[0] / window_w,
                         0.45, logo_size[0] / window_w, 0.15), game_strings.get_string("play"))
    ranking_button = Button(window,
                            (logo_pos[0] / window_w,
                             0.65,
                             (logo_size[0] / window_w) * 0.65,
                             0.15),
                            game_strings.get_string("leaderboard"))
    help_button = Button(window,
                         (logo_pos[0] / window_w + (logo_size[0] / window_w) * 0.65,
                          0.65,
                          (logo_size[0] / window_w) * 0.35,
                          0.15),
                         game_strings.get_string("help"))
    
    frame = pygame.Surface(window.get_size())
    frame.blit(logo_to_display, (logo_pos))
    play_button.draw(frame)
    help_button.draw(frame)
    ranking_button.draw(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()
    return play_button, ranking_button, help_button


def main_menu(window):
    play_button, ranking_button, help_button = create_main_menu(window)
    # évènements pygame
    proceed = True
    while proceed:
        for event in pygame.event.get():
            loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                play_button, ranking_button, help_button = create_main_menu(window)
            if play_button.is_pressed(event):
                game_choice_menu(window)
                proceed = False
                return
            if ranking_button.is_pressed(event):
                leaderboard_menu(window, 1)
                proceed = False
                return
            if help_button.is_pressed(event):
                # menuplay()
                proceed = False
                return


def create_mode(window):
    mode_a = Button(window,
                            (0.175,
                             0.2,
                             0.3,
                             0.6),
                             '',
                            (100, 100, 100))
    mode_b = Button(window,
                           (0.525,
                            0.2,
                            0.3,
                            0.6),
                            '',
                           (100, 100, 100))
    mode = RadioButton((mode_a, mode_b))
    level_button_list = []
    y_value = 0.35
    for i in range(2):
        x_value = 0.15
        for j in range(5):
            button = Button(mode_b,
                           (x_value,
                            y_value,
                            0.14,  # 1/7
                            0.1),
                            str(i * 5 + j),
                           (110, 110, 110))
            level_button_list.append(button)
            x_value += 0.14
        y_value += 0.1
    hight_button_list = []
    y_value = 0.7
    for i in range(2):
        x_value = 0.15
        for j in range(3):
            button = Button(mode_b,
                           (x_value,
                            y_value,
                            0.23,  # 7/30
                            0.1),
                            str(i * 3 + j),
                           (110, 110, 110))
            hight_button_list.append(button)
            x_value += 0.23
        y_value += 0.1
    b_mode_option = (RadioButton(tuple(level_button_list)),
                     RadioButton(tuple(hight_button_list)))
    plus_button = Button(mode_a,
                            (0.65,
                             0.5,
                             0.2,
                             0.1),
                             '+',
                            (120, 120, 120))
    less_button = Button(mode_a,
                           (0.65,
                            0.7,
                            0.2,
                            0.1),
                            '-',
                           (120, 120, 120))
    a_mode = [1, plus_button, less_button]
    return mode, b_mode_option, a_mode


def create_surface(window, mode):
    surface = pygame.Surface(window.get_size())
    statement_1 = Text(window,
                     (0.175,
                      0.05,
                      0.65,
                      0.15),
                     game_strings.get_string("select_mode"))
    statement_2 = Text(window,
                     (0,
                      0.85,
                      1,
                      0.1),
                     game_strings.get_string("enter_game"))
    statement_a = Text(mode.button_list[0],
                     (0,
                      0.3,
                      1,
                      0.15),
                     game_strings.get_string("a_mode_statement"))
    mode_a_text = Text(mode.button_list[0],
                     (0,
                      0.08,
                      1,
                      0.25),
                     game_strings.get_string("mode_a"))
    mode_b_text = Text(mode.button_list[1],
                     (0,
                      0.08,
                      1,
                      0.25),
                     game_strings.get_string("mode_b"))
    level = Text(mode.button_list[1],
                     (0.15,
                      0.25,
                      1,
                      0.1),
                     game_strings.get_string("level"),
                     True)
    hight = Text(mode.button_list[1],
                     (0.15,
                      0.6,
                      1,
                      0.1),
                     game_strings.get_string("difficulty"),
                     True)
    previous_menu_button = Button2(window, (0.9, 0.05, 0.04), 'back')
    statement_1.draw(surface)
    statement_2.draw(surface)
    statement_a.draw(surface)
    mode_a_text.draw(surface)
    mode_b_text.draw(surface)
    level.draw(surface)
    hight.draw(surface)
    previous_menu_button.draw(surface)
    surface.set_colorkey((0, 0, 0))
    return surface, previous_menu_button


def create_game_choice_menu(window, mode, surface, b_mode_option, a_mode):
    window.fill(0x000000)
    mode.button_list[0].draw(window)
    mode.button_list[1].draw(window)
    for option in b_mode_option:
        for button in option.button_list:
            button.draw(window)
    for button in a_mode[1:]:
        button.draw(window)
    level = Text(mode.button_list[0],
                     (0.15,
                      0.43,
                      0.4,
                      0.7),
                     str(a_mode[0]))
    level.draw(window)
    window.blit(surface, (0, 0))
    pygame.display.flip()


def handle_a_mode(event, a_mode):
    if a_mode[1].is_pressed(event):
        if a_mode[0] < 15:
            a_mode[0] += 1
            return True 
    if a_mode[2].is_pressed(event):
        if a_mode[0] > 1:
            a_mode[0] -= 1
            return True
    return False


def game_choice_menu(window):
    mode, b_mode_option, a_mode = create_mode(window)
    surface, previous_menu_button = create_surface(window, mode)
    create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            window = loop_starter_pack(window, event)

            if handle_a_mode(event, a_mode):
                create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)

            if mode.radio_change(event):
                create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)

            for option in b_mode_option:
                if option.click_change(event):
                    create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)

            if event.type == pygame.VIDEORESIZE:
                for button in mode.button_list:
                    button.resize(window)
                for option in b_mode_option:
                    for button in option.button_list:
                        button.resize(mode.button_list[1])
                a_mode[1].resize(mode.button_list[0])
                a_mode[2].resize(mode.button_list[0])
                surface, previous_menu_button = create_surface(window, mode)
                create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if mode.get_value() == 0:
                        window.fill(0x000000)
                        level = a_mode[0]
                        data = gameplay(window, (level, 0))
                        game_over_menu(window, data.get_score())
                        proceed = False
                    else:
                        window.fill(0x000000)
                        level, hight = b_mode_option
                        data = gameplay(window, (level.get_value(), hight.get_value()))
                        game_over_menu(window, data.get_score())
                        proceed = False
            
            if previous_menu_button.is_pressed(event):
                main_menu(window)
                proceed = False
                return


def create_leaderboard_menu(window):
    previous_menu_button = Button2(window, (0.9, 0.05, 0.04), 'back')
    frame = pygame.Surface(window.get_size())
    previous_menu_button.draw(frame)
    window.blit(frame, (0, 0))
    statement = Button(window,
                         (0.15,
                          0.15,
                          0.7,
                          0.7),
                         '')
    statement.draw(window)
    pygame.display.flip()
    return previous_menu_button


def create_leaderboard_table(window, leaderboard, page):
    window_w, window_h = window.get_size()
    x_value = round(0.15 * window_w)+5
    y_value = round(0.15 * window_h)+5
    w_value = round(0.7 * window_w)-10
    h_value = round(0.15 * window_h)-5
    leaderboard = leaderboard.split(":")
    pages = (len(leaderboard) // 5) + 1
    for values in leaderboard[(page-1)*5:(page-1)*5+5]:
        try:
            values = values.split("#")
            rank = values[0]
            username = values[1]
            score = values[2]
        except IndexError:
            continue
        rect_rectangle = pygame.Rect(x_value, y_value, w_value, h_value)
        pygame.draw.rect(
            window,
            (150, 150, 150),
            rect_rectangle,
            5
        )
        rank_surface = pygame.Surface((w_value/3, h_value-10))
        username_surface = pygame.Surface((w_value/3, h_value-10))
        score_surface = pygame.Surface(((w_value/3)-10, h_value-10))
        if rank == "1":
            rank_surface.fill(COLOR['GOLD'])
        elif rank == "2":
            rank_surface.fill(COLOR['SILVER'])
        elif rank == "3":
            rank_surface.fill(COLOR['BRONZE'])
        pygame.draw.rect(rank_surface, (255, 255, 255), (0, 0, w_value/3, h_value-10), 2)
        pygame.draw.rect(username_surface, (255, 255, 255), (0, 0, w_value/3, h_value-10), 2)
        pygame.draw.rect(score_surface, (255, 255, 255), (0, 0, (w_value/3)-10, h_value-10), 2)
        font = pygame.font.SysFont("./others/Anton-Regular.ttf", round(0.07 * window_h))
        rank_text = font.render(rank, True, COLOR["WHITE"])
        username_text = font.render(username, True, COLOR["WHITE"])
        score_text = font.render(score, True, COLOR["WHITE"])
        rank_rect = rank_text.get_rect(center=((w_value/3)/2, (h_value-10)/2))
        username_rect = username_text.get_rect(center=((w_value/3)/2, (h_value-10)/2))
        score_rect = score_text.get_rect(center=((w_value/3)/2, (h_value-10)/2))
        rank_surface.blit(rank_text, rank_rect)
        username_surface.blit(username_text, username_rect)
        score_surface.blit(score_text, score_rect)
        window.blit(rank_surface, (x_value+5, y_value+5))
        window.blit(username_surface, (x_value+5+w_value/3, y_value+5))
        window.blit(score_surface, (x_value+5+2*w_value/3, y_value+5))
        y_value += h_value
    page_right = Button2(window,
                            (0.88,
                            0.45,
                            0.05),
                            'right_arrow')
    page_left = Button2(window,
                            (0.02,
                            0.45,
                            0.05),
                            'left_arrow')
    if page < pages:
        page_right.draw(window)
    if page > 1:
        page_left.draw(window)
    pygame.display.flip()
    return page_right, page_left, pages


def create_error_table(window, error):
    message = Button(window,
                         (0.15,
                          0.425,
                          0.7,
                          0.15),
                         error,
                         COLOR['RED'])
    message.draw(window)
    pygame.display.flip()


def leaderboard_menu(window, page):
    previous_menu_button = create_leaderboard_menu(window)
    proceed = True
    response, status_code = post_request("http://tetrisnsi.tk/leaderboard")
    while proceed:
        for event in pygame.event.get():
            loop_starter_pack(window, event)
            if status_code == 200:
                page_right, page_left, limit = create_leaderboard_table(window, response, page)
                if page_right.is_pressed(event) and page < limit:
                    proceed = False
                    leaderboard_menu(window, page+1)
                if page_left.is_pressed(event) and page > 1:
                    proceed = False
                    leaderboard_menu(window, page-1)
            else:
                create_error_table(window, game_strings.get_string("error"))
            if event.type == pygame.VIDEORESIZE:
                previous_menu_button = create_leaderboard_menu(window)
            if previous_menu_button.is_pressed(event):
                main_menu(window)
                proceed = False
                return


def create_game_over_menu(window, score):
    font_height = round(0.15 * window.get_height())
    font_size = get_font_size(font_height)
    end = Text(window,
               (0,
                0.075,
                1,
                0.3),
               game_strings.get_string("gameover"))
    score = Text(window,
                 (0,
                  0.3,
                  1,
                  0.15),
                 game_strings.get_string("yourscore").format(score))
    rejouer_button = Button(window,
                            (0.3,
                             0.5,
                             0.4,
                             0.18),
                            game_strings.get_string("replay"),
                            font_size)
    quitter_button = Button(window,
                            (0.3,
                             0.7,
                             0.4,
                             0.18),
                            game_strings.get_string("quit"),
                            font_size)

    frame = pygame.Surface(window.get_size())
    end.draw(frame)
    score.draw(frame)
    quitter_button.draw(frame)
    rejouer_button.draw(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()
    return rejouer_button, quitter_button


def game_over_menu(window, score):
    rejouer_button, quitter_button = create_game_over_menu(window, score)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                rejouer_button, quitter_button = create_game_over_menu(window, score)
            if rejouer_button.is_pressed(event):
                game_choice_menu(window)
                proceed = False
                return
            if quitter_button.is_pressed(event):
                proceed = False
                main_menu(window)
                return
