from pyspectrace.Control.Menusbar.File.filecontrol import FileControl
from pyspectrace.Control.Menusbar.Tool.toolcontrol import ToolControl
from pyspectrace.Control.Menusbar.SDK.sdkcontrol import SDKControl

class MenusbarControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view

        self.filecontrol = FileControl(model, view)
        self.toolcontrol = ToolControl(model, view)
        self.sdkcontrol = SDKControl(model, view)
