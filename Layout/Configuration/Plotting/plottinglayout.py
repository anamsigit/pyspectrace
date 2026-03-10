from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Layout.Configuration.Plotting.Sensorgram.sensorgramlayout import SensorgramLayout
from Layout.Configuration.Plotting.Spectrum.spectrumlayout import SpectrumLayout

class PlottingLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Tab Spectrum Layout
        self.spectrumlayout = SpectrumLayout(self)

        # Tab Sensorgram Layout
        self.sensorgramlayout = SensorgramLayout(self)

        # Menambahkan nestab bertingkat ke tab induk
        nested_tab_configuration = QTabWidget()
        nested_tab_configuration.addTab(self.spectrumlayout.nested_tabs, 'Spectrum')
        nested_tab_configuration.addTab(self.sensorgramlayout.nested_tabs, 'Sensorgram')

        main_layout = QVBoxLayout()
        main_layout.addWidget(nested_tab_configuration)
        self.setLayout(main_layout)