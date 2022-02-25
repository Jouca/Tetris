"""module codé par Bastien (@BLASTUHQ) TG8, contenant des fonctions pour
les menus du jeu Tetris. Repassage du code par Solène, (@periergeia)."""


import pygame
from zmq import PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_MESSAGE
try:
    from constant import LANG, COLOR
    from diego import GameStrings, post_request
    from gameplay import gameplay
    from useful import get_font_size, loop_starter_pack, Button, Text
except ModuleNotFoundError:
    from modules.constant import LANG, COLOR
    from modules.diego import GameStrings, post_request
    from modules.gameplay import gameplay
    from modules.useful import get_font_size, loop_starter_pack, Button, Text


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
                menuplay()
                proceed = False
                return


def create_game_choice_menu(window):
    menu_background = pygame.image.load('./image/menu_background2.png').convert_alpha()
    font_height = round(0.15 * window.get_height())
    font_size = get_font_size(font_height)
    background = pygame.transform.scale(menu_background, window.get_size())
    statement = Text(window,
                     (0.175,
                      0.175,
                      0.65,
                      0.15),
                     game_strings.get_string("select_mode"))
    mode_a_button = Button(window,
                            (0.175,
                             0.4,
                             0.3,
                             0.4),
                            game_strings.get_string("mode_a"), font_size)
    mode_b_button = Button(window,
                           (0.525,
                            0.4,
                            0.3,
                            0.4),
                           game_strings.get_string("mode_b"), font_size)

    frame = pygame.Surface(window.get_size())
    frame.blit(background, (0, 0))
    statement.draw(frame)
    mode_a_button.draw(frame)
    mode_b_button.draw(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()
    return mode_a_button, mode_b_button


def game_choice_menu(window):
    mode_a_button, mode_b_button = create_game_choice_menu(window)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            window = loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                mode_a_button, mode_b_button = create_game_choice_menu(window)
            if mode_a_button.is_pressed(event):
                window.fill(0x000000)
                gameplay(window, (1, 0))
                game_over_menu(window)
                proceed = False
                return
            elif mode_b_button.is_pressed(event):
                window.fill(0x000000)
                gameplay(window, (4, 4)) # ## level 4 hight 4
                game_over_menu(window)
                proceed = False
                return
            '''elif back_button.is_pressed(event):
                main_menu()
                proceed = False
                return'''


def create_game_over_menu(window):
    font_height = round(0.15 * window.get_height())
    font_size = get_font_size(font_height)
    end = Text(window,
               (0,
                0.075,
                1,
                0.3),
               game_strings.get_string("gameover"))
    score = "123456"
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
                            "REJOUER", font_size)
    quitter_button = Button(window,
                            (0.3,
                             0.7,
                             0.4,
                             0.18),
                            "QUITTER", font_size)

    frame = pygame.Surface(window.get_size())
    end.draw(frame)
    score.draw(frame)
    quitter_button.draw(frame)
    rejouer_button.draw(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()
    return rejouer_button, quitter_button


def game_over_menu(window):
    rejouer_button, quitter_button = create_game_over_menu(window)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                rejouer_button, quitter_button = create_game_over_menu(window)
            if rejouer_button.is_pressed(event):
                game_choice_menu(window)
                proceed = False
                return
            if quitter_button.is_pressed(event):
                proceed = False
                pygame.quit()


def create_leaderboard_menu(window):
    font_height = round(0.15 * window.get_height())
    font_size = get_font_size(font_height)
    retour_button = Button(window,
                            (0.01,
                             0.01,
                             0.2,
                             0.1),
                            game_strings.get_string("retour"),
                            font_size
    )

    frame = pygame.Surface(window.get_size())
    retour_button.draw(frame)
    window.blit(frame, (0, 0))
    window_w, window_h = window.get_size()
    x_value = round(0.15 * window_w)
    y_value = round(0.15 * window_h)
    w_value = round(0.7 * window_w)
    h_value = round(0.7 * window_h)
    rect_rectangle = pygame.Rect(x_value, y_value, w_value, h_value)
    pygame.draw.rect(
        window,
        (255, 255, 255),
        rect_rectangle,
        5
    )
    pygame.display.flip()
    return retour_button


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
            rank_surface.fill((245, 189, 2))
        elif rank == "2":
            rank_surface.fill((187, 194, 204))
        elif rank == "3":
            rank_surface.fill((205, 127, 50))
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
        y_value += 98
    page_right = Button(window,
                            (0.88,
                            0.45,
                            0.1,
                            0.15),
                            "->",
                            get_font_size(round(0.3 * window_h))
    )
    page_left = Button(window,
                            (0.02,
                            0.45,
                            0.1,
                            0.15),
                            "<-",
                            get_font_size(round(0.3 * window_h))
    )
    if page < pages:
        page_right.draw(window)
    if page > 1:
        page_left.draw(window)
    pygame.display.flip()
    return page_right, page_left, pages


def create_error_table(window, error):
    window_w, window_h = window.get_size()
    x_value = round(0.15 * window_w)+5
    y_value = round(0.15 * window_h)+5
    w_value = round(0.7 * window_w)-10
    h_value = round(0.15 * window_h)-5
    rect_rectangle = pygame.Rect(x_value, y_value, w_value, h_value)
    pygame.draw.rect(
        window,
        (150, 150, 150),
        rect_rectangle,
        5
    )
    font = pygame.font.SysFont("./others/Anton-Regular.ttf", round(0.07 * window_h))
    error_text = font.render(error, True, COLOR["WHITE"])
    error_rect = error_text.get_rect(center=((w_value)/2, (h_value-10)/2))
    error_surface = pygame.Surface((w_value-10, h_value-10))
    error_surface.fill((255, 0, 0))
    error_surface.blit(error_text, error_rect)
    window.blit(error_surface, (x_value+5, y_value+5))
    pygame.display.flip()


def leaderboard_menu(window, page):
    retour_button = create_leaderboard_menu(window)
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
                retour_button = create_leaderboard_menu(window)
            if retour_button.is_pressed(event):
                main_menu(window)
                proceed = False
                return


def menuhelp():
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(150, 50, 700, 400))
    retour = Button((255, 300, 500, 100), "RETOUR MENU", 50, (250, 250, 250))
    """help = Button((505, 350, 300, 100), "Aide", 50, (0, 0, 255))
    classement = Button((195, 350, 300, 100), "Classement", 50, (0, 0, 255))"""

    txt = myfont.render("Voici les regle du jeux : - ne pas dire bonsoir", False, (255, 255, 255))
    screen.blit(txt, (290, 200))

    """screen.blit(logo, (350, 50))"""
    retour.draw(screen)
    """help.draw(screen)
    classement.draw(screen)"""
    pygame.display.flip()


def menuderoulant():
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(150, 50, 700, 400))

    retour = Button((205, 80, 590, 90), "RETOUR MENU", 50, (250, 250, 250))
    help = Button((205, 200, 590, 90), "MENU AIDE", 50, (250, 250, 250))
    options = Button((205, 320, 590, 90), "OPTIONS", 50, (250, 250, 250))

    """screen.blit(logo, (350, 50))"""
    retour.draw(screen)
    help.draw(screen)
    options.draw(screen)
    pygame.display.flip()
