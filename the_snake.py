import sys
from random import choice, randint

import pygame

# Размеры игрового поля
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_cell(surface, position, color):
    """Рисует квадрат размером GRID_SIZE по координатам position."""
    rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, color, rect)


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(
        self,
        position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
        body_color=None,
    ):
        """Инициализирует позицию (центр экрана) и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод отрисовки: переопределяется в наследниках."""
        pass


class Apple(GameObject):
    """Яблоко — случайный корм для змейки."""

    body_color = RED

    def __init__(self):
        """Задаёт цвет яблока и вызывает randomize_position()."""
        super().__init__(body_color=self.body_color)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока в пределах поля."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле."""
        draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Змейка: движение, рост, отрисовка и сброс."""

    body_color = GREEN

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color=self.body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Применяет направление, заданное нажатием клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку: новая голова, хвост удаляется при росте."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Отрисовывает сегменты змейки и затирает след хвоста."""
        for position in self.positions:
            draw_cell(surface, position, self.body_color)
        if self.last:
            draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы: первый элемент positions."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку: длина 1, центр, случайное направление."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает выход из игры и нажатия клавиш управления."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')
    screen.fill(BOARD_BACKGROUND_COLOR)
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()