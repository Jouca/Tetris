"""module codé par Diego (@Jouca) TG8, contenant diverses classes et
fonctions utiles au bon fonctionnement du jeu Tetris."""


import json
import pygame
try:
    from constant import COLOR
    from useful import get_font_size
except ModuleNotFoundError:
    from modules.constant import COLOR
    from modules.useful import get_font_size


class GameStrings:
    def __init__(self, language="FR"):
        with open(f"./others/game_string/{language}/game_strings.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
    
    def get_string(self, key):
        return self.data[key]

    def get_all_strings(self):
        return self.data


class Spritesheet:
    """classe s'occupant d'un fichier type spritesheet."""

    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data, encoding="utf-8") as fichier:
            self.data = json.load(fichier)
        fichier.close()

    def get_sprite(self, x_position, y_position, width, heigth):
        """
        Permet d'avoir le sprite avec sa position x, sa position y,
        sa taille et sa hauteur.
        """
        sprite = pygame.Surface((width, heigth))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(
            self.sprite_sheet,
            (0, 0),
            (x_position, y_position, width, heigth)
        )
        return sprite

    def parse_sprite(self, name):
        """
        Permet de dessiner le sprite.
        """
        sprite = self.data['frames'][name]['frame']
        x_position, y_position = sprite["x"], sprite["y"]
        w_position, h_position = sprite["w"], sprite["h"]
        image = self.get_sprite(
            x_position,
            y_position,
            w_position,
            h_position
        )
        return image


class Button:
    """crée un bouton visuel formaté avec le style général du jeu."""

    def __init__(self, window, relative_position, text, font_size=0):
        """méthode constructeur de la classe :
        - `window` est la fenêtre sur laquelle est créé le bouton ;
        - `relative_position` correspond à un 4-uple (`x`, `y`, `w`, `h`)
        indiquant la position et les dimensions relatives selon les dimensions
        de la fenêtre, toutes les valeurs doivent être comprises entre 0 et 1
        exclus afin que le bouton soit visible, dans l'ordre :
            - position relative `x`, positionnement x par rapport à la largeur
            de la fenêtre (sur bord gauche lorsque `x` vaut 0, droit lorsque
            `x` vaut 1 (sort du cadre)) ;
            - position relative `y`, positionnement y par rapport à la longueur
            de la fenêtre (sur le bord haut lorsque `y` vaut 0, sur le bord bas
            lorsque `y` vaut 1 auquel cas ne sera pas visible puisque le bouton
            sortira du cadre de la fenêtre)) ;
            - valeur `w`, représente la largeur du bouton selon la largeur de
            la fenêtre (pour `w` égal à 0, le bouton est inexistant ce qui
            n'est pas très intéressant, lorsque `w` vaut 1, le bouton possède
            une largeur égale à celle de la fenêtre) ;
            - valeur `h`, représente la longueur du bouton selon la longueur
            de la fenêtre (pour `h` égal à 0, le bouton est inexistant ce qui
            n'est pas très intéressant, lorsque `w` vaut 1, le bouton possède
            une longueur égale à celle de la fenêtre)
        - `text` est le texte associé au bouton, doit être une chaîne de
        caractères ;
        - font_size, un entier spécifiant la taille de la police pour le texte
        à afficher sur le bouton visuel, dans le cas où elle n'est pas
        indiqué, la taille dépendra de la hauteur du bouton.
        >>> button = Button((0, 0, 1, 1), "Hello world !", 50)"""
        self.text = text
        window_w, window_h = window.get_size()
        x_value = round(relative_position[0] * window_w)
        y_value = round(relative_position[1] * window_h)
        w_value = round(relative_position[2] * window_w)
        h_value = round(relative_position[3] * window_h)
        self.rect = pygame.Rect(x_value, y_value, w_value, h_value)
        # si la taille de la font n'est pas définie
        if not font_size:
            font_size = get_font_size(round(self.rect.h * 0.6))
        font = pygame.font.SysFont("./others/Anton-Regular.ttf", font_size)
        self.text_image = font.render(self.text, 1, COLOR['WHITE'])

    def draw(self, surface):
        """permet de dessiner le bouton sur une surface `surface` devant
        être un objet pygame.Surface"""
        # ##voir pour transparence
        button_surface = pygame.Surface((self.rect.w, self.rect.h))
        button_surface.set_alpha(175)
        surface.blit(button_surface, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, (150, 150, 150), self.rect, 4)
        center_pos = self.text_image.get_rect(center=self.rect.center)
        surface.blit(self.text_image, center_pos)

    def is_pressed(self, event):
        """permet de détecter si le joueur a fait un clic gauche
        sur le bouton. Renvoie un booléen, True si le bouton est cliqué,
        False sinon."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False


def clear_lines(content):
    """supprime les lignes remplies (valeur autre que 0) d'un
    tableau `content`, les décale vers le bas, le tableau `content`
    conserve le format initial, même nombre de lignes et de colonnes.
    La fonction renvoie ce nouveau tableau ainsi que le nombre de
    lignes supprimées.
    >>> content = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    >>> clear_lines(content)
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
     3"""
    nb_line_clear = 0
    copy_content = content.copy()
    for i in range(len(content)):
        if copy_content[i].count(0) == 0:
            copy_content.pop(i)
            copy_content.insert(0, [0] * len(content[0]))
            nb_line_clear += 1
    return copy_content, nb_line_clear
