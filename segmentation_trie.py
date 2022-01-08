#!/bin/bash
# grouping and labeling

import pandas as pd
import string
from trie import *
from affixes import *

#%% Testing system... 
#goodwords = ["report", "reporter", "reporters", "reported",
#             "reportable", "reportage", "reportages", "reporting"] 
#badwords = ["repo", "save", 't', "ejis", "rep"]
#MyTrie = TrieDS()
#print("----Adding Words to Trie----")
#for word in goodwords:
#    MyTrie.addWord(word)
#print("----Checking if all good words return True----")
#goodwords += ["tito"]
#for word in goodwords:
#    MyTrie.hasWord(word)
#    boundaryChecker(MyTrie, word)

#badwords += ["report"]
#print("----Checking if all bad words return False----")
#for word in badwords:
#    MyTrie.hasWord(word)

#%%

ranked_suffixes = dict()
ranked_prefixes = dict()
def affixBuilder(trie_strc, word):
    for i, char in enumerate(word):  # for 2 char words there won't be any freqs added
        if i < (len(word) - 1):
            suffix_testing = SuffixScoring(word[:i], word[i], word[i+1], word[i+2:], trie_strc)
            boundary_suffix, suffix_score = suffix_testing.boundaryTests()
            ranked_suffixes.setdefault(boundary_suffix, suffix_score)
            real_suffixes = [morpheme[1] for morpheme in ranked_suffixes.keys()]
            if boundary_suffix[1] in real_suffixes:
                ranked_suffixes[boundary_suffix] += suffix_score
            prefix_testing = PrefixScoring(word[:i], word[i], word[i+1], word[i+2:], trie_strc)
            boundary_prefix, prefix_score = prefix_testing.boundaryTests()
            ranked_prefixes.setdefault(boundary_prefix[::-1], prefix_score)
            real_prefixes = [morpheme[1] for morpheme in ranked_prefixes.keys()]
            if boundary_prefix[1] in real_prefixes:
                ranked_prefixes[boundary_prefix[::-1]] += prefix_score
#%%
def clean_corpus(file):
    df =  pd.read_csv(file, delimiter='\t')
    df.dropna(inplace=True)
    df = df[df["Freq"] > 201]  # mutates index, hence why .loc is better
    df.loc[:, "word"] = df["word"].str.lower()
    df = df[df["word"].apply(spanish_alphabet)]   
    df.drop_duplicates(subset=["word"], keep="first", inplace=True)
    #df = df[df["word"].str.len() > 1]  # ~df["word"] inverting mask, i.e. doing the opposte
    df.reset_index(drop=True, inplace=True)  # resetting index in case it was mutated
    return df

def spanish_alphabet(word):  # 2min
    alphabet = string.ascii_lowercase 
    special_chars = "wxqyz"
    fake_vowels = "áéíóúyüh"
    sp_alphabet = list(alphabet + "áéíóúñü")
    flag = True
    for i in range(len(word) - 1):
        if (word[i] not in sp_alphabet) or (word[i+1] not in sp_alphabet):
            flag = False
            break
        if (word[i] in special_chars) and (word[i+1] not in fake_vowels):
            flag = False
            break
    for i in range(len(word) - 5):
        cons = [word[i+j] for j in range(5) if word[i+j] not in fake_vowels + "aeiou"]
        if len(cons) == 5:
            flag = False
    return flag


#%%
spanish_corpus = clean_corpus("clean_spanish.txt")  
print(spanish_corpus)
raise SystemExit
MyTrie = TrieDS()
spanish_corpus.apply(lambda row: MyTrie.addWord(row["word"], row["Freq"]), axis=1)  # map may be faster
# two methods to append a row and show that elements are not in the trie
#test = test.append({"word": "tito", "Freq": 69}, ignore_index=True)
#data = pd.Series(data={"word": "tito", "Freq": 90}, name=test.shape[0])
#test = test.append(data, ignore_index=False)

spanish_corpus.apply(lambda row: MyTrie.hasWord(row["word"]), axis=1)
spanish_corpus.apply(lambda row: affixBuilder(MyTrie, row["word"]), axis=1)
# 0 in affix is the key and 1 the value
ranked_suffixes = dict(filter(lambda affix: affix[1] > 0, ranked_suffixes.items()))
ranked_prefixes = dict(filter(lambda affix: affix[1] > 0, ranked_prefixes.items()))

print(ranked_suffixes.keys())
print(ranked_prefixes.keys())
ranked_suffixes = sorted(ranked_suffixes.keys(), key=ranked_suffixes.get, reverse=True)
ranked_prefixes = sorted(ranked_prefixes.keys(), key=ranked_prefixes.get, reverse=True)
#print(bool(ranked_suffixes))
#print(bool(ranked_prefixes))

# https://albertauyeung.github.io/2020/06/15/python-trie.html/
# https://www.aleksandrhovhannisyan.com/blog/trie-data-structure-implementation-in-python/
# https://towardsdatascience.com/pandas-concat-tricks-you-should-know-to-speed-up-your-data-analysis-cd3d4fdfe6dd
# http://morpho.aalto.fi/events/morphochallenge2005/P05_KeshavaPitler.pdf
# https://slideplayer.com/slide/5016724/
# https://www.geeksforgeeks.org/selecting-rows-in-pandas-dataframe-based-on-conditions/
#https://digital.lib.washington.edu/researchworks/bitstream/handle/1773/22453/Lushtak_washington_0250O_11149.pdf?sequence=1
