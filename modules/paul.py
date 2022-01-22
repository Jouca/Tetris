def Dico_ghost(x):
    """Renvoie un dictionnaire avec la liste des blocs au extrémiter dans chaque orientation"""
    haut = []
    droite = []
    bas = []
    gauche = []
    taille = len(TETRIMINO_SHAPE[x])
    for i in range(taille):
        min_haut = 5
        max_droite = 0
        max_bas = 0
        min_gauche = 5
        collone, ligne = 10, 10
        for j in range(taille):
            if TETRIMINO_SHAPE[x][i][j] == 1:
                if j < min_gauche:
                    gauche.append((i, j))
                    min_gauche = j
                if j >= max_droite:
                    collone = j
            if TETRIMINO_SHAPE[x][j][i] == 1:
                if j < min_haut:
                    haut.append((j, i))
                    min_haut = j
                if j >= max_bas:
                    ligne = j
        if collone != 10:
            droite.append((i, collone))
        if ligne != 10:
            bas.append((ligne, i))
    return {"0":haut, "1":droite, "2":bas, "3":gauche}


def Convert_Liste(Liste, Orientation):
    """Prend un Liste et la renvoie sous forme compacté par rapport à l'orientation
    >>>Convert_Liste(Liste1, 0)
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


def Ghost(X):
    """Renvoie un dictionnaire des bloc à l'extrémiter de chaque côté"""
    Dico = Dico_ghost(X)
    Dico_Retour = {}
    for l in range(len(Dico)):
        Dico_Retour[str(l)] = Convert_Liste(Dico[str(l)], l)
    return Dico_Retour


