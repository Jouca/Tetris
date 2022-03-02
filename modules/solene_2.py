"""module codé par Solène (@periergeia) TG8, contenant diverses classes et
fonctions utiles au bon fonctionnement du jeu Tetris."""


# importation de librairies python
import random
import pygame
import pygame.freetype
try:
    import solene_1 as sln
    from constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR
    from constant import ROTATION_POINT, PHASIS_NAME, MULTIPLY_BY
    from diego import clear_lines
    from paul import border_dict
except ModuleNotFoundError:
    import modules.solene_1 as sln
    from modules.constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR
    from modules.constant import ROTATION_POINT, PHASIS_NAME, MULTIPLY_BY
    from modules.diego import clear_lines
    from modules.paul import border_dict


# pylint: disable=E1101


def display_visual_tetrimino(surface, place_properties, y_axis, t_type):
    """permet de définir un tetrimino visuel, notamment pour la hold
    queue et la next queue, ce, sans création d'un objet tetrimino qui
    fausserait le compte des tetrimino lors de leur création.
    Prend en paramètre :
    - `surface`, un objet pygame.Surface ;
    - `place_properties`, un objet HoldQueue ou NextQueue, utile afin de
    récupérer des informations de l'emplacement du tetrimino visuel ;
    - `y_axis` : la position y, particulière de l'emplacement du tetrimino
    visuel sous la forme d'un int ;
    - `t_type` : le type du tetrimino indiqué par un entier compris entre 1
    et 7 inclus."""
    # variables modélisant l'apparence du tetrimino visuel
    tetrimino_shape = TETRIMINO_SHAPE[t_type]
    # définition des emplacements
    x_axis = place_properties.t_rect.x
    w_value = place_properties.t_rect.w
    h_value = place_properties.t_rect.h
    # et de la largeur des traits du tetrimino
    width = place_properties.width // 2 + 1
    # dans le cas où le tetrimino n'est ni 'I' ni 'O'
    # placé en début on gagne une comparaison :)
    if t_type > 2:
        # la taille d'un mino correspond à la largeur occupable divisé par 3
        # puisque qu'il s'agit d'un tetrimino 3x3
        cell_size = w_value // 3
        # determination de la couleur du tetrimino
        color = Tetrimino.COLOR_SHADE[t_type][0]
        for j in range(2):
            for k in range(3):
                # dans le cas où un mino occupe l'emplacement
                if tetrimino_shape[j][k]:
                    # représentation du mino sous la forme d'un tuple
                    # contenant les informations d'emplacement et dimensions
                    rect = (x_axis + k * cell_size,
                            y_axis + j * cell_size,
                            cell_size,
                            cell_size)
                    # dessin du fond du mino rempli avec la couleur
                    pygame.draw.rect(surface, color, pygame.Rect(rect))
                    # dessin du contour du mino en blanc
                    pygame.draw.rect(surface, COLOR['WHITE'],
                                     pygame.Rect(rect), width)
    # si le tetrimino est un 'I' tetrimino
    elif t_type == 2:
        # le côté d'un mino est égal au quart de la largeur pouvant être occupé
        # par le tetrimino visuel
        cell_size = w_value // 4
        # correspond au décalement sur la longueur de l'emplacement du
        # tetrimino de sorte que le I tetrimino paraisse centré
        shift = (h_value - cell_size) // 2
        for j in range(4):
            # représentation d'un mino sous la forme d'un tuple
            # contenant les informations d'emplacement et dimensions
            rect = (x_axis + j * cell_size,
                    y_axis + shift,
                    cell_size,
                    cell_size)
            # dessin du fond du mino rempli avec la couleur cyan
            pygame.draw.rect(surface, COLOR['CYAN'], pygame.Rect(rect))
            # dessin du contour du mino en blanc
            pygame.draw.rect(surface, COLOR['WHITE'], pygame.Rect(rect), width)
    # s'il s'agit d'un 'O' tetrimino
    else:
        cell_size = h_value // 2
        shift = (w_value - 2 * cell_size) // 2
        for j in range(2):
            for k in range(2):
                # représentation d'un mino sous la forme d'un tuple
                # contenant les informations d'emplacement et dimensions
                rect = (x_axis + k * cell_size + shift,
                        y_axis + j * cell_size,
                        cell_size,
                        cell_size)
                # dessin du fond du mino rempli avec la couleur jaune
                pygame.draw.rect(surface, COLOR['YELLOW'], pygame.Rect(rect))
                # dessin du contour du mino en blanc
                pygame.draw.rect(surface, COLOR['WHITE'], pygame.Rect(rect),
                                 width)


class Matrix:
    """modélisation de matrix dans laquelle tombent les tetrimino.

    ATTRIBUTS DE CLASSE:
    - `cell` (dict) comportant les informations d'emplacement de chaque
    cellule de matrix selon son abcisse et son ordonné dans matrix. Toutes
    les valeurs de `Matrix.cell` sont des objets de type pygame.Rect.

    ATTRIBUTS:
    - `cell_size` (int) la longueur d'un côté d'une cellule de matrix en
    nombre de pixel, elle est dépendante des dimensions de la fenêtre ;
    - `content` (list) liste de liste (matrice de format 22 x 10) contenant
    des entiers naturels inférieur strictement à 8, 0 signifiant que qu'aucun
    mino ne figure à l'emplacement, autrement un mino occupe l'emplacement.
    - `end_game` (bool) True si le jeu se termine avec l'issue gagnant
    lorsque le joueur est en mode B et qu'il parvient à remplir l'objectif
    des 25 lignes ;
    - `grid_surface` (pygame.Surface) surface de matrix comprenant les
    lignes de grilles tracés et les contours de matrix ;
    - `higher_row` (int) représente l'ordonnée la plus haute atteinte par un
    mino dans la matrix de jeu ;
    - `rect` (pygame.Rect) contient tous les informations d'emplacement de
    la représentation visuelle de matrix sur la fenêtre de jeu, position
    et dimensions ;
    - `width` (int) largeur du trait de dessin des contours de la
    représentation visuelle de matrix."""

    cell = {}

    def __init__(self, window, game_type):
        """initialisation des différents attributs de la classe Matrix."""
        self.grid_surface = None
        self.end_game = False
        self.resize(window)
        # création d'une matrice vide avec deux lignes pour la skyline
        self.content = [[0 for j in range(10)] for i in range(22)]
        self.higher_row = 22
        # si le mode B est spécifié par `game_type`, rempli 2 x difficulté
        # lignes incomplètes de matrix de mino
        for i in range(game_type[1] * 2):
            # création d'une ligne incomplète
            line = [random.randint(0, 9) for j in range(10)]
            for j in range(10):
                # remplace les éléments supérieur à 7 par 0
                line[j] = 0 if line[j] > 7 else line[j]
            # fait en sorte de remplacer une ligne par `line` depuis le bas
            # de matrix avec l'astuce en indice
            self.content[21-i] = line

    def check_clear_lines(self, data):
        """voir dans `diego.py`, l'attribut highter_row est modifié au besoin
        pour correspondre à la ligne la plus haute afin de respecter la
        cohérence quand des lignes sont "cleared", la méthode permet entre
        autres choses de mettre à jour `data` en ce qui concerne le stockage
        de la valeur du nombre de line_clear."""
        self.content, nb_line_cleared = clear_lines(self.content)
        # dans le cas où il y a un line clear
        if nb_line_cleared > 0:
            # ajoute le nombre de line_clear aux informations du jeu
            self.end_game = data.add_to_line_clear(nb_line_cleared)
            # le score est augmenté de level x le type de line clear,
            # se reférer à la guideline en ce qui concerne le scoring
            level = data.values['level']
            data.score_increase(level * MULTIPLY_BY[nb_line_cleared])
            # mise à jour de l'attribut higher_row
            self.higher_row += nb_line_cleared

    def resize(self, window):
        """redimmensionne les valeurs utile à la représentation
        graphique de matrix. La fonction permet la création d'un dictionnaire
        pratique à la représentation visuelle des mino avec les infomations
        d'emplacement stockés avec des objets pygame.Rect."""
        # calcul de l'espace restant en hauteur en ce qui concerne window
        remaining_height_spaces = window['height'] - 2 * window['margin']
        self.cell_size = remaining_height_spaces // 21
        rect_width = self.cell_size * 10
        rect_height = self.cell_size * 21
        rect_x = (window['width'] - rect_width) // 2
        rect_y = (window['height'] - rect_height) // 2
        self.rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        self.width = round(self.cell_size * 3/10)
        # création d'un attribut de classe de type dictionnaire
        # contenant des objets de type pygame.Rect pour chaque case
        Matrix.cell = {}
        y_axis = self.rect.y - self.width
        # pour chaque colonne
        for i in range(10):
            # création d'un dictionnaire contenant l'information de la colonne
            Matrix.cell[i] = {}
            # pour chaque lignes (exeptée la skyline invisible)
            for j in range(21):
                x_axis = self.rect.x + i * self.cell_size
                if j == 0:
                    Matrix.cell[i][1] = pygame.Rect(x_axis,
                                                    self.rect.y,
                                                    self.cell_size,
                                                    self.cell_size * 7/10)
                else:
                    y_value = y_axis + j * self.cell_size
                    Matrix.cell[i][j+1] = pygame.Rect(x_axis,
                                                      y_value,
                                                      self.cell_size,
                                                      self.cell_size)
        self.resize_grid_surface(window)

    def resize_grid_surface(self, window):
        """crée une surface redimensionnée selon les dimensions de la
        fenêtre `window`, `window` est un dictionnaire contenant les
        données relative à la fenêtre de jeu."""
        grid_surface = pygame.Surface(window['size'])
        grid_surface.set_colorkey((0, 0, 0))
        # dessin de la grille
        # lignes horizontales du quadrillage de matrix
        for i in range(1, 22):
            grid_y = self.cell[1][i].y
            pygame.draw.line(grid_surface, COLOR['WHITE'],
                             (self.rect.x, grid_y),
                             (self.rect.x + self.rect.w, grid_y))
        # lignes verticales du quadrillage de matrix
        for i in range(1, 10):
            grid_x = self.cell[i][1].x
            pygame.draw.line(grid_surface, COLOR['WHITE'],
                             (grid_x, self.rect.y),
                             (grid_x, self.rect.y + self.rect.h - self.width))
        # lignes de bords
        # haut
        pygame.draw.rect(grid_surface, (150, 0, 0),
                         pygame.Rect(self.rect.x,
                                     self.rect.y,
                                     self.rect.w,
                                     self.width))
        # bas
        pygame.draw.rect(grid_surface, (150, 150, 150),
                         pygame.Rect(self.rect.x,
                                     self.rect.y + self.rect.h - self.width,
                                     self.rect.w,
                                     self.width))
        # gauche
        pygame.draw.rect(grid_surface, (150, 150, 150),
                         pygame.Rect(self.rect.x - self.width,
                                     self.rect.y,
                                     self.width,
                                     self.rect.h))
        # droite
        pygame.draw.rect(grid_surface, (150, 150, 150),
                         pygame.Rect(self.rect.x + 10 * self.cell_size,
                                     self.rect.y,
                                     self.width,
                                     self.rect.h))
        self.grid_surface = grid_surface

    def display(self, surface):
        """dessine matrix selon ses attributs sur une surface `surface` devant
        être du type pygame.Surface."""
        for i in range(1, 22):
            for j in range(10):
                current_cell = self.content[i][j]
                if current_cell:
                    # affichage d'un mino de matrix
                    color = Tetrimino.COLOR_SHADE[current_cell][0]
                    pygame.draw.rect(surface,
                                     color, self.cell[j][i])
        surface.blit(self.grid_surface, (0, 0))

    def draw_ghost_piece(self, surface, tetrimino):
        """dessin de la ghost piece."""
        color = Tetrimino.COLOR_SHADE[tetrimino.type][tetrimino.shade]
        line_to_draw = Tetrimino.BORDER[tetrimino.type][tetrimino.facing]
        pos_y = tetrimino.lower_pos
        # dessin des lignes en haut
        for element in line_to_draw[0]:
            coordinates = element[0]
            line_lenght = element[1] * self.cell_size
            cell_pos_x = tetrimino.x_coordinate + coordinates[1]
            cell_pos_y = coordinates[0] + pos_y
            try:
                x_value = self.cell[cell_pos_x][cell_pos_y].x
                y_value = self.cell[cell_pos_x][cell_pos_y].y
                pygame.draw.line(surface, color,
                                 (x_value, y_value),
                                 (x_value + line_lenght, y_value), 3)
            except KeyError:
                pass
        # dessin des lignes à droite
        for element in line_to_draw[1]:
            coordinates = element[0]
            line_lenght = element[1] * self.cell_size
            cell_pos_x = tetrimino.x_coordinate + coordinates[1]
            cell_pos_y = coordinates[0] + pos_y
            try:
                x_value = self.cell_size + self.cell[cell_pos_x][cell_pos_y].x
                y_value = self.cell[cell_pos_x][cell_pos_y].y
                pygame.draw.line(surface, color,
                                 (x_value, y_value),
                                 (x_value, y_value + line_lenght), 3)
            except KeyError:
                pass
        # dessin des lignes en dessous
        for element in line_to_draw[2]:
            coordinates = element[0]
            line_lenght = element[1] * self.cell_size
            cell_pos_x = tetrimino.x_coordinate + coordinates[1]
            cell_pos_y = coordinates[0] + pos_y
            try:
                x_value = self.cell[cell_pos_x][cell_pos_y].x
                y_value = self.cell_size + self.cell[cell_pos_x][cell_pos_y].y
                pygame.draw.line(surface, color,
                                 (x_value, y_value),
                                 (x_value + line_lenght, y_value), 3)
            except KeyError:
                pass
        # dessin des lignes à gauche
        for element in line_to_draw[3]:
            coordinates = element[0]
            line_lenght = element[1] * self.cell_size
            cell_pos_x = tetrimino.x_coordinate + coordinates[1]
            cell_pos_y = coordinates[0] + pos_y
            try:
                x_value = self.cell[cell_pos_x][cell_pos_y].x
                y_value = self.cell[cell_pos_x][cell_pos_y].y
                pygame.draw.line(surface, color,
                                 (x_value, y_value),
                                 (x_value, y_value + line_lenght), 3)
            except KeyError:
                pass

    def is_game_won(self):
        """renseigne si la partie est gagnée."""
        return self.end_game


def start_center(tetrimino_type):
    """indique l'indice permettant de centrer un tetrimino
    selon son type (spécifié en argument de la fonction, un
    entier compris entre 1 et 7 inclus) dans matrice."""
    return (10 - len(TETRIMINO_SHAPE[tetrimino_type])) // 2


class Tetrimino:
    """modélise un tetrimino.

    ATTRIBUTS DE CLASSE:
    - `BORDER` (dict) contient des dictionnaires modélisant les traits
    sur les différents côtés d'un tetrimino pour ses contours, (en haut, à
    droite, en bas et à gauche) pratique pour les tests alentours et pour
    le dessin de la ghost piece ;
    - `COLOR_SHADE` (dict) contient par type du tetrimino exprimé par la
    correspondance avec un entier compris entre 1 et 7 (en clef de
    dictionnaire), un dictionnaire contenant les nuances de couleurs pour
    le type du tetrimino ;
    - `count` (int) compteur du nombre d'instances créées ;
    - `ROTATION_PHASIS` (dict) contient les représentations sous forme de
    matrices (2x2, 3x3 ou 4x4 selon le type du tetrimino) avec toute leur
    phase concernant l'orientation du tetrimino (4 par type : nord, est, sud
    ouest).

    ATTRIBUTS:
    - `facing` (int) compris entre 0 et 3 inclus, il s'agit de l'orientation
    du tetrimino :
        - 0: nord ;
        - 1: est ;
        - 2: sud ;
        - 3: ouest ;
    - `shade` (int) compris entre 0 et 9 inclus, représente la nuance de
    couleur prise par le tetrimino plus le nombre est grand plus le tetrimino
    est sombre ;
    - `state` (int) compris entre 0 et 2 inclus :
        - 0 si le tetrimino est en 'falling phase', c'est-à-dire que le
        tetrimino continue à tomber ;
        - 1 si le tetrimino est en 'lock phase', phase où le tetrimino
        s'apprête à se figer dans la matrice ;
        - 2 lorsque le tetrimino est en 'completion phase' ;
    - `type` (int) compris entre 1 et 7 inclus, il s'agit du type du
    tetrimino :
        - 1: O-tetrimino;
        - 2: I-tetrimino;
        - 3: T-tetrimino;
        - 4: L-tetrimino;
        - 5: J-tetrimino;
        - 6: S-tetrimino;
        - 7: Z-tetrimino;
    - `x_coordinate` (int) compris entre -2 et 8, situe le tetrimino sur
    l'axe des abscisses de matrix grâce au coin haut gauche de la
    représentation du tetrimino sur une matrice 2x2, 3x3 ou 4x4 dépendant
    du type du tetrimino. Plus `x_coordinate` est petit, plus le tetrimino
    se situe vers le bord gauche, à l'inverse, plus il est grand plus le
    tetrimino est situé sur le bord droit.
    - `y_coordinate` (int) compris entre 0 et 20, situe le tetrimino sur
    l'axe des ordonnées de matrix, plus `y_coordinate` est petit, plus le
    tetrimino est haut situé sur matrix."""

    # compteur intéressant pour les informations en fin de partie
    count = 0

    # création d'un dictionnaire contenant toutes les rotations
    ROTATION_PHASIS = {}
    for i in range(1, 8):
        ROTATION_PHASIS[i] = {}
        for facing in range(4):
            ROTATION_PHASIS[i][facing] = sln.turn_right(TETRIMINO_SHAPE[i],
                                                    facing)

    # création du dictionnaire utile aux ghost pieces et aux test alentours
    BORDER = {}
    for i in range(1, 8):
        BORDER[i] = {}
        for facing in range(4):
            BORDER[i][facing] = border_dict(ROTATION_PHASIS[i][facing])

    # création d'un dictionnaire des teintes pour le lock phase
    COLOR_SHADE = {}
    for tetrimino_type in range(1, 8):
        color = TETRIMINO_DATA[tetrimino_type]['color']
        color_rgb = COLOR[color]
        COLOR_SHADE[tetrimino_type] = {0: color_rgb}
        for shade in range(1, 10):
            previous_color = COLOR_SHADE[tetrimino_type][shade-1]
            changed_color = sln.change_color_luminosity(previous_color, 14)
            COLOR_SHADE[tetrimino_type][shade] = changed_color

    def __init__(self, bag, matrix):
        """initialise une instance avec l'attribution de la phase à 0 ("Nord"),
        l'état à : 0 ("falling phase"), le type dépendant de la pièce en
        attente de l'instance de Bag et les attributs `x` et `y` tels qu'ils
        indique leur position en fonction d'une instance Matrix de sorte que
        l'instance créée soit centré dans la skyline."""
        self.facing = 0
        self.state = 0
        self.type = bag.next_tetrimino()
        # définit la nuance de couleur du tetrimino
        self.shade = 0
        # position centrée horizontalement
        self.x_coordinate = start_center(self.type)
        # dans la skyline (en haut de la matrice)
        self.y_coordinate = 0
        self.find_lower_pos(matrix)
        # incrémente le nombre de tetrimino créé de 1
        Tetrimino.count += 1

    def __lock_on_matrix__(self, matrix):
        """Méthode permettant de lock un tetrimino (celui de l'instance),
        dans la matrix de jeu. `matrix` est une instance de la classe
        Matrix. Elle renvoie un booléen, False en condition de fin de jeu,
        c'est-à-dire que la ligne la plus haute est dans la partie invisible
        de la skyline. True quand la gameplay peut continuer sans être
        interrompu."""
        t_type = self.type
        t_phasis = self.facing
        tetrimino_shape = self.ROTATION_PHASIS[t_type][t_phasis]
        tetrimino_lenght = len(tetrimino_shape)
        # parcours de la matrice représentatrice du tetrimino
        for i in range(tetrimino_lenght):
            for j in range(tetrimino_lenght):
                # dans le cas où un mino se situe à l'emplacement
                if tetrimino_shape[j][i]:
                    pos_y = self.y_coordinate + j
                    pos_x = self.x_coordinate + i
                    matrix.content[pos_y][pos_x] = self.type
                    if pos_y < matrix.higher_row:
                        matrix.higher_row = pos_y
                        # vérifie la condition de fin
                        if matrix.higher_row < 1:
                            return False
        return True

    def __can_fall__(self, matrix):
        """test afin de vérifier si un tetrimino peut tomber.
        Il prend en paramètre `matrix` une instance de la classe Matrix,
        et renvoie un booléen correspondant à l'issue du test (succès ou
        échec)."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.facing]
        nb_column = len(tetrimino_shape)
        self.y_coordinate += 1
        if self.test_around(matrix, tetrimino_shape, nb_column):
            return True
        # rétablit la valeur y du tetrimino
        self.y_coordinate -= 1
        return False

    def test_around(self, matrix, tetrimino_shape, nb_column):
        """les test de super rotation system sont effectuées dans cette
        fonction. Elle renvoie un booléen, True lorsque le test est passé
        avec succès avec l'une des translations possible, False sinon.
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
                    if mino and j + self.x_coordinate > -1:
                        # cellule de matrix libre pour mino
                        y_value = i + self.y_coordinate
                        x_value = j + self.x_coordinate
                        if matrix.content[y_value][x_value] == 0:
                            # reussite du test par mino
                            count += 1
            # dans le cas où les quatre mino réussissent le test
            if count == 4:
                return True
        # dans le cas où un mino n'appartient pas à matrix
        except IndexError:
            return False
        return False

    def super_rotation_system(self, matrix, facing):
        """le super rotation système décrit par la guideline de Tetris,
        permet de faire tourner un tetrimino bien que la situation
        ne soit pas confortable à la manoeuvre en temps habituel (contre
        un bord matrix, sur la floor de matrix, se sortir d'une "roue", ...).
        La fonction effectue des test en changeant les coordonnées x, y
        d'un tetrimino via des translations et non de rotation avec un
        point de rotation comme le suggère la guideline.
        `matrix` est un objet de la classe Matrix.
        `facing` est la phase vers laquelle le tetrimino doit tourner.
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
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][facing]
        # optimisable, mais comme cela on a une économie en calcul
        # je privilégie la performance :) (et puis, pas besoin de mettre
        # (0, 0) dans le dictionnaire des test à chaque fois x))
        if self.test_around(matrix, tetrimino_shape, nb_column):
            return True
        # dans le cas où la rotation au point de rotation naturel échoue
        # on fait appel à d'autres test existants
        current_phasis = PHASIS_NAME[self.facing]
        next_phasis = PHASIS_NAME[facing]
        coordinates = (self.x_coordinate, self.y_coordinate)
        try:
            test_list = ROTATION_POINT[t_type][current_phasis][next_phasis]
            for rotation_test in test_list:
                # déplacement des coordonnées selon les test
                self.x_coordinate = coordinates[0] + rotation_test[0]
                self.y_coordinate = coordinates[1] + rotation_test[1]
                if self.test_around(matrix, tetrimino_shape, nb_column):
                    return True
        # s'opère lorsque facing vaut SOUTH pour un tetrimino 3x2
        # il n'y a pas de test supplémentaire donc ne peut pas tourner
        except KeyError:
            self.x_coordinate = coordinates[0]
            self.y_coordinate = coordinates[1]
            return False
        # dans le cas où tous les test échouent
        self.x_coordinate = coordinates[0]
        self.y_coordinate = coordinates[1]
        return False

    def hard_drop(self, data):
        """permet au joueur de réaliser un hard drop en plaçant le
        tetrimino en jeu directement à la position la plus basse
        atteignable par la pièce. `data` est une instance de la classe
        Data."""
        # incrémentation du score
        data.score_increase((self.lower_pos - self.y_coordinate) * 2)
        # fait descendre le tetrimino à sa position la plus basse
        # atteignable sur matrix
        self.y_coordinate = self.lower_pos
        # le tetrimino est en completion phase
        self.state = 2

    def lock_phase(self, matrix, chrono, first, phase):
        """il s'agit de la phase où le tetrimino est sur le point de se
        bloquer, elle fait en sorte de varier la couleur du tetrimino avec
        l'attribut shade, afin que le joueur puisse mieux prendre en compte
        la situation du tetrimino. Un chronomètre est mis en place lors du
        premier appel du lock phase, paramètre su grâce à `first` valant 1
        dans ce cas particulier. `phase` indique la phase de changement de
        couleur : 1 lorsque le tetrimino doit s'assombrir, 0 dans le cas où
        la couleur doit s'éclaircir. `chrono` est le chronomètre associé au
        lock phase. La fonction renvoie deux paramètres, `first` et `phase`.
        Le premier vaut 1 ou 0 et le second de même."""
        # initialisation du chronomètre
        if first:
            chrono.reset()
            first = 0
        # temps du lock phase écoulé
        if chrono == 0.5:
            self.state = 2
            first = 1
            return first, 1
        # dans le cas où le tetrimino peut tomber
        if self.__can_fall__(matrix):
            # permet de sortir de la lock phase
            self.state = 0
            self.shade = 0
            # on renvoie 1 afin de reinitialiser phase
            return 1, 1
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
        return first, phase

    def find_lower_pos(self, matrix):
        """renvoie la position la plus basse pouvant être atteinte par
        l'instance afin de déterminer la position des ordonnées de la ghost
        piece dans `matrix`. La méthode prend en paramètre `matrix` une
        instance de la classe Matrix."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.facing]
        # variable utile pour la méthode test_around de l'objet `tetrimino`
        # afin d'éviter de calculer la longueur à chaque tour de boucle
        nb_column = len(tetrimino_shape)
        # stockage de la valeur de l'attribut y_coordinate de `tetrimino`
        y_coordinate = self.y_coordinate
        proceed = True
        # du moment que le tetrimino peut être placé sans accroc
        while proceed:
            if self.test_around(matrix, tetrimino_shape, nb_column):
                # on incrémente pour faire descendre le tetrimino d'une ligne
                self.y_coordinate += 1
                if self.y_coordinate > 20:
                    proceed = False
            else:
                proceed = False
        # on renvoie la valeur d'ordonnée trouvée
        self.lower_pos = self.y_coordinate - 1
        # on rétablit la valeur initiale de la coordonnée y du tetrimino
        self.y_coordinate = y_coordinate

    def display(self, surface):
        """dessine l'instance de tetrimino en fonction de ses spécificités
        sur `surface`, un objet pygame.Surface."""
        tetrimino_shape = self.ROTATION_PHASIS[self.type][self.facing]
        color = Tetrimino.COLOR_SHADE[self.type][self.shade]
        # parcours de la matrice représentative de tetrimino_shape
        for i, row in enumerate(tetrimino_shape):
            for j in range(len(tetrimino_shape)):
                if row[j]:
                    # affichage mino par mino sur matrix
                    try:
                        abcsissa = j + self.x_coordinate
                        ordinate = i + self.y_coordinate
                        pygame.draw.rect(surface,
                                         color,
                                         Matrix.cell[abcsissa][ordinate])
                    except KeyError:
                        pass

    def leftmost(self):
        """renvoie le plus petit coordonnée x possédé par un mino de
        l'instance."""
        # on selectionne les bords gauche du tetrimino
        left = Tetrimino.BORDER[self.type][self.facing][3]
        left_most = 4
        for shift in left:
            if shift[0][1] < left_most:
                left_most = shift[0][1]
        return left_most + self.x_coordinate

    def rightmost(self):
        """renvoie la plus grande valeur x d'un mino de l'instance"""
        # on selectionne les bords droit du tetrimino
        right = Tetrimino.BORDER[self.type][self.facing][1]
        right_most = 0
        for shift in right:
            if shift[0][1] + shift[1] > right_most:
                right_most = shift[0][1]
        return right_most + self.x_coordinate

    def fall(self, matrix):
        """permet de faire tomber le tetrimino, s'il ne peut pas,
        le tetrimino passe en lock phase. A pour paramètre une instance de
        la classe Matrix `matrix`."""
        # teste si le tetrimino est apte à tomber
        if self.__can_fall__(matrix):
            return True
        # le test a échoué, le tetrimino ne peut pas tomber,
        # on passe en lock phase
        self.state = 1
        return False

    def move_left(self, matrix):
        """déplace d'une case vers la gauche le tetrimino dans matrix.
        `matrix` est un objet de la classe Matrix."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.facing]
        nb_column = len(tetrimino_shape)
        # dans le cas où le mino le plus à gauche n'est pas adjacent au mur
        if self.leftmost() > 0:
            self.x_coordinate -= 1
            if self.test_around(matrix, tetrimino_shape, nb_column):
                # redéfini emplacement de la ghost piece
                self.find_lower_pos(matrix)
                return
            # le test a échoué, le tetrimino ne peut pas aller à gauche
            self.x_coordinate += 1

    def move_right(self, matrix):
        """déplace d'une case vers la droite le tetrimino dans matrix.
        `matrix` est un objet de la classe Matrix."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.facing]
        nb_column = len(tetrimino_shape)
        self.x_coordinate += 1
        if self.test_around(matrix, tetrimino_shape, nb_column):
            # redéfini emplacement de la ghost piece
            self.find_lower_pos(matrix)
            return
        # le test a échoué, le tetrimino ne peut pas aller à droite
        self.x_coordinate -= 1

    def turn_left(self, matrix):
        """permet de tourner le tetrimino de 90° dans le sens anti-horaire.
        `matrix` est une instance de la classe Matrix."""
        facing = (self.facing - 1) % 4
        # dans le cas où le tetrimino peut tourner
        if self.super_rotation_system(matrix, facing):
            self.facing = facing
            # redéfini emplacement de la ghost piece
            self.find_lower_pos(matrix)

    def turn_right(self, matrix):
        """permet de tourner le tetrimino de 90° dans le sens horaire.
        `matrix` est une instance de la classe Matrix."""
        facing = (self.facing + 1) % 4
        # dans le cas où le tetrimino peut tourner
        if self.super_rotation_system(matrix, facing):
            self.facing = facing
            # redéfinition de l'emplacement de la ghost piece
            self.find_lower_pos(matrix)

    def set_type(self, new_type):
        """change le type d'un tetrimino pour `new_type` un entier
        naturel compris entre 1 et 7 inclus."""
        self.type = new_type

    def set_y(self, value):
        """place le tetrimino à la position `value` spécifié.
        `value` doit être un int compris entre 0 et 21 inclus."""
        self.y_coordinate = value

    def get_count(self):
        """renvoie le nombre de tetrimino créés."""
        return self.count

    def get_state(self):
        """renvoie l'état du tetrimino."""
        return self.state

    def get_type(self):
        """renvoie le type du tetrimino."""
        return self.type

    def get_x(self):
        """renvoie la position x du tetrimino relatif à matrix."""
        return self.x_coordinate

    def get_y(self):
        """renvoie la position y du tetrimino dans matrix."""
        return self.y_coordinate


class HoldQueue:
    """modélise la hold queue, là où les tetrimino sont mis sur le côté et
    pouvant être rappelé dans le jeu à tout moment à raison d'une fois par
    tetrimino.

    ATTRIBUTS:
    - `can_hold` (bool) lorsque `can_hold` vaut True, le joueur a la
    possibilité de hold un tetrimino, dans le cas contraire, il ne pourra
    pas effectuer cette action ;
    - `t_rect` (pygame.Rect) contient les informations d'emplacement pour
    le tetrimino dans la hold queue à afficher ;
    - `t_type` (int) compris entre 0 et 7 inclus, 0 lorsque la hold queue
    est vide, autrement, il s'agit d'un tetrimino selon son identification
    par la correspondance entier et type ;
    - `rect` (pygame.Rect) contient les informations d'emplacement de
    l'encadré de la hold queue ;
    - `width` (int) en nombre de pixel, l'épaisseur du trait de dessin pour
    l'encadré de la hold queue."""

    def __init__(self, window, matrix):
        """instanciation par l'attribution de ses valeurs pratique à sa
        représentation."""
        self.resize(window, matrix)
        # l'attribut t_type est à 0 : il n'y a pas de tetrimino hold
        self.t_type = 0
        # le joueur peut hold
        self.can_hold = True

    def hold(self, tetrimino):
        """permet de hold une pièce et d'interdire le joueur de hold une
        seconde fois. `tetrimino` doit être une instance de la classe
        Tetrimino."""
        # le type du tetrimino est stocké dans l'attribut t_type
        self.t_type = tetrimino.get_type()
        # l'attribut can_hold est défini à False
        self.can_hold = False

    def resize(self, window, matrix):
        """redimensionne selon les valeurs de `window` et `matrix` deux
        dictionnaire contenant les informations utiles au placement et
        dimensions de objets du même nom instanciés."""
        # informations générales de l'emplacement de la hold queue
        remaining_space = matrix['rect'].x - window['margin']
        w_value = round(matrix['cell_size'] * 3.7)
        x_axis = (remaining_space - w_value) * 0.8
        self.width = w_value // 39 + 1
        self.rect = pygame.Rect(x_axis, matrix['rect'].y, w_value, w_value)
        # informations de l'emplacement tetrimino
        t_w = matrix['cell_size'] * 3
        t_h = matrix['cell_size'] * 2
        t_x = self.rect.x + (self.rect.w - t_w) // 2
        t_y = self.rect.y + (self.rect.w - t_h) // 2
        self.t_rect = pygame.Rect(t_x, t_y, t_w, t_h)

    def display(self, surface):
        """affichage de l'encadré associé à la hold queue, avec si y a le
        type du tetrimino ayant été hold."""
        # représentation de l'encadré
        pygame.draw.rect(surface, (150, 150, 150),
                         self.rect,
                         self.width)
        # dans le cas où il y a un tetrimino mis de côté
        if self.t_type:
            # l'afficher
            display_visual_tetrimino(surface, self, self.t_rect.y,
                                     self.t_type)

    def get_t_type(self):
        """renvoie le type du tetrimino dans la hold_queue, un int compris
        entre 0 et 7 inclus. 0 signifiant que la hold queue est vide."""
        return self.t_type

    def allow_hold(self):
        """permet de reinitialiser l'attribut can_hold à l'appel de la
        méthode."""
        self.can_hold = True


class NextQueue:
    """modélisation de la next queue dans laquelle sont représentés les six
    prochaines pièces de la partie en cours.

    ATTRIBUTS:
    - `bag_content` (list) liste des six prochaines pièces contenus dans bag
    à afficher par l'instance. Il s'agit d'une liste d'entier représentant les
    types des tetrimino par le nombre qui leur correspond ;
    - `next_y` (list) liste contenant le nombre l'information d'emplacement y
    sur l'axe des ordonnées de la fenêtre de jeu pour chacune des six
    emplacements des tetrimino à afficher ;
    - `rect_1` (pygame.Rect) correspond à l'encadré carré pour la prochaine
    pièce directe ;
    - `rect_2` (pygame.Rect) correspond à l'encadré rectangle contenant
    verticalement les cinq pièces suivant celle contenue dans le premier
    encadré d'après `bag_content`
    - `width` (int) en pixel, l'épaisseur du trait de dessin des contours des
    encadrés de la next queue."""

    def __init__(self, window, matrix, bag):
        """méthode constructrice de la classe."""
        self.bag_content = bag.content[-6:]
        self.resize(window, matrix)

    def resize(self, window, matrix):
        """permet d'après les données de `Window` de redimensionner l'encadré
        grâce à la mise à jour des attributs de l'instance concernant cela."""
        matrix_place = matrix['rect'].x + matrix['rect'].w
        remaining_space = window['width'] - matrix_place - window['margin']
        # évaluation des paramètres utiles pour définir les encadrés
        w_value = round(matrix['cell_size'] * 3.7)
        h_value = (w_value, round(matrix['rect'].h * 0.9) - w_value)
        x_axis = (round((remaining_space - w_value) * 0.3)) + matrix_place
        y_axis_1 = matrix['rect'].y
        y_axis_2 = round(y_axis_1 + w_value + (matrix['rect'].h / 10))
        self.width = h_value[0] // 39 + 1
        self.rect_1 = pygame.Rect(x_axis, y_axis_1, w_value, h_value[0])
        self.rect_2 = pygame.Rect(x_axis, y_axis_2, w_value, h_value[1])
        # liste des positions 'y' des différents emplacement des tetriminos
        t_w = matrix['cell_size'] * 3
        t_h = matrix['cell_size'] * 2
        t_x = x_axis + (w_value - t_w) // 2
        self.next_y = [y_axis_1 + (w_value - t_h) // 2]
        space = (h_value[1] - 5 * t_h) // 6
        # y_axis comme variable définissant successivement les ordonnées y
        # pour les différents tetrimino visuel
        y_axis_2 += space
        for _ in range(5):
            self.next_y.append(y_axis_2)
            y_axis_2 += t_h + space
        self.t_rect = pygame.Rect(t_x, 0, t_w, t_h)

    def update(self, bag):
        """met à jour l'attribut bag_content."""
        self.bag_content = bag.content[-6:]

    def display(self, surface):
        """affiche des encadrés correspondant à la next queue dans lesquelles
        figurent les tetrimino en attente dans l'instance de `Bag` sont
        visibles. `surface` doit être un objet de type pygame.Surface."""
        # conteneur de la prochaine pièce de jeu
        pygame.draw.rect(surface,
                         (150, 150, 150),
                         self.rect_1,
                         self.width)
        # conteneur des cinq pièces suivantes
        pygame.draw.rect(surface,
                         (150, 150, 150),
                         self.rect_2,
                         self.width)
        # affichage des tetrimino suivant contenu dans bag
        for i in range(6):
            display_visual_tetrimino(surface, self,
                                     self.next_y[i - 1], self.bag_content[-i])


def find_align_center_x(lenght, remaining_place):
    """permet de trouver la position x tel que l'objet que l'on cherche
    à aligner au centre soit centré. Prend en paramètre la taille de la largeur
    de l'objet (`lenght`) et la largeur de l'objet sur lequel on cherche à
    centrer (`remaining_place`)."""
    return (remaining_place - lenght) // 2
