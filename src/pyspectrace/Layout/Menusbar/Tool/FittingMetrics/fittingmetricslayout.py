from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class FittingMetricsLayout:
    """Window that displays metrics produced by fitting operations."""

    HEADERS = ["Fitting", "R2", "-", "-"]

    def __init__(self, parent):
        self.parent = parent
        self.convert = QAction("Fitting Metrics", self.parent)
        self.convert.triggered.connect(self.show_dialog)

        self.dialog = None
        self.table_widget = None
        self.dialog_open = False
        self._rows = []

    def show_dialog(self):
        """Open the Fitting Metrics window, or bring it to the foreground."""
        if self.dialog is not None and self.dialog.isVisible():
            self.dialog.raise_()
            self.dialog.activateWindow()
            return

        self.dialog = QDialog(self.parent)
        self.dialog.setWindowTitle("Fitting Metrics")
        self.dialog.resize(960, 300)
        self.dialog.finished.connect(self._dialog_closed)

        layout = QVBoxLayout(self.dialog)
        self.table_widget = QTableWidget(0, len(self.HEADERS), self.dialog)
        self.table_widget.setHorizontalHeaderLabels(self.HEADERS)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        layout.addWidget(self.table_widget)

        self._refresh_table()

        self.dialog_open = True
        self.dialog.show()

    def add_row(self, fitting, r2, column_3="-", column_4="-"):
        """Add a metric row from this class or another class."""
        row = (fitting, r2, column_3, column_4)
        self._rows.append(row)

        if self.table_widget is not None:
            self._insert_table_row(*row)

    def set_rows(self, rows):
        """Replace all metric rows with the latest fitting results."""
        self._rows = [
            (row[0], row[1], row[2] if len(row) > 2 else "-", row[3] if len(row) > 3 else "-")
            for row in rows
        ]

        if self.table_widget is not None:
            self._refresh_table()

    def _refresh_table(self):
        self.table_widget.setRowCount(len(self._rows))

        for row_index, row in enumerate(self._rows):
            for column, value in enumerate(row):
                item = self.table_widget.item(row_index, column)
                if item is None:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_widget.setItem(row_index, column, item)
                item.setText(str(value))

    def _insert_table_row(self, fitting, r2, column_3, column_4):
        row_index = self.table_widget.rowCount()
        self.table_widget.insertRow(row_index)

        for column, value in enumerate((fitting, r2, column_3, column_4)):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row_index, column, item)

    def _dialog_closed(self, _result):
        self.dialog_open = False
        self.table_widget = None
        self.dialog = None
