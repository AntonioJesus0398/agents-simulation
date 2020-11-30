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

def _percent_to_number(percent, total):
    return int(percent * total / 100)

def _number_to_percent(number, total):
    return (number / total * 100)


class Enviroment:
    def __init__(self, N, M, dirty_percent, obstacle_percent, no_kids, time, t):
        self.rows = N
        self.columns = M
        self.dirty_percent = dirty_percent
        self.obstacle_percent = obstacle_percent
        self.total_kids = no_kids
        self.time = time
        self.t = t

        self.total_cells = N * M
        self.board = [['E' for _ in range(M)] for _ in range(N)]
        self.directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        self.free_kids = no_kids
        self.total_obstacles = _percent_to_number(obstacle_percent, self.total_cells)

        # place the playpens
        available_cells = [(random.randint(0, N - 1), random.randint(0, M - 1))]
        for _ in range(no_kids):
            random.shuffle(available_cells)
            x, y = available_cells.pop(0)
            self.board[x][y] = 'P'
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                if self.valid_position(nx, ny) and self.board[nx][ny] == 'E' and (nx, ny) not in available_cells:
                    available_cells.append((nx, ny))

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

        self.robot_position = [(i,j) for i in range(self.rows) for j in range(self.columns) if self.board[i][j] == 'R'][0]

        logger.write(self)

    def valid_position(self, x, y):
        return x >= 0 and x < self.rows and y >= 0 and y < self.columns

    def change(self):
        kids_moved = []
        # the kids move and push obstacles
        for x in range(self.rows):
            for y in range(self.columns):
                if self.board[x][y] == 'K' and (x, y) not in kids_moved:
                    dx, dy = self.directions[random.randint(0, 7)]
                    nx, ny = x + dx, y + dy
                    if self.valid_position(nx, ny):
                        if self.board[nx][ny] == 'E':
                            self.board[x][y] = 'E'
                            self.board[nx][ny] = 'K'
                            kids_moved.append((nx, ny))
                            logger.write(f"Kid moved from {x, y} to {nx, ny}\n")
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
                                    logger.write(f"Kid pushed object from {txx, tyy} to {txx + dx, tyy + dy}\n")
                                self.board[nxx][nyy] = 'O'
                                self.board[nx][ny] = 'K'
                                self.board[x][y] = 'E'
                                kids_moved.append((nx, ny))
                                logger.write(f"Kid moved from {x, y} to {nx, ny}\n")

                    # the kids generate dirt
                    available_cells = [(x + dh, y + dv) for dh, dv in self.directions if self.valid_position(x + dh, y + dv)] + [(x, y)]
                    no_kids = len([(a, b) for a,b in available_cells if self.board[a][b] == 'K'])
                    available_cells = [(a,b) for a, b in available_cells if self.board[a][b] == 'E']
                    random.shuffle(available_cells)

                    N = 1
                    if no_kids == 2:
                        N = 3
                    if no_kids > 2:
                        N = 6
                    for _ in range(N):
                        if len(available_cells) == 0:
                            break
                        if random.random() < 0.33:
                            a1, a2 = available_cells.pop(0)
                            self.board[a1][a2] = 'D'
                            self.no_dirty_cells += 1
                            logger.write(f'Kid generates dirt at {a1, a2}\n')

        logger.write(self)

    def __repr__(self):
        result = f'Enviroment after {self.time} units of time:\n'
        for i in range(self.rows):
            for j in range(self.columns):
                content = self.board[i][j]
                assert len(content) >= 1 and len(content) <=5
                result += content + ' ' * (6 - len(content))
            result += '\n'
        result += f'Robot position: {self.robot_position}\n'
        result += f'Free kids: {self.free_kids}\n'
        result += f'Dirty cells: {self.dirt_cells_percent}%\n\n'
        return result

    @property
    def dirt_cells_percent(self):
        total_empty_cells = self.total_cells - self.free_kids - self.total_kids - self.total_obstacles - 1
        return _number_to_percent(self.no_dirty_cells, total_empty_cells)

    def variate(self):
        return Enviroment(self.rows, self.columns, self.dirty_percent, self.obstacle_percent, self.total_kids, self.time, self.t)
