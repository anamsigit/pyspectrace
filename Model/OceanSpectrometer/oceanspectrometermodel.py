from PyQt5.QtCore import QTimer
import numpy as np

from PyQt5.QtCore import QObject, pyqtSignal
from Model.OceanSpectrometer.Oceandirect.OceanDirectAPI import OceanDirectAPI

class OceanSpectrometer(QObject):
    frame_finish_emit = pyqtSignal()
    frame_on_emit = pyqtSignal()
    frame_start_emit = pyqtSignal()
    def __init__(self):
        od = OceanDirectAPI()
        device_count = od.find_usb_devices()
        device_ids = od.get_device_ids()

        device_count = len(device_ids)
        (major, minor, point) = od.get_api_version_numbers()

        print("API Version  : %d.%d.%d " % (major, minor, point))
        print("Total Device : %d     \n" % device_count)

        try:
            for id in device_ids:
                self.device       = od.open_device(id)
                serialNumber = self.device.get_serial_number()

            print("First Device : %d       " % id)
            print("Serial Number: %s     \n" % serialNumber)
        except:
            pass

        self.integration_min = self.device.get_minimum_integration_time()
        self.integration_max = self.device.get_maximum_integration_time()

        self.device.set_integration_time(self.integration_min)

        self.range_wavelength = self.device.get_formatted_spectrum_length()

        self.wavelengths = np.array(self.device.get_wavelengths())
        self.intensities = np.array(self.device.get_formatted_spectrum())

        self.current_frame_index = 0
        
        self.upper_frame = 1
        self.lower_frame = 0

    def get_minimum_integration_time(self):
        return self.integration_min
    
    def get_maximum_integration_time(self):
        return self.integration_max
    
    def get_acquisition_delay_maximum(self):
        return self.device.get_acquisition_delay_maximum()

    def get_acquisition_delay_minimum(self):
        return self.device.get_acquisition_delay_minimum()
    
    def set_acquisition_delay(self, acquisition_delay):
        # self.device.set_acquisition_delay(acquisition_delay)
        pass
    
    def mainloop(self):
        pass
    
    def start(self):
        pass   

    def get_model(self):
        # return self.dev.get_model()
        return self.device.get_serial_number()

    def acquire_spectrum_for_normalization(self):
        self.wavelengths = np.array(self.device.get_wavelengths())
        self.intensities = np.array(self.device.get_formatted_spectrum())
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
        self.device.set_integration_time(integration_time)
