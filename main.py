import pygame
import tkinter
import sys
import time
from solene import Bag, Hold_queue, Matrix, Next_queue, Tetrimino, Window

pygame.init()


#préréglage du module mixer
pygame.mixer.pre_init(44100,-16,2,1024)
pygame.mixer.music.set_volume(0.4)


tk = tkinter.Tk()
tk.withdraw()

FULLSCREEN_WIDTH = tk.winfo_screenwidth()

WINDOW_HEIGHT = round(tk.winfo_screenheight() * 2/3)
WINDOW_WIDTH = round(WINDOW_HEIGHT * 1.8)


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


window_size = pygame.display.get_surface().get_size()



def resize_all(Window, Object):
    for element in Object:
        element.resize(Window, Object[0])

def display_all(Window, Object, resize = False):
    frame = pygame.Surface(Window.size)
    if resize:
        resize_all(Window, Object)
    for element in Object:
        element.display(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()



game_window = Window(window_size)
bag = Bag()
matrix = Matrix(game_window)
next_queue = Next_queue(game_window, matrix)
hold_queue = Hold_queue(game_window, matrix)
# à placer dans boucle principale dans la partie generation
tetrimino = Tetrimino(bag)

Object = (matrix, next_queue, hold_queue)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            try:
                print(game_window.size, FULLSCREEN_SIZE)
                if game_window.size == FULLSCREEN_SIZE:
                    pygame.draw.rect(window,(0,0,250),pygame.Rect(0,0, 1700,200))
                    pygame.display.flip()
                    pygame.quit()
                    sys.exit()
            except NameError:
                FULLSCREEN_SIZE = pygame.display.get_surface().get_size()

        window_current_size = pygame.display.get_surface().get_size()
        if game_window.size != window_current_size:
            game_window.change_size(window_current_size)
            print(game_window.size)
            display_all(game_window, Object, True)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
