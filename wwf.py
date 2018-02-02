import re
from collections import Counter
from Board import Board, LETTERS, all_words
from itertools import combinations
from trie import my_trie
from functools import reduce
from operator import mul
# import pickle
# from datetime import datetime

# def subanagram(str1, str2):
#     str1_counter, str2_counter = Counter(str1), Counter(str2)
#     return all(str1_counter[char] <= str2_counter[char]
#                  for char in str1_counter)


def first_round(wc, hand_counter):
    words = [word for word in all_words if subanagram(word, wc, hand_counter)]
    words_with_wc = [[(word, ch) for ch in word if word.count(ch) > hand_wc.count(ch)] for word in words]
    words_with_wc = [item for sublist in words_with_wc for item in sublist]
    words = replace_wc(words, words_with_wc, wc)


    w_n_p_4 = [(word, sum(LETTERS[letter][1] for i, letter in enumerate(word) if i < len(word) - 1 and word[i+1] != '.' ))
               for word in words if len(word) <= 4]

    w_n_p_5_6 = [(word, sum(LETTERS[letter][1] for i, letter in enumerate(word) if i < len(word) - 1  and word[i+1] != '.' )) * 2
                 for word in words if len(word) in (5, 6)]

    w_n_p_7 = [(word, sum(LETTERS[letter][1] for i, letter in enumerate(word) if i < len(word) - 1 and word[i+1] != '.' ) * 2 + 35)
               for word in words if len(word) == 7]

    w_n_p = w_n_p_4 + w_n_p_5_6 + w_n_p_7

    w_n_p.sort(key=lambda x: x[1], reverse=True)

    print('Top 10 options', w_n_p[0:10])
    print('\n' + 'BEST OPTION: ', str(w_n_p[0]) + '\n')
    return w_n_p[0]


def replace_wc(listy_1, listy_2, wc):
    listy_2_words = [entry[0] for entry in listy_2]
    listy_1 = [word for word in listy_1 if word not in listy_2_words]
    for word, ch in listy_2:
        listy_word = list(word)
        for i, letter in enumerate(word):
            if letter == ch:
                listy_word[i] = ch + '.'
                listy_1.append(''.join(listy_word))
                listy_word[i] = ch
        if wc == 2 and len(positions) >= 2:
            positions_2 = combinations(positions, 2)
            for i, j in positions_2:
                word[i] = ch + '.'
                word[j] = ch + '.'
                listy_1.append(''.join(listy_word))
    return listy_1

# def replace_all(word, listy):
#     [i for i, letter in enumerate(s) if letter == ch]
#     for char in listy:
#         word = word.replace(char, char + '.')
#     return word


# add to collection when prev is not empty and current is empty
# or when row is finished
# print(possible_letters, reg, seg_word, first_letter(seg_word), seg[0],)
# hairsc hairs _hairs 1 0
# hairsc hairs _hairs_l 1 0

# with open('dict.txt') as f:
#     content = f.readlines()
#     all_words = [x.strip() for x in content]
# with open('all_words.pkl', 'rb') as f:
#     all_words = pickle.load(f)

# frequencies wrong


list_board = [
        ['TL', '_', 'TW', '_', '_', '_', '_', '_', 'TW', '_', 'TL'],
        ['_', 'DW', '_', '_', '_', 'DW', '_', '_', '_', 'DW', '_'],
        ['TW', '_', 'TL', '_', 'DL', '_', 'DL', '_', 'TL', '_', '_'],
        ['_', '_', '_', 'TL', '_', '_', '_', 'TL', '_', '_', '_'],
        ['_', '_', 'DL', '_', '_', '_', '_', '_', 'DL', '_', '_'],
        ['_', 'DW', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', 'DL', '_', '_', '_', '_', '_', 'DL', '_', '_'],
        ['_', '_', '_', 'TL', '_', '_', '_', 'TL', '_', '_', '_'],
        ['TW', '_', 'TL', '_', 'DL', '_', 'DL', '_', 'TL', '_', '_'],
        ['_', 'DW', '_', '_', '_', 'DW', '_', '_', '_', 'DW', '_'],
        ['TL', '_', 'TW', '_', '_', '_', '_', '_', 'TW', '_', 'TL']
]
board = Board(list_board)

go_first = False

# hand = 'eetnboi'
board.display()
hand = input('hand e.g. abcdefg :').lower()
wc = hand.count('.')
hand_wc = hand.replace('.', '')
hand_counter = Counter(hand_wc)
if go_first:
    first_round(wc, hand_counter)
    placed = input('placed e.g. \'word\', True, 1, 2: ')
    eval('board.place({})'.format(placed))
    board.display()
    hand = input('hand e.g. abcdefg: ').lower()
    wc = hand.count('.')
    hand_wc = hand.replace('.', '')
    hand_counter = Counter(hand_wc)
    op_placed = input('opponent_placed e.g. \'word\', True, 1, 2: ')
    eval('board.place({})'.format(op_placed))
    board.display()
# board.place('fraises', True, 2, 6)
# board.place('feaze', False, 2, 6)
# board.place('doxies', True, 2, 11)
# board.place('chukars', False, 3, 1)
# board.place('izar', True, 1, 9)
# board.place('joule', True, 1, 3)
# board.place('thebe.', True, 2, 2)
# board.place('divan', True, 6, 10)
board.place('cat', True, 6, 5)
board.display()

def score(entry):
    word = entry[0]
    x = entry[1]
    y = entry[2]
    sq_list = [board.get_square(x + i, y) for i in range(0, len(word))]
    hm = reduce(mul, [sq.wm for sq in sq_list], 1)
    cross_score = sum([sq.wm * (sq.cross_score + LETTERS[word[sq.x - x - 1]][1] * sq.lm) for sq in sq_list if sq.empty])
    hori_score = hm * sum([LETTERS[word[sq.x - x - 1]][1] * sq.lm for sq in sq_list])
    emptys = sum(1 for sq in sq_list if sq.empty)
    score = cross_score + hori_score
    if emptys == 7:
        print('BINGO')
        score += 35
    return score

all_plays = []
anchors = board.get_anchors()
for sq in board.get_anchors():
    sq.LeftPart('', my_trie.Root, sq.x - 1, set(hand))
    for x in sq.legal_moves:
        if score(x) > 0:
            all_plays.append((score(x), True, x))


all_plays.sort(key=lambda x: x[0], reverse=True)
print('Top ten plays: ', all_plays[0:10])

best_play = all_plays[0]
print('\n', 'BEST PLAY:', best_play, '\n')

while True:
    combos = [[word for word in all_words if subanagram(word, wc, hand_counter) and len(word) == i] for i in range(2, 12)]

    if wc > 0:
        new_combos = []
        for combo in combos:
            words_with_wc = [[(word, ch) for ch in word if word.count(ch) > hand_wc.count(ch)] for word in combo]
            words_with_wc = [item for sublist in words_with_wc for item in sublist]
            new_combos.append(replace_wc(combo, words_with_wc, wc))
        combos = new_combos
        # print(combos)

    rows = board.lines
    columns = [''.join([place_split(row)[i] for row in rows]) for i in range(0, 11)]
    # print(rows)
    # print(columns)
    hori_words = []
    for row, line in enumerate(rows):
        line = line.replace('.', '')
        blank = False
        if line == '_' * 11:
            blank = True
        if row == len(rows) - 1:
            if line == rows[row - 1] and blank:
                continue
        elif row == 0:
            if line == rows[row + 1] and blank:
                continue
        else:
            if line == rows[row - 1] == rows[row + 1] and blank:
                continue
        row = row + 1
        print('row', row)
        segments = get_segments(line)
        antisegments = board.get_antisegments(row, True)
        block_dicto = {}

        prev_size = 0
        hand_wc = hand.replace('.', '')
        hand_counter = Counter(hand_wc)
        for antisegment in antisegments:
            size = antisegment[1] - antisegment[0] + 1
            anti_words = [(word, row, antisegment[0]) for word in combos[size - 2]]
            hori_words += anti_words

        for seg in segments:
            if blank:
                continue
            size = seg[1] - seg[0]
            seg_word = line[seg[0]:seg[1] + 1]
            # print(seg_word)
            block_dicto[seg] = block(line[seg[0]:seg[1] + 1])
            block_words = [x.replace('_', '') for x in block_dicto[seg] if not x == len(x) * '_']
            my_hand = '[{}]'.format(hand)
            reg = build_reg(block_dicto[seg])
            in_word_letters = ''.join(block_dicto[seg]).replace('_', '')
            possible_letters = in_word_letters + hand
            reg = reg.format(hand=my_hand)
            blanks = blank_counter(line)
            rev_blanks = rev_counter(line)
            possi_wc = possible_letters.replace('.', '')
            poss_counter = Counter(possi_wc)
            # print('dict time' ,datetime.now())
            # print(line, block_dicto[seg], seg_word, reg)
            match_words = [word for word in all_words if subanagram(word, wc, poss_counter) and re.search(reg, word) and word not in block_words]
            if wc > 0:
                words_with_wc = [[(word, ch) for ch in word if word.count(ch) > possi_wc.count(ch)] for word in match_words]
                words_with_wc = [item for sublist in words_with_wc for item in sublist]
                match_words = replace_wc(match_words, words_with_wc, wc)

            # print('match_words', len(match_words))
            matches = []
            for word in match_words:
                for match in re.finditer(reg, word.replace('.', '')):
                    matches.append((word, match.start(), match.end()))
            # print('matches', len(matches))
            fit_words = [(word, row, first_letter(seg_word) - start + seg[0] + 1) for word, start, end in matches if blanks >= start and rev_blanks >= len(word) - end]
            # print('fit_words', len(fit_words))
            hori_words += fit_words

    # print('vert')
    verti_words = []
    for column, line in enumerate(columns):
        line = line.replace('.', '')
        if line == '_' * 11:
            blank = True
        if column == len(columns) - 1:
            if line == columns[column - 1] == '_' * 11:
                continue
        elif column == 0:
            if line == columns[column + 1] == '_' * 11:
                continue
        else:
            if line == columns[column - 1] == columns[column + 1] == '_' * 11:
                continue
        column = column + 1
        print('column', column)
        segments = get_segments(line)
        antisegments = board.get_antisegments(column, False)
        block_dicto = {}

        prev_size = 0
        hand_wc = hand.replace('.', '')
        hand_counter = Counter(hand_wc)
        for antisegment in antisegments:
            size = antisegment[1] - antisegment[0] + 1
            anti_words = [(word, column, antisegment[0]) for word in combos[size - 2]]
            verti_words += anti_words

        for seg in segments:
            if blank:
                continue
            size = seg[1] - seg[0]
            seg_word = line[seg[0]:seg[1] + 1]
            block_dicto[seg] = block(line[seg[0]:seg[1] + 1])
            block_words = [x.replace('_', '') for x in block_dicto[seg] if not x == len(x) * '_']
            my_hand = '[{}]'.format(hand)
            reg = build_reg(block_dicto[seg])
            in_word_letters = ''.join(block_dicto[seg]).replace('_', '')
            possible_letters = in_word_letters + hand
            # print('poss', possible_letters)
            reg = reg.format(hand=my_hand)
            blanks = blank_counter(line)
            rev_blanks = rev_counter(line)
            possi_wc = possible_letters.replace('.', '')
            poss_counter = Counter(possi_wc)
            # print('dict time' ,datetime.now())
            # print(line, block_dicto[seg], seg_word, reg)
            match_words_v = [word for word in all_words if subanagram(word, wc, poss_counter) and re.search(reg, word) and word not in block_words]
            if wc > 0:
                words_with_wc = [[(word, ch) for ch in word if word.count(ch) > possi_wc.count(ch)] for word in match_words_v]
                words_with_wc = [item for sublist in words_with_wc for item in sublist]
                match_words_v = replace_wc(match_words_v, words_with_wc, wc)

            # print('match_words_v', len(match_words_v))
            # print([subanagram(word, wc, poss_counter) for word in all_words])
            matches_v = []

            for word in match_words_v:
                for match in re.finditer(reg, word.replace('.', '')):
                    matches_v.append((word, match.start(), match.end()))
            # print('matches', len(matches_v))
            fit_words_v = [(word, column, first_letter(seg_word) - start + seg[0] + 1) for word, start, end in matches_v if blanks >= start and rev_blanks >= len(word) - end]
            # print('fit_words_v', len(fit_words_v))
            verti_words += fit_words_v

    vert_plays = [board.trial_place(word, False, column, start) for (word, column, start) in set(verti_words) if board.trial_place(word, False, column, start)]
    hori_plays = [board.trial_place(word, True, start, row) for (word, row, start) in set(hori_words) if board.trial_place(word, True, start, row)]
    all_plays = hori_plays + vert_plays
    all_plays.sort(key=lambda x: x[4], reverse=True)
    print('Top ten words: ', all_plays[0:10])

    best_play = all_plays[0]
    print('\n', 'BEST PLAY:', best_play, '\n')

    placed = input('placed \'word\', hori, x, y: ')
    eval('board.place({})'.format(placed))
    board.display()
    hand = input('hand: ').lower()
    wc = hand.count('.')
    hand_wc = hand.replace('.', '')
    hand_counter = Counter(hand_wc)
    op_placed = input('opponent_placed \'word\', hori, x, y: ')
    eval('board.place({})'.format(op_placed))
    board.display()

    # board.place(best_play[0], best_play[4], best_play[2], best_play[3])
    # board.display()
