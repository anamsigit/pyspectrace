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
    QColorDialog, QSlider, QDoubleSpinBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class CommunicationLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.nested_tabs = QWidget()
        self.nested_tabs_layout = QVBoxLayout()


        time_integration_label, time_integration_spinbox = self.TimeIntegration()
        time_integration_button = self.TimeIntegrationButton()

        TimeIntegration_layout = QHBoxLayout()
        TimeIntegration_layout.addWidget(time_integration_label, 3)
        TimeIntegration_layout.addWidget(time_integration_spinbox, 3)
        TimeIntegration_layout.addWidget(time_integration_button, 1)


        AcquisitionDelay_label, AcquisitionDelay_spinbox = self.AcquisitionDelay()
        acquisitiondelay_button = self.AcquisitionDelayButton()

        AcquisitionDelay_layout = QHBoxLayout()
        AcquisitionDelay_layout.addWidget(AcquisitionDelay_label, 3)
        AcquisitionDelay_layout.addWidget(AcquisitionDelay_spinbox, 3)
        AcquisitionDelay_layout.addWidget(acquisitiondelay_button, 1)

        AcquisitionAverage_label, AcquisitionAverage_spinbox = self.AcquisitionAverage()
        acquisitionaverage_button = self.AcquisitionAverageButton()

        AcquisitionAverage_layout = QHBoxLayout()
        AcquisitionAverage_layout.addWidget(AcquisitionAverage_label, 3)
        AcquisitionAverage_layout.addWidget(AcquisitionAverage_spinbox, 3)
        AcquisitionAverage_layout.addWidget(acquisitionaverage_button, 1)

        self.nested_tabs_layout.addLayout(AcquisitionDelay_layout)
        self.nested_tabs_layout.addLayout(TimeIntegration_layout)
        self.nested_tabs_layout.addLayout(AcquisitionAverage_layout)

        self.nested_tabs_layout.addStretch()

        self.time_integration_max = None
        self.time_integration_min = None

        # Set layout utama ke QWidget
        self.nested_tabs.setLayout(self.nested_tabs_layout)
        self.timer = QTimer(self)
        
    def AcquisitionDelay(self):
        acquisitiondelay_label = QLabel("Refresh rate (ms):", self)
        self.acquisitiondelay_spinbox = QSpinBox(self)
        self.acquisitiondelay_spinbox.setRange(1, 10000000)  # milisecound
        self.acquisitiondelay_spinbox.setValue(250)  # Set default value
        return acquisitiondelay_label, self.acquisitiondelay_spinbox

    
    def AcquisitionDelayButton(self):
        self.acquisitiondelay_button = QPushButton("Set")
        return self.acquisitiondelay_button
    
    def AcquisitionAverage(self):
        acquisitionaverage_label = QLabel("Acquisition average :", self)
        self.acquisitionaverage_spinbox = QSpinBox(self)
        self.acquisitionaverage_spinbox.setRange(1, 100)  # Smilisecound
        self.acquisitionaverage_spinbox.setValue(1)  # Set default value
        return acquisitionaverage_label, self.acquisitionaverage_spinbox
    
    def AcquisitionAverageButton(self):
        self.acquisitionaverage_button = QPushButton("Set")
        return self.acquisitionaverage_button
    
    def TimeIntegration(self):
        time_integration_label = QLabel("Integration time (µs):", self)
        self.time_integration_spinbox = QSpinBox(self)
        self.time_integration_spinbox.setSingleStep(10)  # Kenaikan
        return time_integration_label, self.time_integration_spinbox
    
    def TimeIntegrationButton(self):
        self.time_integration_button = QPushButton("Set")
        return self.time_integration_button

    def BufferingEnabled(self):
        bufferingenabled_layout = QCheckBox("Buffering Enabled")
        bufferingenabled_layout.setCheckState(Qt.CheckState.Checked)
        return bufferingenabled_layout
        

