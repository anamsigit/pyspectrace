class SensorgramControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        self.current_frame = []
        self.index = []
        self.time = 250
        # self.running = True

    def mainloop(self):
        # if self.running:
        #     self.update_plot()
        self.update_plot()

    def update_plot(self):
        self.view.plottinglayout.sensorgramlayout.plot_uniform()
    
    def update_frame_time(self, time):
        self.time = time
        self.view.plottinglayout.sensorgramlayout.frame_time(self.time)
        

    
