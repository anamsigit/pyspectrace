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

from Layout.Configuration.Processing.ShiftPeak.GaussianPeakFitting.gaussianpeakfittinglayout import GaussianPeakFittingLayout
from Layout.Configuration.Processing.ShiftPeak.LorentzianPeakFitting.lorentzianpeakfittinglayout import LorentzianPeakFittingLayout
from Layout.Configuration.Processing.ShiftPeak.PolynomialPeakFitting.polynomialpeakfittinglayout import PolynomialPeakFittingLayout
from Layout.Configuration.Processing.ShiftPeak.PolyPeakFitting.polypeakfittinglayout import PolyPeakFittingLayout


class ShiftPeakLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.nested_tabs_layout = QVBoxLayout()

        self.gaussianpeakfittinglayout = GaussianPeakFittingLayout()
        self.lorentzianpeakfittinglayout = LorentzianPeakFittingLayout()
        self.polynomialpeakfittinglayout = PolynomialPeakFittingLayout()
        self.polypeakfittinglayout = PolyPeakFittingLayout()

        self.nested_tabs_layout.addWidget(self.gaussianpeakfittinglayout.fitting_button)
        self.nested_tabs_layout.addWidget(self.lorentzianpeakfittinglayout.fitting_button)
        self.nested_tabs_layout.addWidget(self.polypeakfittinglayout.fitting_button)
        self.nested_tabs_layout.addWidget(self.polynomialpeakfittinglayout.fitting_button)
        self.nested_tabs_layout.addStretch()
        
        self.setLayout(self.nested_tabs_layout)    