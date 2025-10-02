from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QComboBox, QGroupBox
from .Spectrum.spectrumlayout import SpectrumLayout
from .Sensorgram.sensorgramlayout import SensorgramLayout


class PlottingLayout(QWidget):  # Mengubah dari QMainWindow ke QWidget
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.spectrumlayout = SpectrumLayout(self)
        self.sensorgramlayout = SensorgramLayout(self)
