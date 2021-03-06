"""module codé par Bastien (@BLASTUHQ) TG5, contenant des fonctions pour
les menus du jeu Tetris. Repassage du code par Solène, (@periergeia)."""


import datetime
import os
import pygame
try:
    from constant import LANG, COLOR
    from diego import GameStrings, post_request, read_json
    from paul import main_rule
    from gameplay import gameplay
    from solene_1 import RadioButton
    from paul import main_rule
    from useful import loop_starter_pack, Button1, Button2, Text
except ModuleNotFoundError:
    from modules.constant import LANG, COLOR
    from modules.diego import GameStrings, post_request, read_json
    from modules.paul import main_rule
    from modules.gameplay import gameplay
    from modules.solene_1 import RadioButton
    from modules.paul import main_rule
    from modules.useful import loop_starter_pack, Button1, Button2, Text


game_strings = GameStrings(LANG)


def create_main_menu(window):
    """partie affichage du menu principal."""
    # importation du logo
    logo = pygame.image.load('./image/logo.jpg').convert_alpha()
    logo_height = window.get_height() // 4
    logo_size = (round(340 * logo_height / 153), logo_height)
    logo_to_display = pygame.transform.scale(logo, logo_size)
    logo_pos = (window.get_width() - logo_size[0]) // 2, round(window.get_height() * 0.15)

    window_w = window.get_width()

    # définition de boutons
    play_button = Button1(window,
                          (logo_pos[0] / window_w,
                           0.45,
                           logo_size[0] / window_w,
                           0.15),
                          game_strings.get_string("play"))
    ranking_button = Button1(window,
                             (logo_pos[0] / window_w,
                              0.65,
                              (logo_size[0] / window_w) * 0.65,
                              0.15),
                             game_strings.get_string("leaderboard"))
    help_button = Button1(window,
                          (logo_pos[0] / window_w + (logo_size[0] / window_w) * 0.65,
                           0.65,
                           (logo_size[0] / window_w) * 0.35,
                           0.15),
                          game_strings.get_string("help"))

    #placement sur la fenêtre de jeu
    frame = pygame.Surface(window.get_size())
    frame.blit(logo_to_display, (logo_pos))
    play_button.draw(frame)
    help_button.draw(frame)
    ranking_button.draw(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()
    return play_button, ranking_button, help_button


def main_menu(window):
    """partie logique, qui gère le menu principal appelant la fonction
    adéquate au bouton pressé."""
    play_button, ranking_button, help_button = create_main_menu(window)
    # évènements pygame
    proceed = True
    while proceed:
        for event in pygame.event.get():
            loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                # pour resize les éléments de la fenettre
                play_button, ranking_button, help_button = create_main_menu(window)
            # bouton "jouer" pressé
            if play_button.is_pressed(event):
                # appel de la fonction des options de jeu
                game_choice_menu(window)
                proceed = False
                return
            # bouton "classement" pressé
            if ranking_button.is_pressed(event):
                # appel de la fonction gérant l'affichage du classement
                leaderboard_menu(window, 1)
                proceed = False
                return
            # bouton aide pressé
            if help_button.is_pressed(event):
                # appel d'affichage des règles
                main_rule(window)
                # retour au menu principal lorsque la fonction précédente se termine
                main_menu(window)
                proceed = False
                return


def create_mode(window):
    """fonction annexe des options de jeu.
    La fonction renvoie des objets utiles au maniement des options."""
    # création des encadrés qui seront sensibles au survol de la souris
    mode_a = Button1(window,
                     (0.175,
                      0.2,
                      0.3,
                      0.6),
                     '',
                     (100, 100, 100))
    mode_b = Button1(window,
                     (0.525,
                      0.2,
                      0.3,
                      0.6),
                     '',
                     (100, 100, 100))
    mode = RadioButton((mode_a, mode_b))
    # création de listes pour les options du mode B
    # liste contenant les choix de niveau
    level_button_list = []
    y_value = 0.35
    for i in range(2):
        x_value = 0.15
        for j in range(5):
            button = Button1(mode_b,
                             (x_value,
                              y_value,
                              0.14,  # 1/7
                              0.1),
                              str(i * 5 + j),
                             (110, 110, 110))
            level_button_list.append(button)
            x_value += 0.14
        y_value += 0.1
    # liste des choix de hauteur (difficulté)
    hight_button_list = []
    y_value = 0.7
    for i in range(2):
        x_value = 0.15
        for j in range(3):
            button = Button1(mode_b,
                             (x_value,
                              y_value,
                              0.23,  # 7/30
                              0.1),
                              str(i * 3 + j),
                             (110, 110, 110))
            hight_button_list.append(button)
            x_value += 0.23
        y_value += 0.1
    # création de l'objet gérant les options selectionnées dans le mode B
    b_mode_option = (RadioButton(tuple(level_button_list)),
                     RadioButton(tuple(hight_button_list)))
    # création des boutons "+" et "-" apparent dans le mode A
    plus_button = Button1(mode_a,
                          (0.65,
                           0.5,
                           0.2,
                           0.1),
                          '+',
                          (120, 120, 120))
    minus_button = Button1(mode_a,
                           (0.65,
                            0.7,
                            0.2,
                            0.1),
                            '-',
                           (120, 120, 120))
    a_mode = [1, plus_button, minus_button]
    return mode, b_mode_option, a_mode


def create_surface(window, mode):
    """fonction créant la surface de fond visible du menu des options."""
    surface = pygame.Surface(window.get_size())
    # textes
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
    # dessin des textes sur la surface à renvoyer
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
    """partie affichage du menu des options de jeu, elle requiert différents
    paramètres issues de fonctions annexes."""
    window.fill(0x000000)
    # dessin des encadrés d'options de jeu A et B
    mode.button_list[0].draw(window)
    mode.button_list[1].draw(window)
    # dessin des boutons du mode B
    for option in b_mode_option:
        for button in option.button_list:
            button.draw(window)
    # dessin des boutons "+" et "-" du mode A
    for button in a_mode[1:]:
        button.draw(window)
    # ajout du texte Level
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
    """gère le mode A. Renvoie un booléen, True lorsqu'un des boutons
    du mode A est pressé, False autrement. Le niveau est compris entre
    1 et 15 inclus."""
    # dans le cas où le bouton "+" est pressé
    if a_mode[1].is_pressed(event):
        if a_mode[0] < 15:
            a_mode[0] += 1
            return True
    # dans le cas où le bouton "-" est pressé
    if a_mode[2].is_pressed(event):
        if a_mode[0] > 1:
            a_mode[0] -= 1
            return True
    return False


def game_choice_menu(window):
    """partie logique du menu des options de jeu.
    Elle permet après que la touche entrée soit pressée de commencer la partie
    en prenant en considération les choix du joueur."""
    # premières attributions de valeurs aux variables utilisées
    mode, b_mode_option, a_mode = create_mode(window)
    surface, previous_menu_button = create_surface(window, mode)
    create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            window = loop_starter_pack(window, event)

            # si l'un des boutons du mode A est pressé
            if handle_a_mode(event, a_mode):
                # mise à jour de l'affichage
                create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)

            # si la souris survole une surface mode différente de celle sur laquelle elle est
            if mode.radio_change(event):
                # mise à jour de l'affichage
                create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)
            
            # vérification pour chaque option contenu dans le mode B
            for option in b_mode_option:
                # si un clic de la souris s'opère
                if option.click_change(event):
                    # mise à jour de l'affichage
                    create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)

            # si la fenêtre est redimensionnée
            if event.type == pygame.VIDEORESIZE:
                # redimenssionnement de tous les objets nécéssaire à l'affichage
                for button in mode.button_list:
                    button.resize(window)
                for option in b_mode_option:
                    for button in option.button_list:
                        button.resize(mode.button_list[1])
                a_mode[1].resize(mode.button_list[0])
                a_mode[2].resize(mode.button_list[0])
                surface, previous_menu_button = create_surface(window, mode)
                # mise à jour de l'affichage
                create_game_choice_menu(window, mode, surface, b_mode_option, a_mode)

            # lorsque la touche entrée est pressée
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # si le choix du joueur est le mode A
                    if mode.get_value() == 0:
                        window.fill(0x000000)
                        level = a_mode[0]
                        # appel de la fonction du gameplay
                        game_data, game_screen, screenshot = gameplay(window, (level, -1))
                        # renvoi vers le game over
                        game_over_menu(window, game_data, game_screen, screenshot)
                        proceed = False
                    # autrement le choix ne peut que être le mode B
                    else:
                        window.fill(0x000000)
                        level, hight = b_mode_option
                        # appel de la fonction du gameplay
                        game_data, game_screen, screenshot = gameplay(window,
                                                                      (level.get_value(),
                                                                      hight.get_value()))
                        # renvoi vers le game over
                        game_over_menu(window, game_data, game_screen, screenshot)
                        proceed = False

            # dans le cas où le bouton de retour au menu précédent est pressé
            if previous_menu_button.is_pressed(event):
                # appel du menu principal
                main_menu(window)
                proceed = False
                return


def create_leaderboard_menu(window):
    """Affichage du classement."""
    previous_menu_button = Button2(window, (0.9, 0.05, 0.04), 'back')
    frame = pygame.Surface(window.get_size())
    previous_menu_button.draw(frame)
    window.blit(frame, (0, 0))
    statement = Button1(window,
                         (0.15,
                          0.15,
                          0.7,
                          0.7),
                         '')
    statement.draw(window)
    pygame.display.flip()
    return previous_menu_button


def create_leaderboard_table(window, leaderboard, page):
    """Crée la table du classement."""
    window_w, window_h = window.get_size()
    x_value = round(0.15 * window_w)+5
    y_value = round(0.15 * window_h)+5
    w_value = round(0.7 * window_w)-10
    h_value = round(0.145 * window_h)-5
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
    """Affiche le message d'erreur sur la table du classement."""
    message = Button1(window,
                         (0.15,
                          0.425,
                          0.7,
                          0.15),
                         error,
                         COLOR['RED'])
    message.draw(window)
    pygame.display.flip()


def leaderboard_menu(window, page):
    """Menu du leaderboard."""
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


def get_now_string():
    """renvoie la date mise en forme."""
    now = datetime.datetime.now()
    return now.strftime('%d-%m-%Y_%Hh%M')


def create_game_over_menu(window, game_data, game_screen, enregistrer_texte):
    """partie affichage du menu game over."""
    frame = pygame.Surface(window.get_size())
    background = Button1(window,
                           (0.1,
                            0.1,
                            0.78,
                            0.8),
                           '',
                           (100, 100, 100))
    background.draw(frame)
    end = Text(background,
               (0,
                0.025,
                1,
                0.3),
               game_strings.get_string(game_data['issue']))
    end.draw(frame)
    score_text = Text(background,
                 (0.1,
                  0.25,
                  1,
                  0.15),
                 game_strings.get_string("yourscore").format(game_data['score']),
                 True)
    score_text.draw(frame)
    time = Text(background,
                 (0.1,
                  0.40,
                  1,
                  0.15),
                 game_strings.get_string("yourtime").format(game_data['time']),
                 True)
    time.draw(frame)
    lines = Text(background,
                 (0.1,
                  0.55,
                  1,
                  0.15),
                 game_strings.get_string("lines_count").format(game_data['lines']),
                 True)
    lines.draw(frame)
    replay_button = Button2(background, (0.1, 0.75, 0.1), 'retry')
    quit_button = Button2(background, (0.225, 0.75, 0.1), 'back')
    save_button = Button2(background, (0.350, 0.75, 0.1), 'save')
    score_upload_button = Button2(background, (0.475, 0.75, 0.1), 'upload')
    local_score_surface = Button1(background,
                           (0.6,
                            0.25,
                            0.3,
                            0.5 + 0.1 * background.get_width()/background.get_height()),
                           '',
                           (1, 1, 1))
    local_score_surface.draw(frame)
    local_scores = read_json("./others/game_save/data.json")
    for i in range(1, len(local_scores)+1):
        color = COLOR["WHITE"]
        if game_data['score'] == int(local_scores[str(i)]):
            color = COLOR["YELLOW"]
        current_score = Text(local_score_surface,
                             (0.07,
                              0.1 * i,
                              1,
                              0.23),
                             f"{i} - {local_scores[str(i)]}",
                             True,
                             color)
        current_score.draw(frame)
    frame.set_colorkey(COLOR['BLACK'])
    screen_save = pygame.transform.scale(game_screen, window.get_size())
    window.blit(screen_save, (0, 0))
    window.blit(frame, (0, 0))
    replay_button.draw(window)
    quit_button.draw(window)
    save_button.draw(window)
    score_upload_button.draw(window)
    if enregistrer_texte:
        text = Text(window,
                    (0.37,
                    0.9,
                    0.3,
                    0.1),
                    game_strings.get_string("save_success"))
        text.draw(window)
    pygame.display.flip()
    return replay_button, quit_button, save_button


def game_over_menu(window, game_data, game_screen, screenshot):
    """partie logique du menu game over."""
    proceed = True
    enregistrer_texte = False
    while proceed:
        replay_button, quit_button, save_button = create_game_over_menu(
            window,
            game_data,
            game_screen,
            enregistrer_texte
        )
        for event in pygame.event.get():
            loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                replay_button, quit_button, save_button = create_game_over_menu(
                    window,
                    game_data,
                    game_screen,
                    enregistrer_texte
                )
            if replay_button.is_pressed(event):
                game_choice_menu(window)
                proceed = False
                return
            if quit_button.is_pressed(event):
                proceed = False
                main_menu(window)
                return
            if save_button.is_pressed(event):
                if not enregistrer_texte:
                    pygame.image.save(screenshot, 'game_screen_save/screenshot.png')
                    os.rename(
                        'game_screen_save/screenshot.png',
                        f'game_screen_save/{get_now_string()}.png'
                    )
                    enregistrer_texte = True
