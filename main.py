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
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# font du jeu
game_score = pygame.freetype.Font("others/Anton-Regular.ttf", 18)
scoring_data_name = pygame.font.Font("others/Anton-Regular.ttf", 18)

# définition de la fenêtre pygame de taille dynamique
tetris_window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE, 64)

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


def resize_all(window, obj):
    """"redimensionne toutes les choses nécéssitant d'être
    redimensionnées."""
    # redimensionne chaque objet avec leur méthode resize
    for element in obj[1:]:
        element.resize(window)
    # redimensionne les emplacements des fonts pour l'affichage des
    # informations du jeu en cours
    obj[-1].font_resize()


def display_all(window, obj):
    """raffraîchit le jeu en faisant afficher une frame,
    contenant les objets dont les caractéristiques ont été
    mis à jour."""
    # création d'une frame
    frame = pygame.Surface(window.size)
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
    display_game_data(obj[5])
    # rafraichissement de la fenêtre pygame
    pygame.display.flip()


def display_game_data(data):
    # utiliser autre méthode si possible
    temp = [1, None, 0, 1, None, 0, 0, 0, 1, 0, 1, 0, 1]
    # création d'une d'un objet pygame.Surface de la taille de l'encadré data
    frame = pygame.Surface((data.rect.w - 2 * data.width, data.rect.h - 2 * data.width))
    # ## en guise de test
    frame.fill(0x440000)
    score = scoring_data_name.render(data.score, 1, (255,255,255))

    rect2 = pygame.Surface(data.font_place)  # 5/13 = 0.2173
    rect2.fill(0x004444)
    frame.blit(rect2, (data.margin // 2, data.margin))

    y = data.margin
    font_h = data.font_rect_dict[0].get_size()
    i = 0
    for e in temp:
        if e == 1:
            frame.blit(data.font_rect_dict[i], (data.margin, y))
            i += 1
            y += font_h[1]
        elif e == None:
            frame.blit(score, (data.margin, y))
            y += font_h[1]
        else:
            y += data.space_between_string

    tetris_window.blit(frame, (data.rect.x + data.width , data.rect.y + data.width))
    pygame.display.flip()


'''def display_game_data(data):
    # création d'une d'un objet pygame.Surface de la taille de l'encadré data
    frame = pygame.Surface((data.rect.w - 2 * data.width, data.rect.h - 2 * data.width))
    # ## en guise de test
    frame.fill(0x440000)
    message_erreur = scoring_data_name.render(data.message, 1, (255,255,255))
    score = scoring_data_name.render(data.score, 1, (255,255,255))

    # ##data.resize_font(score.get_size())
    # score = pygame.transform.scale(score, (score_w //2, score_h //2)) ##

    y = 8
    for i in range(5):
        frame.blit(data.font_rect_dict[i], (data.margin, y))
        size = data.font_rect_dict[i].get_size()
        y += size[1]

    rect2 = pygame.Surface(data.font_place)  # 5/13 = 0.2173
    rect2.fill(0x004444)
    frame.blit(rect2, (data.margin // 2, data.margin))

    w, h = message_erreur.get_size()
    rect3 = pygame.Surface((w, h-(round(2 * (0.218 * h)))))  # 5/13 = 0.2173
    rect3.fill(0x000044)
    frame.blit(rect3, (data.margin, data.margin + 0.218 * h))

    rect = pygame.Surface(score.get_size())
    rect.fill(0x004400)
    frame.blit(rect, (data.margin, data.margin * 5))

    frame.blit(message_erreur, (data.margin, data.margin))
    frame.blit(score, (data.margin, data.margin * 5))
    tetris_window.blit(frame, (data.rect.x + data.width , data.rect.y + data.width))
    pygame.display.flip()'''


# ## voir à déplacer dans un autre fichier ?
def get_file_lst(lang, line, file_name, as_string=True):
    """ renvoie une liste de chaîne de caractères séparées par '|' lorsque
    `line` est spécifiée, sinon elle renvoie la liste de toutes les chaînes
    du fichier texte spécifiés dans le répertoire `lang` contenu dans le
    répertoire "game_string", portant le nom `file_name`, `as_string` s'il
    vaut True convertit la liste en un string avec pour séparateur, le saut
    de ligne """
    # voir à enlever partie si non string en commun
    if lang == '/':
        file = open(f'others/game_string/{file_name}.txt', 'r', encoding='utf-8')
    else:
        path = 'others/game_string/{}/{}.txt'.format(lang, file_name)
        file = open(path, 'r', encoding='utf-8')
    file_as_list = list(file)
    file.close()
    try:
        list_element_line = file_as_list[line-1][:-1].split('|')
        if as_string:
            text = ''
            for element in list_element_line:
                text += element
                text += '\n'
            return text[:-1]
        return list_element_line
    except TypeError:
        return file_as_list


def get_str(lang, file_name, line=None):
    """permet d'obtenir la chaîne de caractère voulue spécifiée par la ligne
    `line` dans le fichier `file_name`."""
    file = get_file_lst(lang, None, file_name)
    return file[line-1][:-1]


# mieux si dans classe, ici pour le moment cause : soucis chemin fichiers
def data_name_list(lang):
    return get_file_lst(lang, 1, 'data_name', False)


# déplacer plus haut lors réorganisation
lang = 'EN'


def gameplay():
    """gameplay du jeu tetris"""
    # ## instanciation à mettre dans une fonction ?
    bag = Bag()
    game_window = Window(window_size)
    matrix = Matrix(game_window)
    next_queue = NextQueue(game_window)
    hold_queue = HoldQueue(game_window)
    menu_button = MenuButton(game_window)
    # voir à déplacer ?
    data = Data(game_window, data_name_list(lang))

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
