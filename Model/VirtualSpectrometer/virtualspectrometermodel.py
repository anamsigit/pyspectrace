import seatease.cseatease as spectro
from scipy.ndimage import gaussian_filter1d
from PyQt5.QtCore import QTimer, pyqtSignal, QThread, QObject
import numpy as np

class VirtualSpectrometerEngine(QThread):
    data_signal = pyqtSignal(list, list)
    def __init__(self):
        super().__init__()
        self.api = spectro.SeaTeaseAPI()
        self.dev = self.api.list_devices()[0]

        self.integration_min = 100
        self.integration_max = 100000

        self.acquisition_delay_min = 1
        self.acquisition_delay_max = 500

        self.dev.f.spectrometer.set_integration_time_micros(self.integration_min)
        
        self.wavelengths = self.dev.f.spectrometer.get_wavelengths()
        self.intensities = self.dev.f.spectrometer.get_intensities()

    def run(self):
        self.acquire_spectrum_for_normalization()
        
    def set_integration_time(self, integration_time):
        self.dev.f.spectrometer.set_integration_time_micros(integration_time)

    def acquire_spectrum_for_normalization(self):
        self.wavelengths = self.dev.f.spectrometer.get_wavelengths()
        self.intensities = self.dev.f.spectrometer.get_intensities()
        self.data_signal.emit(self.wavelengths.tolist(), self.intensities.tolist())

    def get_model(self):
        return self.dev.get_model()

    def get_minimum_integration_time(self):
        return self.integration_min
    
    def get_maximum_integration_time(self):
        return self.integration_max
    
    def get_acquisition_delay_maximum(self):
        return self.acquisition_delay_max

    def get_acquisition_delay_minimum(self):
        return self.acquisition_delay_min


class VirtualSpectrometer:
    frame_finish_emit = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.engine = VirtualSpectrometerEngine()
        self.engine.start()
        self.engine.data_signal.connect(self.engine_data_wrapper)
        # self.wavelengths = [0,0,0]
        # self.intensities = [0,0,0]

        self.current_frame_index = 0
        self.upper_frame = 1
        self.lower_frame = 0
    
    def engine_data_wrapper(self, wavelengths, intensities):
        self.wavelengths_wrapped =  np.array(wavelengths)
        self.intensities_wrapped =  np.array(intensities)       

    def get_model(self):
        return self.engine.dev.get_model()

    def get_minimum_integration_time(self):
        return self.engine.get_minimum_integration_time()
    
    def get_maximum_integration_time(self):
        return self.engine.get_maximum_integration_time()
    
    def get_acquisition_delay_maximum(self):
        return self.engine.get_acquisition_delay_maximum()

    def get_acquisition_delay_minimum(self):
        return self.engine.get_acquisition_delay_minimum()

    def set_acquisition_delay(self, acquisition_delay):
        self.acquisition_delay = acquisition_delay

    def set_integration_time(self, integration_time):
        self.engine.set_integration_time(integration_time)

    def acquire_spectrum_for_normalization(self):
        self.wavelengths = self.wavelengths_wrapped
        self.intensities = self.intensities_wrapped
        return self.wavelengths, self.intensities
    
    def acquire_spectrum_from_normalization(self, wavelengths, intensities):
        self.wavelengths = wavelengths
        self.intensities = intensities
        return self.wavelengths, self.intensities
    
    def acquire_spectrum(self):
        return self.wavelengths, self.intensities

    def start(self):
        pass  

    def mainloop(self):
        self.engine.start()
        