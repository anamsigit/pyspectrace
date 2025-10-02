import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
import pyqtgraph as pg


class PlotSensorgramControl(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQtGraph CSV Plotter")
        self.setGeometry(100, 100, 1000, 700)

        # Widget utama
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Layout utama
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        # Tombol untuk menambah file
        self.addFileButton = QPushButton("Add sensorgram file")
        self.addFileButton.clicked.connect(self.load_csv)
        self.layout.addWidget(self.addFileButton)

        # Plot area
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setBackground('w')
        self.plotWidget.setLabel('left', "Descriptor")
        self.plotWidget.setLabel('bottom', "Time")
        self.plotWidget.addLegend()
        self.layout.addWidget(self.plotWidget)

        self.data = []  # List untuk menyimpan data CSV yang di-load
        self.curves = []  # List untuk menyimpan plot yang ditampilkan

    def load_csv(self):
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if file_paths:
            for file_path in file_paths:
                data = pd.read_csv(file_path)
                if 'Descriptor' not in data.columns or 'Time' not in data.columns:
                    print(f"{file_path} 'Descriptor' or 'Time' column not found")
                    continue
                
                y = data['Descriptor'].values
                x = data['Time'].values
                
                self.data.append((x, y, file_path))
            
            self.update_plot()
    
    def update_plot(self):
        self.plotWidget.clear()
        self.curves = []
        
        for i, (x, y, label) in enumerate(self.data):
            curve = self.plotWidget.plot(x, y, pen=(i, len(self.data)), name=label)
            self.curves.append(curve)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotSensorgramControl()
    window.show()
    sys.exit(app.exec_())
