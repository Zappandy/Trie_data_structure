class TrieDS:
    def __init__(self):
        """
        self: TrieDS class initialized with an instance of a trie node.
        Root nodes are always empty strings and the first node of the trie strc.
        """
        print("I am the Root Node, I have no name")
        self.RootNode = TrieNode("")  # create an instance

    def addWord(self, word, frequency=0):
        """
        word: a string to be added to current trie node instance
        frequency: an int may be passed, but if it isn't then freq is initialized with 0
        returns: True after adding word
        """
        if frequency == 0:
            print("No given frequency, initializing with 0")
        add_entry =  self.RootNode.addEntry(word, frequency)
        #print(f"Adding {word} {add_entry}")  # for debugging/demo purposes
        return add_entry

    def hasWord(self, word):
        """
        word: a string that is sought out for in the trie
        returns: True if word in trie, otherwise False
        """
        has_word = self.RootNode.hasWord(word)
        #print(f"Checking for {word} {has_word}")  # for debugging/demo purposes
        return has_word

    def getFrequency(self, word):
        """
        word: a string that is bound to a specific frequency. 
        Subtrings have frequencies as well, regardless of the boolean value of hasWord
        returns: an int. The value in the string's frequency
        """
        frequency = self.RootNode.getFrequency(word)
        return frequency

class TrieNode:

    def __init__(self, myCharName):

        """
        self: TrieNode class initialized with the name of the char and 3 other attributes.
        """
        self.endToken = False  # True only when the node represents the end of the word
        self.char = myCharName # setting the name character of this node
        self.ChildNodes = {}  # dict with chars as keys and nodes as their respective values
        # this dict may only contain one char and node per run. Its node value contains its
        # children
        self.frequency = 0  # cumulative frequency initialized 

    def getNodeChar(self):
        """
        returns a node's character name
        """
        return self.char

    def getFrequency(self, substring):
        """
        substring: sliced string or complete word
        returns an int. A substring's frequency
        """
        node = self
        for char in substring:
            if not node.getChildNode(char):
                break
            node = node.getChildNode(char)
        return node.frequency

    def getChildNode(self, childChar):
        """
        childChar: a char used to find a node with the passed char name
        returns a trie node if we find a node with childChars. Otherwise None
        """
        for node in self.ChildNodes.values():
            if node.getNodeChar() == childChar:
                return self.ChildNodes[node.getNodeChar()]
        return None

    def addEntry(self, substring, freq):
        """
        substring: iterate over word to fetch each char
        check if char has a childNode, if there isn't a new one is created and stored
        as a child of corresponding char in childNodes.
        returns endToken which will be True after we reach the end of the string
        """
        node = self
        for i, char in enumerate(substring):
            if not node.getChildNode(char):
                node.ChildNodes.setdefault(char, TrieNode(char))
            node = node.getChildNode(char)
            node.frequency += freq  
        node.endToken = True
        return node.endToken

    def hasWord(self, substring):
        """
        substring: iterate over word to fetch each char
        check if char has a childNode, if there isn't a new one break out of the loop
        otherwise, getChildNode 
        returns endToken which will be True depending on the node's endToken value
        """
        node = self
        for char in substring:
            if not node.getChildNode(char):
                break
            node = node.getChildNode(char)
        return node.endToken

