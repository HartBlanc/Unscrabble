from Square import Square, all_words
from operator import mul
from functools import reduce

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

    def direction_relations(self):
        for sq in self.squares:
            sq.left = self.get_square(sq.x - 1, sq.y)
            sq.right = self.get_square(sq.x + 1, sq.y)
            sq.above = self.get_square(sq.x, sq.y - 1)
            sq.below = self.get_square(sq.x, sq.y + 1)
            sq.adjacent = (sq.right, sq.left, sq.above, sq.below)
            sq.real_adjacent = tuple(filter(lambda x: x is not None, sq.adjacent))
            sq.get_cross_set()

    def get_anchors(self):
        potential_anchors = [sq for sq in self.squares
                                  if sq.empty
                                  and any((not adj.empty for adj in sq.real_adjacent))
                            ]
        print([(sq.x, sq.y) for sq in potential_anchors])
        rows = [[sq for sq in potential_anchors if sq.y == i] for i in range(1, self.N + 1)]
        anchors = [min(row, key=lambda sq: sq.x, default=None) for row in rows]
        anchors = [sq for sq in anchors if sq is not None]
        print(anchors)
        return anchors

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
        listy = place_split(word)
        if horizontal:
            for i, letter in enumerate(listy):
                sq = self.get_square(x + i, y)
                if sq.empty:
                    sq.value = letter
                    sq.empty = False
                    sq.wm = 1
                    sq.lm = sq.letter_multiplier()
                    for adj in sq.real_adjacents:
                        adj.get_cross_set()

        else:
            for i, letter in enumerate(listy):
                sq = self.get_square(x, y + i)
                if sq.empty:
                    sq.value = letter
                    sq.empty = False
                    sq.wm = 1
                    sq.lm = sq.letter_multiplier()
                    for adj in sq.real_adjacents:
                        adj.get_cross_set()

        self.build_lines()

    def display(self):
        print('***********')
        for line in self.lines:
            print(line)
        print('***********')

    def trial_place(self, word, horizontal, x, y):
        # print(word, horizontal, x, y)
        score = 0
        word = place_split(word)
        first_square = self.get_square(x, y)

        square = first_square
        if horizontal:
            sq_list = [self.get_square(square.x + i, square.y) for i in range(0, len(word))]
            emptys = sum(1 for sq in sq_list if sq.empty)
            wm = reduce(mul, [sq.wm for sq in sq_list], 1)
            lms = [sq.lm for sq in sq_list]
            for i, letter in enumerate(word):
                if sq_list[i].empty:
                    part_score = square.trial_place(letter, horizontal)
                    if part_score is None:
                        return False
                    else:
                        score += part_score
                square = square.right
            horizontal_score = wm * sum([LETTERS[letter[-1]][1] * lms[i] for i, letter in enumerate(word)])
            score += horizontal_score
        else:
            sq_list = [self.get_square(square.x, square.y + i) for i in range(0, len(word))]
            emptys = sum(1 for sq in sq_list if sq.empty)
            wm = reduce(mul, [sq.wm for sq in sq_list], 1)
            lms = [sq.lm for sq in sq_list]
            for letter in word:
                value = square.trial_place(letter, horizontal)
                if value is None:
                    return False
                else:
                    score += value
                    square = square.below
            vertical_score = wm * sum([LETTERS[letter[-1]][1] * lms[i] for i, letter in enumerate(word)])
            score += vertical_score
        if emptys == 7:
            score += 35
        word = ''.join([item for sublist in word for item in sublist])
        # print(word, horizontal, x, y, score)
        return (word, horizontal, x, y, score)

    def get_antisegments(self, place, horizontal):
        # antisegment: 'range of line that can be played on without touching any other letter in line'
        # span is any range that contains at least one element from
        # the range of words on the adjacent lines
        # get occupied squares above and below
        # generate all spans and remove those which do not contain any of the above or below
        if horizontal:
            first = self.get_square(1, place)
            above_range = []
            if place != 1:
                above = first.above
                current = above
                for i in range(0, self.N):
                    if i == self.N - 1 and not current.empty:
                            above_range.append(i + 1)
                            break
                    if not current.empty:
                        above_range.append(i + 1)
                    current = current.right
            below_range = []
            if place != self.N:
                current = first.below
                for i in range(0, self.N):
                    if i == self.N - 1 and not current.empty:
                            below_range.append(i + 1)
                            break
                    if not current.empty:
                        below_range.append(i + 1)
                    current = current.right
            mid_range = []
            current = first
            for i in range(0, self.N):
                if i == 0:
                    if current.empty and current.right.empty:
                        mid_range.append(i + 1)
                elif i == self.N - 1:
                    if current.empty and current.left.empty:
                        mid_range.append(i + 1)
                else:
                    if current.empty and current.left.empty and current.right.empty:
                        mid_range.append(i + 1)
                current = current.right
            spans = []
            if mid_range:
                start = mid_range[0]
                end = start
                for i, position in enumerate(mid_range):
                    if i == 0:
                        continue
                    if mid_range[i - 1] == position - 1:
                        end += 1
                    else:
                        spans.append((start, end))
                        start = position
                        end = start
                    if i == len(mid_range) - 1:
                        spans.append((start, end))

            # print(place, spans, horizontal, below_range, mid_range, above_range)
            spano = [list(range(x[0], x[1] + 1)) for x in spans]
            spana = set([item for sublist in spano for item in sublist])
            adjacent = set(below_range + above_range)
            antisegments = [AS for AS in flat_all_spans if not set(range(AS[0], AS[1] + 1)).isdisjoint(adjacent) and set(range(AS[0], AS[1] + 1)) <= spana]
            return antisegments

        else:
            first = self.get_square(place, 1)
            left_range = []
            if place != 1:
                left = first.left
                current = left
                for i in range(0, self.N):
                    if i == self.N - 1 and not current.empty:
                            left_range.append(i + 1)
                            break
                    if not current.empty:
                        left_range.append(i + 1)
                    current = current.below
            right_range = []
            if place != self.N:
                right = first.right
                current = right
                for i in range(0, self.N):
                    if i == self.N - 1 and not current.empty:
                            right_range.append(i + 1)
                            break
                    if not current.empty:
                        right_range.append(i + 1)
                    current = current.below
            mid_range = []
            current = first
            for i in range(0, self.N):
                if i == 0:
                    if current.empty and current.below.empty:
                        mid_range.append(i + 1)
                elif i == self.N - 1:
                    if current.empty and current.above.empty:
                        mid_range.append(i + 1)
                        break
                else:
                    if current.empty and current.above.empty and current.below.empty:
                        mid_range.append(i + 1)
                current = current.below
            spans = []
            if mid_range:
                start = mid_range[0]
                end = start
                for i, position in enumerate(mid_range):
                    if i == 0:
                        continue
                    if mid_range[i - 1] == position - 1:
                        end += 1
                    else:
                        spans.append((start, end))
                        start = position
                        end = start
                    if i == len(mid_range) - 1:
                        spans.append((start, end))
            # print(place, horizontal, left_range, mid_range, right_range)
            adjacent = set(left_range + right_range)
            spano = [list(range(x[0], x[1] + 1)) for x in spans]
            spana = set([item for sublist in spano for item in sublist])
            antisegments = [AS for AS in flat_all_spans if not set(range(AS[0], AS[1] + 1)).isdisjoint(adjacent) and set(range(AS[0], AS[1] + 1)) <= set(spana)]
            # print(antisegments)
            return antisegments


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
