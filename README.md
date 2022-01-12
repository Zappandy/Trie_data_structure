# Instructions

**Warning**: \*.txt files are not in the repo. Have access to a corpus with 2 columns (word, Freq) in order to test this out.

The main script is **segmentation_trie.py**. Therein, both the trie.py and affixes.py have been imported. The former creates the trie structure without using any external libraries. Affixes.py contains 2 custom classes and 3 functions to create the top affixes. 

In the segmentation module, both the data cleaning and segmentation are performed. Vectorized methods were implemented with pandas to speed up function and class implementation. However, even with that in mind, filtering out words using frequencies is needed to reduce the dataset from 3 million to 120000.


# Assignment Discussion
## 2.3 Interacting with the Trie

For debugging purposes, I added print statements to both addWord and hasWord in TrieDS. Plus I decided to pass an initialized frequency to test it out with the *reports* example found in the assignment description. To compute and mutate the frequencies, I addeed a getFrequency method.

To add the word, I initially considered performing a recursive call on the string. However, since we are already recursively calling the TrieNode in the loop, the additional recursive call ran into issues like reinitalizing the node to its previous state. In hindsight, this could've been remedied with the following pseudo-code

```Python
addEntry(self, substring, freq):
    node = self
    if len(substring) == 0:
         node.endToken = True
         return node.endToken
    if node.getChildNode(substring[0]):
         node.ChildNodes.setdefault(substring[0], TrieNode(substring[0]))
    node = node.getChildNode(substring[0])
    node.frequency += freq
    node.addEntry(self, substring[1:], freq)
```
Because of this, I did not get the right result immediately. Having said that, the biggest challenge was to realize that the self itself had to be updated when calling the node during the loop again (be it iteration or recursion).

After having figured out addEntry, hasWord was much more straightforward and to avoid looping all over words that have not been added to the dictionary, I added a break statement.

I think a defaultdict may have been faster than the current implementation and I wish I would've implemented a shell file to automatically remove 4 empty lines from the corpus instead of doing it manually. Evidence of this is found in the segmentation script where I have a bash line to improve this implementation down the line

## 2.7 Segmentation comments

Segmentation was mostly performed with the original trie_segmentation script, but a demo ipython notebook was added via the following command

```bash
ipynb-py-convert segmentation_trie.py demo_segmentation.ipynb
```
Initially the segmentation was performed with an additional trie structure wherein the words had been reversed to perform analysis of stem + suffixes as if they were prefix + stem. While an interesting idea, this was extremely inefficent. Therefore, the better solution was to perform it dynamically while building the affixes and scoring them. This also helped to allevate issues with affix and words that had the same scores. However, to actually break these ties, word pruning should be implemented. This can be expanded by fetching the frequencies during the iteration of affix building. From there we can create a hash table (a dictionary) to perform computations to find the most suitable affix. This can be by fetching the max frequency or max score + frequency. The following paper by [Lushtak form 2012](https://digital.lib.washington.edu/researchworks/bitstream/handle/1773/22453/Lushtak_washington_0250O_11149.pdf?sequence=1) contains interesting experiments on this front that are out of the scope of this project.

The current segmentation may have been overengineered and in fact a simple depth first search in the trie may have been more efficent to query the system with a given affix. Albert Yeung's implementation of [data structures](https://albertauyeung.github.io/) reflect this faster solution. Albeit with no frequencies. 

Interestingly enough, the prefix slicing and handling declines when accessing words with frequencies lower than 600. Whereas suffix slicing sees virtually no changes. This is actually an advantage because it means the script can run faster. Unfortunately when dropping the frequency condition to 70, the trie really slows down and since the segmentation implementation is not optimized, we also see these runtime issues.

Additional comments have been made about the segmentation in the trie_segmentation and demo scripts. Further experiments can be performed to include other top affixes, since the current program is only checking the top 5% affixes.

# Resources to solve main computational challenges during implementation

- https://towardsdatascience.com/pandas-concat-tricks-you-should-know-to-speed-up-your-data-analysis-cd3d4fdfe6dd
- http://morpho.aalto.fi/events/morphochallenge2005/P05_KeshavaPitler.pdf
- https://slideplayer.com/slide/5016724/
- https://www.geeksforgeeks.org/selecting-rows-in-pandas-dataframe-based-on-conditions/
