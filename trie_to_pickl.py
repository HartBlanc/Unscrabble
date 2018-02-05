import pickle
from trie import Trie

with open('lexi.txt') as f:
    content = f.readlines()
    dicto = [x.strip() for x in content]

my_trie = Trie(dicto)
with open('lexi.pkl', "wb") as f:
    pickle.dump(my_trie, f, protocol=pickle.HIGHEST_PROTOCOL)
