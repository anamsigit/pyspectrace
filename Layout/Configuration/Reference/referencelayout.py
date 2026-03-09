from PyQt5.QtWidgets import (
    QTabWidget, QWidget, QVBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from Layout.Configuration.Reference.NormalizationSpectrum.BrightSpectrum.brightspectrumlayout import BrightSpectrumLayout
# from Layout.Configuration.Reference.NormalizationSpectrum.DarkSpectrum.darkspectrumlayout import DarkSpectrumLayout
from Layout.Configuration.Reference.BaselineSpectrum.baselinespectrumlayout import BaselineSpectrumLayout
from Layout.Configuration.Reference.NormalizationSpectrum.normalizationspectrumlayout import NormalizationSpectrumLayout

class ReferenceLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Tab BrightSpectrum
        # self.brightspectrumlayout = BrightSpectrumLayout(self)
        # self.darkspectrumlayout = DarkSpectrumLayout(self)
        self.baselinespectrumlayout = BaselineSpectrumLayout(self)
        self.normalizationspectrumlayout = NormalizationSpectrumLayout(self)

        # Menambahkan nestab bertingkat ke tab induk
        nested_tab = QTabWidget()
        # nested_tab.addTab(self.brightspectrumlayout, 'Bright')
        nested_tab.addTab(self.normalizationspectrumlayout, 'Blank referencing')
        # nested_tab.addTab(self.darkspectrumlayout, 'Dark')
        nested_tab.addTab(self.baselinespectrumlayout, 'Baseline correction')

        main_layout = QVBoxLayout()
        main_layout.addWidget(nested_tab)
        self.setLayout(main_layout)

