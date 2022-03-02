"""module codé par Solène (@periergeia) TG8, contenant diverses classes et
fonctions utiles au bon fonctionnement du jeu Tetris."""


# importation de librairies python
import random
import colorsys
import time
import pygame
import pygame.freetype
try:
    from constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR, PHASIS_NAME
    from constant import ROTATION_POINT, DATA_KEYS, MULTIPLY_BY
    from constant import DATA_STRINGS, LANG, VISUAL_STRUCTURE
    from diego import clear_lines, GameStrings
    from paul import border_dict
    from useful import get_font_size, Button1
except ModuleNotFoundError:
    from modules.constant import TETRIMINO_DATA, TETRIMINO_SHAPE, COLOR
    from modules.constant import ROTATION_POINT, DATA_KEYS, MULTIPLY_BY
    from modules.constant import DATA_STRINGS, LANG, VISUAL_STRUCTURE
    from modules.constant import PHASIS_NAME
    from modules.diego import clear_lines, GameStrings
    from modules.paul import border_dict
    from modules.useful import get_font_size, Button1


game_strings = GameStrings(LANG)

# pylint: disable=E1101


def resize_all(window_data, game_objet):
    """"redimensionne tous les objets contenus dans `game_objet`
    nécéssitant d'être redimensionnés."""
    # redimensionnement de matrix
    game_objet[1].resize(window_data)
    # récupération des nouvelles valeurs de matrix
    matrix_data = {'rect': game_objet[1].rect,
                   'cell_size': game_objet[1].cell_size}
    # redimensionne chaque objet avec leur méthode resize
    for element in game_objet[2:5]:
        element.resize(window_data, matrix_data)
    game_objet[5].resize(window_data)


def display_all(window, game_objet):
    """raffraîchit le jeu en faisant afficher une frame contenant les objets
    de `game_objet` dont les caractéristiques ont été mis à jour."""
    # création d'une surface
    frame = pygame.Surface(window.get_size())
    # rect pour l'emplacement de Data
    transparent_rect = pygame.Surface(game_objet[4].get_size())
    transparent_rect.fill((45, 0, 0))
    # ajout de transparent_rect sur frame
    frame.blit(transparent_rect, game_objet[4].get_position())
    # réglage de la transparence du rect pour l'emplacement de data
    frame.set_colorkey((45, 0, 0))
    # affiche chaque objet avec leur méthode display
    for element in game_objet[:-2]:
        element.display(frame)
    # dessin du bouton des options
    game_objet[5].draw(frame)
    # dessin de la ghost piece
    game_objet[1].draw_ghost_piece(frame, game_objet[0])
    # frame sur la fenêtre
    window.blit(frame, (0, 0))
    # rafraichissement de la fenêtre pygame
    pygame.display.flip()


def display_game_data(window, data, chronometer):
    """affiche les données de jeu dans l'encadré de Data."""
    # création d'un objet pygame.Surface de la taille de l'encadré data
    frame = pygame.Surface(data.get_size())
    frame.blit(data.surface, (0, 0))
    # ajout des informations de données du jeu
    data.update(chronometer, frame)
    # affiche frame à son emplacement
    window.blit(frame, data.get_position())
    # raffraîchissement de la fenêtre pygame
    pygame.display.flip()


def create_game_pause(window):
    """crée un visuel permettant au joueur de comprendre que le jeu
    est mis en pause. La fonction renvoie les deux boutons crées."""
    # représentation du bouton pour reprendre le jeu
    resume_button = Button1(window,
                            (0.25,
                             0.3,
                             0.5,
                             0.15),
                            game_strings.get_string("resume"),
                            (75, 75, 75))
    # représentation du bouton des options
    option_button = Button1(window,
                            (0.25,
                             0.55,
                             0.5,
                             0.15),
                            game_strings.get_string("options"),
                            (75, 75, 75))
    # création d'une frame occupant toute la fenêtre
    frame = pygame.Surface(window.get_size())
    # transparence de la frame
    frame.set_colorkey((0, 0, 0))
    # représente le fond du menu
    background = Button1(window,
                         (0.1,
                          0.1,
                          0.78,
                          0.8),
                         '',
                         (100, 100, 100))
    # dessins des différent objets Button1 créés
    background.draw(frame)
    resume_button.draw(frame)
    option_button.draw(frame)
    # ajout de frame sur la fenêtre de jeu
    window.blit(frame, (0, 0))
    # raffraîchissement de la fenêtre pygame
    pygame.display.flip()
    # renvoi des boutons créés
    return resume_button, option_button


def get_game_picture(window):
    """(fonction réalisée par @Jouca) fait une sauvegarde du
    jeu sous la forme d'un pygame.Surface.
    La fonction renvoie deux éléments, le premier correspond à
    la capture d'écran avec un assombrissement et le deuxième
    est la capture d'écran. Tout deux sont sous forme de
    pygame.Surface."""
    screenshot = window.subsurface(window.get_rect())
    normal_screenshot = screenshot.copy()
    screen_window = pygame.Surface(screenshot.get_size())
    screenshot.set_alpha(60)
    screen_window.blit(screenshot, (0, 0))
    return screen_window, normal_screenshot


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


def turn_right(tetrimino, facing):
    """fait tourner une pièce tetrimino avec une rotation
    vers la droite. Utilise la récursivité.
    - `tetrimino` : modélisé par une matrice ;
    - `facing` : un entier compris entre 0 et 3 modélisant l'orientation.
    Renvoie une matrice correspondant à la phase indiquée.
    >>> turn_right([[0, 0, 1], [1, 1, 1], [0, 0, 0]], 2)
    [[0, 0, 0], [1, 1, 1], [1, 0, 0]]
    >>> turn_right([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]], 3)
    [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]"""
    # dans le cas où le tetrimino n'a plus besoin d'être tourné
    if facing == 0:
        # renvoie du tetrimino
        return tetrimino
    # décrémentation de facing
    facing -= 1
    # création d'une liste vide pour la matrice du tetrimino ayant subi une
    # rotation de 90° dans le sens horaire
    rotated_tetrimino = []
    for i in range(len(tetrimino)):
        # liste vide pour une ligne de la modélisation d'un tetrimino
        tetrimino_line = []
        for j in range(len(tetrimino)-1, -1, -1):
            tetrimino_line.append(tetrimino[j][i])
        rotated_tetrimino.append(tetrimino_line)
    # auto-appel jusqu'à ce que le tetrimino n'ait plus à tourner pour
    # correspondre à la modelisation du tetrimino avec l'orientation voulue
    return turn_right(rotated_tetrimino, facing)


def change_color_luminosity(color, rate_of_change):
    """change la luminosité de la couleur, renvoie un tuple rgb de la couleur
    assombrie selon `rate_of_change`, un entier. `couleur` doit être un tuple
    représentant les valeurs rgb (chaque entier est compris entre 0 et 255).
    Renvoie une couleur éclaircie à la condition que `rate_of_change` soit
    négatif.
    >>> change_color_luminosity((150, 150, 150), 15)
    (135, 135, 135)
    >>> change_color_luminosity((150, 3, 204), 27)
    (130, 3, 177)"""
    red, green, blue = color
    # conversion de la couleur au format hsv plus adapté pour assombrir
    hue, saturation, lightness = colorsys.rgb_to_hsv(red, green, blue)
    # le paramètre de la luminosité est diminué de `rate_of_change`
    lightness -= rate_of_change
    # la couleur est reconvertie vers le format rgb
    temp_color = colorsys.hsv_to_rgb(hue, saturation, lightness)
    final_color = [0, 0, 0]
    for i, primary in enumerate(temp_color):
        # permet d'obtenir des valeurs entières et non les float
        # renvoyé par l'usage de la méthode hsv_to_rgb du module colorsys
        final_color[i] = round(primary)
    return tuple(final_color)


class RadioButton:
    """classe permettant de selectionner un bouton parmi plusieurs.
    Donner une priorité selon des évènements pygame.

    ATTRIBUTS DE CLASSE:
    - `select_sound` est un objet de la classe Sound de la librairie pygame,
    il s'agit du son qui sera diffusé à chaque fois qu'un changement de
    priorité entre les boutons s'effectue.

    ATTRIBUTS:
    - `attribute` (dict) dictionnaire attribuant à chaque bouton concerné
    par l'instance un numéro selon l'ordre dans lequel il est donné lors
    de l'instanciation ;
    - `button_list` (tuple) contient les boutons concernés par le système
    de radio button ;
    - `color` (dict), un dictionnaire ayant deux valeurs exprimé en rgb:
        - 'priority': (tuple) couleur de base du bouton ;
        - 'non-priority': (tuple) couleur plus sombre permettant de signifier
        que le bouton n'est pas prioritaire ;
    - `nb_button` (int) représente le nombre de boutons, existe afin
    d'optimiser le jeu et ne pas recalculer le nombre de bouton à vérifier à
    chaque tour de boucle et/ou appel d'une méthode de cette classe ;
    - `priority`: objet bouton ayant la priorité, par défaut le premier de la
    `button_list`. autrement, le bouton prioritaire change selon la méthode
    utilisé prenant en compte le placement de la souris sur un bouton ou
    un clic gauche de la souris sur un bouton."""

    select_sound = pygame.mixer.Sound('sound/select.wav')

    def __init__(self, list_of_button):
        """méthode constructrice de la classe. `list_of_button` est un tuple
        contenant des objets useful.Button1 indiquant les boutons créé concerné
        par le système radio à définir."""
        self.nb_button = len(list_of_button)
        self.priority = list_of_button[0]
        self.button_list = list_of_button
        self.attribute = {list_of_button[i]: i for i in range(self.nb_button)}
        priority_color = self.priority.get_color()
        # définition d'une couleur non prioritaire
        darker_color = change_color_luminosity(self.priority.get_color(), 40)
        # dictionnaire contenant les couleurs des boutons
        self.color = {'priority': priority_color, 'non-priority': darker_color}
        # change la couleur de tous les autres boutons de la listes
        # (tout sauf le premier) en la couleur non prioritaire
        for element in list_of_button[1:]:
            element.change_color(darker_color)

    def get_value(self):
        """renvoie la valeur du bouton prioritaire."""
        return self.attribute[self.priority]

    def change_visibility(self, last_priority, current_priority):
        """change la visibilité d'un bouton en influant sur la couleur de fond
        du bouton. `last_priority` est rendu plus sombre tandis que
        `current_priority` est éclairci (tous deux sont des objets
        useful.Button1)."""
        last_priority.change_color(self.color['non-priority'])
        current_priority.change_color(self.color['priority'])

    def give_priority(self, event):
        """détecte s'il y a nécéssité de changer de priorité,
        renvoie un booléen répondant à la question de la nécéssité."""
        # pour chaque bouton concerné
        for i in range(self.nb_button):
            # dans le cas où la souris se situe sur un bouton
            if self.button_list[i].mouse_on(event):
                button = self.button_list[i]
                # si ce bouton n'avait pas la priorité
                if button != self.priority:
                    # le son de sélection est joué
                    pygame.mixer.Sound.play(RadioButton.select_sound)
                    # permutation de la visibilité entre les boutons
                    # concernés
                    self.change_visibility(self.priority, button)
                    # changement de la priorité
                    self.priority = button
                    return True
        return False

    def radio_change(self, event):
        """Un booléen est renvoyé, True dans le cas où la souris a été déplacé
        sur un autre bouton, lequel est alors mis en avant. Autrement la
        méthode renvoie False."""
        # dans le cas où la souris change de position
        if event.type == pygame.MOUSEMOTION:
            # changement de priorité si besoin
            return self.give_priority(event)
        return False

    def click_change(self, event):
        """détecte si un clic gauche a été effectué sur l'un des boutons.
        Si oui, la méthode renvoie True, dans le cas contraire, elle renvoie
        False."""
        # dans le cas où un évènement clic gauche avec la souris est détecté
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # change la priorité si lieu d'avoir changement
                return self.give_priority(event)
        return False


class Chronometer:
    """modélise un chronomètre.

    ATTRIBUTS DE CLASSE:
    les trois attributs suivant sont des attributs de la classe Sound de
    la librairie pygame.
    - `muhahaha` "Attention. Self destruct sequence activated. Self destruct
    sequence activated" ;
    - `pause_off` son lorsque le jeu est repris après une pause ;
    - `pause_on` son lorsque le jeu est mis en pause.

    ATTRIBUTS:
    - `duration` (int) généré par le module time, représente la durée à
    laquelle le chronomètre a été stoppé lors d'une pause, sans avoir mis
    en pause lors d'une partie, cette valeur est de type None
    - `time` (int) également généré par le module time avec une précision
    en nanoseconde."""

    muhahaha = pygame.mixer.Sound('sound/muhahaha.wav')
    pause_off = pygame.mixer.Sound('sound/pause_off.wav')
    pause_on = pygame.mixer.Sound('sound/pause_on.wav')

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
        """définit l'attribut duration pour sauvegarder la valeur du
        chronomètre au moment de l'appel à la méthode freeze, le
        son de mise en pause est joué."""
        # stocke la durée du chronomètre
        self.duration = self.time_elapsed()
        # le son de pause est joué
        pygame.mixer.Sound.play(Chronometer.pause_on)

    def unfreeze(self):
        """redéfinit l'attribut time afin que le chronomètre puisse
        afficher une valeur cohérente par rapport aux actions, le son de
        reprise après une game_pause est joué."""
        # définit une valeur cohérente au chronomètre après la pause
        self.time = time.time_ns() - self.duration
        # le son spécial a une chance sur deux d'être joué
        if random.random() < 0.5:
            # son "normal"
            pygame.mixer.Sound.play(Chronometer.pause_off)
        else:
            # son spécial
            pygame.mixer.Sound.play(Chronometer.muhahaha)
            # déai de 10 secondes :)
            time.sleep(10)

    def get_chrono_value(self):
        """renvoie les valeurs en durée du nombre d'heures (si besoin),
        de minutes, de secondes et de millisecondes de la partie avec un
        formatage des valeurs en chaîne de caractère"""
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
        """renvoie le booléen vrai si le temps indiqué sur le chronomètre
        correspond à la durée `duration` (float) en seconde comparée,
        autrement, il renvoie faux."""
        # l'égalité entre int et float n'est pas efficace
        return time.time_ns() - self.time > duration * 10 ** 9

    def reset(self):
        """reinitialise le chronomètre."""
        self.time = time.time_ns()


class Bag:
    """modélise un sac contenant l'ordre des tetrimino suivant
    le numéro correspondant à leur type.

    ATTRIBUTS:
    - `content` (list) de taille variable, elle contient des valeurs
    entières comprises entre 1 et 7."""

    def __init__(self):
        """méthode constructrice."""
        self.content = list(range(1, 8))
        random.shuffle(self.content)

    def __len__(self):
        """renvoie le nombre de tetrimino en attente."""
        return len(self.content)

    def next_tetrimino(self):
        """renvoie le prochain tetrimino et fait en sorte qu'il
        y ait toujours au moins 6 tetrimino en attente."""
        # si le nombre de tetrimino est inférieur à 7 strictement
        if len(self) < 7:
            # création d'une nouvelle suite de tetrimino de type
            # différent et à l'ordre aléatoire
            next_generation = list(range(1, 8))
            random.shuffle(next_generation)
            # placement de cette suite sur le début de la liste
            # self.content
            self.content = next_generation + self.content
        # dernière valeur remvoyée
        return self.content.pop()


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
        """méthode constructrice de la classe. Initialise le score
        et les données d'une parties. `window`, `matrix` et `chronometer` sont
        des instances de classes du même nom, `game_type` est un 2-uplet
        contenant dans l'ordre, le niveau et la difficulté imposée au mode B.
        le niveau peut-être compris entre 0 et 10 inclus. La difficulté quant à
        elle est comprise entre -1 et 5 inclus, -1 signifiant qu'il s'agit du
        mode A (le mode B permettant de choisir pour niveau max 5)."""
        level, hight = game_type
        # goal correspond à l'objectif à atteindre avant le passage au niveau
        # suivant. 25 dans le cas du mode B, autrement 5 fois le niveau choisi
        goal = 25 if hight != -1 else level * 5
        first_values = [0, 0, level, goal]
        self.values = {DATA_KEYS[i]: first_values[i] for i in range(4)}
        self.values['game_mode'] = 'B' if hight != -1 else 'A'
        self.values_surface = {DATA_STRINGS[i]:
                               {'surface': None,
                                'position': None} for i in range(5)}
        self.font = None
        self.surface = None
        self.resize(window, matrix)
        self.chrono_value(chronometer)
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
        """définit les positions des surfaces de valeurs."""
        w_value, h_value = self.rect.w, self.rect.h
        # attribution d'une marge locale
        local_margin = h_value // 11
        # liste pour le nombre "zero à compléter" aux valeurs
        nb_zero_to_fill = [10, 3, 2, 3]
        # parcours des éléments de valeurs
        for i, element in enumerate(DATA_KEYS):
            value = str(self.values[element]).zfill(nb_zero_to_fill[i])
            value_rendered = self.font.render(value, 1, COLOR['WHITE'])
            self.values_surface[element]['surface'] = value_rendered
        # stocke les positions, le temps et le score sont centrés
        # le reste sont alignés à gauche dans l'encadré de data
        pos_x = []
        temp_chrono = Chronometer()
        self.chrono_value(temp_chrono)
        # position centrés
        for element in DATA_STRINGS[:2]:
            obj_w_value = self.values_surface[element]['surface'].get_size()[0]
            pos_x.append(find_align_center_x(obj_w_value, w_value))
        # alignement à gauche
        for element in DATA_STRINGS[2:]:
            obj_w_value = self.values_surface[element]['surface'].get_size()[0]
            pos_x.append(w_value - local_margin - obj_w_value)
        # mise à jour des informations sur les positions dans l'attribut
        # values_surface
        for i, element in enumerate(DATA_STRINGS):
            position = (pos_x[i], self.values_surface[element]['position'])
            self.values_surface[element]['position'] = position

    def set_fall_speed(self):
        """met à jour la valeur du temps entre chaque frame du jeu en accord
        avec la guideline officiel du jeu."""
        level = self.values['level']
        self.fall_speed = (0.8 - (level - 1) * 0.007) ** (level - 1)

    def resize(self, window, matrix):
        """change les attributs relatifs aux dimensions de l'encadré. `window`
        et `matrix` sont des dictionnaires contenant les informations relatifs
        aux dimensions de ces deux objets."""
        # informations générales de l'emplacement de l'encadré
        remaining_space = matrix['rect'].x - window['margin']
        w_value = round(matrix['cell_size'] * 7.4)
        x_axis = (remaining_space - w_value) * 0.72
        y_axis = matrix['rect'].y + w_value
        h_value = matrix['cell_size'] * 21 - y_axis + window['margin']
        self.width = round(matrix['cell_size'] * 3.7) // 39 + 1
        self.rect = pygame.Rect(x_axis, y_axis, w_value, h_value)
        # redimensionnement des textes et repositionnement
        self.font_resize()
        self.values_relative_position()

    def chrono_value(self, chronometer):
        """la valeur du chronomètre est donnée selon celle de `chronometer`
        une instance de la classe Chronometer."""
        # la valeur du chronomètre est stockée dans `chrono_value` avec
        # un formatage en chaîne de caractère
        chrono_value = chronometer.get_chrono_value()
        # mise à jour de la surface du chronomètre
        chrono_surface = self.font.render(chrono_value, 1, COLOR['WHITE'])
        self.values_surface['time']['surface'] = chrono_surface

    def update(self, chronometer, surface):
        """met à jour les attributs de l'instance concernant la surface
        pour la valeur du chronomètre de jeu et les autres données du jeu.
        `chronometer` est une instance de la classe Chronometer et `surface`
        est un objet pygame.Surface."""
        # mise à jour du chronomètre
        self.chrono_value(chronometer)
        # pour chacun des données contenu par l'instance sur le jeu
        for element in DATA_STRINGS:
            # affichage sur `surface`
            surface.blit(self.values_surface[element]['surface'],
                         self.values_surface[element]['position'])

    def add_to_line_clear(self, value_to_add):
        """ajoute `value_to_add` au nombre de line_clear. Renvoie un booléen
        `game_win` qui vaut True si le jeu est gagné en mode B, autrement,
        elle renvoie False."""
        game_win = False
        # la donnée stockant le nombre de line_clear est incrémentée de
        # `value_to_add`
        self.values['lines'] += value_to_add
        # mise à jour de la surface représentant le nombre de line clear
        lines = self.font.render(str(self.values['lines']).zfill(3), 1,
                                 COLOR['WHITE'])
        self.values_surface['lines']['surface'] = lines
        # l'objectif est décrémenté de `value_to_add`
        self.values['goal'] -= value_to_add
        # dans le cas où cet objectf est atteint
        if self.values['goal'] < 1:
            # au mode A
            if self.values['game_mode'] == 'A':
                # le niveau est augmenté de 1
                self.values['level'] += 1
                # changement de la vitesse de chute des tetrimino
                self.set_fall_speed()
                # un nouvel objectif est défini selon le niveau atteint
                self.values['goal'] = self.values['level'] * 5
                # mise à jour de la surface représentant le niveau
                level = self.font.render(str(self.values['level']).zfill(2), 1,
                                         COLOR['WHITE'])
                self.values_surface['level']['surface'] = level
            # au mode B
            else:
                # il s'agit d'une victoire, la partie est gagnée
                game_win = True
        # mise à jour de la surface représentant l'objectif
        goal = self.font.render(str(self.values['goal']).zfill(3), 1,
                                COLOR['WHITE'])
        self.values_surface['goal']['surface'] = goal
        return game_win

    def score_increase(self, value_to_add):
        """augmente l'attribut score de `value_to_add` devant
        être un entier."""
        # mise à jour du score
        self.values['score'] += value_to_add
        # mise à jour de la surface représentant le score
        score = self.font.render(str(self.values['score']).zfill(10), 1,
                                 COLOR['WHITE'])
        self.values_surface['score']['surface'] = score

    def get_size(self):
        """renvoie les dimensions de l'encadré de l'instance."""
        return (self.rect.w, self.rect.h)

    def get_position(self):
        """renvoie la position de l'encadré de l'instance."""
        return (self.rect.x, self.rect.y)
