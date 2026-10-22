import numpy as np

class SpectrumControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view

    def mainloop(self):
        self.update_plot()

    def update_plot(self):
        self.view.plottinglayout.spectrumlayout.plot_uniform()
    

        