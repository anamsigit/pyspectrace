from PyQt5.QtWidgets import (QWidget, QVBoxLayout)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class InfoLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.nested_tabs = QWidget()
        self.nested_tabs_layout = QVBoxLayout()
        self.nested_tabs.setLayout(self.nested_tabs_layout)
    
    def normalization_status(self):
        pass

    def spectrometerconnect_status(self):
        pass
    
    def computerresourcesusage_status(self):
        pass

    def computerresourcesusage_status(self):
        pass

    