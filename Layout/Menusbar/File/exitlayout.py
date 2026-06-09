from PyQt5.QtWidgets import  QAction

class ExitLayout:
    def __init__(self, parent):
        self.parent = parent
        self.trigger_exit = QAction('Exit', self.parent)
