from Control.Menusbar.File.filecontrol import FileControl
from Control.Menusbar.Tool.toolcontrol import ToolControl

class MenusbarControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view

        self.filecontrol = FileControl(model, view)
        self.toolcontrol = ToolControl(model, view)
