from PyQt5 import QtGui, QtWidgets
from header_area.search_bar import SearchBar


class SearchHeader:
    BUTTON_STYLE = """
        QPushButton {
            border-radius: 20px;
            background-color: white;
            border: none;
        }
        QPushButton:hover {
            background-color: rgb(216, 216, 216);
        }
        QPushButton:pressed {
            background-color: rgb(197, 197, 197);
        }
    """

    def __init__(self, trie_model, header_frame):
        self.header_frame = header_frame

        # Redo Button
        self.redo_button = QtWidgets.QPushButton()
        self.redo_button.setFixedSize(45, 45)
        self.redo_button.setStyleSheet(SearchHeader.BUTTON_STYLE)
        self.redo_button.setFont(QtGui.QFont("", 18))
        self.redo_button.setText("🡆")

        # Search Bar
        self.search_bar = SearchBar(trie_model)
        
        # Search Button
        self.search_button = QtWidgets.QPushButton()
        self.search_button.setFixedSize(45, 45)
        self.search_button.setStyleSheet(SearchHeader.BUTTON_STYLE)
        self.search_button.setFont(QtGui.QFont("Segoe UI Symbol", 16))
        self.search_button.setText("🔍")
        
        # Product Type Filter Combobox
        self.filter_combobox = QtWidgets.QComboBox()
        self.filter_combobox.addItems(["ALL", "OTC", "PRESCRIPTION"])
        self.filter_combobox.setFont(QtGui.QFont("Arial", 10))
        self.filter_combobox.setMinimumHeight(42)
        self.filter_combobox.setFixedWidth(155)
        self.filter_combobox.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 8px;
                min-width: 80px;
                font-family: Arial;
                font-size: 16px;
                color: #333;
            }

            QComboBox:hover {
                border: 1px solid #d64545;
            }

            QComboBox::drop-down {
                width: 0px;
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #eaf3f6;
                border: 1px solid #bbb;
                selection-background-color: #d64545;
                selection-color: white;
                padding: 4px;
                font-size: 14px;
                font-family: Arial;
                outline: none;
            }
        """)
        self.filter_combobox.setCurrentIndex(0)


    def show(self):
        self.header_frame.clear()
        self.header_frame.add_widget(self.redo_button)
        self.header_frame.add_spacing(10)
        self.header_frame.add_widget(self.search_bar)
        self.header_frame.add_spacing(3)
        self.header_frame.add_widget(self.search_button)
        self.header_frame.add_spacing(8)
        self.header_frame.add_widget(self.filter_combobox)

    def get_filter(self, index) -> str:
        return self.filter_combobox.itemText(index)
    
    def set_filter(self, index):
        self.filter_combobox.setCurrentIndex(index)