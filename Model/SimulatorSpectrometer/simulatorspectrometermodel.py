import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, 
    QWidget, QSlider, QDoubleSpinBox, 
    QHBoxLayout, QLabel, QGroupBox, 
    QCheckBox, QMessageBox, QPushButton, QSpinBox
    )

from PyQt5.QtCore import QTimer, pyqtSignal, QThread, QObject
import time
from pyqtgraph import PlotWidget, plot
import os

class SimulatorSpectrometer(QMainWindow):
    frame_finish_emit = pyqtSignal()
    frame_on_emit = pyqtSignal()
    frame_start_emit = pyqtSignal()
    def __init__(self):  
        super().__init__()

        self.microsecvar = 1000

        self.acquisition_delay_min = 40
        self.acquisition_delay_max = 200
        self.min_source_wav = 400
        self.max_source_wav = 700
        self.min_source_inte = 10
        self.max_source_inte = 200

        self.default_wavx1 = 480
        self.default_wavx2 = 590

        self.delta = int((self.max_source_wav - self.min_source_wav) * 0.10)
        self.peak1_wavelength = self.default_wavx1 - self.delta
        self.peak1_intensity = 1
        self.peak2_wavelength = self.default_wavx2 - self.delta
        self.peak2_intensity = 1

        self.setWindowTitle("Simulator Spectrometer")
        self.setGeometry(100, 100, 400,450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.graph_widget = PlotWidget()
        layout.addWidget(self.graph_widget)
        self.graph_widget.setLabel('left', 'Intensity')
        self.graph_widget.setLabel('bottom', 'Wavelength (nm)')

        self.source_button = QPushButton("Turn on source")
        self.source_on = False
        self.source_button.clicked.connect(self.toggle_source)

        # First peak controls
        peak1_group = QGroupBox("Lorentzian Peak (1) Controls")
        peak1_layout = QVBoxLayout()
        peak1_group.setLayout(peak1_layout)

        self.x1_slider, self.x1_checkbox, self.minx1_slider, self.maxx1_slider = self.create_slider_with_checkbox("Wavelength (nm):", 
                                                                                                                  self.min_source_wav, 
                                                                                                                  self.max_source_wav, 
                                                                                                                  self.default_wavx1)
                                                                                                                #   450)
        self.y1_slider, self.y1_checkbox, self.miny1_slider, self.maxy1_slider= self.create_slider_with_checkbox("Intensity:", 
                                                                                                                 self.min_source_inte, 
                                                                                                                 self.max_source_inte, 
                                                                                                                 100)
        peak1_layout.addWidget(self.x1_slider[0])
        peak1_layout.addWidget(self.y1_slider[0])

        # Second peak controls
        peak2_group = QGroupBox("Gaussian Peak (2) Controls")
        peak2_layout = QVBoxLayout()
        peak2_group.setLayout(peak2_layout)

        self.x2_slider, self.x2_checkbox, self.minx2_slider, self.maxx2_slider = self.create_slider_with_checkbox("Wavelength (nm):", 
                                                                                                                  self.min_source_wav, 
                                                                                                                  self.max_source_wav, 
                                                                                                                  self.default_wavx2)
                                                                                                                #   600)
        self.y2_slider, self.y2_checkbox, self.miny2_slider, self.maxy2_slider = self.create_slider_with_checkbox("Intensity:", 
                                                                                                                  self.min_source_inte, 
                                                                                                                  self.max_source_inte, 
                                                                                                                  100)
        peak2_layout.addWidget(self.x2_slider[0])
        peak2_layout.addWidget(self.y2_slider[0])

        # Peak noise
        peaknoise_group = QGroupBox("Noise level")
        peaknoise_layout = QVBoxLayout()
        peaknoise_group.setLayout(peaknoise_layout)

        self.noise_value = 1
        self.integration_time = 100

        
        self.widget_noise_value = QDoubleSpinBox()
        self.widget_noise_value.setRange(0.00, 100.0)
        self.widget_noise_value.setDecimals(2) 
        self.widget_noise_value.setSingleStep(0.01)
        self.widget_noise_value.setValue(self.noise_value)
        self.widget_noise_value.valueChanged.connect(self.update_noise_value)
        
        peaknoise_layout.addWidget(self.widget_noise_value)


        layout.addWidget(self.source_button)
        layout.addWidget(peak1_group)
        layout.addWidget(peak2_group)
        layout.addWidget(peaknoise_group)

        self.wavelengths_simulator = np.linspace(self.min_source_wav, self.max_source_wav, 1000)
        # delta = int((self.max_source_wav - self.min_source_wav) * 0.10)
        
        self.curve = self.graph_widget.plot(self.wavelengths_simulator, self.generate_data())

        self.timer = QTimer()
        self.timer.setInterval(250)  # Update every 50 ms
        # self.timer.setInterval(50)  # Update every 50 ms
        self.timer.timeout.connect(self.update_plot)
        self.timer.timeout.connect(self.update_source)
        self.timer.start()

        self.x1_slider[1].valueChanged.connect(lambda value: self.update_param('peak1_wavelength', value))
        self.y1_slider[1].valueChanged.connect(lambda value: self.update_param('peak1_intensity', value))
        self.x2_slider[1].valueChanged.connect(lambda value: self.update_param('peak2_wavelength', value))
        self.y2_slider[1].valueChanged.connect(lambda value: self.update_param('peak2_intensity', value))

        self.sim_timer = QTimer()
        self.sim_timer.setInterval(200)  # Update simulation every 50 ms
        # self.sim_timer.setInterval(50)  # Update simulation every 50 ms
        self.sim_timer.timeout.connect(self.update_simulation)
        self.sim_timer.start()

        self.sim_directions = {'x1': 1, 'y1': 1, 'x2': 1, 'y2': 1}  # Individual directions for each parameter

        self.wavelengths = np.array(self.wavelengths_simulator)
        self.intensities = np.array(self.generate_data())
        
        self.integration_min = 100
        self.integration_max = 200000

        self.current_frame_index = 0

        self.upper_frame = 1
        self.lower_frame = 0

        self.frame_on_emit.emit()
    
    def get_model(self):
        return "Simulator spectrometer"

    def get_minimum_integration_time(self):
        return self.integration_min
    
    def get_maximum_integration_time(self):
        return self.integration_max
    
    def get_acquisition_delay_maximum(self):
        return self.acquisition_delay_max

    def get_acquisition_delay_minimum(self):
        return self.acquisition_delay_min

    def set_acquisition_delay(self, acquisition_delay):
        self.acquisition_delay = acquisition_delay
        self.sim_timer.setInterval(self.acquisition_delay) 
        self.timer.setInterval(self.acquisition_delay)
    
    def start(self):
        self.show()
    
    def mainloop(self):
        pass
            
    def acquire_spectrum_for_normalization(self):
        self.dataready = False               
        self.wavelengths = np.array(self.wavelengths_simulator)
        self.intensities = np.array(self.generate_data())
        return self.wavelengths, self.intensities
    
    def acquire_spectrum_from_normalization(self, wavelengths, intensities):       
        self.wavelengths = wavelengths
        self.intensities = intensities
        return self.wavelengths, self.intensities
    
    def acquire_spectrum(self):
        self.wavelengths = self.wavelengths
        self.intensities = self.intensities
        return self.wavelengths, self.intensities
    
    def set_integration_time(self, integration_time):
        self.integration_time = integration_time

    def create_slider_with_checkbox(self, 
                                    label, 
                                    min_val, 
                                    max_val,
                                    default_val):
        self.delta = int((max_val - min_val) * 0.10)
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        slider = QSlider()
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val - self.delta)

        slider.setOrientation(1)  # Horizontal
        layout.addWidget(slider)
        checkbox = QCheckBox("Auto")
        layout.addWidget(checkbox)
        max_label = QLabel("Max")
        min_label = QLabel("Min")
        minspin = QSpinBox(self)
        maxspin = QSpinBox(self)


        minspin.setRange(min_val, max_val)
        maxspin.setRange(min_val, max_val)
        maxspin.setValue(default_val + self.delta)
        minspin.setValue(default_val - self.delta)

        layout.addWidget(minspin)
        layout.addWidget(min_label)
        layout.addWidget(maxspin)
        layout.addWidget(max_label)


        container = QWidget()
        container.setLayout(layout)
        return (container, slider), checkbox, minspin, maxspin

    def generate_data(self):
        peak1 = self.peak1_intensity / (1 + ((self.wavelengths_simulator - self.peak1_wavelength) / 10)**2)
        peak2 = self.peak2_intensity * np.exp(-((self.wavelengths_simulator - self.peak2_wavelength)**2) / (2 * 10**2))

        if self.source_on:
            merged = self.integration_time + ((peak1 + peak2) * self.integration_time)
        else:
            merged = np.random.normal(0, self.noise_value * 0.1, self.wavelengths_simulator.shape)

        return merged + np.random.normal(0, self.noise_value, self.wavelengths_simulator.shape)
    
    def toggle_source(self):
        if self.source_button.text() == "Turn on source":
            self.source_button.setText("Turn off source")
            self.source_on = True
        else:
            self.source_button.setText("Turn on source")
            self.source_on = False
    
    def update_source(self):
        self.source_on = self.source_on 

    def update_plot(self):
        self.curve.setData(self.wavelengths_simulator, self.generate_data())
    
    def update_noise_value(self):
        self.noise_value = self.widget_noise_value.value()

    def update_param(self, param, value):
        if param.endswith('wavelength'):
            setattr(self, param, value)
        elif param.endswith('intensity'):
            setattr(self, param, value / 100)

    def update_simulation(self):
        step_size = 1  # Adjust this to change the speed of scanning

        self.update_slider_auto('x1', self.x1_slider[1], self.x1_checkbox, 'peak1_wavelength', self.minx1_slider.value(), self.maxx1_slider.value(), step_size)
        self.update_slider_auto('y1', self.y1_slider[1], self.y1_checkbox, 'peak1_intensity', self.miny1_slider.value(), self.maxy1_slider.value(), step_size)
        self.update_slider_auto('x2', self.x2_slider[1], self.x2_checkbox, 'peak2_wavelength', self.minx2_slider.value(), self.maxx2_slider.value(), step_size)
        self.update_slider_auto('y2', self.y2_slider[1], self.y2_checkbox, 'peak2_intensity', self.miny2_slider.value(), self.maxy2_slider.value(), step_size)

    def update_slider_auto(self, key, slider, checkbox, param, min_val, max_val, step_size):
        if checkbox.isChecked():
            slider = slider
            current_value = slider.value()


            new_value = current_value + step_size * self.sim_directions[key]
            
            if new_value >= max_val or new_value <= min_val:
                self.sim_directions[key] *= -1  # Reverse direction
                new_value = current_value + step_size * self.sim_directions[key]
            
            if not (min_val - 1 < current_value < max_val + 1):
                slider.setValue(int(min_val))
            else:
                slider.setValue(int(new_value))
            

            self.update_param(param, new_value)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Warning",
            "Are you sure want to close this window?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()  # Izinkan keluar
        else:
            event.ignore()  # Batalkan keluar
