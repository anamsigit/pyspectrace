from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QComboBox, QGroupBox, QLabel
from .Acquisition.acquisitionlayout import AcquisitionLayout
from .Reference.referencelayout import ReferenceLayout
from .Processing.processinglayout import ProcessingLayout
from .Plotting.plottinglayout import PlottingLayout


class ConfigurationLayout(QWidget):  # Mengubah dari QMainWindow ke QWidget
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Tab Acquisition
        self.acquisitionlayout = AcquisitionLayout(self)

        # # Tab Main Reference
        self.referencelayout = ReferenceLayout(self)

        # # Tab Main Processing
        self.processinglayout = ProcessingLayout(self)

        # # Tab Main Plotting
        self.plottinglayout = PlottingLayout(self)
