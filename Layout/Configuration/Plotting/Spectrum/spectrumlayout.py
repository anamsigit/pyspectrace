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
    QColorDialog, QDoubleSpinBox, QProgressBar
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SpectrumLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.nested_tabs = QWidget()
        self.nested_tabs_layout = QVBoxLayout()

        spectrumscalling = self.SpectrumScalling()
        self.nested_tabs_layout.addWidget(spectrumscalling)
        spectrumplotovertime = self.SpectrumPlotOverTime()
        self.nested_tabs_layout.addWidget(spectrumplotovertime)

        self.nested_tabs_layout.addStretch()
        self.nested_tabs.setLayout(self.nested_tabs_layout)
    
    def SpectrumScalling(self):
        groupBox = QGroupBox("View scalling")

        hboxLayout_range = QHBoxLayout()
        hboxLayout_autoscale = QHBoxLayout()

        self.fit_interest_x = QPushButton("Fit interest X")
        self.fit_interest_y = QPushButton("Fit interest Y")


        hboxLayout_autoscale.addWidget(self.fit_interest_x)
        hboxLayout_autoscale.addWidget(self.fit_interest_y)

        vboxLayout = QVBoxLayout()
        
        vboxLayout.addLayout(hboxLayout_autoscale) 
        vboxLayout.addLayout(hboxLayout_range) 
        # vboxLayout.addWidget(self.update_fixed_range_merge) 

        groupBox.setLayout(vboxLayout)
        return groupBox

    def SpectrumPlotOverTime(self):
        groupBox = QGroupBox("Plotting overtime")

        interval_acquire_layout = QHBoxLayout()
        interval_acquire_label = QLabel("acquire interval (s) :", self)
        self.interval_acquire = QDoubleSpinBox(self)
        self.progress = QProgressBar(self)
        self.sum = QLabel("0", self)
        self.interval_acquire.setRange(0.01, 1000)
        # self.interval_acquire.setEnabled(False)
        self.interval_acquire.setValue(30)
        self.progress.setTextVisible(False)
        interval_acquire_layout.addWidget(interval_acquire_label,4)
        interval_acquire_layout.addWidget(self.interval_acquire, 2)
        interval_acquire_layout.addWidget(self.progress,5)
        interval_acquire_layout.addWidget(self.sum,1)

        pauseresume_hbox_layout = QHBoxLayout()
        self.start_acquire = QPushButton("Resume")
        self.pause_acquire = QPushButton("Pause")
        self.plot = QPushButton("Plot")
        self.restart = QPushButton("Restart")
        pauseresume_hbox_layout.addWidget(self.start_acquire)
        pauseresume_hbox_layout.addWidget(self.pause_acquire)
        pauseresume_hbox_layout.addWidget(self.plot)
        pauseresume_hbox_layout.addWidget(self.restart)

        vboxLayout = QVBoxLayout()
        vboxLayout.addLayout(interval_acquire_layout) 
        vboxLayout.addLayout(pauseresume_hbox_layout) 

        groupBox.setLayout(vboxLayout)
        return groupBox
    


