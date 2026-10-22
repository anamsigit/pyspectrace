from pyspectrace.Control.Plotting.Spectrum.spectrumcontrol import SpectrumControl
from pyspectrace.Control.Plotting.Sensorgram.sensorgramcontrol import SensorgramControl

class PlottingControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.spectrumcontrol = SpectrumControl(model, view)
        self.sensorgramcontrol = SensorgramControl(model, view)
