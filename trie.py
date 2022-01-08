
from collections import defaultdict

class TrieDS:
    def __init__(self):
        print("I am the Root Node, I have no name")
        self.RootNode = TrieNode("")  # create an instance

    def addWord(self, word, frequency=0):
        if frequency == 0:
            print("No given frequency, initializing with 0")
        add_entry =  self.RootNode.addEntry(word, frequency)
        print(f"Adding {word} {add_entry}")
        return add_entry

    def hasWord(self, word):
        has_word = self.RootNode.hasWord(word)
        print(f"Checking for {word} {has_word}")
        return has_word

    def getFrequency(self, word):
        frequency = self.RootNode.getFrequency(word)
        return frequency

class TrieNode:

    def __init__(self, myCharName):
        self.endToken = False  
        self.char = myCharName
        self.ChildNodes = {} 
        self.frequency = 0  

    def getNodeChar(self):
        return self.char

    def getFrequency(self, substring):
        node = self
        for char in substring:
            if not node.getChildNode(char):
                break
            node = node.getChildNode(char)
        return node.frequency

    def getChildNode(self, childChar):
        for node in self.ChildNodes.values():
            if node.getNodeChar() == childChar:
                return self.ChildNodes[node.getNodeChar()]
        return None

    def addEntry(self, substring, freq):
        node = self
        for i, char in enumerate(substring):
            if not node.getChildNode(char):
                node.ChildNodes.setdefault(char, TrieNode(char))
            node = node.getChildNode(char)
            node.frequency += freq  
        node.endToken = True
        return node.endToken

    def hasWord(self, substring):
        node = self
        for char in substring:
            if not node.getChildNode(char):
                break
            node = node.getChildNode(char)
        return node.endToken

