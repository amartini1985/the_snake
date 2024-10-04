from random import choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

GRID_WIDTH_VAL = [i * GRID_SIZE for i in range(SCREEN_WIDTH // GRID_SIZE)]
GRID_HEIGHT_VAL = [i * GRID_SIZE for i in range(SCREEN_HEIGHT // GRID_SIZE)]
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = BLACK_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет гнилого яблока
BAD_APPLE_COLOR = (0, 0, 255)

# Цвет камня
STONE_COLOR = (255, 255, 255)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет змейки
STONE_COLOR = (255, 255, 255)

# Скорость движения змейки:
SPEED = 3

# Словарь для фиксации нажатых клавиш:
KEY_PAD = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

# Настройка кнопки:

BUTTON_TEXT_COLOR = (0, 0, 0)

WHITE_COLOR = (255, 255, 255)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100), 0, 32)

# Линия отделяющая игровое и служебные части экрана
pg.draw.line(screen, WHITE_COLOR, (0, SCREEN_HEIGHT), SCREEN_SIZE)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Отрисовка кнопки выхода
rect_button = pg.Rect(((SCREEN_WIDTH / 2) - 50, SCREEN_HEIGHT + 33), (100, 33))
pg.draw.rect(screen, WHITE_COLOR, rect_button)


class GameObject:
    """Описания базового класса."""

    def __init__(self, position=None, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод который будет переопределен в наследуемых классах."""
        raise NotImplementedError('Необходимо переопределить метод')

    def draw_rect(self, position, body_color, border_color=BORDER_COLOR):
        """Метод отрисовки прямоугольника."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Snake(GameObject):
    """Описания наследуемого от GameObject класса поведения змейки."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод реализующий движение змейки."""
        direct_x = self.direction[0] * GRID_SIZE
        direct_y = self.direction[1] * GRID_SIZE
        current_х = self.get_head_position()[0]
        current_y = self.get_head_position()[1]
        new_position_x = (current_х + direct_x) % SCREEN_WIDTH
        new_position_y = (current_y + direct_y) % SCREEN_HEIGHT
        self.positions.insert(0, (new_position_x, new_position_y))
        self.last = self.positions.pop()

    def draw(self):
        """Метод отрисовывающий положение змейки на игровом поле."""
        self.draw_rect(self.positions[0], self.body_color)

        if self.last:
            self.draw_rect(self.last, BLACK_COLOR, BLACK_COLOR)

    def get_head_position(self):
        """Метод определения положения головы змейки."""
        return (self.positions[0])

    def reset(self):
        """Метод инициализации новой змейки."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def add_body(self):
        """Метод для добавления к телу змейки нового элемента."""
        self.positions.append(self.last)
        self.last = None

    def kill_snake_body(self):
        """Метод для затирания тела змейки после наползания змейки на себя."""
        for position in self.positions:
            self.draw_rect(position, BLACK_COLOR, BLACK_COLOR)

    def del_element(self):
        """Метод для затирания элемента змеки после наползания на
        "Плохое bad_apple".
        """
        self.draw_rect(self.positions.pop(), BLACK_COLOR, BLACK_COLOR)


class Apple(GameObject):
    """Описания наследуемого от GameObject класса поведения "яблока",
    "плохого яблока" и "препятствия".
    """

    def __init__(
            self,
            position=None,
            body_color=APPLE_COLOR,
            occupied_position=[]
    ):
        super().__init__(position, body_color)
        self.occupied_position = occupied_position
        self.randomize_position(occupied_position)

    def randomize_position(self, occupied_position):
        """Метод определения координат объекта на игровом поле."""
        while True:
            self.position = (choice(GRID_WIDTH_VAL), choice(GRID_HEIGHT_VAL))
            if self.position not in occupied_position:
                break

    def draw(self):
        """Метод отображения объекта на игровом поле."""
        self.draw_rect(self.position, self.body_color)

    def draw_erase(self):
        """Метод для затирания "камня"."""
        self.draw_rect(self.position, BLACK_COLOR, BLACK_COLOR)


def handle_keys(game_object):
    """Функция обработки событий клавиш."""
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            game_object.next_direction = KEY_PAD.get(
                (game_object.direction, event.key)
            )
        elif event.type == pg.MOUSEBUTTONDOWN:
            if (
                SCREEN_WIDTH / 2 - 50 <= mouse[0] <= SCREEN_WIDTH / 2 + 50
                and SCREEN_HEIGHT + 10 <= mouse[1] <= SCREEN_HEIGHT + 90
            ):
                pg.quit()


def main():
    """Функция основного игрового процесса."""
    pg.init()
    occupied_position = []
    font = pg.font.SysFont(None, 20, False, False)
    text = font.render('Escape', True, BUTTON_TEXT_COLOR)
    screen.blit(text, (SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT + 45))
    snake = Snake()
    occupied_position.extend(snake.positions)
    apple = Apple(occupied_position)
    occupied_position.append(apple.position)
    bad_app = Apple(
        body_color=BAD_APPLE_COLOR,
        occupied_position=occupied_position
    )
    occupied_position.append(bad_app.position)
    stone = Apple(
        body_color=STONE_COLOR,
        occupied_position=occupied_position
    )
    occupied_position.append(stone.position)
    while True:
        clock.tick(SPEED)
        occupied_position = []
        occupied_position.extend(snake.positions)
        occupied_position.append(apple.position)
        occupied_position.append(bad_app.position)
        occupied_position.append(stone.position)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            occupied_position.remove(apple.position)
            apple.randomize_position(occupied_position)
            occupied_position.append(apple.position)
            snake.add_body()
            snake.length += 1
        elif snake.get_head_position() == bad_app.position:
            occupied_position.remove(bad_app.position)
            bad_app.randomize_position(occupied_position)
            occupied_position.append(bad_app.position)
            if snake.length > 1:
                snake.del_element()
                snake.length -= 1
        elif snake.get_head_position() == stone.position:
            stone.draw_erase()
            snake.kill_snake_body()
            occupied_position.remove(stone.position)
            stone.randomize_position(occupied_position)
            occupied_position.append(stone.position)
            snake.kill_snake_body()
            snake.reset()
        elif snake.get_head_position() in snake.positions[1:]:
            snake.kill_snake_body()
            snake.reset()
        apple.draw()
        bad_app.draw()
        stone.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
