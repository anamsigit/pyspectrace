from PyQt5.QtCore import QTimer
import numpy as np

class CommunicationControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.delay_time = 250

        self.view.configurationlayout.acquisitionlayout.communicationlayout.time_integration_button.clicked.connect(
            lambda: self.integration_time_change(
                self.view.configurationlayout.acquisitionlayout.communicationlayout.time_integration_spinbox.value()
                )
            )
        self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitiondelay_button.clicked.connect(
            lambda: self.acquisition_delay_change(
                self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitiondelay_spinbox.value()
                )
            )
    
    def mainloop(self):
        self.acquire()

    def acquire(self):
        cumulative_plot = [self.model.acquire_spectrum()]       
        self.view.plottinglayout.spectrumlayout.num_spectrum = [None]
        self.view.plottinglayout.spectrumlayout.plot_spectrum(cumulative_plot, cumulative_plot)

    def integration_time_change(self, slot_integration_value):
        self.model.set_integration_time(slot_integration_value)

    def acquisition_delay_change(self, slot_delay_value):
        self.delay_time = slot_delay_value
        self.model.set_acquisition_delay(slot_delay_value)

