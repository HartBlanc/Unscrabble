import pickle
# from trie import Trie


LETTERS = {
    '.': (2, 0), 'a': (9, 1), 'b': (2, 4), 'c': (2, 4), 'd': (5, 2),
    'e': (13, 1), 'f': (2, 4), 'g': (3, 3), 'h': (4, 3), 'i': (8, 1),
    'j': (1, 10), 'k': (1, 5), 'l': (4, 2), 'm': (2, 4), 'n': (5, 2),
    'o': (8, 1), 'p': (2, 4), 'q': (1, 10), 'r': (6, 1), 's': (5, 1),
    't': (7, 1), 'u': (4, 2), 'v': (2, 5), 'w': (2, 4), 'x': (1, 8),
    'y': (2, 3), 'z': (1, 10),
}

# with open('enable.txt') as f:
#     content = f.readlines()
#     all_words = [x.strip() for x in content]
#
#
# length = [(word, len(word)) for word in all_words]
# length.sort(key=lambda x: x[1], reverse=True)
#
# print(length[0])
#
# lexi = [x for x in all_words if len(x) <= 11]

# my_trie = Trie(dicto)


# with open("lexi.pkl", "wb") as f:
#     pickle.dump(my_trie, f, protocol=pickle.HIGHEST_PROTOCOL)

with open('lexi.pkl', "rb") as f:
    my_trie = pickle.load(f)
