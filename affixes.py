import pandas as pd
from trie import *


ranked_suffixes = dict()  # initialized as global variables
ranked_prefixes = dict()  # initialized as global variables

class SuffixScoring:
    def __init__(self, stem, suffix, trie_instance):
        """
        A scoring class initialized with a stem (alphaA), a suffix (Bbeta), and
        a TrieDS (trie dictionary) instance that should have already been populated
        """
        self.suffixTrie = trie_instance
        self.stem = stem
        self.suffix = suffix

    def freqBuilder(self):

        """
        Builds alpha frequency, alphaA frequency and b frequency from stem and suffix
        returns ints. The frequencies corresponding to strings, alpha, alphaA, and alphaAB.
        """
        alpha_freq = self.suffixTrie.getFrequency(self.stem[:-1])
        alpha_a_freq = self.suffixTrie.getFrequency(self.stem)
        b_freq = self.suffixTrie.getFrequency(self.stem + self.suffix[0])
        return alpha_a_freq, alpha_freq, b_freq 

    def boundaryTests(self):
        """
        Calls self.freqBuilder to feed ints to the boundary tests and mutate the initialized
        score value
        returns: an int. The score of the suffix
        """
        frequencies = self.freqBuilder()
        score = 0
        if self.boundaryTest_2(frequencies[0], frequencies[1]) and self.boundaryTest_3(frequencies[2], frequencies[0]):
            score += 19
        else:
            score = -1
        return score


    def boundaryTest_2(self, freq_1, freq_2):
        """
        freq_1: alphaA's frequency int value
        freq_2: alpha's frequency int value
        returns: True if resulting conditional probability is between 0.9 and 1
        """
        conditional_prob = self.conditionalProbability(freq_1, freq_2)  # conditional operation
        if 0.9 <= conditional_prob <= 1:
            return True

    def boundaryTest_3(self, freq_1, freq_2):
        """
        freq_1: alphaAB's frequency int value
        freq_2: alphaA's frequency int value
        returns: True if resulting conditional probability is less than 1
        """
        conditional_prob = self.conditionalProbability(freq_1, freq_2)
        if 0 <= conditional_prob < 1:  # probabilities can't be negative
            return True

    @staticmethod
    def conditionalProbability(freq_1, freq_2):
        """
        static method to perform conditionalProbability operation. 
        For this problem it's a simple division
        freq_1: a substring's frequency int value
        freq_2: a substring's frequency int value
        returns: float value resulting from the division operation
        """
        if freq_2 == 0:  # added condition to deal ZeroDivisionErrors
            return -1 
        return freq_1 / freq_2

class PrefixScoring(SuffixScoring):

    def __init__(self, prefix, stem, trie_instance):

        """
        A scoring prefix class initialized with a prefix (alphaA), a stem (Bbeta), and
        a TrieDS (trie dictionary) instance that should have already been populated.
        Inherits all behaviors from SuffixScoring, except that the frequency values
        have to be fetched from different sliced strings.
        """
        self.prefixTrie = trie_instance
        self.prefix = prefix
        self.stem = stem

    def freqBuilder(self):
        a_freq = self.prefixTrie.getFrequency(self.prefix)
        beta_freq = self.prefixTrie.getFrequency(self.prefix + self.stem)
        b_freq = self.prefixTrie.getFrequency(self.prefix + self.stem[0])
        return beta_freq, b_freq, a_freq 

    def boundaryTests(self):
        score = 0
        frequencies = self.freqBuilder()
        test_2 = self.boundaryTest_2(frequencies[0], frequencies[1])
        test_3 = self.boundaryTest_3(frequencies[0], frequencies[2])

        if test_2 and test_3:
            score += 19
        else:
            score = -1
        return score


def affixBuilder(trie_strc, word):
    """
    trie_strct: populated TrieDS object
    word: string to be sliced to score its affixes
    returns None, but populates global dictionaries
    """
    for i, char in enumerate(word):  # for 2 char words there won't be any freqs added
        if i < (len(word) - 1):
            stem = prefix = word[:i+1]
            suffix = leaf = word[i+1:]
            ranked_suffixes.setdefault(suffix, 0)  # to avoid overwriting existing affixes
            if not trie_strc.hasWord(stem):  # Test 1
                ranked_suffixes[suffix] -= 1
            else:
                suffix_testing = SuffixScoring(stem, suffix, trie_strc)
                ranked_suffixes[suffix] += suffix_testing.boundaryTests()

            # same as above, but computing prefixes instead
            ranked_prefixes.setdefault(prefix, 0)
            if not trie_strc.hasWord(leaf):
                ranked_prefixes[prefix] -= 1
            else:
                prefix_testing = PrefixScoring(prefix, leaf, trie_strc)
                ranked_prefixes[prefix] += prefix_testing.boundaryTests()


def rank_affixes(ranked_affixes):
    """
    ranked_affixes: A dictionary with populated affixes and their respective scores
    returns: a list wherein negative values have been removed and the affixes 
    have been sorted by the sort_affixes function
    """
    affixes = ranked_affixes.items()
    # 0 in affix is the key and 1 the value
    return sort_affixes(dict(filter(lambda affix: affix[1] > 0, affixes)))

def sort_affixes(ranked_affixes):
    """
    ranked_affixes: A dictionary with populated affixes and no negative scores
    returns: a sorted list where the leading values are the highest scores
    """

    return sorted(ranked_affixes.keys(), key=ranked_affixes.get, reverse=True)

def top_affixes(ranked_affixes, percentage):
    """
    ranked_affixes: A list to be sliced 
    percentage: a float from 0 to 1 representing the percentage of affixes we want to fetch
    returns: top affixes based on percentage fed. If percentage == 0.4, then
    40% of leading affixes will be returned. 
    """
    return ranked_affixes[:round(percentage * len(ranked_affixes)) + 1]

ranked_suffixes = rank_affixes(ranked_suffixes)
ranked_prefixes = rank_affixes(ranked_prefixes)

top_suffixes = top_affixes(ranked_suffixes, 0.4)
top_prefixes = top_affixes(ranked_prefixes, 0.4)
