from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal



class Card(QtWidgets.QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, brand_name, manufacturer_name, product_type, index, parent=None):
        super().__init__(parent)

        self.index = index

        self.setObjectName("card")
        self.setFixedHeight(120)
        self.setMinimumWidth(980)

        self.setStyleSheet("""
            #card {
                padding-right: 20px;
                background-color: white;
                border: 2px solid #ccc;
                border-bottom: 5px solid #aaa;
                border-right: 3px solid #aaa;
                border-radius: 10px;
            }
        """)

        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        # Layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        # Text container (vertical)
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(5)

        self.brand_label = QtWidgets.QLabel(brand_name)
        self.brand_label.setStyleSheet("QLabel {color: black;}")
        self.brand_label.setFont(QtGui.QFont("Trebuchet MS", 14, italic=True))

        self.manufacturer_label = QtWidgets.QLabel(manufacturer_name)
        self.manufacturer_label.setStyleSheet("QLabel {color: rgb(75,75,75);}")
        self.manufacturer_label.setFont(QtGui.QFont("Tw Cen MT", 12, italic=True))

        self.prodtype_label = QtWidgets.QLabel(product_type)
        self.prodtype_label.setStyleSheet("QLabel {color: rgb(110,110,110);}")
        self.prodtype_label.setFont(QtGui.QFont("Tw Cen MT", 11, italic=True))

        text_layout.addWidget(self.brand_label)
        text_layout.addWidget(self.manufacturer_label)
        text_layout.addWidget(self.prodtype_label)

        # Spacer between text and button
        layout.addLayout(text_layout)
        layout.addStretch()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)