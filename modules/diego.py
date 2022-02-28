"""module codé par Diego (@Jouca) TG5, contenant diverses classes et
fonctions utiles au bon fonctionnement du jeu Tetris."""


import json
import pygame
import requests
import json
try:
    from constant import LANG
except ModuleNotFoundError:
    from modules.constant import LANG


class GameStrings:
    def __init__(self, language="FR"):
        with open(f"./others/game_string/{language}/game_strings.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
    
    def get_string(self, key):
        return self.data[key]

    def get_all_strings(self):
        return self.data


game_strings = GameStrings(LANG)


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


def post_request(url, data=None, headers=None):
    """
    Permet d'envoyer une requête POST à l'url `url` avec les données
    `data`.
    """
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        return response.text, response.status_code
    except requests.exceptions.ConnectionError as e:
        return game_strings.get_string("error"), 0


def read_json(filename):
    """
    Permet de lire un fichier json.
    """
    with open(filename, encoding="utf-8") as fichier:
        data = json.load(fichier)
    fichier.close()
    return dict(data)


def insert_local_score(score):
    """
    Permet d'insérer un score dans le fichier `data.json`.
    """
    data = read_json("./others/game_save/data.json")
    for i in data:
        if score >= int(data[i]):
            data[i] = str(score).zfill(8)
            break
    with open("./others/game_save/data.json", "w", encoding="utf-8") as fichier:
        json.dump(data, fichier, indent=4)
    fichier.close()
