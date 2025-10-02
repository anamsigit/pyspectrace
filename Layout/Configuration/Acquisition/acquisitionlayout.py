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
    QColorDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from .Communication.communicationlayout import CommunicationLayout
from .Saving.savinglayout import SavingLayout
from .Info.infolayout import InfoLayout


class AcquisitionLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Tab Communication
        self.communicationlayout = CommunicationLayout(self)

        # # Tab Saving
        self.savinglayout = SavingLayout(self)

        # # Tab info
        infolayout = InfoLayout(self)


        # Menambahkan nestab bertingkat ke tab induk
        nested_tab_configuration = QTabWidget()
        nested_tab_configuration.addTab(self.communicationlayout.nested_tabs, 'Communication')
        nested_tab_configuration.addTab(self.savinglayout.nested_tabs, 'Saving')
        nested_tab_configuration.addTab(infolayout.nested_tabs, 'Info')

        main_layout = QVBoxLayout()
        # main_layout.addWidget(self.BufferingEnabled())
        main_layout.addWidget(self.output())
        main_layout.addWidget(nested_tab_configuration)
        self.setLayout(main_layout)

    def output(self):
        self.output_spectrum_option = QComboBox()
        self.output_spectrum_option.addItems(['Raw', 'Transmision', 'Absorbance'])

        group_box_output_spectrum_option_layout = QVBoxLayout()
        group_box_output_spectrum_option_layout.addWidget(self.output_spectrum_option)

        group_box_output_spectrum_option = QGroupBox('Output')
        group_box_output_spectrum_option.setLayout(group_box_output_spectrum_option_layout)
        return group_box_output_spectrum_option
    
    def BufferingEnabled(self):
        bufferingenabled = QCheckBox("Buffering Enabled")
        bufferingenabled.setCheckState(Qt.CheckState.Checked)
        return bufferingenabled
    
