import sys
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import matplotlib.pyplot as plt
import seatease.cseatease as spectro
from matplotlib.figure import Figure
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QSpinBox, QAction, QCheckBox, 
    QFileDialog, QComboBox, QGroupBox, QLineEdit, QFormLayout, QTableWidget,
    QColorDialog, QDialog, QToolBar, QDoubleSpinBox
)

class LorentzianPeakFittingLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label_plot = []
        self.num_fitting = []
        self.num_shiftpeak = []
        self.num_widthpeak = []

        self.name_values = []
        self.status_inverse = []
        self.transform_selected = []
        self.dialog_open = False
        self.method_selected = []
        self.axis_selected = []
        self.min_values_archive = []
        self.max_values_archive = []  
        self.initial_center_values = []

        self.min_values = []
        self.max_values = []        
        self.color_values = []
        self.initUI()

    def initUI(self):
        self.fitting_button = self.createPeakFittingButton()
    

    def createPeakFittingButton(self):
        self.button = QPushButton('Open Fitting Hub', self)
        self.button.clicked.connect(self.show_dialog)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.button)
        box = QGroupBox('Lorentzian')
        box.setLayout(vertical_layout)
        return box
    
    def apply(self):
        self.dialog_open = True
        

    def show_dialog(self):
        self.dialog = QWidget()
        self.dialog.setWindowTitle("Lorentzian Peak Fitting")
        self.setupTableFitting(self.dialog)
        self.dialog.resize(960, 300)
        self.dialog.show()

    def setupTableFitting(self, dialog):
        layout = QVBoxLayout(dialog)
        self.table_widget = QTableWidget(len(self.num_fitting), 9, dialog)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setShowGrid(True)
        self.table_widget.setHorizontalHeaderLabels(['Init center (nm)', '-Δ λ (nm)', '+Δ λ (nm)', 'Axis', 'Descriptor', 'Transform', 'Auto', 'Label', 'Color'])
        layout.addWidget(self.table_widget)

        self.populate_table(self.table_widget)

        self.addRowButton = QPushButton('Add')
        self.removeRowButton = QPushButton('Remove')
        self.applyRowButton = QPushButton('Apply')

        button = QHBoxLayout()
        button.addWidget(self.addRowButton)
        button.addWidget(self.removeRowButton)
        appbutton = QHBoxLayout()
        appbutton.addWidget(self.applyRowButton)
        
        layout.addLayout(button)
        layout.addLayout(appbutton)

        self.addRowButton.clicked.connect(lambda: self.add_row(self.table_widget))
        self.removeRowButton.clicked.connect(lambda: self.remove_row(self.table_widget))
        self.applyRowButton.clicked.connect(self.apply)

        dialog.setLayout(layout)

    def populate_table(self, table_widget):
        table_widget.setRowCount(len(self.num_fitting))
        for i in range(len(self.num_fitting)):
            initial_center = QLineEdit()
            initial_center.setText(self.initial_center_values[i])
            initial_center.setAlignment(Qt.AlignCenter) 
            initial_center.setValidator(QDoubleValidator(float(self.min_values[i]), float(self.max_values[i]), 2))
            initial_center.textChanged.connect(lambda value, row=i: self.update_initial_center(row, value))
            table_widget.setCellWidget(i, 0, initial_center)

            min = QLineEdit()
            min.setText(self.min_values[i])
            min.setAlignment(Qt.AlignCenter) 
            min.setValidator(QDoubleValidator(float(self.min_values[i]), float(self.max_values[i]), 2))
            min.textChanged.connect(lambda value, row=i: self.update_min(row, value))
            table_widget.setCellWidget(i, 1, min)

            max = QLineEdit()
            max.setText(self.max_values[i]) 
            max.setAlignment(Qt.AlignCenter) 
            max.setValidator(QDoubleValidator(float(self.min_values[i]), float(self.max_values[i]), 2))
            max.textChanged.connect(lambda value, row=i: self.update_max(row, value))
            table_widget.setCellWidget(i, 2, max)

            axis_selected = QComboBox()
            axis_selected.addItems(["x", "y"]) 
            axis_selected.setCurrentIndex(self.axis_selected[i])
            axis_selected.setStyleSheet('text-align: center;') 
            axis_selected.currentIndexChanged.connect(lambda index, row=i: self.update_axis(row, index))
            table_widget.setCellWidget(i, 3, axis_selected)

            method = QComboBox()
            method.addItems(["Peak position", "Inflection position"]) 
            method.setCurrentIndex(self.method_selected[i])
            method.setStyleSheet('text-align: center;') 
            method.currentIndexChanged.connect(lambda index, row=i: self.update_method(row, index))
            table_widget.setCellWidget(i, 4, method)

            transform = QComboBox()
            transform.addItems(["f(x) = x", "f(x) = √x", "f(x) = x^2", "f(x) = ln([x])", "f(x) = 1/[x]", "f(x) = 1/2[x]^2", "f(x) = log x"]) 
            transform.setCurrentIndex(self.transform_selected[i])
            transform.setStyleSheet('text-align: center;') 
            transform.currentIndexChanged.connect(lambda index, row=i: self.update_transform(row, index))
            table_widget.setCellWidget(i, 5, transform)

            inverse = QCheckBox()
            inverse.setChecked(self.status_inverse[i])
            inverse.setStyleSheet('text-align: center;')
            inverse.stateChanged.connect(lambda state, row=i: self.update_inverse(row, state))
            table_widget.setCellWidget(i, 6, inverse)

            name = QLineEdit()
            name.setText(self.name_values[i]) 
            name.setAlignment(Qt.AlignCenter) 
            
            name.textChanged.connect(lambda value, row=i: self.update_name(row, value))
            table_widget.setCellWidget(i, 7, name)

            color = QPushButton()
            color.setStyleSheet(f"background-color: {self.color_values[i].name()}")
            color.clicked.connect(lambda _, row=i: self.update_color(row, color))
            table_widget.setCellWidget(i, 8, color)


    def update_inverse(self, row, state):
        self.status_inverse[row] = state == Qt.Checked

    def update_max(self, row, value):
        self.max_values[row] = value

    def update_initial_center(self, row, value):
        self.initial_center_values[row] = value
        
    def update_min(self, row, value):
        self.min_values[row] = value

    def update_transform(self, row, index):
        self.transform_selected[row] = index

    def update_method(self, row, index):
        self.method_selected[row] = index

    def update_axis(self, row, index):
        self.axis_selected[row] = index

    def update_name(self, row, value):
        self.name_values[row] = value

    def update_color(self, row, button):
        color = QColorDialog.getColor(initial=self.color_values[row], parent=self)
        self.color_values[row] = color
        button = self.table_widget.cellWidget(row, 8)
        button.setStyleSheet(f"background-color: {color.name()}")

    def add_row(self, table_widget):
        self.num_fitting.append(None)
        self.num_shiftpeak.append(None)
        self.status_inverse.append(False)  # Tambah status baru (unchecked)
        self.axis_selected.append(0)
        self.method_selected.append(0)
        self.name_values.append('')
        self.transform_selected.append(0)
        self.max_values.append(self.max_values[-1])
        self.min_values.append(self.min_values[-1])
        self.initial_center_values.append(self.initial_center_values[-1])
        self.color_values.append(QColor(*(tuple(np.random.randint(0, 256, size=3)))))

        self.populate_table(table_widget)

    def remove_row(self, table_widget):
        if len(self.num_fitting) > 0:
            self.num_fitting.pop()
            self.num_shiftpeak.pop()
            self.name_values.pop()
            self.max_values.pop()
            self.min_values.pop()
            self.initial_center_values.pop()
            self.axis_selected.pop()
            self.status_inverse.pop() 
            self.transform_selected.pop() 
            self.method_selected.pop()
            self.color_values.pop()
            self.populate_table(table_widget)
        
    def clear_all_fitting(self):
        self.max_values_archive = self.max_values[-1] # kalau habis GA, akan didapatkan GA
        self.min_values_archive = self.min_values[-1]
        self.initial_center_values_archive = self.initial_center_values[-1]
        for _ in range(len(self.num_fitting)):
            self.num_fitting.pop()
            self.num_shiftpeak.pop()
            self.name_values.pop()
            self.max_values.pop()
            self.min_values.pop()
            self.initial_center_values.pop()
            self.axis_selected.pop()
            self.status_inverse.pop() 
            self.transform_selected.pop() 
            self.method_selected.pop()
            self.color_values.pop()
        self.max_values.append(f"{float(self.max_values_archive):.2f}")
        self.min_values.append(f"{float(self.min_values_archive):.2f}")
        self.initial_center_values.append(f"{(float(self.max_values_archive) + float(self.min_values_archive)) / 2:.2f}")

