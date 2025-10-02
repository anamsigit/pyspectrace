import sys
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import matplotlib.pyplot as plt
import seatease.cseatease as spectro
from matplotlib.figure import Figure
from PyQt5.QtGui import QTextDocument, QDoubleValidator, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QSpinBox, QDoubleSpinBox, QAction, QCheckBox, 
    QFileDialog, QComboBox, QGroupBox, QLineEdit, QFormLayout, QTableWidget,
    QColorDialog, QTextEdit, QProgressBar
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt
import os
import re

class SavingLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.text_edit = QTextEdit(self)
        self.document = QTextDocument() 
        self.status_saving = False
        self.inittime_save = ""
        self.initUI()


    def initUI(self):
        self.nested_tabs = QWidget()
        self.nested_tabs_layout = QVBoxLayout()
        enable_record_checkbox = self.EnableRecordCheckbox()
        interval_saving_layout = self.IntervalSaving()
        folder_button = self.SavingFolderName()
        experiment_layout = self.SavingNameFile()
        savingnamefilecombined = self.SavingNameFileCombined()
        apply_button = self.ApplyButtonHBox()

        # Tambahkan widget lain dan elemen layout lainnya
        self.nested_tabs_layout.addWidget(enable_record_checkbox)
        self.nested_tabs_layout.addWidget(folder_button)
        # self.nested_tabs_layout.addWidget(file_name_label)
        self.nested_tabs_layout.addLayout(experiment_layout)  # Perbaikan di sini
        self.nested_tabs_layout.addLayout(savingnamefilecombined)
        self.nested_tabs_layout.addLayout(interval_saving_layout)
        self.nested_tabs_layout.addLayout(apply_button)
        self.nested_tabs_layout.addStretch()

        # Set layout utama ke QWidget
        self.nested_tabs.setLayout(self.nested_tabs_layout)
    
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.selectedfolder_path)
        if folder:
            # self.folder_button.setText(folder)
            self.selectedfolder_path = folder
            self.update_combined_text()

    def update_combined_text(self):
        folder_path = self.selectedfolder_path
        experiment_text = self.experiment_line_edit.text()
        conditions_text = self.conditions_line_edit_1.text()

        # Membersihkan teks dari karakter yang tidak diperbolehkan
        experiment_text = re.sub(r'[^\w\-]', '_', experiment_text)
        conditions_text = re.sub(r'[^\w\-]', '_', conditions_text)
        
        self.combined_path_text = os.path.join(folder_path, f"{self.inittime_save}-{experiment_text}-{conditions_text}")
        self.document.setPlainText(self.combined_path_text)
        self.text_edit.setAlignment(Qt.AlignCenter)
    


    def toggle_editability(self):
        is_enabled = self.enable_record_checkbox.isChecked()
        if is_enabled == False:
            self.status_saving = False
            self.pixmap = QPixmap(".\Layout\Configuration\Acquisition\Saving\iconrecordoff.png")  # Ganti dengan path gambar/icon Anda
            self.pixmap = self.pixmap.scaled(23, 23)
            self.icon_label.setPixmap(self.pixmap)
        self.folder_button.setEnabled(is_enabled)
        self.experiment_line_edit.setEnabled(is_enabled)
        self.conditions_line_edit_1.setEnabled(is_enabled)
        self.apply_button.setEnabled(is_enabled)
        self.syncsensorgram.setEnabled(is_enabled)
        self.pauseresumebuttom.setEnabled(is_enabled)
        # self.saving_npz.setEnabled(is_enabled)
        self.interval_saving.setEnabled(is_enabled)
        self.progress.setValue(0)
        self.progress.setMaximum(100)
        # self.progress.setMaximum(1000)

        
    def apply_action(self):
        # Disable editing of experiment, conditions, and folder selection after applying
        self.experiment_line_edit.setEnabled(False)
        self.interval_saving.setEnabled(False)
        # self.saving_npz.setEnabled(False)
        self.conditions_line_edit_1.setEnabled(False)
        self.folder_button.setEnabled(False)
        self.syncsensorgram.setEnabled(False)
        self.apply_button.setEnabled(False)

    def EnableRecordCheckbox(self):
        self.enable_record_checkbox = QCheckBox("Enable record spectrum")
        self.enable_record_checkbox.stateChanged.connect(self.toggle_editability)
        return self.enable_record_checkbox

    def SavingFolderName(self):
        self.selectedfolder_path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'data')
        self.folder_button = QPushButton("Select Foldeer")
        self.folder_button.setEnabled(False)
        self.folder_button.clicked.connect(self.select_folder)
        return self.folder_button

    def SavingNameFile(self):
        # File Name Label
        self.file_name_label = QLabel("File name")
        self.file_name_label.setStyleSheet("font-weight: bold;")

        # Experiment Section
        self.experiment_form_layout = QFormLayout()
        self.experiment_label = QLabel("Filename:")
        self.experiment_label.setAlignment(Qt.AlignCenter)
        self.experiment_line_edit = QLineEdit("")
        self.experiment_line_edit.setEnabled(False)
        self.experiment_form_layout.addRow(self.experiment_label, self.experiment_line_edit )
        
        # Conditions Section
        self.conditions_form_layout = QFormLayout()
        self.conditions_label = QLabel("Label :")
        self.conditions_label.setAlignment(Qt.AlignCenter)
        self.conditions_line_edit_1 = QLineEdit("")
        self.conditions_line_edit_1.setEnabled(False)
        self.conditions_form_layout.addRow(self.conditions_label,self.conditions_line_edit_1)


        self.update_combined_text()  # Initial update
        
        # Layout for Experiment and Conditions
        self.experiment_layout = QVBoxLayout()
        # self.experiment_layout.addWidget(self.experiment_label)
        # self.experiment_layout.addWidget(self.experiment_line_edit)
        self.experiment_layout.addLayout(self.experiment_form_layout)
        self.experiment_layout.addLayout(self.conditions_form_layout)
        # self.experiment_layout.addWidget(self.conditions_label)
        # self.experiment_layout.addWidget(self.conditions_line_edit_1)

        self.experiment_line_edit.textChanged.connect(self.update_combined_text)
        self.conditions_line_edit_1.textChanged.connect(self.update_combined_text)
        self.folder_button.clicked.connect(self.update_combined_text)

        # return self.file_name_label, self.experiment_layout
        return self.experiment_layout

    def SavingNameFileCombined(self):
        self.experiment_layout_combined = QVBoxLayout()     
        self.text_edit.setDocument(self.document)
        self.text_edit.setReadOnly(True)
        self.text_edit.setAlignment(Qt.AlignCenter)
        label = QLabel("Preview save path")
        self.experiment_layout_combined.addWidget(label)
        self.experiment_layout_combined.addWidget(self.text_edit)
        self.experiment_layout_combined.setAlignment(Qt.AlignCenter)

    #     self.group_box = QGroupBox("Preview Path Saving")
    #     self.group_box.setLayout(QVBoxLayout())
    #     self.group_box.layout().addWidget(self.text_edit)
        
    # # Create the main layout for the function
    #     self.experiment_layout_combined = QVBoxLayout()
    #     self.experiment_layout_combined.addWidget(self.group_box)

        return self.experiment_layout_combined
    
    def IntervalSaving(self):
        interval_saving_layout = QHBoxLayout()

        interval_saving_label = QLabel("Saving interval (s) :", self)
        self.interval_saving = QDoubleSpinBox(self)
        self.interval_saving.setRange(0, 1000)
        self.interval_saving.setEnabled(False)
        self.interval_saving.setValue(1)

        self.progress = QProgressBar(self)
        self.progress.setTextVisible(False)

        interval_saving_layout.addWidget(interval_saving_label,4)
        interval_saving_layout.addWidget(self.interval_saving, 5)
        interval_saving_layout.addWidget(self.progress,3)
        return interval_saving_layout

    
    def ApplyButtonHBox(self):
        self.hboxlayout = QHBoxLayout() 
        self.pauseresumebuttom = QPushButton("Pause")
        self.pauseresumebuttom.setEnabled(False)
        
        self.syncsensorgram = QCheckBox("syc. snsrgrm")
        self.syncsensorgram.setChecked(False)
        self.syncsensorgram.setEnabled(False)

        self.saving_txt = QCheckBox(".txt")
        self.saving_txt.setChecked(True)
        self.saving_txt.setEnabled(False)   
        
        self.apply_button = QPushButton("Record")
        self.apply_button.clicked.connect(self.apply_action)
        self.apply_button.clicked.connect(self.StartRecord)
        self.apply_button.setEnabled(False)      
        # self.apply_button.setIcon(QIcon('.\Layout\Configuration\Acquisition\Saving\iconrecording.png'))

        self.icon_label = QLabel()
        self.pixmap = QPixmap(".\Layout\Configuration\Acquisition\Saving\iconrecordoff.png")  # Ganti dengan path gambar/icon Anda
        self.pixmap = self.pixmap.scaled(23, 23)
        self.icon_label.setPixmap(self.pixmap)

        self.hboxlayout.addWidget(self.saving_txt)
        self.hboxlayout.addWidget(self.syncsensorgram)
        # self.hboxlayout.addWidget(self.saving_npz)
        # self.hboxlayout.addWidget(self.saving_interval)
        self.hboxlayout.addWidget(self.apply_button, 6)
        self.hboxlayout.addWidget(self.pauseresumebuttom, 3)
        self.hboxlayout.addWidget(self.icon_label, 1)
        return self.hboxlayout
    
    def StartRecord(self):
        self.status_saving = True
        self.pixmap = QPixmap(".\Layout\Configuration\Acquisition\Saving\iconrecordon.png")  # Ganti dengan path gambar/icon Anda
        self.pixmap = self.pixmap.scaled(23, 23)  # Skalakan gambar ke ukuran 32x32 piksel
        self.icon_label.setPixmap(self.pixmap)
        