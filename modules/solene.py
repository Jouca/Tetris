"""module codé par Zheng Solène TG8, contenant diverses classes et
fonctions utiles au bon fonctionnement du jeu Tetris."""

# pylint: disable=W0231
# (super-init-not-called), il m'est inutile de faire appel à la méthode
# constructeur des classes parent vu que leur méthode constructeur font appel
# à une méthode présente dans la même classe nommée "resize". C'est dans la
# méthode du même nom ("resize") que je fais appel à la classe parent.
# Comprenez que j'évite d'attribuer des attributs inutiles à une classe et que
# les classes parents sont avant tout pratique pour les positions relatives
# des différents objets entre eux.

# importation de librairies python utiles
import random
import colorsys
import pygame
from others.constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR, PHASIS_NAME, ROTATION_POINT
from diego import clear_lines
from paul import border_dict


def display_visual_tetrimino(surface, place_properties, y, t_type):
    """permet de définir un tetrimino visuel, notamment pour la hold
    queue et la next queue, ce, sans création d'un objet tetrimino.
    Prend en paramètre :
    - `surface`, un objet pygame.Surface ;
    - `place_properties`, un objet HoldQueue ou NextQueue, utile afin de
    récupérer des informations de l'emplacement du tetrimino visuel ;
    - `y` : la position y, particulière de l'emplacement du tetrimino visuel
    sous la forme d'un int ;
    - `t_type` : le type du tetrimino indiqué par un entier compris entre 1
    et 7 inclus"""
    tetrimino_shape = TETRIMINO_SHAPE[t_type]
    # ##color = COLOR[TETRIMINO_DATA[t_type]['color']]
    color = Tetrimino.COLOR_SHADE[t_type][0]
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


def change_color_luminosity(color, rate_of_change):
    """change la luminosité de la couleur, renvoie un tuple rgb de la couleur
    assombrie selon `rate_of_change`, un entier. `couleur` doit être un tuple
    représentant les valeurs rgb (chaque entier est compris entre 0 et 255)."""
    red, green, blue = color
    hue, saturation, lightness = colorsys.rgb_to_hsv(red, green, blue)
    temp_color = colorsys.hsv_to_rgb(hue, saturation, lightness - rate_of_change)
    final_color = [0, 0, 0]
    for i, primary in enumerate(temp_color):
        final_color[i] = round(primary)
    return tuple(final_color)


# j'aurais préféré mettre une
class Window:
    """objet stockant les propriétés de la fenêtre."""

    def __init__(self, window_size):
        """initialisation de l'instance."""
        self.change_size(window_size)
        # pylint n'est pas content lorsque l'on ne définit pas
        # l'attribut margin dans la méthode constructeur
        self.update_margin()

    def change_size(self, new_size):
        """la taille de la fenêtre est mise à jour."""
        self.width = new_size[0]
        self.height = new_size[1]
        self.size = new_size
        self.update_margin()

    def update_margin(self):
        """met à jour la valeur de la marge."""
        self.margin = round(0.05 * self.height)


class Bag:
    """modélise un sac contenant l'ordre des tetrimino suivant
    représentés par un numéro correspondant à leur type."""

    content = list(range(1, 8))
    # ##content = [5 for _ in range(10)]
    random.shuffle(content)

    def __len__(self):
        """renvoie le nombre de tetrimino en attente."""
        return len(Bag.content)

    def next_tetrimino(self):
        """renvoie le prochain tetrimino et fait en sorte qu'il
        y ait toujours au moins 5 tetrimino en attente."""
        if len(self) < 6:
            next_generation = list(range(1, 8))
            random.shuffle(next_generation)
            Bag.content = next_generation + Bag.content
        return self.content.pop()


class Matrix:
    """modélisation de matrix dans laquelle tombe les tetrimino."""

    def __init__(self, window):
        """initialisation des différents attribut de la classe Matrix."""
        self.resize(window)
        self.content = [[0 for j in range(10)] for i in range(22)]
        # création d'une matrice vide avec deux lignes pour la skyline
        self.higher_row = 22

    # ##temporaire
    def __str__(self):
        stock = ''
        for i in range(1, 22):
            stock += ' '.join(str(self.content[i]))
            stock += '\n'
        return stock

    def __add__(self, tetrimino):
        """méthode spéciale permettant d'utiliser l'opérateur '+' pour
        lock down un `tetrimino`, un objet de la classe `Tetrimino`."""
        t_type = tetrimino.type
        t_phasis = tetrimino.phasis
        tetrimino_shape = tetrimino.ROTATION_PHASIS[t_type][t_phasis]
        tetrimino_lenght = len(tetrimino_shape)
        for i in range(tetrimino_lenght):
            for j in range(tetrimino_lenght):
                if tetrimino_shape[j][i] == 1:
                    pos_y = tetrimino.y + j
                    pos_x = tetrimino.x + i
                    self.content[pos_y][pos_x] = tetrimino.type
                    if tetrimino.y + j < self.higher_row:
                        self.higher_row = tetrimino.y + j
                        print(self.higher_row)

    def clear_lines(self, data):
        """voir dans `diego.py`"""
        self.content, nb_line_cleared = clear_lines(self.content)
        data.add_to_line_clear(nb_line_cleared)

    def resize(self, window):
        """redimmensionne les valeurs utile à la représentation
        graphique de matrix. La fonction permet la création d'un dictionnaire
        pratique à la représentation des mino."""
        # pourrait être enlevé, mais mieux pour compréhension étapes
        remaining_height_spaces = window.height - 2 * window.margin
        self.cell_size = remaining_height_spaces // 21
        self.w = self.cell_size * 10
        self.h = self.cell_size * 21
        self.x = (window.width - self.w) // 2
        self.y = (window.height - self.h) // 2
        self.width = round(self.cell_size * 3/10)
        # création d'un attribut de classe de type dictionnaire
        # contenant des objets de type pygame.Rect pour chaque case
        Matrix.cell = {}
        y = self.y - self.width
        for i in range(10):
            Matrix.cell[i] = {}
            for j in range(21):
                x = self.x + i * self.cell_size
                if j == 0:
                    Matrix.cell[i][1] = pygame.Rect(x,
                                                    self.y,
                                                    self.cell_size,
                                                    self.cell_size * 7/10)
                else:
                    Matrix.cell[i][j+1] = pygame.Rect(x,
                                                      y + j * self.cell_size,
                                                      self.cell_size,
                                                      self.cell_size)

    def display(self, surface):
        """dessine matrix selon ses attributs sur une surface `surface` devant
        être du type pygame.Surface."""

        for i in range(1, 22):
            for j in range(10):
                current_cell = self.content[i][j]
                if current_cell:
                    # affichage d'un mino de matrix
                    # ##color = COLOR[TETRIMINO_DATA[current_cell]['color']]
                    color = Tetrimino.COLOR_SHADE[current_cell][0]
                    pygame.draw.rect(surface,
                                     color, self.cell[j][i])

        # demo toutes les cases, première et dernière de matrix visible
        '''for e in self.cell:
            for i in range(10):
                for j in range(1, 22):
                    # ##couleurs sympa garder pour mode spécial ?
                    color = (i*4, j*4, 40)
                    pygame.draw.rect(surface, color, self.cell[i][j])
        pygame.draw.rect(surface, (250, 0, 0), self.cell[0][1])
        pygame.draw.rect(surface, (0, 250, 0), self.cell[9][21])'''

        # dessin de la grille
        # lignes horizontales du quadrillage de matrix
        for i in range(1, 22):
            grid_y = self.cell[1][i].y
            pygame.draw.line(surface, (255, 255, 255),
                             (self.x, grid_y),
                             (self.x + self.w, grid_y))
        # lignes verticales du quadrillage de matrix
        for i in range(1, 10):
            grid_x = self.cell[i][1].x
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


class Tetrimino(Bag, Matrix):
    """modélise un tetrimino."""

    # compteur intéressant pour les informations en fin de partie
    count = 0

    # création d'un dictionnaire contenant toutes les rotations
    ROTATION_PHASIS = {}
    for i in range(1, 8):
        ROTATION_PHASIS[i] = {}
        for phasis in range(4):
            ROTATION_PHASIS[i][phasis] = turn_right(TETRIMINO_SHAPE[i],
                                                    phasis)

    # création du dictionnaire utile aux ghost pieces et aux test alentours
    BORDER = {}
    for i in range(1, 8):
        BORDER[i] = {}
        for phasis in range(4):
            BORDER[i][phasis] = border_dict(ROTATION_PHASIS[i][phasis])

    # création d'un dictionnaire des teintes pour le lock phase
    COLOR_SHADE = {}
    for tetrimino_type in range(1, 8):
        color = TETRIMINO_DATA[tetrimino_type]['color']
        color_rgb = COLOR[color]
        COLOR_SHADE[tetrimino_type] = {0: color_rgb}
        for shade in range(1, 10):
            previous_color = COLOR_SHADE[tetrimino_type][shade-1]
            changed_color = change_color_luminosity(previous_color, 14)
            COLOR_SHADE[tetrimino_type][shade] = changed_color

    @staticmethod
    def start_center(tetrimino_type):
        """indique l'indice permettant de centrer un tetrimino
        selon son type (spécifié en argument de la fonction, un
        entier compris entre 1 et 7 inclus) dans matrice."""
        return (10 - len(TETRIMINO_SHAPE[tetrimino_type])) // 2

    def __init__(self):
        """initialise une instance avec l'attribution de la phase à 0 ("Nord"),
        l'état à : 0 ("falling phase"), le type dépendant de la pièce en
        attente de l'instance de Bag et les attributs `x` et `y` tels qu'ils
        indique leur position en fonction d'une instance Matrix de sorte que
        l'instance créée soit centré dans la skyline."""
        self.phasis = 0
        self.state = 0
        self.type = self.next_tetrimino()
        # définit la nuance de couleur du tetrimino
        self.shade = 0
        # position centrée horizontalement
        self.x = Tetrimino.start_center(self.type)
        # dans la skyline (en haut de la matrice)
        self.y = 0
        # incrémente le nombre de tetrimino créé de 1
        Tetrimino.count += 1
        # ##à enlever en fin
        print(f"Tetrimino {self.type}")
        print(self)

    # ##temporaire, pour la visualisation du tetrimino, à enlever à la fin
    def __str__(self):
        """ceci est une docstring pylint :)"""
        stock = ''
        for element in Tetrimino.ROTATION_PHASIS[self.type][self.phasis]:
            stock += ' '.join(str(element))
            stock += '\n'
        stock += f'\n type du tetrimino : {TETRIMINO_SHAPE[self.type]}'
        return stock

    # si 2 --> test pour voir si line clear ou autre, puis passage au
    # tetrimino suivant version non finie, il reste à déterminer les cas
    # où le tetrimino sort de la matrice !
    def current_state(self):
        """renvoie:
        - 0 si le tetrimino est en 'falling phase', c'est-à-dire que le
        tetrimino continue à tomber
        - 1 si le tetrimino est en 'lock phase', phase où le tetrimino
        s'apprête à se figer dans la matrice avec un temps escompté
        - 2 lorsque le tetrimino est en 'completion phase'"""

    def can_fall(self, matrix):
        """test afin de vérifier si un tetrimino peut tomber.
        Il prend en paramètre `matrix` une instance de la classe Matrix,
        et renvoie un booléen correspondant à l'issue du test (succès ou
        échec)."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
        nb_column = len(tetrimino_shape)
        self.y += 1
        if self.test_around(matrix, tetrimino_shape, nb_column):
            return True
        # rétablit la valeur y du tetrimino
        self.y -= 1
        return False

    def test_around(self, matrix, tetrimino_shape, nb_column):
        """les test de super rotation system sont effectuées dans cette
        fonction. Elle renvoie un booléen, True lorsque le test est passé
        avec succès, False sinon.
        `tetrimino_shape` est la forme prise par le tetrimino une fois tournée,
        `nb_column` est la longueur du tetrimino, il s'agit d'un entier, valant
        4 lorsqu'il s'agit d'un I tetrimino, 3 autrement, les test pour le O
        tetrimino ne sont jamais réalisés puisqu'il est inutile d'appliquer une
        rotation."""
        # initialisation d'un compteur de mino réussissant le test
        count = 0
        try:
            # parcours de la matrice représentatant le tetrimino
            for i, row in enumerate(tetrimino_shape):
                for j in range(nb_column):
                    mino = row[j]
                    # le mino ne sort pas de matrix
                    if mino and j + self.x > -1:
                        # cellule de matrix libre pour mino
                        if matrix.content[i + self.y][j + self.x] == 0:
                            # reussite du test par mino
                            count += 1
            # dans le cas où les quatre mino réussissent le test
            if count == 4:
                return True
        # dans le cas où un mino n'appartient pas à matrix
        except IndexError:
            return False
        return False

    def super_rotation_system(self, matrix, phasis):
        """super rotation système décrit par la guideline de Tetris,
        permet de faire tourner un tetrimino bien que la situation
        ne soit pas confortable à la manoeuvre en temps habituel (contre
        un bord de matrix, sur la floor, ...).
        La fonction effectue des test en changeant les coordonnées x, y
        d'un tetrimino via des translations et non de rotation avec un
        point de rotation comme le suggère la guideline.
        `matrix` est un objet de la classe Matrix.
        `phasis` est la phase vers laquelle le tetrimino doit tourner.
        La fonction renvoie un booléen selon si la pièce peut tourner ou non,
        elle change les attributs x et y de l'instance avant d'effectuer les
        test, si tous échouent, les valeurs initiales de ces deux attributs
        sont rétablis."""
        # ne rien faire dans le cas d'un O tetrimino
        if self.type == 1:
            return True
        # s'il s'agit d'un tetrimino 3x2 : (L, J, S, Z, T)
        if self.type != 2:
            t_type = '3x2'
            nb_column = 3
        # autrement, il s'agit d'un I tetrimino
        else:
            t_type = 'I'
            nb_column = 4
        # ## test pour les situation de rotation à enlever en fin
        print(f'{PHASIS_NAME[self.phasis]}  -->  {PHASIS_NAME[phasis]}')
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][phasis]
        # optimisable, mais comme cela on a une économie en calcul
        # je privilégie la performance :) (et puis, pas besoin de mettre
        # (0, 0) dans le dictionnaire des test à chaque fois x))
        if self.test_around(matrix, tetrimino_shape, nb_column):
            return True
        # dans le cas où la rotation au point de rotation naturel échoue
        # on fait appel à d'autres test existants
        current_phasis = PHASIS_NAME[self.phasis]
        next_phasis = PHASIS_NAME[phasis]
        coordinates = (self.x, self.y)
        try:
            test_list = ROTATION_POINT[t_type][current_phasis][next_phasis]
            for rotation_test in test_list:
                # déplacement des coordonnées selon les test
                self.x = coordinates[0] + rotation_test[0]
                self.y = coordinates[1] + rotation_test[1]
                if self.test_around(matrix, tetrimino_shape, nb_column):
                    return True
        # s'opère lorsque phasis vaut SOUTH pour un tetrimino 3x2
        # il n'y a pas de test supplémentaire donc ne peut pas tourner
        except KeyError:
            print('turn point : FAIL')
            self.x = coordinates[0]
            self.y = coordinates[1]
            return False
        # dans le cas où tous les test échouent
        print('turn point : FAIL')
        self.x = coordinates[0]
        self.y = coordinates[1]
        return False

    # fonction améliorable
    def lock_phase(self, matrix, phase): ## continuer docstring une fois finie
        """il s'agit de la phase où le tetrimino est sur le point de se bloquer,
        elle fait en sorte de varier la couleur du tetrimino afin que le joueur
        puisse mieux prendre en compte la situation du tetrimino."""
        # dans le cas où le tetrimino peut tomber
        if self.can_fall(matrix):
            # permet de sortir de la lock phase
            self.state = 0
            self.shade = 0
            # on renvoie 1 afin de reinitialiser phase
            return 1
        # dans le cas où la phase vaut 1
        if phase == 1:
            # on assombrit la couleur du tetrimino
            self.shade += 1
        # autrement
        else:
            # la couleur est eclaircie
            self.shade -= 1
        # si la couleur atteint un des "bords"
        if self.shade in (0, 9):
            # on change de phase
            phase = (phase + 1) % 2
        return phase
    
    def display(self, surface):
        """affiche l'instance de tetrimino en fonction de ses spécificités."""
        tetrimino_shape = self.ROTATION_PHASIS[self.type][self.phasis]
        color = Tetrimino.COLOR_SHADE[self.type][self.shade]
        for i, row in enumerate(tetrimino_shape):
            for j in range(len(tetrimino_shape)):
                if row[j]:
                    # affichage mino par mino sur matrix
                    # ## devrait pouvoir enlever ceci
                    try:
                        pygame.draw.rect(surface,
                                         color,
                                         self.cell[j+self.x][i+self.y])
                    except KeyError:
                        pass

    def leftmost(self):
        """renvoie le plus petit coordonnée x possédé par un mino."""
        # on selectionne les bords gauche du tetrimino
        left = Tetrimino.BORDER[self.type][self.phasis][3]
        left_most = 4
        for shift in left:
            if shift[0][1] < left_most:
                left_most = shift[0][1]
        return left_most + self.x

    # ## n'est pas utilisé pour le moment, voir par la suite
    def rightmost(self):
        """renvoie la plus grande valeur x d'un mino."""
        # on selectionne les bords droit du tetrimino
        right = Tetrimino.BORDER[self.type][self.phasis][1]
        right_most = 0
        for shift in right:
            if shift[0][1] + shift[1] > right_most:
                right_most = shift[0][1]
        return right_most + self.x

    def fall(self, matrix):
        """permet de faire tomber le tetrimino, s'il ne peut pas,
        le tetrimino passe en lock phase. A pour paramètre une instance de
        la classe Matrix."""
        # teste si le tetrimino est apte à tomber
        if self.can_fall(matrix):
            return
        # le test a échoué, le tetrimino ne peut pas tomber,
        # on passe en lock phase
        self.state = 1

    def move_left(self, matrix):
        """déplace d'une case vers la gauche le tetrimino."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
        nb_column = len(tetrimino_shape)
        # dans le cas où le mino le plus à gauche n'est pas adjacent au mur
        if self.leftmost() > 0:
            self.x -= 1
            if self.test_around(matrix, tetrimino_shape, nb_column):
                return
            # le test a échoué, le tetrimino ne peut pas aller à gauche
            self.x += 1

    def move_right(self, matrix):
        """déplace d'une case vers la droite le tetrimino."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
        nb_column = len(tetrimino_shape)
        self.x += 1
        if self.test_around(matrix, tetrimino_shape, nb_column):
            return
        # le test a échoué, le tetrimino ne peut pas aller à droite
        self.x -= 1

    # ##penser à l'implémentationo quand méthode turn_right ok
    def turn_left(self, matrix):
        """permet de tourner le tetrimino de 90° dans le sens
        horaire."""
        phasis = (self.phasis - 1) % 4
        if self.super_rotation_system(matrix, phasis):
            self.phasis = phasis

    def turn_right(self, matrix):
        """permet de tourner le tetrimino de 90° dans le sens
        anti-horaire."""
        phasis = (self.phasis + 1) % 4
        if self.super_rotation_system(matrix, phasis):
            self.phasis = phasis

    def set_type(self, new_type):
        """change le type d'un tetrimino pour `new_type` un entier
        naturel compris entre 1 et 7 inclus."""
        self.type = new_type

    def set_y(self, value):
        """place le tetrimino à la position `value` spécifié.
        `value` doit être un int compris entre 0 et 21 compris."""
        self.y = value

    def get_count(self):
        """renvoie le nombre de tetrimino créés."""
        return self.count

    def get_state(self):
        """renvoie l'état du tetrimino."""
        return self.current_state

    def get_type(self):
        """renvoie le type du tetrimino."""
        return self.type

    # ## docstring foireuses à améliorer par la suite en fonction
    # vu que pas forcément vrai avec super rotation system
    def get_x(self):
        """renvoie la position x du tetrimino relatif à matrix.
        - 0 s'il est dans la colonne la plus à gauche ;
        - 8, valeur maximale pour la colonne la plus à droite
        possible pour un tetrimino"""
        return self.x

    def get_y(self):
        """renvoie la position y du tetrimino dans matrix.
        - 0 s'il est dans la partie supérieure à la skyline ;
        - 1, dans la skyline ;
        - 20, valeur maximale pouvant être renvoyée (si on prend
        un O tetrimino sachant que sa représentation se fait sur
        une matrice 2x2)."""
        return self.y


class HoldQueue(Matrix):
    """modélise la hold queue, là où les tetrimino sont mis sur le côté et
    pouvant être rappelé dans le jeu à tout moment à raison d'une fois par
    tetrimino."""

    def __init__(self, window):
        """initialisation de l'instance par l'attribution de ses valeurs
        pratique à sa représentation. L'attribut t_type est à 0 : il n'y a
        pas de tetrimino hold."""
        self.resize(window)
        self.t_type = 0
        self.can_hold = True

    def hold(self, tetrimino):
        """permet de hold une pièce. `tetrimino` doit être une instance
        de la classe Tetrimino."""
        self.t_type = tetrimino.type
        self.can_hold = False

    def resize(self, window):
        """redimensionne selon les valeurs de `Window` une instance de la
        classe Window."""
        # informations générales de l'emplacement de la hold queue
        super().resize(window)
        remaining_space = window.width - (self.x + self.w) - window.margin
        self.w = self.h = round(self.cell_size * 3.7)
        self.x = (remaining_space - self.w) * 0.7 + window.margin
        self.width = self.h // 39 + 1
        # informations de l'emplacement tetrimino
        self.t_w = self.cell_size * 3
        self.t_h = self.cell_size * 2
        self.t_x = self.x + (self.w - self.t_w) // 2
        self.t_y = self.y + (self.w - self.t_h) // 2

    def display(self, surface):
        """affichage de l'encadré associé à la hold queue, avec si y a le
        type du tetrimino hold."""
        # représentation de l'encadré
        pygame.draw.rect(surface, (150, 150, 150),
                         pygame.Rect(self.x, self.y, self.w, self.h),
                         self.width)
        # dans le cas où il y a un tetrimino mis de côté, l'afficher
        try:
            if self.t_type:
                display_visual_tetrimino(surface, self, self.t_y, self.t_type)
        # afin de ne pas définir un attribut t_type à des instances de
        # MenuButton et Data
        except AttributeError:
            pass

    def get_t_type(self):
        """renvoie le type du tetrimino dans la hold_queue, un int compris
        entre 0 et 7 inclus. 0 signifiant que la hold queue est vide."""
        return self.t_type


class NextQueue(Bag, Matrix):
    """modélisation de la next queue dans laquelle sont représentés les six
    prochaines pièces de la partie en cours."""

    def __init__(self, window):
        """méthode constructeur de la classe."""
        self.resize(window)

    def resize(self, window):
        """permet d'après les données de `Window` de redimensionner l'encadré
        grâce à la mise à jour des attributs de l'instance concernant cela."""
        super().resize(window)
        matrix_place = self.x + self.w
        remaining_space = window.width - matrix_place - window.margin
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
        for _ in range(5):
            t_place = y
            y += self.t_h + space
            self.next_y.append(t_place)

    def display(self, surface):
        """affiche des encadrés correspondant à la next queue dans lesquelles
        figurent les tetrimino en attente dans l'instance de `Bag`, `surface`
        doit être un objet de type pygame.Surface."""
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
        # affichage des tetrimino suivant contenu dans bag
        for i in range(6):
            display_visual_tetrimino(surface, self,
                                     self.next_y[i - 1], self.content[-i])


class MenuButton(HoldQueue):
    """crée le boutton de jeu."""

    def __init__(self, window):
        """initialisation de l'instance."""
        self.resize(window)

    def resize(self, window):
        """redimensionne selon les valeurs de `Window` une instance de la
        classe Window."""
        # informations générales de l'emplacement de la hold queue
        super().resize(window)
        self.w = self.h = self.w // 2
        self.x = window.width - window.margin - self.w
        self.width = self.h // 39 + 1

    # ###
    def bind(self):
        """affichage dans le cas où le boutton est appuyé."""


class Data(HoldQueue):
    """regroupe les données relatifs aux informations du jeu, ainsi que les
    attributs permettant de tracer l'encadré d'affichage du score, niveau,
    nombre de line clear."""

    def __init__(self, window):
        """méthode constructeur de la classe. Initialise le score les données
        d'une parties."""
        self.resize(window)
        self.score = 0
        self.level = 1
        self.line_clear = 0
        self.set_refresh()

    def set_refresh(self):
        """met à jour la valeur du temps entre chaque frame du jeu en accord
        avec la guideline officiel du jeu."""
        self.refresh = (0.8 - (self.level - 1) * 0.007) ** (self.level - 1)

    def resize(self, window):
        """change les attributs relatifs aux dimensions de l'encadré."""
        # informations générales de l'emplacement de l'encadré
        super().resize(window)
        self.x = self.x - self.w
        # ##si la marge n'est pas respectée
        if self.x > window.margin:
            pass
        self.w = self.w * 2
        self.y = self.y + self.h * 2
        self.h = self.cell_size * 21 - self.y + window.margin
        # changer en information pour le texte
        """# informations de l'emplacement tetrimino
        self.t_w = self.cell_size * 3
        self.t_h = self.cell_size * 2
        self.t_x = self.x + (self.w - self.t_w) // 2
        self.t_y = self.y + (self.w - self.t_h) // 2"""

    def add_to_line_clear(self, value_to_add):
        """ajoute `value_to_add` au nombre de line_clear."""
        self.line_clear += value_to_add
