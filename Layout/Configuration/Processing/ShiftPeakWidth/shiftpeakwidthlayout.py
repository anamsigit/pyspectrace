from PyQt5.QtWidgets import (QWidget, QVBoxLayout)

from pyspectrace.Layout.Configuration.Processing.ShiftPeakWidth.GaussianPeakWidthFitting.gaussianpeakwidthfittinglayout import GaussianPeakWidthFittingLayout
from pyspectrace.Layout.Configuration.Processing.ShiftPeakWidth.LorentzianPeakWidthFitting.lorentzianpeakwidthfittinglayout import LorentzianPeakWidthFittingLayout
from pyspectrace.Layout.Configuration.Processing.ShiftPeakWidth.PolynomialPeakWidthFitting.polynomialpeakwidthfittinglayout import PolynomialPeakWidthFittingLayout

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