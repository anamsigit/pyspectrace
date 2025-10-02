from Control.Configuration.configurationcontrol import ConfiggurationControl
from Control.Plotting.plottingcontrol import PlottingControl
from Control.Menusbar.menusbarcontrol import MenusbarControl
from PyQt5.QtCore import QTimer, QTime
import sys
import time
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QSpinBox, QAction, QCheckBox, 
    QFileDialog, QComboBox, QGroupBox, QLineEdit, QFormLayout, QTableWidget,
    QColorDialog, QDoubleSpinBox, QSlider, QMessageBox
)
import numpy as np

class MainControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.configurationcontrol = ConfiggurationControl(model, view)
        self.plottingcontrol = PlottingControl(model, view)
        self.menusbarcontrol = MenusbarControl(model, view)
        self.load_symbols = ["|", "/", "-", "\\"]

        self.last_print_time_saving = time.time()

        
        self.timer = QTimer()
        # self.timer.timeout.connect(self.mainloop)

        self.timer.timeout.connect(self.configurationcontrol.acquisitioncontrol.savingcontrol.mainloop) # saving dibelakang reference mainloop. agar tidak merusak referencing 
        self.timer.timeout.connect(self.configurationcontrol.referencecontrol.mainloop)

        self.timer.timeout.connect(self.configurationcontrol.plottingcontrol.spectrumcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.plottingcontrol.sensorgramcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.acquisitioncontrol.communicationcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.processingcontrol.gaussianfittingcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.processingcontrol.lorentzianfittingcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.processingcontrol.polynomialfittingcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.processingcontrol.polynomialpeakfittingcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.processingcontrol.polypeakfittingcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.processingcontrol.lorentzianwidthpeakfittingcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.processingcontrol.gaussianwidthpeakfittingcontrol.mainloop)
        self.timer.timeout.connect(self.configurationcontrol.processingcontrol.polynomialwidthpeakfittingcontrol.mainloop)

        self.timer.timeout.connect(self.plottingcontrol.spectrumcontrol.mainloop)
        self.timer.timeout.connect(self.plottingcontrol.sensorgramcontrol.mainloop)

        
        self.timer.timeout.connect(self.mainloop)
        self.frame_count = 0
        self.frame_number = 0
        self.fps = 1
    
        self.last_time = time.time()
        self.is_running = False
        
        self.total_elapsed = 0
        self.start_segment_time = None
        self.start_time = QTime.currentTime()

        self.device_list = []
        self.spectrometer_connected = ''
        self.recordspectrometermodel_mode = False

        self.isEnableAllMainUI( 
            False,
            False,
            True,
            True,
            True
            )

        config = {
                "output_spectrum_option": False,
                "acquisitiondelay_spinbox": False,
                "acquisitiondelay_button": False,
                "acquisitionaverage_spinbox": False,
                "acquisitionaverage_button": False,
                "time_integration_spinbox": False,
                "time_integration_button": False,
                "enable_record_checkbox": False,
                "take_dark_button": False,
                "clear_dark_button": False,
                "save_dark_button": False,
                "load_dark_button": False,
                "take_bright_button": False,
                "clear_bright_button": False,
                "save_bright_button": False,
                "load_bright_button": False,
                "allow_baseline": False,
                "polynomial_fitting_button": False,
                "gaussian_peak_fitting_button": False,
                "lorentzian_peak_fitting_button": False,
                "polynomial_peak_fitting_button": False,
                "poly_peak_fitting_button": False,
                "gaussian_peak_width_fitting_button": False,
                "lorentzian_peak_width_fitting_button": False,
                "polynomial_peak_width_fitting_button": False,
                "autoscale_y": False,
                "autoscale_x": False,
                "update_fixed_range": False,
                "min_range_input": False,
                "max_range_input": False,
                "select_time_unit": False,
                "reset_button": False,
                "save_sensorgram": False,
                "plot_sensorgram": False,
                "fit_interest_y": False,
                "fit_interest_x": False
            }

        self.isEnableAllConfigurationUI(config)

        self.view.device_list.itemClicked.connect(self.selected_spectrometer)
        self.view.connect_button.clicked.connect(self.toggle_connected_disconnected)
        self.view.uploadrecord_button.clicked.connect(self.uploadrecord)
        self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitiondelay_button.clicked.connect(self.acquisition_delay_change)
        self.view.rescan_button.clicked.connect(self.spectrometer_list)
        self.view.start_button.clicked.connect(self.setStart)
        self.view.abort_button.clicked.connect(self.setStop)

        # self.thread_manager()
        # self.view.configurationlayout.acquisitionlayout.output_spectrum_option.currentTextChanged.connect(self.update_properties_viewplot)
        self.timer.start(self.configurationcontrol.acquisitioncontrol.communicationcontrol.delay_time) # hapus agar init mengikuti tombol

        # self.disconnected_trigger()
        self.timer.stop()


    def setStart(self):
        if not self.is_running:
            self.is_running = True
            self.start_segment_time = time.time()
            self.last_time = time.time()  # reset timer untuk fps
        # self.timer.start(self.configurationcontrol.acquisitioncontrol.communicationcontrol.delay_time)
        self.timer.start(self.configurationcontrol.acquisitioncontrol.communicationcontrol.delay_time)
        if self.recordspectrometermodel_mode:
            self.model.restart_slider()
            # self.model.playrecord(True)

            # self.isEnableAllConfigurationUI(
            #     True, True, True, True,
            #     True, False, False, True,
            #     True, True, True, True,
            #     True, True, True, True, 
            #     True, True, True, True,
            #     True, True, True, True, 
            #     True, True, True, True, 
            #     True, True, True, True,
            #     True, True
            # )
            config = {
                "output_spectrum_option": True,
                "acquisitiondelay_spinbox": True,
                "acquisitiondelay_button": True,
                "acquisitionaverage_spinbox": True,
                "acquisitionaverage_button": True,
                "time_integration_spinbox": False,
                "time_integration_button": False,
                "enable_record_checkbox": True,
                "take_dark_button": True,
                "clear_dark_button": True,
                "save_dark_button": True,
                "load_dark_button": True,
                "take_bright_button": True,
                "clear_bright_button": True,
                "save_bright_button": True,
                "load_bright_button": True,
                "allow_baseline": True,
                "polynomial_fitting_button": True,
                "gaussian_peak_fitting_button": True,
                "lorentzian_peak_fitting_button": True,
                "polynomial_peak_fitting_button": True,
                "poly_peak_fitting_button": True,
                "gaussian_peak_width_fitting_button": True,
                "lorentzian_peak_width_fitting_button": True,
                "polynomial_peak_width_fitting_button": True,
                "autoscale_y": True,
                "autoscale_x": True,
                "update_fixed_range": True,
                "min_range_input": True,
                "max_range_input": True,
                "select_time_unit": True,
                "reset_button": True,
                "save_sensorgram": True,
                "plot_sensorgram": True,
                "fit_interest_y": True,
                "fit_interest_x": True
            }

            self.isEnableAllConfigurationUI(config)
        else:
            config = {
                "output_spectrum_option": True,
                "acquisitiondelay_spinbox": True,
                "acquisitiondelay_button": True,
                "acquisitionaverage_spinbox": True,
                "acquisitionaverage_button": True,
                "time_integration_spinbox": True,
                "time_integration_button": True,
                "enable_record_checkbox": True,
                "take_dark_button": True,
                "clear_dark_button": True,
                "save_dark_button": True,
                "load_dark_button": True,
                "take_bright_button": True,
                "clear_bright_button": True,
                "save_bright_button": True,
                "load_bright_button": True,
                "allow_baseline": True,
                "polynomial_fitting_button": True,
                "gaussian_peak_fitting_button": True,
                "lorentzian_peak_fitting_button": True,
                "polynomial_peak_fitting_button": True,
                "poly_peak_fitting_button": True,
                "gaussian_peak_width_fitting_button": True,
                "lorentzian_peak_width_fitting_button": True,
                "polynomial_peak_width_fitting_button": True,
                "autoscale_y": True,
                "autoscale_x": True,
                "update_fixed_range": True,
                "min_range_input": True,
                "max_range_input": True,
                "select_time_unit": True,
                "reset_button": True,
                "save_sensorgram": True,
                "plot_sensorgram": True,
                "fit_interest_y": True,
                "fit_interest_x": True
            }

            self.isEnableAllConfigurationUI(config)
            # self.timer.start(self.configurationcontrol.acquisitioncontrol.communicationcontrol.delay_time)


    def setStop(self):
        if self.is_running:
            self.is_running = False
            segment_duration = time.time() - self.start_segment_time
            self.total_elapsed += segment_duration
            self.start_segment_time = None
        self.timer.stop()


        config = {
            "output_spectrum_option": False,
            "acquisitiondelay_spinbox": False,
            "acquisitiondelay_button": False,
            "acquisitionaverage_spinbox": False,

            "acquisitionaverage_button": False,
            "time_integration_spinbox": False,
            "time_integration_button": False,
            "enable_record_checkbox": False,
            
            "take_dark_button": False,
            "clear_dark_button": False,
            "save_dark_button": True,
            "load_dark_button": False,
            
            "take_bright_button": False,
            "clear_bright_button": False,
            "save_bright_button": True,
            "load_bright_button": False,
            
            "allow_baseline": False,
            "polynomial_fitting_button": False,
            "gaussian_peak_fitting_button": False,
            "lorentzian_peak_fitting_button": False,
            
            "polynomial_peak_fitting_button": False,
            "poly_peak_fitting_button": False,
            "gaussian_peak_width_fitting_button": False,
            "lorentzian_peak_width_fitting_button": False,
            "polynomial_peak_width_fitting_button": False,

            "autoscale_y": True,
            "autoscale_x": True,
            "update_fixed_range": True,
            "min_range_input": True,
            "max_range_input": True,
            "select_time_unit": True,
            "reset_button": True,
            "save_sensorgram": True,
            "plot_sensorgram": True,
            "fit_interest_y": True,
            "fit_interest_x": True
        }

        self.isEnableAllConfigurationUI(config)



        # self.isEnableAllConfigurationUI(
        #     False, False, False, False,
        #     False, False, False, False,
        #     False, False, True, False,
        #     False, False, True, False, 
        #     False, False, False, False,
        #     False, False, False, True,
        #     True, True, True, True, 
        #     True, True, True, True,
        #     # False, False, True, True, #RESET DATA SENSORGRAM
        #     True, True
        # )

        # if self.recordspectrometermodel_mode:
        #     self.model.playrecord(False)

    def selected_spectrometer(self, item):
        self.view.connect_button.setEnabled(True)
        self.spectrometer_connected = item.text()
        
    def toggle_connected_disconnected(self):
        if self.view.connect_button.text() == "Connect":
            self.connected_trigger()
            self.view.connect_button.setText("Disconnect")
            self.got_properties_fitting = False
        else:
            reply = QMessageBox.question(
                self.view,
                "Warning",
                "Are you sure want to disconnect this source? ",  # Pesan konfirmasi
                QMessageBox.Yes | QMessageBox.No,  # Tombol yang ditampilkan
                QMessageBox.Yes  # Tombol default
            )

            if reply == QMessageBox.Yes:
                self.disconnected_trigger()
                self.view.connect_button.setText("Connect")

    def connected_trigger(self):   
        # self.setStart()

        self.isEnableAllMainUI( 
            True,
            False,
            # False,
            # True,
            False,
            False,
            False)

        # self.isEnableAllConfigurationUI(
        #     False, False, False, False,
        #     False, False, False, False,
        #     False, False, True, False,
        #     False, False, True, False, 
        #     False, False, False, False,
        #     False, False, False, True,
        #     True, True, True, True, 
        #     False, False, True, True,
        #     True, True
        # )

        config = {
            "output_spectrum_option": False,
            "acquisitiondelay_spinbox": False,
            "acquisitiondelay_button": False,
            "acquisitionaverage_spinbox": False,

            "acquisitionaverage_button": False,
            "time_integration_spinbox": False,
            "time_integration_button": False,
            "enable_record_checkbox": False,
            
            "take_dark_button": False,
            "clear_dark_button": False,
            "save_dark_button": True,
            "load_dark_button": False,
            
            "take_bright_button": False,
            "clear_bright_button": False,
            "save_bright_button": True,
            "load_bright_button": False,
            
            "allow_baseline": False,
            "polynomial_fitting_button": False,
            "gaussian_peak_fitting_button": False,
            "lorentzian_peak_fitting_button": False,
            
            "polynomial_peak_fitting_button": False,
            "poly_peak_fitting_button": False,
            "gaussian_peak_width_fitting_button": False,
            "lorentzian_peak_width_fitting_button": False,
            "polynomial_peak_width_fitting_button": False,
            "autoscale_y": True,

            "autoscale_x": True,
            "update_fixed_range": True,
            "min_range_input": True,
            "max_range_input": True,

            "select_time_unit": False,
            "reset_button": False,
            "save_sensorgram": True,
            "plot_sensorgram": True,
            
            "fit_interest_y": True,
            "fit_interest_x": True
        }

        self.isEnableAllConfigurationUI(config)

        
        selected_spectrometer_index = self.model.spectrometer_model_name.index(self.spectrometer_connected)
        self.model.set_spectrometer(self.model.available_spectrometer[selected_spectrometer_index])
        if self.model.available_spectrometer[selected_spectrometer_index].__class__.__name__ == "RecordSpectrometer":
            self.model.frame_start_emit.connect(self.frame_start)
            self.model.frame_finish_emit.connect(self.frame_finish)
            self.recordspectrometermodel_mode = True
            self.view.plottinglayout.sensorgramlayout.pI.setLabel('bottom', 'Time')

        else:
            self.recordspectrometermodel_mode = False

        # self.init_properties_fitting()
        
    def disconnected_trigger(self):
        self.clearAll()
        self.isEnableAllMainUI( 
            False,
            False,
            True,
            True,
            True)

        config = {
            "output_spectrum_option": False,
            "acquisitiondelay_spinbox": False,
            "acquisitiondelay_button": False,
            "acquisitionaverage_spinbox": False,
            "acquisitionaverage_button": False,
            "time_integration_spinbox": False,
            "time_integration_button": False,
            "enable_record_checkbox": False,
            "take_dark_button": False,
            "clear_dark_button": False,
            "save_dark_button": False,
            "load_dark_button": False,
            "take_bright_button": False,
            "clear_bright_button": False,
            "save_bright_button": False,
            "load_bright_button": False,
            "allow_baseline": False,
            "polynomial_fitting_button": False,
            "gaussian_peak_fitting_button": False,
            "lorentzian_peak_fitting_button": False,
            "polynomial_peak_fitting_button": False,
            "poly_peak_fitting_button": False,
            "gaussian_peak_width_fitting_button": False,
            "lorentzian_peak_width_fitting_button": False,
            "polynomial_peak_width_fitting_button": False,
            "autoscale_y": False,
            "autoscale_x": False,
            "update_fixed_range": False,
            "min_range_input": False,
            "max_range_input": False,
            "select_time_unit": False,
            "reset_button": False,
            "save_sensorgram": False,
            "plot_sensorgram": False,
            "fit_interest_y": False,
            "fit_interest_x": False
        }

        self.isEnableAllConfigurationUI(config)
        self.setStop()

       
    def get_properties_fitting(self):    

        self.view.configurationlayout.acquisitionlayout.communicationlayout.time_integration_spinbox.setRange(self.model.get_minimum_integration_time(), self.model.get_maximum_integration_time())
        self.view.configurationlayout.acquisitionlayout.communicationlayout.time_integration_spinbox.setValue(self.model.get_minimum_integration_time())

        self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitiondelay_spinbox.setRange(self.model.get_acquisition_delay_minimum(), self.model.get_acquisition_delay_maximum())
        self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitiondelay_spinbox.setValue(self.model.get_acquisition_delay_maximum())

        self.view.configurationlayout.referencelayout.baselinespectrumlayout.min_range_input.setRange(self.model.wavelengths[0], self.model.wavelengths[-1])
        self.view.configurationlayout.referencelayout.baselinespectrumlayout.max_range_input.setRange(self.model.wavelengths[0], self.model.wavelengths[-1])

        self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.min_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.max_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.initial_center_values = [f"{(self.model.wavelengths[-1 - 1] + self.model.wavelengths[0 + 1])/2:.2f}"]

        self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.min_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.max_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.initial_center_values = [f"{(self.model.wavelengths[-1 - 1] + self.model.wavelengths[0 + 1])/2:.2f}"]

        self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.min_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.max_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.initial_center_values = [f"{(self.model.wavelengths[-1 - 1] + self.model.wavelengths[0 + 1])/2:.2f}"]

        self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.min_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.max_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.initial_center_values = [f"{(self.model.wavelengths[-1 - 1] + self.model.wavelengths[0 + 1])/2:.2f}"]
        
        self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.min_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.max_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.initial_center_values = [f"{(self.model.wavelengths[-1 - 1] + self.model.wavelengths[0 + 1])/2:.2f}"]

        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.min_values =  [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.max_values =  [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.initial_center_values =   [f"{(self.model.wavelengths[-1 - 1] + self.model.wavelengths[0 + 1])/2:.2f}"]

        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.min_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.max_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.initial_center_values = [f"{(self.model.wavelengths[-1 - 1] + self.model.wavelengths[0 + 1])/2:.2f}"]

        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.min_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.max_values = [f"{(self.model.wavelengths[-1 - 1] - self.model.wavelengths[0 + 1])*0.10:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.initial_center_values =[f"{(self.model.wavelengths[-1 - 1] + self.model.wavelengths[0 + 1])/2:.2f}"]


        

    def clear_average_acquisition(self):
        self.configurationcontrol.referencecontrol.sum_intensities.clear()
        self.configurationcontrol.referencecontrol.sum_wavelengths.clear()
    
    def clear_all_fitting(self):
        # self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.clear_all_fitting()
        # self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.clear_all_fitting()
        # self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.clear_all_fitting()
        # self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.clear_all_fitting()
        # self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.clear_all_fitting()
        # self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.clear_all_fitting()
        # self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.clear_all_fitting()
        # self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.clear_all_fitting()
        
        for i in range(len(self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.num_fitting)):
            self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.removeRowButton.click()
            self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.applyRowButton.click()
            
        for i in range(len(self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.num_fitting)):
            self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.removeRowButton.click()
            self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.applyRowButton.click()

        for i in range(len(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.num_fitting)):
            self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.removeRowButton.click()
            self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.applyRowButton.click()

        for i in range(len(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.num_fitting)):
            self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.removeRowButton.click()
            self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.applyRowButton.click()

        for i in range(len(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.num_fitting)):
            self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.removeRowButton.click()
            self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.applyRowButton.click()

        for i in range(len(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.num_fitting)):
            self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.removeRowButton.click()
            self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.applyRowButton.click()

        for i in range(len(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.num_fitting)):
            self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.removeRowButton.click()
            self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.applyRowButton.click()

        for i in range(len(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.num_fitting)):
            self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.removeRowButton.click()
            self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.applyRowButton.click()
        
        # Gaussian Peak Fitting
        self.view.plottinglayout.spectrumlayout.num_gaussianshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.num_fitting
        self.view.plottinglayout.spectrumlayout.num_gaussianpeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.num_fitting
        self.view.plottinglayout.sensorgramlayout.num_gaussianshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.num_fitting

        # Lorentzian Peak Fitting
        self.view.plottinglayout.spectrumlayout.num_lorentzianshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.num_fitting
        self.view.plottinglayout.spectrumlayout.num_lorentzianpeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.num_fitting
        self.view.plottinglayout.sensorgramlayout.num_lorentzianshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.num_fitting

        # Polynomial Peak Fitting
        self.view.plottinglayout.spectrumlayout.num_polynomialshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.num_fitting
        self.view.plottinglayout.spectrumlayout.num_polynomialpeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.num_fitting
        self.view.plottinglayout.sensorgramlayout.num_polynomialshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.num_fitting

        # Poly Peak Fitting
        self.view.plottinglayout.spectrumlayout.num_polyshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.num_fitting
        self.view.plottinglayout.spectrumlayout.num_polypeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.num_fitting
        self.view.plottinglayout.sensorgramlayout.num_polyshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.num_fitting

        # Lorentzian Peak Width Fitting
        self.view.plottinglayout.spectrumlayout.num_lorentzianshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.num_fitting
        self.view.plottinglayout.spectrumlayout.num_lorentzianpeakwidthfitting = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.num_fitting
        self.view.plottinglayout.sensorgramlayout.num_lorentzianshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.num_fitting

        # Gaussian Peak Width Fitting
        self.view.plottinglayout.spectrumlayout.num_gaussianshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.num_fitting
        self.view.plottinglayout.spectrumlayout.num_gaussianpeakwidthfitting = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.num_fitting
        self.view.plottinglayout.sensorgramlayout.num_gaussianshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.num_fitting

        # Polynomial Peak Width Fitting
        self.view.plottinglayout.spectrumlayout.num_polynomialshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.num_fitting
        self.view.plottinglayout.spectrumlayout.num_polynomialpeakwidthfitting = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.num_fitting
        self.view.plottinglayout.sensorgramlayout.num_polynomialshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.num_fitting

        # Polynomial Fitting
        self.view.plottinglayout.spectrumlayout.num_polynomialshift = self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.num_fitting
        self.view.plottinglayout.spectrumlayout.num_polynomialfitting = self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.num_fitting
        self.view.plottinglayout.sensorgramlayout.num_polynomialshift = self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.num_fitting
        
        self.view.plottinglayout.spectrumlayout.init_plot_args()
        self.view.plottinglayout.sensorgramlayout.init_plot_args()
        
    
    def clear_reference(self):
        # self.configurationcontrol.referencecontrol.brightspectrumcontrol.clear()
        # self.configurationcontrol.referencecontrol.darkspectrumcontrol.clear()
        # self.configurationcontrol.referencecontrol.brightspectrumcontrol.update()
        # self.configurationcontrol.referencecontrol.darkspectrumcontrol.update()
        # self.configurationcontrol.referencecontrol.brightreference = 0
        # self.configurationcontrol.referencecontrol.darkreference = 0
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_bright_button.click()
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_dark_button.click()
        
    
    def clear_baseline(self):
        self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.setChecked(False)
        self.view.configurationlayout.referencelayout.baselinespectrumlayout.min_range_input.setDisabled(True)
        self.view.configurationlayout.referencelayout.baselinespectrumlayout.max_range_input.setDisabled(True)
        self.view.configurationlayout.referencelayout.baselinespectrumlayout.plt.clear()

    def uploadrecord(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Upload Spectrum", r"..\..\data\record", "NPZ Files (*.npz);;All Files (*)", options=options)
        if file_name:
            self.view.uploadrecord_button.setEnabled(False)
            self.view.connect_button.setEnabled(False)
            self.model.init_recordspectrometer_model_name = os.path.normpath(file_name)
            self.model.change_init_recordspectrometer_model_name = os.path.normpath(file_name)
                    
    def spectrometer_list(self):
        self.view.uploadrecord_button.setEnabled(True)
        self.view.connect_button.setEnabled(False)
        self.model.delete_all_model()
        self.model.model()
        self.model.update_list_spectrometer()

        for _ in range(len(self.model.spectrometer_model_name)):
            self.view.device_list.clear()
            print(self.model.spectrometer_model_name)
            self.view.device_list.addItems(self.model.spectrometer_model_name)
        
    def mainloop(self):
        self.change_statistics_value()
        self.model.mainloop()
        if self.recordspectrometermodel_mode:
            self.plottingcontrol.sensorgramcontrol.update_frame_time(self.model.acquire_deltatimes())
        else:
            self.plottingcontrol.sensorgramcontrol.update_frame_time(1/self.fps)
        if not self.got_properties_fitting:
            print("getting..........")
            self.get_properties_fitting()
            self.got_properties_fitting = True
    
    def frame_finish(self):
        self.view.abort_button.click()
    
    def frame_start(self):
        self.configurationcontrol.plottingcontrol.sensorgramcontrol.resetsensorgram()
        
        


    def change_statistics_value(self):
        self.frame_count += 1
        self.frame_number += 1
        current_time = time.time()
        elapsed_time = current_time - self.last_time

        if elapsed_time >= 1.0:
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0  # Reset frame count
            self.last_time = current_time  # Reset last time

        running_time = self.total_elapsed
        if self.start_segment_time is not None:
            running_time += (current_time - self.start_segment_time)
        
        elapsed = QTime(0, 0).addSecs(int(running_time))
        
        self.view.frame_value_received.setText(f"{self.frame_number}")
        self.view.FPS_value_received.setText(f"{self.fps:.2f}")
        self.view.livetime_value_received.setText(f"{elapsed.toString('hh:mm:ss')}")
        self.view.frame_value_processed.setText(f"{self.frame_number-1}")

    def acquisition_delay_change(self):
        self.timer.setInterval(self.configurationcontrol.acquisitioncontrol.communicationcontrol.delay_time)
        # self.plottingcontrol.sensorgramcontrol.update_frame_time(self.fps)
    
    def clearAll(self):
        self.clear_all_fitting()
        self.clear_average_acquisition()
        self.clear_baseline()
        self.clear_reference()

    def isEnableAllMainUI(self, 
                          start_button_bool,
                          abort_button_bool,
                          rescan_button_bool,
                          uploadrecord_button_bool,
                          device_list_bool):
        
        self.view.configurationlayout.acquisitionlayout.output_spectrum_option.setCurrentText("Raw")
        self.view.start_button.setEnabled(start_button_bool)
        self.view.abort_button.setEnabled(abort_button_bool)
        self.view.rescan_button.setEnabled(rescan_button_bool)
        self.view.uploadrecord_button.setEnabled(uploadrecord_button_bool)
        self.view.device_list.setEnabled(device_list_bool)

    # def isEnableAllConfigurationUI(
    #     self,
    #     output_spectrum_option_bool,
    #     acquisitiondelay_spinbox_bool,
    #     acquisitiondelay_button_bool,
    #     acquisitionaverage_spinbox_bool,
    #     acquisitionaverage_button_bool,
    #     time_integration_spinbox_bool,
    #     time_integration_button_bool,
    #     enable_record_checkbox_bool,
    #     take_dark_button_bool,
    #     clear_dark_button_bool,
    #     save_dark_button_bool,
    #     load_dark_button_bool,
    #     take_bright_button_bool,
    #     clear_bright_button_bool,
    #     save_bright_button_bool,
    #     load_bright_button_bool,
    #     allow_baseline_bool,
    #     polynomial_fitting_button_bool,
    #     gaussian_peak_fitting_button_bool,
    #     lorentzian_peak_fitting_button_bool,
    #     polynomial_peak_fitting_button_bool,
    #     gaussian_peak_width_fitting_button_bool,
    #     lorentzian_peak_width_fitting_button_bool,
    #     autoscale_y_bool,
    #     autoscale_x_bool,
    #     update_fixed_range_bool,
    #     min_range_input_bool,
    #     max_range_input_bool,
    #     select_time_unit_bool,
    #     reset_button_bool,
    #     save_sensorgram_bool,
    #     plot_sensorgram_bool,
    #     fit_interest_y_bool,
    #     fit_interest_x_bool
        
    # ):
    #     self.view.configurationlayout.acquisitionlayout.output_spectrum_option.setEnabled(output_spectrum_option_bool)
    #     self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitiondelay_spinbox.setEnabled(acquisitiondelay_spinbox_bool)
    #     self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitiondelay_button.setEnabled(acquisitiondelay_button_bool)
    #     self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitionaverage_spinbox.setEnabled(acquisitionaverage_spinbox_bool)
    #     self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitionaverage_button.setEnabled(acquisitionaverage_button_bool)
    #     self.view.configurationlayout.acquisitionlayout.communicationlayout.time_integration_spinbox.setEnabled(time_integration_spinbox_bool)
    #     self.view.configurationlayout.acquisitionlayout.communicationlayout.time_integration_button.setEnabled(time_integration_button_bool)
    #     self.view.configurationlayout.acquisitionlayout.savinglayout.enable_record_checkbox.setEnabled(enable_record_checkbox_bool)
    #     self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_dark_button.setEnabled(take_dark_button_bool)
    #     self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_dark_button.setEnabled(clear_dark_button_bool)
    #     self.view.configurationlayout.referencelayout.normalizationspectrumlayout.save_dark_button.setEnabled(save_dark_button_bool)
    #     self.view.configurationlayout.referencelayout.normalizationspectrumlayout.load_dark_button.setEnabled(load_dark_button_bool)
    #     self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_bright_button.setEnabled(take_bright_button_bool)
    #     self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_bright_button.setEnabled(clear_bright_button_bool)
    #     self.view.configurationlayout.referencelayout.normalizationspectrumlayout.save_bright_button.setEnabled(save_bright_button_bool)
    #     self.view.configurationlayout.referencelayout.normalizationspectrumlayout.load_bright_button.setEnabled(load_bright_button_bool)
    #     self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.setEnabled(allow_baseline_bool)
    #     self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.button.setEnabled(polynomial_fitting_button_bool)
    #     self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.button.setEnabled(gaussian_peak_fitting_button_bool)
    #     self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.button.setEnabled(lorentzian_peak_fitting_button_bool)
    #     self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.button.setEnabled(polynomial_peak_fitting_button_bool)
    #     self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.button.setEnabled(gaussian_peak_width_fitting_button_bool)
    #     self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.button.setEnabled(lorentzian_peak_width_fitting_button_bool)
    #     self.view.configurationlayout.plottinglayout.sensorgramlayout.autoscale_y.setEnabled(autoscale_y_bool)
    #     self.view.configurationlayout.plottinglayout.sensorgramlayout.autoscale_x.setEnabled(autoscale_x_bool)
    #     self.view.configurationlayout.plottinglayout.sensorgramlayout.update_fixed_range.setEnabled(update_fixed_range_bool)
    #     self.view.configurationlayout.plottinglayout.sensorgramlayout.min_range_input.setEnabled(min_range_input_bool)
    #     self.view.configurationlayout.plottinglayout.sensorgramlayout.max_range_input.setEnabled(max_range_input_bool)
    #     self.view.configurationlayout.plottinglayout.sensorgramlayout.select_time_unit.setEnabled(select_time_unit_bool)
    #     self.view.configurationlayout.plottinglayout.sensorgramlayout.reset_button.setEnabled(reset_button_bool)
    #     self.view.configurationlayout.plottinglayout.sensorgramlayout.savesensorgram.setEnabled(save_sensorgram_bool)
    #     self.view.configurationlayout.plottinglayout.sensorgramlayout.plotsensorgram.setEnabled(plot_sensorgram_bool)
    #     self.view.configurationlayout.plottinglayout.spectrumlayout.fit_interest_y.setEnabled(fit_interest_y_bool)
    #     self.view.configurationlayout.plottinglayout.spectrumlayout.fit_interest_x.setEnabled(fit_interest_x_bool)


    def isEnableAllConfigurationUI(self, config: dict):
        self.view.configurationlayout.acquisitionlayout.output_spectrum_option.setEnabled(config.get("output_spectrum_option", False))
        self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitiondelay_spinbox.setEnabled(config.get("acquisitiondelay_spinbox", False))
        self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitiondelay_button.setEnabled(config.get("acquisitiondelay_button", False))
        self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitionaverage_spinbox.setEnabled(config.get("acquisitionaverage_spinbox", False))
        self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitionaverage_button.setEnabled(config.get("acquisitionaverage_button", False))
        self.view.configurationlayout.acquisitionlayout.communicationlayout.time_integration_spinbox.setEnabled(config.get("time_integration_spinbox", False))
        self.view.configurationlayout.acquisitionlayout.communicationlayout.time_integration_button.setEnabled(config.get("time_integration_button", False))
        self.view.configurationlayout.acquisitionlayout.savinglayout.enable_record_checkbox.setEnabled(config.get("enable_record_checkbox", False))
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_dark_button.setEnabled(config.get("take_dark_button", False))
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_dark_button.setEnabled(config.get("clear_dark_button", False))
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.save_dark_button.setEnabled(config.get("save_dark_button", False))
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.load_dark_button.setEnabled(config.get("load_dark_button", False))
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_bright_button.setEnabled(config.get("take_bright_button", False))
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_bright_button.setEnabled(config.get("clear_bright_button", False))
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.save_bright_button.setEnabled(config.get("save_bright_button", False))
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.load_bright_button.setEnabled(config.get("load_bright_button", False))
        self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.setEnabled(config.get("allow_baseline", False))
        self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.button.setEnabled(config.get("polynomial_fitting_button", False))
        self.view.configurationlayout.processinglayout.shiftpeaklayout.gaussianpeakfittinglayout.button.setEnabled(config.get("gaussian_peak_fitting_button", False))
        self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.button.setEnabled(config.get("lorentzian_peak_fitting_button", False))
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.button.setEnabled(config.get("polynomial_peak_fitting_button", False))
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.button.setEnabled(config.get("poly_peak_fitting_button", False))
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.button.setEnabled(config.get("gaussian_peak_width_fitting_button", False))
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout.button.setEnabled(config.get("lorentzian_peak_width_fitting_button", False))
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.button.setEnabled(config.get("polynomial_peak_width_fitting_button", False))
        self.view.configurationlayout.plottinglayout.sensorgramlayout.autoscale_y.setEnabled(config.get("autoscale_y", False))
        self.view.configurationlayout.plottinglayout.sensorgramlayout.autoscale_x.setEnabled(config.get("autoscale_x", False))
        self.view.configurationlayout.plottinglayout.sensorgramlayout.update_fixed_range.setEnabled(config.get("update_fixed_range", False))
        self.view.configurationlayout.plottinglayout.sensorgramlayout.min_range_input.setEnabled(config.get("min_range_input", False))
        self.view.configurationlayout.plottinglayout.sensorgramlayout.max_range_input.setEnabled(config.get("max_range_input", False))
        self.view.configurationlayout.plottinglayout.sensorgramlayout.select_time_unit.setEnabled(config.get("select_time_unit", False))
        self.view.configurationlayout.plottinglayout.sensorgramlayout.reset_button.setEnabled(config.get("reset_button", False))
        self.view.configurationlayout.plottinglayout.sensorgramlayout.savesensorgram.setEnabled(config.get("save_sensorgram", False))
        self.view.configurationlayout.plottinglayout.sensorgramlayout.plotsensorgram.setEnabled(config.get("plot_sensorgram", False))
        self.view.configurationlayout.plottinglayout.spectrumlayout.fit_interest_y.setEnabled(config.get("fit_interest_y", False))
        self.view.configurationlayout.plottinglayout.spectrumlayout.fit_interest_x.setEnabled(config.get("fit_interest_x", False))
