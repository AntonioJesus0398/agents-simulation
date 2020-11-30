from main import *

robot_logger = Logger('R1.txt')

class Robot:
    def __init__(self, enviroment):
        self.enviroment = enviroment
        self.state = 'I'

    def execute(self):
        pass

class HibridRobot(Robot):
    def build_path(self, distances, end):
        x, y = end
        d = distances[x][y]
        if d == 0:
            return [(x, y)]
        for dx, dy in self.enviroment.directions:
            nx, ny = x + dx, y + dy
            if self.enviroment.valid_position(nx, ny) and distances[nx][ny] == d - 1:
                return  self.build_path(distances, (nx, ny)) + [(x, y)]

    def search(self, symbol):
        INF = self.enviroment.rows * self.enviroment.columns + 1
        distances = [[INF for _ in range(self.enviroment.columns)] for _ in range(self.enviroment.rows)]
        rx, ry = self.enviroment.robot_position
        robot_logger.write(f'Robot position: {rx, ry}\n')
        pending_cells = [(rx, ry)]
        distances[rx][ry] = 0
        while pending_cells:
            x, y = pending_cells.pop()
            for dx, dy in self.enviroment.directions:
                nx, ny = x + dx, y + dy
                if self.enviroment.valid_position(nx, ny) and self.enviroment.board[nx][ny] != 'O':
                    if distances[nx][ny] > distances[x][y] + 1:
                        distances[nx][ny] = distances[x][y] + 1
                        pending_cells.append((nx, ny))
        distances_to_targets = []
        for i in range(self.enviroment.rows):
            for j in range(self.enviroment.columns):
                if self.enviroment.board[i][j] == symbol:
                    distances_to_targets.append((distances[i][j], (i, j)))
        distances_to_targets.sort()
        robot_logger.write(f'distances: {distances_to_targets}\n')
        d, pos = distances_to_targets[0]
        path = self.build_path(distances, pos)
        robot_logger.write(f'Path to nearest: {path}\n\n')
        return path

    def execute(self):
        if self.enviroment.time == 100:
            if self.enviroment.dirt_cells_percent <= 40: self.state = 'FS'
            else: self.state = 'FF'

        elif self.enviroment.dirt_cells_percent > 40:
            self.state = 'FF'

        elif self.state == 'I':
            if self.enviroment.free_kids == 0 and self.enviroment.no_dirty_cells == 0:
                self.state = 'FS'
                robot_logger.write(f'Switched state from I to FS\n')
            elif self.enviroment.dirt_cells_percent <= 20 and self.enviroment.free_kids:
                path = self.search('K')
                nx, ny = path[1]
                self.move_robot(self.enviroment.robot_position, path[1])
                if self.enviroment.board[nx][ny] == 'R_K':
                    self.enviroment.board[nx][ny] = 'RK'
                    robot_logger.write(f'Switched state from I to MK\n')
                    self.state = 'MK'
                else:
                    self.state = 'SK'
                    robot_logger.write(f'Switched state from I to SK\n')
            elif (self.enviroment.dirt_cells_percent > 20 and self.enviroment.dirt_cells_percent < 40) or (self.enviroment.dirt_cells_percent < 40 and self.enviroment.free_kids == 0):
                path = self.search('D')
                self.move_robot(self.enviroment.robot_position, path[1])
                self.state = 'SD'
                robot_logger.write(f'Switched state from I to SD\n')
            else:
                self.state = 'FF'
                robot_logger.write(f'Switched state from I to FF\n')

        elif self.state == 'SK':
            path = self.search('K')
            nx, ny = path[1]
            self.move_robot(self.enviroment.robot_position, path[1])
            if self.enviroment.board[nx][ny] == 'R_K':
                self.enviroment.board[nx][ny] = 'RK'
                robot_logger.write(f'Switched state from SK to MK\n')
                self.state = 'MK'

        elif self.state == 'SD':
            x, y = self.enviroment.robot_position
            if self.enviroment.board[x][y] == 'R_D':
                self.enviroment.board[x][y] = 'R'
                self.enviroment.no_dirty_cells -= 1
                logger.write(f'Robot cleaned {x, y}\n')
                self.state = 'I'
                robot_logger.write(f'Switched state from SD to I\n')
            else:
                path = self.search('D')
                self.move_robot(self.enviroment.robot_position, path[1])

        elif self.state == 'MK':
            x, y = self.enviroment.robot_position
            path = self.search('P')
            nx, ny = path[1]
            if self.enviroment.board[nx][ny] != 'P':
                nx, ny = path[2]
            self.move_robot((x, y), (nx, ny))
            if self.enviroment.board[nx][ny] == 'RK_P':
                self.enviroment.board[nx][ny] = 'R_PK'
                logger.write(f'Robot left a kid in {nx, ny}\n')
                self.enviroment.free_kids -= 1
                self.state = 'I'
                robot_logger.write(f'Switched state from MK to I\n')

    def move_robot(self, src, dest):
        sx, sy = src
        dx, dy = dest

        src_content = self.enviroment.board[sx][sy].split('_')
        assert len(src_content) in [1, 2], f'The length is: {len(src_content)}'
        # if only the robot is in src
        if len(src_content) == 1:
            self.enviroment.board[sx][sy] = 'E'
        else:
            self.enviroment.board[sx][sy] = src_content[1]

        # the robot and the element in the dest cell coexist temporally
        dest_content = self.enviroment.board[dx][dy]
        if dest_content == 'E':
            self.enviroment.board[dx][dy] = src_content[0]
        else:
            self.enviroment.board[dx][dy] = src_content[0] + '_' + dest_content
        assert len(self.enviroment.board[dx][dy].split('_')) in [1, 2]

        self.enviroment.robot_position = (dx, dy)
        logger.write(f'Robot moved from {sx, sy} to {dx, dy}\n')
