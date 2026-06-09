from pyspectrace.Control.Menusbar.Tool.Plot3D.plot3dcontrol import Plot3DControl
from pyspectrace.Control.Menusbar.Tool.Convert.convertcontrol import ConvertControl
from pyspectrace.Control.Menusbar.Tool.PlotSensorgram.plotsensorgramcontrol import PlotSensorgramControl

class ToolControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view

        
        self.plot3dcontrol = Plot3DControl(model, view)
        # self.plotsensorgramcontrol = PlotSensorgramControl()
        # self.convert_control = ConvertControl()

        self.view.menusbarlayout.toollayout.convertlayout.convert.triggered.connect(self.convertcontrol)
        self.view.menusbarlayout.toollayout.plotsensorgramlayout.plot_sensogram_choosing.triggered.connect(self.plotsensorgram)

    def convertcontrol(self):
        self.convert_control = ConvertControl()
        self.convert_control.show()
    
    def plotsensorgram(self):
        self.plotsensorgramcontrol = PlotSensorgramControl()
        self.plotsensorgramcontrol.show()