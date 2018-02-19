from Square import Square
from itertools import chain
from colorama import Back, Style


class Board:

    wwf_board = [
                ['TL', '_', 'TW', '_', '_', '_', '_', '_', 'TW', '_', 'TL'],
                ['_', 'DW', '_', '_', '_', 'DW', '_', '_', '_', 'DW', '_'],
                ['TW', '_', 'TL', '_', 'DL', '_', 'DL', '_', 'TL', '_', '_'],
                ['_', '_', '_', 'TL', '_', '_', '_', 'TL', '_', '_', '_'],
                ['_', '_', 'DL', '_', '_', '_', '_', '_', 'DL', '_', '_'],
                ['_', 'DW', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
                ['_', '_', 'DL', '_', '_', '_', '_', '_', 'DL', '_', '_'],
                ['_', '_', '_', 'TL', '_', '_', '_', 'TL', '_', '_', '_'],
                ['TW', '_', 'TL', '_', 'DL', '_', 'DL', '_', 'TL', '_', 'TW'],
                ['_', 'DW', '_', '_', '_', 'DW', '_', '_', '_', 'DW', '_'],
                ['TL', '_', 'TW', '_', '_', '_', '_', '_', 'TW', '_', 'TL']
    ]

    def __init__(self, build_list=wwf_board):
        self.build_squares(build_list)
        self.direction_relations()
        self.transposed = False
        self.get_anchors()
        for sq in chain.from_iterable(self.squares):
            sq.get_cross_set()

    def __str__(self):
        str_board = [['|{}|'.format(sq.value) if len(sq.value) == 2
                        else '|__|' if sq.value == '_'
                        else '|{} |'.format(sq.value)
                       for sq in row]
                       for row in self.squares]
        str_board = [[Style.BRIGHT + Back.YELLOW + p_sq.upper() + Style.RESET_ALL
                        if p_sq[1].islower()
                        else p_sq
                        for p_sq in row]
                       for row in str_board]
        return '\n'+'\n\n'.join([' '.join(row) for row in str_board])+'\n'

    def transpose(self):
        for sq in chain.from_iterable(self.squares):
            old_x = sq.x
            sq.x = sq.y
            sq.y = old_x
            sq.legal_moves = set()
        self.squares = list(map(list, zip(*self.squares)))
        self.transposed = not self.transposed
        self.direction_relations()
        for sq in chain.from_iterable(self.squares):
            sq.get_cross_set()
        self.get_anchors()

    def direction_relations(self):
        for sq in chain.from_iterable(self.squares):
            sq.left = self.get_square(sq.x - 1, sq.y)
            sq.right = self.get_square(sq.x + 1, sq.y)
            sq.above = self.get_square(sq.x, sq.y - 1)
            sq.below = self.get_square(sq.x, sq.y + 1)
            sq.adjacent = (sq.right, sq.left, sq.above, sq.below)
            sq.real_adjacent = tuple(filter(lambda x: x is not None,
                                            sq.adjacent))

    def get_anchors(self):
        anchors = [sq for sq in chain.from_iterable(self.squares)
                   if sq.empty
                   and any(not adj.empty for adj in sq.real_adjacent)
                   ]
        # print([(sq.x, sq.y) for sq in anchors])
        self.anchors = anchors if anchors else [self.get_square(6, 6)]
        for sq in chain.from_iterable(self.squares):
            sq.anchor = True if sq in self.anchors else False


    def build_squares(self, build_list):
        self.squares = []
        for y, row in enumerate(build_list):
            sq_row = []
            for x, value in enumerate(row):
                sq_row.append(Square(value, x + 1, y + 1, self))
            self.squares.append(sq_row)

        self.N = y + 1

    def get_square(self, x_val, y_val):
        if (1 <= x_val <= self.N) and (1 <= y_val <= self.N):
            return self.squares[y_val - 1][x_val - 1]

    def place(self, word, horizontal, x, y):
        dot_places = (i for i, letter in enumerate(word)[:len(word) - 1]
                      if word[i + 1] == '.')
        blank_places = {i - j for j, i in enumerate(dot_places)}
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
                sq.value = letter + '.' if i in blank_places else letter
                sq.empty = False
                sq.wm = 1
                sq.lm = 0 if i in blank_places else 1
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
