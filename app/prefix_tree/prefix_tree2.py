import pickle
import os
from trie_node import TrieNode

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word): # This method will insert the word into Trie
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.endOfWord = True

    def autoComplete(self, prefix, pklDir): # This method will retrieve necessary suggestions
                                            # by loading the relevant serialized Trie.
        if not prefix:
            return []
         # This will identify the correct Trie file based on the first letter of the prefix.
        firstLetter = prefix[0].lower()
        triePklPath = os.path.join(pklDir, f"trie{firstLetter.upper()}.pkl")

        if not os.path.exists(triePklPath):
            return [] # Return an empty list if the file does not exist.
        
        # Loading of the serialized Trie from the file.
        with open(triePklPath, "rb") as pkl_file:
            loadedTrie = pickle.load(pkl_file)
        
        curr = loadedTrie.root
        # Traverse the Trie based on the prefix given.
        for char in prefix:
            if char not in curr.children:
                return [] # If the prefix is not found, it will return an empty list.
            curr = curr.children[char]

        # Collect suggestions from the current node
        suggestions = []
        self.stopper(curr, prefix, suggestions, limit = 10) # Limiting the suggestion to maximum of 10 only.
        return suggestions
    

    def stopper(self, node, prefix, suggestions, limit): # This method is a will just ensure that the suggestion is only 10.
        if len(suggestions) >= limit:
            return # Will stop giving suggestion if the limit is reached.
        if node.endOfWord:
            suggestions.append(prefix) # Add the prefix to suggestions if it forms a word.
        # Recurring for each child node.
        for char, childNode in node.children.items():
            self.stopper(childNode, prefix + char, suggestions, limit)