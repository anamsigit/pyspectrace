import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
import warnings
import copy

class GaussianWidthPeakFittingControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.wavelengths = np.array([])
        self.intensities = np.array([])
        self.range_wavelengths = np.array([])

        self.intensities_fit = None
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.min_values = [f"{self.model.wavelengths[0 + 1]:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.max_values = [f"{self.model.wavelengths[-1 - 1]:.2f}"]

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
        if self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.dialog_open:
            self.num_fitting = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.num_fitting)
            self.num_shiftpeak = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.num_shiftpeak)
            self.center_func_time = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.initial_center_values)
            self.inverse_axis = [1] * len(self.num_fitting)
            self.min_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.min_values)
            self.max_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.max_values)
            self.method_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.method_selected)
            # self.inverse_axis = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.axis_selected)
            self.transform_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.transform_selected)
            self.status_inverse = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.status_inverse)
           
            self.view.plottinglayout.spectrumlayout.name_gaussianpeakwidthfitting = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.name_values
            self.view.plottinglayout.sensorgramlayout.name_gaussianpeakwidthfitting = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.name_values
            self.view.plottinglayout.spectrumlayout.color_gaussianshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.color_values
            self.view.plottinglayout.spectrumlayout.color_gaussianpeakwidthfitting = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.color_values
            self.view.plottinglayout.sensorgramlayout.color_gaussianshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.color_values


        self.fitting()
        if self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.dialog_open:
            self.view.plottinglayout.spectrumlayout.init_plot_args()
            self.view.plottinglayout.sensorgramlayout.init_plot_args()
            self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout.dialog_open = False

    
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
        cumulative_center = []
        cumulative_plot_fitting = []
        cumulative_plot_shiftpeak = []
        cumulative_fwhm = []
        for i in range(len(self.num_fitting)):
            cumulative_center.append([])

        for i in range(len(self.num_fitting)):
            wavelengths_ranged, intensities_fit, center_fit, sigma_fit, amplitude_fit, intercept_fit = self.gaussianfit(
                float(self.center_func_time[i]) - float(self.min_values[i]), float(self.center_func_time[i]) + float(self.max_values[i])
                )
            if self.method_selected[i] == 0:
                percent = 0.50
                I_target = amplitude_fit * percent
                delta_x = sigma_fit * np.sqrt(-2 * np.log(percent))
                x1 = center_fit - delta_x
                x2 = center_fit + delta_x
                plot = x1, x2
                width = x2 - x1
                cumulative_fwhm.append((width, plot))
                cumulative_plot_shiftpeak.append((I_target  + intercept_fit, plot))      
            
            cumulative_center[i] = center_fit
            cumulative_plot_fitting.append((wavelengths_ranged, intensities_fit))
            if self.status_inverse[i]:
                self.center_func_time[i] = cumulative_center[i]
            if not self.status_inverse[i]:
                self.center_func_time[i] = self.center_func_time[i]

        self.view.plottinglayout.spectrumlayout.num_gaussianpeakwidthfitting = self.num_fitting
        self.view.plottinglayout.spectrumlayout.plot_gaussianpeakwidthfitting(cumulative_plot_fitting, cumulative_plot_fitting)
                
        self.view.plottinglayout.spectrumlayout.num_gaussianshiftpeakwidth = self.num_shiftpeak 
        self.view.plottinglayout.spectrumlayout.plot_gaussianshiftpeakwidth(self.inverse_axis, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)   
            
        self.view.plottinglayout.sensorgramlayout.num_gaussianshiftpeakwidth = self.num_shiftpeak
        self.view.plottinglayout.sensorgramlayout.plot_gaussianshiftpeakwidth(self.transform_selected, cumulative_fwhm, cumulative_fwhm)

    def gaussianfit(self, min, max):
        min_range = self.wavelengths >= min
        max_range = self.wavelengths <= max
        min_range_index = np.argmax(min_range)
        max_range_index = np.argmin(max_range)
        init_center, init_sigma, init_amplitude, init_intercept = self.autoguess(min_range_index, max_range_index)
        warnings.filterwarnings('ignore', category=OptimizeWarning)

        try:
            optimized_parameters, covariance_parameters = curve_fit(
                self.gaussian_function, 
                self.wavelengths[min_range_index:max_range_index], 
                self.intensities[min_range_index:max_range_index],
                p0 = [float(init_center), float(init_sigma), float(init_amplitude), float(init_intercept)],
                maxfev=500
            )
            
            center_fit, sigma_fit, amplitude_fit, intercept_fit = optimized_parameters
            self.intensities_fit = self.gaussian_function(self.wavelengths[min_range_index:max_range_index], *optimized_parameters)
            self.wavelengths_ranged = self.wavelengths[min_range_index:max_range_index]
        except:
            self.wavelengths_ranged = [np.nan,np.nan]
            self.intensities_fit = [np.nan,np.nan]
            center_fit = np.nan
            sigma_fit = np.nan
            amplitude_fit = np.nan
            intercept_fit = np.nan
        return self.wavelengths_ranged, self.intensities_fit, center_fit, sigma_fit, amplitude_fit, intercept_fit

    def gaussian_function(self, wavelengths, center, sigma, amplitude, intercept):
        return amplitude * np.exp(-0.5 * ((wavelengths - center) / sigma) ** 2) + intercept
    

