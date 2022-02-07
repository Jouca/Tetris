import black
import pygame
from diego import Button

pygame.init()

continuer = True
screen = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)
pygame.display.set_caption("TETRIS")
image = pygame.image.load("./image_save/LOGOPROVISOIRE.png").convert_alpha()
pygame.display.set_icon(image)

### import img ###
logo = pygame.image.load('./image_save/logo.jpg').convert_alpha()
logo = pygame.transform.scale(logo, (300, 150))
### import img ###

### import font ###
myfont = pygame.font.SysFont("./others/Anton-Regular.ttf", 30)
### import font ###


def mainmenu():
    play = Button((195, 220, 605,  100), "JOUER", 50, (250, 250, 250))
    help = Button((505, 340, 295, 100), "AIDE", 50, (250, 250, 250))
    classement = Button((195, 340, 295, 100), "CLASSEMENT", 50, (250, 250, 250))

    screen.blit(logo, (350, 50))
    play.draw(screen)
    help.draw(screen)
    classement.draw(screen)
    if play.event_handler(event):
        
        screen.fill((0, 0, 0))
        menuplay()
    pygame.display.flip()
    """classement.draw(screen)
    if play.event_handler():
    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                print("test")"""

def menuplay():
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 10000, 40000))
    pygame.display.flip()
    aa = Button((195, 230, 605,  100), "aa", 50, (250, 250, 250))
    modeA = Button((195, 200, 295, 190), "MODE A", 50, (250, 250, 250))
    modeB = Button((505, 200, 295, 190), "MODE B", 50, (250, 250, 250))
    screen.blit(logo, (350, 50))
    modeA.draw(screen)
    modeB.draw(screen)
    """aa.draw(screen)"""
    if modeA.event_handler(event):
        print("try")
    pygame.display.flip()

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

while continuer:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
    mainmenu()