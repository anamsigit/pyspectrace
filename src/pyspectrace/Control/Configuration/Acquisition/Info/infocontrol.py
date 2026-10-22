from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QWidget
from datetime import datetime
import os
import re
import time

# Note for githuh changes description: the change statistics from maincontrol was moved to infocontrol.py to make a good separation

class InfoControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.frame_count = 0
        self.frame_number = 0
        self.fps = 1
        self.total_elapsed = 0
        self.start_segment_time = None
        self.last_time = time.time()
        self.processed_frame_number = 0
        self.processed_start_time = None
        self.info_layout = self._find_info_layout()
        if self.info_layout is not None:
            self.info_layout.submit_log_button.clicked.connect(self.submit_log)

    def _find_info_layout(self):
        """Return the Info tab when it is available in the main view."""
        configuration_layout = getattr(self.view, "configurationlayout", None)
        acquisition_layout = getattr(configuration_layout, "acquisitionlayout", None)
        if acquisition_layout is None:
            return None
        return acquisition_layout.findChild(QWidget, "info_layout")

    def mainloop(self):
        sensorgram = [
            self.view.plottinglayout.sensorgramlayout.num_gaussianshiftpeak,
            self.view.plottinglayout.sensorgramlayout.num_lorentzianshiftpeak,
            self.view.plottinglayout.sensorgramlayout.num_polynomialshiftpeak,
            self.view.plottinglayout.sensorgramlayout.num_polyshiftpeak,
            self.view.plottinglayout.sensorgramlayout.num_lorentzianshiftpeakwidth,
            self.view.plottinglayout.sensorgramlayout.num_gaussianshiftpeakwidth,
            self.view.plottinglayout.sensorgramlayout.num_polynomialshiftpeakwidth,
            self.view.plottinglayout.sensorgramlayout.num_polynomialshift
        ]
        total_num_fitting = sum(v.count(None) for v in sensorgram if v is not None)
        current_time = time.time()
        self.change_statistics_value()
        self.update_processed_statistics(total_num_fitting, current_time)

    def start_acquisition(self):
        if self.start_segment_time is None:
            self.start_segment_time = time.time()
        self.last_time = time.time()

    def stop_acquisition(self):
        if self.start_segment_time is not None:
            self.total_elapsed += time.time() - self.start_segment_time
            self.start_segment_time = None
        self.update_livetime()

    def change_statistics_value(self):
        self.frame_count += 1
        self.frame_number += 1
        current_time = time.time()
        elapsed_time = current_time - self.last_time

        if elapsed_time >= 1.0:
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0  # Reset frame count
            self.last_time = current_time  # Reset last time

            # Realtime resolution performance validation
            running_time = self.total_elapsed
            if self.start_segment_time is not None:
                running_time += current_time - self.start_segment_time
            '''
            with open("performance_realtimeacquisition_log.txt", "a") as file:
                file.write(
                    f"{running_time:.2f}\t{self.fps:.2f}\n"
                )
            '''

        self.view.frame_value_received.setText(f"{self.frame_number}")
        self.view.FPS_value_received.setText(f"{self.fps:.2f}")
        self.update_livetime(current_time)

    def update_processed_statistics(self, total_num_fitting, current_time=None):
        if current_time is None:
            current_time = time.time()

        if total_num_fitting > 0:
            if self.processed_start_time is None:
                self.processed_start_time = current_time
                self.processed_frame_number = 0
            self.processed_frame_number += 1
            processed_elapsed = current_time - self.processed_start_time
        else:
            self.processed_start_time = None
            self.processed_frame_number = 0
            processed_elapsed = 0

        elapsed = QTime(0, 0).addSecs(int(processed_elapsed))
        self.view.frame_value_processed.setText(f"{self.processed_frame_number}")
        self.view.livetime_value_processed.setText(elapsed.toString('hh:mm:ss'))

    def update_livetime(self, current_time=None):
        if current_time is None:
            current_time = time.time()
        running_time = self.total_elapsed
        if self.start_segment_time is not None:
            running_time += current_time - self.start_segment_time

        elapsed = QTime(0, 0).addSecs(int(running_time))
        self.view.livetime_value_received.setText(elapsed.toString('hh:mm:ss'))

    def submit_log(self):
        """Submit the text from the Info tab with the current statistics."""
        if self.info_layout is None:
            return None

        log_name = self.info_layout.log_name_textbox.text().strip()
        log_message = self.info_layout.log_message_textbox.toPlainText()
        return self.logging(log_name, log_message)

    def logging(self, log_name="", log_message=""):
        """Append an Info-tab entry and the current statistics to a text file."""
        if not log_name.strip():
            return None

        acquisition_layout = self.view.configurationlayout.acquisitionlayout
        communication_layout = acquisition_layout.communicationlayout
        saving_layout = acquisition_layout.savinglayout
        statistics = {
            "Log name": log_name,
            "Message": log_message,
            "Refresh rate (ms)": communication_layout.acquisitiondelay_spinbox.value(),
            "Integration time (µs)": communication_layout.time_integration_spinbox.value(),
            "Acquisition average": communication_layout.acquisitionaverage_spinbox.value(),
            "Enable record spectrum": saving_layout.enable_record_checkbox.isChecked(),
            "Preview save path": saving_layout.text_edit.toPlainText(),
            "Saving interval (s)": saving_layout.interval_saving.value(),
            "Output spectrum": acquisition_layout.output_spectrum_option.currentText(),
            "Received spectra": self.view.frame_value_received.text(),
            "Received spectra/sec": self.view.FPS_value_received.text(),
            "Received elapsed time": self.view.livetime_value_received.text(),
            "Processed spectra": self.view.frame_value_processed.text(),
            "Processed elapsed time": self.view.livetime_value_processed.text(),
            "Saved record count": self.view.record_value_saved.text(),
        }

        log_text = "\n".join(f"{label}: {value}" for label, value in statistics.items())
        log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n{log_text}\n\n"
        safe_log_name = re.sub(r'[<>:"/\\\\|?*]+', "_", log_name).strip(". ")
        if not safe_log_name:
            return None
        if not safe_log_name.lower().endswith(".txt"):
            safe_log_name = f"{safe_log_name}.txt"

        log_path = os.path.join(os.getcwd(), safe_log_name)
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
        print(f"Log appended to: {log_path}")
        return log_text
