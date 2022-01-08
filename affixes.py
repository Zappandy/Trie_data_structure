#!/bin/bash

import pandas as pd
from trie import *


class SuffixScoring:
    def __init__(self, alpha, A, B, beta, trie_instance):
        self.affixTrie = trie_instance
        self.boundary = alpha + A
        self.affix = B + beta
        self.score = 0
        self.boundary_test_flag = False

    def freqBuilder(self):
        alpha_freq = self.affixTrie.getFrequency(self.boundary[:-1])
        alpha_a_freq = self.affixTrie.getFrequency(self.boundary)
        b_freq = self.affixTrie.getFrequency(self.boundary + self.affix[0])
        return alpha_a_freq, alpha_freq, b_freq 

    def boundaryTests(self):
        frequencies = self.freqBuilder()
        test_1 = self.boundaryTest_1(self.boundary)  # washington paper considers this for German and maybe Spanish as well
        test_2 = self.boundaryTest_2(frequencies[0], frequencies[1])
        test_3 = self.boundaryTest_3(frequencies[2], frequencies[0])
        if (test_1 and test_2 and test_3):
            self.score += 19
        else:
            self.score = -1
        return (self.boundary, self.affix), self.score

    def boundaryTest_1(self, stem):
        if self.affixTrie.hasWord(stem): 
            return True

    def boundaryTest_2(self, freq_1, freq_2):
        conditional_prob = self.conditionalProbability(freq_1, freq_2)
        if 0.9 <= conditional_prob <= 1:
            return True

    def boundaryTest_3(self, freq_1, freq_2):
        conditional_prob = self.conditionalProbability(freq_1, freq_2)
        if 0 <= conditional_prob < 1:  # probabilities can't be negative
            return True

    @staticmethod
    def conditionalProbability(freq_1, freq_2):
        if freq_2 == 0:
            return -1  # can't divide by 0. FIX
        #print(freq_1 / freq_2)
        return freq_1 / freq_2

class PrefixScoring(SuffixScoring):

    def __init__(self, alpha, A, B, beta, trie_instance):
        super().__init__(alpha, A, B, beta, trie_instance)
        self.affix = alpha + A
        self.boundary = B + beta

    def freqBuilder(self):
        a_freq = self.affixTrie.getFrequency(self.affix)
        beta_freq = self.affixTrie.getFrequency(self.affix + self.boundary)
        b_freq = self.affixTrie.getFrequency(self.affix + self.boundary[0])
        return beta_freq, b_freq, a_freq 

    def boundaryTests(self):
        frequencies = self.freqBuilder()
        test_1 = self.boundaryTest_1(self.boundary) 
        test_2 = self.boundaryTest_2(frequencies[0], frequencies[1])
        test_3 = self.boundaryTest_3(frequencies[0], frequencies[2])

        if (test_1 and test_2 and test_3):
            self.score += 19
        else:
            self.score = -1
        return (self.boundary, self.affix), self.score

 

