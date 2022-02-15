import pygame
import sys
try:
    from constant import COLOR, FONT_HEIGHT
except ModuleNotFoundError:
    from modules.constant import COLOR, FONT_HEIGHT


def get_font_size(font_height):
    """récupère une valeur de taille de police selon `font_height` un entier
    naturel représentant la hauteur de font voulu en nombre de pixel sur la
    fenêtre de jeu."""
    if font_height < 19:
        return 12
    else:
        i = 0
        while font_height > FONT_HEIGHT[i]:
            i += 1
        return i + 12


def loop_starter_pack(tetris_window, event):
    """permet dans une boucle de jeu avec les évènements pygame de quitter
    le jeu lorsque le joueur appuie sur la croix en haut à droite.
    Permet également de limiter les redimensionnement de la fenêtre en
    instaurant une hauteur, largeur et ratio minimal admis."""
    # appui sur la croix de la fenêtre
    if event.type == pygame.QUIT:
        # fermeture de la fenêtre
        pygame.quit()
        sys.exit()
    # dans le cas où l'utilisateur change la taille de la fenêtre
    if event.type == pygame.VIDEORESIZE:
        width, height = event.size
        if width < 545:
            width = 545
        if width / height < 1.1:
            width = round(1.8 * height)
        if height < 303:
            height = 303
        window_size = (width, height)
        tetris_window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    return tetris_window


class Button2:
    """crée un bouton visuel formaté avec le style général du jeu."""

    def __init__(self, window, relative_position, image):
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
        self.image = image
        window_w, window_h = window.get_size()
        x_value = round(relative_position[0] * window_w)
        y_value = round(relative_position[1] * window_h)
        w_value = h_value = round(relative_position[2] * window_w)
        self.rect = pygame.Rect(x_value, y_value, w_value, h_value)

    def draw(self, surface):
        """permet de dessiner le bouton sur une surface `surface` devant
        être un objet pygame.Surface"""
        # ##voir pour transparence
        button_surface = pygame.Surface((self.rect.w, self.rect.h))
        image = pygame.transform.scale(self.image,
                                       (self.rect.w, self.rect.h))
        button_surface.blit(image, (0, 0))
        surface.blit(button_surface, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, (150, 150, 150), self.rect, 3)

    def is_pressed(self, event):
        """permet de détecter si le joueur a fait un clic gauche
        sur le bouton. Renvoie un booléen, True si le bouton est cliqué,
        False sinon."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False


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


class Text:
    """modélise un texte visuel formaté avec le style général du jeu."""

    def __init__(self, window, relative_position, text):
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
            lorsque `y` vaut 1 auquel cas ne sera pas visible puisque le
            rectangle associé au texte sortira du cadre de la fenêtre)) ;
            - valeur `w`, représente la largeur du texte selon la largeur de
            la fenêtre (pour `w` égal à 0, le texte est apparent, seulement, son
            emplacement sur l'axe des abscisse est peu certaine, ce qui est peu
            recommendable pour contrôler la disposition des objets pour la partie
            graphique. Lorsque `w` vaut 1, le texte possède une largeur dépendant
            fortement de la longueur du texte) ;
            - valeur `h`, représente la longueur du texte selon la proportion par
            rapport à la longueur de la fenêtre. Cette valeur est approximative et
            fait appel à une fonction permettant de trouver la taille de la police
            sient le mieux l'exigence (pour `h` égal à 0, le texte est égal à 12,
            ce qui et peu intéressant vu que cela rend impossible un
            redimensionnement s'adaptant à la taille de la fenêtre vu que fixe.
            Lorsque `h` vaut 1, le texte possède une longueur égale approche celle
            de la fenêtre ou soulèvera une erreur si la résolution de l'écran est
            supérieur à la marge laissé au préalable).
        - `text` est le texte à afficher, doit être une chaîne de caractères ;
        >>> text = Text((0.3, 0.4, 0.4, 0.2), "Hello world !")"""
        window_w, window_h = window.get_size()
        x_value = round(relative_position[0] * window_w)
        y_value = round(relative_position[1] * window_h)
        w_value = round(relative_position[2] * window_w)
        font_size = get_font_size(round(relative_position[3] * window_h))
        font = pygame.font.SysFont("./others/Anton-Regular.ttf", font_size)
        self.text_image = font.render(text, 1 , COLOR['WHITE'])
        self.rect = pygame.Rect(x_value, y_value, w_value, font_size)

    def draw(self, surface):
        """permet de dessiner le bouton sur une surface `surface` devant
        être un objet pygame.Surface"""
        center_pos = self.text_image.get_rect(center = self.rect.center)
        surface.blit(self.text_image, center_pos)
