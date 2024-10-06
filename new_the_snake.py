
from the_snake import *


def main():
    """Функция основного игрового процесса."""
    pygame.init()
    apple = Apple()
    bad_apple = Apple((0, 0, 255))
    stone = Apple((0, 177, 177))
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