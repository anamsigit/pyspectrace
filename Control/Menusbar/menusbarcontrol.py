import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
