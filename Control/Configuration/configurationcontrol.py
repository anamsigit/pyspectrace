from pyspectrace.Control.Configuration.Acquisition.acquisitioncontrol import AcquisitionControl
from pyspectrace.Control.Configuration.Reference.referencecontrol import ReferenceControl
from pyspectrace.Control.Configuration.Plotting.plottingcontrol import PlottingLayout
from pyspectrace.Control.Configuration.Processing.processingcontrol import ProcessingControl

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

        