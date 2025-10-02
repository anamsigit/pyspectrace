
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from matplotlib.figure import Figure
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QSpinBox,
)

import numpy as np
import pyqtgraph as pg
import time

# class SpectrumLayout(QWidget): 
class SpectrumLayout(pg.PlotWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # self.plt = pg.plot()
        self.plt = self
        self.plt.setBackground('w')
        self.plt.showGrid(x=False, y=False)
        self.plt.addLegend()
        
        # self.plt.setLabel('left', 'Intensity')
        self.plt.setLabel('left', 'Intensity')
        self.plt.setLabel('bottom', 'λ (nm)')
        self.plt.scene().sigMouseMoved.connect(self.mouseMoved)

        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('b'))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('b'))
        self.label = pg.TextItem(text='', color='w',  angle=0, fill=pg.mkBrush((0, 0, 255, 150)), anchor=(1, 1))

        self.initspectrum = True

        self.intensities = []
        self.wavelengths = []

        self.num_gaussianpeakfitting = []
        self.num_gaussianshiftpeak = []

        self.num_lorentzianpeakfitting = []
        self.num_lorentzianshiftpeak = []

        self.num_polynomialfitting = []
        self.num_polynomialshift = []
        
        self.num_polynomialpeakfitting = []
        self.num_polynomialshiftpeak = []

        self.num_polypeakfitting = []
        self.num_polyshiftpeak = []
  
        self.num_lorentzianpeakwidthfitting = []
        self.num_lorentzianshiftpeakwidth = []

        self.num_gaussianpeakwidthfitting = []
        self.num_gaussianshiftpeakwidth = []

        self.num_polynomialpeakwidthfitting = []
        self.num_polynomialshiftpeakwidth = []
        
        self.name_valus = []
        self.num_spectrum = [None]

        self.color_gaussianshiftpeak = [None]
        self.color_gaussianpeakfitting = [None]

        self.color_lorentzianshiftpeak = [None]
        self.color_lorentzianpeakfitting = [None]

        self.color_polynomialshift = [None]
        self.color_polynomialfitting = [None]

        self.color_polynomialshiftpeak = [None]
        self.color_polynomialpeakfitting = [None]

        self.color_polyshiftpeak = [None]
        self.color_polypeakfitting = [None]

        self.color_lorentzianshiftpeakwidth = [None]
        self.color_lorentzianpeakwidthfitting = [None]

        self.color_gaussianshiftpeakwidth = [None]
        self.color_gaussianpeakwidthfitting = [None]

        self.color_polynomialshiftpeakwidth = [None]
        self.color_polynomialpeakwidthfitting = [None]

        self.name_polypeakfitting = []
        self.name_polynomialpeakfitting = []
        self.name_gaussianpeakfitting = []
        self.name_lorentzianpeakfitting = []
        self.name_polynomialfitting = []
        self.name_lorentzianpeakwidthfitting = []
        self.name_gaussianpeakwidthfitting = []
        self.name_polynomialpeakwidthfitting = []

        self.mousecoordinating = True

        self.invisible_plot = []

    def init_plot_args(self):
        total_plot = (
            len(self.num_spectrum) 
            +len(self.num_gaussianpeakfitting) 
            +len(self.num_gaussianshiftpeak) 

            +len(self.num_lorentzianpeakfitting) 
            +len(self.num_lorentzianshiftpeak) 

            +len(self.num_polynomialfitting) 
            +len(self.num_polynomialshift) 

            +len(self.num_polynomialpeakfitting) 
            +len(self.num_polynomialshiftpeak) 

            +len(self.num_polypeakfitting) 
            +len(self.num_polyshiftpeak) 

            +len(self.num_lorentzianpeakwidthfitting) 
            +len(self.num_lorentzianshiftpeakwidth) 

            +len(self.num_gaussianpeakwidthfitting) 
            +len(self.num_gaussianshiftpeakwidth) 

            +len(self.num_polynomialpeakwidthfitting) 
            +len(self.num_polynomialshiftpeakwidth) 
            )

        def bundle_kwargs(color, width, style, name):
            params_kwargs = {
                'pen': pg.mkPen(color=color, width=width, style=style),
                'name': name,
                # 'symbol': 'o'
            }
            return params_kwargs
        self.plt.clear()

        self.bundle_plot_list = [None] * (total_plot)          
        self.plot_args_list = [None] * (total_plot)          
        self.params_kwargs_list = [None] * (total_plot)          
        self.plot_list = [None] * (total_plot)          

        for i in range(total_plot):
            self.bundle_plot_list[i] = ([(np.array([]), np.array([])), 
                                    bundle_kwargs((0, 255, 0), 1, pg.QtCore.Qt.SolidLine,f"{i}")])
            
        index = 0

        for _ in range(len(self.num_spectrum)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs((255, 0, 0), 1, pg.QtCore.Qt.SolidLine, f"Spectrum")])
            index += 1




        for i in range(len(self.num_gaussianpeakfitting)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_gaussianpeakfitting[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_gaussianpeakfitting[i]} Gaussian Peak Fitting")])
            index += 1
        for i in range(len(self.num_gaussianshiftpeak)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_gaussianshiftpeak[i], 2, pg.QtCore.Qt.DashLine, f"{self.name_gaussianpeakfitting[i]} Gaussian Peak Shift")])
            index += 1





        for i in range(len(self.num_lorentzianpeakfitting)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_lorentzianshiftpeak[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_lorentzianpeakfitting[i]} Lorentzian Peak Shift")])
            index += 1
        for i in range(len(self.num_lorentzianshiftpeak)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_lorentzianpeakfitting[i], 2, pg.QtCore.Qt.DashLine, f"{self.name_lorentzianpeakfitting[i]} Lorentzian Peak Fitting")])
            index += 1





        for i in range(len(self.num_polynomialpeakfitting)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polynomialshiftpeak[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_polynomialpeakfitting[i]} Polynomial Peak Fitting")])
            index += 1
        for i in range(len(self.num_polynomialshiftpeak)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polynomialpeakfitting[i], 2, pg.QtCore.Qt.DashLine, f"{self.name_polynomialpeakfitting[i]} Polynomial Peak Shift")])
        



        for i in range(len(self.num_polypeakfitting)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polyshiftpeak[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_polypeakfitting[i]} Poly Peak Fitting")])
            index += 1
        for i in range(len(self.num_polyshiftpeak)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polypeakfitting[i], 2, pg.QtCore.Qt.DashLine, f"{self.name_polypeakfitting[i]} Poly Peak Shift")])
            index += 1




        for i in range(len(self.num_polynomialfitting)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polynomialshift[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_polynomialfitting[i]} Polynomial Shift")])
            index += 1
        for i in range(len(self.num_polynomialshift)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polynomialfitting[i], 2, pg.QtCore.Qt.DashLine, f"{self.name_polynomialfitting[i]} Polynomial Fitting")])
            index += 1




        for i in range(len(self.num_lorentzianpeakwidthfitting)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_lorentzianshiftpeakwidth[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_lorentzianpeakwidthfitting[i]} Lorentzian Peak Width Shift")])
            index += 1
        for i in range(len(self.num_lorentzianshiftpeakwidth)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_lorentzianpeakwidthfitting[i], 2, pg.QtCore.Qt.DashLine, f"{self.name_lorentzianpeakwidthfitting[i]} Lorentzian Peak Width Fitting")])
            index += 1



        for i in range(len(self.num_gaussianpeakwidthfitting)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_gaussianshiftpeakwidth[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_gaussianpeakwidthfitting[i]} Lorentzian Peak Width Shift")])
            index += 1
        for i in range(len(self.num_gaussianshiftpeakwidth)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_gaussianpeakwidthfitting[i], 2, pg.QtCore.Qt.DashLine, f"{self.name_gaussianpeakwidthfitting[i]} Lorentzian Peak Width Fitting")])
            index += 1


        for i in range(len(self.num_polynomialpeakwidthfitting)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polynomialshiftpeakwidth[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_polynomialpeakwidthfitting[i]} Polynomial Peak Width Shift")])
            index += 1
        for i in range(len(self.num_polynomialshiftpeakwidth)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polynomialpeakwidthfitting[i], 2, pg.QtCore.Qt.DashLine, f"{self.name_polynomialpeakwidthfitting[i]} Polynomial Peak Width Fitting")])
            index += 1



        if len(self.invisible_plot) < (total_plot):
            self.invisible_plot.append(True)
            self.invisible_plot.append(True) # karena sekali plotting akan ada curve fiting dan track
            self.invisible_plot.append(True) # karena sekali plotting akan ada curve fiting dan track
            self.invisible_plot.append(True) # karena sekali plotting akan ada curve fiting dan track
            self.invisible_plot.append(True) # karena sekali plotting akan ada curve fiting dan track
            self.invisible_plot.append(True) # karena sekali plotting akan ada curve fiting dan track
        if len(self.invisible_plot) > (total_plot):
            self.invisible_plot.pop()

        
            
        for i in range(total_plot):
            self.plot_args_list[i] = (self.bundle_plot_list[i][0])
            self.params_kwargs_list[i] = (self.bundle_plot_list[i][1])
        for i in range(total_plot):
            self.plot_list[i] = (self.plt.plot(*self.plot_args_list[i], **self.params_kwargs_list[i]))
            # self.plot_list[i].setVisible(self.invisible_plot[i])

    def plot_spectrum(self, wavelengths, intensities):
        self.intensities = []
        self.wavelengths = []
        for i in range(len(self.num_spectrum)):
            self.wavelengths.append(wavelengths[i][0])
            self.intensities.append(intensities[i][1])

    def plot_gaussianshiftpeak(self, inverse_axis, wavelengths_gaussianshiftpeak, intensities_gaussianshiftpeak):
        self.intensities_gaussianshiftpeak = []
        self.wavelengths_gaussianshiftpeak = []
        for i in range(len(self.num_gaussianshiftpeak)):
            if inverse_axis[i] == 1:
                self.wavelengths_gaussianshiftpeak.append([min(wavelengths_gaussianshiftpeak[i][1]), max(wavelengths_gaussianshiftpeak[i][1])])
                self.intensities_gaussianshiftpeak.append([intensities_gaussianshiftpeak[i][0], intensities_gaussianshiftpeak[i][0]])
            if inverse_axis[i] == 0:
                self.intensities_gaussianshiftpeak.append([min(wavelengths_gaussianshiftpeak[i][1]), max(wavelengths_gaussianshiftpeak[i][1])])
                self.wavelengths_gaussianshiftpeak.append([intensities_gaussianshiftpeak[i][0], intensities_gaussianshiftpeak[i][0]])

    def plot_gaussianpeakfitting(self, wavelengths_gaussianpeakfitting, intensities_gaussianpeakfitting):
        self.intensities_gaussianpeakfitting = []
        self.wavelengths_gaussianpeakfitting = []
        for i in range(len(self.num_gaussianpeakfitting)):
            self.wavelengths_gaussianpeakfitting.append(wavelengths_gaussianpeakfitting[i][0])
            self.intensities_gaussianpeakfitting.append(intensities_gaussianpeakfitting[i][1])

    def plot_lorentzianshiftpeak(self, inverse_axis, wavelengths_lorentzianshiftpeak, intensities_lorentzianshiftpeak):
        self.intensities_lorentzianshiftpeak = []
        self.wavelengths_lorentzianshiftpeak = []
        for i in range(len(self.num_lorentzianshiftpeak)):
            if inverse_axis[i] == 1:
                self.wavelengths_lorentzianshiftpeak.append([min(wavelengths_lorentzianshiftpeak[i][1]), max(wavelengths_lorentzianshiftpeak[i][1])])
                self.intensities_lorentzianshiftpeak.append([intensities_lorentzianshiftpeak[i][0], intensities_lorentzianshiftpeak[i][0]])
            if inverse_axis[i] == 0:
                self.intensities_lorentzianshiftpeak.append([min(wavelengths_lorentzianshiftpeak[i][1]), max(wavelengths_lorentzianshiftpeak[i][1])])
                self.wavelengths_lorentzianshiftpeak.append([intensities_lorentzianshiftpeak[i][0], intensities_lorentzianshiftpeak[i][0]])

    def plot_lorentzianpeakfitting(self, wavelengths_lorentzianpeakfitting, intensities_lorentzianpeakfitting):
        self.intensities_lorentzianpeakfitting = []
        self.wavelengths_lorentzianpeakfitting = []
        for i in range(len(self.num_lorentzianpeakfitting)):
            self.wavelengths_lorentzianpeakfitting.append(wavelengths_lorentzianpeakfitting[i][0])
            self.intensities_lorentzianpeakfitting.append(intensities_lorentzianpeakfitting[i][1])

    def plot_polynomialshift(self, inverse_axis, wavelengths_polynomialshift, intensities_polynomialshift):
        self.intensities_polynomialshift = []
        self.wavelengths_polynomialshift = []
        for i in range(len(self.num_polynomialshift)):
            self.wavelengths_polynomialshift.append([min(wavelengths_polynomialshift[i][1]), max(wavelengths_polynomialshift[i][1])])
            self.intensities_polynomialshift.append([intensities_polynomialshift[i][0], intensities_polynomialshift[i][0]])

    def plot_polynomialfitting(self, wavelengths_polynomialfitting, intensities_polynomialfitting):
        self.intensities_polynomialfitting = []
        self.wavelengths_polynomialfitting = []
        for i in range(len(self.num_polynomialfitting)):
            self.wavelengths_polynomialfitting.append(wavelengths_polynomialfitting[i][0])
            self.intensities_polynomialfitting.append(intensities_polynomialfitting[i][1])

    def plot_polynomialshiftpeak(self, inverse_axis, wavelengths_polynomialshiftpeak, intensities_polynomialshiftpeak):
        self.intensities_polynomialshiftpeak = []
        self.wavelengths_polynomialshiftpeak = []
        for i in range(len(self.num_polynomialshiftpeak)):
            if inverse_axis[i] == 1:
                self.wavelengths_polynomialshiftpeak.append([min(wavelengths_polynomialshiftpeak[i][1]), max(wavelengths_polynomialshiftpeak[i][1])])
                self.intensities_polynomialshiftpeak.append([intensities_polynomialshiftpeak[i][0], intensities_polynomialshiftpeak[i][0]])
            if inverse_axis[i] == 0:
                self.intensities_polynomialshiftpeak.append([min(wavelengths_polynomialshiftpeak[i][1]), max(wavelengths_polynomialshiftpeak[i][1])])
                self.wavelengths_polynomialshiftpeak.append([intensities_polynomialshiftpeak[i][0], intensities_polynomialshiftpeak[i][0]])

    def plot_polynomialpeakfitting(self, wavelengths_polynomialpeakfitting, intensities_polynomialpeakfitting):
        self.intensities_polynomialpeakfitting = []
        self.wavelengths_polynomialpeakfitting = []
        for i in range(len(self.num_polynomialpeakfitting)):
            self.wavelengths_polynomialpeakfitting.append(wavelengths_polynomialpeakfitting[i][0])
            self.intensities_polynomialpeakfitting.append(intensities_polynomialpeakfitting[i][1])

    def plot_polyshiftpeak(self, inverse_axis, wavelengths_polyshiftpeak, intensities_polyshiftpeak):
        self.intensities_polyshiftpeak = []
        self.wavelengths_polyshiftpeak = []
        for i in range(len(self.num_polyshiftpeak)):
            if inverse_axis[i] == 1:
                self.wavelengths_polyshiftpeak.append([min(wavelengths_polyshiftpeak[i][1]), max(wavelengths_polyshiftpeak[i][1])])
                self.intensities_polyshiftpeak.append([intensities_polyshiftpeak[i][0], intensities_polyshiftpeak[i][0]])
            if inverse_axis[i] == 0:
                self.intensities_polyshiftpeak.append([min(wavelengths_polyshiftpeak[i][1]), max(wavelengths_polyshiftpeak[i][1])])
                self.wavelengths_polyshiftpeak.append([intensities_polyshiftpeak[i][0], intensities_polyshiftpeak[i][0]])


    def plot_polypeakfitting(self, wavelengths_polypeakfitting, intensities_polypeakfitting):
        self.intensities_polypeakfitting = []
        self.wavelengths_polypeakfitting = []
        for i in range(len(self.num_polypeakfitting)):
            self.wavelengths_polypeakfitting.append(wavelengths_polypeakfitting[i][0])
            self.intensities_polypeakfitting.append(intensities_polypeakfitting[i][1])

    def plot_lorentzianshiftpeakwidth(self, inverse_axis, wavelengths_lorentzianshiftpeakwidth, intensities_lorentzianshiftpeakwidth):
        self.intensities_lorentzianshiftpeakwidth = []
        self.wavelengths_lorentzianshiftpeakwidth = []
        for i in range(len(self.num_lorentzianshiftpeakwidth)):
            if inverse_axis[i] == 1:
                self.wavelengths_lorentzianshiftpeakwidth.append([min(wavelengths_lorentzianshiftpeakwidth[i][1]), max(wavelengths_lorentzianshiftpeakwidth[i][1])])
                self.intensities_lorentzianshiftpeakwidth.append([intensities_lorentzianshiftpeakwidth[i][0], intensities_lorentzianshiftpeakwidth[i][0]])
            if inverse_axis[i] == 0:
                self.intensities_lorentzianshiftpeakwidth.append([min(wavelengths_lorentzianshiftpeakwidth[i][1]), max(wavelengths_lorentzianshiftpeakwidth[i][1])])
                self.wavelengths_lorentzianshiftpeakwidth.append([intensities_lorentzianshiftpeakwidth[i][0], intensities_lorentzianshiftpeakwidth[i][0]])

    def plot_lorentzianpeakwidthfitting(self, wavelengths_lorentzianpeakwidthfitting, intensities_lorentzianpeakwidthfitting):
        self.intensities_lorentzianpeakwidthfitting = []
        self.wavelengths_lorentzianpeakwidthfitting = []
        for i in range(len(self.num_lorentzianpeakwidthfitting)):
            self.wavelengths_lorentzianpeakwidthfitting.append(wavelengths_lorentzianpeakwidthfitting[i][0])
            self.intensities_lorentzianpeakwidthfitting.append(intensities_lorentzianpeakwidthfitting[i][1])


    def plot_gaussianshiftpeakwidth(self, inverse_axis, wavelengths_gaussianshiftpeakwidth, intensities_gaussianshiftpeakwidth):
        self.intensities_gaussianshiftpeakwidth = []
        self.wavelengths_gaussianshiftpeakwidth = []
        for i in range(len(self.num_gaussianshiftpeakwidth)):
            if inverse_axis[i] == 1:
                self.wavelengths_gaussianshiftpeakwidth.append([min(wavelengths_gaussianshiftpeakwidth[i][1]), max(wavelengths_gaussianshiftpeakwidth[i][1])])
                self.intensities_gaussianshiftpeakwidth.append([intensities_gaussianshiftpeakwidth[i][0], intensities_gaussianshiftpeakwidth[i][0]])
            if inverse_axis[i] == 0:
                self.intensities_gaussianshiftpeakwidth.append([min(wavelengths_gaussianshiftpeakwidth[i][1]), max(wavelengths_gaussianshiftpeakwidth[i][1])])
                self.wavelengths_gaussianshiftpeakwidth.append([intensities_gaussianshiftpeakwidth[i][0], intensities_gaussianshiftpeakwidth[i][0]])

    def plot_gaussianpeakwidthfitting(self, wavelengths_gaussianpeakwidthfitting, intensities_gaussianpeakwidthfitting):
        self.intensities_gaussianpeakwidthfitting = []
        self.wavelengths_gaussianpeakwidthfitting = []
        for i in range(len(self.num_gaussianpeakwidthfitting)):
            self.wavelengths_gaussianpeakwidthfitting.append(wavelengths_gaussianpeakwidthfitting[i][0])
            self.intensities_gaussianpeakwidthfitting.append(intensities_gaussianpeakwidthfitting[i][1])


    def plot_polynomialshiftpeakwidth(self, inverse_axis, wavelengths_polynomialshiftpeakwidth, intensities_polynomialshiftpeakwidth):
        self.intensities_polynomialshiftpeakwidth = []
        self.wavelengths_polynomialshiftpeakwidth = []
        for i in range(len(self.num_polynomialshiftpeakwidth)):
            if inverse_axis[i] == 1:
                self.wavelengths_polynomialshiftpeakwidth.append([min(wavelengths_polynomialshiftpeakwidth[i][1]), max(wavelengths_polynomialshiftpeakwidth[i][1])])
                self.intensities_polynomialshiftpeakwidth.append([intensities_polynomialshiftpeakwidth[i][0], intensities_polynomialshiftpeakwidth[i][0]])
            if inverse_axis[i] == 0:
                self.intensities_polynomialshiftpeakwidth.append([min(wavelengths_polynomialshiftpeakwidth[i][1]), max(wavelengths_polynomialshiftpeakwidth[i][1])])
                self.wavelengths_polynomialshiftpeakwidth.append([intensities_polynomialshiftpeakwidth[i][0], intensities_polynomialshiftpeakwidth[i][0]])

    def plot_polynomialpeakwidthfitting(self, wavelengths_polynomialpeakwidthfitting, intensities_polynomialpeakwidthfitting):
        self.intensities_polynomialpeakwidthfitting = []
        self.wavelengths_polynomialpeakwidthfitting = []
        for i in range(len(self.num_polynomialpeakwidthfitting)):
            self.wavelengths_polynomialpeakwidthfitting.append(wavelengths_polynomialpeakwidthfitting[i][0])
            self.intensities_polynomialpeakwidthfitting.append(intensities_polynomialpeakwidthfitting[i][1])

    def update_plot_args(self):
        update_plot_args_spectrum = [None] * len(self.num_spectrum)

        update_plot_args_gaussianpeakfitting = [None] * len(self.num_gaussianpeakfitting)
        update_plot_args_gaussianshiftpeak = [None] * len(self.num_gaussianshiftpeak)

        update_plot_args_lorentzianpeakfitting = [None] * len(self.num_lorentzianpeakfitting)
        update_plot_args_lorentzianshiftpeak = [None] * len(self.num_lorentzianshiftpeak)

        update_plot_args_polynomialfitting = [None] * len(self.num_polynomialfitting)
        update_plot_args_polynomialshift = [None] * len(self.num_polynomialshift)

        update_plot_args_polynomialpeakfitting = [None] * len(self.num_polynomialpeakfitting)
        update_plot_args_polynomialshiftpeak = [None] * len(self.num_polynomialshiftpeak)

        update_plot_args_polypeakfitting = [None] * len(self.num_polypeakfitting)
        update_plot_args_polyshiftpeak = [None] * len(self.num_polyshiftpeak)

        update_plot_args_lorentzianpeakwidthfitting = [None] * len(self.num_lorentzianpeakwidthfitting)
        update_plot_args_lorentzianshiftpeakwidth = [None] * len(self.num_lorentzianshiftpeakwidth)

        update_plot_args_gaussianpeakwidthfitting = [None] * len(self.num_gaussianpeakwidthfitting)
        update_plot_args_gaussianshiftpeakwidth = [None] * len(self.num_gaussianshiftpeakwidth)

        update_plot_args_polynomialpeakwidthfitting = [None] * len(self.num_polynomialpeakwidthfitting)
        update_plot_args_polynomialshiftpeakwidth = [None] * len(self.num_polynomialshiftpeakwidth)

        for i in range(len(self.num_spectrum)):
            update_plot_args_spectrum[i] = (self.wavelengths[i], self.intensities[i])  

        for i in range(len(self.num_gaussianpeakfitting)):
            update_plot_args_gaussianpeakfitting[i] = (self.wavelengths_gaussianpeakfitting[i], self.intensities_gaussianpeakfitting[i])
        for i in range(len(self.num_gaussianshiftpeak)):
            update_plot_args_gaussianshiftpeak[i] = (self.wavelengths_gaussianshiftpeak[i], self.intensities_gaussianshiftpeak[i])

        for i in range(len(self.num_lorentzianpeakfitting)):
            update_plot_args_lorentzianpeakfitting[i] = (self.wavelengths_lorentzianpeakfitting[i], self.intensities_lorentzianpeakfitting[i])
        for i in range(len(self.num_lorentzianshiftpeak)):
            update_plot_args_lorentzianshiftpeak[i] = (self.wavelengths_lorentzianshiftpeak[i], self.intensities_lorentzianshiftpeak[i])

        for i in range(len(self.num_polynomialfitting)):
            update_plot_args_polynomialfitting[i] = (self.wavelengths_polynomialfitting[i], self.intensities_polynomialfitting[i])
        for i in range(len(self.num_polynomialshift)):
            update_plot_args_polynomialshift[i] = (self.wavelengths_polynomialshift[i], self.intensities_polynomialshift[i])

        for i in range(len(self.num_polynomialpeakfitting)):
            update_plot_args_polynomialpeakfitting[i] = (self.wavelengths_polynomialpeakfitting[i], self.intensities_polynomialpeakfitting[i])
        for i in range(len(self.num_polynomialshiftpeak)):
            update_plot_args_polynomialshiftpeak[i] = (self.wavelengths_polynomialshiftpeak[i], self.intensities_polynomialshiftpeak[i])

        for i in range(len(self.num_polypeakfitting)):
            update_plot_args_polypeakfitting[i] = (self.wavelengths_polypeakfitting[i], self.intensities_polypeakfitting[i])
        for i in range(len(self.num_polyshiftpeak)):
            update_plot_args_polyshiftpeak[i] = (self.wavelengths_polyshiftpeak[i], self.intensities_polyshiftpeak[i])

        for i in range(len(self.num_lorentzianpeakwidthfitting)):
            update_plot_args_lorentzianpeakwidthfitting[i] = (self.wavelengths_lorentzianpeakwidthfitting[i], self.intensities_lorentzianpeakwidthfitting[i])
        for i in range(len(self.num_lorentzianshiftpeakwidth)):
            update_plot_args_lorentzianshiftpeakwidth[i] = (self.wavelengths_lorentzianshiftpeakwidth[i], self.intensities_lorentzianshiftpeakwidth[i])

        for i in range(len(self.num_gaussianpeakwidthfitting)):
            update_plot_args_gaussianpeakwidthfitting[i] = (self.wavelengths_gaussianpeakwidthfitting[i], self.intensities_gaussianpeakwidthfitting[i])
        for i in range(len(self.num_gaussianshiftpeakwidth)):
            update_plot_args_gaussianshiftpeakwidth[i] = (self.wavelengths_gaussianshiftpeakwidth[i], self.intensities_gaussianshiftpeakwidth[i])
        
        for i in range(len(self.num_polynomialpeakwidthfitting)):
            update_plot_args_polynomialpeakwidthfitting[i] = (self.wavelengths_polynomialpeakwidthfitting[i], self.intensities_polynomialpeakwidthfitting[i])
        for i in range(len(self.num_polynomialshiftpeakwidth)):
            update_plot_args_polynomialshiftpeakwidth[i] = (self.wavelengths_polynomialshiftpeakwidth[i], self.intensities_polynomialshiftpeakwidth[i])

        self.update_plot_args_list =    (
                                        update_plot_args_spectrum

                                       +update_plot_args_gaussianpeakfitting 
                                       +update_plot_args_gaussianshiftpeak 

                                       +update_plot_args_lorentzianpeakfitting 
                                       +update_plot_args_lorentzianshiftpeak 

                                       +update_plot_args_polynomialfitting 
                                       +update_plot_args_polynomialshift 

                                       +update_plot_args_polynomialpeakfitting 
                                       +update_plot_args_polynomialshiftpeak 

                                       +update_plot_args_polypeakfitting 
                                       +update_plot_args_polyshiftpeak 

                                       +update_plot_args_lorentzianpeakwidthfitting 
                                       +update_plot_args_lorentzianshiftpeakwidth

                                       +update_plot_args_gaussianpeakwidthfitting 
                                       +update_plot_args_gaussianshiftpeakwidth

                                       +update_plot_args_polynomialpeakwidthfitting 
                                       +update_plot_args_polynomialshiftpeakwidth
                                        )

    def plot_uniform(self):
        if self.initspectrum == True:
            self.init_plot_args()
            self.initspectrum = False
        self.update_plot_args()   

        for i in range(
            len(self.num_spectrum) 

            +len(self.num_gaussianpeakfitting) 
            +len(self.num_gaussianshiftpeak) 

            +len(self.num_lorentzianpeakfitting) 
            +len(self.num_lorentzianshiftpeak) 

            +len(self.num_polynomialfitting) 
            +len(self.num_polynomialshift) 

            +len(self.num_polynomialpeakfitting) 
            +len(self.num_polynomialshiftpeak) 

            +len(self.num_polypeakfitting) 
            +len(self.num_polyshiftpeak) 

            +len(self.num_lorentzianpeakwidthfitting) 
            +len(self.num_lorentzianshiftpeakwidth) 

            +len(self.num_gaussianpeakwidthfitting) 
            +len(self.num_gaussianshiftpeakwidth) 

            +len(self.num_polynomialpeakwidthfitting) 
            +len(self.num_polynomialshiftpeakwidth) 
            ):

            self.plot_list[i].setData(*self.update_plot_args_list[i])

    def mouseMoved(self, pos):
        if self.plt.sceneBoundingRect().contains(pos):
            mousePoint = self.plt.getViewBox().mapSceneToView(pos)
            
            self.mousePointx = mousePoint.x()
            self.mousePointy = mousePoint.y()

            self.plt.removeItem(self.vLine)
            self.plt.removeItem(self.hLine)
            self.plt.removeItem(self.label)
            self.plt.addItem(self.vLine, ignoreBounds=True)
            self.plt.addItem(self.hLine, ignoreBounds=True)
            self.plt.addItem(self.label, ignoreBounds=True)

            # Set positions of the lines and the label
            self.vLine.setPos(self.mousePointx)
            self.hLine.setPos(self.mousePointy)
            self.label.setText(f"({self.mousePointx:.2f}, {self.mousePointy:.2f})")
            self.label.setPos(self.mousePointx, self.mousePointy)

    def autoscale_x(self):
        x_list = []

        for i in range(
                    len(self.num_gaussianshiftpeak) +
                    len(self.num_lorentzianshiftpeak) +
                    len(self.num_polynomialshiftpeak) +
                    len(self.num_polyshiftpeak) +
                    len(self.num_polynomialshift) +
                    len(self.num_lorentzianshiftpeakwidth) +
                    len(self.num_gaussianshiftpeakwidth) +
                    len(self.num_polynomialshiftpeakwidth) 
                    ):
            data_x, _ = self.plot_list[i+1].getData()

            if data_x is not None:
                x_list.append(data_x)

        all_x = np.concatenate(x_list)

        x_min = np.min(all_x)
        x_max = np.max(all_x)

        self.plot_list[0].getViewBox().setRange(
            xRange=(x_min, x_max),
            padding=0.1
        )

    def autoscale_y(self):
        y_list = []

        for i in range(
                    len(self.num_gaussianshiftpeak) +
                    len(self.num_lorentzianshiftpeak) +
                    len(self.num_polynomialshiftpeak) +
                    len(self.num_polyshiftpeak) +
                    len(self.num_polynomialshift) +
                    len(self.num_lorentzianshiftpeakwidth) +
                    len(self.num_gaussianshiftpeakwidth) +
                    len(self.num_polynomialshiftpeakwidth)
                    ):
            _, data_y = self.plot_list[i+1].getData() # saya tambah satu agar spectrum plot tidak terinclude

            if data_y is not None:
                y_list.append(data_y)

        all_y = np.concatenate(y_list)

        y_min = np.min(all_y)
        y_max = np.max(all_y)

        self.plot_list[0].getViewBox().setRange(
            yRange=(y_min, y_max),
            padding=0.1
        )