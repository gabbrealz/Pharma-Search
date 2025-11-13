from PyQt5.QtCore import QAbstractListModel, Qt
from os import path


class TrieModel(QAbstractListModel): # A custom model for providing autocomplete suggestions using a Trie data structure.
    def __init__(self, trie, parent = None):
        super().__init__(parent)
        self.trie = trie
        # Set the directory where serialized Trie files are stored.
        self.pklDir = path.join(path.dirname(path.abspath(__file__)), "pickled_tree")
        self.suggestions = [] # List of current autocomplete suggestions.

    def setPrefix(self, prefix): # This method will update the suggestions based on the inputted prefix.
        self.beginResetModel()                                          # The model is about to change,
        self.suggestions = self.trie.autoComplete(prefix, self.pklDir)  
        self.endResetModel()                                            # The model has been updated.

    def rowCount(self, parent): # Returns the number of suggestions in the model.
        return len(self.suggestions)
    
    def data(self, index, role): # This method will return a data for a specific index and role.
        # Check if the index is valid and if the role is either for display or editing.
        if index.isValid() and role == Qt.EditRole or role == Qt.DisplayRole:
            return self.suggestions[index.row()]
        return None