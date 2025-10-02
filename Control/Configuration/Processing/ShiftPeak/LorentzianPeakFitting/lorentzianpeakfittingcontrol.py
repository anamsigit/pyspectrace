import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
import warnings
import copy

class LorentzianPeakFittingControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.wavelengths = np.array([])
        self.intensities = np.array([])
        self.range_wavelengths = np.array([])

        self.intensities_fit = None
        self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.min_values = [f"{self.model.wavelengths[0 + 1]:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.max_values = [f"{self.model.wavelengths[-1 - 1]:.2f}"]

        self.num_fitting = []
        self.num_shiftpeak = []
        self.min_values = []
        self.max_values = []
        self.method_selected = []
        self.inverse_axis = []
        self.transform_selected = []
        self.center_func_time = []

    def mainloop(self):
        self.acquire()
        if self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.dialog_open:
            self.num_fitting = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.num_fitting)
            self.num_shiftpeak = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.num_shiftpeak)
            self.center_func_time = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.initial_center_values)
            self.min_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.min_values)
            self.max_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.max_values)
            self.method_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.method_selected)
            self.inverse_axis = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.axis_selected)
            self.transform_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.transform_selected)
            self.status_inverse = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.status_inverse)
           
            self.view.plottinglayout.spectrumlayout.name_lorentzianpeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.name_values
            self.view.plottinglayout.sensorgramlayout.name_lorentzianpeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.name_values
            self.view.plottinglayout.spectrumlayout.color_lorentzianshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.color_values
            self.view.plottinglayout.spectrumlayout.color_lorentzianpeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.color_values
            self.view.plottinglayout.sensorgramlayout.color_lorentzianshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.color_values

        self.fitting()
        if self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.dialog_open:
            self.view.plottinglayout.spectrumlayout.init_plot_args()
            self.view.plottinglayout.sensorgramlayout.init_plot_args()
            self.view.configurationlayout.processinglayout.shiftpeaklayout.lorentzianpeakfittinglayout.dialog_open = False
    
    def acquire(self):
        self.wavelengths, self.intensities = self.model.acquire_spectrum()

    def autoguess(self, min_range_index, max_range_index):    
        try:
            init_amplitude = np.max(self.intensities[min_range_index:max_range_index],)
            init_center = np.mean(self.wavelengths[min_range_index:max_range_index],)
            init_sigma = np.std(self.wavelengths[min_range_index:max_range_index],)
            init_intercept = np.std(self.wavelengths[min_range_index:max_range_index],)
        except:
            init_center, init_sigma, init_amplitude, init_intercept = 1,1,1,1
        return init_center, init_sigma, init_amplitude, init_intercept
  
    def fitting(self):
        cumulative_plot_fitting = []
        cumulative_plot_shiftpeak = []
        cumulative_center = []
        for i in range(len(self.num_fitting)):
            cumulative_center.append([])
        
        for i in range(len(self.num_fitting)):
            wavelengths_ranged, intensities_fit, center_fit, sigma_fit, amplitude_fit, intercept_fit = self.lorentzianfit(
                float(self.center_func_time[i]) - float(self.min_values[i]), float(self.center_func_time[i]) + float(self.max_values[i])
                )
            cumulative_center[i] = center_fit
            cumulative_plot_fitting.append((wavelengths_ranged, intensities_fit))
            if self.method_selected[i] ==0:
                if self.inverse_axis[i] == 1:
                    amplitude = amplitude_fit + intercept_fit
                    cumulative_plot_shiftpeak.append((amplitude, wavelengths_ranged))
                if self.inverse_axis[i] == 0:
                    centermass = center_fit
                    cumulative_plot_shiftpeak.append((centermass, intensities_fit)) 
            if self.method_selected[i] ==1:
                if self.inverse_axis[i] == 1:
                    amplitude = self.inflection_function_y(intensities_fit)
                    cumulative_plot_shiftpeak.append((amplitude, wavelengths_ranged))
                if self.inverse_axis[i] == 0:
                    centermass = self.inflection_function_x(intensities_fit)
                    cumulative_plot_shiftpeak.append((centermass, intensities_fit))  
            
            if self.status_inverse[i]:
                self.center_func_time[i] = cumulative_center[i]
            if not self.status_inverse[i]:
                self.center_func_time[i] = self.center_func_time[i]

        self.view.plottinglayout.spectrumlayout.num_lorentzianpeakfitting = self.num_fitting
        self.view.plottinglayout.spectrumlayout.plot_lorentzianpeakfitting(cumulative_plot_fitting, cumulative_plot_fitting)
                
        self.view.plottinglayout.spectrumlayout.num_lorentzianshiftpeak = self.num_shiftpeak
        self.view.plottinglayout.spectrumlayout.plot_lorentzianshiftpeak(self.inverse_axis, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)   
            
        self.view.plottinglayout.sensorgramlayout.num_lorentzianshiftpeak = self.num_shiftpeak
        self.view.plottinglayout.sensorgramlayout.plot_lorentzianshiftpeak(self.transform_selected, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)  

    def lorentzianfit(self, min, max):
        min_range = self.wavelengths >= min
        max_range = self.wavelengths <= max
        min_range_index = np.argmax(min_range)
        max_range_index = np.argmin(max_range)
        init_center, init_sigma, init_amplitude, init_intercept = self.autoguess(min_range_index, max_range_index)
        warnings.filterwarnings('ignore', category=OptimizeWarning)

        try:
            optimized_parameters, covariance_parameters = curve_fit(
                self.lorentzian_function, 
                self.wavelengths[min_range_index:max_range_index], 
                self.intensities[min_range_index:max_range_index],
                p0 = [float(init_center), float(init_sigma), float(init_amplitude), float(init_intercept)],
                maxfev=500
            )
            
            center_fit, sigma_fit, amplitude_fit, intercept_fit = optimized_parameters
            self.intensities_fit = self.lorentzian_function(self.wavelengths[min_range_index:max_range_index], *optimized_parameters)

            self.wavelengths_ranged = self.wavelengths[min_range_index:max_range_index]
        except:
            self.wavelengths_ranged = [np.nan,np.nan]
            self.intensities_fit = [np.nan,np.nan]
            center_fit = np.nan
            sigma_fit = np.nan
            amplitude_fit = np.nan
            intercept_fit = np.nan
        return self.wavelengths_ranged, self.intensities_fit, center_fit, sigma_fit, amplitude_fit, intercept_fit

    def lorentzian_function(self, wavelengths, center, sigma, amplitude, intercept):
        return amplitude / (1 + ((wavelengths - center) / sigma) ** 2) + intercept

    def inflection_function_x(self, intensities_fit):
        secondderivative = np.gradient(np.gradient(intensities_fit))
        infls = np.where(np.diff(np.sign(secondderivative)))[0]
        try:
            inflectionpoint = self.wavelengths_ranged[infls[0]]
        except:
            inflectionpoint = np.nan
        return inflectionpoint

    def inflection_function_y(self, intensities_fit):
        secondderivative = np.gradient(np.gradient(intensities_fit))
        infls = np.where(np.diff(np.sign(secondderivative)))[0]
        try:
            inflectionpoint = intensities_fit[infls[0]]
        except:
            inflectionpoint = np.nan
        return inflectionpoint
            
