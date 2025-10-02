import sys
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
import matplotlib.pyplot as plt
import seatease.cseatease as spectro
from matplotlib.figure import Figure
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Layout.Configuration.Processing.ShiftPeakWidth.GaussianPeakWidthFitting.gaussianpeakwidthfittinglayout import GaussianPeakWidthFittingLayout
from Layout.Configuration.Processing.ShiftPeakWidth.LorentzianPeakWidthFitting.lorentzianpeakwidthfittinglayout import LorentzianPeakWidthFittingLayout
from Layout.Configuration.Processing.ShiftPeakWidth.PolynomialPeakWidthFitting.polynomialpeakwidthfittinglayout import PolynomialPeakWidthFittingLayout

class ShiftPeakWidthLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.nested_tabs_layout = QVBoxLayout()

        self.gaussianpeakwidthfittinglayout = GaussianPeakWidthFittingLayout()
        self.lorentzianpeakwidthfittinglayout = LorentzianPeakWidthFittingLayout()
        self.polynomialpeakwidthfittinglayout = PolynomialPeakWidthFittingLayout()

        self.nested_tabs_layout.addWidget(self.gaussianpeakwidthfittinglayout.fitting_button)
        self.nested_tabs_layout.addWidget(self.lorentzianpeakwidthfittinglayout.fitting_button)
        self.nested_tabs_layout.addWidget(self.polynomialpeakwidthfittinglayout.fitting_button)
        self.nested_tabs_layout.addStretch()
        
        self.setLayout(self.nested_tabs_layout)    