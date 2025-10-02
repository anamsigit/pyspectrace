from PyQt5.QtCore import QTimer
import numpy as np
from datetime import datetime
import os
from PyQt5.QtWidgets import (
    QFileDialog, QMessageBox
)

class DarkSpectrumControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.wavelengths = np.array([])
        self.intensities = np.array([])
        self.dark_wavelengths = np.array([])
        self.dark_intensities = np.array([])
        self.mainpath = os.path.dirname(os.path.dirname(os.getcwd()))

    def saving(self):
        if len(self.dark_intensities) != 0:
            current_time = datetime.now()
            default_filename = f'{current_time.strftime("%Y-%m-%d_%H-%M-%S_%f")}_darkspectrum.npz'
            default_path = os.path.join(self.mainpath, 'data', default_filename)
            save_path, _ = QFileDialog.getSaveFileName(
                None, 
                "Save File", 
                default_path, 
                "NPZ Files (*.npz)"
            )
            np.savez(save_path, wavelengths=np.array(self.wavelengths), intensities=np.array(self.intensities))
    
    def load(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", os.path.join(self.mainpath, 'data') , "NPZ Files (*.npz)")
        if file_path:
            data = np.load(file_path)
            self.wavelengths = data['wavelengths']
            self.intensities = data['intensities']
            
        self.update()
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.dark_plot_spectrum(self.wavelengths, self.intensities)


    def take(self):
        wavelengths, intensities = self.model.acquire_spectrum()
        self.wavelengths = wavelengths
        self.intensities = intensities

        self.update()
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.dark_plot_spectrum(self.wavelengths, self.intensities)
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_dark_button.setEnabled(True)
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_dark_button.setEnabled(False)


    def clear(self):
        self.wavelengths = np.array([])
        self.intensities = np.array([])

        self.update()
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.dark_clear_plot_spectrum(self.wavelengths, self.intensities)
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_dark_button.setEnabled(False)
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_dark_button.setEnabled(True)

    def update(self):
        self.dark_wavelengths = self.wavelengths
        self.dark_intensities = self.intensities 
