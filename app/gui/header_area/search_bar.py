from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from prefix_tree.auto_completer import TrieModel


class SearchBar(QtWidgets.QLineEdit):
    search_requested = pyqtSignal(str)

    def __init__(self, trie_model, parent=None):
        super().__init__(parent)

        self.setPlaceholderText("Search here")
        self.setFont(QtGui.QFont("Poppins", 12))
        self.setMinimumHeight(42)
        self.setStyleSheet("""
            QLineEdit {
                background-color: white;
                padding-left: 15px;
                border: 1px solid #cccccc;
                border-radius: 15px;
            }
        """)

        # Initialize the QCompleter with a custom model for autocompletion.
        self.completer = QtWidgets.QCompleter(trie_model)

        # This will display the popup suggestions below the search bar.
        self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        # Make the auto completion case-insensitive.
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        # Attach the QCompleter to the Search Bar
        self.setCompleter(self.completer)

        # To make sure that the suggestions change as the user types.
        self.textChanged.connect(self.update_completer)

        # Customizing the appearance of QCompleter popup.
        self.completer.popup().setStyleSheet("""
            QAbstractItemView {
                background-color: white;
                border: 2px solid rgb(211, 211, 211);
                font-size: 18px;
                selection-background-color: #d64545;
                selection-color: white;
            }
                                             
            QAbstractItemView::item {
                padding: 8px;
                margin: 4px;
            }
        """)
        self.completer.setMaxVisibleItems(999)  # High limit
        self.completer.popup().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.completer.popup().setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.search_requested.emit(self.text())
            self.clearFocus()
        else:
            super().keyPressEvent(event)

    def emit_signal(self):
        self.search_requested.emit(self.text())

    def update_completer(self, text):
        trie_model = self.completer.model()
        trie_model.setPrefix(text)
        self.completer.complete()