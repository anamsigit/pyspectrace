from pyspectrace.Control.Configuration.Acquisition.Communication.communicationcontrol import CommunicationControl
from pyspectrace.Control.Configuration.Acquisition.Saving.savingcontrol import SavingControl
from pyspectrace.Control.Configuration.Acquisition.Info.infocontrol import InfoControl
class AcquisitionControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.communicationcontrol = CommunicationControl(model, view)
        self.savingcontrol = SavingControl(model, view)
        self.infocontrol = InfoControl(model, view)
