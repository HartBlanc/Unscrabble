import pickle
from sys import argv



LETTERS = {
    '.': (2, 0), 'a': (9, 1), 'b': (2, 4), 'c': (2, 4), 'd': (5, 2),
    'e': (13, 1), 'f': (2, 4), 'g': (3, 3), 'h': (4, 3), 'i': (8, 1),
    'j': (1, 10), 'k': (1, 5), 'l': (4, 2), 'm': (2, 4), 'n': (5, 2),
    'o': (8, 1), 'p': (2, 4), 'q': (1, 10), 'r': (6, 1), 's': (5, 1),
    't': (7, 1), 'u': (4, 2), 'v': (2, 5), 'w': (2, 4), 'x': (1, 8),
    'y': (2, 3), 'z': (1, 10),
}

if (len(argv) > 1 and argv[1] != 'build') or len(argv) <= 1:
    with open('lexi.pkl', "rb") as f:
        lexicon = pickle.load(f)

if __name__ == '__main__':
    if len(argv) > 1:
        if argv[1] == 'in':
            quotes = '\'{}\''
            for arg in argv[2:]:
                if lexicon.contains(arg):
                    print(quotes.format(arg), "in lexicon")
                else:
                    print(quotes.format(arg), "not in lexicon")

        elif argv[1] == 'build':
            from trie import Trie
            filename = argv[2]
            with open(filename) as f:
                content = f.readlines()
                all_words = [x.strip() for x in content if len(x) <= 11]
            lexicon = Trie(all_words)
            if all([lexicon.contains(word) for word in all_words]):
                print("Successfully constructed lexicon trie")
            else:
                print("Some words missing from lexicon trie")
            with open("lexi.pkl", "wb") as f:
                pickle.dump(lexicon, f, protocol=pickle.HIGHEST_PROTOCOL)

        elif argv[1] == 'del':
            for word in argv[2:]:
                lexicon.delete(word)
            if all([not lexicon.contains(word) for word in argv[2:]]):
                print("Successfully removed words from lexicon trie")
            else:
                print("Some words not deleted from lexicon trie")
            with open("lexi.pkl", "wb") as f:
                pickle.dump(lexicon, f, protocol=pickle.HIGHEST_PROTOCOL)

        elif argv[1] == 'add':
            for word in argv[2:]:
                lexicon.insert(word)
            if all([lexicon.contains(word) for word in argv[2:]]):
                print("Successfully added words to lexicon trie")
            else:
                print("Some words not added to lexicon trie")
            with open("lexi.pkl", "wb") as f:
                pickle.dump(lexicon, f, protocol=pickle.HIGHEST_PROTOCOL)
