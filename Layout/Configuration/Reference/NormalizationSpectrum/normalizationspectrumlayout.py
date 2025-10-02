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
import pyqtgraph as pg

class NormalizationSpectrumLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.dark_wavelengths = np.array([])
        self.dark_intensities = np.array([])

        self.bright_wavelengths = np.array([])
        self.bright_intensities = np.array([])

        self.nested_tabs_layout = QVBoxLayout()

        brightspectrumbox = self.BrightSpectrumBox()
        darkspectrumbox = self.DarkSpectrumBox()
        normalizationreferencespectrumbox = self.NormalizationReferenceSpectrumBox()
    
        # self.applied = QPushButton("Correction")

        actionlayout = QHBoxLayout()
        # actionlayout.addWidget(self.applied)

        self.nested_tabs_layout.addWidget(brightspectrumbox)
        self.nested_tabs_layout.addWidget(darkspectrumbox)
        
        self.nested_tabs_layout.addWidget(normalizationreferencespectrumbox)
        self.nested_tabs_layout.addLayout(actionlayout)
        self.nested_tabs_layout.addStretch()
        self.setLayout(self.nested_tabs_layout)



    def NormalizationReferenceSpectrumBox(self):
        groupBox = QGroupBox("Preview")
        brightreferencespectrumbox_layout = QVBoxLayout()

        self.plt = pg.PlotWidget()
        self.plt.setBackground('w')

        legend = self.plt.addLegend(offset=(10, 10))
        # self.plt.addLegend()

        
        self.bright_plot = self.plt.plot(self.bright_wavelengths, self.bright_intensities, pen=pg.mkPen('b', width=2), name="Bright")
        self.dark_plot = self.plt.plot(self.dark_wavelengths, self.dark_intensities, pen=pg.mkPen('r', width=2), name="Dark")

        brightreferencespectrumbox_layout.addWidget(self.plt)
        groupBox.setLayout(brightreferencespectrumbox_layout)
        return groupBox


    def BrightSpectrumBox(self):
        groupBox = QGroupBox("Bright Spectrum Reference")
        self.take_bright_button = QPushButton("Take")
        self.clear_bright_button = QPushButton("Clear")
        self.save_bright_button = QPushButton("Save")
        self.load_bright_button = QPushButton("Load")

        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(self.take_bright_button)
        hboxLayout.addWidget(self.clear_bright_button)
        hboxLayout.addWidget(self.save_bright_button)
        hboxLayout.addWidget(self.load_bright_button)
        groupBox.setLayout(hboxLayout)
        
        self.clear_bright_button.setEnabled(False)
        return groupBox
    
    def DarkSpectrumBox(self):
        groupBox = QGroupBox("Dark Spectrum Reference")
        self.take_dark_button = QPushButton("Take")
        self.clear_dark_button = QPushButton("Clear")
        self.save_dark_button = QPushButton("Save")
        self.load_dark_button = QPushButton("Load")

        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(self.take_dark_button)
        hboxLayout.addWidget(self.clear_dark_button)
        hboxLayout.addWidget(self.save_dark_button)
        hboxLayout.addWidget(self.load_dark_button)
        groupBox.setLayout(hboxLayout)

        self.clear_dark_button.setEnabled(False)
        return groupBox


    def dark_plot_spectrum(self, wavelengths, intensities):
        self.dark_plot.setData(wavelengths, intensities)

    def dark_clear_plot_spectrum(self, wavelengths, intensities):
        self.dark_plot.setData(wavelengths, intensities)

    def bright_plot_spectrum(self, wavelengths, intensities):
        self.bright_plot.setData(wavelengths, intensities)

    def bright_clear_plot_spectrum(self, wavelengths, intensities):
        self.bright_plot.setData(wavelengths, intensities)
 