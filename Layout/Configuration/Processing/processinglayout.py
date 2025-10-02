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
    QColorDialog, QDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Layout.Configuration.Processing.Shift.shiftlayout import ShiftLayout
from Layout.Configuration.Processing.ShiftPeak.shiftpeaklayout import ShiftPeakLayout
from Layout.Configuration.Processing.ShiftPeakWidth.shiftpeakwidthlayout import ShiftPeakWidthLayout

class ProcessingLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        self.shiftlayout = ShiftLayout(self)
        self.shiftpeaklayout = ShiftPeakLayout(self)
        self.shiftpeakwidthlayout = ShiftPeakWidthLayout(self)

        nested_tab = QTabWidget()
        nested_tab.addTab(self.shiftpeaklayout, "Peak Position")
        nested_tab.addTab(self.shiftpeakwidthlayout, "Peak Width")
        nested_tab.addTab(self.shiftlayout, "Non Peak")
        
        main_layout.addWidget(nested_tab)
        main_layout.addStretch()
        self.setLayout(main_layout)
        
    def FilteringAlgorithm(self):
        self.algorithm_filtering_option = QComboBox()
        self.algorithm_filtering_option.addItems(['Gaussian', 'Lorentzian'])
        self.algorithm_filtering_option.setEnabled(False)

        self.enable_filtering = QCheckBox("Enable Filtering")

        algorithm_option_layout = QVBoxLayout()
        algorithm_option_layout.addWidget(self.enable_filtering)
        algorithm_option_layout.addWidget(self.algorithm_filtering_option)

        return algorithm_option_layout

