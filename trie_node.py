class TrieNode:
    def __init__(self, label, terminal):
        self.label = label
        self.terminal = terminal
        self.next_nodes = {}
