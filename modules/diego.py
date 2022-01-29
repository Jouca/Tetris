"""module codé par Diego (@Jouca) TG8, contenant diverses classes et
fonctions utiles au bon fonctionnement du jeu Tetris."""

import json
import pygame

class Spritesheet:
    """
    Objet s'occupant d'un fichier type spritesheet.
    """
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
        image = self.get_sprite(x_position, y_position, w_position, h_position)
        return image

class Button:
    def __init__(self, rect, text, size, color):
        """
        Exemple :
        Button((200, 200, 100, 100), "Test", 60, (255, 255, 255))
        """
        self.text = text
        self.size = size
        self.font = pygame.font.SysFont(
            "./others/Anton-Regular.ttf",
            self.size,
            bold = True
        )
        self.rect = pygame.Rect(rect)
        self.text_image = self.font.render(self.text, 1 , color)

    def draw(self, screen):
        """
        Permet de dessiner le bouton
        """
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)
        screen.blit(self.text_image, (self.text_image.get_rect(center = self.rect.center)))

    def event_handler(self, event):
        """
        Permet de détecter si le joueur a fait un clique gauche
        sur le bouton.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False

def clear_lines(content):
    """
    Permet de supprimer les lignes d'un tableau `content` quand la ligne
    ne contient une ligne remplies (valeur autre que 0), et de les décaler
    vers le bas et de garder le nombre de lignes supprimées

    >>> clear_lines([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ] 3
    """
    nb_line_clear = 0
    copy_content = content.copy()
    for i in range(len(content)):
        if copy_content[i].count(0) == 0:
            copy_content.pop(i)
            copy_content.insert(0, [0] * len(content[0]))
            nb_line_clear += 1
    return copy_content, nb_line_clear
