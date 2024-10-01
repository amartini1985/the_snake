from random import choice


import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


GRID_WIDTH_VALUE = list(_ * 20 for _ in range(int(SCREEN_WIDTH / GRID_SIZE)))
GRID_HEIGHT_VALUE = list(_ * 20 for _ in range(int(SCREEN_HEIGHT / GRID_SIZE)))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет змейки
STONE_COLOR = (255, 255, 255)

# Скорость движения змейки:
SPEED = 3

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Описания базового класса."""

    def __init__(self):
        self.position = tuple([int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)])
        self.body_color = None

    def draw(self):
        """Метод который будет переопределен в наследуемых классах."""
        pass


class Snake(GameObject):
    """Описания наследуемого от GameObject класса поведения змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__()
        self.length = 1
        self.positions = []
        list.append(self.positions, (0, 0))
        self.direction = (1, 0)
        self.next_direction = None
        self.body_color = body_color
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод реализующий движение змейки."""
        self.last = self.positions[-1]
        list.insert(self.positions, 0, self.get_head_position())
        list.remove(self.positions, self.positions[(-1)])

    def draw(self):
        """Метод отрисовывающий положение змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод определение положения головы змейки."""
        direction_x = self.direction[0] * GRID_SIZE
        direction_y = self.direction[1] * GRID_SIZE
        if ((direction_x + self.positions[0][0]) < SCREEN_WIDTH and
           (direction_x + self.positions[0][0]) >= 0):
            position_x = direction_x + self.positions[0][0]
        elif ((direction_x + self.positions[0][0]) >= SCREEN_WIDTH and
              (direction_x + self.positions[0][0]) >= 0):
            position_x = 0
        else:
            position_x = SCREEN_WIDTH - GRID_SIZE
        if ((direction_y + self.positions[0][1]) < SCREEN_HEIGHT and 
           (direction_y + self.positions[0][1]) >= 0):
            position_y = direction_y + self.positions[0][1]
        elif ((direction_y + self.positions[0][1]) >= SCREEN_HEIGHT and 
              (direction_y + self.positions[0][1]) >= 0):
            position_y = 0
        else:
            position_y = SCREEN_HEIGHT - GRID_SIZE
        return (position_x, position_y)

    def reset(self):
        """Метод определения наползания змейки на себя."""
        if self.length > 3:
            for i in range(1, self.length):
                if self.positions[0] == self.positions[i]:
                    return True

    def add_body(self):
        """Метод для добавления к телу змейки нового элемента."""
        list.append(self.positions, self.last)
        return

    def kill_snake_body(self):
        """Метод для затирания тела змейки после наползания змейки на себя."""
        for position in self.positions:
            kill_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, kill_rect)

    def del_body(self):
        """Метод для затирания элемента змеки после наползания на
        "Плохое bad_apple".
        """
        last_rect = pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        list.pop(self.positions)
        return


class Apple(GameObject):
    """Описания наследуемого от GameObject класса поведения "яблока",
    "плохого яблока" и "препятствия".
    """

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__()
        self.body_color = body_color
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод определения координат объекта на игровом поле."""
        return (choice(GRID_WIDTH_VALUE), choice(GRID_HEIGHT_VALUE))

    def draw(self):
        """Метод отображения объекта на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw_erase(self):
        """Метод для затирания элемента змеки после наползания на "камень"."""
        kill_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, kill_rect)


def handle_keys(game_object):
    """Функция обработки событий клавиш."""
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
    """Функция основного игрового процесса."""
    pygame.init()
    apple = Apple()
    bad_apple = Apple((0, 0, 255))
    stone = Apple((255, 255, 255))
    while bad_apple.position == apple.position:
        bad_apple.position = bad_apple.randomize_position()
    while ((stone.position == apple.position) or
           (stone.position == bad_apple.position)):
        stone.position = stone.randomize_position()
    snake = Snake()
    apple.draw()
    bad_apple.draw()
    snake.draw()
    stone.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw()
        bad_apple.draw()
        stone.draw()
        snake.draw()
        if snake.positions[0] == apple.position:
            apple.position = apple.randomize_position()
            apple.draw()
            snake.add_body()
            snake.length += 1
        if snake.positions[0] == bad_apple.position:
            bad_apple.position = bad_apple.randomize_position()
            bad_apple.draw()
            if snake.length > 1:
                snake.del_body()
                snake.length -= 1
        if snake.positions[0] == stone.position:
            stone.draw_erase()
            snake.kill_snake_body()
            stone.position = stone.randomize_position()
            stone.draw()
            del snake
            snake = Snake((0, 255, 0))
        if snake.reset():
            snake.kill_snake_body()
            del snake
            snake = Snake((0, 255, 0))
        pygame.display.update()


if __name__ == '__main__':
    main()
