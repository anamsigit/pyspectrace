import sys
import os
import numpy as np
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
    QFileDialog, QLabel, QProgressBar, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

def extract_data_from_file(file_path):
    wavelengths = []
    intensities = []
    deltatimes = []
    times = []
    spectral_data_started = False
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):
            if '>>>>>Begin Processed Spectral Data<<<<<' in line:
                spectral_data_started = True
                continue
            if '>>>>>End Processed Spectral Data<<<<<' in line:
                break
            if spectral_data_started:
                # wavelength, intensity = map(float, line.split())
                data = line.split()

                wavelength = float(data[0])
                wavelengths.append(wavelength)
                
                intensity = float(data[1])
                intensities.append(intensity)
                
                try:
                    deltatime = float(data[2])
                except:
                    deltatime = 1
                deltatimes.append(deltatime)

                try:
                    time = data[4]
                except:
                    time = i
                times.append(time)
            else:
                try:
                    data = line.split()

                    wavelength = float(data[0])
                    wavelengths.append(wavelength)
                    
                    intensity = float(data[1])
                    intensities.append(intensity)
                    
                    try:
                        deltatime = float(data[2])
                    except:
                        deltatime = 1
                    deltatimes.append(deltatime)

                    try:
                        time = data[4]
                    except:
                        time = i
                    times.append(time)
                except:
                    pass

    return np.array(wavelengths), np.array(intensities), np.array(deltatimes), np.array(times)


class ConversionThread(QThread):
    progress_update = pyqtSignal(int)
    conversion_complete = pyqtSignal(bool, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        all_frame = []
        all_wavelengths = []
        all_intensities = []
        all_deltatimes = []
        all_times = []

        txt_files = sorted(
            [f for f in os.listdir(self.folder_path) if f.endswith(".txt")],
            key=lambda x: int(re.findall(r'\d+', x.split('-')[0])[0])
            )

        total_files = len(txt_files)
        for i, filename in enumerate(txt_files):
            file_path = os.path.join(self.folder_path, filename)
            wavelengths, intensities, deltatimes, times = extract_data_from_file(file_path)
            # print(wavelengths)
            # print(deltatimes)

            all_frame.append(i)
            all_wavelengths.append(wavelengths)
            all_intensities.append(intensities)
            all_times.append(times[0])

            all_deltatimes.append(deltatimes[0])
            # if i == 0:
            #     all_deltatimes.append(deltatimes[0])
            # if i > 0:
            #     all_deltatimes.append(all_deltatimes[i-1] + deltatimes[0])

            progress = int((i + 1) / total_files * 100)
            self.progress_update.emit(progress)

        all_frame = np.array(all_frame)
        all_intensities = np.array(all_intensities)
        all_wavelengths = np.array(all_wavelengths)
        all_deltatimes = np.array(all_deltatimes)
        all_times = np.array(all_times)

        if all_wavelengths.ndim == 2:
            ones_wavelengths = all_wavelengths[0]
        else:
            ones_wavelengths = all_wavelengths

        self.conversion_complete.emit(True, all_frame, ones_wavelengths, all_intensities, all_deltatimes, all_times)

class ConvertControl(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Converter")
        self.folder_path = None
        self.converted_data = None

        # Main layout
        layout = QVBoxLayout()

        # Button to select folder containing .txt files
        self.select_folder_button = QPushButton("Select Directory Containing .txt")
        self.select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_button)

        # Button to start conversion process
        self.convert_button = QPushButton("Start Convert")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_button)

        # Progress bar to show conversion progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory Containing .txt", "")
        if folder:
            self.folder_path = folder
            self.select_folder_button.setText(os.path.basename(folder))
            self.convert_button.setEnabled(True)

    def start_conversion(self):
        self.progress_bar.setValue(0)
        self.convert_button.setEnabled(False)

        # Start the conversion in a separate thread
        self.thread = ConversionThread(self.folder_path)
        self.thread.progress_update.connect(self.update_progress)
        self.thread.conversion_complete.connect(self.conversion_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self, success, frames, wavelengths, intensities, deltatimes, times):
        if success:
            self.progress_bar.setValue(100)
            self.save_converted_file(frames, wavelengths, intensities, deltatimes, times)
        else:
            QMessageBox.critical(self, "Error", "Conversion failed!")
        self.convert_button.setEnabled(True)

    def save_converted_file(self, frames, wavelengths, intensities, deltatimes, times):
        initial_path = self.folder_path if self.folder_path else ""
        save_file, _ = QFileDialog.getSaveFileName(self, "Save Converted File", os.path.join(os.path.dirname(initial_path), "Converted_Spectrum"), "NPZ Files (*.npz);;All Files (*)")
        
        if save_file:
            if not save_file.endswith('.npz'):
                save_file += '.npz'
            np.savez(save_file, frame=frames, wavelengths=wavelengths, intensities=intensities, deltatime=deltatimes, time=times)
            # np.savez_compressed(save_file, frame=frames, wavelengths=wavelengths, intensities=intensities, deltatimes=deltatimes, times=times)


# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConvertControl()
    window.show()
    sys.exit(app.exec_())
