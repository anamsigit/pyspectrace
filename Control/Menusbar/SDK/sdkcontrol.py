import os
import subprocess
import sys

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from pyspectrace.Model.sdkmanager import get_sdk_root, install_sdk_files


class SDKControl:
    VENDORS = {
        "ocean": "Ocean Optics",
        "cni": "CNI Laser",
        "avantes": "Avantes",
    }

    def __init__(self, model, view):
        self.model = model
        self.view = view
        layout = self.view.menusbarlayout.sdklayout

        layout.ocean_add_dll.triggered.connect(lambda: self.add_dll("ocean"))
        layout.cni_add_dll.triggered.connect(lambda: self.add_dll("cni"))
        layout.avantes_add_dll.triggered.connect(lambda: self.add_dll("avantes"))
        layout.open_sdk_folder.triggered.connect(self.open_sdk_folder)

    def add_dll(self, vendor):
        vendor_name = self.VENDORS[vendor]
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            f"Select {vendor_name} DLL",
            "",
            "DLL files (*.dll);;All files (*)",
        )
        if not file_path:
            return

        try:
            copied = install_sdk_files(vendor, [file_path])
            self.show_success(vendor_name, copied)
        except OSError as error:
            QMessageBox.critical(self.view, "SDK install failed", str(error))

    def open_sdk_folder(self):
        sdk_root = get_sdk_root()
        os.makedirs(sdk_root, exist_ok=True)

        if sys.platform.startswith("win"):
            os.startfile(sdk_root)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", sdk_root])
        else:
            subprocess.Popen(["xdg-open", sdk_root])

    def show_success(self, vendor_name, copied):
        if not copied:
            QMessageBox.warning(
                self.view,
                "No DLL copied",
                f"No DLL was copied for {vendor_name}.",
            )
            return

        QMessageBox.information(
            self.view,
            "DLL installed",
            f"{vendor_name} DLL copied:\n{os.path.basename(copied[0])}\n\nTarget:\n{os.path.dirname(copied[0])}\n\nPlease close and reopen PySpectra to load the new SDK.",
        )
