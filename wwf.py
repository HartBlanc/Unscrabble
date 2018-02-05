from Board import Board
from trie import my_trie, LETTERS
from functools import reduce
from operator import mul


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
print(board.transposed)
go_first = True
# rack = 'eetnboi'
board.display()
rack = input('rack e.g. abcdefg :').lower()
all_plays = set()
if go_first:
    center = board.get_square(6, 6)
    center.LeftPart('', my_trie.Root, 5, list(rack))
    for x in center.legal_moves:
        my_score = score(x)
        if my_score > 0:
            all_plays.add((my_score, x))
    board.transpose()
    center.LeftPart('', my_trie.Root, 5, list(rack))
    for x in center.legal_moves:
        my_score = score(x)
        if my_score > 0:
            all_plays.add((my_score, x))
    board.transpose()
    all_plays = list(all_plays)
    all_plays.sort(key=lambda x: x[0], reverse=True)
    print('Top ten plays: ', all_plays[0:10])

    best_play = all_plays[0]
    print('\n', 'BEST PLAY:', best_play, '\n')
    placed = input('placed e.g. \'word\', \'Vertical\', 1, 2: ')
while True:
    try:
        eval('board.place({})'.format(placed))
        break
    except:
        print('try again')
    board.display()
while True:
    try:
        op_placed = input('opponent_placed e.g. \'word\', \'Vertical\', 1, 2: ')
        eval('board.place({})'.format(op_placed))
        break
    except:
        print('try again')
    board.display()


# board.place('aahed', True, 2, 6, [5, ])
# board.place('shiv', False, 4, 5, [])
# board.place('almes', True, 1, 9, [])
# board.place('mux', False, 3, 9, [])
# board.place('ayin', True, 2, 7, [])
# board.place('rex', True, 1, 11, [])
# board.place('foetid', False, 6, 1, [])
# board.place('before', True, 4, 1, [])
# board.place('pinweed', True, 1, 3, [5])
# board.place('zeps', False, 1, 1, [])
# board.place('ikat', True, 5, 10, [])
# board.place('golds', True, 7, 11, [])
# board.display()
while True:
    all_plays = set()
    rack = input('rack e.g. abcdefg :').lower()
    print(board.transposed)
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
    print(board.transposed)
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
    board.transpose()
    all_plays = list(all_plays)
    all_plays.sort(key=lambda x: x[0], reverse=True)
    print('Top ten plays: ', all_plays[0:10])

    best_play = all_plays[0]
    print('\n', 'BEST PLAY:', best_play, '\n')
    while True:
        try:
            placed = input('placed e.g. \'word\', \'Vertical\' , 1, 2: ')
            eval('board.place({})'.format(placed))
            break
        except:
            print('try again')
    board.display()
while True:
    try:
        op_placed = input('opponent_placed e.g. \'word\', \'Vertical\', 1, 2: ')
        eval('board.place({})'.format(op_placed))
        break
    except:
        print('try again')
    board.display()
