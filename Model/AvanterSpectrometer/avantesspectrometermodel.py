import os
import time
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import pyqtSignal, QThread

from Model.AvanterSpectrometer.avaspec import *

class AvantesSpectrometerEngine(QThread):
    data_signal = pyqtSignal(list, list)
    def __init__(self):
        super().__init__()
        self.microsecvar = 1000

        self.ret = AVS_Init(-1)
        self.ret = AVS_UpdateUSBDevices()
        self.ret = AVS_GetList()
        self.handle = AVS_Activate(self.ret[0])
        self.modelavaspec = "AvantesSPC"

        config = DeviceConfigType
        self.ret = AVS_GetParameter(self.handle)
        pixels = AVS_GetNumPixels(self.handle)
        lamb = AVS_GetLambda(self.handle)
        self.wavelengths = []
        for pix in range(pixels):
            self.wavelengths.append(lamb[pix])

        self.ret = AVS_UseHighResAdc(self.handle, True)
        self.measconfig = MeasConfigType
        self.measconfig.m_StartPixel = 0
        self.measconfig.m_StopPixel = pixels - 1
        self.measconfig.m_IntegrationTime = 50 #in milliseconds
        self.measconfig.m_IntegrationDelay = 0 #in FPGA clock cycles
        self.measconfig.m_NrAverages = 1
        self.measconfig.m_CorDynDark_m_Enable = 0  # nesting of types does NOT work!!
        self.measconfig.m_CorDynDark_m_ForgetPercentage = 100
        self.measconfig.m_Smoothing_m_SmoothPix = 0
        self.measconfig.m_Smoothing_m_SmoothModel = 0
        self.measconfig.m_SaturationDetection = 0
        self.measconfig.m_Trigger_m_Mode = 0
        self.measconfig.m_Trigger_m_Source = 0
        self.measconfig.m_Trigger_m_SourceType = 0
        self.measconfig.m_Control_m_StrobeControl = 0
        self.measconfig.m_Control_m_LaserDelay = 0
        self.measconfig.m_Control_m_LaserWidth = 0
        self.measconfig.m_Control_m_LaserWaveLength = 0.0
        self.measconfig.m_Control_m_StoreToRam = 0
        self.ret = AVS_PrepareMeasure(self.handle, self.measconfig)

        scans = 1
        self.ret = AVS_Measure(self.handle, 0, scans)
        dataready = False
        while not dataready:
            dataready = AVS_PollScan(self.handle)
            time.sleep(self.measconfig.m_IntegrationTime/1000)
                
        self.intensities = []        
        timestamp, scopedata = AVS_GetScopeData(self.handle)
        for i,pix in enumerate(self.wavelengths):
            self.intensities.append(scopedata[i])

        self.integration_min = 50
        self.integration_max = 20000000

    def get_minimum_integration_time(self):
        return self.integration_min
    
    def get_maximum_integration_time(self):
        return self.integration_max
    
    def get_model(self):
        return self.modelavaspec

    def run(self):
        self.acquire_spectrum_for_normalization()

    def acquire_spectrum_for_normalization(self):
        scans = 1
        self.ret = AVS_Measure(self.handle, 0, scans)
        dataready = False
        import time
        while not dataready:
            dataready = AVS_PollScan(self.handle)
            time.sleep(self.measconfig.m_IntegrationTime/1000)
                
        self.intensities = []        
        timestamp, scopedata = AVS_GetScopeData(self.handle)
        for i,pix in enumerate(self.wavelengths):
            self.intensities.append(scopedata[i])
        self.data_signal.emit(self.wavelengths, self.intensities)

    def set_integration_time(self, integration_time):
        self.ret = AVS_UseHighResAdc(self.handle, True)
        measconfig = MeasConfigType
        measconfig.m_StartPixel = 0
        measconfig.m_IntegrationTime = integration_time/self.microsecvar #in microseconds
        measconfig.m_IntegrationDelay = 0 #in FPGA clock cycles
        measconfig.m_NrAverages = 1
        measconfig.m_CorDynDark_m_Enable = 0  # nesting of types does NOT work!!
        measconfig.m_CorDynDark_m_ForgetPercentage = 100
        measconfig.m_Smoothing_m_SmoothPix = 0
        measconfig.m_Smoothing_m_SmoothModel = 0
        measconfig.m_SaturationDetection = 0
        measconfig.m_Trigger_m_Mode = 0
        measconfig.m_Trigger_m_Source = 0
        measconfig.m_Trigger_m_SourceType = 0
        measconfig.m_Control_m_StrobeControl = 0
        measconfig.m_Control_m_LaserDelay = 0
        measconfig.m_Control_m_LaserWidth = 0
        measconfig.m_Control_m_LaserWaveLength = 0.0
        measconfig.m_Control_m_StoreToRam = 0
        self.ret = AVS_PrepareMeasure(self.handle, measconfig)

class AvantesSpectrometer:
    frame_finish_emit = pyqtSignal()
    frame_start_emit = pyqtSignal()

    def __init__(self):
        self.engine = AvantesSpectrometerEngine()
        self.engine.start()
        self.engine.data_signal.connect(self.engine_data_wrapper)
        
        self.wavelengths = [0,0,0]
        self.intensities = [0,0,0]
        
        self.current_frame_index = 0
        self.upper_frame = 1
        self.lower_frame = 0
    
    def engine_data_wrapper(self, wavelengths, intensities):
        self.wavelengths_wrapped =  wavelengths
        self.intensities_wrapped =  intensities
  
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
        self.wavelengths = self.wavelengths
        self.intensities = self.intensities
        return self.wavelengths, self.intensities

    def get_model(self):
        return self.engine.get_model()
    
    def get_minimum_integration_time(self):
        return self.engine.get_minimum_integration_time()
    
    def get_maximum_integration_time(self):
        return self.engine.get_maximum_integration_time()
    
    def get_acquisition_delay_maximum(self):
        return 10000000

    def get_acquisition_delay_minimum(self):
        return 10
    def set_acquisition_delay(self, acquisition_delay):
        pass

    def mainloop(self):
        self.engine.start()
    
    def start(self):
        pass   