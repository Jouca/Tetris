from telnetlib import LOGOUT
import pygame

pygame.init()

continuer = True
screen = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)
pygame.display.set_caption("TETRIS")
image = pygame.image.load("prix.png").convert_alpha()
pygame.display.set_icon(image)

### import img ###
logo = pygame.image.load('ressources/TETRIS.png').convert_alpha()
### import img ###

class Button:
    pass

def menu1():
    screen.blit(logo, (100, 100))
    pygame.display.flip()


while continuer:
    menu1()
