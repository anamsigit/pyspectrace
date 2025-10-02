from PyQt5.QtWidgets import QMenuBar, QAction
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Layout.Menusbar.Tool.toollayout import ToolLayout
from Layout.Menusbar.File.showrecordcontrollerlayout import ShowRecordControllerLayout
from Layout.Menusbar.File.exitlayout import ExitLayout

class MenusbarLayout:
    def __init__(self, parent):
        self.parent = parent

        self.toollayout = ToolLayout(self.parent)
        self.exitlayout = ExitLayout(self.parent)
        self.showrecordcontrollerlayout = ShowRecordControllerLayout(self.parent)
        menubar = QMenuBar(self.parent)

        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        tool_menu = menubar.addMenu('Tool')
        # optimize_menu = menubar.addMenu('Optimize')
        help_menu = menubar.addMenu('Help')
        # geneticalgorithm_menu  = optimize_menu.addMenu('Genetic Algorithm')

        plot3d_menu = tool_menu.addMenu('3D Plot')
        self.preference = QAction('Preference', self.parent)
        
        # self.show_log = QAction('Show log', self.parent)
        # self.save_configuration = QAction('Save configuration', self.parent)
        # self.load_configuration = QAction('Load configuration', self.parent)
        about = QAction('About', self.parent)

        # file_menu.addAction(self.save_configuration)
        # file_menu.addAction(self.load_configuration)
        help_menu.addAction(about)
        file_menu.addAction(self.exitlayout.trigger_exit)
        # file_menu.addAction(self.showrecordcontrollerlayout.trigger_showrecordcontroller)
        # edit_menu.addAction(self.show_log)
        edit_menu.addAction(self.preference)
        tool_menu.addAction(self.toollayout.convertlayout.convert)
        tool_menu.addAction(self.toollayout.plotsensorgramlayout.plot_sensogram_choosing)
        # plot3d_menu.addAction(self.toollayout.plot3dlayout.plot_3d_current)
        plot3d_menu.addAction(self.toollayout.plot3dlayout.plot_3d_choosing)
        self.parent.setMenuBar(menubar)


