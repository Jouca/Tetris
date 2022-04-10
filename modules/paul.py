"""module codé par Paul TG5 (@DominataurusRex), contenant des fonctions utiles
au bon fonctionnement du jeu Tetris."""

import pygame
try:
    from constant import LANG
    from diego import GameStrings
    from useful import loop_starter_pack, Button1, Button2, Text
except:
    from modules.constant import LANG
    from modules.diego import GameStrings
    from modules.useful import loop_starter_pack, Button1, Button2, Text


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
    frame = pygame.Surface(window.get_size())
    # Mise en place du bouton retour
    back_button = Button2(window,
                          (0.9, 0.05, 0.04),
                          'back')
    back_button.draw(frame)

    # Mise en place des règles communes
    for line in range(1, 6):
        text = Text(window,
                    (0.25, (0.05 * line), 0.5, 0.08),
                    game_strings.get_string("regle_ligne" + str(line)))
        text.draw(frame)

    # Mise en place des règles du Mode A et du Mode B
    list_regle = ["A1", "A2", "A3", "B1", "B2", "B3"]
    for line in range(3):
        for side in range(2):
            x_value = 0.1 + (0.4 * side)
            y_value = 0.35 + (0.05 * line)
            text_pos = line + (side * 3)
            text = Text(window,
                        (x_value, y_value, 0.4, 0.08),
                        game_strings.get_string("regle_ligne" + list_regle[text_pos]))
            text.draw(frame)
    
    # Mise en place des touches des deux colonnes
    list_touch = ["arrow_up", "arrow_left", "arrow_right", "arrow_down",
                  "escape", "turn_left", "hold", "space"]
    for touch in range(4):
        for side in range(2):
            x_value_button = 0.08 + (0.46 * side)
            x_value_text = 0.2 + (0.46 * side)
            y_value = 0.55 + (0.1 * touch)
            text_pos = touch + (side * 4)
            button = Button1(window,
                             (x_value_button, y_value, 0.11, 0.08),
                             game_strings.get_string(list_touch[text_pos]))
            text = Text(window,
                        (x_value_text, y_value, 0.1, 0.08),
                        game_strings.get_string(list_touch[text_pos] + "_text"), True)
            button.draw(frame)
            text.draw(frame)

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
