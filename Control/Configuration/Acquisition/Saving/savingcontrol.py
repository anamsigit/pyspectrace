import numpy as np
from datetime import datetime, timedelta
import time
import os
from PyQt5.QtCore import Qt

class SavingControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.mainpath = self.view.configurationlayout.acquisitionlayout.savinglayout.combined_path_text
        self.processed_wavelengths = None
        self.processed_intensities = None

        self.raw_wavelengths = None
        self.raw_intensities = None

        self.stateresume = True

        self.current_forprogress = 0
        self.elapsed_time = 0

        # self.current_progress = 0
        self.count_saved = 0

        self.cumulative_delta_time = 0
        self.frame_list_txt = 0
        self.cumulative_delta_time_raw = 0

        self.cumulative_delta_time_list = []
        self.cumulative_delta_time_list_raw = []

        self.delta_timestart = datetime.now()   
        # self.delta_timestart_raw = datetime.now()
        # self.delta_timestart = time.perf_counter()      
        # self.delta_timestart_raw = time.perf_counter()
        self.start_time = datetime.now()
        self.start_time_progress = datetime.now()

        self.view.configurationlayout.acquisitionlayout.savinglayout.enable_record_checkbox.stateChanged.connect(self.inittime_save_slot)
        self.view.configurationlayout.acquisitionlayout.savinglayout.apply_button.clicked.connect(self.init_time_save)
        self.view.configurationlayout.acquisitionlayout.savinglayout.pauseresumebuttom.clicked.connect(self.pauseresumestate)

    def mainloop(self):
        if self.view.configurationlayout.acquisitionlayout.savinglayout.status_saving:     
            if self.stateresume:
                _current_time = datetime.now()
                self.elapsed_time = (_current_time - self.start_time).total_seconds()
                
                interval = self.view.configurationlayout.acquisitionlayout.savinglayout.interval_saving.value()
                progress_percent = min(int((self.elapsed_time / interval) * 100), 100)
                self.view.configurationlayout.acquisitionlayout.savinglayout.progress.setValue(progress_percent)
                
                
                if self.elapsed_time >= self.view.configurationlayout.acquisitionlayout.savinglayout.interval_saving.value():
                    self.intervalstart()
                    self.savingtxt()
                    self.start_time = _current_time
                    self.current_progress = 0
                    self.view.record_value_saved.setText(f"{self.count_saved}")
                    self.view.configurationlayout.acquisitionlayout.savinglayout.progress.setValue(0)
                    self.intervalend()
            else:
                _current_time = datetime.now()
                self.start_time = _current_time - timedelta(seconds=self.elapsed_time)

                self.delta_timestart =  _current_time - timedelta(seconds=self.elapsed_time)
                # self.delta_timestart_raw =  _current_time - timedelta(seconds=self.elapsed_time)


    def pauseresumestate(self):
        if self.view.configurationlayout.acquisitionlayout.savinglayout.pauseresumebuttom.text() == "Pause":
            self.stateresume = False
            self.view.configurationlayout.acquisitionlayout.savinglayout.pauseresumebuttom.setText("Resume")

        elif self.view.configurationlayout.acquisitionlayout.savinglayout.pauseresumebuttom.text() == "Resume":
            self.stateresume = True
            self.view.configurationlayout.acquisitionlayout.savinglayout.pauseresumebuttom.setText("Pause")

    def intervalstart(self):
        self.current_time = datetime.now()
        self.current_time_raw = datetime.now()

    def intervalend(self):
        self.delta_timestart = self.delta_timeend 
        # self.delta_timestart_raw = self.delta_timeend_raw
    
    def savingtxt(self):
        processed_wavelengths, processed_intensities = self.model.acquire_spectrum()
        raw_wavelengths, raw_intensities = self.model.acquire_spectrum_for_normalization()

        self.delta_timeend = datetime.now()
        self.delta_timeend_raw = datetime.now()
        # self.delta_timeend = time.perf_counter()
        # self.delta_timeend_raw = time.perf_counter()

        self.delta_time = (self.delta_timeend - self.delta_timestart).total_seconds()
        self.delta_time = np.array(self.delta_time)
        self.delta_time = np.full(len(processed_intensities), self.delta_time)
        
        self.frame_list_txt = self.frame_list_txt + 1

        processed_data = [processed_wavelengths, processed_intensities, self.delta_time]
        raw_data = [raw_wavelengths, raw_intensities, self.delta_time]

        processed_data_transposed = list(map(list, zip(*processed_data)))
        raw_data_transposed = list(map(list, zip(*raw_data)))

        filename = self.current_time.strftime("%Y-%m-%d_%H-%M-%S")

        self.mainpath = self.view.configurationlayout.acquisitionlayout.savinglayout.combined_path_text
        os.makedirs(os.path.join(self.mainpath, 'processed'), exist_ok=True)
        os.makedirs(os.path.join(self.mainpath, 'raw'), exist_ok=True)

        save_path_processed = os.path.join(self.mainpath, 'processed', f'{self.frame_list_txt}-index-processed_spectrum_{filename}.txt')
        save_path_raw = os.path.join(self.mainpath, 'raw', f'{self.frame_list_txt}-index-raw_spectrum_{filename}.txt')

        for sublist in processed_data_transposed:
            sublist.append(self.current_time.strftime("%Y-%m-%d %H-%M-%S-%f"))
        try:
            with open(save_path_processed, "w") as file:
                file.write(("[wavelength, intensities, timedelta, date, time]") + "\n")
                file.write((">>>>>Begin Processed Spectral Data<<<<<") + "\n")
                for sublist in processed_data_transposed:
                    file.write(" ".join(map(str, sublist)) + "\n")
                file.write((">>>>>End Processed Spectral Data<<<<<") + "\n")
                self.count_saved = self.count_saved + 1
        except:
            print("error txt processed saved")
            pass

        for sublist in raw_data_transposed:
            sublist.append(self.current_time.strftime("%Y-%m-%d %H-%M-%S-%f"))
        try:
            with open(save_path_raw, "w") as file:
                file.write(("[wavelength, intensities, timedelta, date, time]") + "\n")
                file.write((">>>>>Begin Processed Spectral Data<<<<<") + "\n")
                for sublist in raw_data_transposed:
                    file.write(" ".join(map(str, sublist)) + "\n")
                file.write((">>>>>End Processed Spectral Data<<<<<") + "\n")
            self.count_saved = self.count_saved + 1
        except:
            print("error txt raw saved")
            pass


    def inittime_save_slot(self, state):
        if state == 2:
            self.view.configurationlayout.acquisitionlayout.savinglayout.inittime_save = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
            self.view.configurationlayout.acquisitionlayout.savinglayout.update_combined_text()
            self.mainpath = self.view.configurationlayout.acquisitionlayout.savinglayout.combined_path_text

        if state == 0:
            self.count_saved = 0
            self.view.record_value_saved.setText(f"{self.count_saved}")
    
    def init_time_save(self):
            if self.view.configurationlayout.acquisitionlayout.savinglayout.syncsensorgram.isChecked():
                self.view.configurationlayout.plottinglayout.sensorgramlayout.reset_button.click()

            self.processed_wavelengths = None
            self.processed_intensities = None

            self.raw_wavelengths = None
            self.raw_intensities = None

            # self.current_progress = 0
            self.current_forprogress = 0
            self.count_saved = 0
            

            self.cumulative_delta_time = 0
            self.frame_list_txt = 0
            self.cumulative_delta_time_raw = 0

            self.delta_timestart = datetime.now()     
            # self.delta_timestart = time.perf_counter()      
            self.cumulative_delta_time_list = []
            # self.delta_timestart_raw = datetime.now()
            # self.delta_timestart_raw = time.perf_counter()
            self.cumulative_delta_time_list_raw = []
            self.start_time = datetime.now()
            self.start_time_progress = datetime.now()
        
            

    def onesecond_left(self, start_time):
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time >= 0.1:
            return True
        return False