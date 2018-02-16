from Square import Square


class Board:
    def __init__(self, build_list):
        self.build_squares(build_list)
        self.build_lines()
        self.direction_relations()
        self.transposed = False
        self.get_anchors()
        for sq in self.squares:
            sq.get_cross_set()

    def transpose(self):
        for sq in self.squares:
            old_x = sq.x
            sq.x = sq.y
            sq.y = old_x
            sq.legal_moves = set()
        self.transposed = not self.transposed
        self.direction_relations()
        for sq in self.squares:
            sq.get_cross_set()
        self.build_lines()
        self.get_anchors()

    def direction_relations(self):
        for sq in self.squares:
            sq.left = self.get_square(sq.x - 1, sq.y)
            sq.right = self.get_square(sq.x + 1, sq.y)
            sq.above = self.get_square(sq.x, sq.y - 1)
            sq.below = self.get_square(sq.x, sq.y + 1)
            sq.adjacent = (sq.right, sq.left, sq.above, sq.below)
            sq.real_adjacent = tuple(filter(lambda x: x is not None,
                                            sq.adjacent))

    def get_anchors(self):
        anchors = [sq for sq in self.squares
                   if sq.empty
                   # and (sq.left is None or sq.left.empty)
                   and any(not adj.empty for adj in sq.real_adjacent)
                   ]
        # print([(sq.x, sq.y) for sq in anchors])
        self.anchors = anchors
        for sq in self.squares:
            sq.anchor = True if sq in self.anchors else False

    def build_lines(self):
        self.lines = []
        for y in range(1, self.N + 1):
            line = ''
            for x in range(1, self.N + 1):
                sq = self.get_square(x, y)
                if sq.empty:
                    line += '_'
                else:
                    line += sq.value
            self.lines.append(line)

    def build_squares(self, build_list):
        self.squares = []
        for y, row in enumerate(build_list):
            for x, value in enumerate(row):
                self.squares.append(Square(value, x + 1, y + 1, self))
        self.N = y + 1

    def get_square(self, x_val, y_val):
        square = [sq for sq in self.squares
                  if (sq.x, sq.y) == (x_val, y_val)]
        if square:
            return square[0]

    def place(self, word, horizontal, x, y):
        dot_places = [i for i, letter in list(enumerate(word))[:len(word) - 1] if word[i + 1] == '.']
        blank_places = [i - j for j, i in enumerate(dot_places)]
        word = word.replace('.', '')
        if horizontal == 'Vertical':
            horizontal = False
        else:
            horizontal = True
        if not horizontal:
            self.transpose()
            old_x = x
            x = y
            y = old_x
        for i, letter in enumerate(word):
            sq = self.get_square(x + i, y)
            if sq.empty:
                sq.value = letter
                sq.empty = False
                sq.wm = 1
                sq.lm = sq.letter_multiplier()
                if i in blank_places:
                    sq.lm = 0
                for adj in (sq.first_empty_above().above,
                            sq.first_empty_below().below):
                    if adj is not None:
                        adj.get_cross_set()
                if i == 0:
                    lefty = sq.first_empty_left().left
                    if lefty is not None:
                        lefty.get_cross_set()
                if i == len(word) - 1:
                    righty = sq.first_empty_right().right
                    if righty is not None:
                        righty.get_cross_set()
        if not horizontal:
            self.transpose()
        self.get_anchors()
        self.build_lines()

    def display(self):
        print('***********')
        for line in self.lines:
            print(line)
        print('***********')
