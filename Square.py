# from Board import Board
from trie import my_trie

LETTERS = {
    '.': (2, 0), 'a': (9, 1), 'b': (2, 4), 'c': (2, 4), 'd': (5, 2),
    'e': (13, 1), 'f': (2, 4), 'g': (3, 3), 'h': (4, 3), 'i': (8, 1),
    'j': (1, 10), 'k': (1, 5), 'l': (4, 2), 'm': (2, 4), 'n': (5, 2),
    'o': (8, 1), 'p': (2, 4), 'q': (1, 10), 'r': (6, 1), 's': (5, 1),
    't': (7, 1), 'u': (4, 2), 'v': (2, 5), 'w': (2, 4), 'x': (1, 8),
    'y': (2, 3), 'z': (1, 10)
    # 'a.': (9, 0), 'b.': (2, 4), 'c.': (2, 4), 'd.': (5, 2),
    # 'e.': (13, 1), 'f.': (2, 4), 'g.': (3, 3), 'h.': (4, 3), 'i.': (8, 1),
    # 'j.': (1, 10), 'k.': (1, 5), 'l.': (4, 2), 'm.': (2, 4), 'n.': (5, 2),
    # 'o.': (8, 1), 'p.': (2, 4), 'q.': (1, 10), 'r.': (6, 1), 's.': (5, 1),
    # 't.': (7, 1), 'u.': (4, 2), 'v.': (2, 5), 'w.': (2, 4), 'x.': (1, 8),
    # 'y.': (2, 3), 'z.': (1, 10)
}

alphabet = 'abcdefghijklmnopqrstuvwxyz'

with open('dict.txt') as f:
    content = f.readlines()
    all_words = [x.strip() for x in content]


class Square:

    def __init__(self, value, x, y, board):
        self.value = value
        self.x = x
        self.y = y
        self.board = board
        self.empty = True
        self.wm = self.word_multiplier()
        self.lm = self.letter_multiplier()
        self.cross_set = set()
        self.left = None
        self.right = None
        self.above = None
        self.below = None
        self.adjacents = tuple()
        self.real_adjacents = tuple()
        self.legal_moves = set()

    def LeftPart(self, PartialWord, N, limit, hand):
        self.ExtendRight(PartialWord, N, self, hand, limit)
        if limit > 0:
            valid_chars = hand.intersection(self.cross_set)
            adj_nodes = N.next_nodes
            for char in set(adj_nodes.keys()).intersection(valid_chars):
                self.LeftPart(PartialWord + char, adj_nodes[char], limit - 1, hand - set(char))

    def ExtendRight(self, PartialWord, N, sq, hand, limit):
        adj_nodes = N.next_nodes
        if sq is None:
            return
        if sq.empty:
            if N.terminal:
                self.legal_moves.add((PartialWord, limit + 1, self.y))
            valid_chars = hand.intersection(self.cross_set)
            pruned = set(adj_nodes.keys()).intersection(valid_chars)
            for char in pruned:
                self.ExtendRight(PartialWord + char, adj_nodes[char], sq.right, hand - set(char), limit)
        else:
            char = sq.value
            if char in adj_nodes:
                ## hand stays the same
                self.ExtendRight(PartialWord + char, adj_nodes[char], sq.right, hand, limit)


    def word_multiplier(self):
        if self.value == 'TW':
                return 3
        elif self.value == 'DW':
            return 2
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
        right = current.right
        while True:
            if right is None or right.empty:
                return current
            else:
                current = right
                right = current.right

    def first_empty_left(self):
        current = self
        left = current.left
        while True:
            if left is None or left.empty:
                return current
            else:
                current = left
                left = current.left

    def first_empty_above(self):
        current = self
        above = current.above
        while True:
            if above is None or above.empty:
                return current
            else:
                current = above
                above = current.above

    def first_empty_below(self):
        current = self
        below = current.below
        while True:
            if below is None or below.empty:
                return current
            else:
                current = below
                below = current.below

    def get_cross_set(self):
        above = self.first_empty_above()
        below = self.first_empty_below()
        if above == below == self:
            self.cross_set = set(alphabet)
            self.cross_score = 0
            return
        min_y = above.y
        max_y = below.y
        sq_list_up = [self.board.get_square(self.x, y_val) for y_val in range(min_y, self.y)]
        prefix = ''.join([sq.value for sq in sq_list_up])
        sq_list_down = [self.board.get_square(self.x, y_val) for y_val in range(self.y + 1, max_y + 1)]
        suffix = ''.join([sq.value for sq in sq_list_down])
        word = '{}{}{}'
        self.cross_set = {char for char in alphabet if my_trie.contains(word.format(prefix, char, suffix))}
        self.cross_score = sum([LETTERS[letter][1] for letter in prefix + suffix])

    def get_placed_prefix(self):
        left = self.first_empty_left()
        min_x = left.x
        sq_list = [self.board.get_square(x_val, self.y) for x_val in range(min_x, self.x)]
        prefix = ''.join([sq.value for sq in sq_list])
        return prefix

    def get_placed_suffix(self):
        right = self.first_empty_right()
        max_x = right.x
        sq_list = [self.board.get_square(x_val, self.y) for x_val in range(self.x + 1, max_x + 1)]
        suffix = ''.join([sq.value for sq in sq_list])
        return suffix

    def trial_place(self, letter, horizontal):
        initial_value = self.value
        self.value = letter
        global all_words
        if horizontal:
            vert_list = self.vertical_range()
            if len(vert_list) > 1:
                word = ''.join([sq.value[0] for sq in vert_list])
                if word in all_words:
                    vert_score = self.wm * (sum([LETTERS[sq.value[-1]][1] for sq in vert_list]) + LETTERS[self.value[-1]][1] * (self.lm - 1))
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
                hori_score = self.wm * (sum([LETTERS[sq.value[-1]][1] for sq in hori_list]) + LETTERS[self.value[-1]][1] * (self.lm - 1))
                self.value = initial_value
                return hori_score
            else:
                self.value = initial_value
                return None
        else:
            self.value = initial_value
            return 0
