from pyspectrace.Layout.Menusbar.Tool.Plot3D.plot3dlayout import Plot3DLayout
from pyspectrace.Layout.Menusbar.Tool.PlotSensorgram.plotsensorgramlayout import PlotSensorgramLayout
from pyspectrace.Layout.Menusbar.Tool.Convert.convertlayout import ConvertLayout

class ToolLayout:
    def __init__(self, parent):
        self.parent = parent
        self.plotsensorgramlayout = PlotSensorgramLayout(self.parent)
        self.plot3dlayout = Plot3DLayout(self.parent)
        self.convertlayout = ConvertLayout(self.parent)