from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class InfoLayout(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("info_layout")
        self.initUI()

    def initUI(self):
        self.nested_tabs = QWidget()
        self.nested_tabs_layout = QVBoxLayout()

        self.log_name_label = QLabel("Log name")
        self.log_name_textbox = QLineEdit()
        self.log_name_textbox.setPlaceholderText("Enter log name")

        self.log_name_layout = QHBoxLayout()
        self.log_name_layout.addWidget(self.log_name_label)
        self.log_name_layout.addWidget(self.log_name_textbox)

        self.log_message_label = QLabel("Log message")
        self.log_message_textbox = QTextEdit()
        self.log_message_textbox.setPlaceholderText("Write a log message...")
        self.submit_log_button = QPushButton("Save log")
        self.submit_log_button.setEnabled(False)

        self.log_name_textbox.textChanged.connect(self.update_log_controls)

        self.nested_tabs_layout.addLayout(self.log_name_layout)
        self.nested_tabs_layout.addWidget(self.log_message_label)
        self.nested_tabs_layout.addWidget(self.log_message_textbox)
        self.nested_tabs_layout.addWidget(self.submit_log_button)
        self.nested_tabs_layout.addStretch()
        self.nested_tabs.setLayout(self.nested_tabs_layout)

    def update_log_controls(self, _=None):
        """Require a log name before a log entry can be saved."""
        has_log_name = bool(self.log_name_textbox.text().strip())
        self.submit_log_button.setEnabled(has_log_name)
    
    def normalization_status(self):
        pass

    def spectrometerconnect_status(self):
        pass
    
    def computerresourcesusage_status(self):
        pass

    def computerresourcesusage_status(self):
        pass

    
