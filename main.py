# importations des librairies python
import pygame
import tkinter
import sys
import time
import termcolor
from solene import Bag, HoldQueue, Matrix, NextQueue, Tetrimino, Window, Data

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


# définition de la fenêtre pygame de taille dynamique
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                 pygame.RESIZABLE)

# importation d'images
icon = pygame.image.load("icon.jpg").convert_alpha()
prop = pygame.image.load("prop2.png").convert_alpha()
"""window.blit(prop, (55, 16))
pygame.display.flip()"""

# personnalisation de la fenêtre
pygame.display.set_caption("TETRIS")
pygame.display.set_icon(icon)
window_size = pygame.display.get_surface().get_size()


def resize_all(Window, Object):
    """"redimensionne tous les objets nécéssitant d'être
    redimensionnés."""
    for element in Object[2:]:
        element.resize(Window)


def display_all(Window, Object, resize=False):
    """raffraîchit le jeu en faisant afficher une frame,
    contenant les objets dont les caractéristiques ont été
    mis à jour. Dans le cas où resize est spécifié au booléen
    True, les objets sont redimensionnés."""
    frame = pygame.Surface(Window.size)
    if resize:
        resize_all(Window, Object)
    """for element in Object:
        element.display(frame, Object[-1])"""
    # pour la next_queue qui est particulière
    Object[3].display(frame, Object[0])
    # tetrimino particulier
    Object[1].display(frame, Object[2])
    Object[2].display(frame)
    Object[5].display(frame)
    Object[4].display(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()

# ## instanciation à mettre dans une fonction ?
bag = Bag()
game_window = Window(window_size)
matrix = Matrix(game_window)
next_queue = NextQueue(game_window)
hold_queue = HoldQueue(game_window)
data = Data(game_window)

tetrimino = Tetrimino(bag)

Object = (bag, tetrimino, matrix, next_queue, hold_queue, data)

display_all(game_window, Object)
time_before_refresh = time.time()

while True:

    # stocke la valeur actuelle de la taille de la fenêtre
    window_current_size = pygame.display.get_surface().get_size()
    Object = (bag, tetrimino, matrix, next_queue, hold_queue, data)
    current_time = time.time()
    time_elapsed = current_time - time_before_refresh

    # évènements pygame
    for event in pygame.event.get():
        # appui sur la croix de la fenêtre
        if event.type == pygame.QUIT:
            # fermeture de la fenêtre
            pygame.quit()
            sys.exit()

        """# appui sur le boutton redimensionner de la fenêtre
        if event.type == pygame.VIDEORESIZE:
            # test merdique, reprendrais plus tard
            try:
                print(game_window.size, FULLSCREEN_SIZE)
                if game_window.size == FULLSCREEN_SIZE:
                    pygame.draw.rect(window, (0, 0, 250),
                                     pygame.Rect(0, 0, 1700, 200))
                    pygame.display.flip()
                    #pygame.quit()
                    #sys.exit()
            except NameError:
                FULLSCREEN_SIZE = pygame.display.get_surface().get_size()"""

        # dans le cas où l'utilisateur change la taille de la fenêtre
        if game_window.size != window_current_size:
            # mise à jour des attributs de l'objet Window
            game_window.change_size(window_current_size)
            print(game_window.size)
            # reaffichage avec changement des tailles et emplacement des objets
            display_all(game_window, Object, True)

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

        # ##guise de test
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                tetrimino = Tetrimino(bag)
                termcolor.cprint(bag.get_content(), 'red')
        
            if event.key == pygame.K_RIGHT:
                tetrimino.move_right()

            if event.key == pygame.K_LEFT:
                tetrimino.move_left()

            if event.key == pygame.K_UP:
                tetrimino.turn_right()

            if event.key == pygame.K_c:
                temp = hold_queue.get_t_type()
                hold_queue.hold(tetrimino)
                # dans le cas où la hold queue n'est pas vide
                if temp:
                    tetrimino.set_type(temp)
                    tetrimino.set_y(0)
                else:
                    tetrimino = Tetrimino(bag)

            display_all(game_window, Object)

    # l'égalité entre int et float n'est pas efficace
    if time_elapsed > data.refresh:
        tetrimino.fall()
        time_before_refresh = time.time()
        display_all(game_window, Object)
