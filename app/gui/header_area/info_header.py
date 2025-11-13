from PyQt5 import QtGui, QtWidgets, QtCore



class InfoHeader:
    def __init__(self, header_frame):
        self.header_frame = header_frame

        # Header labels
        self.label_widget = QtWidgets.QWidget()
        self.label_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        label_layout = QtWidgets.QVBoxLayout(self.label_widget)
        label_layout.setContentsMargins(0,0,0,0)

        # Brand name label
        self.brand_label = QtWidgets.QLabel()
        self.brand_label.setFont(QtGui.QFont("Trebuchet MS", 22, QtGui.QFont.Bold))
        self.brand_label.setAlignment(QtCore.Qt.AlignCenter)
        self.brand_label.setStyleSheet("color: white; background: transparent;")

        label_layout.addWidget(self.brand_label)

        # Manufacturer name label
        self.manufacturer_label = QtWidgets.QLabel()
        self.manufacturer_label.setFont(QtGui.QFont("Tw Cen MT", 18))
        self.manufacturer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.manufacturer_label.setStyleSheet("color: white; background: transparent;")

        label_layout.addWidget(self.manufacturer_label)


    def show(self, data):
        self.brand_label.setText(data[0][1])
        self.manufacturer_label.setText(data[1][1])

        self.header_frame.clear()
        self.header_frame.add_widget(self.label_widget)