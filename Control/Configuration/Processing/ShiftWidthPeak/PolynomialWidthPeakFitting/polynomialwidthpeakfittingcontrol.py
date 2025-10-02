import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
import copy
import warnings

class PolynomialWidthPeakFittingControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.wavelengths = np.array([])
        self.intensities = np.array([])
        self.range_wavelengths = np.array([])

        self.intensities_fit = None
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.min_values = [f"{self.model.wavelengths[0 + 1]:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.max_values = [f"{self.model.wavelengths[-1 - 1]:.2f}"]
    
        self.num_fitting = []
        self.num_shiftpeak = []
        self.min_values = []
        self.max_values = []
        self.orde = []
        self.method_selected = []
        self.inverse_axis = []
        self.transform_selected = []
        self.center_func_time = []

    def mainloop(self):
        self.acquire()
        if self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.dialog_open:
            self.num_fitting = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.num_fitting)
            self.num_shiftpeak = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.num_shiftpeak)
            self.center_func_time = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.initial_center_values)
            self.inverse_axis = [1] * len(self.num_fitting)
            self.min_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.min_values)
            self.max_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.max_values)
            self.method_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.method_selected)
            self.orde = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.function_orde)
            # self.inverse_axis = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.axis_selected)
            self.transform_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.transform_selected)
            self.status_inverse = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.status_inverse)
           
            self.view.plottinglayout.spectrumlayout.name_polynomialpeakwidthfitting = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.name_values
            self.view.plottinglayout.sensorgramlayout.name_polynomialpeakwidthfitting = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.name_values
            self.view.plottinglayout.spectrumlayout.color_polynomialshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.color_values
            self.view.plottinglayout.spectrumlayout.color_polynomialpeakwidthfitting = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.color_values
            self.view.plottinglayout.sensorgramlayout.color_polynomialshiftpeakwidth = self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.color_values


        self.fitting()
        if self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.dialog_open:
            self.view.plottinglayout.spectrumlayout.init_plot_args()
            self.view.plottinglayout.sensorgramlayout.init_plot_args()
            self.view.configurationlayout.processinglayout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout.dialog_open = False

    def acquire(self):
        self.wavelengths, self.intensities = self.model.acquire_spectrum()

    def autoguess(self, min_range_index, max_range_index):    
        init_amplitude = np.max(self.intensities[min_range_index:max_range_index],)
        init_center = np.mean(self.wavelengths[min_range_index:max_range_index],)
        init_sigma = np.std(self.wavelengths[min_range_index:max_range_index],)
        return init_center, init_sigma, init_amplitude
  
    def fitting(self):
        cumulative_center = []
        cumulative_plot_fitting = []
        cumulative_plot_shiftpeak = []
        cumulative_fwhm = []
        for i in range(len(self.num_fitting)):
            cumulative_center.append([])
        # for i in range(len(self.num_fitting)):
        #     wavelengths_ranged, intensities_fit = self.polynomialfit(int(orde[i]), self.min_values[i], max_values)
        #     cumulative_plot_fitting.append((wavelengths_ranged, intensities_fit))
        for i in range(len(self.num_fitting)):
            wavelengths_ranged, intensities_fit = self.polynomialfit(int(self.orde[i]),
                float(self.center_func_time[i]) - float(self.min_values[i]), float(self.center_func_time[i]) + float(self.max_values[i])
                )
            y_mid = (intensities_fit[np.argmin(intensities_fit)] + intensities_fit[np.argmax(intensities_fit)]) / 2
            crossings = []
            for k in range(len(intensities_fit) - 1):
                y0, y1 = intensities_fit[k], intensities_fit[k+1]
                if (y0 - y_mid) * (y1 - y_mid) < 0:
                    x0, x1 = wavelengths_ranged[k], wavelengths_ranged[k+1]
                    x_cross = x0 + (x1 - x0) * ((y_mid - y0) / (y1 - y0))
                    crossings.append(x_cross)

            if len(crossings) >= 2:
                shortest_pair = min(
                    [(crossings[k], crossings[l]) for k in range(len(crossings)) for l in range(k+1, len(crossings))],
                    key=lambda pair: abs(pair[1] - pair[0])
                )
                x_start, x_end = shortest_pair
                wavelengths_cut = np.linspace(x_start, x_end, 100)

                cumulative_plot_shiftpeak.append((y_mid, wavelengths_cut))                  
                width = wavelengths_cut[-1] - wavelengths_cut[0]
                center_fit = (wavelengths_cut[0] + wavelengths_cut[-1])/2
                cumulative_fwhm.append((width, wavelengths_cut))
            else:

                cumulative_plot_shiftpeak.append((y_mid, wavelengths_ranged))                  
                width = wavelengths_ranged[-1] - wavelengths_ranged[0]
                center_fit = (wavelengths_ranged[0] + wavelengths_ranged[-1])/2
                cumulative_fwhm.append((width, wavelengths_ranged))
            
            cumulative_center[i] = center_fit
            cumulative_plot_fitting.append((wavelengths_ranged, intensities_fit))
            cumulative_plot_fitting.append((wavelengths_ranged, intensities_fit))
            if self.status_inverse[i]:
                self.center_func_time[i] = cumulative_center[i]
            if not self.status_inverse[i]:
                self.center_func_time[i] = self.center_func_time[i]  

        self.view.plottinglayout.spectrumlayout.num_polynomialpeakwidthfitting = self.num_fitting
        self.view.plottinglayout.spectrumlayout.plot_polynomialpeakwidthfitting(cumulative_plot_fitting, cumulative_plot_fitting)
        
        self.view.plottinglayout.spectrumlayout.num_polynomialshiftpeakwidth = self.num_shiftpeak
        self.view.plottinglayout.spectrumlayout.plot_polynomialshiftpeakwidth(self.inverse_axis, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)

        self.view.plottinglayout.sensorgramlayout.num_polynomialshiftpeakwidth = self.num_shiftpeak 
        self.view.plottinglayout.sensorgramlayout.plot_polynomialshiftpeakwidth(self.transform_selected, cumulative_fwhm, cumulative_fwhm)  


    def polynomialfit(self, degree, min_wavelength, max_wavelength):
        min_range = self.wavelengths >= min_wavelength
        max_range = self.wavelengths <= max_wavelength
        # warnings.filterwarnings('ignore', category=OptimizeWarning)
        # warnings.filterwarnings('ignore', category=UserWarning)


        selected_wavelengths = self.wavelengths[min_range & max_range]
        selected_intensities = self.intensities[min_range & max_range]
        coeffs = np.polyfit(selected_wavelengths, selected_intensities, deg=degree)
        wavelengths_ranged = np.linspace(min_wavelength, max_wavelength, len(selected_wavelengths))
        intensities_fit = np.poly1d(coeffs)(wavelengths_ranged)
        return wavelengths_ranged, intensities_fit
    
    