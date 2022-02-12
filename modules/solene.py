"""module codé par Solène (@periergeia) TG8, contenant diverses classes et
fonctions utiles au bon fonctionnement du jeu Tetris."""


# importation de librairies python utiles
import random
import colorsys
import time
import termcolor  # ##à enlever, utile pour test avec print
import pygame
import pygame.freetype

try:
    from collect_file_s_text import get_file_lst
    from constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR, PHASIS_NAME
    from constant import ROTATION_POINT, DATA_KEYS, DATA_STRINGS, LANG
    from diego import clear_lines, GameStrings
    from paul import border_dict
    from useful import get_font_size, loop_starter_pack
except ModuleNotFoundError:
    from modules.collect_file_s_text import get_file_lst
    from modules.constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR
    from modules.constant import ROTATION_POINT, DATA_KEYS, DATA_STRINGS, LANG
    from modules.constant import PHASIS_NAME
    from modules.diego import clear_lines, GameStrings
    from modules.paul import border_dict
    from modules.useful import get_font_size, loop_starter_pack


GAME_STRINGS = GameStrings(LANG)


# pylint: disable=E1101
# pylint: disable=W0231
# (super-init-not-called), il m'est inutile de faire appel à la méthode
# constructeur des classes parent vu que leur méthode constructeur font appel
# à une méthode présente dans la même classe nommée "resize". C'est dans la
# méthode du même nom ("resize") que je fais appel à la classe parent.
# Comprenez que j'évite d'attribuer des attributs inutiles à une classe et que
# les classes parents sont avant tout pratique pour les positions relatives
# des différents objets entre eux.

# supprimer des attributs avec delattr(self, 'field_to_delete') super().__init__(*args, **kwargs)


def resize_all(window_data, obj):
    """"redimensionne toutes les choses nécéssitant d'être
    redimensionnées."""
    # redimensionne chaque objet avec leur méthode resize
    for element in obj[1:]:
        element.resize(window_data)
    obj[-1].values_relative_position()


def display_all(window, chronometer, obj):
    """raffraîchit le jeu en faisant afficher une frame,
    contenant les objets dont les caractéristiques ont été
    mis à jour."""
    #  ###############provisoire
    menubutton = pygame.image.load("./image/menubutton.png").convert_alpha()
    # création d'une surface
    frame = pygame.Surface(window.get_size())
    # affichage de l'image pour le boutton des menus, ## voir arrangement ?
    menu_image = pygame.transform.scale(menubutton,
                                        (obj[4].rect.w,
                                        obj[4].rect.h))
    frame.blit(menu_image, (obj[4].rect.x, obj[4].rect.y))
    # affiche chaque objet avec leur méthode display
    for element in obj:
        element.display(frame)
    # dessin de la ghost piece
    if obj[0].state != 2:
        # ## test à enlever si pas de soucis
        if obj[1].draw_ghost_piece(frame, obj[0]) == "ERROR snif :')":
            pygame.image.save(window, "screenshot.jpeg")
    # frame sur la fenêtre
    window.blit(frame, (0, 0))
    # ## voir à supprimer ?
    display_game_data(window, obj[5], chronometer)
    # rafraichissement de la fenêtre pygame
    pygame.display.flip()


def display_game_data(window, data, chronometer):
    """affiche les données de jeu dans l'encadré de Data."""
    frame_size = (data.rect.w - 2 * data.width, data.rect.h - 2 * data.width)
    # création d'un objet pygame.Surface de la taille de l'encadré data
    frame = pygame.Surface(frame_size)
    frame.blit(data.surface, (0, 0))
    data.update(chronometer, frame)
    window.blit(frame, (data.rect.x + data.width, data.rect.y + data.width))
    pygame.display.flip()


def game_pause():
    """crée un visuel permettant au joueur de comprendre que le
    jeu est mis en pause."""


def gameplay(window, game_type, lang):
    """gameplay du jeu tetris."""
    w_width, w_height = window.get_size()
    window_data = {'size': (w_width, w_height),
                   'width': w_width,
                   'height': w_height,
                   'margin': round(0.05 * w_height)}
    bag = Bag()
    game_chrono = Chronometer()
    matrix = Matrix(window_data, game_type)
    next_queue = NextQueue(window_data)
    hold_queue = HoldQueue(window_data)
    menu_button = MenuButton(window_data)
    data = Data(window_data, lang, game_chrono, game_type)

    tetrimino = Tetrimino(matrix)

    game_object = (tetrimino, matrix, next_queue, hold_queue, menu_button, data)

    display_all(window, game_chrono, game_object)


    time_before_refresh = Chronometer()
    lock_down_chrono = Chronometer()
    SHADE_PHASE = 1
    LOCK_PHASE_FIRST = 1
    softdrop = False

    while True:

        game_object = (tetrimino, matrix, next_queue, hold_queue, menu_button, data)

        # évènements pygame
        for event in pygame.event.get():
            window = loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                window_data = {'size': (window_w, window_h),
                               'width': window_w,
                               'height': window_h,
                               'margin': round(0.05 * window_h)}
                print(f'current window size :   {window_data}')
                # reaffichage avec changement des tailles et emplacement des objets
                resize_all(window_data, game_object)
                display_all(window, game_chrono, game_object)

            # ## à enlever en fin
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    softdrop = False
                    data.set_fall_speed()

            if event.type == pygame.KEYDOWN:

                key_mod = pygame.key.get_mods()
                key = pygame.key.get_pressed()

                if key[pygame.K_F1] or key[pygame.K_ESCAPE]:
                    game_pause()

                elif key[pygame.K_SPACE]:
                    tetrimino.hard_drop(data)

                elif key[pygame.K_DOWN]:
                    softdrop = True
                    data.fall_speed /= 20  # ## pas bon

                elif key[pygame.K_RIGHT]:
                    tetrimino.move_right(matrix)

                elif key[pygame.K_LEFT]:
                    tetrimino.move_left(matrix)



                elif key[pygame.K_UP] or key[pygame.K_x]:
                    tetrimino.turn_right(matrix)

                elif event.key == pygame.K_c or (event.mod and pygame.KMOD_SHIFT):
                    if hold_queue.can_hold:
                        temp = hold_queue.get_t_type()
                        hold_queue.hold(tetrimino)
                        # dans le cas où la hold queue n'est pas vide
                        if temp:
                            tetrimino.set_type(temp)
                            tetrimino.set_y(0)
                            tetrimino.find_lower_pos(matrix)
                        # si vide
                        else:
                            # création d'un nouveau tetrimino
                            tetrimino = Tetrimino(matrix)

                display_all(window, game_chrono, game_object)

        # phase précédant le lock down
        if tetrimino.state == 1:
            # permet de jouer sur la couleur du tetrimino
            values = tetrimino.lock_phase(matrix, lock_down_chrono,
                                        LOCK_PHASE_FIRST, SHADE_PHASE)
            LOCK_PHASE_FIRST, SHADE_PHASE = values
            display_all(window, game_chrono, game_object)
            time.sleep(0.015)

        # phase lock down
        elif tetrimino.state == 2:
            # le tetrimino est lock dans matrix
            tetrimino.lock_on_matrix(matrix)
            # le tetrimino suivant est créé
            tetrimino = Tetrimino(matrix)
            hold_queue.allow_hold()
            display_all(window, game_chrono, game_object)
            # clear les lines s'il y a
            matrix.clear_lines(data)
            display_all(window, game_chrono, game_object)
            # le chronomètre est raffraîchi
            time_before_refresh.reset()

        # dans le cas où le tetrimino est en falling phase
        else:
            # dans le cas où le joueur souhaite faire un softdrop
            # spécifié par le fait que la touche flèche bas est
            # maintenue pressée
            if time_before_refresh == data.fall_speed:
                # score incrémenté de 1 lorsque le tetrimino peut tomber
                if tetrimino.fall(matrix) and softdrop:
                    data.score_increase(1)
                # on reinitialise le chrono
                time_before_refresh.reset()
            # reaffichage de l'écran
            display_all(window, game_chrono, game_object)
        # ##pour tester au besoin
        # display_all(window_data, game_object)
        display_game_data(window, data, game_chrono)


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
        self.reset()

    # ##enlever ?
    def time_elapsed(self):
        """renvoie le temps passé depuis l'initialisation
        du chronomètre"""
        return time.time_ns() - self.time

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

    content = list(range(1, 8))
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
    """modélisation de matrix dans laquelle tombent les tetrimino."""

    def __init__(self, window, game_type):
        """initialisation des différents attribut de la classe Matrix."""
        self.resize(window)
        self.content = [[0 for j in range(10)] for i in range(22)]
        self.modelisation = [22 for i in range(10)]
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
            for i in range(10):
                if self.modelisation[i] != 22:
                    self.modelisation[i] += 1
            self.higher_row -= 1

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

    # ## optimiser
    def draw_ghost_piece(self, surface, tetrimino):
        """dessin de la ghost piece."""
        color = Tetrimino.COLOR_SHADE[tetrimino.type][tetrimino.shade]
        line_to_draw = Tetrimino.BORDER[tetrimino.type][tetrimino.phasis]
        pos_y = tetrimino.lower_pos
        # dessin des lignes en haut
        for element in line_to_draw[0]:
            coordinates = element[0]
            line_lenght = element[1] * self.cell_size
            try:
                x = self.cell[tetrimino.x_coordinate + coordinates[1]][coordinates[0] + pos_y].x
                y = self.cell[tetrimino.x_coordinate + coordinates[1]][coordinates[0] + pos_y].y
                pygame.draw.line(surface, color,
                             (x, y),
                             (x + line_lenght, y), 3)
            # pour le moment
            except KeyError:
                pass
        # dessin des lignes à droite
        for element in line_to_draw[1]:
            coordinates = element[0]
            line_lenght = element[1] * self.cell_size
            try:
                x = self.cell_size + self.cell[tetrimino.x_coordinate + coordinates[1]][coordinates[0] + pos_y].x
                y = self.cell[tetrimino.x_coordinate + coordinates[1]][coordinates[0] + pos_y].y
                pygame.draw.line(surface, color,
                             (x, y),
                             (x, y + line_lenght), 3)
            # pour le moment
            except KeyError:
                pass
        # dessin des lignes en dessous
        for element in line_to_draw[2]:
            coordinates = element[0]
            line_lenght = element[1] * self.cell_size
            try:
                x = self.cell[tetrimino.x_coordinate + coordinates[1]][coordinates[0] + pos_y].x
                y = self.cell_size + self.cell[tetrimino.x_coordinate + coordinates[1]][coordinates[0] + pos_y].y
                pygame.draw.line(surface, color,
                             (x, y),
                             (x + line_lenght, y), 3)
            # pour le moment
            except KeyError:
                pass
        # dessin des lignes à gauche
        for element in line_to_draw[3]:
            coordinates = element[0]
            line_lenght = element[1] * self.cell_size
            try:
                x = self.cell[tetrimino.x_coordinate + coordinates[1]][coordinates[0] + pos_y].x
                y = self.cell[tetrimino.x_coordinate + coordinates[1]][coordinates[0] + pos_y].y
                pygame.draw.line(surface, color,
                                 (x, y),
                                 (x, y + line_lenght), 3)
            # pour le moment
            except KeyError:
                pass


def start_center(tetrimino_type):
    """indique l'indice permettant de centrer un tetrimino
    selon son type (spécifié en argument de la fonction, un
    entier compris entre 1 et 7 inclus) dans matrice."""
    return (10 - len(TETRIMINO_SHAPE[tetrimino_type])) // 2


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

    def __init__(self, matrix):
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
        for element in Tetrimino.ROTATION_PHASIS[self.type][self.phasis]:
            stock += ' '.join(str(element))
            stock += '\n'
        stock += f'\n type du tetrimino : {TETRIMINO_SHAPE[self.type]}'
        return stock

    # ## si 2 --> test pour voir si line clear ou autre, puis passage au
    # tetrimino suivant version non finie, il reste à déterminer les cas
    # où le tetrimino sort de la matrice !
    def __current_state__(self):
        """renvoie:
        - 0 si le tetrimino est en 'falling phase', c'est-à-dire que le
        tetrimino continue à tomber
        - 1 si le tetrimino est en 'lock phase', phase où le tetrimino
        s'apprête à se figer dans la matrice avec un temps escompté
        - 2 lorsque le tetrimino est en 'completion phase'"""

    def lock_on_matrix(self, matrix):
        """Méthode permettant de lock un tetrimino (celui de l'instance),
        dans sur la matrix de jeu. `matrix` est une instance de la classe
        Matrix."""
        t_type = self.type
        t_phasis = self.phasis
        tetrimino_shape = self.ROTATION_PHASIS[t_type][t_phasis]
        tetrimino_lenght = len(tetrimino_shape)
        for i in range(tetrimino_lenght):
            for j in range(tetrimino_lenght):
                if tetrimino_shape[j][i] == 1:
                    pos_y = self.y_coordinate + j
                    pos_x = self.x_coordinate + i
                    matrix.content[pos_y][pos_x] = self.type
                    # ajoute à modelisation au besoin afin de créer
                    # un sorte de cartographie des plus haut à chaque fois
                    if pos_y < matrix.modelisation[pos_x]:
                        matrix.modelisation[pos_x] = pos_y
                        if matrix.modelisation[pos_x] < matrix.higher_row:
                            matrix.higher_row = matrix.modelisation[pos_x]

    def can_fall(self, matrix):
        """test afin de vérifier si un tetrimino peut tomber.
        Il prend en paramètre `matrix` une instance de la classe Matrix,
        et renvoie un booléen correspondant à l'issue du test (succès ou
        échec)."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
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
        coordinates = (self.x_coordinate, self.y_coordinate)
        try:
            test_list = ROTATION_POINT[t_type][current_phasis][next_phasis]
            for rotation_test in test_list:
                # déplacement des coordonnées selon les test
                self.x_coordinate = coordinates[0] + rotation_test[0]
                self.y_coordinate = coordinates[1] + rotation_test[1]
                if self.test_around(matrix, tetrimino_shape, nb_column):
                    return True
        # s'opère lorsque phasis vaut SOUTH pour un tetrimino 3x2
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
        if self.can_fall(matrix):
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

    '''def find_lower_pos(self, matrix):
        """renvoie la position la plus basse pouvant être atteinte par
        l'instance afin de déterminer la position des ordonnées de la ghost
        piece dans `matrix`. La méthode prend en paramètre `matrix` une
        instance de la classe Matrix."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
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
        self.y_coordinate = y_coordinate'''
    
    
    def find_lower_pos(self, matrix):
        """renvoie la position la plus basse pouvant être atteinte par
        l'instance afin de déterminer la position des ordonnées de la ghost
        piece dans `matrix`. La méthode prend en paramètre `matrix` une
        instance de la classe Matrix."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
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
        tetrimino_shape = self.ROTATION_PHASIS[self.type][self.phasis]
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
        left = Tetrimino.BORDER[self.type][self.phasis][3]
        left_most = 4
        for shift in left:
            if shift[0][1] < left_most:
                left_most = shift[0][1]
        return left_most + self.x_coordinate

    # ## n'est pas utilisé pour le moment, voir par la suite
    def rightmost(self):
        """renvoie la plus grande valeur x d'un mino."""
        # on selectionne les bords droit du tetrimino
        right = Tetrimino.BORDER[self.type][self.phasis][1]
        right_most = 0
        for shift in right:
            if shift[0][1] + shift[1] > right_most:
                right_most = shift[0][1]
        return right_most + self.x_coordinate

    def fall(self, matrix):
        """permet de faire tomber le tetrimino, s'il ne peut pas,
        le tetrimino passe en lock phase. A pour paramètre une instance de
        la classe Matrix."""
        # teste si le tetrimino est apte à tomber
        if self.can_fall(matrix):
            return True
        # le test a échoué, le tetrimino ne peut pas tomber,
        # on passe en lock phase
        self.state = 1
        return False

    def move_left(self, matrix):
        """déplace d'une case vers la gauche le tetrimino."""
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
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
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
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
        phasis = (self.phasis - 1) % 4
        if self.super_rotation_system(matrix, phasis):
            self.phasis = phasis
            # redéfini emplacement de la ghost piece
            self.find_lower_pos(matrix)

    def turn_right(self, matrix):
        """permet de tourner le tetrimino de 90° dans le sens
        anti-horaire."""
        phasis = (self.phasis + 1) % 4
        if self.super_rotation_system(matrix, phasis):
            self.phasis = phasis
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
        remaining_space = window['width'] - (self.rect.x + self.rect.w) - window['margin']
        w_value = self.rect.h = round(self.cell_size * 3.7)
        x_axis = (remaining_space - w_value) * 0.7 + window['margin']
        self.width = self.rect.h // 39 + 1
        self.rect = pygame.Rect(x_axis, self.rect.y, w_value, self.rect.h)
        # informations de l'emplacement tetrimino
        # ## tester utilité des variables
        t_w = self.cell_size * 3
        t_h = self.cell_size * 2
        t_x = self.rect.x + (self.rect.w - t_w) // 2
        t_y = self.rect.y + (self.rect.w - t_h) // 2
        self.t_rect = pygame.Rect(t_x, t_y, t_w, t_h)

    def display(self, surface):
        """affichage de l'encadré associé à la hold queue, avec si y a le
        type du tetrimino hold."""
        # représentation de l'encadré
        pygame.draw.rect(surface, (150, 150, 150),
                         self.rect,
                         self.width)
        # dans le cas où il y a un tetrimino mis de côté, l'afficher
        try:
            if self.t_type:
                display_visual_tetrimino(surface, self, self.t_rect.y,
                                         self.t_type)
        # afin de ne pas définir un attribut t_type à des instances de
        # MenuButton et Data
        except AttributeError:
            pass

    def get_t_type(self):
        """renvoie le type du tetrimino dans la hold_queue, un int compris
        entre 0 et 7 inclus. 0 signifiant que la hold queue est vide."""
        return self.t_type

    def allow_hold(self):
        """permet de reinitialiser l'attribut can_hold à l'appel de la
        méthode."""
        self.can_hold = True


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
        matrix_place = self.rect.x + self.rect.w
        remaining_space = window['width'] - matrix_place - window['margin']
        # évaluation des paramètres utiles pour définir les encadrés
        w_value = round(self.cell_size * 3.7)
        h_value = (w_value, round(self.rect.h*0.9) - w_value)
        x_axis = (round((remaining_space - w_value) * 0.3)) + matrix_place
        y_axis_1 = self.rect.y
        y_axis_2 = round(y_axis_1 + w_value + (self.rect.h / 10))
        self.width = h_value[0] // 39 + 1
        # ## trouver moyen de supprimer self.rect des attributs
        self.rect_1 = pygame.Rect(x_axis, y_axis_1, w_value, h_value[0])
        self.rect_2 = pygame.Rect(x_axis, y_axis_2, w_value, h_value[1])
        # liste des positions 'y' des différents emplacement des tetriminos
        # ## optimiser avec changement de la fonction display_visual_tetrimino
        t_w = self.cell_size * 3
        t_h = self.cell_size * 2
        t_x = x_axis + (w_value - t_w) // 2
        self.next_y = [y_axis_1 + (w_value - t_h) // 2]
        space = (h_value[1] - 5 * t_h) // 6
        # y_axis comme variable définissant successivement les ordonnées y
        # pour les différents tetrimino visuel
        y_axis_2 += space
        for _ in range(5):
            t_place = y_axis_2
            y_axis_2 += t_h + space
            self.next_y.append(t_place)
        self.t_rect = pygame.Rect(t_x, 0, t_w, t_h)

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
                                     self.next_y[i - 1], self.content[-i])


# ## à changer, utiliser classe Button retravaillé par Bastien
class MenuButton(HoldQueue, NextQueue):
    """crée le boutton de jeu."""

    def __init__(self, window):
        """initialisation de l'instance."""
        self.resize(window)

    def resize(self, window):
        """redimensionne selon les valeurs de `Window` une instance de la
        classe Window."""
        # informations générales de l'emplacement de la hold queue
        super().resize(window)
        w_value = self.rect_1.h = self.rect_1.w // 2
        remaining_space = window['width'] - self.rect_1.x - self.rect_1.w - w_value
        x_axis = self.rect_1.x + self.rect.w + (remaining_space // 2)
        self.width = self.rect_1.h // 39 + 1
        self.rect = pygame.Rect(x_axis, self.rect_1.y, w_value, self.rect_1.h)

    # ###
    def bind(self):
        """affichage dans le cas où le boutton est appuyé."""


# fonctions plus pour la lisibilité du code
def find_align_center_x(lenght, remaining_place):
    """permet de trouver la position x tel que l'objet que l'on cherche
    à aligner au centre soit centré. Prend en paramètre la taille de la largeur
    de l'objet (`lenght`) et la largeur de l'objet sur lequel on cherche à
    centrer (`remaining_place`)."""
    return (remaining_place - lenght) // 2


# ## garder ?
'''def find_align_right_x(lenght, remaining_place):
    """permet de trouver la position x tel que l'objet que l'on cherche
    à aligner soit à droite. Prend en paramètre la taille de la largeur
    de l'objet (`lenght`) et la largeur de l'objet sur lequel on cherche à
    centrer (`remaining_place`)."""
    return remaining_place - lenght'''


class Data(HoldQueue):
    """regroupe les données relatifs aux informations du jeu, ainsi que les
    attributs permettant de tracer l'encadré d'affichage du score, niveau,
    nombre de line clear, ...

    attributs des instances:
    - font
    - margin
    - name
    - rect
    - values
    - values_surface
    - width

    à supprimer :
    cell_size
    """

    def __init__(self, window, lang, chronometer, game_type):
        """méthode constructeur de la classe. Initialise le score
        et les données d'une parties."""
        level, hight = game_type
        goal = 25 if hight else level * 5
        first_values = [0, 0, level, goal]
        self.values = {DATA_KEYS[i]: first_values[i] for i in range(4)}
        self.name = GAME_STRINGS.get_all_strings()
        self.resize(window)
        self.values_surface = [None, 0]
        self.chrono_value(chronometer)
        self.values_relative_position()  # ##
        self.set_fall_speed()

    def change_text_language(self, lang):
        """change la langue du texte selon `lang` une chaîne de caractère."""
        self.name = GAME_STRINGS.get_all_strings()
        self.font_resize()

    def font_resize(self):
        """redimenssione les polices."""
        w_value, h_value = self.rect.w, self.rect.h
        # attribution d'une marge locale
        local_margin = h_value // 11
        # ## font place en tant que variable plutôt qu'attribut ?
        font_place = (w_value - local_margin, h_value - 2 * local_margin)
        # taille que devrait avoir la hauteur du texte
        font_height = round((0.86 * font_place[1]) / 7)
        font_size = get_font_size(font_height)
        # redéfinition de l'attribut font selon les résultats obtenus
        self.font = pygame.font.Font("others/Anton-Regular.ttf", font_size)
        name_surface = []
        for i in DATA_STRINGS:
            name_surface.append(self.font.render(self.name[i], 1, COLOR['WHITE']))
        space_between_string = (font_place[1] - 7 * font_height) // 6

        # création d'un objet surface servant de calque afin d'optimiser le jeu
        surface = pygame.Surface((w_value - 2 * self.width, h_value - 2 * self.width))
        temp = [1, None, 0, 1, None, 0, 0, 0, 1, 0, 1, 0, 1]
        y_value = local_margin
        self.position = []
        font_h = name_surface[0].get_size()
        i = 0
        for element in temp:
            if element == 1:
                surface.blit(name_surface[i], (local_margin // 2, y_value))
                if i > 1:
                    self.position.append(y_value)
                i += 1
                y_value += font_h[1]
            elif element is None:
                self.position.append(y_value)
                y_value += font_h[1]
            else:
                y_value += space_between_string

        self.surface = surface

    def values_relative_position(self):
        """définit les positions des valeurs."""
        w_value, h_value = self.rect.w, self.rect.h
        # attribution d'une marge locale
        local_margin = h_value // 11

        nb_zero_to_fill = [10, 3, 2, 3]
        chrono_save = self.values_surface[1]
        self.values_surface = [self.font.render(str(self.values[DATA_KEYS[i]]).zfill(nb_zero_to_fill[i]), 1, COLOR['WHITE']) for i in range(4)]
        self.values_surface.insert(1, chrono_save)
        # ## recours boucle pour ne pas dépasser limite de 79 caractères
        '''for i in range(4):
            # ##besoin d'un nom à un caractère TvT
            j = str(self.values[DATA_KEYS[i]]).zfill(nb_zero_to_fill[i])
            self.values_surface.append(self.font.render(j, 1, COLOR['WHITE']))
        self.values_surface.insert(1, chrono_save)'''

        pos_x = []
        termcolor.cprint(self.position, 'red')
        temp_chrono = Chronometer()  # ##
        self.chrono_value(temp_chrono)  # ##
        print(self.values_surface)
        for i in range(2):
            obj_w_value = self.values_surface[i].get_size()[0]
            pos_x.append(find_align_center_x(obj_w_value, w_value))
        for i in range(2, 5):
            obj_w_value = self.values_surface[i].get_size()[0]
            pos_x.append(w_value - local_margin - obj_w_value)

        for i in range(5):
            self.position[i] = ((pos_x[i], self.position[i]))

    def set_fall_speed(self):
        """met à jour la valeur du temps entre chaque frame du jeu en accord
        avec la guideline officiel du jeu."""
        level = self.values['level']
        self.fall_speed = (0.8 - (level - 1) * 0.007) ** (level - 1)

    """SCORING (aide-mémoire) :
    There is a special bonus for Back-to-Backs, which is when two actions such as a Tetris and
    T-Spin Double (see complete list below) take place without a Single, Double, or Triple Line
    Clear occurring between them.

    Action              Action Total        Description
    Mini T-Spin         100 x Level         An easier T-Spin with no Line Clear.
    Mini T-Spin Single  200 x Level         An easier T-Spin clearing 1 line of Blocks.
    T-Spin              400 x Level         T-Tetrimino is spun into a T-Slot with no Line Clear.
    T-Spin Single       800 x Level         T-Spin clearing 1 line of Blocks.
    T-Spin Double       1200 x Level        T-Spin simultaneously clearing 2 lines of 10 Blocks.
    T-Spin Triple       1600 x Level        T-Spin simultaneously clearing 3 lines of 10 Blocks.
    Back-to-Back Bonus  0.5 x Action        Total Bonus for Tetrises, T-Spin Line Clears, and Mini
                                            T-Spin Line Clears performed consecutively in a B2B
                                            sequence."""

    def resize(self, window):
        """change les attributs relatifs aux dimensions de l'encadré."""
        # informations générales de l'emplacement de l'encadré
        super().resize(window)
        x_axis = self.rect.x - self.rect.w
        # dans le cas où la marge n'est pas respectée
        if x_axis < window['margin']:
            x_axis = window['margin']
            w_value = self.rect.w + self.rect.x - x_axis
        else:
            w_value = self.rect.w * 2
        y_axis = self.rect.y + self.rect.h * 2
        h_value = self.cell_size * 21 - y_axis + window['margin']
        self.rect = pygame.Rect(x_axis, y_axis, w_value, h_value)
        # redimensionnement des textes et repositionnement
        self.font_resize()

    def chrono_value(self, chronometer):
        """la valeur du chronomètre est donnée selon celle de `chronometer`
        une instance de la classe Chronometer."""
        chrono_value = chronometer.get_chrono_value()
        self.values_surface[1] = self.font.render(chrono_value, 1,
                                                  COLOR['WHITE'])

    def update(self, chronometer, surface):
        """met à jour les attributs de l'instance."""
        self.chrono_value(chronometer)
        for i in range(5):
            surface.blit(self.values_surface[i], self.position[i])

    def add_to_line_clear(self, value_to_add):
        """ajoute `value_to_add` au nombre de line_clear."""
        self.values['lines'] += value_to_add
        lines = self.font.render(str(self.values['lines']).zfill(3), 1,
                                 COLOR['WHITE'])
        self.values_surface[2] = lines
        self.values['goal'] -= value_to_add
        if self.values['goal'] < 1:
            self.values['level'] += 1
            self.set_fall_speed()
            self.values['goal'] = self.values['level'] * 5
            level = self.font.render(str(self.values['level']).zfill(2), 1,
                                     COLOR['WHITE'])
            self.values_surface[3] = level
        chrono = self.font.render(str(self.values['goal']).zfill(3), 1,
                                  COLOR['WHITE'])
        self.values_surface[4] = chrono

    def score_increase(self, value_to_add):
        """augmente l'attribut score de `value_to_add` devant
        être un entier."""
        self.values['score'] += value_to_add
        score = self.font.render(str(self.values['score']).zfill(10), 1,
                                 COLOR['WHITE'])
        self.values_surface[0] = score
