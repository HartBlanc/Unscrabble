from Square import Square

LETTERS = {
    'a': (9, 1), 'b': (2, 4), '.': (2, 0), 'c': (2, 4), 'd': (5, 2),
    'e': (13, 1), 'f': (2, 4), 'g': (3, 3), 'h': (4, 3), 'i': (8, 1),
    'j': (1, 10), 'k': (1, 5), 'l': (4, 2), 'm': (2, 4), 'n': (5, 2),
    'o': (8, 1), 'p': (2, 4), 'q': (1, 10), 'r': (6, 1), 's': (5, 1),
    't': (7, 1), 'u': (4, 2), 'v': (2, 5), 'w': (2, 4), 'x': (1, 8),
    'y': (2, 3), 'z': (1, 10),
    # 'a.': (9, 1), 'b.': (2, 4), 'c.': (2, 4), 'd.': (5, 2),
    # 'e.': (13, 1), 'f.': (2, 4), 'g.': (3, 3), 'h.': (4, 3), 'i.': (8, 1),
    # 'j.': (1, 10), 'k.': (1, 5), 'l.': (4, 2), 'm.': (2, 4), 'n.': (5, 2),
    # 'o.': (8, 1), 'p.': (2, 4), 'q.': (1, 10), 'r.': (6, 1), 's.': (5, 1),
    # 't.': (7, 1), 'u.': (4, 2), 'v.': (2, 5), 'w.': (2, 4), 'x.': (1, 8),
    # 'y.': (2, 3), 'z.': (1, 10)
}

# all_spans = [[(i, n + i) for i in range(1, 12 - n)] for n in range(1, 11)]
# flat_all_spans = [item for sublist in all_spans for item in sublist]


class Board:
    def __init__(self, build_list):
        self.build_squares(build_list)
        self.build_lines()
        self.direction_relations()
        self.transposed = False
        self.anchors = []

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
        print([(sq.x, sq.y) for sq in anchors])
        self.anchors = anchors
        for sq in self.squares:
            # sq.anchor = True if sq in self.anchors else False
            if sq in self.anchors:
                sq.anchor = True
            else:
                sq.anchor = False

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

    def place(self, word, horizontal, x, y, wcs):
        listy = place_split(word)
        if not horizontal:
            self.transpose()
            old_x = x
            x = y
            y = old_x
        for i, letter in enumerate(listy):
            sq = self.get_square(x + i, y)
            if sq.empty:
                sq.value = letter
                sq.empty = False
                sq.wm = 1
                sq.lm = sq.letter_multiplier()
                if i + 1 in wcs:
                    sq.lm = 0
                for adj in (sq.first_empty_above().above, sq.first_empty_below().below):
                    if adj is not None:
                        adj.get_cross_set()
                if i == 0:
                    if sq.left is not None:
                        sq.left.get_cross_set()
                if i == len(listy) - 1:
                    if sq.right is not None:
                        sq.right.get_cross_set()
        if not horizontal:
            self.transpose()
        self.get_anchors()
        self.build_lines()

    def display(self):
        print('***********')
        for line in self.lines:
            print(line)
        print('***********')


def place_split(word):
    listy = []
    if '.' in word:
        for i, letter in enumerate(word):
            if letter == '.':
                continue
            if i < len(word) - 1:
                if word[i + 1] == '.':
                    letter += '.'
            listy.append(letter)
    else:
        listy = list(word)
    return listy
