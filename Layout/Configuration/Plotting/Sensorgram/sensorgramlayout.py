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
    QColorDialog, QDoubleSpinBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SensorgramLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.nested_tabs = QWidget()
        self.nested_tabs_layout = QVBoxLayout()

        # self.reset_button = QPushButton("Reset", self)
        # self.savesensorgram = QPushButton("Save sensorgram", self)
        # self.plotsensorgram = QPushButton("Plot sensorgram", self)

        self.select_time_unit = QComboBox()
        sensorgramdata = self.SensorgramData()
        sensorgramscalling = self.SensorgramScalling()
    

        self.nested_tabs_layout.addWidget(sensorgramdata)
        self.nested_tabs_layout.addWidget(sensorgramscalling)
        # self.nested_tabs_layout.addWidget(self.select_time_unit)

        self.nested_tabs_layout.addStretch()
        self.nested_tabs.setLayout(self.nested_tabs_layout)

    def SensorgramScalling(self):
        groupBox = QGroupBox("View scalling")

        hboxLayout_range = QHBoxLayout()
        hboxLayout_autoscale = QHBoxLayout()

        self.autoscale_y = QPushButton("Fit descriptor")
        self.autoscale_x = QPushButton("Fit time")
        self.update_fixed_range = QPushButton("Fit")
        # self.update_fixed_range_merge = QPushButton("Merge")

        self.min_range_input = QDoubleSpinBox()
        self.min_range_input.setDecimals(3)
        self.min_range_input.setRange(-1000000, 1000000)
        self.min_range_input.setDisabled(True)
        
        self.max_range_input = QDoubleSpinBox()
        self.max_range_input.setDecimals(3)
        self.max_range_input.setRange(-1000000, 1000000)
        self.max_range_input.setDisabled(True)

        min_label = QLabel("Low. :")
        max_label = QLabel("Upp. :")
        hboxLayout_range.addWidget(min_label)
        hboxLayout_range.addWidget(self.min_range_input)
        hboxLayout_range.addWidget(max_label)
        hboxLayout_range.addWidget(self.max_range_input)
        hboxLayout_range.addWidget(self.update_fixed_range) 
        # hboxLayout_range.addWidget(self.update_fixed_range_merge) 

        hboxLayout_autoscale.addWidget(self.autoscale_x)
        hboxLayout_autoscale.addWidget(self.autoscale_y)

        vboxLayout = QVBoxLayout()
        
        vboxLayout.addLayout(hboxLayout_autoscale) 
        vboxLayout.addLayout(hboxLayout_range) 
        # vboxLayout.addWidget(self.update_fixed_range_merge) 

        groupBox.setLayout(vboxLayout)
        return groupBox

    def SensorgramData(self):
        groupBox = QGroupBox("Sensorgram data")

        hboxLayout = QHBoxLayout()
        hboxLayout_time_unit = QHBoxLayout()

        self.select_time_unit.addItems(['Milisecond', 'Second', 'Minute'])
        self.select_time_unit.setCurrentText('Second')
        time_unit = QLabel("Time unit: ")

        hboxLayout_time_unit.addWidget(time_unit)
        hboxLayout_time_unit.addWidget(self.select_time_unit)

        self.reset_button = QPushButton("Reset", self)
        self.savesensorgram = QPushButton("Save", self)
        self.plotsensorgram = QPushButton("Plot", self)

        hboxLayout.addWidget(self.reset_button)
        hboxLayout.addWidget(self.savesensorgram)
        hboxLayout.addWidget(self.plotsensorgram)

        vboxLayout = QVBoxLayout()
        
        vboxLayout.addLayout(hboxLayout) 
        vboxLayout.addLayout(hboxLayout_time_unit) 

        groupBox.setLayout(vboxLayout)
        return groupBox