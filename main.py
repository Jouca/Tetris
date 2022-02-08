"""fichier python principal du jeu Tetris codé en tant que projet de deuxième
trimestre pour la spécialité NSI."""


# importations des librairies python
import sys
import time
import pygame
import pygame.freetype
from modules.solene import Bag, HoldQueue, Matrix, NextQueue
from modules.solene import Tetrimino, MenuButton, Data, Chronometer

# pylint: disable=E1101
# (no-member) erreur apparaissant pour les constantes de pygame référant aux
# touches de clavier et boutons de fenêtre, ...

# initialisation de pygame
pygame.init()

'''# préréglage du module mixer
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.music.set_volume(0.4)'''


FULLSCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][1]
WINDOW_HEIGHT = round(FULLSCREEN_WIDTH * 2/3)
WINDOW_WIDTH = round(WINDOW_HEIGHT * 1.8)
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)


# définition de la fenêtre pygame de taille dynamique
tetris_window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
window_data = {'size' : WINDOW_SIZE,
               'width': WINDOW_WIDTH,
               'height': WINDOW_HEIGHT,
               'margin': round(0.05 * WINDOW_HEIGHT)}


# importation d'images
icon = pygame.image.load("./image/window_logo.png").convert_alpha()
# prop = pygame.image.load("prop2.png").convert_alpha()
menubutton = pygame.image.load("./image/menubutton.png").convert_alpha()

"""tetris_window.blit(prop, (55, 16))
pygame.display.flip()"""

# personnalisation de la fenêtre
pygame.display.set_caption("TETRIS")
pygame.display.set_icon(icon)


def resize_all(window, obj):
    """"redimensionne toutes les choses nécéssitant d'être
    redimensionnées."""
    # redimensionne chaque objet avec leur méthode resize
    for element in obj[1:]:
        element.resize(window)
    obj[-1].values_relative_position()


def display_all(window, chronometer, obj):
    """raffraîchit le jeu en faisant afficher une frame,
    contenant les objets dont les caractéristiques ont été
    mis à jour."""
    # création d'une frame
    frame = pygame.Surface(window['size'])
    # affichage de l'image pour le boutton des menus, ## voir arrangement ?
    menu_image = pygame.transform.scale(menubutton,
                                        (obj[4].rect.w,
                                        obj[4].rect.h))
    frame.blit(menu_image, (obj[4].rect.x, obj[4].rect.y))
    # affiche chaque objet avec leur méthode display
    for element in obj:
        element.display(frame)
    # dessin de la ghost piece
    if obj[0].state != 2:
        # ## test à enlever si pas de soucis
        if obj[1].draw_ghost_piece(frame, obj[0]) == "ERROR snif :')":
            pygame.image.save(tetris_window, "screenshot.jpeg")
    # frame sur la fenêtre
    tetris_window.blit(frame, (0, 0))
    # ## voir à supprimer ?
    display_game_data(obj[5], chronometer)
    # rafraichissement de la fenêtre pygame
    pygame.display.flip()


def display_game_data(data, chronometer):
    # création d'un objet pygame.Surface de la taille de l'encadré data
    frame = pygame.Surface((data.rect.w - 2 * data.width, data.rect.h - 2 * data.width))

    frame.blit(data.surface, (0, 0))
    data.update(chronometer, frame)
    tetris_window.blit(frame, (data.rect.x + data.width , data.rect.y + data.width))
    pygame.display.flip()

'''def display_game_data(data):
    # utiliser autre méthode si possible
    temp = [1, None, 0, 1, None, 0, 0, 0, 1, 0, 1, 0, 1]
    # création d'un objet pygame.Surface de la taille de l'encadré data
    frame = pygame.Surface((data.rect.w - 2 * data.width, data.rect.h - 2 * data.width))
    score = data.values_surface[0]
    time = data.values_surface[1]

    rect2 = pygame.Surface(data.font_place)  # 5/13 = 0.2173
    rect2.fill(0x004444)
    frame.blit(rect2, (data.margin // 2, data.margin))

    y = data.margin
    font_h = data.name_surface[0].get_size()
    i = 0
    for e in temp:
        if e == 1:
            a, b = data.name_surface[i].get_size()
            rect = pygame.Surface((a, b))  # 5/13 = 0.2173
            rect.fill(0x660044)

            frame.blit(rect, (data.margin // 2, y))
            frame.blit(data.name_surface[i], (data.margin // 2, y))

            i += 1
            y += font_h[1]
        elif e == None:
            a, b = time.get_size()
            rect = pygame.Surface((a, b))  # 5/13 = 0.2173
            rect.fill(0x6666)
            frame.blit(rect, (data.margin // 2, y))

            frame.blit(time, (data.margin // 2, y))
            y += font_h[1]
        else:
            y += data.space_between_string

    tetris_window.blit(frame, (data.rect.x + data.width , data.rect.y + data.width))
    pygame.display.flip()'''


def game_pause():
    pass

# déplacer plus haut lors réorganisation
lang = 'EN'

# provisoire, sans les menus
level = 1
mode_B = False


def gameplay(tetris_window):
    """gameplay du jeu tetris"""
    w_width, w_height = tetris_window.get_size()
    window_data = {'size' : (w_width, w_height),
                   'width': w_width,
                   'height': w_height,
                   'margin': round(0.05 * w_height)}
    game_type = (level, mode_B)
    bag = Bag()
    game_chrono = Chronometer()
    matrix = Matrix(window_data, game_type)
    next_queue = NextQueue(window_data)
    hold_queue = HoldQueue(window_data)
    menu_button = MenuButton(window_data)
    data = Data(window_data, lang, game_chrono, game_type)

    tetrimino = Tetrimino(matrix)

    game_object = (tetrimino, matrix, next_queue, hold_queue, menu_button, data)

    display_all(window_data, game_chrono, game_object)


    time_before_refresh = Chronometer()
    lock_down_chrono = Chronometer()
    SHADE_PHASE = 1
    LOCK_PHASE_FIRST = 1
    softdrop = False

    while True:

        game_object = (tetrimino, matrix, next_queue, hold_queue, menu_button, data)

        # évènements pygame
        for event in pygame.event.get():
            # appui sur la croix de la fenêtre
            if event.type == pygame.QUIT:
                # fermeture de la fenêtre
                pygame.quit()
                sys.exit()
            
            # dans le cas où l'utilisateur change la taille de la fenêtre
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                if width < 545:
                    width = 545
                if width / height < 1.1:
                    width = round(1.8 * height)
                if height < 303:
                    height = 303
                window_size = (width, height)
                tetris_window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                window_data = {'size' : window_size,
                               'width': width,
                               'height': height,
                               'margin': round(0.05 * height)}
                print(f'current window size :   {window_data}')
                # reaffichage avec changement des tailles et emplacement des objets
                resize_all(window_data, game_object)
                display_all(window_data, game_chrono, game_object)
            
            # ## à enlever en fin
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    softdrop = False
                    data.set_fall_speed()

            if event.type == pygame.KEYDOWN:

                key_mod = pygame.key.get_mods()
                key = pygame.key.get_pressed()
                
                if key[pygame.K_F1] or key[pygame.K_ESCAPE]:
                    game_pause()

                elif key[pygame.K_SPACE]:
                    tetrimino.hard_drop(data)

                elif key[pygame.K_DOWN]:
                    softdrop = True
                    data.fall_speed /= 20  # ## pas bon

                elif key[pygame.K_RIGHT]:
                    tetrimino.move_right(matrix)

                elif key[pygame.K_LEFT]:
                    tetrimino.move_left(matrix)

                elif key[pygame.K_w] or (key_mod and pygame.KMOD_CTRL):
                    tetrimino.turn_left(matrix)

                elif key[pygame.K_UP] or key[pygame.K_x]:
                    tetrimino.turn_right(matrix)

                elif event.key == pygame.K_c or (event.mod and pygame.KMOD_SHIFT):
                    if hold_queue.can_hold:
                        temp = hold_queue.get_t_type()
                        hold_queue.hold(tetrimino)
                        # dans le cas où la hold queue n'est pas vide
                        if temp:
                            tetrimino.set_type(temp)
                            tetrimino.set_y(0)
                        # si vide
                        else:
                            # création d'un nouveau tetrimino
                            tetrimino = Tetrimino(matrix)

                display_all(window_data, game_chrono, game_object)
        
        # phase précédant le lock down
        if tetrimino.state == 1:
            # permet de jouer sur la couleur du tetrimino
            values = tetrimino.lock_phase(matrix, lock_down_chrono,
                                        LOCK_PHASE_FIRST, SHADE_PHASE)
            LOCK_PHASE_FIRST, SHADE_PHASE = values
            display_all(window_data, game_chrono, game_object)
            time.sleep(0.015)

        # phase lock down
        elif tetrimino.state == 2:
            # le tetrimino est lock dans matrix
            tetrimino.lock_on_matrix(matrix)
            # le tetrimino suivant est créé
            tetrimino = Tetrimino(matrix)
            hold_queue.allow_hold()
            display_all(window_data, game_chrono, game_object)
            # clear les lines s'il y a
            matrix.clear_lines(data)
            display_all(window_data, game_chrono, game_object)
            # le chronomètre est raffraîchi
            time_before_refresh.reset()

        # dans le cas où le tetrimino est en falling phase
        else:
            # dans le cas où le joueur souhaite faire un softdrop
            # spécifié par le fait que la touche flèche bas est
            # maintenue pressée
            if time_before_refresh == data.fall_speed:
                # score incrémenté de 1 lorsque le tetrimino peut tomber
                if tetrimino.fall(matrix) and softdrop:
                    data.score_increase(1)
                # on reinitialise le chrono
                time_before_refresh.reset()
            # reaffichage de l'écran
            display_all(window_data, game_chrono, game_object)
        # ##pour tester au besoin
        # display_all(window_data, game_object)
        display_game_data(data, game_chrono)


if __name__ == "__main__":
    gameplay(tetris_window)
