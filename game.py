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

        self.snake_body = []
        self.snake_direction = []

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

    def generate_initial_snake_state(self):
        self.snake_body = [{
            'coordinate_x': int(self.field_size // 2),
            'coordinate_y': int(self.field_size // 2)
        }, {
            'coordinate_x': int(self.field_size // 2) - 1,
            'coordinate_y': int(self.field_size // 2)
        }, {
            'coordinate_x': int(self.field_size // 2) - 2,
            'coordinate_y': int(self.field_size // 2)
        }]
        self.snake_direction = SnakeDirection.Right

    def add_snake_to_the_field(self):
        if not self.snake_body or not self.snake_direction:
            self.generate_initial_snake_state()
        for part in self.snake_body:
            self.field[part['coordinate_y']][part['coordinate_x']] = self.SNAKE_BODY_PART

    def operate_snake_body(self):
        ...


if __name__ == '__main__':
    snake = SnakeGame(10)
    snake.add_fruit_to_the_field()
    snake.add_snake_to_the_field()
    snake.draw_game_field()

