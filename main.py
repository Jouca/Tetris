"""fichier python principal du jeu Tetris codé en tant que projet de deuxième
trimestre pour la spécialité NSI."""


# importations des librairies python
import pygame
import pygame.freetype
from modules.bastien import main_menu

# pylint: disable=E1101
# (no-member) erreur apparaissant pour les constantes de pygame référant aux
# touches de clavier et boutons de fenêtre, ...

# initialisation de pygame
pygame.init()

# préréglage du module mixer
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.music.set_volume(0.4)

# charge la musique
pygame.mixer.music.load("./sound/korobeiniki.ogg")
# la joue indéfiniment
pygame.mixer.music.play(-1)

# définition de variables de fenêtre
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
icon = pygame.image.load("./image/logo.ico").convert_alpha()


# personnalisation de la fenêtre
pygame.display.set_caption("TETRIS")
pygame.display.set_icon(icon)


if __name__ == "__main__":
    main_menu(tetris_window)
