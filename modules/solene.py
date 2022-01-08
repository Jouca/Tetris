import random
import pygame


COLOR = {'RED' : (237, 41, 57),
         'ORANGE' : (255, 121, 0),
         'YELLOW' : (254, 203, 0),
         'GREEN' : (105, 190, 40),
         'CYAN' : (0, 159, 218),
         'BLUE' : (0, 101, 189),
         'PURPLE' : (149, 45, 152)}

# à compléter en prévision pour plus tard
TETRIMINO_DATA = {1 : {'name' : 'O', 'color' : '', 'monochrome' : ''},
                  2 : 'I',
                  3 : 'T',
                  4 : 'L',
                  5 : 'J',
                  6 : 'S',
                  7 : 'Z'}

TETRIMINO_SHAPE = {1 : [[1, 1],
                        [1, 1]],
                   2 : [[0, 0, 0, 0],
                        [1, 1, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]],
                   3 : [[0, 1, 0],
                        [1, 1, 1],
                        [0, 0, 0]],
                   4 : [[0, 0, 1],
                        [1, 1, 1],
                        [0, 0, 0]],
                   5 : [[1, 0, 0],
                        [1, 1, 1],
                        [0, 0, 0]],
                   6 : [[0, 1, 1],
                        [1, 1, 0],
                        [0, 0, 0]],
                   7 : [[1, 1, 0],
                        [0, 1, 1],
                        [0, 0, 0]]}

# l'utilité est moyen, serviable plus tard pour les statistiques eventuellement
ROTATION_PHASIS_NAME = {0 : 'N',
                        1 : 'E',
                        2 : 'S',
                        3 : 'W'}

# pour se réprer, le dico n'a aucune utilité en soi
TETRIMINO_STATE = {0 : 'falling',
                   1 : 'lock_down'}


SIDE = [(0, -1), # haut
        (1, 0), # droite
        (0, 1), # gauche
        (-1, 0)] # gauche



def turn_right(tetrimino, phasis):
    if phasis == 0:
        return tetrimino
    else:
        phasis -= 1    
        rotated_tetrimino = []
        for i in range(len(tetrimino)):
            tetrimino_line = []
            for j in range(len(tetrimino)-1, -1, -1):
                tetrimino_line.append(tetrimino[j][i])
            rotated_tetrimino.append(tetrimino_line)
    return turn_right(rotated_tetrimino, phasis)




class Bag:
    
    content = list(range(7))
    random.shuffle(content)

    def __len__(self):
        return len(Bag.content)

    def __getitem__(self, key):
        # voir à enlever try/except vu que ce ne sera jamais raised ?
        try:
            return Bag.content[key]
        except IndexError:
            return IndexError

    def get_content(self):
        return Bag.content

    def next_tetrimino(self):
        if len(self) < 4 :
            next_generation = list(range(7))
            random.shuffle(next_generation)
            Bag.content += next_generation
        return Bag.content.pop()
            


# pas très optimal mais au moins ça permet de bien comprendre
def start_center(tetrimino_type):
    return (10 - len(TETRIMINO_SHAPE[tetrimino_type])) // 2


class Tetrimino:
    
    count = 0
    
    # création d'un dictionnaire contenant toutes les rotations
    ROTATION_PHASIS = {}
    for i in range(1, 8):
        ROTATION_PHASIS[i] = {}
        for phasis in range(4):
            ROTATION_PHASIS[i][phasis] = turn_right(TETRIMINO_SHAPE[i],
                                                    phasis)

    def __init__(self, Bag):
        self.phasis = 0
        self.current_state = 0
        self.type = Bag.next_tetrimino()+1
        print(f"Tetrimino {self.type}" )
        self.x = start_center(self.type)
        print(self)
        self.y = 0  # dans skyline
        Tetrimino.count += 1
        
    # temporaire, pour la visualisation du tetrimino, à enlever à la fin
    def __str__(self):
        stock = ''
        for e in Tetrimino.ROTATION_PHASIS[self.type][self.phasis]:
            stock += ' '.join(str(e))
            stock += '\n'
        stock += f'\n type du tetrimino : {TETRIMINO_SHAPE[self.type]}'
        return stock

    # optimisation possible mais ça rendra la compréhension du code difficile
    # vu que le tout est assez astucieux déjà
    def list_test_around(self):
        """renvoie une liste de trois listes, par indice:
        - 0 pour les test en bas
        - 1 pour les test à gauche
        - 2 pour les test à droite
        """
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[self.type][self.phasis]
        test_list = [[] for i in range(3)]
        
        square_len = len(tetrimino_shape)
        last_row = last_column =  square_len - 1
        first_column = 0

        # du moment que la liste de test correspondant est vide
        while not test_list[0]:
            for i in range(square_len):
                # ajouter le couple d'indice s'il n'est pas égal à 0
                if tetrimino_shape[last_row][i]:
                    test_list[0].append((last_row, i))
            last_row -= 1

        while not test_list[1]:
            for i in range(square_len):
                if tetrimino_shape[i][first_column]:
                    test_list[1].append((i, first_column))
            first_column += 1
        
        while not test_list[2]:
            for i in range(square_len):
                if tetrimino_shape[i][last_column]:
                    test_list[2].append((i, last_column))
            last_column -= 1

        return test_list

    # si 2 --> test pour voir si line clear ou autre, puis passage au
    # tetrimino suivant version non finie, il reste à déterminer les cas
    # où le tetrimino sort de la matrice !
    def state(self, Matrix):
        """renvoie:
        - 0 si le tetrimino est en 'falling phase', c'est-à-dire que le
        tetrimino continue à tomber
        - 1 si le tetrimino est en 'lock phase', phase où le tetrimino
        s'apprête à se figer dans la matrice avec un temps escompté
        - 2 lorsque le tetrimino est en 'completion phase'"""
        test_list = self.list_test_around()
        
        for element in test_list[0]:
            print(element)
            if not Matrix.content[self.x + element[0]][self.y + element[1]]:
                return 1

        """try:
                if Matrix.content[self.x + i][self.y + j] != 0:
                    return 1
            except:
                super_rotation_system()"""
        return 0

    def super_rotation_system():
        pass

    # je ne pense pas qu'il y ait besoin de compléter plus si on fait bien les
    # test avant de permettre au tetrimino de tomber
    def fall(self):
        self.y += 1

    # setters
    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def turn_left(self):
        self.phasis = (self.phasis - 1) % 4

    def turn_right(self):
        self.phasis = (self.phasis + 1) % 4

    # getters
    def get_count(self):
        return Tetrimino.count

    def get_phasis(self):
        return self.phasis

    def get_state(self):
        return self.current_state
    
    def get_type(self):
        return self.type



class Window:
    def __init__(self, window_size):
        self.width = window_size[0]
        self.height = window_size[1]
        self.size = window_size
        self.margin = round(0.05 * self.height)
    
    def change_size(self, new_size):
        self.width = new_size[0]
        self.height = new_size[1]
        self.size = new_size
        self.update_margin()

    def update_margin(self):
        self.margin = round(0.05 * self.height)




class Verification:

    def line_clear(Matrix):
        """"""

        pass

class Matrix:

    def __init__(self, Window):
        self.resize(Window)
        self.content = [[0 for j in range(10)] for i in range(22)] # deux colonnes pour skyline
        self.highter_row = 22

    def __str__(self):
        stock = ''
        for i in range(1, 22):
            stock += ' '.join(str(self.content[i]))
            stock += '\n'
        return stock

    def __add__(self, Tetrimino:Tetrimino):
        tetrimino_shape = Tetrimino.ROTATION_PHASIS[Tetrimino.type][Tetrimino.phasis]
        """print(Tetrimino)
        print(Tetrimino.x)
        print(Tetrimino.y)"""
        for i in range(len(tetrimino_shape)):
            for j in range(len(tetrimino_shape)):
                if tetrimino_shape[j][i] == 1:
                    self.content[Tetrimino.y + j][Tetrimino.x + i] = Tetrimino.type
                    if Tetrimino.y + j < self.highter_row:
                        self.highter_row = Tetrimino.y + j
                        print(self.highter_row)

    def resize(self, Window:Window):
        # pourrait être enlevé, mais mieux pour compréhension étapes
        remaining_height_spaces = Window.height - 2 * Window.margin
        self.cell_size = remaining_height_spaces // 21
        self.x = (Window.width - self.cell_size * 10) // 2
        self.y = (Window.height - self.cell_size * 21) // 2
        self.w = self.cell_size * 10
        self.h = self.cell_size * 21

    def display(self, surface):
        pygame.draw.rect(surface,(250,0,0),pygame.Rect(self.x, self.y, self.w, self.h))



class Hold_queue:

    def __init__(self, Window, Matrix):
        self.resize(Window, Matrix)

    def resize(self, Window:Window, Matrix:Matrix):
        remaining_space = Window.width - (Matrix.x + Matrix.w) - Window.margin
        self.w = self.h = round(Matrix.cell_size * 3.7)
        self.x = (remaining_space - self.w) * 0.7 + Window.margin
        self.y = Matrix.y

    def display(self, surface):
        pygame.draw.rect(surface,(250,0,0),pygame.Rect(self.x, self.y, self.w, self.h))


class Next_queue:

    def __init__(self, Window, Matrix):
        self.resize(Window, Matrix)

    def resize(self, Window:Window, Matrix:Matrix):
        matrix_place = Matrix.x + Matrix.w
        remaining_space = Window.width - matrix_place - Window.margin
        self.w = round(Matrix.cell_size * 3.7)
        self.x = (round((remaining_space - self.w) * 0.3)) + matrix_place
        self.y1 = Matrix.y
        self.y2 = round(self.y1 + self.w + (Matrix.h / 10))
        self.h1 = self.w
        self.h2 = round(Matrix.h*0.9) - self.w
        self.next = pygame.Rect(self.x + (self.w - Matrix.cell_size * 3) // 2,
                                self.y1 + (self.w - Matrix.cell_size * 2) // 2,
                                Matrix.cell_size * 3,
                                Matrix.cell_size * 2)

    def display(self, surface):
        pygame.draw.rect(surface,(250,0,0),pygame.Rect(self.x, self.y1, self.w, self.h1))
        pygame.draw.rect(surface,(250,0,0),pygame.Rect(self.x, self.y2, self.w, self.h2))
        pygame.draw.rect(surface,(0,0,250),self.next)
        space = (self.h2 - 5 *  self.next.height) // 6
        y = self.y2 + space
        for i in range(5):
            tetrimino_place = pygame.Rect(self.next.x, y, self.next.width, self.next.height)
            y += self.next.height + space
            pygame.draw.rect(surface, (0, 0, 250), tetrimino_place)


    

# je ne sais pas si c'est pertinent ou pas, mais je le laisse pour le moment
class Statistic:

    def stat_view(self):
        nb_tetrimino = Tetrimino.get_count(Tetrimino)
    
