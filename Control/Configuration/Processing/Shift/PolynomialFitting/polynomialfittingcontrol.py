import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
import warnings
import copy

class PolynomialFittingControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.wavelengths = np.array([])
        self.intensities = np.array([])
        self.range_wavelengths = np.array([])

        self.intensities_fit = None
        self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.min_values = [f"{self.model.wavelengths[0 + 1]:.2f}"]
        self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.max_values = [f"{self.model.wavelengths[-1 - 1]:.2f}"]
    
        self.num_fitting = []
        self.num_shiftpeak = []
        self.min_values = []
        self.max_values = []
        self.transform_selected = []
        self.center_func_time = []
        self.inverse_axis = []

    def mainloop(self):
        self.acquire()
        if self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.dialog_open:
            self.num_fitting = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.num_fitting)
            self.num_shiftpeak = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.num_shiftpeak)
            self.center_func_time = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.initial_center_values)
            self.min_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.min_values)
            self.max_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.max_values)
            self.orde = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.function_orde)
            self.inverse_axis = [1] * len(self.num_fitting)
            self.transform_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.transform_selected)
            self.status_inverse = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.status_inverse)
           
            self.view.plottinglayout.spectrumlayout.name_polynomialfitting = self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.name_values
            self.view.plottinglayout.sensorgramlayout.name_polynomialfitting = self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.name_values
            self.view.plottinglayout.spectrumlayout.color_polynomialshift = self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.color_values
            self.view.plottinglayout.spectrumlayout.color_polynomialfitting = self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.color_values
            self.view.plottinglayout.sensorgramlayout.color_polynomialshift = self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.color_values

        self.fitting()
        if self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.dialog_open:
            self.view.plottinglayout.spectrumlayout.init_plot_args()
            self.view.plottinglayout.sensorgramlayout.init_plot_args()
            self.view.configurationlayout.processinglayout.shiftlayout.polynomialfittinglayout.dialog_open = False

    def acquire(self):
        self.wavelengths, self.intensities = self.model.acquire_spectrum()

    def autoguess(self, min_range_index, max_range_index):    
        init_amplitude = np.max(self.intensities[min_range_index:max_range_index],)
        init_center = np.mean(self.wavelengths[min_range_index:max_range_index],)
        init_sigma = np.std(self.wavelengths[min_range_index:max_range_index],)
        return init_center, init_sigma, init_amplitude
  
    def fitting(self):
        cumulative_plot_fitting = []
        cumulative_plot_shiftpeak = []

        for i in range(len(self.num_fitting)):
            # wavelengths_ranged, intensities_fit, center_fit, sigma_fit, amplitude_fit, intercept_fit = self.polynomialfit(
            #     float(self.center_func_time[i]) - float(self.min_values[i]), float(self.center_func_time[i]) + float(self.max_values[i])
            #     )
                        
            # floatspecific = float(self.center_func_time[i])
            # if floatspecific < float(self.min_values[i]):
            #     floatspecific = float(self.min_values[i])
            # if floatspecific > float(self.max_values[i]):
            #     floatspecific = float(self.max_values[i])

            if int(self.orde[i]) > 0:
                wavelengths_ranged, intensities_fit = self.polynomialfit(int(self.orde[i]), 
                    float(self.center_func_time[i]) - float(self.min_values[i]), float(self.center_func_time[i]) + float(self.max_values[i])
                    )
            if int(self.orde[i]) == 0:
                wavelengths_ranged, intensities_fit = self.raw(
                    float(self.center_func_time[i]) - float(self.min_values[i]), float(self.center_func_time[i]) + float(self.max_values[i])
                    )


            cumulative_plot_fitting.append((wavelengths_ranged, intensities_fit))
            closest_index = np.argmin(np.abs(wavelengths_ranged - float(self.center_func_time[i])))
            # closest_index = np.abs(wavelengths_ranged - np.array(self.center_func_time[i], dtype=np.float64)).argmin()
            # closest_index = np.argmin(np.abs(self.center_func_time[i]))
            cumulative_plot_shiftpeak.append((intensities_fit[closest_index], wavelengths_ranged))                     

        self.view.plottinglayout.spectrumlayout.num_polynomialfitting = self.num_fitting
        self.view.plottinglayout.spectrumlayout.plot_polynomialfitting(cumulative_plot_fitting, cumulative_plot_fitting)
        
        self.view.plottinglayout.spectrumlayout.num_polynomialshift = self.num_shiftpeak
        self.view.plottinglayout.spectrumlayout.plot_polynomialshift(self.inverse_axis, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)

        self.view.plottinglayout.sensorgramlayout.num_polynomialshift = self.num_shiftpeak
        self.view.plottinglayout.sensorgramlayout.plot_polynomialshift(self.transform_selected, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)  


    def polynomialfit(self, degree, min_wavelength, max_wavelength):
        min_range = self.wavelengths >= min_wavelength
        max_range = self.wavelengths <= max_wavelength

        selected_wavelengths = self.wavelengths[min_range & max_range]
        selected_intensities = self.intensities[min_range & max_range]
        warnings.filterwarnings('ignore', category=OptimizeWarning)


        coeffs = np.polyfit(selected_wavelengths, selected_intensities, deg=degree)
        wavelengths_ranged = np.linspace(min_wavelength, max_wavelength, len(selected_wavelengths))
        intensities_fit = np.poly1d(coeffs)(wavelengths_ranged)
        return wavelengths_ranged, intensities_fit
    
    def raw(self, min_wavelength, max_wavelength):
        min_range = self.wavelengths >= min_wavelength
        max_range = self.wavelengths <= max_wavelength

        selected_wavelengths = self.wavelengths[min_range & max_range]
        selected_intensities = self.intensities[min_range & max_range]

        wavelengths_ranged = selected_wavelengths
        intensities_fit = selected_intensities
        return wavelengths_ranged, intensities_fit
    