def ghost_left_right(x):
     liste_gauche = []
     liste_droite = []
     for i in range(len(TETRIMINO_SHAPE[x])):
          mini = 5
          maxi = 0
          collone = 10
          for j in range(len(TETRIMINO_SHAPE[x][i])):
               if TETRIMINO_SHAPE[x][i][j] == 1:
                    if j < mini:
                         liste_gauche.append((i, j))
                         mini = j
                    if j >= maxi:
                         collone = j
          if collone != 10:
               liste_droite.append((i, collone))
     return liste_droite, liste_gauche


def ghost_top_down(x):
     liste_haut = []
     liste_bas = []
     lenght = len(TETRIMINO_SHAPE[x])
     for j in range(lenght):
          mini = 5
          maxi = 0
          ligne = 10
          for i in range(lenght):
               if TETRIMINO_SHAPE[x][i][j] == 1:
                    if i < mini:
                         liste_haut.append((i, j))
                         mini = i
                    if i >= maxi:
                         ligne = i
          if ligne != 10:
               liste_bas.append((ligne, j))
     return liste_haut, liste_bas



print(ghost_left_right(5))
print(ghost_top_down(5))
