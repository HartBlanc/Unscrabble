# 'The unique node with no outedges
# is given an index of zero by convention.'
print(55)
from trie_node import TrieNode

with open('dict.txt') as f:
    content = f.readlines()
    dicto = [x.strip() for x in content]

alphabet = 'abcdefghijklmnopqrstuvwxyz'


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
            Node.terminal = True



    def get_adjacents(self, current):
        adjacent = {}
        for char in alphabet:
            new_prefix = current.label + char
            if any((word.startswith(new_prefix) for word in build_dict)):
                terminal = True if new_prefix in build_dict else False
                if terminal:
                    print(new_prefix)
                adjacent[char]= TrieNode(new_prefix, terminal)
        for next_node in adjacent.values():
            next_node.next_nodes = self.get_adjacents(next_node)
        return adjacent

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
print(1)
my_trie = Trie(dicto)
print(2)
print(my_trie.contains('abcdefg'))
