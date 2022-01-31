"""fichier python principal du jeu Tetris codé en tant que projet de deuxième
trimestre pour la spécialité NSI."""

# pylint: disable=E1101
# (no-member) erreur apparaissant pour les constantes de pygame référant aux
# touches de clavier et boutons de fenêtre, ...

# importations des librairies python
import tkinter
import sys
import time
import pygame
import pygame.freetype
from modules.solene import Bag, HoldQueue, Matrix, NextQueue
from modules.solene import Tetrimino, Window, MenuButton, Data, Chronometer


# initialisation de pygame
pygame.init()

# préréglage du module mixer
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.music.set_volume(0.4)

# création d'un objet tkinter afin de récupérer
# les données liées à la taille de l'écran
tk = tkinter.Tk()
tk.withdraw()


FULLSCREEN_WIDTH = tk.winfo_screenwidth()
WINDOW_HEIGHT = round(tk.winfo_screenheight() * 2/3)
WINDOW_WIDTH = round(WINDOW_HEIGHT * 1.8)

# font du jeu
game_score = pygame.freetype.Font("others/Anton-Regular.ttf", 18)
scoring_data_name = pygame.font.Font("others/Anton-Regular.ttf", 30)

# définition de la fenêtre pygame de taille dynamique
tetris_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE, 64)

# importation d'images
icon = pygame.image.load("image/logo.ico").convert_alpha()
# prop = pygame.image.load("prop2.png").convert_alpha()
menubutton = pygame.image.load("image/menubutton.png").convert_alpha()

"""tetris_window.blit(prop, (55, 16))
pygame.display.flip()"""

# personnalisation de la fenêtre
pygame.display.set_caption("TETRIS")
# pygame.display.set_icon(icon)
window_size = pygame.display.get_surface().get_size()


def resize_all(window_ob, obj):
    """"redimensionne tous les objets nécéssitant d'être
    redimensionnés."""
    for element in obj[1:]:
        element.resize(window_ob)


def display_all(window, obj):
    """raffraîchit le jeu en faisant afficher une frame,
    contenant les objets dont les caractéristiques ont été
    mis à jour."""
    frame = pygame.Surface(window.size)
    # affichage de l'image pour le boutton des menus, ## voir arrangement
    menu_image = pygame.transform.scale(menubutton,
                                        (obj[4].rect.w,
                                        obj[4].rect.h))
    frame.blit(menu_image, (obj[4].rect.x, obj[4].rect.y))
    for element in obj:
        element.display(frame)
    # dessin de la ghost piece
    if obj[0].state != 2:
        if obj[1].draw_ghost_piece(frame, obj[0]) == "ERROR snif :')":
            pygame.image.save(tetris_window, "screenshot.jpeg")
    # frame sur la fenêtre
    tetris_window.blit(frame, (0, 0))
    # ## voir à supprimer
    display_game_data(obj[5])
    # rafraichissement de la fenêtre pygame
    pygame.display.flip()


def display_game_data(data):
    # création d'une d'un objet pygame.Surface de la taille de l'encadré data
    frame = pygame.Surface((data.rect.w - 2 * data.width, data.rect.h - 2 * data.width))
    # ## en guise de test
    frame.fill(0x440000)
    message_erreur = scoring_data_name.render(data.message, 1, (255,255,255))
    score = scoring_data_name.render(data.score, 1, (255,255,255))
    rect = pygame.Surface(score.get_size())
    rect.fill(0x004400)
    frame.blit(rect, (data.margin, data.margin * 5))
    frame.blit(message_erreur, (data.margin, data.margin))
    frame.blit(score, (data.margin, data.margin * 5))
    tetris_window.blit(frame, (data.rect.x + data.width , data.rect.y + data.width))
    pygame.display.flip()


def gameplay():
    """gameplay du jeu tetris"""
    # ## instanciation à mettre dans une fonction ?
    bag = Bag()
    game_window = Window(window_size)
    matrix = Matrix(game_window)
    next_queue = NextQueue(game_window)
    hold_queue = HoldQueue(game_window)
    menu_button = MenuButton(game_window)
    data = Data(game_window)

    tetrimino = Tetrimino(matrix)

    game_object = (tetrimino, matrix, next_queue, hold_queue, menu_button, data)

    display_all(game_window, game_object)


    time_before_refresh = Chronometer()
    lock_down_chrono = Chronometer()
    SHADE_PHASE = 1
    LOCK_PHASE_FIRST = 1

    while True:

        # stocke la valeur actuelle de la taille de la fenêtre
        window_current_size = pygame.display.get_surface().get_size()
        game_object = (tetrimino, matrix, next_queue, hold_queue, menu_button, data)

        # évènements pygame
        for event in pygame.event.get():
            # appui sur la croix de la fenêtre
            if event.type == pygame.QUIT:
                # fermeture de la fenêtre
                pygame.quit()
                sys.exit()

            '''# appui sur le boutton redimensionner de la fenêtre
            if event.type == pygame.VIDEORESIZE:
                try:
                    print(game_window.size, FULLSCREEN_SIZE)
                    if game_window.size == FULLSCREEN_SIZE:
                        pygame.draw.rect(tetris_window, (0, 0, 250),
                                        pygame.Rect(0, 0, 1700, 200))
                        pygame.display.flip()
                        time.sleep(3)
                        pygame.quit()
                        sys.exit()
                except NameError:
                    FULLSCREEN_SIZE = pygame.display.get_surface().get_size()'''

            # dans le cas où l'utilisateur change la taille de la fenêtre
            if game_window.size != window_current_size:
                # mise à jour des attributs de l'objet Window
                game_window.change_size(window_current_size)
                print(game_window.size)
                # reaffichage avec changement des tailles et emplacement des objets
                resize_all(game_window, game_object)
                display_all(game_window, game_object)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    tetrimino.hard_drop()

                if event.key == pygame.K_DOWN:
                    tetrimino.soft_drop(matrix, data)

                if event.key == pygame.K_RIGHT:
                    tetrimino.move_right(matrix)

                if event.key == pygame.K_LEFT:
                    tetrimino.move_left(matrix)

                if event.key == pygame.K_z:
                    tetrimino.turn_left(matrix)

                if event.key == pygame.K_UP:
                    tetrimino.turn_right(matrix)

                if event.key == pygame.K_c:
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

                display_all(game_window, game_object)
        
        # phase précédant le lock down
        if tetrimino.state == 1:
            # permet de jouer sur la couleur du tetrimino
            values = tetrimino.lock_phase(matrix, lock_down_chrono,
                                        LOCK_PHASE_FIRST, SHADE_PHASE)
            LOCK_PHASE_FIRST, SHADE_PHASE = values
            display_all(game_window, game_object)
            time.sleep(0.015)

        # phase lock down
        elif tetrimino.state == 2:
            # le tetrimino est lock dans matrix
            tetrimino.lock_on_matrix(matrix)
            # le tetrimino suivant est créé
            tetrimino = Tetrimino(matrix)
            hold_queue.allow_hold()
            display_all(game_window, game_object)
            # clear les lines s'il y a
            matrix.clear_lines(data)
            display_all(game_window, game_object)
            # le chronomètre est raffraîchi
            time_before_refresh.reset()

        # dans le cas où le tetrimino est en falling phase
        else:
            display_all(game_window, game_object)
            if time_before_refresh == data.refresh:
                tetrimino.fall(matrix)
                # on reinitialise le chrono
                time_before_refresh.reset()
        # ##pour tester au besoin
        # display_all(game_window, game_object)
        display_game_data(data)


if __name__ == "__main__":
    gameplay()
