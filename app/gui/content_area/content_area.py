from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from content_area.card import Card
from content_area.collapsible_content import CollapsibleContent



class ContentArea(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setFrameShape(QtWidgets.QScrollArea.NoFrame)
        self.setObjectName("search_results_area")

        self.setStyleSheet("""
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 16px;
                margin: 12px 0;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 24px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover {
                background: #a8a8a8;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: #d0d0d0;
                height: 12px;
                border-radius: 6px;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:vertical {
                subcontrol-position: bottom;
            }

            QScrollBar::sub-line:vertical {
                subcontrol-position: top;
            }

            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                width: 8px;
                height: 8px;
                background: none;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # Container widget
        self.container = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.container)
        self.layout.setContentsMargins(20,10,20,10)
        self.layout.setAlignment(Qt.AlignTop)
        self.container.setLayout(self.layout)

        self.setWidget(self.container)


    def add_cards(self, data, card_func):
        i = 0
        for info in data:
            card = Card(*info, i)
            card.clicked.connect(card_func)
            self.layout.addWidget(card, stretch=1)
            i += 1


    def add_content(self, data):
        for i in range(2,len(data)):
            if not data[i][1]: continue
            self.layout.addWidget(CollapsibleContent(*data[i]))


    def add_widget(self, widget):
        self.layout.addWidget(widget)


    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            item.widget().setParent(None)