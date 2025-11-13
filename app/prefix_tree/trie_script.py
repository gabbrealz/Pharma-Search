import os
import pickle
from prefix_tree import Trie

def save_tries(pklDir, trieDictionary):
    os.makedirs(pklDir, exist_ok=True)
    for letter, subTrie in trieDictionary.items():
        outFile = os.path.join(pklDir, f"trie{letter.upper()}.pkl")
        with open(outFile, "wb") as pkl_file:
            pickle.dump(subTrie, pkl_file)
            
def build_trie_from_files(pklDir):
    trieDictionary = {}
    for fileName in os.listdir(pklDir):
        if fileName.endswith(".pkl"):
            filePath = os.path.join(pklDir, fileName)
            with open(filePath, "rb") as pkl_file:
                words = pickle.load(pkl_file)
                for word in words:
                    word = word.strip()
                    if word.isalpha():
                        firstLetter = word[0].lower()
                        if firstLetter not in trieDictionary:
                            trieDictionary[firstLetter] = Trie()
                        trieDictionary[firstLetter].insert(word)
    return trieDictionary


if __name__ == "__main__":
    wordsDir = "word_files"
    pklDir = "pickled_tree"
    trieDict = build_trie_from_files(wordsDir)
    save_tries(pklDir, trieDict)
    print("Tries built and saved.")