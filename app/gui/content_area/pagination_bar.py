from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

from loader import ENTRIES_PER_PAGE



class NavigateButton(QtWidgets.QPushButton):
    chosen = pyqtSignal(int)

    def __init__(self, unicode_icon, direction, parent=None):
        super().__init__(parent)

        self.setProperty("navigate", True)

        self.direction = direction
        self.setText(unicode_icon)

        self.clicked.connect(self.emit_signal)

    def emit_signal(self):
        self.chosen.emit(self.direction)


class PageButton(QtWidgets.QPushButton):
    chosen = pyqtSignal(int)

    def __init__(self, pagination_bar, parent=None):
        super().__init__(parent)

        self.pagination_bar = pagination_bar
        self.setProperty("page", True)
        self.setCheckable(True)

        self.toggled.connect(self.emit_signal)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.isChecked():
            return
        return super().mousePressEvent(event)

    def emit_signal(self, checked):
        if checked:
            checked_btn = self.pagination_bar.checked_btn
            if checked_btn is not None and checked_btn != self:
                checked_btn.setChecked(False)
                self.pagination_bar.checked_btn = self

            page_num = int(self.text())
            self.pagination_bar.current_page = page_num
            self.chosen.emit(page_num)

    def get_pagenum(self):
        return int(self.text())


class PaginationBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("pagination_bar")

        self.setStyleSheet("""
            QPushButton[page="true"] {
                background-color: #fef2f2;
                color: #333;
                border: 1px solid #e0b4b4;
                padding: 6px 12px;
                min-width: 32px;
                min-height: 32px;
                border-radius: 6px;
                font-family: Arial;
                font-size: 16px;
            }

            QPushButton[page="true"]:hover {
                background-color: #f8d7da;
                border: 1px solid #d08c8c;
            }

            QPushButton[page="true"]:checked {
                background-color: #d64545;
                color: white;
                border: 1px solid #b03030;
                font-weight: bold;
            }

            QPushButton[page="true"]:disabled {
                background-color: #f5f5f5;
                color: #bbb;
                border: 1px solid #ddd;
            }
            
            QPushButton[navigate="true"] {
                background-color: #eeeeee;
                border: 1px solid #aaa;
                min-width: 32px;
                min-height: 32px;
                padding: 6px 10px;
                border-radius: 6px;
                font-size: 20px;
            }
            QPushButton[navigate="true"]:hover {
                background-color: #ddd;
            }
            QPushButton[navigate="true"]:disabled {
                color: #999;
                background-color: #f9f9f9;
            }
        """)

        self.page_limit = None
        self.current_page = 1
        self.checked_btn = None

        pagebtn_widget = QtWidgets.QWidget()
        self.pagebtn_layout = QtWidgets.QHBoxLayout(self)
        self.pagebtn_layout.setContentsMargins(5,5,5,5)

        self.buttons = [PageButton(self) for _ in range(10)]

        self.pagebtn_layout.addStretch()
        for button in self.buttons:
            self.pagebtn_layout.addWidget(button)
        self.pagebtn_layout.addStretch()


    def navigatebtn_func(self, direction: int):
        for button in self.buttons:
            page_num = button.get_pagenum() + direction
            button.setText(str(page_num))

            button.blockSignals(True)
            button.setChecked(page_num == self.current_page)
            button.blockSignals(False)

            button.setEnabled(page_num <= self.page_limit)

    
    def update_state(self, entries: int):
        self.page_limit = -(-entries//ENTRIES_PER_PAGE)

        self.checked_btn = self.buttons[0]
        self.checked_btn.setText("1")
        self.checked_btn.blockSignals(True)
        self.checked_btn.setChecked(True)
        self.checked_btn.blockSignals(False)
    
        for i in range(1,len(self.buttons)):
            self.buttons[i].setText(str(i+1))
            self.buttons[i].blockSignals(True)
            self.buttons[i].setChecked(False)
            self.buttons[i].blockSignals(False)
            self.buttons[i].setEnabled(i+1 <= self.page_limit)

        self.current_page = 1
    

    def goto_current_page(self):
        page_num = ((self.current_page-1)//10)*10+1

        for button in self.buttons:
            button.setText(str(page_num))

            button.blockSignals(True)
            if page_num == self.current_page:
                button.setChecked(True)
                self.checked_btn = button
            else: 
                button.setChecked(False)
            button.blockSignals(False)

            page_num += 1