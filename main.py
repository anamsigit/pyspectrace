import sys
from PyQt5.QtWidgets import QApplication
from Layout.mainlayout import MainLayout
from Control.maincontrol import MainControl
from Model.mainmodel import MainModel

# def __del__(self):
#     # Pastikan untuk melepaskan perangkat saat objek ini dihancurkan
#     self.dll.LTs_ReleaseAllSpectrometers()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = MainModel()
    view = MainLayout()
    presenter = MainControl(model, view)
    view.show()
    sys.exit(app.exec_())