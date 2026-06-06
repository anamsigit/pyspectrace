import sys
from PyQt5.QtWidgets import QApplication
from pyspectrace.Layout.mainlayout import MainLayout
from pyspectrace.Control.maincontrol import MainControl
from pyspectrace.Model.mainmodel import MainModel

def main():
    app = QApplication(sys.argv)

    model = MainModel()
    view = MainLayout()
    presenter = MainControl(model, view)

    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()