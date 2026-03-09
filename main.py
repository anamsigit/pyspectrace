# Copyright 2026 - BRIN.Nanoplasmonics

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


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
