# In order for game to exist we need:
# - controllers for person
# - operations for the snake to perform
# - snake state
# - visual representation of the field and the snake
import time

from pynput import keyboard


class SnakeDirection:
    UP = keyboard.Key.up
    DOWN = keyboard.Key.down
    LEFT = keyboard.Key.left
    RIGHT = keyboard.Key.right
    ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


class SnakeGame:
    FRUIT_CELL = ' @ '
    FIELD_CELL = ' . '
    SNAKE_BODY_PART = ' % '

    X_KEY = 'coordinate_x'
    Y_KEY = 'coordinate_y'

    def __init__(self, field_size):
        self.field_size = field_size
        self.field = []

        self.snake_body = self.get_initial_snake_body()
        self.snake_direction = SnakeDirection.RIGHT

        self.fruit = None

    def generate_square_field(self):
        for i in range(self.field_size):
            self.field.append([self.FIELD_CELL for _ in range(self.field_size)])

    def draw_game_field(self):
        self.add_snake_to_the_field()

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
        self.field[self.fruit[self.Y_KEY]][self.fruit[self.X_KEY]] = self.FRUIT_CELL

    def get_initial_snake_body(self):
        middle_field_idx = int(self.field_size // 2)
        return [{self.X_KEY: middle_field_idx - i, self.Y_KEY: middle_field_idx} for i in range(3)]

    def move_snake_in_direction(self):
        # To calculate the movement we need to:
        #  increase the body if the fruit is in the place where the head is heading :)
        #  save the angles of body
        #  recalculate position of the first and the last known segment of body
        #  the first component is in the direction of movement
        #  the last component disappears or stays the same depending on the fruit case
        prev_coord_x, prev_coord_y = self.snake_body[0][self.X_KEY], self.snake_body[0][self.Y_KEY]

        if self.snake_direction == SnakeDirection.UP:
            self.snake_body.insert(0, {self.X_KEY: prev_coord_x, self.Y_KEY: prev_coord_y - 1})
        elif self.snake_direction == SnakeDirection.DOWN:
            self.snake_body.insert(0, {self.X_KEY: prev_coord_x, self.Y_KEY: prev_coord_y + 1})
        elif self.snake_direction == SnakeDirection.LEFT:
            self.snake_body.insert(0, {self.X_KEY: prev_coord_x - 1, self.Y_KEY: prev_coord_y})
        elif self.snake_direction == SnakeDirection.RIGHT:
            self.snake_body.insert(0, {self.X_KEY: prev_coord_x + 1, self.Y_KEY: prev_coord_y})

        if self.fruit != self.snake_body[0]:
            self.snake_body.pop(-1)
        else:
            self.fruit = None
            self.add_fruit_to_the_field()

    def add_snake_to_the_field(self):
        for part in self.snake_body:
            self.field[part[self.Y_KEY]][part[self.X_KEY]] = self.SNAKE_BODY_PART

    def record_the_arrow_keys_pressing(self):
        with keyboard.Events() as events:
            # Block at most one second
            event = events.get(1.0)
            if event is not None:
                if event.key in SnakeDirection.ALL_DIRECTIONS:
                    self.snake_direction = event.key

    def check_borders(self):
        if self.snake_body[0][self.X_KEY] == 0 and self.snake_direction == SnakeDirection.LEFT:
            return False
        elif self.snake_body[0][self.X_KEY] == self.field_size and self.snake_direction == SnakeDirection.RIGHT:
            return False
        elif self.snake_body[0][self.Y_KEY] == self.field_size and self.snake_direction == SnakeDirection.DOWN:
            return False
        elif self.snake_body[0][self.Y_KEY] == 0 and self.snake_direction == SnakeDirection.UP:
            return False
        elif self.snake_body[0] in self.snake_body[1:]:
            return False
        else:
            return True

    def launch_game(self):
        # We need to record the last instruction from user, otherwise we use previous snake_direction.
        # We also need to render the field every second (2, 3?).
        # We need while loop that stops when the snake's head is on any edge of the field and heading towards this edge.
        self.add_fruit_to_the_field()

        while self.check_borders():
            self.draw_game_field()

            self.record_the_arrow_keys_pressing()

            self.move_snake_in_direction()


if __name__ == '__main__':
    snake = SnakeGame(10)
    snake.launch_game()
