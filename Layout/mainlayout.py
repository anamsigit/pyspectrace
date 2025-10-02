from PyQt5.QtWidgets import QTabWidget, QListWidget, QSplitter, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow, QGroupBox, QLabel
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Layout.Configuration.configurationlayout import ConfigurationLayout
from Layout.Menusbar.menusbarlayout import MenusbarLayout
from Layout.Plotting.plottinglayout import PlottingLayout
import pyqtgraph as pg

class MainLayout(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySpecTrace")
        self.initUI()
        self.showMaximized()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Membuat menubar
        self.menusbarlayout = MenusbarLayout(self)

        # Membuat layout utama
        # main_layout = QHBoxLayout()
        main_layout = QHBoxLayout()


        main_widget.setLayout(main_layout)

        # Membuat layout konfigurasi dan plotting
        configuration_layout = QVBoxLayout()
        
        # Membuat QSplitter untuk layout plotting
        plotting_vsplitter = QSplitter(Qt.Vertical)  # Menggunakan orientasi vertikal
        plotting_hsplitter = QSplitter(Qt.Horizontal)  # Menggunakan orientasi vertikal
        
        # Membuat list di layout konfigurasi
        spectrometer_list = self.spectrometer_list()
        configuration_layout.addWidget(spectrometer_list)

        # Membuat tombol di layout konfigurasi
        hlayout_button = QHBoxLayout()
        start_button, abort_button = self.button()

        hlayout_button.addWidget(start_button)
        hlayout_button.addWidget(abort_button)
        configuration_layout.addLayout(hlayout_button)

        # Membuat QTabWidget di layout konfigurasi
        self.configurationlayout = ConfigurationLayout(main_widget)

        # Tab Konfigurasi
        tab_configuration = QTabWidget()
        tab_configuration.addTab(self.configurationlayout.acquisitionlayout, "Acquisition")
        tab_configuration.addTab(self.configurationlayout.referencelayout, "Referencing and Baseline")
        tab_configuration.addTab(self.configurationlayout.processinglayout, "Processing")
        tab_configuration.addTab(self.configurationlayout.plottinglayout, "Plotting")
        configuration_layout.addWidget(tab_configuration)

        statistic = self.Statistics()
        configuration_layout.addWidget(statistic)
        
        # Tambahkan layout konfigurasi ke dalam main layout

        # Setup layout plotting dan masukkan ke dalam QSplitter
        self.plottinglayout = PlottingLayout(main_widget)

        # plotting_hsplitter.addWidget(self.plottinglayout.sensorgramlayout.plt)
        plotting_hsplitter.addWidget(self.plottinglayout.sensorgramlayout)
        # plotting_hsplitter.addWidget(self.plottinglayout.sensorgramlayout2.plt)
        # plotting_hsplitter.addWidget(self.plottinglayout.sensorgramlayout3.plt)
        # plotting_hsplitter.addWidget(self.bottom_plot1)
        # plotting_hsplitter.addWidget()


        
        # plotting_vsplitter.addWidget(self.plottinglayout.spectrumlayout.canvas)
        plotting_vsplitter.addWidget(self.plottinglayout.spectrumlayout.plt)

        # plotting_vsplitter.addWidget(self.plottinglayout.sensorgramlayout.plt)
        plotting_vsplitter.addWidget(plotting_hsplitter)

        # Tambahkan QSplitter ke dalam main layout
        main_layout.addLayout(configuration_layout, 1)
        main_layout.addWidget(plotting_vsplitter, 3)

        self.start = False


    def spectrometer_list(self):
        spectrometer_groupbox = QGroupBox('Spectroscopy Controls')
        group_layout = QHBoxLayout()

        device_layout = QVBoxLayout()

        self.device_list = QListWidget()
        
        
    
        # self.device_list.addItem('Simulator Spectrometer')
        # self.device_list.addItem(self.model.get_model())
        
        # self.device_list.addItem('Simulator Spectrometer')
        # self.device_list.clicked.connect

        device_layout.addWidget(self.device_list)
        group_layout.addLayout(device_layout)

        right_layout = QVBoxLayout()

        self.rescan_button = QPushButton('Rescan')
        self.connect_button = QPushButton('Connect')
        self.connect_button.setEnabled(False)
        # self.connect_button.setText('sdf')
        self.uploadrecord_button = QPushButton('Upload a record')

        # right_layout.addWidget(self.connection_status)
        right_layout.addWidget(self.rescan_button)
        right_layout.addWidget(self.connect_button)
        right_layout.addWidget(self.uploadrecord_button)
        right_layout.addStretch()  # Push buttons to the top

        group_layout.addLayout(right_layout)

        # Set layout for the group box
        spectrometer_groupbox.setLayout(group_layout)
        return spectrometer_groupbox

    def button(self):
        # Membuat tombol
        self.start_button = QPushButton("Start Acquisition")
        self.abort_button = QPushButton("Abort Acquisition")
        # for init start up software
        self.start_button.setDisabled(True)
        self.abort_button.setDisabled(True)

        self.start_button.clicked.connect(self.status_start)
        self.abort_button.clicked.connect(self.status_abort)

        self.start_button.setFixedHeight(40)
        self.abort_button.setFixedHeight(40)

        return self.start_button, self.abort_button
    
    def status_start(self):
        self.start = True
        self.start_button.setEnabled(False)
        self.abort_button.setEnabled(True)

    def status_abort(self):
        self.start = False
        self.start_button.setEnabled(True)
        self.abort_button.setEnabled(False)
    
    def Statistics(self):
        group_box_statistics = QGroupBox('Statistics')

        self.frame_value_received = QLabel("0", self) ; self.frame_value_received.setStyleSheet('color: green;')
        self.FPS_value_received = QLabel("0", self); self.FPS_value_received.setStyleSheet('color: green;')
        self.livetime_value_received = QLabel("0", self); self.livetime_value_received.setStyleSheet('color: green;')
        # self.record_value_received = QLabel("0 MB", self); self.record_value_received.setStyleSheet('color: green;')
        
        self.frame_value_processed = QLabel("0", self) ; self.frame_value_processed.setStyleSheet('color: green;')
        # self.FPS_value_processed = QLabel("0", self); self.FPS_value_processed.setStyleSheet('color: green;')
        # self.livetime_value_processed = QLabel("0", self); self.livetime_value_processed.setStyleSheet('color: green;')
        self.record_value_saved = QLabel("0", self); self.record_value_saved.setStyleSheet('color: green;')

        qgrid_layout = QGridLayout()

        qgrid_layout.addWidget(QLabel(f"Received", self), 0, 1)
        qgrid_layout.addWidget(QLabel(f"Processed", self), 0, 2)
        qgrid_layout.addWidget(QLabel(f"Saved", self), 0, 3)

        qgrid_layout.addWidget(QLabel(f"Spectra", self), 1, 0)
        qgrid_layout.addWidget(QLabel(f"Spectra/sec", self), 2, 0)
        qgrid_layout.addWidget(QLabel(f"Elapsed time", self), 3, 0)
        qgrid_layout.addWidget(QLabel(f"Record count", self), 4, 0)

        qgrid_layout.addWidget(self.frame_value_received, 1, 1)
        qgrid_layout.addWidget(self.FPS_value_received, 2, 1)
        qgrid_layout.addWidget(self.livetime_value_received, 3, 1)
        # qgrid_layout.addWidget(self.record_value_received, 4, 1)
        
        qgrid_layout.addWidget(self.frame_value_processed, 1, 2)
        # qgrid_layout.addWidget(self.FPS_value_processed, 2, 2)
        # qgrid_layout.addWidget(self.livetime_value_processed, 3, 2)
        qgrid_layout.addWidget(self.record_value_saved, 4, 3)
        
        group_box_statistics.setLayout(qgrid_layout)

        return group_box_statistics
    