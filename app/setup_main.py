from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from header_area.header import HeaderFrame
from header_area.search_header import SearchHeader
from header_area.info_header import InfoHeader

from content_area.content_area import ContentArea
from content_area.pagination_bar import PaginationBar

from searcher import ProdFilter


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, searcher, loader, history, trie_model):
        super().__init__()

        # Initializing backend logic objects
        self.searcher = searcher
        self.loader = loader
        self.reader = self.loader.reader
        self.history = history
        self.trie_model = trie_model

        # Main window setup
        self.setWindowTitle("PharmaSearch")
        self.setObjectName("MainWindow")
        self.resize(1100, 700)
        self.setAutoFillBackground(False)
        
        central_widget = QtWidgets.QWidget()
        central_widget.setStyleSheet("QWidget {background-color: rgb(255, 255, 255)};")
        self.setCentralWidget(central_widget)

        self.window_layout = QtWidgets.QVBoxLayout(central_widget)
        self.window_layout.setContentsMargins(0, 0, 0, 0)

        # Header frame
        self.header = HeaderFrame()
        self.search_header = SearchHeader(trie_model, self.header)
        self.info_header = InfoHeader(self.header)
        self.search_header.show()

        # Connecting undo and redo buttons to methods for functionality
        self.header.undo_button.clicked.connect(self.undo_func)
        self.search_header.redo_button.clicked.connect(self.redo_func)

        # Connecting search-related elements to methods for functionality
        self.search_header.search_bar.search_requested.connect(self.do_search)
        self.search_header.search_button.clicked.connect(self.search_header.search_bar.emit_signal)

        # Connecting the filter combo box to a method for functionality
        self.search_header.filter_combobox.activated.connect(self.filter_change)

        self.window_layout.addWidget(self.header)
    
        # Initializing area where all content will be displayed
        self.content_area = ContentArea()
        self.window_layout.addWidget(self.content_area)

        # Setting up the pagination bar at the bottom
        self.pagination_bar = PaginationBar()
        for button in self.pagination_bar.buttons:
            button.chosen.connect(self.change_page)

        # Setting up label for when no results are found
        self.noresults_label = QtWidgets.QLabel("No results found :(")
        self.noresults_label.setContentsMargins(0,30,0,30)
        self.noresults_label.setAlignment(Qt.AlignCenter)
        self.noresults_label.setStyleSheet("""
            QLabel {
                color: gray;
                font-family: Arial;
                font-weight: bold;
                font-size: 24px;
            }
        """)

        # Label at the start of the program
        welcome_label = QtWidgets.QLabel("""
            <div style="line-height: 125%;">
                <span style="font-size: 50px;">Welcome to</span><br>
                <span style="font-weight: 600; font-size: 60px;">PharmaSearch</span>
            </div>
        """)
        welcome_label.setTextFormat(Qt.RichText)
        welcome_label.setContentsMargins(0,150,0,100)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                font-family: Castellar;
                color: #333;
            }
        """)
        self.content_area.add_widget(welcome_label)


    def do_search(self, query, change_history=True, page_num=1):
        if query == "":
            self.content_area.clear()
            self.content_area.add_widget(self.noresults_label)
        else:
            hist_data = (query, self.search_header.filter_combobox.currentIndex(), self.pagination_bar.current_page)

            if change_history and not self.history.push_history(hist_data):
                return
            
            self.history.reading_page = False
            self.loader.posting_list = self.searcher.search(query)

            if self.loader.posting_list: self.update_pagination_bar(page_num)
            else:
                self.loader.posting_list = None
                self.content_area.clear()
                self.content_area.add_widget(self.noresults_label)
                self.window_layout.removeWidget(self.pagination_bar)
                self.pagination_bar.hide()


    def filter_change(self, index, change_history=True, page_num=1, do_search=True):
        hist_data = (self.search_header.search_bar.text(), index, 1)

        if change_history and not self.history.push_history(hist_data):
            return
        
        self.history.reading_page = False
        filter_name = self.search_header.get_filter(index)
        
        if filter_name == "ALL":
            self.searcher.prod_filter = ProdFilter.ALL
        elif filter_name == "OTC": 
            self.searcher.prod_filter = ProdFilter.OTC
        else: 
            self.searcher.prod_filter = ProdFilter.PRESCRIPTION

        if do_search: self.do_search(self.search_header.search_bar.text(), page_num=page_num, change_history=False)


    def read_page(self, entry_index, change_history=True):
        if change_history and not self.history.push_history(entry_index):
            return

        self.history.reading_page = True

        self.window_layout.removeWidget(self.pagination_bar)
        self.pagination_bar.hide()

        content = self.reader.load_page(entry_index)
        self.info_header.show(content)

        self.content_area.clear()
        self.content_area.add_content(content)


    def update_pagination_bar(self, page_num):
        self.content_area.clear()
        self.content_area.add_cards(self.loader.load_results(page_num), self.read_page)

        self.pagination_bar.update_state(len(self.loader.posting_list))
        self.window_layout.addWidget(self.pagination_bar)
        self.pagination_bar.show()


    def change_page(self, page_num, change_history=True):
        hist_data = (self.search_header.search_bar.text(), self.search_header.filter_combobox.currentIndex(), page_num)

        if change_history and not self.history.push_history(hist_data):
            return

        self.content_area.clear()
        self.content_area.add_cards(self.loader.load_results(page_num), self.read_page)


    def undo_func(self):
        if not self.history.can_undo(): return

        # If the user was reading from an info page, go back to the search page
        if self.history.reading_page:
            self.search_header.show()
            self.window_layout.addWidget(self.pagination_bar)
            self.pagination_bar.show()

        self.history.reading_page = False

        data = self.history.undo()

        self.pagination_bar.current_page = data[2]
        self.pagination_bar.goto_current_page()

        self.search_header.search_bar.setText(data[0])
        self.search_header.set_filter(data[1])
        if data[1] == 0:
            self.searcher.prod_filter = ProdFilter.ALL
        elif data[1] == 1:
            self.searcher.prod_filter = ProdFilter.OTC
        else:
            self.searcher.prod_filter = ProdFilter.PRESCRIPTION

        self.loader.posting_list = self.searcher.search(data[0])

        if self.loader.posting_list:
            self.content_area.clear()
            self.content_area.add_cards(self.loader.load_results(data[2]), self.read_page)
            self.window_layout.addWidget(self.pagination_bar)
            self.pagination_bar.show()
        else:
            self.loader.posting_list = None
            self.content_area.clear()
            self.content_area.add_widget(self.noresults_label)
            self.window_layout.removeWidget(self.pagination_bar)
            self.pagination_bar.hide()


    def redo_func(self):
        if not self.history.can_redo(): return

        data = self.history.redo()

        if type(data) == int:
            self.read_page(data, change_history=False)
            return
            
        self.pagination_bar.current_page = data[2]
        self.pagination_bar.goto_current_page()

        self.search_header.search_bar.setText(data[0])
        self.search_header.set_filter(data[1])
        if data[1] == 0:
            self.searcher.prod_filter = ProdFilter.ALL
        elif data[1] == 1:
            self.searcher.prod_filter = ProdFilter.OTC
        else:
            self.searcher.prod_filter = ProdFilter.PRESCRIPTION

        self.loader.posting_list = self.searcher.search(data[0])

        if self.loader.posting_list:
            self.content_area.clear()
            self.content_area.add_cards(self.loader.load_results(data[2]), self.read_page)
            self.window_layout.addWidget(self.pagination_bar)
            self.pagination_bar.show()
        else:
            self.loader.posting_list = None
            self.content_area.clear()
            self.content_area.add_widget(self.noresults_label)
            self.window_layout.removeWidget(self.pagination_bar)
            self.pagination_bar.hide()