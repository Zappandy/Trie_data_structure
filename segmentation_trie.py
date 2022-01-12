#%%

import pandas as pd
import string
import collections
import random  # to test the system by shuffling its segmentations
import time  # tacky way to time program's execution time
from trie import *
from affixes import *

#%%
start = time.time()
def clean_corpus(file):
    """
    file: text file manually edited to feed the trie and perform segmentations
    returns clean dataframe. Removed elements by frequency, dropped nans, turned words
    to lowercase, dropped duplicates and filtered with the Spanish alphabet
    """
    df =  pd.read_csv(file, delimiter='\t')
    df.dropna(inplace=True)
    df = df[df["Freq"] > 600]  # mutates index, hence why .loc is better. okay speed at 100
    #  differentce between 90 and 80 not too great but there's 10k rows of more data
    # so go with 90. With 2 tries, above 600 is faster. Prefixes are cleaner with 600, though
    df.loc[:, "word"] = df["word"].str.lower()
    df = df[df["word"].apply(spanish_alphabet)]   
    df.drop_duplicates(subset=["word"], keep="first", inplace=True)
    #df = df[df["word"].str.len() > 1]  # ~df["word"] inverting mask, i.e. doing the opposte
    df.reset_index(drop=True, inplace=True)  # resetting index in case it was mutated
    return df

def spanish_alphabet(word):  
    """
    word: from dataset
    returns: boolean value to mask words that can't be built with non-Spanish characters
    """
    alphabet = string.ascii_lowercase 
    special_chars = "wxqyz"
    fake_vowels = "áéíóúyüh"
    sp_alphabet = list(alphabet + "áéíóúñü")
    flag = True
    for i in range(len(word) - 1):
        # if current character or next one are not part of the alphabet, mask as False
        if (word[i] not in sp_alphabet) or (word[i+1] not in sp_alphabet):
            flag = False
            break
        # if char in uncommon Spanish characters and following character is followed by a "vowel"
        # then remove. These would not correspond to Spanish words
        if (word[i] in special_chars) and (word[i+1] not in fake_vowels):
            flag = False
            break
    # there aren't Spanish words with more than 5 consonants in a row
    for i in range(len(word) - 5):
        cons = [word[i+j] for j in range(5) if word[i+j] not in fake_vowels + "aeiou"]
        if len(cons) == 5:  # this is a range of 5 so changing the boolean validation to
            # greater than would not be worth it
            flag = False
    return flag


#%%

spanish_corpus = clean_corpus("clean_spanish.txt")  
print(spanish_corpus)
MyTrie = TrieDS()
spanish_corpus.apply(lambda row: MyTrie.addWord(row["word"], row["Freq"]), axis=1)  # map may be faster
spanish_corpus.apply(lambda row: MyTrie.hasWord(row["word"]), axis=1)
spanish_corpus.apply(lambda row: affixBuilder(MyTrie, row["word"]), axis=1)  # don't need to do this twice

#%%
ranked_suffixes = sort_affixes(rank_affixes(ranked_suffixes))
ranked_prefixes = sort_affixes(rank_affixes(ranked_prefixes))
top_suffixes = top_affixes(ranked_suffixes, 0.05)
top_prefixes = top_affixes(ranked_prefixes, 0.05)  

print(len(top_suffixes))
print(len(top_prefixes))
print(top_suffixes[:10])
print(top_prefixes[:10])

#%%
random.shuffle(prefix_segmentation)
random.shuffle(suffix_segmentation)
print(prefix_segmentation[:10])
print(suffix_segmentation[:10])

#%% 
# this is when the script starts running slower. This can be further optimized
def dup_affixes(segmentation):
    """
    segmentation: takes random prefix or suffix segmentation to find words with multiple affixes
    returns: list of duplicates
    """
    dup_affix = collections.Counter("".join(word) for word in segmentation)
    return [word for word, num in dup_affix.items() if num > 1]

dup_prefixes = dup_affixes(prefix_segmentation)
dup_suffixes = dup_affixes(suffix_segmentation)
#%%
def cleaning_affixes(segmentation, dup_affix):
    """
    segmentation: dictionary containing its respective word and segmentation
    returns: clean segmentation to include words with multiple and single affixes to facilitate
    indexing and reviewing of the trie model
    """
    clean_affix = {}
    count = 0
    for word in segmentation:
        full_word = "".join(word)
        if full_word in dup_affix:  # checking if word has multiple affixes
            if full_word in clean_affix:
                clean_affix[full_word].append(f"{word[0]}-{word[1]}")
            else:
                clean_affix.setdefault(full_word, [f"{word[0]}-{word[1]}"])
        else:  # store its single affix
            count += 1
            clean_affix.setdefault(full_word, f"{word[0]}-{word[1]}")
    print(count)  # reviewing how many words have only one affix
    return clean_affix

clean_prefs = cleaning_affixes(prefix_segmentation, dup_prefixes)
clean_suffs = cleaning_affixes(suffix_segmentation, dup_suffixes)

#%%
print(set(clean_prefs["silenciar"]))
print(set(clean_prefs["consciente"]))
print(set(clean_suffs["esclerosis"]))
print(set(clean_suffs["discriminacion"]))

end = time.time()
print(f"Execution time {end - start}")
