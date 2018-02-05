from trie_node import TrieNode


class Trie:
    def __init__(self, build_lexi=None):
        self.Root = TrieNode('', False)
        if build_lexi is not None:
            self.construct(build_lexi)

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

    def construct(self, build_lexi):
        for word in build_lexi:
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
