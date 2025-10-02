import sys
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import matplotlib.pyplot as plt
import seatease.cseatease as spectro
from matplotlib.figure import Figure
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QSpinBox, QAction, QCheckBox, 
    QFileDialog, QComboBox, QGroupBox, QLineEdit, QFormLayout, QTableWidget,
    QColorDialog
)
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

    