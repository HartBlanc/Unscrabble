from trie_node import TrieNode

with open('dict.txt') as f:
    content = f.readlines()
    dicto = [x.strip() for x in content]

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


my_trie = Trie(dicto)
print(all([my_trie.contains(word) for word in dicto]))
