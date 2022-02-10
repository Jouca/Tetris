"""module codé par Bastien (@BLASTQ) TG8, contenant des fonctions pour
les menus du jeu Tetris. Repassage du code par Solène, (@periergeia)."""

import pygame
import sys
from diego import Button
from useful import get_font_size
from constant import COLOR

pygame.init()


# CODE DANS main.py
#########################################################
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

icon = pygame.image.load("./image/window_logo.png").convert_alpha()
menubutton = pygame.image.load("./image/menubutton.png").convert_alpha()

pygame.display.set_caption("TETRIS")
pygame.display.set_icon(icon)


################################################################



### import img ###
logo = pygame.image.load('./image/logo.jpg').convert_alpha()
menu_background = pygame.image.load('./image/menu_background2.png').convert_alpha()
### import img ###

### import font ###
myfont = pygame.font.SysFont("./others/Anton-Regular.ttf", 30)
### import font ###


def loop_starter_pack(event):
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


def create_main_menu(window):
    logo_height = window.get_height() // 4
    logo_size = (round(340 * logo_height / 153), logo_height)
    logo_to_display = pygame.transform.scale(logo, logo_size)
    logo_pos = (window.get_width() - logo_size[0]) // 2, round(window.get_height() * 0.15)

    window_w = window.get_width()
    
    play_button = Button(window, (logo_pos[0] / window_w,
                         0.45, logo_size[0] / window_w, 0.15), "JOUER")
    ranking_button = Button(window,
                            (logo_pos[0] / window_w,
                             0.65,
                             (logo_size[0] / window_w) * 0.65,
                             0.15),
                            "CLASSEMENT")
    help_button = Button(window,
                         (logo_pos[0] / window_w + (logo_size[0] / window_w) * 0.65,
                          0.65,
                          (logo_size[0] / window_w) * 0.35,
                          0.15),
                         "AIDE")
    
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
            loop_starter_pack(event)
            if event.type == pygame.VIDEORESIZE:
                play_button, ranking_button, help_button = create_main_menu(window)
            if play_button.is_pressed(event):
                game_choice_menu(window)
                proceed = False
                return
            if ranking_button.is_pressed(event):
                menuplay()
                proceed = False
                return
            if help_button.is_pressed(event):
                menuplay()
                proceed = False
                return


def create_game_choice_menu(window):
    font_height = round(0.15 * window.get_height())
    font_size = get_font_size(font_height)
    font = pygame.font.SysFont("./others/Anton-Regular.ttf", font_size)
    statement = font.render('SELECTIONNEZ  UN  MODE', 1 , COLOR['WHITE'])
    menu_background_to_display = pygame.transform.scale(menu_background, window.get_size())
    mode_a_button = Button(window,
                            (0.175,
                             0.4,
                             0.3,
                             0.4),
                            "MODE  A", font_size)
    mode_b_button = Button(window,
                         (0.525,
                          0.4,
                          0.3,
                          0.4),
                         "MODE  B", font_size)

    frame = pygame.Surface(window.get_size())
    frame.blit(menu_background_to_display, (0, 0))
    frame.blit(statement, ((window.get_width() - statement.get_width()) // 2, round(0.175 * window.get_height())))
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
            loop_starter_pack(event)
            if event.type == pygame.VIDEORESIZE:
                mode_a_button, mode_b_button = create_game_choice_menu(window)
            if mode_a_button.is_pressed(event):
                game_choice_menu(window)
                proceed = False
                return
            elif mode_b_button.is_pressed(event):
                menuplay()
                proceed = False
                return
            '''elif back_button.is_pressed(event):
                main_menu()
                proceed = False
                return'''


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





lang = 'EN'

# provisoire, sans les menus
level = 1
mode_B = False


if __name__ == "__main__":
    main_menu(tetris_window)


