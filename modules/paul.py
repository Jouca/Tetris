def get_all_side(tetrimino_shape):
    """Renvoie un dictionnaire avec la liste des blocs aux
    extremités dans chaque orientation."""
    north = []
    east = []
    south = []
    west = []
    taille = len(tetrimino_shape)
    for i in range(taille):
        min_north = 5
        max_east = 0
        max_south = 0
        min_west = 5
        column, row = 10, 10
        for j in range(taille):
            if tetrimino_shape[i][j] == 1:
                if j < min_west:
                    west.append((i, j))
                    min_west = j
                if j >= max_east:
                    column = j
            if tetrimino_shape[j][i] == 1:
                if j < min_north:
                    north.append((j, i))
                    min_north = j
                if j >= max_south:
                    row = j
        if column != 10:
            east.append((i, column))
        if row != 10:
            south.append((row, i))
    return {"0":north, "1":east, "2":south, "3":west}


def list_conversion(Liste, Orientation):
    """Prend une liste `Liste` et la renvoie sous forme "compactée"
    par rapport à l'orientation.
    >>> list_conversion(Liste1, 0)
    [[(1, 0), 1], [(0, 1), 2]]
    """
    Liste.append((5, 5))
    Taille = len(Liste)
    Rang = 1
    Liste_Retour = []
    Dimension = 1
    if Orientation % 2 == 0:
        Place = 0
    else:
        Place = 1
    Cloud = Liste[0]
    while Rang < Taille:
        if Cloud[Place] != Liste[Rang][Place]:
            Liste_Retour.append([Cloud, Dimension])
            Cloud = Liste[Rang]
            Dimension = 1
        elif Cloud[Place] == Liste[Rang][Place]:
            Dimension += 1
        Rang += 1
    return Liste_Retour


def border_dict(tetrimino_shape):
    """Renvoie un dictionnaire des bloc à l'extremité de chaque côté."""
    all_side_dict = get_all_side(tetrimino_shape)
    Dico_Retour = {}
    for l in range(len(all_side_dict)):
        Dico_Retour[str(l)] = list_conversion(all_side_dict[str(l)], l)
    return Dico_Retour
