import random
import pygame
from others.constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR


def display_visual_tetrimino(surface, place_properties, y, t_type):
    """permet de définir un tetrimino visuel, notamment pour la hold
    queue et la next queue, ce, sans création d'un objet tetrimino.
    Prend en paramètre :
    - `surface`, un objet pygame.Surface ;
    - `place_properties`, un objet Hold_queue ou Next_queue, utile afin de
    récupérer des informations de l'emplacement du tetrimino visuel ;
    - `y` : la position y, particulière de l'emplacement du tetrimino visuel
    sous la forme d'un int ;
    - `t_type` : le type du tetrimino indiqué par un entier compris entre 1
    et 7 inclus"""
    tetrimino_shape = TETRIMINO_SHAPE[t_type]
    color = COLOR[TETRIMINO_DATA[t_type]['color']]
    x = place_properties.t_x
    w = place_properties.t_w
    h = place_properties.t_h
    width = place_properties.width // 2 + 1
    # dans le cas où le tetrimino n'est ni 'I' ni 'O'
    # placé en début on gagne une comparaison :)
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
    """fait tourner une pièce tetrimino avec une rotation
    vers la droite. Utilise la récursivité.
    - tetrimino : modélisé par une matrice ;
    - phasis : un entier compris entre 0 et 3.
    Renvoie une matrice correspondant à la phase indiquée.
    >>> turn_right([[0, 0, 1], [1, 1, 1], [0, 0, 0]], 2)
    [[0, 0, 0], [1, 1, 1], [1, 0, 0]]
    >>> turn_right([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]], 3)
    [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]"""
    if phasis == 0:
        return tetrimino
    phasis -= 1
    rotated_tetrimino = []
    for i in range(len(tetrimino)):
        tetrimino_line = []
        for j in range(len(tetrimino)-1, -1, -1):
            tetrimino_line.append(tetrimino[j][i])
        rotated_tetrimino.append(tetrimino_line)
    return turn_right(rotated_tetrimino, phasis)


class Bag:
    """modélise un sac contenant l'ordre des tetrimino suivant
    représentés par un numéro correspondant à leur type."""

    def __init__(self):
        """initialisation de l'instance avec la première génération de
        tetrimino sans oublier la randomisation de l'ordre."""
        self.content = list(range(1, 8))
        random.shuffle(self.content)

    def __len__(self):
        """renvoie le nombre de tetrimino en attente."""
        return len(self.content)

    def __getitem__(self, key):
        """renvoie l'élément du sac d'indice `key`."""
        # ##voir à enlever try/except vu que ce ne sera jamais raised ?
        try:
            return self.content[key]
        except IndexError:
            return IndexError

    # ##voir à enlever
    def get_content(self):
        """renvoie le contenu du sac."""
        return self.content

    def next_tetrimino(self):
        """renvoie le prochain tetrimino et fait en sorte qu'il
        y ait toujours au moins 5 tetrimino en attente."""
        if len(self) < 6:
            next_generation = list(range(1, 8))
            random.shuffle(next_generation)
            self.content = next_generation + self.content
        return self.content.pop()


def start_center(tetrimino_type):
    """indique l'indice permettant de centrer un tetrimino
    selon son type (spécifié en argument de la fonction, un
    entier compris entre 1 et 7 inclus) dans matrice."""
    return (10 - len(TETRIMINO_SHAPE[tetrimino_type])) // 2


class Tetrimino:
    """modélise un tetrimino"""

    # compteur intéressant pour les informations en fin de partie
    count = 0

    # création d'un dictionnaire contenant toutes les rotations
    ROTATION_PHASIS = {}
    for i in range(1, 8):
        ROTATION_PHASIS[i] = {}
        for phasis in range(4):
            ROTATION_PHASIS[i][phasis] = turn_right(TETRIMINO_SHAPE[i],
                                                    phasis)

    def __init__(self, Bag):
        """initialise une instance avec l'attribution de la phase à 0 ("Nord"),
        l'état à : 0 ("falling phase"), le type dépendant de la pièce en
        attente de l'instance de Bag et les attributs `x` et `y` tels qu'ils
        indique leur position en fonction d'une instance Matrix de sorte que
        l'instance créée soit centré dans la skyline."""
        self.phasis = 0
        self.current_state = 0
        self.type = Bag.next_tetrimino()
        # position centrée horizontalement
        self.x = start_center(self.type)
        # dans la skyline (en haut de la matrice)
        self.y = 0
        # incrémente le nombre de tetrimino créé de 1
        Tetrimino.count += 1
        # ##à enlever en fin
        print(f"Tetrimino {self.type}")
        print(self)

    # ##temporaire, pour la visualisation du tetrimino, à enlever à la fin
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

    def display(self, surface, Matrix):
        y = Matrix.y - 3/10 * Matrix.cell_size
        tetrimino_shape = self.ROTATION_PHASIS[self.type][self.phasis]
        color = COLOR[TETRIMINO_DATA[self.type]['color']]
        for i in range(len(tetrimino_shape)):
            for j in range(len(tetrimino_shape)):
                if tetrimino_shape[i][j]:
                    # affichage mino par mino sur matrix
                    mino_x = Matrix.x + (j+self.x) * Matrix.cell_size
                    mino_y = y + (i+self.y) * Matrix.cell_size
                    pygame.draw.rect(surface,
                                     color,
                                     pygame.Rect(mino_x,
                                                 mino_y,
                                                 Matrix.cell_size,
                                                 Matrix.cell_size))
        # dissimule la partie n'appartenant pas à la matrice
        if self.y == 0:
            pygame.draw.rect(surface, (0, 0, 0),
                             pygame.Rect(Matrix.x,
                                         Matrix.y - Matrix.cell_size,
                                         Matrix.w,
                                         Matrix.cell_size))

    # setters
    def fall(self):
        """permet de faire tomber le tetrimino."""
        self.y += 1

    def move_left(self):
        """déplace d'une case vers la gauche le tetrimino."""
        self.x -= 1

    def move_right(self):
        """déplace d'une case vers la droite le tetrimino."""
        self.x += 1

    def turn_left(self):
        """permet de tourner le tetrimino de 90° dans le sens
        horaire."""
        self.phasis = (self.phasis - 1) % 4

    def turn_right(self):
        """permet de tourner le tetrimino de 90° dans le sens
        anti-horaire."""
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
        t_type = Tetrimino.type
        t_phasis = Tetrimino.phasis
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[t_type][t_phasis]
        for i in range(len(tetrimino_shape)):
            for j in range(len(tetrimino_shape)):
                if tetrimino_shape[j][i] == 1:
                    pos_y = Tetrimino.y + j
                    pos_x = Tetrimino.x + i
                    self.content[pos_y][pos_x] = Tetrimino.type
                    if Tetrimino.y + j < self.higher_row:
                        self.higher_row = Tetrimino.y + j
                        print(self.higher_row)

    def resize(self, Window: Window):
        # pourrait être enlevé, mais mieux pour compréhension étapes
        remaining_height_spaces = Window.height - 2 * Window.margin
        self.cell_size = remaining_height_spaces // 21
        self.w = self.cell_size * 10
        self.h = self.cell_size * 21
        self.x = (Window.width - self.w) // 2
        self.y = (Window.height - self.h) // 2
        # self.width = (self.h // 147) + 1
        self.width = round(self.cell_size * 3/10)

    def display(self, surface, *args):
        # variable utile pour dessiner la skyline
        y = self.y - 3/10 * self.cell_size
        for i in range(self.higher_row, 22):
            for j in range(10):
                current_cell = self.content[i][j]
                if current_cell:
                    # affichage d'un mino de matrix
                    color = COLOR[TETRIMINO_DATA[current_cell]['color']]
                    pygame.draw.rect(surface,
                                     color,
                                     pygame.Rect(self.x + j * self.cell_size,
                                                 y + i * self.cell_size,
                                                 self.cell_size,
                                                 self.cell_size))

        # dessin de la grille
        for i in range(1, 21):
            grid_y = y + i * self.cell_size
            pygame.draw.line(surface, (255, 255, 255),
                             (self.x, grid_y),
                             (self.x + self.w, grid_y))
        for i in range(1, 10):
            grid_x = self.x + i * self.cell_size
            pygame.draw.line(surface, (255, 255, 255),
                             (grid_x, self.y),
                             (grid_x, self.y + self.h - self.width))
        # lignes de bords
        # haut
        pygame.draw.rect(surface, (150, 0, 0),
                         pygame.Rect(self.x,
                                     self.y,
                                     self.w,
                                     self.width))
        # bas
        pygame.draw.rect(surface, (150, 150, 150),
                         pygame.Rect(self.x,
                                     self.y + self.h - self.width,
                                     self.w,
                                     self.width))
        # gauche
        pygame.draw.rect(surface, (150, 150, 150),
                         pygame.Rect(self.x - self.width,
                                     self.y,
                                     self.width,
                                     self.h))
        # droite
        pygame.draw.rect(surface, (150, 150, 150),
                         pygame.Rect(self.x + 10 * self.cell_size,
                                     self.y,
                                     self.width,
                                     self.h))
        # efface imperfection du rectangle initialement tracé
        if self.higher_row == 0:
            pygame.draw.rect(surface, (0, 0, 0),
                             pygame.Rect(self.x,
                                         self.y - self.cell_size,
                                         self.w,
                                         self.cell_size))


class Hold_queue(Matrix):

    def __init__(self, Window):
        self.resize(Window)
        self.t_type = 0

    def hold(self, Tetrimino):
        self.t_type = Tetrimino.type

    def resize(self, Window):
        # informations générales de l'emplacement de la hold queue
        super().resize(Window)
        remaining_space = Window.width - (self.x + self.w) - Window.margin
        self.w = self.h = round(self.cell_size * 3.7)
        self.x = (remaining_space - self.w) * 0.7 + Window.margin
        self.width = self.h // 39 + 1
        # informations de l'emplacement tetrimino
        self.t_w = self.cell_size * 3
        self.t_h = self.cell_size * 2
        self.t_x = self.x + (self.w - self.t_w) // 2
        self.t_y = self.y + (self.w - self.t_h) // 2

    def display(self, surface):
        # représentation de l'encadré
        pygame.draw.rect(surface, (150, 150, 150),
                         pygame.Rect(self.x, self.y, self.w, self.h),
                         self.width)
        # dans le cas où il y a un tetrimino mis de côté, l'afficher
        if self.t_type:
            display_visual_tetrimino(surface, self, self.t_y, self.t_type)


class Next_queue(Matrix):

    def __init__(self, Window):
        self.resize(Window)

    def resize(self, Window):
        super().resize(Window)
        matrix_place = self.x + self.w
        remaining_space = Window.width - matrix_place - Window.margin
        # évaluation des paramètres utiles pour définir les encadrés
        self.w = round(self.cell_size * 3.7)
        self.h_1 = self.w
        self.h_2 = round(self.h*0.9) - self.w
        self.x = (round((remaining_space - self.w) * 0.3)) + matrix_place
        self.y_1 = self.y
        self.y_2 = round(self.y_1 + self.w + (self.h / 10))
        self.width = self.h_1 // 39 + 1
        # liste des positions 'y' des différents emplacement des tetriminos
        self.t_w = self.cell_size * 3
        self.t_h = self.cell_size * 2
        self.t_x = self.x + (self.w - self.t_w) // 2
        self.next_y = [self.y_1 + (self.w - self.t_h) // 2]
        space = (self.h_2 - 5 * self.t_h) // 6
        y = self.y_2 + space
        for i in range(5):
            t_place = y
            y += self.t_h + space
            self.next_y.append(t_place)

    def display(self, surface, Bag):
        # conteneur de la prochaine pièce de jeu
        pygame.draw.rect(surface,
                         (150, 150, 150),
                         pygame.Rect(self.x, self.y_1, self.w, self.h_1),
                         self.width)
        # conteneur des cinq pièces suivantes
        pygame.draw.rect(surface,
                         (150, 150, 150),
                         pygame.Rect(self.x, self.y_2, self.w, self.h_2),
                         self.width)
        # encadrement (provisoire)
        for i in range(6):
            pygame.draw.rect(surface, (0, 0, 250),
                             pygame.Rect(self.t_x, self.next_y[i],
                                         self.t_w, self.t_h), self.width)
        # affichage des tetrimino suivant contenu dans bag
        for i in range(6):
            display_visual_tetrimino(surface, self,
                                     self.next_y[i - 1], Bag.content[-i])


class Verification():
    """regroupe les fonction de vérification sur les différents objets
    du jeu."""

    def line_clear(self, Matrix: Matrix):
        """renvoie le nombre de line_clear:
        - 1 single
        - 2 double
        - 3 triple"""
        Matrix.higher_row
        pass


class Data(Hold_queue):
    """regroupe les données relatifs aux informations du jeu, ainsi que les
    attributs permettant de tracer l'encadré d'affichage du score, niveau,
    nombre de line clear."""

    # pylint: disable=W0231
    # (super-init-not-called), il m'est inutile de faire appel à la méthode
    # constructeur de Hold_queue vu qu'elle même fait appel à la méthode resize
    # que j'utilise dans la méthode du même nom dans cette classe.

    def __init__(self, Window):
        """méthode constructeur de la classe. Initialise le score à 0"""
        self.resize(Window)
        self.t_type = 0
        self.score = 0
        self.level = 1
        self.set_refresh()

    def set_refresh(self):
        """met à jour la valeur du temps entre chaque frame du jeu en accord avec
        la guideline officiel du jeu."""
        self.refresh = (0.8 - (self.level - 1) * 0.007) ** (self.level - 1)

    def resize(self, _Window):
        """change les attributs relatifs aux dimensions de l'encadré."""
        # informations générales de l'emplacement de l'encadré
        super().resize(_Window)
        self.x = self.x - self.w
        self.w = self.w * 2
        self.y = self.y + self.h * 2
        self.h = self.cell_size * 21 - self.y + _Window.margin
        # changer en information pour le texte
        """# informations de l'emplacement tetrimino
        self.t_w = self.cell_size * 3
        self.t_h = self.cell_size * 2
        self.t_x = self.x + (self.w - self.t_w) // 2
        self.t_y = self.y + (self.w - self.t_h) // 2"""
