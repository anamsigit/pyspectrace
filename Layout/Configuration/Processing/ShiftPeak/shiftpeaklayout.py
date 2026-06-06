from PyQt5.QtWidgets import (QWidget, QVBoxLayout)

from pyspectrace.Layout.Configuration.Processing.ShiftPeak.GaussianPeakFitting.gaussianpeakfittinglayout import GaussianPeakFittingLayout
from pyspectrace.Layout.Configuration.Processing.ShiftPeak.LorentzianPeakFitting.lorentzianpeakfittinglayout import LorentzianPeakFittingLayout
from pyspectrace.Layout.Configuration.Processing.ShiftPeak.PolynomialPeakFitting.polynomialpeakfittinglayout import PolynomialPeakFittingLayout
from pyspectrace.Layout.Configuration.Processing.ShiftPeak.PolyPeakFitting.polypeakfittinglayout import PolyPeakFittingLayout


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