import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT
FPS = 60

# Цвета
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GRAY': (128, 128, 128),
    'CYAN': (0, 255, 255),
    'YELLOW': (255, 255, 0),
    'PURPLE': (128, 0, 128),
    'BLUE': (0, 0, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'ORANGE': (255, 165, 0)
}

# Формы тетромино
TETROMINOES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLOR_MAP = {
    'I': COLORS['CYAN'],
    'O': COLORS['YELLOW'],
    'T': COLORS['PURPLE'],
    'S': COLORS['GREEN'],
    'Z': COLORS['RED'],
    'J': COLORS['BLUE'],
    'L': COLORS['ORANGE']
}


class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 50  # Чем меньше значение, тем быстрее падение

    def new_piece(self):
        shape = random.choice(list(TETROMINOES.keys()))
        return {
            'shape': shape,
            'rotation': 0,
            'x': GRID_WIDTH // 2 - len(TETROMINOES[shape][0]) // 2,
            'y': 0,
            'color': COLOR_MAP[shape]
        }

    def valid_move(self, piece, x, y):
        for i in range(len(TETROMINOES[piece['shape']])):
            for j in range(len(TETROMINOES[piece['shape']][0])):
                if TETROMINOES[piece['shape']][i][j]:
                    new_x = x + j
                    new_y = y + i
                    if (new_x < 0 or new_x >= GRID_WIDTH or
                            new_y >= GRID_HEIGHT or
                            (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True

    def rotate_piece(self):
        old_rotation = self.current_piece['rotation']
        self.current_piece['rotation'] = (self.current_piece['rotation'] + 1) % 4
        rotated = [list(row) for row in TETROMINOES[self.current_piece['shape']]]
        for _ in range(self.current_piece['rotation']):
            rotated = list(zip(*rotated[::-1]))
        temp = TETROMINOES[self.current_piece['shape']]
        TETROMINOES[self.current_piece['shape']] = rotated
        if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
            self.current_piece['rotation'] = old_rotation
            TETROMINOES[self.current_piece['shape']] = temp

    def merge_piece(self):
        for i in range(len(TETROMINOES[self.current_piece['shape']])):
            for j in range(len(TETROMINOES[self.current_piece['shape']][0])):
                if TETROMINOES[self.current_piece['shape']][i][j]:
                    y = self.current_piece['y'] + i
                    x = self.current_piece['x'] + j
                    if y >= 0:
                        self.grid[y][x] = self.current_piece['color']

    def clear_lines(self):
        lines_cleared = 0
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared * 100

    def draw(self):
        self.screen.fill(COLORS['BLACK'])

        # Отрисовка сетки
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.grid[i][j]:
                    pygame.draw.rect(self.screen, self.grid[i][j],
                                     [j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1])
                pygame.draw.rect(self.screen, COLORS['GRAY'],
                                 [j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE], 1)

        # Отрисовка текущей фигуры
        for i in range(len(TETROMINOES[self.current_piece['shape']])):
            for j in range(len(TETROMINOES[self.current_piece['shape']][0])):
                if TETROMINOES[self.current_piece['shape']][i][j]:
                    pygame.draw.rect(self.screen, self.current_piece['color'],
                                     [(self.current_piece['x'] + j) * GRID_SIZE,
                                      (self.current_piece['y'] + i) * GRID_SIZE,
                                      GRID_SIZE - 1, GRID_SIZE - 1])

        # Отрисовка следующей фигуры
        for i in range(len(TETROMINOES[self.next_piece['shape']])):
            for j in range(len(TETROMINOES[self.next_piece['shape']][0])):
                if TETROMINOES[self.next_piece['shape']][i][j]:
                    pygame.draw.rect(self.screen, self.next_piece['color'],
                                     [(GRID_WIDTH + 1 + j) * GRID_SIZE,
                                      (2 + i) * GRID_SIZE,
                                      GRID_SIZE - 1, GRID_SIZE - 1])

        # Отрисовка счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, COLORS['WHITE'])
        self.screen.blit(score_text, (GRID_SIZE * (GRID_WIDTH + 1), GRID_SIZE * 6))

    def run(self):
        while not self.game_over:
            self.fall_time += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.current_piece['x'] - 1, self.current_piece['y']):
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.current_piece['x'] + 1, self.current_piece['y']):
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                            self.current_piece['y'] += 1
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        while self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                            self.current_piece['y'] += 1
                        self.merge_piece()
                        self.clear_lines()
                        self.current_piece = self.next_piece
                        self.next_piece = self.new_piece()
                        if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
                            self.game_over = True

            # Автоматическое падение
            if self.fall_time >= self.fall_speed:
                self.fall_time = 0
                if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                    self.current_piece['y'] += 1
                else:
                    self.merge_piece()
                    self.clear_lines()
                    self.current_piece = self.next_piece
                    self.next_piece = self.new_piece()
                    if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
                        self.game_over = True

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        # Экран окончания игры
        font = pygame.font.Font(None, 48)
        game_over_text = font.render('Game Over!', True, COLORS['WHITE'])
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 24))
        pygame.display.flip()
        pygame.time.wait(2000)


if __name__ == '__main__':
    game = Tetris()
    game.run()
    pygame.quit()