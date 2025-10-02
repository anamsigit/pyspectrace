import numpy as np
from scipy.optimize import curve_fit, fsolve, minimize_scalar, root, root_scalar, OptimizeWarning
import threading
import warnings
import copy

class PolynomialPeakFittingControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # warnings.filterwarnings('ignore', category=np.RankWarning)

        self.wavelengths = np.array([])
        self.intensities = np.array([])
        self.range_wavelengths = np.array([])

        self.intensities_fit = None
        self.frame_indicate = []
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.min_values = [f"{self.model.wavelengths[0 + 1]:.2f}"]
        self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.max_values = [f"{self.model.wavelengths[-1 - 1]:.2f}"]
    

        self.num_fitting = []
        self.num_shiftpeak = []
        self.min_values = []
        self.max_values = []
        self.span = []
        self.method_selected = []
        self.inverse_axis = []
        self.transform_selected = []
        self.center_func_time = []

    def mainloop(self):
        self.acquire()
        if self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.dialog_open:
            self.num_fitting = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.num_fitting)
            self.num_shiftpeak = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.num_shiftpeak)
            self.inverse_axis = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.axis_selected)
            self.orde = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.function_orde)
            self.transform_selected = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.transform_selected)
            self.span = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.span_values)
            self.center_func_time = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.initial_center_values)
            self.min_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.min_values)
            self.max_values = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.max_values)
            self.status_inverse = copy.deepcopy(self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.status_inverse)

            self.view.plottinglayout.sensorgramlayout.name_polynomialpeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.name_values
            self.view.plottinglayout.spectrumlayout.name_polynomialpeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.name_values
            self.view.plottinglayout.spectrumlayout.color_polynomialshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.color_values
            self.view.plottinglayout.spectrumlayout.color_polynomialpeakfitting = self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.color_values
            self.view.plottinglayout.sensorgramlayout.color_polynomialshiftpeak = self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.color_values
        
        
        
        self.fitting()
        if self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.dialog_open:
            self.view.plottinglayout.spectrumlayout.init_plot_args()
            self.view.plottinglayout.sensorgramlayout.init_plot_args()
            self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.dialog_open = False

    def acquire(self):
        self.wavelengths, self.intensities = self.model.acquire_spectrum()
  
    def fitting(self):
        cumulative_plot_fitting = []
        cumulative_plot_shiftpeak = []
        cumulative_center = []
        for i in range(len(self.num_fitting)):
            cumulative_center.append([])
        
        for i in range(len(self.num_fitting)):
            # wavelengths_ranged, intensities_fit, center_fit = self.polynomialfit(int(orde[i]), min_values, max_values, float(span[i]), float(peakguess[i]))
            wavelengths_ranged, intensities_fit, centermass = self.polynomialfit(int(self.orde[i]),
                float(self.center_func_time[i]) - float(self.min_values[i]), float(self.center_func_time[i]) + float(self.max_values[i]),
                float(self.span[i]),
                float(self.center_func_time[i]),
                )
            
                
            if self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.method_selected[i] ==0:
                if self.inverse_axis[i] == 1:
                    pass # not this
                if self.inverse_axis[i] == 0:
                    index = np.argmax(intensities_fit)
                    center_fit = wavelengths_ranged[index]
                    # peak gues untuk input centermass adalah puncak tertinggi dari polynomial
                    cumulative_plot_shiftpeak.append((centermass, intensities_fit)) 
            if self.view.configurationlayout.processinglayout.shiftpeaklayout.polynomialpeakfittinglayout.method_selected[i] ==1:
                if self.inverse_axis[i] == 1:
                    pass # not this
                if self.inverse_axis[i] == 0:
                    centermass = self.inflection_function_x(intensities_fit)
                    cumulative_plot_shiftpeak.append((centermass, intensities_fit))                       
            
            cumulative_center[i] = center_fit
            cumulative_plot_fitting.append((wavelengths_ranged, intensities_fit))
            if self.status_inverse[i]:
                self.center_func_time[i] = cumulative_center[i]
            if not self.status_inverse[i]:
                self.center_func_time[i] = self.center_func_time[i]


        self.view.plottinglayout.spectrumlayout.num_polynomialpeakfitting = self.num_fitting
        self.view.plottinglayout.spectrumlayout.plot_polynomialpeakfitting(cumulative_plot_fitting, cumulative_plot_fitting)
                
        self.view.plottinglayout.spectrumlayout.num_polynomialshiftpeak = self.num_shiftpeak
        self.view.plottinglayout.spectrumlayout.plot_polynomialshiftpeak(self.inverse_axis, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)   
            
        self.view.plottinglayout.sensorgramlayout.num_polynomialshiftpeak = self.num_shiftpeak
        self.view.plottinglayout.sensorgramlayout.plot_polynomialshiftpeak(self.transform_selected, cumulative_plot_shiftpeak, cumulative_plot_shiftpeak)  

    def polynomialfit(self, degree, min_wavelength, max_wavelength, span, peak_guess):
        min_range = self.wavelengths >= min_wavelength
        max_range = self.wavelengths <= max_wavelength
        selected_wavelengths = self.wavelengths[min_range & max_range]
        selected_intensities = self.intensities[min_range & max_range]
        warnings.filterwarnings('ignore', category=OptimizeWarning)

        try:
            coeffs, center_fit = self.parallel_computation(selected_wavelengths, selected_intensities, degree, span, peak_guess)
            self.wavelengths_ranged = np.linspace(min_wavelength, max_wavelength, 100*len(selected_wavelengths))
            # self.wavelengths_ranged = np.linspace(min_wavelength, max_wavelength, 1000)
            self.intensities_fit = np.poly1d(coeffs)(self.wavelengths_ranged)
        except:
            self.wavelengths_ranged = [np.nan,np.nan]
            self.intensities_fit = [np.nan,np.nan]
            center_fit = np.nan
        return self.wavelengths_ranged, self.intensities_fit, center_fit
    
    
    def parallel_computation(self, selected_wavelengths, selected_intensities, degree, span, peak_guess):
        results = {}

        def calculate_polyfit():
            coeffs = np.polyfit(selected_wavelengths, selected_intensities, deg=degree)
  
            m = np.mean(selected_wavelengths)
            s = np.std(selected_wavelengths)
            # coeffs = np.polyfit((selected_wavelengths - m) / s, selected_intensities, degree)
            # P = np.polyfit((selected_wavelengths - m) / s, selected_intensities, degree)
            results['coeffs'] = coeffs


        # Fungsi untuk menghitung center mass polynomial peak fit
        def calculate_center_fit():
            center_fit, ier = self.centermass_polynomialpeakfit(degree, selected_wavelengths, selected_intensities, span, peak_guess)
            if center_fit > (peak_guess + span) or center_fit < (peak_guess - span): # soon to prevent error fsolve, 
                center_fit = np.nan
            if ier != 1:
                center_fit = np.nan
            results['center_fit'] = center_fit

        # Membuat dan memulai thread
        polyfit_thread = threading.Thread(target=calculate_polyfit)
        centerfit_thread = threading.Thread(target=calculate_center_fit)

        polyfit_thread.start()
        centerfit_thread.start()

        # Menunggu kedua thread selesai
        polyfit_thread.join()
        centerfit_thread.join()

        # Mengembalikan hasil dari kedua komputasi
        coeffs = results.get('coeffs')
        center_fit = results.get('center_fit')

        return coeffs, center_fit


    def centermass_polynomialpeakfit(self, degree, selected_wavelengths, selected_intensities, span, peak_guess):   
        m = np.mean(selected_wavelengths)
        s = np.std(selected_wavelengths)
        # left = peak_guess + span/2
        left = peak_guess - span/2

        P = np.polyfit((selected_wavelengths - m) / s, selected_intensities, degree)
        # P = np.polyfit(selected_wavelengths, selected_intensities, deg=degree)

        def equation(x):
            return np.polyval(P, (x - m) / s) - np.polyval(P, (x + span - m) / s)
        sol, infodict, ier, mesg = fsolve(equation, 
                                          left,  
                                        #   xtol=1e-15,
                                          xtol=1e-12,
                                          maxfev = 500, 
                                          full_output=True)
        '''
        The solution converged.
        '''

        left = sol[0]
        # if ier == 1:
        #     left = sol[0]
        #     '''
        #     ier = 1: The solution converged successfully.
        #     ier = 2: The function could not make progress.
        #     ier = 3: The solution does not converge within the given number of iterations.
        #     ier = 4: The iteration failed due to a numerical issue.
        #     '''
        # else:
        #     return np.nan
        
        base = np.polyval(P, (left - m) / s)

        C1 = 0
        C2 = 0
        for b in range(degree+1):
            C1 += P[b] / (degree+ 3 - b) * (((left + span - m) / s)**(degree+ 3 - b) - ((left - m) / s)**(degree+ 3 - b))
            C2 += P[b] / (degree+ 2 - b) * (((left + span - m) / s)**(degree+ 2 - b) - ((left - m) / s)**(degree+ 2 - b))
    
        C1 -= base / 2 * (((left + span - m) / s)**2 - ((left - m) / s)**2)
        C2 -= base * (((left + span - m) / s) - (left - m) / s)
        return (C1 / C2 * s + m), ier

    def inflection_function_x(self, intensities_fit):
        secondderivative = np.gradient(np.gradient(intensities_fit))
        infls = np.where(np.diff(np.sign(secondderivative)))[0]
        try:
            inflectionpoint = self.wavelengths_ranged[infls[0]]
        except:
            inflectionpoint = np.nan
            print('inflection point error')
        return inflectionpoint

    def inflection_function_y(self, intensities_fit):
        secondderivative = np.gradient(np.gradient(intensities_fit))
        infls = np.where(np.diff(np.sign(secondderivative)))[0]
        try:
            inflectionpoint = intensities_fit[infls[0]]
        except:
            print('inflection point error')
            inflectionpoint = np.nan
        return inflectionpoint
            