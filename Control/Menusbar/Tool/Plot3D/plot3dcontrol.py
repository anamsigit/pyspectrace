
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QHBoxLayout, QLabel, QDoubleSpinBox, QSpinBox
)
import matplotlib.pyplot as plt
import numpy as np
import os


class Plot3DControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view

        # self.view.menusbarlayout.toollayout.plot3dlayout.plot_3d_current.triggered.connect(self.mtlib_plot_3d)
        self.view.menusbarlayout.toollayout.plot3dlayout.plot_3d_choosing.triggered.connect(self.plot3dchoosingcontrol)

    def plot3dchoosingcontrol(self):
        self.plot_3d_choosing = Plot3DChoosingControl()
        
    # def mtlib_plot_3d(self):
    #     mainpath = self.view.configurationlayout.acquisitionlayout.savinglayout.combined_path_text
    #     file_path = os.path.join(mainpath, 'raw', 'raw_spectrum.npz')
    #     data = np.load(file_path)
    #     wavelengths = data['wavelengths']
    #     intensities = data['intensities']
    #     frame = data['deltatime']

    #     X, Z = np.meshgrid(wavelengths, frame)
    #     Y = intensities

    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')
    #     ax.plot_surface(X, Z, Y, cmap='viridis')

    #     ax.set_xlabel('Wavelength (nm)')
    #     ax.set_ylabel('Time (s)')
    #     ax.set_zlabel('Value')

    #     fig.show()


class Plot3DChoosingControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plot")
        self.npz_file_path = None

        layout = QVBoxLayout()

        self.file_button = QPushButton("Upload File")
        self.file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.file_button)

        # Wavelength range selection
        wavelength_range_layout = QHBoxLayout()

        # Lower bound (start of wavelength range)
        lower_bound_wavelength_label = QLabel("Min wav:")
        self.lower_bound_wavelength_spinbox = QDoubleSpinBox()
        self.lower_bound_wavelength_spinbox.setSuffix(" nm")
        wavelength_range_layout.addWidget(lower_bound_wavelength_label)
        wavelength_range_layout.addWidget(self.lower_bound_wavelength_spinbox)

        # Upper bound (end of wavelength range)
        upper_bound_wavelength_label = QLabel("Max wav:")
        self.upper_bound_wavelength_spinbox = QDoubleSpinBox()
        self.upper_bound_wavelength_spinbox.setSuffix(" nm")
        wavelength_range_layout.addWidget(upper_bound_wavelength_label)
        wavelength_range_layout.addWidget(self.upper_bound_wavelength_spinbox)

        layout.addLayout(wavelength_range_layout)

        # Frame range selection
        frame_range_layout = QHBoxLayout()

        # Lower bound (start of frame range)
        lower_bound_frame_label = QLabel("Min frame:")
        self.lower_bound_frame_spinbox = QSpinBox()
        frame_range_layout.addWidget(lower_bound_frame_label)
        frame_range_layout.addWidget(self.lower_bound_frame_spinbox)

        # Upper bound (end of frame range)
        upper_bound_frame_label = QLabel("Max frame:")
        self.upper_bound_frame_spinbox = QSpinBox()
        frame_range_layout.addWidget(upper_bound_frame_label)
        frame_range_layout.addWidget(self.upper_bound_frame_spinbox)

        layout.addLayout(frame_range_layout)

        # Plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.setEnabled(False)
        self.plot_button.clicked.connect(self.plot_spectral_data)
        layout.addWidget(self.plot_button)
        layout.addStretch()

        # Set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih File .npz", "", "NPZ Files (*.npz);;All Files (*)", options=options)
        if file_name:
            self.npz_file_path = file_name
            self.plot_button.setEnabled(True)
            self.file_button.setText(os.path.basename(file_name))
            self.update_propertiesspin()
    
    def update_propertiesspin(self):
        npz_data = np.load(self.npz_file_path)
        wavelengths = npz_data['wavelengths']
        frames = npz_data['frame']
        

        # Update wavelength range
        self.lower_bound_wavelength_spinbox.setRange(wavelengths[0], wavelengths[-1])
        self.lower_bound_wavelength_spinbox.setValue(wavelengths[0])
        self.upper_bound_wavelength_spinbox.setRange(wavelengths[0], wavelengths[-1])
        self.upper_bound_wavelength_spinbox.setValue(wavelengths[-1])

        # Update frame range
        self.lower_bound_frame_spinbox.setRange(frames[0], frames[-1])
        self.lower_bound_frame_spinbox.setValue(frames[0])
        self.upper_bound_frame_spinbox.setRange(frames[0], frames[-1])
        self.upper_bound_frame_spinbox.setValue(frames[-1])

    def plot_spectral_data(self):
        # Get wavelength range
        self.lower_bound_wavelength = self.lower_bound_wavelength_spinbox.value()
        self.upper_bound_wavelength = self.upper_bound_wavelength_spinbox.value()

        # Get frame range
        self.lower_bound_frame = self.lower_bound_frame_spinbox.value()
        self.upper_bound_frame = self.upper_bound_frame_spinbox.value()

        npz_data = np.load(self.npz_file_path)
        frame = npz_data['frame']
        wavelengths = npz_data['wavelengths']
        intensities = npz_data['intensities']
        deltatime = npz_data['deltatime']
        print(frame)
        print(deltatime)

        # Call the plotting function with both wavelength and frame range
        self.plot_3d_spectral_data_filtered(frame, wavelengths, intensities, deltatime,
                                            wavelength_range=(self.lower_bound_wavelength, self.upper_bound_wavelength),
                                            frame_range=(self.lower_bound_frame, self.upper_bound_frame))

    def plot_3d_spectral_data_filtered(self, frame, wavelengths, intensities, deltatime, wavelength_range, frame_range):
        lower_bound_wavelength, upper_bound_wavelength = wavelength_range
        lower_bound_frame, upper_bound_frame = frame_range

        # Apply wavelength filtering
        wavelength_mask = (wavelengths >= lower_bound_wavelength) & (wavelengths <= upper_bound_wavelength)
        filtered_wavelengths = wavelengths[wavelength_mask]

        # Apply frame filtering
        frame_mask = (frame >= lower_bound_frame) & (frame <= upper_bound_frame)
        filtered_frames = frame[frame_mask]
        filtered_deltatime = deltatime[frame_mask]

        filtered_intensities = []
        for i in range(len(filtered_frames)):
            filtered_intensities.append(intensities[frame_mask][i][wavelength_mask])
        
        # Create meshgrid for plotting
        frame_mesh, wavelength_mesh = np.meshgrid(filtered_deltatime, filtered_wavelengths)

        # Plotting
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(frame_mesh, wavelength_mesh, np.array(filtered_intensities).T, cmap='viridis')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Wavelength (nm)')
        ax.set_zlabel('Value')
        fig.show()
