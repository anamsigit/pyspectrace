from Control.Configuration.Acquisition.acquisitioncontrol import AcquisitionControl
from Control.Configuration.Reference.referencecontrol import ReferenceControl
from Control.Configuration.Plotting.plottingcontrol import PlottingLayout
from Control.Configuration.Processing.processingcontrol import ProcessingControl
from PyQt5.QtCore import QTimer

class ConfiggurationControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.acquisitioncontrol = AcquisitionControl(model, view)
        self.referencecontrol = ReferenceControl(model, view)
        self.plottingcontrol = PlottingLayout(model, view)
        self.processingcontrol = ProcessingControl(model, view)

        