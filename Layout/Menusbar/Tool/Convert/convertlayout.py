
from PyQt5.QtWidgets import  QAction

class ConvertLayout:
    def __init__(self, parent):
        self.parent = parent
        self.convert = QAction('Converter', self.parent)
