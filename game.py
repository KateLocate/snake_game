import os
import time
from typing import List, Dict

from pynput import keyboard


class SnakeGameInterface:
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

    def __init__(self, field_size):
        self.field_size = field_size
        self.field = []

    def _generate_square_field(self):
        for i in range(self.field_size):
            self.field.append([self.FIELD_CELL for _ in range(self.field_size)])

    def draw_game_field(self, snake_body, max_score, score):
        self._add_snake_to_the_field(snake_body)

        print(self.GREETING_PHRASE.format(max_score, score))
        self._add_horizontal_border_to_the_field()
        for row in self.field:
            str_row = ''
            for cell in row:
                str_row += cell
            print(self.BORDER_CELL + str_row + self.BORDER_CELL)
        self._add_horizontal_border_to_the_field()

    def _add_horizontal_border_to_the_field(self):
        print(self.BORDER_CELL * (self.field_size + 2))

    def add_fruit_to_the_field(self, fruit):
        if not self.field:
            self._generate_square_field()
        self.field[fruit[self.Y_KEY]][fruit[self.X_KEY]] = self.FRUIT_CELL

    def _add_snake_to_the_field(self, snake_body):
        for i, part in enumerate(snake_body):
            body_char = self.SNAKE_BODY_PART
            if i == 0:
                body_char = self.SNAKE_HEAD
            self.field[part[self.Y_KEY]][part[self.X_KEY]] = body_char


class SnakeDirection:
    UP = keyboard.Key.up
    DOWN = keyboard.Key.down
    LEFT = keyboard.Key.left
    RIGHT = keyboard.Key.right
    ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


class SnakeGame:
    X_KEY = 'coordinate_x'
    Y_KEY = 'coordinate_y'

    SCORE_FILE = 'score.txt'

    def __init__(self, field_size=10):
        self.interface = SnakeGameInterface(field_size)

        self.snake_body = self._get_initial_snake_body()
        self.snake_direction = SnakeDirection.RIGHT
        self.previous_snake_direction = None

        self.fruit = None

        self.score = 0

    def launch_game(self):
        self._generate_fruit()
        self.interface.add_fruit_to_the_field(self.fruit)

        while self._check_borders():
            os.system('clear')

            self._move_snake_in_direction()
            self.interface.draw_game_field(self.snake_body, self._max_score, self.score)
            if not self.snake_direction:
                self.snake_direction = self.previous_snake_direction
            else:
                self._record_the_arrow_keys_pressing()
        else:
            if self.score > int(self._max_score):
                print(self.interface.NEW_MAX_SCORE_PHRASE.format(self.score))
                self._max_score = self.score
        print(self.interface.END_PHRASE)

    def _check_borders(self) -> bool:
        max_coordinate = self.interface.field_size - 1
        in_field_borders = True
        if self.snake_body[0][self.X_KEY] == 0 and self.snake_direction == SnakeDirection.LEFT:
            in_field_borders = False
        elif self.snake_body[0][self.X_KEY] == max_coordinate and self.snake_direction == SnakeDirection.RIGHT:
            in_field_borders = False
        elif self.snake_body[0][self.Y_KEY] == max_coordinate and self.snake_direction == SnakeDirection.DOWN:
            in_field_borders = False
        elif self.snake_body[0][self.Y_KEY] == 0 and self.snake_direction == SnakeDirection.UP:
            in_field_borders = False
        elif self.snake_body[0] in self.snake_body[1:]:
            in_field_borders = False
        return in_field_borders

    def _move_snake_in_direction(self):
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
            tail = self.snake_body[-1]
            self.interface.field[tail[self.Y_KEY]][tail[self.X_KEY]] = self.interface.FIELD_CELL
            self.snake_body.pop(-1)
        else:
            self.score += 1
            self._generate_fruit()
            self.interface.add_fruit_to_the_field(self.fruit)

    @staticmethod
    def _add_pause_to_movements(func):
        def wrapper(self):
            max_pause, min_pause, coefficient = 1.0, 0.4, 25
            pause = max_pause - (self.score / coefficient)
            pause = pause if pause > min_pause else min_pause

            start = time.time()
            func(self, pause)
            gap = time.time() - start
            time.sleep(pause - gap if pause > gap > 0 else 0)

        return wrapper

    @_add_pause_to_movements
    def _record_the_arrow_keys_pressing(self, period_in_sec):
        with keyboard.Events() as events:
            event = events.get(period_in_sec)
            if event is not None:
                if event.key in SnakeDirection.ALL_DIRECTIONS:
                    self.previous_snake_direction = self.snake_direction
                    self.snake_direction = event.key

    def _generate_fruit(self):
        import random
        sample = [i for i in range(self.interface.field_size)]

        self.fruit = {
            self.X_KEY: random.choice(sample),
            self.Y_KEY: random.choice(sample)
        }
        if self.fruit in self.snake_body:
            self._generate_fruit()

    def _get_initial_snake_body(self) -> List[Dict]:
        middle_field_idx = int(self.interface.field_size // 2)
        return [{self.X_KEY: middle_field_idx - i, self.Y_KEY: middle_field_idx} for i in range(3)]

    @property
    def _max_score(self) -> int:
        if os.path.exists(self.SCORE_FILE):
            with open(self.SCORE_FILE) as file:
                score = file.readline()
            return int(score)
        else:
            return 0

    @_max_score.setter
    def _max_score(self, value):
        with open(self.SCORE_FILE, 'w') as file:
            file.write(str(value))


if __name__ == '__main__':
    SnakeGame().launch_game()
