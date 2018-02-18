
class TrieNode:
    def __init__(self, label, terminal):
        self.label = label
        self.terminal = terminal
        self.next_nodes = {}


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

    def delete(self, word):
        # NOT IN WORD
        if not self.contains(word):
            return
        else:
            t_node = self.Root
            d_node = None
            for char in word[:-1]:
                if t_node.terminal:
                    d_node = (t_node, char)
                t_node = t_node.next_nodes[char]
            if d_node is None:
                # DELETED WORD IS A UNIQUE KEY
                if len(t_node.next_nodes) == 0:
                    del self.Root.next_nodes[word[0]]
                # DELETED WORD IS A PREFIX
                else:
                    t_node.next_nodes[word[-1]].terminal = False
            # DELETED WORD HAS PREFIX
            else:
                del d_node[0].next_nodes[d_node[1]]
