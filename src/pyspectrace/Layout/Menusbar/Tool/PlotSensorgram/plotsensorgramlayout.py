from PyQt5.QtWidgets import QAction

class PlotSensorgramLayout:
    def __init__(self, parent):
        self.parent = parent
        self.plot_sensogram_choosing = QAction('Plot sensogram', self.parent)
        