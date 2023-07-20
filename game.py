# In order for game to exist we need:
# - controllers for person
# - operations for the snake to perform
# - snake state
# - visual representation of the field and the snake
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

    def move_snake_in_direction(self):
        # To calculate the movement we need to:
        #  increase the body if the fruit is in the place where the head is heading :)
        #  save the angles of body
        #  recalculate position of the first and the last known segment of body
        #  the first component is in the direction of movement
        #  the last component is moving in the direction of the previous segment

        if self.snake_direction == SnakeDirection.UP:



    def add_snake_to_the_field(self):
        for part in self.snake_body:
            self.field[part['coordinate_y']][part['coordinate_x']] = self.SNAKE_BODY_PART

    def record_the_arrow_keys_pressing(self):
        with keyboard.Events() as events:
            # Block at most one second
            event = events.get(1.0)
            if event is not None:
                if event.key in SnakeDirection.ALL_DIRECTIONS:
                    self.snake_direction = event.key

    def operate_snake_body(self):
        # We need to record the last instruction from user, otherwise we use previous snake_direction.
        # We also need to render the field every second (2, 3?).
        # We need while loop that stops when the snake's head is on any edge of the field and heading towards this edge.

        while True:
            if self.snake_body[0]['coordinate_x'] == 0 and self.snake_body[0]['coordinate_y'] == 0 \
                    and self.snake_direction in [SnakeDirection.UP, SnakeDirection.LEFT]:
                break
            elif self.snake_body[0]['coordinate_x'] == self.field_size and self.snake_body[0]['coordinate_y'] == 0 \
                    and self.snake_direction in [SnakeDirection.UP, SnakeDirection.RIGHT]:
                break
            elif self.snake_body[0]['coordinate_x'] == self.field_size and self.snake_body[0][
                'coordinate_y'] == self.field_size \
                    and self.snake_direction in [SnakeDirection.DOWN, SnakeDirection.RIGHT]:
                break
            elif self.snake_body[0]['coordinate_x'] == 0 and self.snake_body[0]['coordinate_y'] == self.field_size \
                    and self.snake_direction in [SnakeDirection.DOWN, SnakeDirection.LEFT]:
                break

            self.draw_game_field()

            self.record_the_arrow_keys_pressing()

            self.move_snake_in_direction()


if __name__ == '__main__':
    snake = SnakeGame(10)
    snake.add_fruit_to_the_field()
    snake.add_snake_to_the_field()
    snake.draw_game_field()
    snake.operate_snake_body()
