import random

class Logger:
    def __init__(self, name):
        self.name = name
        f = open(name, 'w')
        f.close()

    def write(self, s):
        with open(self.name, "a") as f:
            f.write(str(s))

logger = Logger('logging.txt')


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
        self.board = [['E' for _ in range(M)] for _ in range(N)]

        # place the playpens from top to bottom and left to right
        n = no_kids
        for i in range(N):
            if n == 0:
                break
            for j in range(M):
                if n == 0:
                    break
                self.board[i][j] = 'P'
                n -= 1

        empty_positions = [(i, j) for i in range(N) for j in range(M) if self.board[i][j] == 'E']
        random.shuffle(empty_positions)

        def place_randomly(entity, number):
            for _ in range(number):
                x, y = empty_positions.pop(0)
                self.board[x][y] = entity

        self.no_dirty_cells = _percent_to_number(dirty_percent, self.total_cells)
        place_randomly('D', self.no_dirty_cells)
        place_randomly('R', 1)
        place_randomly('O', _percent_to_number(obstacle_percent, self.total_cells))
        place_randomly('K', no_kids)

        self.kids = [(i,j) for i in range(self.rows) for j in range(self.columns) if self.board[i][j] == 'K']

        logger.write(self)
    def valid_position(self, x, y):
        return x >= 0 and x < self.columns and y >= 0 and y < self.rows

    def change(self):
        for i, (x, y) in enumerate(self.kids):
            dx, dy = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)][random.randint(0, 7)]
            nx, ny = x + dx, y + dy
            if self.valid_position(nx, ny):
                if self.board[nx][ny] == 'E':
                    self.board[x][y] = 'E'
                    self.board[nx][ny] = 'K'
                    self.kids[i] = (nx, ny)
                    logger.write(f"Kid {i} moved from {x, y} to {nx, ny}\n")
                elif self.board[nx][ny] == 'O':
                    nxx, nyy = nx, ny
                    while self.valid_position(nxx, nyy) and self.board[nxx][nyy] == 'O':
                        nxx += dx
                        nyy += dy
                    if self.valid_position(nxx, nyy) and self.board[nxx][nyy] == 'E':
                        txx, tyy = nxx, nyy
                        while (txx, tyy) != (nx, ny):
                            txx -= dx
                            tyy -= dy
                            logger.write(f"Kid {i} Pushed object from {txx, tyy} to {txx + dx, tyy + dy}\n")
                        self.board[nxx][nyy] = 'O'
                        self.board[nx][ny] = 'K'
                        self.board[x][y] = 'E'
                        self.kids[i] = (nx, ny)
                        logger.write(f"Kid {i} moved from {x, y} to {nx, ny}\n")

        logger.write(self)

    def __repr__(self):
        result = 'Enviroment:\n'
        for i in range(self.rows):
            for j in range(self.columns):
                content = self.board[i][j]
                assert len(content) >= 1 and len(content) <=3
                result += content + ' ' * (4 - len(content))
            result += '\n'
        result += 'Kids: ' + str({i: (x,y) for i,(x,y) in enumerate(self.kids)}) + '\n\n'
        return result

    # @property
    # def dirt_cells_percent(self):
    #     return _number_to_percent(self.no_dirty_cells, self.total_cells)
