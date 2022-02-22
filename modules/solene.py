"""module codé par Solène (@periergeia) TG8, contenant diverses classes et
fonctions utiles au bon fonctionnement du jeu Tetris."""


# importation de librairies python utiles
import random
import colorsys
import time
import pygame
import pygame.freetype
try:
    from constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR, PHASIS_NAME
    from constant import ROTATION_POINT, DATA_KEYS, DATA_STRINGS, LANG, VISUAL_STRUCTURE
    from diego import clear_lines, GameStrings
    from paul import border_dict
    from useful import get_font_size, loop_starter_pack, Button2, Button
except ModuleNotFoundError:
    from modules.constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR
    from modules.constant import ROTATION_POINT, DATA_KEYS, DATA_STRINGS, LANG, VISUAL_STRUCTURE
    from modules.constant import PHASIS_NAME
    from modules.diego import clear_lines, GameStrings
    from modules.paul import border_dict
    from modules.useful import get_font_size, loop_starter_pack, Button2, Button


game_strings = GameStrings(LANG)


# pylint: disable=E1101

# supprimer des attributs avec delattr(self, 'field_to_delete') super().__init__(*args, **kwargs)


def resize_all(window_data, obj):
    """"redimensionne toutes les choses nécéssitant d'être
    redimensionnées."""
    obj[1].resize(window_data)
    matrix_data = {'rect': obj[1].rect,
                   'cell_size': obj[1].cell_size}
    # redimensionne chaque objet avec leur méthode resize
    for element in obj[2:5]:
        element.resize(window_data, matrix_data)
    '''for element in obj[5:]:
        element.resize(window_data)'''
    obj[4].values_relative_position()


def display_all(window, obj):
    """raffraîchit le jeu en faisant afficher une frame,
    contenant les objets dont les caractéristiques ont été
    mis à jour."""
    # création d'une surface
    frame = pygame.Surface(window.get_size())
    # rect transparent sur l'emplacement de Data
    transparent_rect = pygame.Surface((obj[-1].rect.w, obj[-1].rect.h))
    transparent_rect.fill((45, 0, 0))
    # rect transparent pour le bouton des menus
    transparent_rect_2 = pygame.Surface((round(window.get_width() * 0.1), window.get_height()))
    transparent_rect_2.fill((45, 0, 0))
    frame.blit(transparent_rect, (obj[-1].rect.x, obj[-1].rect.y))
    frame.blit(transparent_rect_2, (round(window.get_width() * 0.89), 0))
    frame.set_colorkey((45, 0, 0))
    # affiche chaque objet avec leur méthode display
    for element in obj[:-1]:
        element.display(frame)
    # dessin de la ghost piece
    obj[1].draw_ghost_piece(frame, obj[0])
    # frame sur la fenêtre
    window.blit(frame, (0, 0))
    # rafraichissement de la fenêtre pygame
    pygame.display.flip()


def display_button(window):
    #  ###############provisoire
    menubutton = pygame.image.load("./image/menubutton.png").convert_alpha()
    # affichage de l'image pour le boutton des menus, ## voir arrangement ?
    menu_button = Button2(window, (0.9, 0.05, 0.08), menubutton)
    menu_button.draw(window)
    pygame.display.flip()


def display_game_data(window, data, chronometer):
    """affiche les données de jeu dans l'encadré de Data."""
    # création d'un objet pygame.Surface de la taille de l'encadré data
    frame = pygame.Surface((data.rect.w, data.rect.h))
    frame.fill(0x009900)
    frame.blit(data.surface, (0, 0))
    data.update(chronometer, frame)
    window.blit(frame, (data.rect.x, data.rect.y))
    pygame.display.flip()


def create_game_pause(window):
    """crée un visuel permettant au joueur de comprendre que le
    jeu est mis en pause."""
    resume_button = Button(window,
                           (0.25,
                            0.3,
                            0.5,
                            0.15),
                           game_strings.get_string("resume"))
    option_button = Button(window,
                           (0.25,
                            0.55,
                            0.5,
                            0.15),
                           game_strings.get_string("options"))

    frame = pygame.Surface(window.get_size())
    frame.set_colorkey((0, 0, 0))
    pygame.draw.rect(frame, (100, 100, 100),
                     pygame.Rect(window.get_width() * 0.1,
                                 window.get_height() * 0.1,
                                 window.get_width() * 0.78,
                                 window.get_height() * 0.8))
    resume_button.draw(frame)
    option_button.draw(frame)
    window.blit(frame, (0, 0))
    pygame.display.flip()
    return resume_button, option_button


def get_game_picture():
    pass


def display_visual_tetrimino(surface, place_properties, y_axis, t_type):
    """permet de définir un tetrimino visuel, notamment pour la hold
    queue et la next queue, ce, sans création d'un objet tetrimino.
    Prend en paramètre :
    - `surface`, un objet pygame.Surface ;
    - `place_properties`, un objet HoldQueue ou NextQueue, utile afin de
    récupérer des informations de l'emplacement du tetrimino visuel ;
    - `y_axis` : la position y, particulière de l'emplacement du tetrimino
    visuel sous la forme d'un int ;
    - `t_type` : le type du tetrimino indiqué par un entier compris entre 1
    et 7 inclus"""
    tetrimino_shape = TETRIMINO_SHAPE[t_type]
    color = Tetrimino.COLOR_SHADE[t_type][0]
    x_axis = place_properties.t_rect.x
    w_value = place_properties.t_rect.w
    h_value = place_properties.t_rect.h
    width = place_properties.width // 2 + 1
    # dans le cas où le tetrimino n'est ni 'I' ni 'O'
    # placé en début on gagne une comparaison :)
    if t_type > 2:
        cell_size = w_value // 3
        for j in range(2):
            for k in range(3):
                if tetrimino_shape[j][k]:
                    rect = (x_axis + k * cell_size,
                            y_axis + j * cell_size,
                            cell_size, cell_size)
                    pygame.draw.rect(surface, color, pygame.Rect(rect))
                    pygame.draw.rect(surface, (250, 250, 250),
                                     pygame.Rect(rect), width)
    # si le tetrimino est un 'I' tetrimino
    elif t_type == 2:
        cell_size = w_value // 4
        shift = (h_value - cell_size) // 2
        for j in range(4):
            rect = (x_axis + j * cell_size,
                    y_axis + shift,
                    cell_size, cell_size)
            pygame.draw.rect(surface, color, pygame.Rect(rect))
            pygame.draw.rect(surface, (250, 250, 250), pygame.Rect(rect),
                             width)
    # s'il s'agit d'un 'O' tetrimino
    else:
        cell_size = h_value // 2
        shift = (w_value - 2 * cell_size) // 2
        for j in range(2):
            for k in range(2):
                rect = (x_axis + k * cell_size + shift,
                        y_axis + j * cell_size,
                        cell_size, cell_size)
                pygame.draw.rect(surface, color, pygame.Rect(rect))
                pygame.draw.rect(surface, (250, 250, 250), pygame.Rect(rect),
                                 width)


def turn_right(tetrimino, facing):
    """fait tourner une pièce tetrimino avec une rotation
    vers la droite. Utilise la récursivité.
    - tetrimino : modélisé par une matrice ;
    - facing : un entier compris entre 0 et 3.
    Renvoie une matrice correspondant à la phase indiquée.
    >>> turn_right([[0, 0, 1], [1, 1, 1], [0, 0, 0]], 2)
    [[0, 0, 0], [1, 1, 1], [1, 0, 0]]
    >>> turn_right([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]], 3)
    [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]"""
    if facing == 0:
        return tetrimino
    facing -= 1
    rotated_tetrimino = []
    for i in range(len(tetrimino)):
        tetrimino_line = []
        for j in range(len(tetrimino)-1, -1, -1):
            tetrimino_line.append(tetrimino[j][i])
        rotated_tetrimino.append(tetrimino_line)
    return turn_right(rotated_tetrimino, facing)


def change_color_luminosity(color, rate_of_change):
    """change la luminosité de la couleur, renvoie un tuple rgb de la couleur
    assombrie selon `rate_of_change`, un entier. `couleur` doit être un tuple
    représentant les valeurs rgb (chaque entier est compris entre 0 et 255)."""
    red, green, blue = color
    hue, saturation, lightness = colorsys.rgb_to_hsv(red, green, blue)
    lightness = lightness - rate_of_change
    temp_color = colorsys.hsv_to_rgb(hue, saturation, lightness)
    final_color = [0, 0, 0]
    for i, primary in enumerate(temp_color):
        final_color[i] = round(primary)
    return tuple(final_color)


class Chronometer:
    """modélise un chronomètre."""

    def __init__(self):
        """initialisation d'un chronomètre."""
        self.time = None
        self.duration = None
        self.reset()

    def time_elapsed(self):
        """renvoie le temps passé depuis l'initialisation
        du chronomètre"""
        return time.time_ns() - self.time

    def freeze(self):
        """défini l'attribut duration pour sauvegarder la valeur du
        chronomètre au moment de l'appel à la méthode freeze."""
        self.duration = self.time_elapsed()

    def unfreeze(self):
        """redéfinit l'attribut time afin que le chronomètre puisse
        afficher une valeur cohérente par rapport aux actions."""
        self.time = time.time_ns() - self.duration

    def get_chrono_value(self):
        """renvoie les valeurs en durée du nombre d'heures,
        de minutes, de secondes et de millisecondes de la partie."""
        time_elapsed = self.time_elapsed()
        # durées stockées dans des variables
        milliseconds = str(time_elapsed % 10 ** 9 % 10 ** 5)[:3]
        seconds = int((time_elapsed / 10 ** 9) % 60)
        minutes = int((time_elapsed / 60 / 10 ** 9) % 60)
        hours = int((time_elapsed / 3600 / 10 ** 9) % 24)
        # évalue si l'affichage du nombre d'heure est nécéssaire
        if hours:
            chrono_format = '{h:02d} : {m:02d} : {s:02d}, {x}'
        else:
            chrono_format = '{m:02d} : {s:02d}, {x}'
        chrono_value = chrono_format.format(h=hours, m=minutes,
                                            s=seconds, x=milliseconds)
        return chrono_value

    def __eq__(self, duration):
        """renvoie le booléen vrai si le temps indiqué sur
        le chronomètre correspond à la durée `duration` (float) en seconde
        comparée, autrement, il renvoie faux."""
        # l'égalité entre int et float n'est pas efficace
        return time.time_ns() - self.time > duration * 10 ** 9

    def reset(self):
        """reinitialise le chronomètre."""
        self.time = time.time_ns()


class Bag:
    """modélise un sac contenant l'ordre des tetrimino suivant
    représentés par un numéro correspondant à leur type."""

    def __init__(self):
        self.content = list(range(1, 8))
        random.shuffle(self.content)

    def __len__(self):
        """renvoie le nombre de tetrimino en attente."""
        return len(self.content)

    def next_tetrimino(self):
        """renvoie le prochain tetrimino et fait en sorte qu'il
        y ait toujours au moins 5 tetrimino en attente."""
        if len(self) < 7:
            next_generation = list(range(1, 8))
            random.shuffle(next_generation)
            self.content = next_generation + self.content
        return self.content.pop()


class Matrix:
    """modélisation de matrix dans laquelle tombent les tetrimino."""

    def __init__(self, window, game_type):
        """initialisation des différents attributs de la classe Matrix."""
        self.grid_surface = None
        self.resize(window)
        self.content = [[0 for j in range(10)] for i in range(22)]
        # création d'une matrice vide avec deux lignes pour la skyline
        self.higher_row = 22
        for i in range(game_type[1] * 2):
            line = [random.randint(0, 9) for j in range(10)]
            for j in range(10):
                line[j] = 0 if line[j] > 7 else line[j]
            self.content[21-i] = line

    # ##temporaire
    def __str__(self):
        stock = ''
        for i in range(1, 22):
            stock += ' '.join(str(self.content[i]))
            stock += '\n'
        return stock

    def clear_lines(self, data):
        """voir dans `diego.py` suivi d'une modification de l'attribut
        modelisation, ainsi que highter_row, la ligne la plus haute afin
        de respecter la cohérence."""
        self.content, nb_line_cleared = clear_lines(self.content)
        # dans le cas où il y a un line clear
        if nb_line_cleared > 0:
            # ajoute le nombre de line_clear aux informations du jeu
            data.add_to_line_clear(nb_line_cleared)
            # ## placer dans constantes ?
            multiply_by = {1: 100, 2: 300, 3: 500, 4: 800}
            level = data.values['lines']
            data.score_increase(level * multiply_by[nb_line_cleared])
            self.higher_row += nb_line_cleared


    def resize(self, window):
        """redimmensionne les valeurs utile à la représentation
        graphique de matrix. La fonction permet la création d'un dictionnaire
        pratique à la représentation des mino."""
        # pourrait être enlevé, mais mieux pour compréhension étapes
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
        for i in range(10):
            Matrix.cell[i] = {}
            for j in range(21):
                x_axis = self.rect.x + i * self.cell_size
                if j == 0:
                    Matrix.cell[i][1] = pygame.Rect(x_axis,
                                                    self.rect.y,
                                                    self.cell_size,
                                                    self.cell_size * 7/10)
                else:
                    Matrix.cell[i][j+1] = pygame.Rect(x_axis,
                                                      y_axis + j * self.cell_size,
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

        # demo toutes les cases, première et dernière de matrix visible
        '''for element in self.cell:
            for i in range(10):
                for j in range(1, 22):
                    # ##couleurs sympa garder pour mode spécial ?
                    color = (i*4, j*4, 40)
                    pygame.draw.rect(surface, color, self.cell[i][j])
        pygame.draw.rect(surface, (250, 0, 0), self.cell[0][1])
        pygame.draw.rect(surface, (0, 250, 0), self.cell[9][21])'''
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


def start_center(tetrimino_type):
    """indique l'indice permettant de centrer un tetrimino
    selon son type (spécifié en argument de la fonction, un
    entier compris entre 1 et 7 inclus) dans matrice."""
    return (10 - len(TETRIMINO_SHAPE[tetrimino_type])) // 2


class Tetrimino(Matrix):
    """modélise un tetrimino.

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
    - `type`
    - x_coordinate
    - y_coordinate
    """

    # compteur intéressant pour les informations en fin de partie
    count = 0

    # création d'un dictionnaire contenant toutes les rotations
    ROTATION_PHASIS = {}
    for i in range(1, 8):
        ROTATION_PHASIS[i] = {}
        for facing in range(4):
            ROTATION_PHASIS[i][facing] = turn_right(TETRIMINO_SHAPE[i],
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
            changed_color = change_color_luminosity(previous_color, 14)
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
        # ##à enlever en fin
        print(f"Tetrimino {self.type}")
        print(self)

    # ##temporaire, pour la visualisation du tetrimino, à enlever à la fin
    def __str__(self):
        """ceci est une docstring pylint :)"""
        stock = ''
        for element in Tetrimino.ROTATION_PHASIS[self.type][self.facing]:
            stock += ' '.join(str(element))
            stock += '\n'
        stock += f'\n type du tetrimino : {TETRIMINO_SHAPE[self.type]}'
        return stock

    def __lock_on_matrix__(self, matrix, game_over):
        """Méthode permettant de lock un tetrimino (celui de l'instance),
        dans sur la matrix de jeu. `matrix` est une instance de la classe
        Matrix."""
        t_type = self.type
        t_phasis = self.facing
        tetrimino_shape = self.ROTATION_PHASIS[t_type][t_phasis]
        tetrimino_lenght = len(tetrimino_shape)
        for i in range(tetrimino_lenght):
            for j in range(tetrimino_lenght):
                if tetrimino_shape[j][i] == 1:
                    pos_y = self.y_coordinate + j
                    pos_x = self.x_coordinate + i
                    matrix.content[pos_y][pos_x] = self.type
                    if matrix.higher_row < 1:
                        game_over = True
                    if pos_y < matrix.higher_row:
                        matrix.higher_row = pos_y
        return game_over

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
                    if mino and j + self.x_coordinate > -1:
                        # cellule de matrix libre pour mino
                        if matrix.content[i + self.y_coordinate][j + self.x_coordinate] == 0:
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
        """super rotation système décrit par la guideline de Tetris,
        permet de faire tourner un tetrimino bien que la situation
        ne soit pas confortable à la manoeuvre en temps habituel (contre
        un bord de matrix, sur la floor, ...).
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
        # ## test pour les situation de rotation à enlever en fin
        print(f'{PHASIS_NAME[self.facing]}  -->  {PHASIS_NAME[facing]}')
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
            print('turn point : FAIL')
            self.x_coordinate = coordinates[0]
            self.y_coordinate = coordinates[1]
            return False
        # dans le cas où tous les test échouent
        print('turn point : FAIL')
        self.x_coordinate = coordinates[0]
        self.y_coordinate = coordinates[1]
        return False

    def hard_drop(self, data):
        """permet au joueur de réaliser un hard drop en plaçant le
        tetrimino en jeu directement à la position la plus basse
        atteignable par la pièce."""
        data.score_increase((self.lower_pos - self.y_coordinate) * 2)
        self.y_coordinate = self.lower_pos
        self.state = 2

    # fonction améliorable
    def lock_phase(self, matrix, chrono, first, phase):
        """il s'agit de la phase où le tetrimino est sur le point de se
        bloquer, elle fait en sorte de varier la couleur du tetrimino avec
        l'attribut shade, afin que le joueur puisse mieux prendre en compte
        la situation du tetrimino. Un chronomètre est mis en place lors du
        premier appel du lock phase, paramètre su grâce à `first` valant 1
        dans ce cas particulier. `phase` indique la phase de changement de
        couleur 1 lorsque le tetrimino doit s'assombrir, 0 dans le cas où
        il s'éclaircit. `chrono` est le chronomètre associé au lock phase."""
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
        """affiche l'instance de tetrimino en fonction de ses spécificités."""
        tetrimino_shape = self.ROTATION_PHASIS[self.type][self.facing]
        color = Tetrimino.COLOR_SHADE[self.type][self.shade]
        for i, row in enumerate(tetrimino_shape):
            for j in range(len(tetrimino_shape)):
                if row[j]:
                    # affichage mino par mino sur matrix
                    # ## devrait pouvoir enlever ceci
                    try:
                        # ## vérifier tarduction
                        abcsissa = j + self.x_coordinate
                        ordinate = i + self.y_coordinate
                        pygame.draw.rect(surface,
                                         color,
                                         self.cell[abcsissa][ordinate])
                    except KeyError:
                        pass

    def leftmost(self):
        """renvoie le plus petit coordonnée x possédé par un mino."""
        # on selectionne les bords gauche du tetrimino
        left = Tetrimino.BORDER[self.type][self.facing][3]
        left_most = 4
        for shift in left:
            if shift[0][1] < left_most:
                left_most = shift[0][1]
        return left_most + self.x_coordinate

    # ## n'est pas utilisé pour le moment, voir par la suite
    def rightmost(self):
        """renvoie la plus grande valeur x d'un mino."""
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
        """déplace d'une case vers la gauche le tetrimino."""
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
        """déplace d'une case vers la droite le tetrimino."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.facing]
        nb_column = len(tetrimino_shape)
        self.x_coordinate += 1
        if self.test_around(matrix, tetrimino_shape, nb_column):
            # redéfini emplacement de la ghost piece
            self.find_lower_pos(matrix)
            return
        # le test a échoué, le tetrimino ne peut pas aller à droite
        self.x_coordinate -= 1

    # ##penser à l'implémentationo quand méthode turn_right ok
    def turn_left(self, matrix):
        """permet de tourner le tetrimino de 90° dans le sens
        horaire."""
        facing = (self.facing - 1) % 4
        if self.super_rotation_system(matrix, facing):
            self.facing = facing
            # redéfini emplacement de la ghost piece
            self.find_lower_pos(matrix)

    def turn_right(self, matrix):
        """permet de tourner le tetrimino de 90° dans le sens
        anti-horaire."""
        facing = (self.facing + 1) % 4
        if self.super_rotation_system(matrix, facing):
            self.facing = facing
            # redéfini emplacement de la ghost piece
            self.find_lower_pos(matrix)

    def set_type(self, new_type):
        """change le type d'un tetrimino pour `new_type` un entier
        naturel compris entre 1 et 7 inclus."""
        self.type = new_type

    def set_y(self, value):
        """place le tetrimino à la position `value` spécifié.
        `value` doit être un int compris entre 0 et 21 compris."""
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

    # ## docstring foireuses à améliorer par la suite en fonction
    # vu que pas forcément vrai avec super rotation system
    def get_x(self):
        """renvoie la position x du tetrimino relatif à matrix.
        - 0 s'il est dans la colonne la plus à gauche ;
        - 8, valeur maximale pour la colonne la plus à droite
        possible pour un tetrimino"""
        return self.x_coordinate

    def get_y(self):
        """renvoie la position y du tetrimino dans matrix.
        - 0 s'il est dans la partie supérieure à la skyline ;
        - 1, dans la skyline ;
        - 20, valeur maximale pouvant être renvoyée (si on prend
        un O tetrimino sachant que sa représentation se fait sur
        une matrice 2x2)."""
        return self.y_coordinate


class HoldQueue:
    """modélise la hold queue, là où les tetrimino sont mis sur le côté et
    pouvant être rappelé dans le jeu à tout moment à raison d'une fois par
    tetrimino."""

    def __init__(self, window, matrix):
        """initialisation de l'instance par l'attribution de ses valeurs
        pratique à sa représentation. L'attribut t_type est à 0 : il n'y a
        pas de tetrimino hold."""
        self.resize(window, matrix)
        self.t_type = 0
        self.can_hold = True

    def hold(self, tetrimino):
        """permet de hold une pièce. `tetrimino` doit être une instance
        de la classe Tetrimino."""
        self.t_type = tetrimino.type
        self.can_hold = False

    def resize(self, window, matrix):
        """redimensionne selon les valeurs de `Window` une instance de la
        classe Window."""
        # informations générales de l'emplacement de la hold queue
        remaining_space = matrix['rect'].x - window['margin']
        w_value = round(matrix['cell_size'] * 3.7)
        x_axis = (remaining_space - w_value) * 0.8
        self.width = w_value // 39 + 1
        self.rect = pygame.Rect(x_axis, matrix['rect'].y, w_value, w_value)
        # informations de l'emplacement tetrimino
        # ## tester utilité des variables
        t_w = matrix['cell_size'] * 3
        t_h = matrix['cell_size'] * 2
        t_x = self.rect.x + (self.rect.w - t_w) // 2
        t_y = self.rect.y + (self.rect.w - t_h) // 2
        self.t_rect = pygame.Rect(t_x, t_y, t_w, t_h)

    '''def resize(self, window, matrix):
        """redimensionne selon les valeurs de `Window` une instance de la
        classe Window."""
        # informations générales de l'emplacement de la hold queue
        remaining_space = window['width'] - (matrix['rect'].x + matrix['rect'].w) - window['margin']
        w_value = round(matrix['cell_size'] * 3.7)
        x_axis = (remaining_space - w_value) * 0.7 + window['margin']
        self.width = w_value // 39 + 1
        self.rect = pygame.Rect(x_axis, matrix['rect'].y, w_value, w_value)
        # informations de l'emplacement tetrimino
        # ## tester utilité des variables
        t_w = matrix['cell_size'] * 3
        t_h = matrix['cell_size'] * 2
        t_x = self.rect.x + (self.rect.w - t_w) // 2
        t_y = self.rect.y + (self.rect.w - t_h) // 2
        self.t_rect = pygame.Rect(t_x, t_y, t_w, t_h)'''

    def display(self, surface):
        """affichage de l'encadré associé à la hold queue, avec si y a le
        type du tetrimino hold."""
        # représentation de l'encadré
        pygame.draw.rect(surface, (150, 150, 150),
                         self.rect,
                         self.width)
        # dans le cas où il y a un tetrimino mis de côté, l'afficher
        if self.t_type:
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
    prochaines pièces de la partie en cours."""

    def __init__(self, window, matrix, bag):
        """méthode constructeur de la classe."""
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
        # ## trouver moyen de supprimer self.rect des attributs
        self.rect_1 = pygame.Rect(x_axis, y_axis_1, w_value, h_value[0])
        self.rect_2 = pygame.Rect(x_axis, y_axis_2, w_value, h_value[1])
        # liste des positions 'y' des différents emplacement des tetriminos
        # ## optimiser avec changement de la fonction display_visual_tetrimino
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
        figurent les tetrimino en attente dans l'instance de `Bag`, `surface`
        doit être un objet de type pygame.Surface."""
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


# fonctions plus pour la lisibilité du code
def find_align_center_x(lenght, remaining_place):
    """permet de trouver la position x tel que l'objet que l'on cherche
    à aligner au centre soit centré. Prend en paramètre la taille de la largeur
    de l'objet (`lenght`) et la largeur de l'objet sur lequel on cherche à
    centrer (`remaining_place`)."""
    return (remaining_place - lenght) // 2


class Data:
    """regroupe les données relatifs aux informations du jeu, ainsi que les
    attributs permettant de tracer l'encadré d'affichage du score, niveau,
    nombre de line clear, ...

    ATTRIBUTS:
    - `fall_speed` (float) vitesse de raffraîchissement en ce qui concerne
    le jeu, il s'agit du temps entre deux positions d'un tetrimino en jeu lors
    du falling_phase, ainsi fall_speed détermine la vitesse de la chute du
    tetrimino, variant selon le niveau ;
    - `font` (pygame.Font) font utilisé pour l'affichage ;
    - `rect` (pygame.Rect) rectangle pygame pour dessiner l'encadré de
    l'instance ;
    - `surface` (pygame.Surface) surface sur laquelle se trouve les noms
    des données ('score', 'temps', ...) à leur emplacement ;
    - `values` (dict) stocke les valeurs des données de jeu ;
    - `values_surface` (dict) contient les objets pygame.surface et les
    positions de ces surfaces exprimé en tuple (position x, position y) par
    rapport à l'encadré de data ;
    - `width` (int) largeur du trait devant devant délimiter l'encadré"""

    def __init__(self, window, matrix, chronometer, game_type):
        """méthode constructeur de la classe. Initialise le score
        et les données d'une parties. `window`, `matrix` et `chronometer` sont
        des instances de classes du même nom, `game_type` est un 2-uplet
        contenant dans l'ordre, le niveau et la difficulté imposée au mode B.
        le niveau peut-être compris entre 0 et 10 inclus. La difficulté quant à
        elle est comprise entre 0 et 6 inclus, 6 signifiant qu'il s'agit du mode
        A (le mode B permettant de choisir pour niveau max 5)."""
        level, hight = game_type
        # goal correspond à l'objectif à atteindre avant le passage au niveau
        # suivant. 25 dans le cas du mode B, autrement 5 fois le niveau choisi
        hight -= 1
        goal = 25 if hight - 1 > 0 else level * 5
        first_values = [0, 0, level, goal]
        self.values = {DATA_KEYS[i]: first_values[i] for i in range(4)}
        self.values_surface = {DATA_STRINGS[i]:
                               {'surface': None,
                                'position': None} for i in range(5)}
        self.font = None
        self.surface = None
        self.resize(window, matrix)
        self.chrono_value(chronometer)
        self.values_relative_position()
        self.set_fall_speed()

    def font_resize(self):
        """redimenssione les polices de caractères."""
        w_value, h_value = self.rect.w, self.rect.h
        # attribution d'une marge locale
        local_margin = h_value // 11
        # dimensions que peut occuper le texte prenant en compte une marge
        font_place = (w_value - local_margin, h_value - 2 * local_margin)
        # taille que devrait avoir la hauteur du texte
        font_height = round((0.86 * font_place[1]) / 7)
        # redéfinition de l'attribut font selon les résultats obtenus
        self.font = pygame.font.Font("others/Anton-Regular.ttf",
                                     get_font_size(font_height))
        # liste qui stockera les textes avec les intitulés des données
        name_surface = []
        # constitution de cette liste
        for i in DATA_STRINGS:
            value = game_strings.get_all_strings()[i]
            name_surface.append(self.font.render(value, 1, COLOR['WHITE']))
        # calcul espace nécéssaire entre deux surface contenant du texte
        space_between_string = (font_place[1] - 7 * font_height) // 6
        # création d'un objet surface servant de calque afin d'optimiser le jeu
        surface = pygame.Surface((w_value, h_value))
        # dessin de l'encadré
        pygame.draw.rect(surface, (150, 150, 150),
                         pygame.Rect(self.width,
                                     self.width,
                                     self.rect.w - 2 * self.width,
                                     self.rect.h - 2 * self.width),
                         self.width)
        # position selon axe y par rapport à l'encadré à stocker dans attribut
        # values_surface
        y_value = local_margin
        # correspond à la hauteur occupé par une surface texte
        font_h = name_surface[0].get_size()
        index = 0
        # parcours de VISUAL_STRUCTURE indiquant la présentation de la chose
        for i, element in enumerate(VISUAL_STRUCTURE):
            # dans le cas où `element` vaut None
            if element is None:
                # récupération de la clef, valeur contenu l'indice d'avant
                element = VISUAL_STRUCTURE[i-1]  # ## key = TvT
                # ajout de la valeur de y_value dans le dictionnaire
                self.values_surface[element]['position'] = y_value
                y_value += font_h[1]
            # dans le cas où `element` vaut 0
            elif not element:
                # incrémentation de y_value
                y_value += space_between_string
            # autrement (quand il s'agit d'un string)
            else:
                # ajout du texte sur surface
                surface.blit(name_surface[index], (local_margin // 2, y_value))
                # dans le cas où `index` est supérieur à 1
                if index > 1:
                    # ajout de la valeur de y_value dans le dictionnaire
                    self.values_surface[element]['position'] = y_value
                # incrémentations
                index += 1
                y_value += font_h[1]
        # attribution de surface à l'instance
        self.surface = surface

    def values_relative_position(self):
        """définit les positions des valeurs."""
        w_value, h_value = self.rect.w, self.rect.h
        # attribution d'une marge locale
        local_margin = h_value // 11

        nb_zero_to_fill = [10, 3, 2, 3]
        for i, element in enumerate(DATA_KEYS):
            value = str(self.values[element]).zfill(nb_zero_to_fill[i])
            value_rendered = self.font.render(value, 1, COLOR['WHITE'])
            self.values_surface[element]['surface'] = value_rendered

        pos_x = []
        temp_chrono = Chronometer()  # ##
        self.chrono_value(temp_chrono)  # ##
        for element in DATA_STRINGS[:2]:
            obj_w_value = self.values_surface[element]['surface'].get_size()[0]
            pos_x.append(find_align_center_x(obj_w_value, w_value))
        for element in DATA_STRINGS[2:]:
            obj_w_value = self.values_surface[element]['surface'].get_size()[0]
            pos_x.append(w_value - local_margin - obj_w_value)
        for i, element in enumerate(DATA_STRINGS):
            position = (pos_x[i], self.values_surface[element]['position'])
            self.values_surface[element]['position'] = position

    def set_fall_speed(self):
        """met à jour la valeur du temps entre chaque frame du jeu en accord
        avec la guideline officiel du jeu."""
        level = self.values['level']
        self.fall_speed = (0.8 - (level - 1) * 0.007) ** (level - 1)

    def resize(self, window, matrix):
        """change les attributs relatifs aux dimensions de l'encadré."""
        # informations générales de l'emplacement de l'encadré
        remaining_space = matrix['rect'].x - window['margin']  # ##laisser ?
        w_value = round(matrix['cell_size'] * 7.4)  # ##soucis
        x_axis = (remaining_space - w_value) * 0.72
        y_axis = matrix['rect'].y + w_value
        h_value = matrix['cell_size'] * 21 - y_axis + window['margin']
        self.width = round(matrix['cell_size'] * 3.7) // 39 + 1  # ##changer ?
        self.rect = pygame.Rect(x_axis, y_axis, w_value, h_value)
        # redimensionnement des textes et repositionnement
        self.font_resize()

    def chrono_value(self, chronometer):
        """la valeur du chronomètre est donnée selon celle de `chronometer`
        une instance de la classe Chronometer."""
        chrono_value = chronometer.get_chrono_value()
        chrono_surface = self.font.render(chrono_value, 1, COLOR['WHITE'])
        self.values_surface['time']['surface'] = chrono_surface

    def update(self, chronometer, surface):
        """met à jour les attributs de l'instance."""
        self.chrono_value(chronometer)
        for element in DATA_STRINGS:
            surface.blit(self.values_surface[element]['surface'],
                         self.values_surface[element]['position'])

    def add_to_line_clear(self, value_to_add):
        """ajoute `value_to_add` au nombre de line_clear."""
        self.values['lines'] += value_to_add
        lines = self.font.render(str(self.values['lines']).zfill(3), 1,
                                 COLOR['WHITE'])
        self.values_surface['lines']['surface'] = lines
        self.values['goal'] -= value_to_add
        if self.values['goal'] < 1:
            self.values['level'] += 1
            self.set_fall_speed()
            self.values['goal'] = self.values['level'] * 5
            level = self.font.render(str(self.values['level']).zfill(2), 1,
                                     COLOR['WHITE'])
            self.values_surface['level']['surface'] = level
        goal = self.font.render(str(self.values['goal']).zfill(3), 1,
                                  COLOR['WHITE'])
        self.values_surface['goal']['surface'] = goal

    def score_increase(self, value_to_add):
        """augmente l'attribut score de `value_to_add` devant
        être un entier."""
        self.values['score'] += value_to_add
        score = self.font.render(str(self.values['score']).zfill(10), 1,
                                 COLOR['WHITE'])
        self.values_surface['score']['surface'] = score
