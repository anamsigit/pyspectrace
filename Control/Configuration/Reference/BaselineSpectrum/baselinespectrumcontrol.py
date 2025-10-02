import numpy as np
import os

class BaselineSpectrumControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view

        # self.wavelengths = np.array([])
        # self.intensities = np.array([])

        # self.baseline_wavelengths = np.array([])
        # self.baseline_intensities = np.array([])

        self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.clicked.connect(self.disable_range)
        
        self.view.configurationlayout.referencelayout.baselinespectrumlayout.min_range_input.setRange(self.model.wavelengths[0], 10000)
        self.view.configurationlayout.referencelayout.baselinespectrumlayout.max_range_input.setRange(self.model.wavelengths[0], 10000)
        self.mainpath = os.path.dirname(os.path.dirname(os.getcwd()))

    def baseline_average_value(self, wavelengths, norm_intensities):
        min_values = float(self.view.configurationlayout.referencelayout.baselinespectrumlayout.min_range_input.value())
        max_values = float(self.view.configurationlayout.referencelayout.baselinespectrumlayout.max_range_input.value())

        if min_values <= wavelengths[0]:
            min_values = wavelengths[0]
        if max_values >= wavelengths[-1]:
            max_values = wavelengths[-1]

        closest_index_min = np.argmin(np.abs(wavelengths - min_values))
        closest_index_max = np.argmin(np.abs(wavelengths - max_values))
        wavelengths = wavelengths[closest_index_min:closest_index_max]  
        intensities = norm_intensities[closest_index_min:closest_index_max] 
        
        if len(intensities) != 0:
            average_value = np.mean(intensities)
        if len(intensities) == 0:
            average_value = 0
        
        if not self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.isChecked():
            average_value = 0
        else:
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.plot_spectrum(wavelengths, intensities)
        return average_value

    def disable_range(self):
        if self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.isChecked():
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.min_range_input.setEnabled(True)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.max_range_input.setEnabled(True)
        else:
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.min_range_input.setDisabled(True)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.max_range_input.setDisabled(True)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.plt.clear()
        