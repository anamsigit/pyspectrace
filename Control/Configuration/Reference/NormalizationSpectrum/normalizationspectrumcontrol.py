from Control.Configuration.Reference.NormalizationSpectrum.BrightSpectrum.brightspectrumcontrol import BrightSpectrumControl
from Control.Configuration.Reference.NormalizationSpectrum.DarkSpectrum.darkspectrumcontrol import DarkSpectrumControl
import numpy as np
from datetime import datetime
import os


class NormalizationSpectrumControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.brightspectrumcontrol = BrightSpectrumControl(model, view)
        self.darkspectrumcontrol = DarkSpectrumControl(model, view)

        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_bright_button.clicked.connect(self.brightspectrumcontrol.take)
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_dark_button.clicked.connect(self.darkspectrumcontrol.take)
        
        # self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_bright_button.clicked.connect(self.brightspectrumcontrol.update)
        # self.view.configurationlayout.referencelayout.normalizationspectrumlayout.take_dark_button.clicked.connect(self.darkspectrumcontrol.update)

        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_bright_button.clicked.connect(self.brightspectrumcontrol.clear)
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.clear_dark_button.clicked.connect(self.darkspectrumcontrol.clear)

        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.save_bright_button.clicked.connect(self.brightspectrumcontrol.saving)
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.save_dark_button.clicked.connect(self.darkspectrumcontrol.saving)

        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.load_bright_button.clicked.connect(self.brightspectrumcontrol.load)
        self.view.configurationlayout.referencelayout.normalizationspectrumlayout.load_dark_button.clicked.connect(self.darkspectrumcontrol.load)

