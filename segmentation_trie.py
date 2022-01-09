#!/bin/bash
# grouping and labeling

import pandas as pd
import string
from trie import *
from affixes import *


#%%
def clean_corpus(file):
    df =  pd.read_csv(file, delimiter='\t')
    df.dropna(inplace=True)
    df = df[df["Freq"] > 201]  # mutates index, hence why .loc is better
    df = df[df["Freq"] > 100]  # mutates index, hence why .loc is better
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
MyTrie = TrieDS()
spanish_corpus.apply(lambda row: MyTrie.addWord(row["word"], row["Freq"]), axis=1)  # map may be faster
spanish_corpus.apply(lambda row: MyTrie.hasWord(row["word"]), axis=1)
spanish_corpus.apply(lambda row: affixBuilder(MyTrie, row["word"]), axis=1)

top_suffixes
top_prefixes
# https://albertauyeung.github.io/2020/06/15/python-trie.html/
# https://www.aleksandrhovhannisyan.com/blog/trie-data-structure-implementation-in-python/
# https://towardsdatascience.com/pandas-concat-tricks-you-should-know-to-speed-up-your-data-analysis-cd3d4fdfe6dd
# http://morpho.aalto.fi/events/morphochallenge2005/P05_KeshavaPitler.pdf
# https://slideplayer.com/slide/5016724/
# https://www.geeksforgeeks.org/selecting-rows-in-pandas-dataframe-based-on-conditions/
#https://digital.lib.washington.edu/researchworks/bitstream/handle/1773/22453/Lushtak_washington_0250O_11149.pdf?sequence=1
