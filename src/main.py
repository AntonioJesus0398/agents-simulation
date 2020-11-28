import random

class Logger:
    def __init__(self, name):
        self.name = name
        f = open(name, 'w')
        f.close()

    def write(self, s):
        with open(self.name, "a") as f:
            f.write(s)

logger = Logger('logging.txt')

class Element:
    def __init__(self):
        self.content = []

    @property
    def empty(self):
        return self.content == []

    def __repr__(self):
        if self.empty:
            return 'E'
        result = ''
        for item in self.content:
            result += str(item)
        return result

class PlayPen:
    def __repr__(self):
        return 'P'

class Obstacle:
    def __repr__(self):
        return 'O'

class Kid:
    def __repr__(self):
        return 'K'

class Dirt:
    def __repr__(self):
        return 'D'

class Robot:
    def __repr__(self):
        return 'R'

def _percent_to_number(percent, total):
    return int(percent * total / 100)

def _number_to_percent(number, total):
    return (number / total * 100)

class Enviroment:
    def __init__(self, N, M, dirty_percent, obstacle_percent, no_kids):
        self.rows = N
        self.columns = M
        self.total_cells = N * M
        self.board = [[Element() for _ in range(M)] for _ in range(N)]

        # place the playpens from top to bottom and left to right
        n = no_kids
        for i in range(N):
            if n == 0:
                break
            for j in range(M):
                if n == 0:
                    break
                self.board[i][j].content.append(PlayPen())
                n -= 1

        empty_positions = [(i, j) for i in range(N) for j in range(M) if self.board[i][j].empty]
        logger.write(str(empty_positions))
        random.shuffle(empty_positions)

        def place_randomly(entity, number):
            for _ in range(number):
                x, y = empty_positions.pop(0)
                self.board[x][y] = entity()

        self.no_dirty_cells = _percent_to_number(dirty_percent, self.total_cells)
        place_randomly(Dirt, self.no_dirty_cells)
        place_randomly(Robot, 1)
        place_randomly(Obstacle, _percent_to_number(obstacle_percent, self.total_cells))
        place_randomly(Kid, no_kids)


    def __repr__(self):
        result = ''
        for i in range(self.rows):
            for j in range(self.columns):
                content = str(self.board[i][j])
                assert len(content) >= 1 and len(content) <=3
                result += content + ' ' * (4 - len(content))
            result += '\n'
        return result

    # @property
    # def dirt_cells_percent(self):
    #     return _number_to_percent(self.no_dirty_cells, self.total_cells)
