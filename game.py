# In order for game to exist we need:
# - controllers for person
# - operations for the snake to perform
# - snake state
# - visual representation of the field and the snake
from enum import Enum, auto


class SnakeDirection(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()


class SnakeGame:
    FRUIT_CELL = ' @ '
    FIELD_CELL = ' . '
    SNAKE_BODY_PART = ' % '

    def __init__(self, field_size):
        self.field_size = field_size
        self.field = []

        self.snake_body = self.get_initial_snake_body()
        self.snake_direction = SnakeDirection.Right

        self.fruit = None

    def generate_square_field(self):
        for i in range(self.field_size):
            self.field.append([self.FIELD_CELL for _ in range(self.field_size)])

    def draw_game_field(self):
        for row in self.field:
            str_row = ''
            for cell in row:
                str_row += cell
            print(str_row)

    def generate_fruit_pos(self):
        import random
        sample = [i for i in range(self.field_size)]
        self.fruit = {
            'coordinate_x': random.choice(sample),
            'coordinate_y': random.choice(sample)
        }

    def add_fruit_to_the_field(self):
        if not self.fruit:
            self.generate_fruit_pos()
        if not self.field:
            self.generate_square_field()
        self.field[self.fruit['coordinate_y']][self.fruit['coordinate_x']] = self.FRUIT_CELL

    def get_initial_snake_body(self):
        middle_field_idx = int(self.field_size // 2)
        return [{'coordinate_x': middle_field_idx - i, 'coordinate_y': middle_field_idx} for i in range(3)]

    def add_snake_to_the_field(self):
        for part in self.snake_body:
            self.field[part['coordinate_y']][part['coordinate_x']] = self.SNAKE_BODY_PART

    def operate_snake_body(self):

        def on_arrow_release(key):
            if key == Key.up:
                self.snake_direction = SnakeDirection.Up
            elif key == Key.down:
                self.snake_direction = SnakeDirection.Down
            elif key == Key.left:
                self.snake_direction = SnakeDirection.Left
            elif key == Key.right:
                self.snake_direction = SnakeDirection.Right
            return False

        import time
        from pynput.keyboard import Key, Listener
        while True:
            time.sleep(1)
            print(self.snake_direction)
            while time.sleep(1):
                with Listener(on_release=on_arrow_release) as listener:
                    listener.join()




if __name__ == '__main__':
    snake = SnakeGame(10)
    snake.add_fruit_to_the_field()
    snake.add_snake_to_the_field()
    snake.draw_game_field()
    snake.operate_snake_body()
