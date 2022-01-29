import pygame
import json

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
    def __init__(self, x, y, width, heigh, text, size, font, color):
        """
        Exemple :
        Button(100, 100, 50, 50, "Test", 20, "arial", (255, 255, 255))
        """
        self.x = x
        self.y = y
        self.width = width
        self.heigh = heigh
        self.text = text
        self.size = size
        self.font = pygame.font.SysFont(
            font,
            self.textSize,
            bold = True
        )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.heigh)
        self.text_image = self.font.render(self.text, 1 , color)

    def draw(self, screen):
        """
        Permet de dessiner le bouton
        """
        pygame.draw.rect(screen, (255, 255, 255, 3), self.rect)
        screen.blit(self.text_image, (self.width/2, self.heigh/2))

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

def clear_lines(tableau):
    """
    Permet de supprimer les lignes d'un tableau quand la ligne ne contient que
    des 1, et de les décaler vers le bas et de garder le nombre de lignes
    supprimé

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
    n = 0
    copy_tableau = tableau.copy()
    for i in range(len(tableau)):
        if copy_tableau[i].count(0) == 0:
            copy_tableau.pop(i)
            copy_tableau.insert(0, [0] * len(tableau[0]))
            n += 1
    return copy_tableau, n
