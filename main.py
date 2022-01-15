# problème avec le resize de la next_queue


# importations des librairies python
import pygame
import tkinter
import sys
import time
import termcolor
from solene import Bag, Hold_queue, Matrix, Next_queue, Tetrimino, Window

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

# personnlalisation de la fenêtre
pygame.display.set_caption("TETRIS")
pygame.display.set_icon(icon)

# pygame.draw.rect(window,(0,0,250),pygame.Rect(0,0, WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.flip()

window_size = pygame.display.get_surface().get_size()


def resize_all(Window, Object):
    for element in Object:
        element.resize(Window, Object[2])


def display_all(Window, Object, resize=False):
    frame = pygame.Surface(Window.size)
    if resize:
        resize_all(Window, Object)
    """for element in Object:
        element.display(frame, Object[-1])"""
    # pour la next_queue qui est particulière
    Object[3].display(frame, Object[0])
    Object[1].display(frame, Object[2])
    """# le reste
    for element in Object[3:]:
        element.display(frame)"""
    Object[2].display(frame)
    Object[4].display(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()


game_window = Window(window_size)
bag = Bag()
matrix = Matrix(game_window)
next_queue = Next_queue(game_window, matrix)
hold_queue = Hold_queue(game_window, matrix)

tetrimino = Tetrimino(bag)

Object = (bag, tetrimino, matrix, next_queue, hold_queue)

display_all(game_window, Object)

while True:

    # stocke la valeur actuelle de la taille de la fenêtre
    window_current_size = pygame.display.get_surface().get_size()

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
                print(tetrimino.get_x())

            if event.key == pygame.K_LEFT:
                tetrimino.move_left()
                print(tetrimino.get_x())

            if event.key == pygame.K_UP:
                tetrimino.turn_right()
                print(tetrimino.get_phasis())

            if event.key == pygame.K_c:
                hold_queue.hold(tetrimino)
                tetrimino = Tetrimino(bag)
            
            Object = (bag, tetrimino, matrix, next_queue, hold_queue)
            display_all(game_window, Object)

    # time.sleep(2)
