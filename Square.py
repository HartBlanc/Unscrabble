# from Board import Board

LETTERS = {
    'a': (9, 1), 'b': (2, 4), '.': (2, 0), 'c': (2, 4), 'd': (5, 2),
    'e': (13, 1), 'f': (2, 4), 'g': (3, 3), 'h': (4, 3), 'i': (8, 1),
    'j': (1, 10), 'k': (1, 5), 'l': (4, 2), 'm': (2, 4), 'n': (5, 2),
    'o': (8, 1), 'p': (2, 4), 'q': (1, 10), 'r': (6, 1), 's': (5, 1),
    't': (7, 1), 'u': (4, 2), 'v': (2, 5), 'w': (2, 4), 'x': (1, 8),
    'y': (2, 3), 'z': (1, 10),
    # 'a.': (9, 0), 'b.': (2, 4), 'c.': (2, 4), 'd.': (5, 2),
    # 'e.': (13, 1), 'f.': (2, 4), 'g.': (3, 3), 'h.': (4, 3), 'i.': (8, 1),
    # 'j.': (1, 10), 'k.': (1, 5), 'l.': (4, 2), 'm.': (2, 4), 'n.': (5, 2),
    # 'o.': (8, 1), 'p.': (2, 4), 'q.': (1, 10), 'r.': (6, 1), 's.': (5, 1),
    # 't.': (7, 1), 'u.': (4, 2), 'v.': (2, 5), 'w.': (2, 4), 'x.': (1, 8),
    # 'y.': (2, 3), 'z.': (1, 10)
}

with open('dict.txt') as f:
    content = f.readlines()
    all_words = [x.strip() for x in content]


class Square:

    def __init__(self, value, x, y, board):
        self.value = value
        self.x = x
        self.y = y
        self.board = board
        self.adjacent = (self.right(), self.left(), self.above(), self.below())

    def right(self):
        return self.board.get_square(self.x + 1, self.y)

    def left(self):
        return self.board.get_square(self.x - 1, self.y)

    def above(self):
        return self.board.get_square(self.x, self.y - 1)

    def below(self):
        return self.board.get_square(self.x, self.y + 1)

    def empty(self):
        if self.value in ('_', 'TL', 'DL', 'TW', 'DW'):
            return True
        else:
            return False

    def word_multiplier(self):
        if self.empty():
            if self.value == 'TW':
                return 3
            elif self.value == 'DW':
                return 2
            else:
                return 1
        else:
            return 1

    def letter_multiplier(self):
        if self.value == 'TL':
                return 3
        elif self.value == 'DL':
                return 2
        elif self.value[-1] == '.':
                return 0
        else:
            return 1

    def first_empty_right(self):
        current = self
        right = current.right()
        while True:
            if right is None or right.empty():
                return current
            else:
                current = right
                right = current.right()

    def first_empty_left(self):
        current = self
        left = current.left()
        while True:
            if left is None or left.empty():
                return current
            else:
                current = left
                left = current.left()

    def first_empty_above(self):
        current = self
        above = current.above()
        while True:
            if above is None or above.empty():
                return current
            else:
                current = above
                above = current.above()

    def first_empty_below(self):
        current = self
        below = current.below()
        while True:
            if below is None or below.empty():
                return current
            else:
                current = below
                below = current.below()

    def vertical_range(self):
        above = self.first_empty_above()
        below = self.first_empty_below()
        max_y = below.y
        min_y = above.y
        vert_list = [self.board.get_square(self.x, y_val) for y_val in range(min_y, max_y + 1)]
        return vert_list

    def horizontal_range(self):
        right = self.first_empty_right()
        left = self.first_empty_left()
        max_x = right.x
        min_x = left.x
        hori_list = [self.board.get_square(x_val, self.y) for x_val in range(min_x, max_x + 1)]
        return hori_list

    def trial_place(self, letter, horizontal):
        initial_value = self.value
        wm = self.word_multiplier()
        lm = self.letter_multiplier()
        self.value = letter
        global all_words
        if horizontal:
            vert_list = self.vertical_range()
            if len(vert_list) > 1:
                word = ''.join([sq.value[0] for sq in vert_list])
                if word in all_words:
                    vert_score = wm * (sum([LETTERS[sq.value[-1]][1] for sq in vert_list]) + LETTERS[self.value[-1]][1] * (lm - 1))
                    self.value = initial_value
                    return vert_score
                else:
                    self.value = initial_value
                    return None
            else:
                self.value = initial_value
                return 0
        else:
            hori_list = self.horizontal_range()
        if len(hori_list) > 1:
            word = ''.join([sq.value[0] for sq in hori_list])
            if word in all_words:
                hori_score = wm * (sum([LETTERS[sq.value[-1]][1] for sq in hori_list]) + LETTERS[self.value[-1]][1] * (lm - 1))
                self.value = initial_value
                return hori_score
            else:
                self.value = initial_value
                return None
        else:
            self.value = initial_value
            return 0
