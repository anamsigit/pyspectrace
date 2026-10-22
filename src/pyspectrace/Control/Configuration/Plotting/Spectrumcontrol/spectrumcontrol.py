from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
import random

class SpectrumControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view       

        self.frame_count = 0

        self.accumulated_wavelengths = []
        self.accumulated_intensities = []
        self.accumulated_frames = []  # Menyimpan informasi frame untuk legenda plot

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
            self.frame_count += 1
            interval = self.view.configurationlayout.plottinglayout.spectrumlayout.interval_acquire.value()
            
            # Menghitung persentase progress bar berdasarkan frame count vs interval
            progress_percent = min(int((self.frame_count / interval) * 100), 100) if interval > 0 else 100
            self.view.configurationlayout.plottinglayout.spectrumlayout.progress.setValue(progress_percent)
            
            if self.frame_count >= interval:
                self.accumulating_spectrum()
                self.accumulated_frames.append(self.frame_count)
                self.frame_count = 0  # Reset frame counter untuk interval berikutnya
                self.view.configurationlayout.plottinglayout.spectrumlayout.progress.setValue(0)
        else:
            pass
            
    def spectrum_data(self):
        spectrum = [
                self.view.plottinglayout.spectrumlayout.wavelengths,
                self.view.plottinglayout.spectrumlayout.intensities,
                ]
        return spectrum[0][0], spectrum[1][0]

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
        self.accumulated_frames = []
        self.frame_count = 0
        self.view.configurationlayout.plottinglayout.spectrumlayout.sum.setText(f"{len(self.accumulated_intensities)}")

    def plot(self):
        self.window = pg.GraphicsLayoutWidget(show=True, title="Spectrum overtime")
        self.window.setBackground('w')
        self.plotting = self.window.addPlot()
        self.plotting.addLegend()
        for i, (wavelengths, intensities) in enumerate(zip(self.accumulated_wavelengths, self.accumulated_intensities)):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pen = pg.mkPen(color=color, width=1)
            # Menyesuaikan label legenda berdasarkan indeks atau akumulasi ke-i
            self.plotting.plot(wavelengths, intensities, pen=pen, name=f"Spectrum {i+1}")