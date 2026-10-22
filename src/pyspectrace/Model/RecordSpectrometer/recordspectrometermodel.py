import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QSpinBox, QGroupBox, QDoubleSpinBox, QSlider,
    QMessageBox, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
import pyqtgraph as pg
import numpy as np

class RecordSpectrometer(QMainWindow):
    frame_finish_emit = pyqtSignal()
    frame_on_emit = pyqtSignal()
    frame_start_emit = pyqtSignal()
    
    def __init__(self, model_name):
        self.model = model_name
        super().__init__()
        self.setWindowTitle("Spectral record")
        self.setGeometry(100, 100, 600, 500)       
        

        self.acquisition_delay_min = 1
        self.acquisition_delay_max = 250
        self.acquisition_delay = 250
        self.npz_file_path = None
        self.current_frame_index = 0
        self.excluded_frame_ranges = []

        self.notice_start = False

        layout = QVBoxLayout()

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        layout.addWidget(self.plot_widget)

        layout.addWidget(self.groupbox_loadspectrum())
        layout.addWidget(self.groupbox_controlspectrum())

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.integration_min = 0 
        self.integration_max = 0      

        npz_data = np.load(self.model)
        __init_wavelengths_record = npz_data['wavelengths']
        __init_intensities_record = npz_data['intensities']
        __init_deltatimes_record = 0

        self.wavelengths_record_deliver = np.array(__init_wavelengths_record)
        self.intensities_record_deliver = np.array(__init_intensities_record)
        self.deltatimes_record_deliver = np.array(__init_deltatimes_record)

        self.wavelengths = np.array(__init_wavelengths_record)
        self.intensities = np.array(__init_intensities_record)
        self.deltatimes = np.array(__init_deltatimes_record)


        
    def start(self):
        self.show()
        self.load_file()

    def get_model(self):
        return self.model

    def get_minimum_integration_time(self):
        return self.integration_min
    
    def get_maximum_integration_time(self):
        return self.integration_max
    
    def get_acquisition_delay_maximum(self):
        return self.acquisition_delay_max

    def get_acquisition_delay_minimum(self):
        return self.acquisition_delay_min

    def set_acquisition_delay(self, acquisition_delay):
        pass

    def set_integration_time(self, _):
        pass

    def acquire_spectrum_for_normalization(self):
        self.wavelengths = np.array(self.wavelengths_record_deliver)
        self.intensities = np.array(self.intensities_record_deliver)
        return self.wavelengths, self.intensities
    
    def acquire_spectrum_from_normalization(self, wavelengths, intensities):
        self.wavelengths = wavelengths
        self.intensities = intensities
        return self.wavelengths, self.intensities
    
    def acquire_spectrum(self):
        return self.wavelengths, self.intensities
    
    def acquire_deltatimes(self):
        self.deltatimes = float(self.deltatimes_record_deliver)
        return self.deltatimes
    
    def load_file(self):
        self.npz_file_path = self.model
        self.lower_frame_spinbox.valueChanged.connect(self.update_frame_range)
        self.upper_frame_spinbox.valueChanged.connect(self.update_frame_range)
        self.frame_slider.setEnabled(True)
        self.load_data()
            

    def groupbox_controlspectrum(self):
        groupbox = QGroupBox("Control Spectrum")
        layout = QVBoxLayout()

        self.frame_slider = QSlider(Qt.Horizontal)
        self.frame_slider.setMinimum(0)
        self.frame_slider.setValue(self.current_frame_index)
        self.frame_slider.valueChanged.connect(self.update_plot)

        skip_range_layout = QHBoxLayout()
        skip_range_layout.addWidget(QLabel("Skip frame ranges:"))
        self.skip_frame_ranges_input = QLineEdit()
        self.skip_frame_ranges_input.setPlaceholderText("e.g. 200-400, 800-829")
        self.apply_skip_ranges_button = QPushButton("Apply")
        self.apply_skip_ranges_button.clicked.connect(self.apply_skip_frame_ranges)
        skip_range_layout.addWidget(self.skip_frame_ranges_input)
        skip_range_layout.addWidget(self.apply_skip_ranges_button)

        self.skip_ranges_status_label = QLabel("No skipped frames")
        self.skip_ranges_status_label.setTextInteractionFlags(Qt.TextSelectableByMouse)



        layout.addWidget(self.frame_slider)
        layout.addLayout(skip_range_layout)
        layout.addWidget(self.skip_ranges_status_label)

        button_layout = QHBoxLayout()

        self.current_frame_label = QLabel(f"Frame: {self.current_frame_index}")
        self.current_frame_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        button_layout.addWidget(self.current_frame_label)

        layout.addLayout(button_layout)
        groupbox.setLayout(layout)
        return groupbox


    def groupbox_loadspectrum(self):
        groupbox = QGroupBox("Load Spectrum")
        
        layout = QVBoxLayout()

        wavelength_range_layout = QHBoxLayout()

        lower_wavelength_label = QLabel("Min wav:")
        self.lower_wavelength_spinbox = QDoubleSpinBox()
        self.lower_wavelength_spinbox.setSuffix(" nm")
        wavelength_range_layout.addWidget(lower_wavelength_label)
        wavelength_range_layout.addWidget(self.lower_wavelength_spinbox)

        upper_wavelength_label = QLabel("Max wav:")
        self.upper_wavelength_spinbox = QDoubleSpinBox()
        self.upper_wavelength_spinbox.setSuffix(" nm")
        wavelength_range_layout.addWidget(upper_wavelength_label)
        wavelength_range_layout.addWidget(self.upper_wavelength_spinbox)
        layout.addLayout(wavelength_range_layout)
        
        frame_range_layout = QHBoxLayout()
        lower_frame_label = QLabel("Min frame:")
        self.lower_frame_spinbox = QSpinBox()

        frame_range_layout.addWidget(lower_frame_label)
        frame_range_layout.addWidget(self.lower_frame_spinbox)

        upper_frame_label = QLabel("Max frame:")
        self.upper_frame_spinbox = QSpinBox()
        frame_range_layout.addWidget(upper_frame_label)
        frame_range_layout.addWidget(self.upper_frame_spinbox)

        layout.addLayout(frame_range_layout)
        groupbox.setLayout(layout)
        return groupbox

    def load_data(self):
        npz_data = np.load(self.npz_file_path)
        for key in npz_data.files:
            print(f"\nIsi array untuk kunci '{key}':")
            # print(npz_data[key])
        
        # print(npz_data.files)

        self.frames = npz_data['frame']
        self.deltatimes_record = npz_data['deltatime']
        self.wavelengths_record = npz_data['wavelengths']
        self.intensities_record = npz_data['intensities']

        self.lower_wavelength_spinbox.setRange(self.wavelengths_record[0], self.wavelengths_record[-1])
        self.lower_wavelength_spinbox.setValue(self.wavelengths_record[0])

        self.upper_wavelength_spinbox.setRange(self.wavelengths_record[0], self.wavelengths_record[-1])
        self.upper_wavelength_spinbox.setValue(self.wavelengths_record[-1])

        self.lower_frame_spinbox.setRange(self.frames[0], self.frames[-1])
        self.lower_frame_spinbox.setValue(self.frames[0])

        self.upper_frame_spinbox.setRange(self.frames[0], self.frames[-1])
        self.upper_frame_spinbox.setValue(self.frames[-1])

        self.frame_slider.setMaximum(len(self.frames) - 1)
        self.current_frame_index = 0
        self.frame_slider.setValue(0)

        self.update_plot()

    def update_plot(self):
        if not hasattr(self, 'frames') or len(self.frames) == 0:
            return

        self.current_frame_index = self.frame_slider.value()
        active_indices = self.active_frame_indices()
        if len(active_indices) == 0:
            self.current_frame_label.setText("Frame: no frames available")
            self.plot_widget.clear()
            return

        if self.current_frame_index not in active_indices:
            following_indices = active_indices[active_indices > self.current_frame_index]
            next_index = following_indices[0] if len(following_indices) else active_indices[-1]
            self.frame_slider.setValue(int(next_index))
            return

        frame = self.frames[self.current_frame_index]
        
        self.current_frame_label.setText(f"Frame: {frame}")

        self.lower_wavelength = self.lower_wavelength_spinbox.value()
        self.upper_wavelength = self.upper_wavelength_spinbox.value()
        self.lower_frame = self.lower_frame_spinbox.value()
        self.upper_frame = self.upper_frame_spinbox.value()

        mask = (self.wavelengths_record >= self.lower_wavelength) & (self.wavelengths_record <= self.upper_wavelength)
        filtered_wavelengths = self.wavelengths_record[mask]
        filtered_intensities = self.intensities_record[self.current_frame_index][mask]
        # filtered_deltatimes = self.deltatimes_record[self.current_frame_index][0]
        filtered_deltatimes = self.deltatimes_record[self.current_frame_index]

                # def acquire_spectrum_for_normalization(self):
        self.wavelengths_record_deliver = filtered_wavelengths
        self.intensities_record_deliver = filtered_intensities
        self.deltatimes_record_deliver = filtered_deltatimes
        # print(self.deltatimes)
        # print(self.deltatimes.shape)
        # print(self.deltatimes[0])



        self.plot_widget.clear()
        self.plot_widget.plot(filtered_wavelengths, filtered_intensities, pen='r')
        self.plot_widget.setLabel('bottom', 'Wavelength')

    def parse_skip_frame_ranges(self, ranges_text):
        """Parse comma-separated inclusive frame ranges, such as ``200-400, 800-829``."""
        if not ranges_text.strip():
            return []

        ranges = []
        for item in ranges_text.split(','):
            bounds = item.strip().split('-')
            if len(bounds) != 2:
                raise ValueError
            start, end = (int(value.strip()) for value in bounds)
            if start > end:
                raise ValueError
            ranges.append((start, end))
        return ranges

    def apply_skip_frame_ranges(self):
        """Apply frame ranges that must be skipped by the slider and playback."""
        try:
            self.excluded_frame_ranges = self.parse_skip_frame_ranges(
                self.skip_frame_ranges_input.text()
            )
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid frame range",
                "Use inclusive ranges separated by commas, for example: 200-400, 800-829.",
            )
            return

        if self.excluded_frame_ranges:
            ranges_text = ", ".join(
                f"{start}-{end}" for start, end in self.excluded_frame_ranges
            )
            self.skip_ranges_status_label.setText(f"Skipped frames: {ranges_text}")
        else:
            self.skip_ranges_status_label.setText("No skipped frames")

        self.update_frame_range()

    def active_frame_indices(self):
        """Return frame indices inside the selected range that are not excluded."""
        if not hasattr(self, 'frames'):
            return np.array([], dtype=int)

        lower_frame = self.lower_frame_spinbox.value()
        upper_frame = self.upper_frame_spinbox.value()
        frame_mask = (self.frames >= lower_frame) & (self.frames <= upper_frame)
        for start, end in self.excluded_frame_ranges:
            frame_mask &= ~((self.frames >= start) & (self.frames <= end))
        return np.flatnonzero(frame_mask)

    def update_frame_range(self):
        active_indices = self.active_frame_indices()
        if len(active_indices) == 0:
            self.update_plot()
            return

        self.current_frame_index = int(active_indices[0])
        self.frame_slider.setValue(self.current_frame_index)


    def mainloop(self):
        active_indices = self.active_frame_indices()
        if len(active_indices) == 0:
            return

        if self.current_frame_index not in active_indices:
            following_indices = active_indices[active_indices > self.current_frame_index]
            self.current_frame_index = int(
                following_indices[0] if len(following_indices) else active_indices[-1]
            )
            self.frame_slider.setValue(self.current_frame_index)

        first_index = int(active_indices[0])
        last_index = int(active_indices[-1])
        if self.current_frame_index == last_index:
            self.finish_trigger()
            return
        if self.current_frame_index == first_index:
            self.start_trigger()
        else:
            self.on_trigger()

        following_indices = active_indices[active_indices > self.current_frame_index]
        self.current_frame_index = int(following_indices[0])
        self.frame_slider.setValue(self.current_frame_index)
        
    def restart_slider(self):
        self.update_frame_range()

    def finish_trigger(self):
        self.frame_finish_emit.emit()

    def start_trigger(self):
        self.frame_start_emit.emit()
    
    def on_trigger(self):
        self.frame_on_emit.emit()

    def closeEvent(self, event):
        # Membuat dialog peringatan
        reply = QMessageBox.question(
            self,
            "Warning",
            "Are you sure want to close this window?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        if reply == QMessageBox.Yes:
            event.accept()  # Izinkan keluar
        else:
            event.ignore()  # Batalkan keluar
