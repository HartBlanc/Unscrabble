from Board import Board
from lexicon import lexicon, LETTERS
from functools import reduce
from operator import mul
from sys import argv


def score(entry, board):
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
    hm = reduce(mul, [sq.wm for sq in sq_list], 1)
    cross_score = sum([sq.wm *
                       (sq.cross_score + LETTERS[word[sq.x - x]][1] * sq.lm)
                       for sq in sq_list if sq.empty and sq.cross_score > 0])
    hori_score = hm * sum([LETTERS[word[sq.x - x]][1] * sq.lm
                           for sq in sq_list])
    emptys = sum(1 for sq in sq_list if sq.empty)
    score = cross_score + hori_score
    if emptys == 7:
        print('BINGO:', word, entry[1], entry[2], entry[3])
        score += 35
    for j, i in enumerate(blank_places):
        sq = sq_list[i]
        sq.lm = old_lms[j]
    return score


def legal_plays(board, rack, lexicon):
    def limit(anchor):
        fla = anchor.first_left_anchor()
        if fla is None:
            return anchor.x - 1
        else:
            return anchor.x - fla.x - 1

    def get_plays(all_plays):
        for sq in board.anchors:
            sq.LeftPart('', lexicon.Root, limit(sq), list(rack))
            for x in sq.legal_moves:
                m_score = score(x, board)
                if m_score > 0:
                    all_plays.add((m_score, x))
    all_plays = set()
    get_plays(all_plays)
    board.transpose()
    get_plays(all_plays)
    return sorted(all_plays, key=lambda x: x[0], reverse=True)


if __name__ == '__main__':

    board = Board()
    board.display()

    if len(argv) > 1 and argv[1] == 'first':
        rack = input('rack e.g. abcdefg :').lower()
        all_plays = legal_plays(board, rack, lexicon)
        board.transpose()
        print('Top ten plays: ', all_plays[0:10])
        print('\n', 'BEST PLAY:', all_plays[0:1], '\n')
        placed = input('placed e.g. \'word\', \'Vertical\', 1, 2: ')
        while True:
            try:
                eval('board.place({})'.format(placed))
                break
            except Exception:
                print('try again')
        board.display()

    while True:
        rack = input('rack e.g. abcdefg :').lower()
        while True:
            try:
                op_placed = input('opponent_placed e.g. \'word\', \'Vertical\', 1, 2: ')
                eval('board.place({})'.format(op_placed))
                break
            except Exception:
                print('try again')
        board.display()
        all_plays = legal_plays(board, rack, lexicon)
        board.transpose()
        print('Top ten plays: ', all_plays[0:10])
        print('\n', 'BEST PLAY:', all_plays[0:1], '\n')
        while True:
            try:
                placed = input('placed e.g. \'word\', \'Vertical\' , 1, 2: ')
                eval('board.place({})'.format(placed))
                break
            except Exception:
                print('try again')
        board.display()
