"""module contenant les constantes utiles au jeu Tetris."""

COLOR = {'RED': (237, 41, 57),
         'ORANGE': (255, 121, 0),
         'YELLOW': (254, 203, 0),
         'GREEN': (105, 190, 40),
         'CYAN': (0, 159, 218),
         'BLUE': (0, 101, 189),
         'PURPLE': (149, 45, 152),
         'WHITE': (255, 255, 255)}


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


PHASIS_NAME = {0: 'NORTH',
               1: 'EAST',
               2: 'SOUTH',
               3: 'WEST'}


# la rotation "naturelle" est testée avant ces "rotations" spéciaux nécéssitant
# un déplacement des coordonnées, de fait, on utilise un système de translation
ROTATION_POINT = {'3x2': {'NORTH': {'WEST': [(1, -1)],  # 3
                                    'EAST': [(-1, -1)]},  # 3
                          'EAST': {'NORTH': [(1, 0),  # 2
                                             (1, -2),  # 4
                                             (0, -2)],  # 5
                                   'SOUTH': [(1, 0)]},  # 2
                          'WEST': {'SOUTH': [(-1, 0)],  # 2
                                   'NORTH': [(-1, 0),  # 2
                                             (-1, -2),  # 5
                                             (0, -2)]}},  # 4
                  'I': {'NORTH': {'WEST': [(-1, -2)],  # 4
                                  'EAST': [(1, -2)]},  # 5
                        'EAST': {'NORTH': [(-1, 0),  # 3
                                           (2, 0),  # 2
                                           (2, -2)],  # X
                                 'SOUTH': [(-1, 0),  # 2
                                           (2, 0),  # 3
                                           (-1, -3)]},  # X
                        'SOUTH': {'EAST': [(-2, -1)],  # 5
                                  'WEST': [(2, -1)]},  # 4
                        'WEST': {'SOUTH': [(-2, 0),  # 2
                                           (1, -1),  # 3
                                           (1, -3)],  # X
                                 'NORTH': [(-2, 0),  # 3
                                           (1, 0),  # 2
                                           (-2, -2)]}}}  # X


FONT_HEIGHT = [19, 20, 22, 23, 25, 26, 28, 29, 31, 32, 34, 35, 37, 38, 40, 41, 43]


DATA_KEYS = ['score', 'lines', 'level', 'goal']


SIDE = [(0, -1),  # haut
        (1, 0),  # droite
        (0, 1),  # bas
        (-1, 0)]  # gauche
