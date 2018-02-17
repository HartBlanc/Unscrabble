from lexicon import lexicon, LETTERS
import pickle
alphabet = 'abcdefghijklmnopqrstuvwxyz'


class Square:

    def __init__(self, value, x, y, board):
        self.value = value
        self.x = x
        self.y = y
        self.board = board
        self.empty = True if value in ('TW', '_', 'TL', 'DL', 'DW', 'CE') else False
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
        self.anchor = False


    def first_left_anchor(self):
        current = self
        left = current.left
        while True:
            if left is None:
                return None
            elif left.anchor:
                return left
            else:
                current = left
                left = current.left

    def LeftPart(self, PartialWord, N, limit, rack):
        adj_nodes = N.next_nodes
        if self.left is not None and not self.left.empty:
            prefix = self.get_placed_prefix()
            try:
                for char in prefix:
                    N = adj_nodes[char]
                    adj_nodes = N.next_nodes
            except KeyError:
                lexicon.insert(prefix)
                with open("lexi.pkl", "wb") as f:
                    pickle.dump(lexicon, f, protocol=pickle.HIGHEST_PROTOCOL)
                with open('wwf.txt', 'a') as f:
                    f.write(prefix + '\n')
                print('INSERTED:', prefix)
                N = lexicon.Root
                adj_nodes = N.next_nodes
                for char in prefix:
                    N = adj_nodes[char]
                    adj_nodes = N.next_nodes
            self.ExtendRight(prefix, N, self, len(prefix), rack)

            return
        self.ExtendRight(PartialWord, N, self, limit, rack)
        if limit > 0:
            # fla = self.first_left_anchor()
            # if fla is None:
            #     current = limit + 1
            # else:
            #     current = fla.x + limit
            for char in adj_nodes:
                if char in rack:
                    rack.remove(char)
                    self.LeftPart(PartialWord + char, adj_nodes[char],
                                  limit - 1, rack)
                    rack.append(char)
                elif '.' in rack:
                    rack.remove('.')
                    self.LeftPart(PartialWord + char + '.', adj_nodes[char],
                                  limit - 1, rack)
                    rack.append('.')

    def ExtendRight(self, PartialWord, N, sq, limit, rack):
        fla = self.first_left_anchor()
        if fla is None:
            start_x = limit + 1
        else:
            start_x = fla.x + limit + 1
        if self.left is not None and not self.left.empty:
            start_x = self.x - limit
        adj_nodes = N.next_nodes
        if sq is None:
            if N.terminal:
                if self.board.transposed:
                    # print(PartialWord, 'Vetical', self.y, start_x)
                    self.legal_moves.add((PartialWord, 'Vertical', self.y,
                                          start_x))
                else:
                    # print(PartialWord, self.x, self.y)
                    # print('yes', PartialWord, 'Horizontal', start_x, self.y)
                    self.legal_moves.add((PartialWord, 'Horizontal', start_x,
                                          self.y))
            return
        if sq.empty:
            if N.terminal and sq != self:
                if self.board.transposed:
                    # print(PartialWord, 'Vetical', self.y, start_x)
                    self.legal_moves.add((PartialWord, 'Vertical', self.y,
                                          start_x))
                else:
                    # print(PartialWord, self.x, self.y)
                    # print('yes', PartialWord, 'Horizontal', start_x, self.y)
                    self.legal_moves.add((PartialWord, 'Horizontal', start_x,
                                          self.y))
            for char in adj_nodes:
                # print(sq.cross_set, sq.x, sq.y)
                if char in rack and char in sq.cross_set:
                    rack.remove(char)
                    self.ExtendRight(PartialWord + char, adj_nodes[char],
                                     sq.right, limit, rack)
                    rack.append(char)
                elif '.' in rack and char in sq.cross_set:
                    rack.remove('.')
                    self.ExtendRight(PartialWord + char + '.', adj_nodes[char],
                                     sq.right, limit, rack)
                    rack.append('.')

        else:
            char = sq.value
            if char in adj_nodes:
                # rack stays the same
                self.ExtendRight(PartialWord + char, adj_nodes[char],
                                 sq.right, limit, rack)

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

    def first_empty_left(self):
        current = self
        left = current.left
        while True:
            if left is None or left.empty:
                return current
            else:
                current = left
                left = current.left

    def first_empty_right(self):
        current = self
        right = current.right
        while True:
            if right is None or right.empty:
                return current
            else:
                current = right
                right = current.right

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
        sq_list_up = [self.board.get_square(self.x, y_val)
                      for y_val in range(min_y, self.y)]
        prefix = ''.join([sq.value for sq in sq_list_up])
        prefix_score = sum([LETTERS[sq.value][1] * sq.lm
                            for sq in sq_list_up])
        sq_list_down = [self.board.get_square(self.x, y_val)
                        for y_val in range(self.y + 1, max_y + 1)]
        suffix = ''.join([sq.value for sq in sq_list_down])
        suffix_score = sum([LETTERS[sq.value][1] * sq.lm
                            for sq in sq_list_down])
        # print('gcs', 'pre:', prefix, 'suf:', suffix, self.x, self.y)
        word = '{}{}{}'
        self.cross_set = {char for char in alphabet
                          if lexicon.contains(
                              word.format(prefix, char, suffix)
                          )}
        # print('me', sq.x, sq.y, cross_set, prefix, suffix)
        self.cross_score = prefix_score + suffix_score

    def get_placed_prefix(self):
        left = self.first_empty_left()
        min_x = left.x
        sq_list = [self.board.get_square(x_val, self.y)
                   for x_val in range(min_x, self.x)]
        prefix = ''.join([sq.value for sq in sq_list])
        return prefix
