import random


COLOR = {'RED' : (237, 41, 57),
         'ORANGE' : (255, 121, 0),
         'YELLOW' : (254, 203, 0),
         'GREEN' : (105, 190, 40),
         'CYAN' : (0, 159, 218),
         'BLUE' : (0, 101, 189),
         'PURPLE' : (149, 45, 152)}
TETRIMINO_NAME = {0 : 'O',
             1 : 'I',
             2 : 'T',
             3 : 'L',
             4 : 'J',
             5 : 'S',
             6 : 'Z'}
TETRIMINO_SHAPE = {0 : [[1, 1],
                        [1, 1]],
                   1 : [[0, 0, 0, 0],
                        [1, 1, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]],
                   2 : [[0, 1, 0],
                        [1, 1, 1],
                        [0, 0, 0]],
                   3 : [[0, 0, 1],
                        [1, 1, 1],
                        [0, 0, 0]],
                   4 : [[1, 0, 0],
                        [1, 1, 1],
                        [0, 0, 0]],
                   5 : [[0, 1, 1],
                        [1, 1, 0],
                        [0, 0, 0]],
                   6 : [[1, 1, 0],
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

    ROTATION_PHASIS = {}
    for i in range(7):
        ROTATION_PHASIS[i] = {}
        for phasis in range(4):
            ROTATION_PHASIS[i][phasis] = turn_right(TETRIMINO_SHAPE[i], phasis)

    def __init__(self):
        self.phasis = 0
        self.state = 0
        self.type = bag.next_tetrimino()
        self.x = 0 # dans skyline
        self.y = start_center(self.type)
        Tetrimino.count += 1
        
    # temporaire, pour la visualisation du tetrimino, à enlever à la fin
    def __str__(self):
        stock = ''
        for e in Tetrimino.ROTATION_PHASIS[self.type][self.phasis]:
            stock += ' '.join(str(e))
            stock += '\n'
        stock += f'\n{TETRIMINO_SHAPE[self.type]}'
        return stock

    # setters
    def turn_right(self):
        self.phasis = (self.phasis + 1) % 4

    def turn_left(self):
        self.phasis = (self.phasis - 1) % 4

    # getters
    def get_count(self):
        return Tetrimino.count

    def get_phasis(self):
        return self.phasis

    def get_state(self):
        return self.state
    
    def get_type(self):
        return self.type



class Mathrix:

    content = [[0 for j in range(10)] for i in range(22)] # deux colonnes pour skyline
    
    def __str__(self):
        stock = ''
        for e in Mathrix.content:
            stock += ' '.join(str(e))
            stock += '\n'
        return stock
    

# je ne sais pas si c'est pertinent ou pas, mais je le laisse pour le moment
class Statistic:

    def stat_view(self):
        nb_tetrimino = Tetrimino.get_count(Tetrimino)
    
    

# penser à initialiser bag et mathrix dans le main
# ce sont des tests comme tu peux le voir, les tetrimino peuvent tourner à gauche et à droite, c'est plutôt pas mal :)
bag = Bag()
mathrix = Mathrix()
print(mathrix)
print(bag.get_content())
tetrimino = Tetrimino()
for i in range(4):
    tetrimino.turn_right()
    print('\n\n')
    print(tetrimino)
print(tetrimino.get_count())
