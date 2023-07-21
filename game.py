import os
import time

from pynput import keyboard


class SnakeDirection:
    UP = keyboard.Key.up
    DOWN = keyboard.Key.down
    LEFT = keyboard.Key.left
    RIGHT = keyboard.Key.right
    ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


class SnakeGame:
    GREETING_PHRASE = '==Ordinary Snake Game==\n=The maximum recorded score is: {}=\nYour score is: {}.\n'
    NEW_MAX_SCORE_PHRASE = '\n=Congratulations! You set a new maximum score: {}!='
    END_PHRASE = '==Good job! Thank you for playing!=='

    FRUIT_CELL = ' @ '
    FIELD_CELL = ' . '
    SNAKE_HEAD = ' % '
    SNAKE_BODY_PART = ' o '

    BORDER_CELL = ' ~ '

    X_KEY = 'coordinate_x'
    Y_KEY = 'coordinate_y'

    def __init__(self, field_size=10):
        self.field_size = field_size
        self.field = []

        self.snake_body = self.get_initial_snake_body()
        self.snake_direction = SnakeDirection.RIGHT
        self.previous_snake_direction = None

        self.fruit = None

        self.score = 0

    @property
    def max_score(self):
        if os.path.exists('score.txt'):
            with open('score.txt') as file:
                score = file.readline()
            return score
        else:
            return 0

    def set_max_score(self):
        with open('score.txt', 'w') as file:
            file.write(str(self.score))

    def generate_square_field(self):
        for i in range(self.field_size):
            self.field.append([self.FIELD_CELL for _ in range(self.field_size)])

    def add_horizontal_border_to_the_field(self):
        print(self.BORDER_CELL * (self.field_size + 2))

    def draw_game_field(self):
        self.add_snake_to_the_field()

        print(self.GREETING_PHRASE.format(self.max_score, self.score))
        self.add_horizontal_border_to_the_field()
        for row in self.field:
            str_row = ''
            for cell in row:
                str_row += cell
            print(self.BORDER_CELL + str_row + self.BORDER_CELL)
        self.add_horizontal_border_to_the_field()

    def generate_fruit_pos(self):
        import random
        sample = [i for i in range(self.field_size)]

        self.fruit = {
            'coordinate_x': random.choice(sample),
            'coordinate_y': random.choice(sample)
        }
        if self.fruit in self.snake_body:
            self.generate_fruit_pos()

    def add_fruit_to_the_field(self):
        if not self.fruit:
            self.generate_fruit_pos()
        if not self.field:
            self.generate_square_field()
        self.field[self.fruit[self.Y_KEY]][self.fruit[self.X_KEY]] = self.FRUIT_CELL

    def get_initial_snake_body(self):
        middle_field_idx = int(self.field_size // 2)
        return [{self.X_KEY: middle_field_idx - i, self.Y_KEY: middle_field_idx} for i in range(3)]

    def check_borders(self):
        if self.snake_body[0][self.X_KEY] == 0 and self.snake_direction == SnakeDirection.LEFT:
            return False
        elif self.snake_body[0][self.X_KEY] == self.field_size - 1 and self.snake_direction == SnakeDirection.RIGHT:
            return False
        elif self.snake_body[0][self.Y_KEY] == self.field_size - 1 and self.snake_direction == SnakeDirection.DOWN:
            return False
        elif self.snake_body[0][self.Y_KEY] == 0 and self.snake_direction == SnakeDirection.UP:
            return False
        elif self.snake_body[0] in self.snake_body[1:]:
            return False
        else:
            return True

    def move_snake_in_direction(self):
        prev_coord_x, prev_coord_y = self.snake_body[0][self.X_KEY], self.snake_body[0][self.Y_KEY]

        new_head = None
        if self.snake_direction == SnakeDirection.UP:
            new_head = {self.X_KEY: prev_coord_x, self.Y_KEY: prev_coord_y - 1}
        elif self.snake_direction == SnakeDirection.DOWN:
            new_head = {self.X_KEY: prev_coord_x, self.Y_KEY: prev_coord_y + 1}
        elif self.snake_direction == SnakeDirection.LEFT:
            new_head = {self.X_KEY: prev_coord_x - 1, self.Y_KEY: prev_coord_y}
        elif self.snake_direction == SnakeDirection.RIGHT:
            new_head = {self.X_KEY: prev_coord_x + 1, self.Y_KEY: prev_coord_y}

        if new_head != self.snake_body[1]:
            self.snake_body.insert(0, new_head)
        else:
            self.snake_direction = None
            return

        if self.fruit != self.snake_body[0]:
            self.field[self.snake_body[-1][self.Y_KEY]][self.snake_body[-1][self.X_KEY]] = self.FIELD_CELL
            self.snake_body = self.snake_body[:-1]
        else:
            self.fruit = None
            self.score += 1
            self.add_fruit_to_the_field()

    def add_snake_to_the_field(self):
        for i, part in enumerate(self.snake_body):
            body_char = self.SNAKE_BODY_PART
            if i == 0:
                body_char = self.SNAKE_HEAD
            self.field[part[self.Y_KEY]][part[self.X_KEY]] = body_char

    @staticmethod
    def add_pause_to_movements(func):
        def wrapper(self):
            max_pause, min_pause, coefficient = 1.0, 0.4, 25
            pause = max_pause - (self.score / coefficient)
            pause = pause if pause > min_pause else min_pause

            start = time.time()
            func(self, pause)
            gap = time.time() - start
            time.sleep(pause - gap if pause > gap > 0 else 0)

        return wrapper

    @add_pause_to_movements
    def record_the_arrow_keys_pressing(self, period_in_sec):
        with keyboard.Events() as events:
            event = events.get(period_in_sec)
            if event is not None:
                if event.key in SnakeDirection.ALL_DIRECTIONS:
                    self.previous_snake_direction = self.snake_direction
                    self.snake_direction = event.key

    def launch_game(self):
        self.add_fruit_to_the_field()

        while self.check_borders():
            os.system('clear')

            self.move_snake_in_direction()
            self.draw_game_field()
            if not self.snake_direction:
                self.snake_direction = self.previous_snake_direction
            else:
                self.record_the_arrow_keys_pressing()
        else:
            if self.score > int(self.max_score):
                print(self.NEW_MAX_SCORE_PHRASE.format(self.score))
                self.set_max_score()
        print(self.END_PHRASE)


if __name__ == '__main__':
    SnakeGame().launch_game()
