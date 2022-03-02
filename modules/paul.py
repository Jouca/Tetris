"""module codé par Paul TG5 (@DominataurusRex), contenant des fonctions utiles
au bon fonctionnement du jeu Tetris."""

import pygame
try:
    from constant import LANG
    from diego import GameStrings
    from useful import loop_starter_pack, Button, Button2, Text
except:
    from modules.constant import LANG
    from modules.diego import GameStrings
    from modules.useful import loop_starter_pack, Button, Button2, Text


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
    return {0: north, 1: east, 2: south, 3: west}


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

# Partie Règlement
game_strings = GameStrings(LANG)


def create_main_rule(window):
    """Génère l'affichage de la page règlement"""
    # Mise en place du bouton retour
    back_button = Button2(window,
                          (0.9,
                           0.05,
                           0.04),
                          'back')
    # Mise en place des règles communes, celui du Mode A et du Mode B
    ligne1 = Text(window,
                  (0.25,
                   0.05,
                   0.5,
                   0.08),
                  game_strings.get_string("regle_ligne1"))
    ligne2 = Text(window,
                  (0.25,
                   0.1,
                   0.5,
                   0.08),
                  game_strings.get_string("regle_ligne2"))
    ligne3 = Text(window,
                  (0.25,
                   0.15,
                   0.5,
                   0.08),
                  game_strings.get_string("regle_ligne3"))
    ligne4 = Text(window,
                  (0.25,
                   0.2,
                   0.5,
                   0.08),
                  game_strings.get_string("regle_ligne4"))
    ligne5 = Text(window,
                  (0.25,
                   0.25,
                   0.5,
                   0.08),
                  game_strings.get_string("regle_ligne5"))
    ligneA1 = Text(window,
                   (0.1,
                    0.35,
                    0.4,
                    0.08),
                   game_strings.get_string("regle_ligneA1"))
    ligneA2 = Text(window,
                   (0.1,
                    0.4,
                    0.4,
                    0.08),
                   game_strings.get_string("regle_ligneA2"))
    ligneA3 = Text(window,
                   (0.1,
                    0.45,
                    0.4,
                    0.08),
                   game_strings.get_string("regle_ligneA3"))
    ligneB1 = Text(window,
                   (0.5,
                    0.35,
                    0.4,
                    0.08),
                   game_strings.get_string("regle_ligneB1"))
    ligneB2 = Text(window,
                   (0.5,
                    0.4,
                    0.4,
                    0.08),
                   game_strings.get_string("regle_ligneB2"))
    ligneB3 = Text(window,
                   (0.5,
                    0.45,
                    0.4,
                    0.08),
                   game_strings.get_string("regle_ligneB3"))
    # Mise en place des touches de la colonne de gauche
    arrow_up = Button(window,
                      (0.08,
                       0.55,
                       0.11,
                       0.08),
                      game_strings.get_string("arrow_up"))
    arrow_up_text = Text(window,
                         (0.2,
                          0.56,
                          0.1,
                          0.08),
                         game_strings.get_string("arrow_up_text"), True)
    arrow_left = Button(window,
                        (0.08,
                         0.65,
                         0.11,
                         0.08),
                        game_strings.get_string("arrow_left"))
    arrow_left_text = Text(window,
                           (0.2,
                            0.66,
                            0.1,
                            0.08),
                           game_strings.get_string("arrow_left_text"), True)
    arrow_right = Button(window,
                         (0.08,
                          0.75,
                          0.11,
                          0.08),
                         game_strings.get_string("arrow_right"))
    arrow_right_text = Text(window,
                            (0.2,
                             0.76,
                             0.1,
                             0.08),
                            game_strings.get_string("arrow_right_text"), True)
    arrow_down = Button(window,
                        (0.08,
                         0.85,
                         0.11,
                         0.08),
                        game_strings.get_string("arrow_down"))
    arrow_down_text = Text(window,
                           (0.2,
                            0.86,
                            0.1,
                            0.08),
                           ": Soft Drop", True)

    # Mise en place des touches de la colonne de droite
    escape = Button(window,
                    (0.54,
                     0.55,
                     0.11,
                     0.08),
                    "Echap / F1")
    escape_text = Text(window,
                       (0.66,
                        0.56,
                        0.1,
                        0.08),
                       ": Pause", True)
    turn_left = Button(window,
                       (0.54,
                        0.65,
                        0.11,
                        0.08),
                       "Z / W")
    turn_left_text = Text(window,
                          (0.66,
                           0.66,
                           0.1,
                           0.08),
                          game_strings.get_string("turn_left"), True)
    hold = Button(window,
                  (0.54,
                   0.75,
                   0.11,
                   0.08),
                  "C")
    hold_text = Text(window,
                     (0.66,
                      0.76,
                      0.1,
                      0.08),
                     ": Hold", True)
    space = Button(window,
                   (0.54,
                    0.85,
                    0.11,
                    0.08),
                   game_strings.get_string("space"))
    space_text = Text(window,
                      (0.66,
                       0.86,
                       0.1,
                       0.08),
                      ": Hard Drop", True)
    frame = pygame.Surface(window.get_size())
    # Affichage bouton retour
    back_button.draw(frame)

    # Affichage règle
    ligne1.draw(frame)
    ligne2.draw(frame)
    ligne3.draw(frame)
    ligne4.draw(frame)
    ligne5.draw(frame)
    ligneA1.draw(frame)
    ligneA2.draw(frame)
    ligneA3.draw(frame)
    ligneB1.draw(frame)
    ligneB2.draw(frame)
    ligneB3.draw(frame)
    # Affichage touches colonne gauche
    arrow_up.draw(frame)
    arrow_up_text.draw(frame)
    arrow_left.draw(frame)
    arrow_left_text.draw(frame)
    arrow_right.draw(frame)
    arrow_right_text.draw(frame)
    arrow_down.draw(frame)
    arrow_down_text.draw(frame)
    # Affichage touches colonne droite
    escape.draw(frame)
    escape_text.draw(frame)
    turn_left.draw(frame)
    turn_left_text.draw(frame)
    hold.draw(frame)
    hold_text.draw(frame)
    space.draw(frame)
    space_text.draw(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()
    return back_button


def main_rule(window):
    """Permet de rendre fonctionnel l'affichage du règlement"""
    back_button = create_main_rule(window)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                back_button = create_main_rule(window)
            if back_button.is_pressed(event):
                proceed = False
                return
