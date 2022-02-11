import pygame
import sys
try:
    from constant import FONT_HEIGHT
except ModuleNotFoundError:
    from modules.constant import FONT_HEIGHT


def get_font_size(font_height):
    if font_height < 19:
        return 12
    else:
        i = 0
        while font_height > FONT_HEIGHT[i]:
            i += 1
        return i + 12


def loop_starter_pack(tetris_window, event):
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
    return tetris_window
