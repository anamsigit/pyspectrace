import numpy as np
from scipy.optimize import curve_fit
import copy

class PolyPeakFittingControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.wavelengths = np.array([])
        self.intensities = np.array([])
        self.range_wavelengths = np.array([])

        self.intensities_fit = None
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.min_values = [f"{self.model.wavelengths[0 + 1]:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.max_values = [f"{self.model.wavelengths[-1 - 1]:.2f}"]
       
        self.num_fitting = []
        self.num_shiftpeak = []
        self.min_values = []
        self.max_values = []
        self.method_selected = []
        self.inverse_axis = []
        self.orde = []
        self.transform_selected = []
        self.center_func_time = []

    
    def mainloop(self):
        self.acquire()
        if self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.dialog_open:
            self.num_fitting = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.num_fitting)
            self.num_shiftpeak = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.num_shiftpeak)
            self.center_func_time = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.initial_center_values)
            self.orde = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.function_orde)
            self.inverse_axis = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.axis_selected)
            self.transform_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.transform_selected)
            self.method_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.method_selected)
            self.min_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.min_values)
            self.max_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.max_values)
            self.status_inverse = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.status_inverse)

            self.view.plottinglayout.sensorgramlayout.name_polypeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.name_values
            self.view.plottinglayout.spectrumlayout.name_polypeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.name_values
            self.view.plottinglayout.spectrumlayout.color_polyshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.color_values
            self.view.plottinglayout.spectrumlayout.color_polypeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.color_values
            self.view.plottinglayout.sensorgramlayout.color_polyshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.color_values

        self.fitting()
        if self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.dialog_open:
            self.view.plottinglayout.spectrumlayout.init_plot_args()
            self.view.plottinglayout.sensorgramlayout.init_plot_args()
            self.view.configurationlayout.processinglayout.shiftpeaklayout.polypeakfittinglayout.dialog_open = False

    def acquire(self):
        self.wavelengths, self.intensities = self.model.acquire_spectrum()

    def autoguess(self, min_range_index, max_range_index):    
        try:
            init_amplitude = np.max(self.intensities[min_range_index:max_range_index],)
            init_center = np.mean(self.wavelengths[min_range_index:max_range_index],)
            init_sigma = np.std(self.wavelengths[min_range_index:max_range_index],)
        except:
            init_center, init_sigma, init_amplitude = 1,1,1
        return init_center, init_sigma, init_amplitude
  
    def fitting(self):
        cumulative_plot_fitting = []
        cumulative_plot_shiftpeak = []
        cumulative_center = []
        for i in range(len(self.num_fitting)):
            cumulative_center.append([])

        for i in range(len(self.num_fitting)):
            wavelengths_ranged, intensities_fit = self.polynomialfit(int(self.orde[i]),
                float(self.center_func_time[i]) - float(self.min_values[i]), float(self.center_func_time[i]) + float(self.max_values[i])
                )
            
            if self.method_selected[i] == 0:
                index = np.argmax(intensities_fit)
                # cumulative_center[i] = index
                if self.inverse_axis[i] == 0:
                    cumulative_plot_shiftpeak.append((wavelengths_ranged[index], intensities_fit))
                if self.inverse_axis[i] == 1:
                    cumulative_plot_shiftpeak.append((intensities_fit[index], wavelengths_ranged))
            if self.method_selected[i] == 1:
                index = np.argmin(intensities_fit)
                if self.inverse_axis[i] == 0:
                    cumulative_plot_shiftpeak.append((wavelengths_ranged[index], intensities_fit))
                if self.inverse_axis[i] == 1:
                    cumulative_plot_shiftpeak.append((intensities_fit[index], wavelengths_ranged))
            
            cumulative_center[i] =  wavelengths_ranged[index]
            cumulative_plot_fitting.append((wavelengths_ranged, intensities_fit))
            if self.status_inverse[i]:
                self.center_func_time[i] = cumulative_center[i]
            if not self.status_inverse[i]:
                self.center_func_time[i] = self.center_func_time[i]

        self.view.plottinglayout.spectrumlayout.num_polypeakfitting = self.num_fitting
        self.view.plottinglayout.spectrumlayout.plot_polypeakfitting(cumulative_plot_fitting, cumulative_plot_fitting)
        
        self.view.plottinglayout.spectrumlayout.num_polyshiftpeak = self.num_shiftpeak
        self.view.plottinglayout.spectrumlayout.plot_polyshiftpeak(self.inverse_axis, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)

        self.view.plottinglayout.sensorgramlayout.num_polyshiftpeak = self.num_shiftpeak 
        self.view.plottinglayout.sensorgramlayout.plot_polyshiftpeak(self.transform_selected, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)  


    def polynomialfit(self, degree, min_wavelength, max_wavelength):
        min_range = self.wavelengths >= min_wavelength
        max_range = self.wavelengths <= max_wavelength
        selected_wavelengths = self.wavelengths[min_range & max_range]
        
        try:
            selected_intensities = self.intensities[min_range & max_range]
            coeffs = np.polyfit(selected_wavelengths, selected_intensities, deg=degree)
            # self.wavelengths_ranged = np.linspace(min_wavelength, max_wavelength, 1000)
            self.wavelengths_ranged = np.linspace(min_wavelength, max_wavelength, 100*len(selected_wavelengths))
            self.intensities_fit = np.poly1d(coeffs)(self.wavelengths_ranged)
        except:
            self.wavelengths_ranged = [np.nan,np.nan]
            self.intensities_fit = [np.nan,np.nan]
        return self.wavelengths_ranged, self.intensities_fit
    
    