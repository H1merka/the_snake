from random import choice, randint
"""Модуль для случайного выбора."""

import pygame
"""Модуль для графического интерфейса."""

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)

# Цвет яблока.
APPLE_COLOR = (255, 0, 0)

# Цвет змейки.
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс, описывающий игровой объект."""

    def __init__(self):
        """Конструктор класса."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Пустой метод отрисовки для переопределения."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.position = Apple.randomize_position(self)
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод определения положения яблока."""
        width_position = randint(0, GRID_WIDTH) * GRID_SIZE
        height_position = randint(0, GRID_HEIGHT) * GRID_SIZE
        return (width_position, height_position)

    def draw(self):
        """Метод отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змею."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод изменения направления движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод отрисовки змеи."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возврата положения головы змеи."""
        return self.positions[0]

    def reset(self):
        """Метод сброса змеи в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)
        return self.positions

    def move(self):
        """Метод, отвечающий за движение змеи."""
        head = Snake.get_head_position(self)
        if self.direction == UP:
            head = (head[0], head[1] - GRID_SIZE)
            if head[1] < 0:
                head[1] = 480
        elif self.direction == DOWN:
            head = (head[0], head[1] + GRID_SIZE)
            if head[1] > 480:
                head[1] = 0
        elif self.direction == RIGHT:
            head = (head[0] + GRID_SIZE, head[1])
            if head[0] > 640:
                head[0] = 0
        else:
            head = (head[0] - GRID_SIZE, head[1])
            if head[0] < 0:
                head[0] = 640

        if head in self.positions[2:]:
            return Snake.reset()
        else:
            self.positions.insert(0, head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop(len(self.positions) - 1)
            else:
                pass


def handle_keys(game_object):
    """Функция, обрабатывающая нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция, описывающая логику игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        pygame.display.update()


if __name__ == '__main__':
    main()
