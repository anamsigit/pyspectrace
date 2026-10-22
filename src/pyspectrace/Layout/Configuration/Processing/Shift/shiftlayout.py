from PyQt5.QtWidgets import (QWidget, QVBoxLayout)
from pyspectrace.Layout.Configuration.Processing.Shift.PolynomialFitting.polynomialfittinglayout import PolynomialFittingLayout

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