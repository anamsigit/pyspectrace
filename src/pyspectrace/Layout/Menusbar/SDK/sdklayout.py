from PyQt5.QtWidgets import QAction


class SDKLayout:
    def __init__(self, parent):
        self.parent = parent

        self.ocean_add_dll = QAction("Add Ocean Optics DLL", self.parent)
        self.cni_add_dll = QAction("Add CNI Laser DLL", self.parent)
        self.avantes_add_dll = QAction("Add Avantes DLL", self.parent)
        self.open_sdk_folder = QAction("Open SDK Folder", self.parent)
