# Règlement

import pygame

pygame.init()
continuer = True
screen = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)
pygame.display.set_caption("TETRIS")
image = pygame.image.load("image.png").convert_alpha()
pygame.display.set_icon(image)

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

font = pygame.font.Font('freesansbold.ttf', 32)
image2 = pygame.transform.scale(image, (1000, 500))


while continuer:
    width = screen.get_width()
    height = screen.get_height()

    text = font.render('Bonjour', True, (0, 59, 111))
    textRect = text.get_rect()



    textRect.center = (width // 2, height // 2)
    screen.blit(text, textRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
    pygame.display.update()
pygame.quit()
