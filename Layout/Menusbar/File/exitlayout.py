from PyQt5.QtWidgets import QMenuBar, QAction

class ExitLayout:
    def __init__(self, parent):
        self.parent = parent
        self.trigger_exit = QAction('Exit', self.parent)
