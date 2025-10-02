from Control.Configuration.Plotting.Spectrumcontrol.spectrumcontrol import SpectrumControl
from Control.Configuration.Plotting.Sensorgramcontrol.sensorgramcontrol import SensorgramControl
class PlottingLayout:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.spectrumcontrol = SpectrumControl(model, view)
        self.sensorgramcontrol = SensorgramControl(model, view)
        