import sys
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
import matplotlib.pyplot as plt
import seatease.cseatease as spectro
# from matplotlib.figure import Figure
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QSpinBox, QAction, QCheckBox, 
    QFileDialog, QComboBox, QGroupBox, QLineEdit, QFormLayout, QTableWidget,
    QColorDialog, QDoubleSpinBox
)
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pyqtgraph as pg


class BaselineSpectrumLayout(QWidget): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.nested_tabs_layout = QVBoxLayout()

        baselinespectrumbox = self.BaselineSpectrumBox()
        # previewbox = self.BaselineReferenceSpectrumBox()
    
        actionlayout = QHBoxLayout()

        self.nested_tabs_layout.addLayout(baselinespectrumbox)
        # self.nested_tabs_layout.addWidget(previewbox)
        self.nested_tabs_layout.addLayout(actionlayout)
        self.nested_tabs_layout.addStretch()

        self.setLayout(self.nested_tabs_layout)

    def BaselineSpectrumBox(self):
        # groupBox = QGroupBox("Baseline correction range preview")

        hboxLayout = QHBoxLayout()
        hboxLayout_range = QHBoxLayout()
        self.allow_baseline = QCheckBox("Enable baseline correction")

        # QDoubleSpinBox untuk range min dan max
        self.min_range_input = QDoubleSpinBox()
        self.min_range_input.setDecimals(2)
        self.min_range_input.setValue(0)
        self.min_range_input.setDisabled(True)
        

        self.max_range_input = QDoubleSpinBox()
        self.max_range_input.setDecimals(2)
        self.max_range_input.setValue(10000)
        self.max_range_input.setDisabled(True)

        # Menambahkan label untuk input
        min_label = QLabel("Min. λ (nm):")
        max_label = QLabel("Max. λ (nm):")

        # Menambahkan widget ke layout range
        hboxLayout_range.addWidget(min_label)
        hboxLayout_range.addWidget(self.min_range_input)
        hboxLayout_range.addWidget(max_label)
        hboxLayout_range.addWidget(self.max_range_input)


        baselinereferencespectrumbox = QWidget()
        baselinereferencespectrumbox_layout = QVBoxLayout()
        baselinereferencespectrumbox_layout.addWidget(baselinereferencespectrumbox)

        self.plt = pg.PlotWidget()
        self.plt.setBackground('w')

        baselinereferencespectrumbox_layout.addWidget(self.plt)

        # Layout utama untuk groupBox
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.allow_baseline)  # Layout range min/max
        vboxLayout.addLayout(hboxLayout_range)  # Layout range min/max
        vboxLayout.addLayout(hboxLayout)        # Layout tombol
        vboxLayout.addLayout(baselinereferencespectrumbox_layout)        # Layout tombol

        # groupBox.setLayout(vboxLayout)
        # return groupBox
        return vboxLayout

    # def BaselineReferenceSpectrumBox(self):
    #     groupBox = QGroupBox("Preview Bright Spectrum Reference")



        # groupBox.setLayout(baselinereferencespectrumbox_layout)

        # return groupBox
    
    def plot_spectrum(self, wavelengths, intensities):
        self.plt.clear()  # Clear previous plots
        self.plt.plot(wavelengths, intensities, pen=pg.mkPen('b', width=3))  # Plot with blue line

    def clear_plot_spectrum(self):
        self.plt.clear()  # Clear the plot
