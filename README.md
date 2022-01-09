# Instructions

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
