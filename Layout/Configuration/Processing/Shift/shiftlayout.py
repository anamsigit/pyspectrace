import sys
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
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

from Layout.Configuration.Processing.Shift.PolynomialFitting.polynomialfittinglayout import PolynomialFittingLayout

class ShiftLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.nested_tabs_layout = QVBoxLayout()

        self.polynomialfittinglayout = PolynomialFittingLayout()
        # self.nested_tabs_layout.addLayout(self.polynomialfittinglayout.fitting_button)
        self.nested_tabs_layout.addWidget(self.polynomialfittinglayout.fitting_button)
        self.nested_tabs_layout.addStretch()
        
        self.setLayout(self.nested_tabs_layout)    