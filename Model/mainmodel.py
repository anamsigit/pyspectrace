try:
    from Model.OceanSpectrometer.oceanspectrometermodel import OceanSpectrometer
except:
    pass
try:
    from Model.CNILaserSpectrometer.cnilaserspectrometermodel import CNILaserSpectrometer
except:
    pass
try:
    from Model.AvanterSpectrometer.avantesspectrometermodel import AvantesSpectrometer
except:
    pass

from Model.RecordSpectrometer.recordspectrometermodel import RecordSpectrometer
from Model.SimulatorSpectrometer.simulatorspectrometermodel import SimulatorSpectrometer
from Model.VirtualSpectrometer.virtualspectrometermodel import VirtualSpectrometer


class MainModel:
    def __init__(self):
        self.num_spectrometer = 0
        
        self.init_recordspectrometer_model_name = "None"
        self.available_spectrometer = []
        self.spectrometer_model_name = []
        self.model()
        self.update_list_spectrometer()
        self.selected_spectrometer = self.simulatorspectrometer
        
    def update_list_spectrometer(self):
        self.spectrometer_model_name = [None] * len(self.available_spectrometer)
        for i in range(len(self.available_spectrometer)):
            self.spectrometer_model_name[i] = self.available_spectrometer[i].get_model()
            print(self.spectrometer_model_name[i])

    def model(self):
        # try:
        self.simulatorspectrometer = SimulatorSpectrometer()
        self.available_spectrometer.append(self.simulatorspectrometer)
        # except:
        #     pass
        try:
            self.oceanspectrometer = OceanSpectrometer()
            self.available_spectrometer.append(self.oceanspectrometer)
        except:
            pass
        # try:
        self.virtualspectrometer = VirtualSpectrometer()
        self.available_spectrometer.append(self.virtualspectrometer)
        # except:
        #     pass
        try:
            self.recordspectrometer = RecordSpectrometer(self.init_recordspectrometer_model_name)
            if self.recordspectrometer.get_model() != "None":
                self.available_spectrometer.append(self.recordspectrometer)
        except:
            pass
        try:
            self.cnilaserspectrometer = CNILaserSpectrometer()
            self.available_spectrometer.append(self.cnilaserspectrometer)
        except:
            pass
        try:
            print("avantess")
            self.avantesspectrometer = AvantesSpectrometer()
            self.available_spectrometer.append(self.avantesspectrometer)
            print("avantess pass")
            # pass
        except:
            pass
        # print("avantess")
        # self.avantesspectrometer = AvantesSpectrometer()
        # self.available_spectrometer.append(self.avantesspectrometer)
        # print("avantess pass")

    def __getattr__(self, name):
        return getattr(self.selected_spectrometer, name)
    
    def delete_all_model(self):
        self.available_spectrometer.clear()

    def set_spectrometer(self, spectrometer):
        self.selected_spectrometer = spectrometer
        self.selected_spectrometer.start()

    def change_init_recordspectrometer_model_name(self, model_name):
        self.init_recordspectrometer_model_name = model_name