from PyQt5.QtWidgets import QMenuBar, QAction

class Plot3DLayout:
    def __init__(self, parent):
        self.parent = parent
        # self.plot_3d_current = QAction('Current raw spectrum', self.parent)
        self.plot_3d_choosing = QAction('Upload spectrum', self.parent)
        