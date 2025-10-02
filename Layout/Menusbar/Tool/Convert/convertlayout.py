from Layout.Menusbar.Tool.Plot3D.plot3dlayout import Plot3DLayout
from PyQt5.QtWidgets import QMenuBar, QAction

class ConvertLayout:
    def __init__(self, parent):
        self.parent = parent
        self.convert = QAction('Converter', self.parent)
