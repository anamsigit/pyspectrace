
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from matplotlib.figure import Figure
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QSpinBox, QMenu, QFileDialog
)

import numpy as np
import pyqtgraph as pg

class SensorgramLayout(pg.GraphicsLayoutWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setBackground('w')
        self.plt = pg.PlotItem()
        self.addItem(self.plt)
        
        self.plt.showGrid(x=False, y=True)
        self.plt.addLegend()
        self.plt.setLabel('left', 'λ (nm)')
        self.plt.setLabel('bottom', 'frame', color = 'red')

        self.initspectrum = True

        self.num_gaussianshiftpeak = []
        self.num_lorentzianshiftpeak = []
        self.num_polynomialshiftpeak = []
        self.num_polyshiftpeak = []
        self.num_polynomialshift = []
        self.num_lorentzianshiftpeakwidth = []
        self.num_gaussianshiftpeakwidth = []
        self.num_polynomialshiftpeakwidth = []

        self.frame_list_gaussianshiftpeak = []
        self.frame_list_lorentzianshiftpeak = []
        self.frame_list_polynomialshiftpeak = []
        self.frame_list_polyshiftpeak = []
        self.frame_list_polynomialshift = []
        self.frame_list_lorentzianshiftpeakwidth = []
        self.frame_list_gaussianshiftpeakwidth = []
        self.frame_list_polynomialshiftpeakwidth = []

        self.gaussianshiftpeak_list = []
        self.lorentzianshiftpeak_list = []
        self.polynomialshiftpeak_list = []
        self.polyshiftpeak_list = []
        self.polynomialshift_list = []
        self.lorentzianshiftpeakwidth_list = []
        self.gaussianshiftpeakwidth_list = []
        self.polynomialshiftpeakwidth_list = []

        self.color_gaussianshiftpeak = []
        self.color_lorentzianshiftpeak = []
        self.color_polynomialshiftpeak = []
        self.color_polyshiftpeak = []
        self.color_polynomialshift = []
        self.color_lorentzianshiftpeakwidth = []
        self.color_gaussianshiftpeakwidth = []
        self.color_polynomialshiftpeakwidth = []

        self.name_polynomialpeakfitting = []
        self.name_polypeakfitting = []
        self.name_gaussianpeakfitting = []
        self.name_lorentzianpeakfitting = []
        self.name_polynomialfitting = []
        self.name_lorentzianpeakwidthfitting = []
        self.name_gaussianpeakwidthfitting = []
        self.name_polynomialpeakwidthfitting = []

        self.frame = 0
        self.time = 250
        self.time_unit = 1 # 1 second

        self.invisible_plot = []

        self.transform_func = lambda x: x

        pw = self
        self.l = pg.GraphicsLayout()
        pw.setCentralWidget(self.l)

        self.pI = pg.PlotItem()
        self.pI.hideAxis('left')
        self.pI.setLabel('bottom', 'Time (s)')
        
        self.mainplot = self.pI.vb

        self.l.addItem(self.pI, col = 10000)

    def init_plot_args(self):   
        total_plot_init = (
            len(self.num_gaussianshiftpeak) 
            +len(self.num_lorentzianshiftpeak)
            +len(self.num_polynomialshiftpeak)
            +len(self.num_polyshiftpeak)
            +len(self.num_polynomialshift)
            +len(self.num_lorentzianshiftpeakwidth)
            +len(self.num_gaussianshiftpeakwidth)
            +len(self.num_polynomialshiftpeakwidth)
                    )
        
        def bundle_kwargs(color, width, style, name):
            params_kwargs = {
                'pen': pg.mkPen(color=color, width=width, style=style),
                'name': name,
                # 'symbol':"o",
                # 'symbolSize': 5,
                # 'symbolBrush': "b",
            }
            return params_kwargs
        self.plt.clear()

        self.bundle_plot_list = [None] * (total_plot_init)
        self.plot_args_list = [None] *  (total_plot_init)     
        self.params_kwargs_list = [None] *  (total_plot_init)          
        self.plot_list = [None] *  (total_plot_init)

        for i in range (total_plot_init):
            self.bundle_plot_list[i] = ([(np.array([]), np.array([])), 
                                    bundle_kwargs((0, 255, 0), 1, pg.QtCore.Qt.DashDotLine,f"{i}")])
            
        index = 0
        for i in range(len(self.num_gaussianshiftpeak)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_gaussianshiftpeak[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_gaussianpeakfitting[i]} (Gaussian)")])
                                            # bundle_kwargs(self.color_gaussianshiftpeak[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_gaussianpeakfitting[i]} Gaussian Peak Shift")])
            index += 1

        for i in range(len(self.num_lorentzianshiftpeak)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_lorentzianshiftpeak[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_lorentzianpeakfitting[i]} (Lorentzian)")])
            index += 1

        for i in range(len(self.num_polynomialshiftpeak)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polynomialshiftpeak[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_polynomialpeakfitting[i]} (Center mass)")])
            index += 1

        for i in range(len(self.num_polyshiftpeak)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polyshiftpeak[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_polypeakfitting[i]} (Polynomial)")])
            index += 1

        for i in range(len(self.num_polynomialshift)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polynomialshift[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_polynomialfitting[i]} (Fixed λ)")])
            index += 1

        for i in range(len(self.num_lorentzianshiftpeakwidth)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_lorentzianshiftpeakwidth[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_lorentzianpeakwidthfitting[i]} (Lorentzian)")])
            index += 1

        for i in range(len(self.num_gaussianshiftpeakwidth)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_gaussianshiftpeakwidth[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_gaussianpeakwidthfitting[i]} (Gaussian)")])
            index += 1

        for i in range(len(self.num_polynomialshiftpeakwidth)):
            self.bundle_plot_list[index] = ([(np.array([]), np.array([])), 
                                            bundle_kwargs(self.color_polynomialshiftpeakwidth[i], 2, pg.QtCore.Qt.SolidLine, f"{self.name_polynomialpeakwidthfitting[i]} (Gaussian)")])
            index += 1

        if len(self.invisible_plot) < (total_plot_init):
            self.invisible_plot.append(True)
            self.invisible_plot.append(True) # karena sekali plotting akan ada curve fiting dan track
            self.invisible_plot.append(True) # karena sekali plotting akan ada curve fiting dan track
            self.invisible_plot.append(True) # karena sekali plotting akan ada curve fiting dan track
            self.invisible_plot.append(True) # karena sekali plotting akan ada curve fiting dan track
        if len(self.invisible_plot) > (total_plot_init):
            self.invisible_plot.pop()
        
        
        for i in range(total_plot_init):
            self.plot_args_list[i] = (self.bundle_plot_list[i][0])
            self.params_kwargs_list[i] = (self.bundle_plot_list[i][1])

        self.axis = [None] * (total_plot_init)
        self.subplot = [None] * (total_plot_init)
        for i in range(total_plot_init):
            self.axis[i] = pg.AxisItem("left")
            self.subplot[i] = pg.ViewBox()


        try:
        
            if not hasattr(self, "item_registry"):
                self.item_registry = {"axis": [], "subplot": [], "curve": []}

            for axis in self.item_registry["axis"]:
                self.l.removeItem(axis)  # Hapus axis dari layout

            for subplot in self.item_registry["subplot"]:
                self.l.scene().removeItem(subplot)  # Hapus subplot dari scene

            for curve in self.item_registry["curve"]:
                subplot_idx = self.item_registry["curve"].index(curve)
                self.subplot[subplot_idx].removeItem(curve)  # Hapus curve dari subplot
        except:
            pass

            # Kosongkan registry setelah penghapusan
        self.item_registry = {"axis": [], "subplot": [], "curve": []}


        # Inisialisasi item baru
        self.init_PlotCurveItem = [None] * total_plot_init
        for i in range(total_plot_init):
            self.init_PlotCurveItem[i] = pg.PlotCurveItem(*self.plot_args_list[i], **self.params_kwargs_list[i])
        
        # Tambahkan item baru dan simpan referensi ke registry
        for i in range(total_plot_init):
            self.l.addItem(self.axis[i], col=i)
            self.item_registry["axis"].append(self.axis[i])  # Simpan referensi axis

            self.l.scene().addItem(self.subplot[i])
            self.item_registry["subplot"].append(self.subplot[i])  # Simpan referensi subplot

            self.subplot[i].addItem(self.init_PlotCurveItem[i])
            self.item_registry["curve"].append(self.init_PlotCurveItem[i])  # Simpan referensi curve
          

        for i in range(total_plot_init):
            pen = self.params_kwargs_list[i]['pen']
            color = pen.color()

            self.axis[i].setLabel(self.params_kwargs_list[i]['name'], color=color.name())
            # self.axis[i].setLabel(self.params_kwargs_list[i])
            self.axis[i].linkToView(self.subplot[i])
            self.subplot[i].setXLink(self.mainplot)
            def updateViews():
                try:
                    self.subplot[i].setGeometry(self.mainplot.sceneBoundingRect())
                except:
                    pass
            self.mainplot.sigResized.connect(updateViews)
            # self.subplot[i].enableAutoRange(axis= pg.ViewBox.XYAxes, enable=True)

    def plot_gaussianshiftpeak(self, transform_selected, wavelengths_gaussianshiftpeak, intensities_gaussianshiftpeak):
        self.wavelengths_gaussianshiftpeak = []
        for i in range(len(self.num_gaussianshiftpeak)):
            self.wavelengths_gaussianshiftpeak.append([self.transform_calc(transform_selected[i], intensities_gaussianshiftpeak[i][0])])

    def plot_lorentzianshiftpeak(self, transform_selected, wavelengths_lorentzianshiftpeak, intensities_lorentzianshiftpeak):
        self.wavelengths_lorentzianshiftpeak = []
        for i in range(len(self.num_lorentzianshiftpeak)):
            self.wavelengths_lorentzianshiftpeak.append([self.transform_calc(transform_selected[i], intensities_lorentzianshiftpeak[i][0])])

    def plot_polynomialshiftpeak(self, transform_selected, wavelengths_polynomialshiftpeak, intensities_polynomialshiftpeak):
        self.wavelengths_polynomialshiftpeak = []
        for i in range(len(self.num_polynomialshiftpeak)):
            self.wavelengths_polynomialshiftpeak.append([self.transform_calc(transform_selected[i], intensities_polynomialshiftpeak[i][0])])
    
    def plot_polyshiftpeak(self, transform_selected, wavelengths_polyshiftpeak, intensities_polyshiftpeak):
        self.wavelengths_polyshiftpeak = []
        for i in range(len(self.num_polyshiftpeak)):
            self.wavelengths_polyshiftpeak.append([self.transform_calc(transform_selected[i], intensities_polyshiftpeak[i][0])])
   
    def plot_polynomialshift(self, transform_selected, wavelengths_polynomialshift, intensities_polynomialshift):
        self.wavelengths_polynomialshift = []
        for i in range(len(self.num_polynomialshift)):
            self.wavelengths_polynomialshift.append([self.transform_calc(transform_selected[i], intensities_polynomialshift[i][0])])

    def plot_lorentzianshiftpeakwidth(self, transform_selected, wavelengths_lorentzianshiftpeakwidth, intensities_lorentzianshiftpeakwidth):
        self.wavelengths_lorentzianshiftpeakwidth = []
        for i in range(len(self.num_lorentzianshiftpeakwidth)):
            self.wavelengths_lorentzianshiftpeakwidth.append([self.transform_calc(transform_selected[i], intensities_lorentzianshiftpeakwidth[i][0])])
    
    def plot_gaussianshiftpeakwidth(self, transform_selected, wavelengths_gaussianshiftpeakwidth, intensities_gaussianshiftpeakwidth):
    # def plot_gaussianshiftpeakwidth(self, transform_selected, wavelengths_lorentzianshiftpeakwidth, intensities_gaussianshiftpeakwidth):
        self.wavelengths_gaussianshiftpeakwidth = []
        for i in range(len(self.num_gaussianshiftpeakwidth)):
            self.wavelengths_gaussianshiftpeakwidth.append([self.transform_calc(transform_selected[i], intensities_gaussianshiftpeakwidth[i][0])])

    def plot_polynomialshiftpeakwidth(self, transform_selected, wavelengths_polynomialshiftpeakwidth, intensities_polynomialshiftpeakwidth):
    # def plot_polynomialshiftpeakwidth(self, transform_selected, wavelengths_lorentzianshiftpeakwidth, intensities_polynomialshiftpeakwidth):
        self.wavelengths_polynomialshiftpeakwidth = []
        for i in range(len(self.num_polynomialshiftpeakwidth)):
            self.wavelengths_polynomialshiftpeakwidth.append([self.transform_calc(transform_selected[i], intensities_polynomialshiftpeakwidth[i][0])])
    
    def time_unit_update(self, value):
        self.time_unit = value

    def update_plot_args(self):
        update_plot_args_gaussianshiftpeak = [None] * len(self.num_gaussianshiftpeak) 
        update_plot_args_lorentzianshiftpeak = [None] * len(self.num_lorentzianshiftpeak) 
        update_plot_args_polynomialshiftpeak = [None] * len(self.num_polynomialshiftpeak) 
        update_plot_args_polyshiftpeak = [None] * len(self.num_polyshiftpeak) 
        update_plot_args_polynomialshift = [None] * len(self.num_polynomialshift) 
        update_plot_args_lorentzianshiftpeakwidth = [None] * len(self.num_lorentzianshiftpeakwidth) 
        update_plot_args_gaussianshiftpeakwidth = [None] * len(self.num_gaussianshiftpeakwidth)
        update_plot_args_polynomialshiftpeakwidth = [None] * len(self.num_polynomialshiftpeakwidth)
        self.frame = self.frame + (self.time / self.time_unit)




        for i in range(len(self.num_gaussianshiftpeak)):
            if len(self.gaussianshiftpeak_list) <= len(self.num_gaussianshiftpeak):
                self.gaussianshiftpeak_list.append([])
                self.frame_list_gaussianshiftpeak.append([])
            if len(self.gaussianshiftpeak_list) > len(self.num_gaussianshiftpeak):
                self.gaussianshiftpeak_list.pop()
                self.frame_list_gaussianshiftpeak.pop()
                
        if len(self.num_gaussianshiftpeak) == 0:
            self.gaussianshiftpeak_list.clear()
            self.frame_list_gaussianshiftpeak.clear()

        for i in range(len(self.num_gaussianshiftpeak)):
            self.frame_list_gaussianshiftpeak[i].append(self.frame)
            self.gaussianshiftpeak_list[i].append(np.array(self.wavelengths_gaussianshiftpeak[i][0]))

        for i in range(len(self.num_gaussianshiftpeak)):
            update_plot_args_gaussianshiftpeak[i] = (self.frame_list_gaussianshiftpeak[i], self.gaussianshiftpeak_list[i])







        for i in range(len(self.num_lorentzianshiftpeak)):
            if len(self.lorentzianshiftpeak_list) <= len(self.num_lorentzianshiftpeak):
                self.lorentzianshiftpeak_list.append([])
                self.frame_list_lorentzianshiftpeak.append([])
            if len(self.lorentzianshiftpeak_list) > len(self.num_lorentzianshiftpeak):
                self.lorentzianshiftpeak_list.pop()
                self.frame_list_lorentzianshiftpeak.pop()
                
        if len(self.num_lorentzianshiftpeak) == 0:
            self.lorentzianshiftpeak_list.clear()
            self.frame_list_lorentzianshiftpeak.clear()

        for i in range(len(self.num_lorentzianshiftpeak)):
            self.frame_list_lorentzianshiftpeak[i].append(self.frame)
            self.lorentzianshiftpeak_list[i].append(np.array(self.wavelengths_lorentzianshiftpeak[i][0]))

        for i in range(len(self.num_lorentzianshiftpeak)):
            update_plot_args_lorentzianshiftpeak[i] = (self.frame_list_lorentzianshiftpeak[i], self.lorentzianshiftpeak_list[i])






        for i in range(len(self.num_polynomialshiftpeak)):
            if len(self.polynomialshiftpeak_list) <= len(self.num_polynomialshiftpeak):
                self.polynomialshiftpeak_list.append([])
                self.frame_list_polynomialshiftpeak.append([])
            if len(self.polynomialshiftpeak_list) > len(self.num_polynomialshiftpeak):
                self.polynomialshiftpeak_list.pop()
                self.frame_list_polynomialshiftpeak.pop()
                
        if len(self.num_polynomialshiftpeak) == 0:
            self.polynomialshiftpeak_list.clear()
            self.frame_list_polynomialshiftpeak.clear()

        for i in range(len(self.num_polynomialshiftpeak)):
            self.frame_list_polynomialshiftpeak[i].append(self.frame)
            self.polynomialshiftpeak_list[i].append(np.array(self.wavelengths_polynomialshiftpeak[i][0]))

        for i in range(len(self.num_polynomialshiftpeak)):
            update_plot_args_polynomialshiftpeak[i] = (self.frame_list_polynomialshiftpeak[i], self.polynomialshiftpeak_list[i])





        for i in range(len(self.num_polyshiftpeak)):
            if len(self.polyshiftpeak_list) <= len(self.num_polyshiftpeak):
                self.polyshiftpeak_list.append([])
                self.frame_list_polyshiftpeak.append([])
            if len(self.polyshiftpeak_list) > len(self.num_polyshiftpeak):
                self.polyshiftpeak_list.pop()
                self.frame_list_polyshiftpeak.pop()
                
        if len(self.num_polyshiftpeak) == 0:
            self.polyshiftpeak_list.clear()
            self.frame_list_polyshiftpeak.clear()

        for i in range(len(self.num_polyshiftpeak)):
            self.frame_list_polyshiftpeak[i].append(self.frame)
            self.polyshiftpeak_list[i].append(np.array(self.wavelengths_polyshiftpeak[i][0]))

        for i in range(len(self.num_polyshiftpeak)):
            update_plot_args_polyshiftpeak[i] = (self.frame_list_polyshiftpeak[i], self.polyshiftpeak_list[i])







        for i in range(len(self.num_polynomialshift)):
            if len(self.polynomialshift_list) <= len(self.num_polynomialshift):
                self.polynomialshift_list.append([])
                self.frame_list_polynomialshift.append([])
            if len(self.polynomialshift_list) > len(self.num_polynomialshift):
                self.polynomialshift_list.pop()
                self.frame_list_polynomialshift.pop()
                
        if len(self.num_polynomialshift) == 0:
            self.polynomialshift_list.clear()
            self.frame_list_polynomialshift.clear()
        
        for i in range(len(self.num_polynomialshift)):
            self.frame_list_polynomialshift[i].append(self.frame)
            self.polynomialshift_list[i].append(np.array(self.wavelengths_polynomialshift[i][0]))

        for i in range(len(self.num_polynomialshift)):
            update_plot_args_polynomialshift[i] = (self.frame_list_polynomialshift[i], self.polynomialshift_list[i])





        for i in range(len(self.num_lorentzianshiftpeakwidth)):
            if len(self.lorentzianshiftpeakwidth_list) <= len(self.num_lorentzianshiftpeakwidth):
                self.lorentzianshiftpeakwidth_list.append([])
                self.frame_list_lorentzianshiftpeakwidth.append([])
            if len(self.lorentzianshiftpeakwidth_list) > len(self.num_lorentzianshiftpeakwidth):
                self.lorentzianshiftpeakwidth_list.pop()
                self.frame_list_lorentzianshiftpeakwidth.pop()
                
        if len(self.num_lorentzianshiftpeakwidth) == 0:
            self.lorentzianshiftpeakwidth_list.clear()
            self.frame_list_lorentzianshiftpeakwidth.clear()
        for i in range(len(self.num_lorentzianshiftpeakwidth)):
            self.frame_list_lorentzianshiftpeakwidth[i].append(self.frame)
            self.lorentzianshiftpeakwidth_list[i].append(np.array(self.wavelengths_lorentzianshiftpeakwidth[i][0]))

        for i in range(len(self.num_lorentzianshiftpeakwidth)):
            update_plot_args_lorentzianshiftpeakwidth[i] = (self.frame_list_lorentzianshiftpeakwidth[i], self.lorentzianshiftpeakwidth_list[i])
        






        for i in range(len(self.num_gaussianshiftpeakwidth)):
            if len(self.gaussianshiftpeakwidth_list) <= len(self.num_gaussianshiftpeakwidth):
                self.gaussianshiftpeakwidth_list.append([])
                self.frame_list_gaussianshiftpeakwidth.append([])
            if len(self.gaussianshiftpeakwidth_list) > len(self.num_gaussianshiftpeakwidth):
                self.gaussianshiftpeakwidth_list.pop()
                self.frame_list_gaussianshiftpeakwidth.pop()
                
        if len(self.num_gaussianshiftpeakwidth) == 0:
            self.gaussianshiftpeakwidth_list.clear()
            self.frame_list_gaussianshiftpeakwidth.clear()
        
        for i in range(len(self.num_gaussianshiftpeakwidth)):
            self.frame_list_gaussianshiftpeakwidth[i].append(self.frame)
            self.gaussianshiftpeakwidth_list[i].append(np.array(self.wavelengths_gaussianshiftpeakwidth[i][0]))

        for i in range(len(self.num_gaussianshiftpeakwidth)):
            update_plot_args_gaussianshiftpeakwidth[i] = (self.frame_list_gaussianshiftpeakwidth[i], self.gaussianshiftpeakwidth_list[i])




        for i in range(len(self.num_polynomialshiftpeakwidth)):
            if len(self.polynomialshiftpeakwidth_list) <= len(self.num_polynomialshiftpeakwidth):
                self.polynomialshiftpeakwidth_list.append([])
                self.frame_list_polynomialshiftpeakwidth.append([])
            if len(self.polynomialshiftpeakwidth_list) > len(self.num_polynomialshiftpeakwidth):
                self.polynomialshiftpeakwidth_list.pop()
                self.frame_list_polynomialshiftpeakwidth.pop()
                
        if len(self.num_polynomialshiftpeakwidth) == 0:
            self.polynomialshiftpeakwidth_list.clear()
            self.frame_list_polynomialshiftpeakwidth.clear()
        
        for i in range(len(self.num_polynomialshiftpeakwidth)):
            self.frame_list_polynomialshiftpeakwidth[i].append(self.frame)
            self.polynomialshiftpeakwidth_list[i].append(np.array(self.wavelengths_polynomialshiftpeakwidth[i][0]))

        for i in range(len(self.num_polynomialshiftpeakwidth)):
            update_plot_args_polynomialshiftpeakwidth[i] = (self.frame_list_polynomialshiftpeakwidth[i], self.polynomialshiftpeakwidth_list[i])
        
        



        
        self.update_plot_args_list = (
            update_plot_args_gaussianshiftpeak 
            +update_plot_args_lorentzianshiftpeak 
            +update_plot_args_polynomialshiftpeak 
            +update_plot_args_polyshiftpeak 
            +update_plot_args_polynomialshift 
            +update_plot_args_lorentzianshiftpeakwidth 
            +update_plot_args_gaussianshiftpeakwidth 
            +update_plot_args_polynomialshiftpeakwidth 
                                      )

    def plot_uniform(self):
        if self.initspectrum == True:
            self.init_plot_args()
            self.initspectrum = False
            print("init spectrum")
        self.update_plot_args()
        for i in range(
            len(self.num_gaussianshiftpeak) 
            +len(self.num_lorentzianshiftpeak)
            +len(self.num_polynomialshiftpeak)
            +len(self.num_polyshiftpeak)
            +len(self.num_polynomialshift)
            +len(self.num_lorentzianshiftpeakwidth)
            +len(self.num_gaussianshiftpeakwidth)
            +len(self.num_polynomialshiftpeakwidth)
            ):
            self.init_PlotCurveItem[i].setData(*self.update_plot_args_list[i])
            
    
    def frame_time(self, time):
        self.time = time

    def transform_calc(self, i, intensities):
        transformations = {
            0: lambda x: x,                  # f(x) = x
            1: lambda x: np.sqrt(x),         # f(x) = √x
            2: lambda x: x**2,               # f(x) = x^2
            3: lambda x: np.log(x),          # f(x) = ln(x)
            4: lambda x: 1/x,                # f(x) = 1/x
            5: lambda x: 1/(x**2),           # f(x) = 1/2[x]^2
            6: lambda x: np.log10(np.abs(x)) # f(x) = log x
        }
        return transformations[i](intensities)

    def autoscale_x(self):
        for i in range(
        len(self.num_gaussianshiftpeak) 
        +len(self.num_lorentzianshiftpeak)
        +len(self.num_polynomialshiftpeak)
        +len(self.num_polyshiftpeak)
        +len(self.num_polynomialshift)
        +len(self.num_lorentzianshiftpeakwidth)
        +len(self.num_gaussianshiftpeakwidth)
        +len(self.num_polynomialshiftpeakwidth)
        ):
            self.subplot[i].enableAutoRange(axis=pg.ViewBox.XAxis, enable=True)

    def autoscale_y(self):
        for i in range(
        len(self.num_gaussianshiftpeak) 
        +len(self.num_lorentzianshiftpeak)
        +len(self.num_polynomialshiftpeak)
        +len(self.num_polyshiftpeak)
        +len(self.num_polynomialshift)
        +len(self.num_lorentzianshiftpeakwidth)
        +len(self.num_gaussianshiftpeakwidth)
        +len(self.num_polynomialshiftpeakwidth)
        ):
            self.subplot[i].enableAutoRange(axis=pg.ViewBox.YAxis, enable=True)
            
    def setscale_y(self, min_yrange, max_yrange):
        self.archive_min_yrange = min_yrange
        self.archive_max_yrange = max_yrange
        for i in range(
        len(self.num_gaussianshiftpeak) 
        +len(self.num_lorentzianshiftpeak)
        +len(self.num_polynomialshiftpeak)
        +len(self.num_polyshiftpeak)
        +len(self.num_polynomialshift)
        +len(self.num_lorentzianshiftpeakwidth)
        +len(self.num_gaussianshiftpeakwidth)
        +len(self.num_polynomialshiftpeakwidth)
        ):
            self.subplot[i].setRange(
            # xRange=(xmin, xmax),   # Rentang untuk sumbu X
            yRange=(min_yrange, max_yrange),   # Rentang untuk sumbu Y
            padding=0.0            # Opsional, padding tambahan (0 berarti tidak ada)
            )

    # def mergesetscale_y(self):
    def mergesetscale_y(self, down, up):
        for i in range(
        len(self.num_gaussianshiftpeak) 
        +len(self.num_lorentzianshiftpeak)
        +len(self.num_polynomialshiftpeak)
        +len(self.num_polyshiftpeak)
        +len(self.num_polynomialshift)
        +len(self.num_lorentzianshiftpeakwidth)
        +len(self.num_gaussianshiftpeakwidth)
        +len(self.num_polynomialshiftpeakwidth)
        ):
            get_y_value = self.init_PlotCurveItem[i]
            _, b = get_y_value.getData()
            # a, _ = get_y_value.getData()
            var = b[-1]
            self.subplot[i].setRange(
            yRange=(var - down, var + up),
            padding=0.0 
            )

    def clearplot_plot_obj(self):
        for i in range(
        len(self.num_gaussianshiftpeak) 
        +len(self.num_lorentzianshiftpeak)
        +len(self.num_polynomialshiftpeak)
        +len(self.num_polyshiftpeak)
        +len(self.num_polynomialshift)
        +len(self.num_lorentzianshiftpeakwidth)
        +len(self.num_gaussianshiftpeakwidth)
        +len(self.num_polynomialshiftpeakwidth)
        ):
            self.subplot[i].clear()

        self.initspectrum = True
        self.plot_uniform()
        
