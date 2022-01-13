COLOR = {'RED': (237, 41, 57),
         'ORANGE': (255, 121, 0),
         'YELLOW': (254, 203, 0),
         'GREEN': (105, 190, 40),
         'CYAN': (0, 159, 218),
         'BLUE': (0, 101, 189),
         'PURPLE': (149, 45, 152)}


TETRIMINO_DATA = {1: {'name': 'O',
                      'color': 'YELLOW',
                      'monochrome': ''},
                  2: {'name': 'I',
                      'color': 'CYAN',
                      'monochrome': ''},
                  3: {'name': 'T',
                      'color': 'PURPLE',
                      'monochrome': ''},
                  4: {'name': 'L',
                      'color': 'ORANGE',
                      'monochrome': ''},
                  5: {'name': 'J',
                      'color': 'BLUE',
                      'monochrome': ''},
                  6: {'name': 'S',
                      'color': 'GREEN',
                      'monochrome': ''},
                  7: {'name': 'Z',
                      'color': 'RED',
                      'monochrome': ''}}


TETRIMINO_SHAPE = {1: [[1, 1],
                       [1, 1]],
                   2: [[0, 0, 0, 0],
                       [1, 1, 1, 1],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]],
                   3: [[0, 1, 0],
                       [1, 1, 1],
                       [0, 0, 0]],
                   4: [[0, 0, 1],
                       [1, 1, 1],
                       [0, 0, 0]],
                   5: [[1, 0, 0],
                       [1, 1, 1],
                       [0, 0, 0]],
                   6: [[0, 1, 1],
                       [1, 1, 0],
                       [0, 0, 0]],
                   7: [[1, 1, 0],
                       [0, 1, 1],
                       [0, 0, 0]]}


# l'utilité est moyen, serviable plus tard pour les statistiques eventuellement
ROTATION_PHASIS_NAME = {0: 'N',
                        1: 'E',
                        2: 'S',
                        3: 'W'}


# pour se réprer, le dico n'a aucune utilité en soi
TETRIMINO_STATE = {0: 'falling',
                   1: 'lock_down'}


SIDE = [(0, -1),  # haut
        (1, 0),  # droite
        (0, 1),  # bas
        (-1, 0)]  # gauche
