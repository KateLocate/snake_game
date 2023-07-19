# In order for game to exist we need:
# - controllers for person
# - operations for the snake to perform
# - snake state
# - visual representation of the field and the snake

class SnakeGame:
    FRUIT_CELL = ' @ '
    FIELD_CELL = ' + '
    SNAKE_BODY_PART = ' . '

    def __init__(self, field_size):
        self.field_size = field_size
        self.fruit = None
        self.field = []

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
        self.fruit = {
            'coordinate_x': random.choice([i for i in range(self.field_size)]),
            'coordinate_y': random.choice([i for i in range(self.field_size)])
        }

    def add_fruit_to_the_field(self):
        if not self.fruit:
            self.generate_fruit_pos()
        if not self.field:
            self.generate_square_field()
        self.field[self.fruit['coordinate_y']][self.fruit['coordinate_x']] = self.FRUIT_CELL

    def operate_snake_body(self):
        ...


if __name__ == '__main__':
    snake = SnakeGame(10)
    snake.add_fruit_to_the_field()
    snake.draw_game_field()

