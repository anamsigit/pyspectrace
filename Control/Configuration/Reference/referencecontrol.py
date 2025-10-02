from Control.Configuration.Reference.NormalizationSpectrum.BrightSpectrum.brightspectrumcontrol import BrightSpectrumControl
from Control.Configuration.Reference.NormalizationSpectrum.DarkSpectrum.darkspectrumcontrol import DarkSpectrumControl
from Control.Configuration.Reference.NormalizationSpectrum.normalizationspectrumcontrol import NormalizationSpectrumControl
from Control.Configuration.Reference.BaselineSpectrum.baselinespectrumcontrol import BaselineSpectrumControl
import numpy as np
import warnings

class ReferenceControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.brightspectrumcontrol = BrightSpectrumControl(model, view)
        self.darkspectrumcontrol = DarkSpectrumControl(model, view)
        self.normalizationspectrumcontrol = NormalizationSpectrumControl(model, view)
        self.baselinespectrumcontrol = BaselineSpectrumControl(model, view)
        self.norm_intensities = []

        self.average = 1
        self.sum_intensities = []
        self.sum_wavelengths = []
        self.current_intensities = None
        self.current_wavelengths = None

        self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitionaverage_button.clicked.connect(
            lambda: self.acquisition_average_change(
                self.view.configurationlayout.acquisitionlayout.communicationlayout.acquisitionaverage_spinbox.value()
                )
            )


    def mainloop(self):
        self.normalization_spectrum()
        self.model_normalization()

    def normalization_spectrum(self):
        wavelengths, intensities = self.model.acquire_spectrum_for_normalization()
        self.average_acquisition(wavelengths, intensities)

        wavelengths = self.current_wavelengths
        intensities = self.current_intensities
        
        self.brightreference = self.normalizationspectrumcontrol.brightspectrumcontrol.bright_intensities
        self.darkreference = self.normalizationspectrumcontrol.darkspectrumcontrol.dark_intensities
        # brightreference = self.normalizationspectrumcontrol.brightspectrumcontrol.bright_intensities
        # darkreference = self.normalizationspectrumcontrol.darkspectrumcontrol.dark_intensities

        if len(self.brightreference) == 0 :
            self.view.configurationlayout.acquisitionlayout.output_spectrum_option.setCurrentText("Raw")
            self.view.configurationlayout.acquisitionlayout.output_spectrum_option.setEnabled(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.setEnabled(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.setChecked(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.min_range_input.setEnabled(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.max_range_input.setEnabled(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.plt.clear()
            
        if len(self.darkreference) == 0 :
            self.view.configurationlayout.acquisitionlayout.output_spectrum_option.setCurrentText("Raw")
            self.view.configurationlayout.acquisitionlayout.output_spectrum_option.setEnabled(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.setEnabled(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.setChecked(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.min_range_input.setEnabled(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.max_range_input.setEnabled(False)
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.plt.clear()

        if len(self.brightreference) != 0 and len(self.darkreference) != 0 :
            self.view.configurationlayout.referencelayout.baselinespectrumlayout.allow_baseline.setEnabled(True)
            self.view.configurationlayout.acquisitionlayout.output_spectrum_option.setEnabled(True)

        if self.view.configurationlayout.acquisitionlayout.output_spectrum_option.currentText() == 'Raw':
            self.view.plottinglayout.spectrumlayout.plt.setLabel('left', 'Intensity')
            norm_intensities = intensities

        if self.view.configurationlayout.acquisitionlayout.output_spectrum_option.currentText() == 'Transmision':
            self.view.plottinglayout.spectrumlayout.plt.setLabel('left', 'Transmision')

            # ORIGINAL
            # norm_intensities = (intensities - darkreference) / (brightreference - darkreference)

            # METHOD I
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            norm_intensities = np.where((self.brightreference - self.darkreference) == 0,0,
                                        (intensities - self.darkreference) / (self.brightreference - self.darkreference)
                                        )
            
        if self.view.configurationlayout.acquisitionlayout.output_spectrum_option.currentText() == 'Absorbance':
            self.view.plottinglayout.spectrumlayout.plt.setLabel('left', 'Absorbance')
            # ORIGINAL
            # norm_intensities = (intensities - darkreference) / (brightreference - darkreference)
            # norm_intensities = -np.log10(norm_intensities)

            # METHOD I
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            norm_intensities = np.where((self.brightreference - self.darkreference) == 0,0,
                            (intensities - self.darkreference) / (self.brightreference - self.darkreference)
                            )
            norm_intensities = np.where(norm_intensities <= 0, 0, -np.log10(norm_intensities))

        baseline_average_value = self.baselinespectrumcontrol.baseline_average_value(wavelengths, norm_intensities)
        norm_intensities = norm_intensities - baseline_average_value
        return wavelengths, norm_intensities
    
    def model_normalization(self):
        wavelengths, norm_intensities = self.normalization_spectrum()
        self.model.acquire_spectrum_from_normalization(wavelengths, norm_intensities)

    def average_acquisition(self, wavelength, intensites):
        self.sum_wavelengths.append(wavelength)
        self.sum_intensities.append(intensites)

        if len(self.sum_intensities) >= self.average:
            try:
                # apabila belum memenuhi batas self.average dan ganti rentang panjang gelombang, maka wavelength akan berbeda
                self.current_intensities = np.mean(self.sum_intensities, axis=0)
            except:
                pass
            self.sum_intensities.clear()

        if len(self.sum_wavelengths) >= self.average:
            try:
                # apabila belum memenuhi batas self.average dan ganti rentang panjang gelombang, maka wavelength akan berbeda
                self.current_wavelengths = np.mean(self.sum_wavelengths, axis=0)
            except:
                pass
            self.sum_wavelengths.clear()
        
    def acquisition_average_change(self, slot_average_value):
        self.average = slot_average_value