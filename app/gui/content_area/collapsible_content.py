from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt


class CollapsibleContent(QtWidgets.QWidget):
    def __init__(self, title, content, is_html=False, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QToolButton {
                font-family: "Trebuchet MS";
                font-size: 18pt;
                font-weight: bold;
                color: rgb(0,12,95);
                padding: 5px;
                           
                border: none;
                background: transparent;
            }
                        
            QToolButton:hover {background: transparent;}
            QToolButton:pressed {background: transparent;}
            QToolButton:checked {background: transparent;}

            QLabel {
                font-weight: Arial;
                font-size: 18px;
            }
        """)

        # The header title
        self.toggle_button = QtWidgets.QToolButton(text="  "+title, checkable=True, checked=False)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.clicked.connect(self.toggle)

        # Container for actual content
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_area.setVisible(False)  # Start collapsed

        # Add content to the content_area
        text_format = Qt.RichText if is_html else Qt.PlainText

        if type(content) == str:
            content_label = QtWidgets.QLabel()
            content_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            content_label.setWordWrap(True)
            content_label.setTextFormat(text_format)
            content_label.setText(content)
            self.content_layout.addWidget(content_label)
        else:
            for item in content:
                content_label = QtWidgets.QLabel()
                content_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                content_label.setWordWrap(True)
                content_label.setTextFormat(text_format)
                content_label.setText(item)
                self.content_layout.addWidget(content_label)
        
        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.content_area)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)


    def toggle(self):
        expanded = self.toggle_button.isChecked()
        self.content_area.setVisible(expanded)
        self.toggle_button.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)