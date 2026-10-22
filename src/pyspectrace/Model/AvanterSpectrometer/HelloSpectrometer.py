from pyspectrace.Model.AvanterSpectrometer.avaspec import *

#(-1 Eth and USB, 0 USB, 256 Eth)
ret = AVS_Init(-1)
ret = AVS_UpdateUSBDevices()
ret = AVS_GetList()
handle = AVS_Activate(ret[0])

config = DeviceConfigType
ret = AVS_GetParameter(handle)
pixels = AVS_GetNumPixels(handle)
lamb = AVS_GetLambda(handle)
wavelengths = []
for pix in range(pixels):
    wavelengths.append(lamb[pix])

ret = AVS_UseHighResAdc(handle, True)
measconfig = MeasConfigType
measconfig.m_StartPixel = 0
measconfig.m_StopPixel = pixels - 1
measconfig.m_IntegrationTime = 50 #in milliseconds
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
ret = AVS_PrepareMeasure(handle, measconfig)

scans = 1
ret = AVS_Measure(handle, 0, scans)
dataready = False
import time
while not dataready:
    dataready = AVS_PollScan(handle)
    time.sleep(measconfig.m_IntegrationTime/1000)
        
spectrum = []        
timestamp, scopedata = AVS_GetScopeData(handle)
for i,pix in enumerate(wavelengths):
    spectrum.append(scopedata[i])

import matplotlib.pyplot as plt
plt.plot(wavelengths,spectrum)
