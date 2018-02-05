from trie_node import TrieNode
import pickle


LETTERS = {
    '.': (2, 0), 'a': (9, 1), 'b': (2, 4), 'c': (2, 4), 'd': (5, 2),
    'e': (13, 1), 'f': (2, 4), 'g': (3, 3), 'h': (4, 3), 'i': (8, 1),
    'j': (1, 10), 'k': (1, 5), 'l': (4, 2), 'm': (2, 4), 'n': (5, 2),
    'o': (8, 1), 'p': (2, 4), 'q': (1, 10), 'r': (6, 1), 's': (5, 1),
    't': (7, 1), 'u': (4, 2), 'v': (2, 5), 'w': (2, 4), 'x': (1, 8),
    'y': (2, 3), 'z': (1, 10),
}

class Trie:
    def __init__(self, build_dict=None):
        self.Root = TrieNode('', False)
        if build_dict is not None:
            self.construct(build_dict)

    def insert(self, word):
        if self.contains(word):
            return
        else:
            Node = self.Root
            for char in word:
                if char in Node.next_nodes:
                    Node = Node.next_nodes[char]
                else:
                    Node.next_nodes[char] = TrieNode(Node.label + char, False)
                    Node = Node.next_nodes[char]
            Node.terminal = True

    def construct(self, build_dict):
        for word in build_dict:
            self.insert(word)

    def contains(self, word):
        Node = self.Root
        for char in word:
            if char in Node.next_nodes:
                Node = Node.next_nodes[char]
            else:
                return False
        if Node.terminal:
            return True
        else:
            return False

with open('lexi.pkl', "rb") as f:
    my_trie = pickle.load(f)

# with open('lexi.txt') as f:
#     content = f.readlines()
#     dicto = [x.strip() for x in content]
#
# my_trie = Trie(dicto)
#
# with open("lexi.pkl", "w") as f:
#     f.write(jsonpickle.encode(my_trie))
#
# with open("lexi.pkl", "r") as f:
#     my_trie = jsonpickle.decode(f.read())
#
# print(my_trie.contains('spooky'))
# string = jsonpickle.encode(obj)
#
# with open("lexi.p", "wb") as f:
#     pickle.dump(my_trie, f, protocol=pickle.HIGHEST_PROTOCOL)
