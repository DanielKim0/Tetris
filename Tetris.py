import pygame, random

class Tetromino(object):
    def __init__(self, board):
        self.locked = False
        self.board = board
        self.rand_num = random.randrange(0, 7)
        self.location = [[3, 0], [4, 0], [4, 0], [5, 0], [4, 0], [4, 0], [4, 0]][self.rand_num]
        self.blocks = [
            [[0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],

            [[1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]],

            [[1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]],

            [[1, 1],
            [1, 1]],

            [[0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]],

            [[0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]],

            [[1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]]
        ][self.rand_num]

    def get_locations(self, blocks):
        locations = []
        for y in range(len(blocks)):
            for x in range(len(blocks[0])):
                if blocks[y][x] == 1:
                    locations.append([self.location[0] + x, self.location[1] + y])
        return locations

    def valid_init(self):
        for coord in self.get_locations(self.blocks):
            if self.board[coord[1]][coord[0]] == 'X':
                return False
        return True

    def remove_board(self):
        for coord in self.get_locations(self.blocks):
            self.board[coord[1]][coord[0]] = ' '

    def update_board(self):
        for coord in self.get_locations(self.blocks):
            self.board[coord[1]][coord[0]] = 'O'

    def lock_piece(self):
        self.locked = True
        for coord in self.get_locations(self.blocks):
            self.board[coord[1]][coord[0]] = 'X'

    def valid_coord(self, coord):
        return 22 > coord[1] >= 0 and 10 > coord[0] >= 0 and self.board[coord[1]][coord[0]] != 'X'

    def move_left(self):
        valid = True
        for coord in self.get_locations(self.blocks):
            if not self.valid_coord([coord[0] - 1, coord[1]]):
                valid = False
        if valid:
            self.remove_board()
            self.location = [self.location[0] - 1, self.location[1]]
            self.update_board()

    def move_right(self):
        valid = True
        for coord in self.get_locations(self.blocks):
            if not self.valid_coord([coord[0] + 1, coord[1]]):
                valid = False
        if valid:
            self.remove_board()
            self.location = [self.location[0] + 1, self.location[1]]
            self.update_board()

    def move_down(self):
        valid = True
        for coord in self.get_locations(self.blocks):
            if not self.valid_coord([coord[0], coord[1] + 1]):
                valid = False
        if valid:
            self.remove_board()
            self.location = [self.location[0], self.location[1] + 1]
            self.update_board()
        else:
            self.lock_piece()

    def rotate(self):
        rotate = list(zip(*self.blocks[::-1]))

        valid = True
        for coord in self.get_locations(rotate):
            if not self.valid_coord([coord[0], coord[1]]):
                valid = False
        if valid:
            self.remove_board()
            self.blocks = rotate
            self.update_board()

    def get_locked(self):
        return self.locked


class Game(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("text.ttf", 40)
        pygame.key.set_repeat(80, 40)

        self.game_over = False
        self.screen = pygame.display.set_mode((500, 600))
        self.clock = pygame.time.Clock()
        self.tick = 0
        self.lines = 0
        self.drop = 30
        self.points = 0

        self.board = []
        for y in range(22):
            self.board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
        self.current_piece = Tetromino(self.board)

        with open("highscore.txt", "r") as score_file:
            self.high_score = int(score_file.read())

        pygame.mixer.init()
        pygame.mixer.music.load("tetris_music.ogg")
        pygame.mixer.music.play(-1, 0.0)

    def new_high(self):
        with open("highscore.txt", "w") as score_file:
            score_file.write(str(self.lines))

    def draw_text(self):
        line = "0" * (3 - len(str(self.lines))) + str(self.lines)
        score = "0" * (3 - len(str(self.high_score))) + str(self.high_score)

        label1 = self.font.render("SCORE", True, (255, 255, 255))
        label2 = self.font.render(str(line), True, (255, 255, 255))
        label3 = self.font.render("HIGH", True, (255, 255, 255))
        label4 = self.font.render(str(score), True, (255, 255, 255))
        self.screen.blit(label1, (315, 100))
        self.screen.blit(label2, (345, 140))
        self.screen.blit(label3, (330, 300))
        self.screen.blit(label1, (315, 340))
        self.screen.blit(label4, (345, 380))

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        for y in range(2, 22):
            for x in range(10):
                if self.board[y][x] == 'X':
                    pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(x * 30 + 5, y * 30 - 57, 24, 24))
                elif self.board[y][x] == 'O':
                    pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(x * 30 + 5, y * 30 - 57, 24, 24))
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x * 30 + 5, y * 30 - 57, 24, 24))

    def update_board(self):
        rows_filled = []
        for row in range(len(self.board)):
            if len(list(filter(lambda x: x == 'X', self.board[row]))) == 10:
                rows_filled.append(row)
        if len(rows_filled) > 0:
            for row in rows_filled:
                del(self.board[row])
                self.board.insert(0, [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
            self.lines += len(rows_filled)
        self.draw_text()

    def update_drop(self):
        self.lines = min(self.lines, 999)
        difficulties = [30, 20, 15, 12, 10, 6, 5, 4, 3, 2]
        self.drop = difficulties[min(self.lines // 10, 9)]

    def run(self):
        self.draw_text()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.current_piece.rotate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.current_piece.move_down()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.current_piece.move_left()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.current_piece.move_right()

            if self.current_piece.get_locked():
                self.current_piece = Tetromino(self.board)
                if not self.current_piece.valid_init():
                    self.new_high()
                    self.game_over = True

            self.update_drop()

            if self.tick % self.drop == 0:
                self.current_piece.move_down()

            self.draw_board()
            self.update_board()
            pygame.display.flip()
            self.clock.tick(60)
            self.tick += 1


game = Game()
game.run()
