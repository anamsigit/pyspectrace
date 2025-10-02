from Control.Plotting.Spectrum.spectrumcontrol import SpectrumControl
from Control.Plotting.Sensorgram.sensorgramcontrol import SensorgramControl
from PyQt5.QtCore import QTimer

class PlottingControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.spectrumcontrol = SpectrumControl(model, view)
        self.sensorgramcontrol = SensorgramControl(model, view)
