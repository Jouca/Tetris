"""module codé par Solène (@periergeia) TG8, contenant diverses classes et
fonctions utiles au bon fonctionnement du jeu Tetris."""


# importation de librairies python
import random
import colorsys
import time
import pygame
import pygame.freetype
try:
    from constant import LANG, COLOR, DATA_KEYS
    from constant import DATA_STRINGS, VISUAL_STRUCTURE
    from diego import GameStrings
    from useful import get_font_size, Button1
except ModuleNotFoundError:
    from modules.constant import LANG, COLOR, DATA_KEYS
    from modules.constant import DATA_STRINGS, VISUAL_STRUCTURE
    from modules.diego import GameStrings
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
