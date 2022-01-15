# obligation de faire tous les getters et setters ?

import random
import pygame
from others.constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR


def display_visual_tetrimino(surface, tetrimino, y, t_type):
    tetrimino_shape = TETRIMINO_SHAPE[t_type]
    color = COLOR[TETRIMINO_DATA[t_type]['color']]
    x = tetrimino.t_x
    w = tetrimino.t_w
    h = tetrimino.t_h
    width = tetrimino.width // 2 + 1
    # dans le cas où le tetrimino n'est ni 'I' ni 'O'
    # la proba d'obtenir est plus grande, on gagne une comparaison :)
    if t_type > 2:
        cell_size = w // 3
        for j in range(2):
            for k in range(3):
                if tetrimino_shape[j][k]:
                    rect = (x + k * cell_size,
                            y + j * cell_size,
                            cell_size, cell_size)
                    pygame.draw.rect(surface, color, pygame.Rect(rect))
                    pygame.draw.rect(surface, (250, 250, 250),
                                     pygame.Rect(rect), width)
    # si le tetrimino est un 'I' tetrimino
    elif t_type == 2:
        cell_size = w // 4
        shift = (h - cell_size) // 2
        for j in range(4):
            rect = (x + j * cell_size,
                    y + shift,
                    cell_size, cell_size)
            pygame.draw.rect(surface, color, pygame.Rect(rect))
            pygame.draw.rect(surface, (250, 250, 250), pygame.Rect(rect),
                             width)
    # s'il s'agit d'un 'O' tetrimino
    else:
        cell_size = h // 2
        shift = (w - 2 * cell_size) // 2
        for j in range(2):
            for k in range(2):
                rect = (x + k * cell_size + shift,
                        y + j * cell_size,
                        cell_size, cell_size)
                pygame.draw.rect(surface, color, pygame.Rect(rect))
                pygame.draw.rect(surface, (250, 250, 250), pygame.Rect(rect),
                                 width)


def turn_right(tetrimino, phasis):
    if phasis == 0:
        return tetrimino
    else:
        phasis -= 1
        rotated_tetrimino = []
        for i in range(len(tetrimino)):
            tetrimino_line = []
            for j in range(len(tetrimino)-1, -1, -1):
                tetrimino_line.append(tetrimino[j][i])
            rotated_tetrimino.append(tetrimino_line)
    return turn_right(rotated_tetrimino, phasis)


class Bag:

    content = list(range(1, 8))
    # random.shuffle(content)

    def __len__(self):
        return len(Bag.content)

    def __getitem__(self, key):
        # voir à enlever try/except vu que ce ne sera jamais raised ?
        try:
            return Bag.content[key]
        except IndexError:
            return IndexError

    def get_content(self):
        return Bag.content

    def next_tetrimino(self):
        if len(self) < 7:
            # next_generation = list(range(7))
            next_generation = list(range(1, 8))
            random.shuffle(next_generation)
            Bag.content = next_generation + Bag.content
        return Bag.content.pop()

    def resize(self, *args):
        pass

    def display(self, *args):
        pass


# pas très optimal mais au moins ça permet de bien comprendre
def start_center(tetrimino_type):
    return (10 - len(TETRIMINO_SHAPE[tetrimino_type])) // 2


class Tetrimino:

    count = 0

    # création d'un dictionnaire contenant toutes les rotations
    ROTATION_PHASIS = {}
    for i in range(1, 8):
        ROTATION_PHASIS[i] = {}
        for phasis in range(4):
            ROTATION_PHASIS[i][phasis] = turn_right(TETRIMINO_SHAPE[i],
                                                    phasis)

    def __init__(self, Bag):
        self.phasis = 0
        self.current_state = 0
        # self.type = Bag.next_tetrimino() + 1
        self.type = Bag.next_tetrimino()
        print(f"Tetrimino {self.type}")
        self.x = start_center(self.type)
        print(self)
        self.y = 0  # dans skyline
        Tetrimino.count += 1

    # temporaire, pour la visualisation du tetrimino, à enlever à la fin
    def __str__(self):
        stock = ''
        for e in Tetrimino.ROTATION_PHASIS[self.type][self.phasis]:
            stock += ' '.join(str(e))
            stock += '\n'
        stock += f'\n type du tetrimino : {TETRIMINO_SHAPE[self.type]}'
        return stock

    # optimisation possible mais ça rendra la compréhension du code difficile
    # vu que le tout est assez astucieux déjà
    def list_test_around(self):
        """renvoie une liste de trois listes, par indice:
        - 0 pour les test en bas
        - 1 pour les test à gauche
        - 2 pour les test à droite
        """
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
        test_list = [[] for i in range(3)]

        square_len = len(tetrimino_shape)
        last_row = last_column = square_len - 1
        first_column = 0

        # du moment que la liste de test correspondant est vide
        while not test_list[0]:
            for i in range(square_len):
                # ajouter le couple d'indice s'il n'est pas égal à 0
                if tetrimino_shape[last_row][i]:
                    test_list[0].append((last_row, i))
            last_row -= 1

        while not test_list[1]:
            for i in range(square_len):
                if tetrimino_shape[i][first_column]:
                    test_list[1].append((i, first_column))
            first_column += 1

        while not test_list[2]:
            for i in range(square_len):
                if tetrimino_shape[i][last_column]:
                    test_list[2].append((i, last_column))
            last_column -= 1

        return test_list

    # si 2 --> test pour voir si line clear ou autre, puis passage au
    # tetrimino suivant version non finie, il reste à déterminer les cas
    # où le tetrimino sort de la matrice !
    def state(self, Matrix):
        """renvoie:
        - 0 si le tetrimino est en 'falling phase', c'est-à-dire que le
        tetrimino continue à tomber
        - 1 si le tetrimino est en 'lock phase', phase où le tetrimino
        s'apprête à se figer dans la matrice avec un temps escompté
        - 2 lorsque le tetrimino est en 'completion phase'"""
        test_list = self.list_test_around()

        for element in test_list[0]:
            print(element)
            if not Matrix.content[self.x + element[0]][self.y + element[1]]:
                return 1

        """try:
                if Matrix.content[self.x + i][self.y + j] != 0:
                    return 1
            except:
                super_rotation_system()"""
        return 0

    def super_rotation_system(self):
        pass

    def resize(self, *args):
        pass

    def display(self, surface, Matrix):
        tetrimino_shape = self.ROTATION_PHASIS[self.type][self.phasis]
        color = COLOR[TETRIMINO_DATA[self.type]['color']]
        for i in range(len(tetrimino_shape)):
            for j in range(len(tetrimino_shape)):
                if tetrimino_shape[i][j]:
                    rect = (Matrix.x + Matrix.cell_size * (self.x + j),
                            Matrix.y + self.y * Matrix.cell_size + i * Matrix.cell_size,
                            Matrix.cell_size, Matrix.cell_size)
                    """rect = (Matrix.x + self.x * Matrix.cell_size + j * Matrix.cell_size,
                            Matrix.y + self.y * Matrix.cell_size + i * Matrix.cell_size,
                            Matrix.cell_size, Matrix.cell_size)"""
                    pygame.draw.rect(surface, color, pygame.Rect(rect))

    # je ne pense pas qu'il y ait besoin de compléter plus si on fait bien les
    # test avant de permettre au tetrimino de tomber
    def fall(self):
        self.y += 1

    # setters
    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def turn_left(self):
        self.phasis = (self.phasis - 1) % 4

    def turn_right(self):
        self.phasis = (self.phasis + 1) % 4

    # getters
    def get_count(self):
        return Tetrimino.count

    def get_phasis(self):
        return self.phasis

    def get_state(self):
        return self.current_state

    def get_type(self):
        return self.type

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Window:
    def __init__(self, window_size):
        self.width = window_size[0]
        self.height = window_size[1]
        self.size = window_size
        self.margin = round(0.05 * self.height)

    def change_size(self, new_size):
        self.width = new_size[0]
        self.height = new_size[1]
        self.size = new_size
        self.update_margin()

    def update_margin(self):
        self.margin = round(0.05 * self.height)


class Matrix:

    def __init__(self, Window):
        self.resize(Window)
        # création d'une matrice vide avec deux lignes pour la skyline
        self.content = [[0 for j in range(10)] for i in range(22)]
        self.higher_row = 22

    def __str__(self):
        stock = ''
        for i in range(1, 22):
            stock += ' '.join(str(self.content[i]))
            stock += '\n'
        return stock

    def __add__(self, Tetrimino: Tetrimino):
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[Tetrimino.type][Tetrimino.phasis]
        for i in range(len(tetrimino_shape)):
            for j in range(len(tetrimino_shape)):
                if tetrimino_shape[j][i] == 1:
                    self.content[Tetrimino.y + j][Tetrimino.x + i] = Tetrimino.type
                    if Tetrimino.y + j < self.higher_row:
                        self.higher_row = Tetrimino.y + j
                        print(self.higher_row)

    def resize(self, Window: Window, *args):
        # pourrait être enlevé, mais mieux pour compréhension étapes
        remaining_height_spaces = Window.height - 2 * Window.margin
        self.cell_size = remaining_height_spaces // 21
        self.w = self.cell_size * 10
        self.h = self.cell_size * 21
        self.x = (Window.width - self.w) // 2
        self.y = (Window.height - self.h) // 2
        self.width = (self.h // 147) + 1

    def display(self, surface, *args):
        print(self.h)
        pygame.draw.rect(surface, (150, 150, 150),
                         pygame.Rect(self.x, self.y, self.w, self.h),
                         self.width)
        for i in range(22):
            pygame.draw.line(surface, (255, 255, 255),
                             (self.x, self.y + i * self.cell_size),
                             (self.x + self.w, self.y + i * self.cell_size))
        for i in range(10):
            pygame.draw.line(surface, (255, 250, 255),
                             (self.x + i * self.cell_size, self.y),
                             (self.x + i * self.cell_size, self.y + self.h))


class Hold_queue:

    def __init__(self, Window, Matrix):
        self.resize(Window, Matrix)
        self.t_type = 0

    def hold(self, Tetrimino: Tetrimino):
        self.t_type = Tetrimino.type

    def resize(self, Window: Window, Matrix: Matrix):
        # informations générales de l'emplacement de la hold queue
        remaining_space = Window.width - (Matrix.x + Matrix.w) - Window.margin
        self.w = self.h = round(Matrix.cell_size * 3.7)
        self.x = (remaining_space - self.w) * 0.7 + Window.margin
        self.y = Matrix.y
        self.width = self.h // 39 + 1
        # informations de l'emplacement tetrimino
        self.t_w = Matrix.cell_size * 3
        self.t_h = Matrix.cell_size * 2
        self.t_x = self.x + (self.w - self.t_w) // 2
        self.t_y = Matrix.y + (self.w - self.t_h) // 2

    def display(self, surface, *args):
        # représentation de l'encadré
        pygame.draw.rect(surface, (150, 150, 150),
                         pygame.Rect(self.x, self.y, self.w, self.h),
                         self.width)
        # dans le cas où il y a un tetrimino mis de côté, l'afficher
        if self.t_type:
            display_visual_tetrimino(surface, self, self.t_y, self.t_type)


class Next_queue:

    def __init__(self, Window, Matrix):
        self.resize(Window, Matrix)

    def resize(self, Window: Window, Matrix: Matrix):
        matrix_place = Matrix.x + Matrix.w
        remaining_space = Window.width - matrix_place - Window.margin
        # évaluation des paramètres utiles pour définir les encadrés
        self.w = round(Matrix.cell_size * 3.7)
        self.h1 = self.w
        self.h2 = round(Matrix.h*0.9) - self.w
        self.x = (round((remaining_space - self.w) * 0.3)) + matrix_place
        self.y1 = Matrix.y
        self.y2 = round(self.y1 + self.w + (Matrix.h / 10))
        self.width = self.h1 // 39 + 1
        # liste des positions 'y' des différents emplacement des tetriminos
        self.t_w = Matrix.cell_size * 3
        self.t_h = Matrix.cell_size * 2
        self.t_x = self.x + (self.w - self.t_w) // 2
        self.next_y = [self.y1 + (self.w - self.t_h) // 2]
        space = (self.h2 - 5 * self.t_h) // 6
        y = self.y2 + space
        for i in range(5):
            t_place = y
            y += self.t_h + space
            self.next_y.append(t_place)

    def display(self, surface, Bag):
        # conteneur de la prochaine pièce de jeu
        pygame.draw.rect(surface,
                         (150, 150, 150),
                         pygame.Rect(self.x, self.y1, self.w, self.h1),
                         self.width)
        # conteneur des cinq pièces suivantes
        pygame.draw.rect(surface,
                         (150, 150, 150),
                         pygame.Rect(self.x, self.y2, self.w, self.h2),
                         self.width)

        """encadrement (provisoire)
        for i in range(6):
            pygame.draw.rect(surface,(0,0,250),pygame.Rect(self.t_x, self.next_y[i], self.t_w, self.t_h), self.width)"""

        """# représentation sur les bons emplacements des différents tetriminos
        for i in range(1, 7):
            tetrimino_type = Bag.content[-i]
            tetrimino_shape = TETRIMINO_SHAPE[tetrimino_type]
            color = COLOR[TETRIMINO_DATA[tetrimino_type]['color']]
            # dans le cas où le tetrimino n'est ni 'I' ni 'O'
            # la proba d'obtenir est plus grande, on gagne une comparaison :)
            if tetrimino_type > 2:
                cell_size = self.t_w // 3
                for j in range(2):
                    for k in range(3):
                        if tetrimino_shape[j][k]:
                            rect = (self.t_x + k * cell_size,
                                    self.next_y[i - 1] + j * cell_size,
                                    cell_size, cell_size)
                            pygame.draw.rect(surface, color, pygame.Rect(rect),
                                             self.width)
            # si le tetrimino est un 'I' tetrimino
            elif tetrimino_type == 2:
                cell_size = self.t_w // 4
                shift = (self.t_h - cell_size) // 2
                for j in range(4):
                    rect = (self.t_x + j * cell_size,
                            self.next_y[i - 1] + shift,
                            cell_size, cell_size)
                    pygame.draw.rect(surface, color,
                                     pygame.Rect(rect), self.width)
            # s'il s'agit d'un 'O' tetrimino
            else:
                cell_size = self.t_h // 2
                shift = (self.t_w - 2 * cell_size) // 2
                for j in range(2):
                    for k in range(2):
                        rect = (self.t_x + k * cell_size + shift,
                                self.next_y[i - 1] + j * cell_size,
                                cell_size, cell_size)
                        pygame.draw.rect(surface, color,
                                         pygame.Rect(rect), self.width)"""
        for i in range(6):
            display_visual_tetrimino(surface, self, self.next_y[i - 1], Bag.content[-i])


class Verification:

    def line_clear(Matrix: Matrix):
        """renvoie le nombre de line_clear:
        - 1 single
        - 2 double
        - 3 triple"""
        Matrix.higher_row
        pass


class Statistic:

    def stat_view(self):
        nb_tetrimino = Tetrimino.get_count(Tetrimino)
