from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QColor
import pyqtgraph as pg
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QFileDialog
import os
import csv
from datetime import datetime
import time
import numpy as np

class SensorgramControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_time = datetime.now()
        # self.view.configurationlayout.plottinglayout.sensorgramlayout.autoscale_y.clicked.connect(
        #     self.view.plottinglayout.sensorgramlayout.setscale)
        self.view.configurationlayout.plottinglayout.sensorgramlayout.autoscale_y.clicked.connect(
            self.view.plottinglayout.sensorgramlayout.autoscale_y)
        self.view.configurationlayout.plottinglayout.sensorgramlayout.autoscale_x.clicked.connect(
            self.view.plottinglayout.sensorgramlayout.autoscale_x)
        # self.view.configurationlayout.plottinglayout.sensorgramlayout.update_fixed_range.clicked.connect(self.update_fixed_range)
        self.view.configurationlayout.plottinglayout.sensorgramlayout.update_fixed_range.clicked.connect(self.update_fixed_range_merge)
        # self.view.configurationlayout.plottinglayout.sensorgramlayout.update_fixed_range_merge.clicked.connect(self.update_fixed_range_merge)
        self.view.configurationlayout.plottinglayout.sensorgramlayout.reset_button.clicked.connect(self.show_confirmation)
        self.view.configurationlayout.plottinglayout.sensorgramlayout.savesensorgram.clicked.connect(self.savesensorgram)
        self.view.configurationlayout.plottinglayout.sensorgramlayout.plotsensorgram.clicked.connect(self.plotsensorgram)
        self.view.configurationlayout.plottinglayout.sensorgramlayout.select_time_unit.currentIndexChanged.connect(self.time_unit)

        self.inittime = 0
    def mainloop(self):
        x = self.view.plottinglayout.sensorgramlayout.gaussianshiftpeak_list
        if any(val > 600 for row in x for val in row):
            # do something
            print("trigger arduino to take an action!")
        pass


    def time_unit(self):
        if self.view.configurationlayout.plottinglayout.sensorgramlayout.select_time_unit.currentIndex() == 0:
            self.view.plottinglayout.sensorgramlayout.time_unit_update(1/1000)
            self.view.plottinglayout.sensorgramlayout.pI.setLabel('bottom', 'Milisecond (ms)')
        if self.view.configurationlayout.plottinglayout.sensorgramlayout.select_time_unit.currentIndex() == 1:
            self.view.plottinglayout.sensorgramlayout.time_unit_update(1)
            self.view.plottinglayout.sensorgramlayout.pI.setLabel('bottom', 'Time (s)')
        if self.view.configurationlayout.plottinglayout.sensorgramlayout.select_time_unit.currentIndex() == 2:
            self.view.plottinglayout.sensorgramlayout.pI.setLabel('bottom', 'Minute (m)')
            self.view.plottinglayout.sensorgramlayout.time_unit_update(1*60)
    
    def update_fixed_range(self):
        min = self.view.configurationlayout.plottinglayout.sensorgramlayout.min_range_input.value()
        max = self.view.configurationlayout.plottinglayout.sensorgramlayout.max_range_input.value()
        self.view.plottinglayout.sensorgramlayout.setscale_y(min, max)

    def update_fixed_range_merge(self):
        min = self.view.configurationlayout.plottinglayout.sensorgramlayout.min_range_input.value()
        max = self.view.configurationlayout.plottinglayout.sensorgramlayout.max_range_input.value()
        self.view.plottinglayout.sensorgramlayout.mergesetscale_y(min, max)
    
    def plotsensorgram(self):
        descriptor, time, name, color = self.sensorgram_data() 
        descriptor_list = []
        time_list = []
        name_list = []
        color_list = []
        for i in range(len(descriptor)):
            for j in range (len(descriptor[i])):
                descriptor_list.append(descriptor[i][j])
                time_list.append(time[i][j])
                name_list.append(name[i][j])
                color_list.append(color[i][j].name())

        for i in range(len(descriptor_list)):
            plt.figure(figsize=(10, 6))
            plt.plot(time_list[i], descriptor_list[i], label=name_list[i], color=color_list[i])
            plt.legend()
            plt.title(f'Plot for "{name_list[i]}"')
            plt.show()

    def savesensorgram(self):
        descriptor, time, name, color = self.sensorgram_data() 
        descriptor_list = []
        time_list = []
        name_list = []
        color_list = []
        for i in range(len(descriptor)):
            for j in range (len(descriptor[i])):
                descriptor_list.append(descriptor[i][j])
                time_list.append(time[i][j])
                name_list.append(name[i][j])
                color_list.append(color[i][j].name())

        folder = QFileDialog.getExistingDirectory(None, "Pilih Folder untuk Menyimpan CSV")
        if not folder:
            print("Penyimpanan dibatalkan. Tidak ada folder yang dipilih.")
            return
        
        for i in range(len(descriptor_list)):
            file_name = f'{i}{self.current_time.strftime("%Y-%m-%d_%H-%M-%S_%f")}{name_list[i]}.csv'
            file_path = os.path.join(folder, file_name)

            # Tulis data ke file CSV
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Menulis header
                writer.writerow(['Time', 'Descriptor', 'Label', 'Color'])
                
                # Menulis data (loop berdasarkan sub-data `time_list[i]` dan `descriptor_list[i]`)
                for j in range(len(time_list[i])):
                    writer.writerow([time_list[i][j], descriptor_list[i][j], name_list[i], color_list[i]])
            print(f"Data disimpan ke: {file_path}")
        
    


    def show_confirmation(self):
        # reply = QMessageBox.question(self.view, 'Info', 'Are you sure to reset sensorgram?', 
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # if reply == QMessageBox.Yes:
            # self.resetsensorgram()
        self.resetsensorgram()
    
    def resetsensorgram(self):
        self.view.plottinglayout.sensorgramlayout.frame_list_gaussianshiftpeak.clear()
        self.view.plottinglayout.sensorgramlayout.gaussianshiftpeak_list.clear()

        self.view.plottinglayout.sensorgramlayout.frame_list_lorentzianshiftpeak.clear()
        self.view.plottinglayout.sensorgramlayout.lorentzianshiftpeak_list.clear()

        self.view.plottinglayout.sensorgramlayout.frame_list_polynomialshiftpeak.clear()
        self.view.plottinglayout.sensorgramlayout.polynomialshiftpeak_list.clear()

        self.view.plottinglayout.sensorgramlayout.frame_list_polyshiftpeak.clear()
        self.view.plottinglayout.sensorgramlayout.polyshiftpeak_list.clear()

        self.view.plottinglayout.sensorgramlayout.frame_list_polynomialshift.clear()
        self.view.plottinglayout.sensorgramlayout.polynomialshift_list.clear()

        self.view.plottinglayout.sensorgramlayout.frame_list_lorentzianshiftpeakwidth.clear()
        self.view.plottinglayout.sensorgramlayout.lorentzianshiftpeakwidth_list.clear()

        self.view.plottinglayout.sensorgramlayout.frame_list_gaussianshiftpeakwidth.clear()
        self.view.plottinglayout.sensorgramlayout.gaussianshiftpeakwidth_list.clear()

        self.view.plottinglayout.sensorgramlayout.frame_list_polynomialshiftpeakwidth.clear()
        self.view.plottinglayout.sensorgramlayout.polynomialshiftpeakwidth_list.clear()

        self.view.plottinglayout.sensorgramlayout.frame = 0
        self.view.plottinglayout.sensorgramlayout.clearplot_plot_obj()

    def sensorgram_data(self):
        descriptor = [
                self.view.plottinglayout.sensorgramlayout.gaussianshiftpeak_list,
                self.view.plottinglayout.sensorgramlayout.lorentzianshiftpeak_list,
                self.view.plottinglayout.sensorgramlayout.polynomialshiftpeak_list,
                self.view.plottinglayout.sensorgramlayout.polyshiftpeak_list,
                self.view.plottinglayout.sensorgramlayout.polynomialshift_list,
                self.view.plottinglayout.sensorgramlayout.lorentzianshiftpeakwidth_list,
                self.view.plottinglayout.sensorgramlayout.gaussianshiftpeakwidth_list,
                self.view.plottinglayout.sensorgramlayout.polynomialshiftpeakwidth_list,
                ]
        
        time = [
                self.view.plottinglayout.sensorgramlayout.frame_list_gaussianshiftpeak,
                self.view.plottinglayout.sensorgramlayout.frame_list_lorentzianshiftpeak,
                self.view.plottinglayout.sensorgramlayout.frame_list_polynomialshiftpeak,
                self.view.plottinglayout.sensorgramlayout.frame_list_polyshiftpeak,
                self.view.plottinglayout.sensorgramlayout.frame_list_polynomialshift,
                self.view.plottinglayout.sensorgramlayout.frame_list_lorentzianshiftpeakwidth,
                self.view.plottinglayout.sensorgramlayout.frame_list_gaussianshiftpeakwidth,
                self.view.plottinglayout.sensorgramlayout.frame_list_polynomialshiftpeakwidth,
                ]

        name = [
                self.view.plottinglayout.sensorgramlayout.name_gaussianpeakfitting,
                self.view.plottinglayout.sensorgramlayout.name_lorentzianpeakfitting,
                self.view.plottinglayout.sensorgramlayout.name_polynomialpeakfitting,
                self.view.plottinglayout.sensorgramlayout.name_polypeakfitting,
                self.view.plottinglayout.sensorgramlayout.name_polynomialfitting,
                self.view.plottinglayout.sensorgramlayout.name_lorentzianpeakwidthfitting,
                self.view.plottinglayout.sensorgramlayout.name_gaussianpeakwidthfitting,
                self.view.plottinglayout.sensorgramlayout.name_polynomialpeakwidthfitting,
                ]
        
        color = [
                self.view.plottinglayout.sensorgramlayout.color_gaussianshiftpeak,
                self.view.plottinglayout.sensorgramlayout.color_lorentzianshiftpeak,
                self.view.plottinglayout.sensorgramlayout.color_polynomialshiftpeak,
                self.view.plottinglayout.sensorgramlayout.color_polyshiftpeak,
                self.view.plottinglayout.sensorgramlayout.color_polynomialshift,
                self.view.plottinglayout.sensorgramlayout.color_lorentzianshiftpeakwidth,
                self.view.plottinglayout.sensorgramlayout.color_gaussianshiftpeakwidth,
                self.view.plottinglayout.sensorgramlayout.color_polynomialshiftpeakwidth,
            ]
        return descriptor, time, name, color