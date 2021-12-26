import pygame
import tkinter
import sys
import time

pygame.init()


#préréglage du module mixer
pygame.mixer.pre_init(44100,-16,2,1024)
pygame.mixer.music.set_volume(0.4)


tk = tkinter.Tk()
tk.withdraw()

WINDOW_HEIGHT = round(tk.winfo_screenheight()*2/3) # 512
WINDOW_WIDTH = round(WINDOW_HEIGHT * 1.8) # 922

print(WINDOW_WIDTH,WINDOW_HEIGHT)
#définition de la fenêtre pygame
#window = pygame.display.set_mode((0, 0)WINDOW_WIDTH,WINDOW_HEIGHT))
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)

icon =  pygame.image.load("icon.jpg").convert_alpha()
prop =  pygame.image.load("prop2.png").convert_alpha()
window.blit(prop, (55,16))
pygame.display.flip()

pygame.display.set_caption("TETRIS")
pygame.display.set_icon(icon)

#pygame.draw.rect(window,(0,0,250),pygame.Rect(0,0, WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.flip()


wh, hh = pygame.display.get_surface().get_size()



def matrix_size(window_width, window_height):
    margin = round(0.05 * window_height)
    # pourrait être enlevé, mais mieux pour compréhension étapes
    remaining_height_spaces = window_height - 2 * margin
    cell_size = remaining_height_spaces // 21
    pos_x = (window_width - cell_size * 10) // 2
    pos_y = (window_height - cell_size * 21) // 2
    return pos_x, pos_y, cell_size, margin


# reste à ajouter les différents autres encadrés : hold queue, next queue, ...
def resize_object(w, h):
    # en ce qui concerne la matrice
    x, y, cell_size, margin = matrix_size(w, h)
    window.fill(0x000000)
    pygame.display.flip()
    time.sleep(1)
    pygame.draw.rect(window,(250,0,0),pygame.Rect(x, y, cell_size*10, cell_size*21))
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #if event.type == pygame.VIDEORESIZE:
            #pygame.draw.rect(window,(0,0,250),pygame.Rect(0,0, 1700,200))
        #    pygame.display.flip()

        w, h = pygame.display.get_surface().get_size()
        if (wh, hh) != (w, h):
            wh, hh = w, h
            print(w, h)

            resize_object(w, h)

        #if event.type == pygame.KEYDOWN:
        #    pygame.quit()
        #    sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
