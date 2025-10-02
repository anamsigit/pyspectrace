from PyQt5.QtCore import QTimer
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout
import time
import pyqtgraph as pg
import random

class SpectrumControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view       

        self.start_time = datetime.now()
        self.current_forprogress = 0
        self.elapsed_time = 0

        self.start_time_foraccumulated = datetime.now()
        self.current_foraccumulated = 0

        self.accumulated_wavelengths = []
        self.accumulated_intensities = []
        self.accumulated_second = []

        self.state_accumulated = False
        self.view.configurationlayout.plottinglayout.spectrumlayout.start_acquire.setEnabled(True)
        self.view.configurationlayout.plottinglayout.spectrumlayout.pause_acquire.setEnabled(False)
        self.view.configurationlayout.plottinglayout.spectrumlayout.restart.clicked.connect(self.show_confirmation)
        self.view.configurationlayout.plottinglayout.spectrumlayout.plot.clicked.connect(self.plot)
        self.view.configurationlayout.plottinglayout.spectrumlayout.start_acquire.clicked.connect(self.truestate)
        self.view.configurationlayout.plottinglayout.spectrumlayout.pause_acquire.clicked.connect(self.falsestate)

        self.view.configurationlayout.plottinglayout.spectrumlayout.fit_interest_x.clicked.connect(
            self.view.plottinglayout.spectrumlayout.autoscale_x)
        self.view.configurationlayout.plottinglayout.spectrumlayout.fit_interest_y.clicked.connect(
            self.view.plottinglayout.spectrumlayout.autoscale_y)
    
    def truestate(self):
        self.state_accumulated = True
        self.view.configurationlayout.plottinglayout.spectrumlayout.start_acquire.setEnabled(False)
        self.view.configurationlayout.plottinglayout.spectrumlayout.pause_acquire.setEnabled(True)

    def falsestate(self):
        self.state_accumulated = False
        self.view.configurationlayout.plottinglayout.spectrumlayout.start_acquire.setEnabled(True)
        self.view.configurationlayout.plottinglayout.spectrumlayout.pause_acquire.setEnabled(False)

    def mainloop(self):
        if self.state_accumulated:
            _current_time = datetime.now()
            self.elapsed_time = (_current_time - self.start_time).total_seconds()
            interval = self.view.configurationlayout.plottinglayout.spectrumlayout.interval_acquire.value()
            progress_percent = min(int((self.elapsed_time / interval) * 100), 100)
            self.view.configurationlayout.plottinglayout.spectrumlayout.progress.setValue(progress_percent)
            if self.elapsed_time >= self.view.configurationlayout.plottinglayout.spectrumlayout.interval_acquire.value():
                self.intervalstart()
                self.accumulated_second.append((_current_time - self.start_time_foraccumulated).total_seconds())
                self.accumulating_spectrum()
                self.start_time = _current_time
                self.view.configurationlayout.plottinglayout.spectrumlayout.progress.setValue(0)
        else:
            _current_time = datetime.now()
            self.start_time = _current_time - timedelta(seconds=self.elapsed_time)
            
    def spectrum_data(self):
        spectrum = [
                self.view.plottinglayout.spectrumlayout.wavelengths,
                self.view.plottinglayout.spectrumlayout.intensities,
                ]
        return spectrum[0][0], spectrum[1][0]

    def intervalstart(self):
        self.current_time = datetime.now()

    def accumulating_spectrum(self):
        wavelengths, intensities = self.spectrum_data()
        self.accumulated_wavelengths.append(wavelengths)
        self.accumulated_intensities.append(intensities)
        self.view.configurationlayout.plottinglayout.spectrumlayout.sum.setText(f"{len(self.accumulated_intensities)}")

    def show_confirmation(self):
        reply = QMessageBox.question(self.view, 'Info', 'Are you sure to reset plot?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.restart()

    def restart(self):
        self.accumulated_wavelengths = []
        self.accumulated_intensities = []
        self.view.configurationlayout.plottinglayout.spectrumlayout.sum.setText(f"{len(self.accumulated_intensities)}")

    def plot(self):
        self.window = pg.GraphicsLayoutWidget(show=True, title="Spectrum Over Time")
        self.window.setBackground('w')
        self.plotting = self.window.addPlot()
        self.plotting.addLegend()
        for i, (wavelengths, intensities) in enumerate(zip(self.accumulated_wavelengths, self.accumulated_intensities)):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pen = pg.mkPen(color=color, width=1)
            self.plotting.plot(wavelengths, intensities, pen=pen, name=f"{self.accumulated_second[i]:.2f} second")
            