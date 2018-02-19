import pickle
from sys import argv
from collections import Counter



LETTERS = {
    '.': (2, 0), 'a': (5, 1), 'b': (1, 4), 'c': (1, 4), 'd': (2, 2),
    'e': (7, 1), 'f': (1, 4), 'g': (1, 3), 'h': (1, 3), 'i': (4, 1),
    'j': (1, 10), 'k': (1, 5), 'l': (2, 2), 'm': (1, 4), 'n': (2, 2),
    'o': (4, 1), 'p': (1, 4), 'q': (1, 10), 'r': (2, 1), 's': (4, 1),
    't': (2, 1), 'u': (1, 2), 'v': (1, 5), 'w': (1, 4), 'x': (1, 8),
    'y': (1, 3), 'z': (1, 10)
}

def wildcards(word):
    Chars = Counter(word)
    return sum((Chars[char] - LETTERS[char][0] for char in word
                if Chars[char] > LETTERS[char][0]))


if (len(argv) > 1 and argv[1] != 'build') or len(argv) <= 1:
    with open('./resources/lexi.pkl', "rb") as f:
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
            with open('./resources/{}'.format(filename)) as f:
                content = f.readlines()
                all_words = (w.strip() for w in content)
                all_words = (w for w in all_words
                             if len(w) <= 11
                             and wildcards(w) <= LETTERS['.'][0]
                             )

            lexicon = Trie(all_words)
            if all([lexicon.contains(word) for word in all_words]):
                print("Successfully constructed lexicon trie")
            else:
                print("Some words missing from lexicon trie")
            with open("./resources/lexi.pkl", "wb") as f:
                pickle.dump(lexicon, f, protocol=pickle.HIGHEST_PROTOCOL)

        elif argv[1] == 'del':
            for word in argv[2:]:
                lexicon.delete(word)
            if all([not lexicon.contains(word) for word in argv[2:]]):
                print("Successfully removed words from lexicon trie")
            else:
                print("Some words not deleted from lexicon trie")
            with open("./resources/lexi.pkl", "wb") as f:
                pickle.dump(lexicon, f, protocol=pickle.HIGHEST_PROTOCOL)

        elif argv[1] == 'add':
            for word in argv[2:]:
                lexicon.insert(word)
            if all([lexicon.contains(word) for word in argv[2:]]):
                print("Successfully added words to lexicon trie")
            else:
                print("Some words not added to lexicon trie")
            with open("./resources/lexi.pkl", "wb") as f:
                pickle.dump(lexicon, f, protocol=pickle.HIGHEST_PROTOCOL)
