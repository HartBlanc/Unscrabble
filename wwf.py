import re
from collections import Counter
from Board import Board, LETTERS, all_words
from itertools import combinations
# import pickle
# from datetime import datetime

# def subanagram(str1, str2):
#     str1_counter, str2_counter = Counter(str1), Counter(str2)
#     return all(str1_counter[char] <= str2_counter[char]
#                  for char in str1_counter)


def subanagram(str1, wc, str2_counter):
    str1_counter = Counter(str1)
    counts = [str1_counter[char] - str2_counter[char]
              for char in str1_counter if str1_counter[char] - str2_counter[char] > 0]
    if sum(counts) > wc:
        return False
    else:
        return True


def letter_or_hand(word, size, line, hand):
    size = seg[1] - seg[0]
    start = seg[0]
    if len(word) > size:
        return False
    for i in range(size):
        if line[start + i] == '_' and word[i] not in hand:
            return False
        elif line[start + i] != '_' and word[i] != line[start + i]:
            return False
    return True


def add_adj(listy):
    combos = []
    if len(listy) == 1:
        return listy
    copy = list(listy)
    while True:
        combos = []
        for i, segment in enumerate(copy):
            if i > 0:
                combos.append((listy[i - 1][0], segment[1]))
        listy += combos
        copy = combos
        if len(combos) == 1:
            return listy


def get_chunk_lengths(listy):
    prev = listy[0]
    current = 1
    lengths = []
    for blank in listy[1:]:
        if prev == blank - 1:
            current += 1
        else:
            lengths.append(current)
            current = 1
        prev = blank
    lengths.append(current)
    return lengths


def get_segments(word):
    if word == '_' * 11:
        return [(0, 0)]
    sandwich = False
    start = 0
    segments = []
    for i, letter in enumerate(word):
        if letter != '_':
            first_end = i
            last_letter = i
            break
    end = first_end
    for i, letter in enumerate(word):
        if i <= first_end:
            continue
        if letter != '_':
            if not sandwich:
                end += 1
            last_letter = i
            if i == len(word) - 1:
                end = i
                segments.append((start, end))
        else:
            if i == len(word) - 1:
                end += 1
                segments.append((start, end))
                continue
            if word[i + 1] != '_':
                segments.append((start, end))
                if word[i - 1] != '_':
                    sandwich = True
                    start = last_letter + 2
                    end = start
                else:
                    start = last_letter + 2
                    end += 1
            else:
                end += 1
    return(add_adj(segments))


def first_letter(word):
    for i, letter in enumerate(word):
        if letter != '_':
            return i


def block(word):
    blocks = []
    block = word[0]
    prev_ = False
    if block == '_':
        prev_ = True
    for i, letter in enumerate(word):
        if i == 0:
            continue
        if prev_ and letter == '_':
            block += letter
        if prev_ and letter != '_':
            if len(word) == 2:
                block += letter
            blocks.append(block)
            block = letter
            if i == len(word) - 1:
                blocks.append(block)
            prev_ = False
            continue
        if not prev_ and letter == '_':
            blocks.append(block)
            block = letter
            if i == len(word) - 1:
                blocks.append(block)
            prev_ = True
            continue
        if not prev_ and letter != '_':
            block += letter
        if i == len(word) - 1:
            blocks.append(block)
    return blocks


def build_reg(seg_block):
    reg = ''
    for i, block in enumerate(seg_block):

        if i == 0:
            for letter in block:
                if letter != '_':
                    reg += letter
            continue
        elif block[0] == '_':
            reg += '{hand}' * len(block)
        else:
            reg += block

    while True:
        if reg[-6:] == '{hand}':
            reg = reg[:-6]
        else:
            break
    reg = '(?=' + reg + ')'
    return reg


def blank_counter(word):
    num = 0
    for letter in word:
        if letter == '_':
            num += 1
        else:
            return num


def rev_counter(word):
    num = 0
    for letter in word[::-1]:
        if letter == '_':
            num += 1
        else:
            return num


def get_score(word):
    score = 0
    for letter in word:
        value = LETTERS[letter][1]
        score += value
    return score


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

go_first = True

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

board.display()

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
