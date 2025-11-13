from PyQt5 import QtGui, QtWidgets



class HeaderFrame(QtWidgets.QFrame):
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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("header_frame")
        self.setStyleSheet("#header_frame { background-color: rgb(255, 78, 78) }")

        self.setMinimumHeight(101)
        self.setMaximumHeight(101)

        # Layout setup
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Undo Button
        self.undo_button = QtWidgets.QPushButton()
        self.undo_button.setFixedSize(45, 45)
        self.undo_button.setStyleSheet(HeaderFrame.BUTTON_STYLE)
        self.undo_button.setFont(QtGui.QFont("", 18))
        self.undo_button.setText("🡄")
        self.layout.addWidget(self.undo_button)


    def clear(self):
        while self.layout.count() > 1:
            item = self.layout.takeAt(1)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                HeaderFrame._clear_all(item.layout())
    
    def add_widget(self, widget):
        self.layout.addWidget(widget)
    
    def add_spacing(self, spacing):
        self.layout.addSpacing(spacing)


    @staticmethod
    def _clear_all(layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                HeaderFrame._clear_all(item.layout())