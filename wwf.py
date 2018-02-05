from collections import Counter
from Board import Board
from itertools import combinations
# from trie import Trie
from trie import my_trie, LETTERS
from functools import reduce
from operator import mul

def subanagram(str1, str2, wc):
    str2 = str2.replace('.', '')
    str1_counter, str2_counter = Counter(str1), Counter(str2)
    total = sum(str1_counter[char] - str2_counter[char]
                for char in str1_counter
                if str1_counter[char] - str2_counter[char] > 0)
    if total > wc:
        return False
    else:
        return True


def first_round(wc, rack_counter):
    words = [word for word in all_words if subanagram(word, rack, wc)]
    words_with_wc = [[(word, ch)
                      for ch in word if word.count(ch) > rack_wc.count(ch)]
                     for word in words]
    words_with_wc = [item for sublist in words_with_wc for item in sublist]
    words = replace_wc(words, words_with_wc, wc)

    w_n_p_4 = [(word, sum(LETTERS[letter][1]
               for i, letter in enumerate(word)
               if i < len(word) - 1
               and word[i + 1] != '.'))
               for word in words if len(word) <= 4]

    w_n_p_5_6 = [(word, sum(LETTERS[letter][1]
                 for i, letter in enumerate(word)
                 if i < len(word) - 1
                 and word[i + 1] != '.')) * 2
                 for word in words if len(word) in (5, 6)]

    w_n_p_7 = [(word, sum(LETTERS[letter][1]
               for i, letter in enumerate(word)
               if i < len(word) - 1 and word[i + 1] != '.') * 2 + 35)
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


def score(entry):
    word = entry[0]
    dot_places = [i for i, letter in list(enumerate(word))[:len(word) - 1]
                  if word[i + 1] == '.']
    blank_places = [i - j for j, i in enumerate(dot_places)]
    word = word.replace('.', '')
    if entry[1] == 'Vertical':
        x = entry[3]
        y = entry[2]
    else:
        x = entry[2]
        y = entry[3]

    sq_list = [board.get_square(x + i, y) for i in range(0, len(word))]
    old_lms = []
    for i in blank_places:
        old_lms.append(sq_list[i].lm)
        sq_list[i].lm = 0
    # print(''.join([sq.value for sq in sq_list]), word)
    # print(word, entry[1], entry[2], entry[3])
    hm = reduce(mul, [sq.wm for sq in sq_list], 1)
    # print(hm)
    cross_score = sum([sq.wm *
                       (sq.cross_score + LETTERS[word[sq.x - x]][1] * sq.lm)
                       for sq in sq_list if sq.empty and sq.cross_score > 0])
    # print(cross_score)
    hori_score = hm * sum([LETTERS[word[sq.x - x]][1] * sq.lm
                           for sq in sq_list])
    # print(hori_score)
    emptys = sum(1 for sq in sq_list if sq.empty)
    # print(emptys)
    score = cross_score + hori_score
    if emptys == 7:
        print('BINGO:', word, entry[1], entry[2], entry[3])
        score += 35
    for j, i in enumerate(blank_places):
        sq = sq_list[i]
        sq.lm = old_lms[j]
    return score


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
# rack = 'eetnboi'
board.display()
rack = input('rack e.g. abcdefg :').lower()
wc = rack.count('.')
rack_wc = rack.replace('.', '')
rack_counter = Counter(rack_wc)
if go_first:
    first_round(wc, rack_counter)
    placed = input('placed e.g. \'word\', True, 1, 2: ')
    eval('board.place({})'.format(placed))
    board.display()
    rack = input('rack e.g. abcdefg: ').lower()
    wc = rack.count('.')
    rack_wc = rack.replace('.', '')
    rack_counter = Counter(rack_wc)
    op_placed = input('opponent_placed e.g. \'word\', True, 1, 2: ')
    eval('board.place({})'.format(op_placed))
    board.display()
board.place('aahed', True, 2, 6, [5, ])
board.place('shiv', False, 4, 5, [])
board.place('almes', True, 1, 9, [])
board.place('mux', False, 3, 9, [])
board.place('ayin', True, 2, 7, [])
board.place('rex', True, 1, 11, [])
board.place('foetid', False, 6, 1, [])
board.place('before', True, 4, 1, [])
board.place('pinweed', True, 1, 3, [5])
board.place('zeps', False, 1, 1, [])
board.place('ikat', True, 5, 10, [])
board.place('golds', True, 7, 11, [])
board.display()

all_plays = set()

for sq in board.anchors:
    fla = sq.first_left_anchor()
    if fla is None:
        limit = sq.x - 1
    else:
        limit = sq.x - fla.x - 1
    sq.LeftPart('', my_trie.Root, limit, list(rack))
    for x in sq.legal_moves:
        if score(x) > 0:
            all_plays.add((score(x), x))

board.transpose()
board.display()
for sq in board.anchors:
    fla = sq.first_left_anchor()
    if fla is None:
        limit = sq.x - 1
    else:
        limit = sq.x - fla.x - 1
    sq.LeftPart('', my_trie.Root, limit, list(rack))
    for x in sq.legal_moves:
        my_score = score(x)
        if my_score > 0:
            all_plays.add((my_score, x))

all_plays = list(all_plays)
all_plays.sort(key=lambda x: x[0], reverse=True)
print('Top ten plays: ', all_plays)

best_play = all_plays[0]
print('\n', 'BEST PLAY:', best_play, '\n')
