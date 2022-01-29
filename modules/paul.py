def get_all_side(tetrimino_shape):
    """Renvoie un dictionnaire avec la liste des blocs aux
    extremités dans chaque orientation."""
    north = []
    east = []
    south = []
    west = []
    size = len(tetrimino_shape)
    for i in range(size):
        min_north = 5
        max_east = 0
        max_south = 0
        min_west = 5
        column, row = 10, 10
        for j in range(size):
            if tetrimino_shape[i][j] == 1:
                if j < min_west:
                    west.append((i, j))
                    min_west = j
                if j > max_east:
                    column = j
            if tetrimino_shape[j][i] == 1:
                if j < min_north:
                    north.append((j, i))
                    min_north = j
                if j > max_south:
                    row = j
        if column != 10:
            east.append((i, column))
        if row != 10:
            south.append((row, i))
    return {"0":north, "1":east, "2":south, "3":west}


def list_conversion(liste, orientation):
    """Prend une liste `Liste` et la renvoie sous forme "compactée"
    par rapport à l'orientation.
    >>> list_conversion(Liste1, 0)
    [[(1, 0), 1], [(0, 1), 2]]
    """
    # Rajoute une coordonnée bidon qui permet seulement de pouvoir parcourir toute la liste
    # C'est 5 car la coordonnée maximal est 3
    liste.append((5, 5))
    size = len(liste)
    rank = 1
    return_list = []
    # Le nombre de coordonnée côte à côte, augmente quand il y en a plusieur et
    # se réinitialise à chaque différence
    dimension = 1
    # Permet de savoir si cela doit être la coordonnée X ou Y qui doit être identique
    if orientation % 2 == 0:
        spot = 0
    else:
        spot = 1
    # Si il y a plusieur coordonnée côte à côte, cela garde la première coordonnée, donc la plus petite
    backup = liste[0]
    while rank < size:
        if backup[spot] != liste[rank][spot]:
            return_list.append([backup, dimension])
            backup = liste[rank]
            dimension = 1
        elif backup[spot] == liste[rank][spot]:
            dimension += 1
        rank += 1
    return return_list


def border_dict(tetrimino_shape):
    """Renvoie un dictionnaire des bloc à l'extremité de chaque côté."""
    all_side_dict = get_all_side(tetrimino_shape)
    return_dico = {}
    for l in range(len(all_side_dict)):
        return_dico[l] = list_conversion(all_side_dict[l], l)
    return return_dico


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

