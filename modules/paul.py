"""module codé par Paul TG5 (@DominataurusRex), contenant des fonctions utiles
au bon fonctionnement du jeu Tetris."""

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
    return {0:north, 1:east, 2:south, 3:west}


def list_conversion(liste, orientation):
    """Prend une liste `liste` et la renvoie sous forme "compactée"
    par rapport à l'orientation.
    >>> list_conversion(Liste1, 0)
    [[(1, 0), 1], [(0, 1), 2]]
    """
    # Rajoute une coordonnée qui permet seulement de pouvoir parcourir
    # toute la liste. C'est 5 car la coordonnée maximal est 3
    liste.append((5, 5))
    size = len(liste)
    rank = 1
    return_list = []
    # Le nombre de coordonnées côte à côte augmente quand il y en a
    # plusieurs et se réinitialise à chaque différence
    dimension = 1
    # Permet de savoir si cela doit être la coordonnée X ou Y qui doit
    # être identique
    if orientation % 2 == 0:
        spot = 0
    else:
        spot = 1
    # Si il y a plusieurs coordonnées côte à côte, cela garde la
    # première coordonnée, donc la plus petite
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
    for i in range(len(all_side_dict)):
        return_dico[i] = list_conversion(all_side_dict[i], i)
    return return_dico
