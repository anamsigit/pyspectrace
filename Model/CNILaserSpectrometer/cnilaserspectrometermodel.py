import numpy as np
from PyQt5.QtCore import pyqtSignal
import os
import ctypes


class CNILaserSpectrometer:
    frame_finish_emit = pyqtSignal()
    frame_start_emit = pyqtSignal()
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dll_name = "SpectrometersControlLTG.dll"
        self.dll_path = os.path.join(current_dir, "SDK", dll_name)
        self.dll = ctypes.CDLL(self.dll_path)

        self.dll.LTs_InitAllSpectrometers()
        self.dll.LTs_GetSerialNumber.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self.dll.LTs_GetWavelengthNmData.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self.dll.LTs_GetIntensityData.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self.dll.LTs_SetIntegralTimeMS2.argtypes = [ctypes.c_int, ctypes.c_double]
        self.dll.LTs_GetSpectrometerCount.restype = ctypes.c_int
        self.dll.LTs_GetSerialNumber.restype = ctypes.c_int
        self.dll.LTs_GetDevPixelCount.restype = ctypes.c_int
        self.dll.LTs_SetIntegralTimeMS2.restype = ctypes.c_int

        self.range_wavelength = self.dll.LTs_GetDevPixelCount(0)

        wavelengths_memory = (ctypes.c_double * self.range_wavelength)()
        intensities_memory = (ctypes.c_int * self.range_wavelength)()
        serialNumber_memory = ctypes.create_string_buffer(30)

        LTs_GetWavelengthNmData = self.dll.LTs_GetWavelengthNmData(0, wavelengths_memory)
        LTs_GetIntensityData = self.dll.LTs_GetIntensityData(0, intensities_memory)
        LTs_SetIntegralTimeMS2 = self.dll.LTs_SetIntegralTimeMS2(ctypes.c_int(0), ctypes.c_double(500.0))
        # LTs_GetSerialNumber = self.dll.LTs_GetSerialNumber(ctypes.c_int(0), serialNumber_memory)
        LTs_GetSerialNumber = self.dll.LTs_GetDeviceName(ctypes.c_int(0), serialNumber_memory)

        self.wavelengths = np.array(wavelengths_memory)
        self.intensities = np.array(intensities_memory)
        self.serialNumber = serialNumber_memory

        self.integration_min = 4.0
        self.integration_max = 10000.0

        self.current_frame_index = 0
        self.upper_frame = 1
        self.lower_frame = 0

    def get_minimum_integration_time(self):
        return self.integration_min
    
    def get_maximum_integration_time(self):
        return self.integration_max
    
    def get_acquisition_delay_maximum(self):
        return 100000

    def get_acquisition_delay_minimum(self):
        return 10
    
    def set_acquisition_delay(self, acquisition_delay):
        # self.device.set_acquisition_delay(acquisition_delay)
        pass
    
    def start(self):
        pass   

    def mainloop(self):
        pass

    def get_model(self):
        return self.serialNumber.value.decode('utf-8')

    def acquire_spectrum_for_normalization(self):
        wavelengths_memory = (ctypes.c_double * self.range_wavelength)()
        intensities_memory = (ctypes.c_int * self.range_wavelength)()

        LTs_GetIntensityData = self.dll.LTs_GetIntensityData(0, intensities_memory)
        LTs_GetWavelengthNmData = self.dll.LTs_GetWavelengthNmData(0, wavelengths_memory)

        self.wavelengths = np.array(wavelengths_memory)
        self.intensities = np.array(intensities_memory)
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
        LTs_SetIntegralTimeMS2 = self.dll.LTs_SetIntegralTimeMS2(0, integration_time)

    # def __del__(self):
    #     # Pastikan untuk melepaskan perangkat saat objek ini dihancurkan
    #     self.dll.LTs_ReleaseAllSpectrometers()

