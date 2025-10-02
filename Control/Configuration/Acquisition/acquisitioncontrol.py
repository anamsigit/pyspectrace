from Control.Configuration.Acquisition.Communication.communicationcontrol import CommunicationControl
from Control.Configuration.Acquisition.Saving.savingcontrol import SavingControl
class AcquisitionControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.communicationcontrol = CommunicationControl(model, view)
        self.savingcontrol = SavingControl(model, view)
