import json
import math

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class SaveLoadConfig:
    """Save and restore all fitting-editor settings as a versioned JSON document."""

    CONFIG_FORMAT = "pyspectrace-fitting-config"
    CONFIG_VERSION = 1

    POSITION_FIELDS = (
        ("initial_center", "initial_center_values"), ("min", "min_values"),
        ("max", "max_values"), ("axis", "axis_selected"),
        ("descriptor", "method_selected"), ("transform", "transform_selected"),
        ("auto", "status_inverse"), ("label", "name_values"),
        ("color", "color_values"),
    )
    WIDTH_FIELDS = (
        ("initial_center", "initial_center_values"), ("min", "min_values"),
        ("max", "max_values"), ("descriptor", "method_selected"),
        ("transform", "transform_selected"), ("auto", "status_inverse"),
        ("label", "name_values"), ("color", "color_values"),
    )
    POLYNOMIAL_POSITION_FIELDS = (
        ("initial_center", "initial_center_values"), ("min", "min_values"),
        ("max", "max_values"), ("order", "function_orde"),
        ("span", "span_values"), ("axis", "axis_selected"),
        ("descriptor", "method_selected"), ("transform", "transform_selected"),
        ("auto", "status_inverse"), ("label", "name_values"),
        ("color", "color_values"),
    )
    POLY_PEAK_FIELDS = (
        ("initial_center", "initial_center_values"), ("min", "min_values"),
        ("max", "max_values"), ("order", "function_orde"),
        ("axis", "axis_selected"), ("descriptor", "method_selected"),
        ("transform", "transform_selected"), ("auto", "status_inverse"),
        ("label", "name_values"), ("color", "color_values"),
    )
    POLYNOMIAL_WIDTH_FIELDS = (
        ("initial_center", "initial_center_values"), ("min", "min_values"),
        ("max", "max_values"), ("descriptor", "method_selected"),
        ("order", "function_orde"), ("transform", "transform_selected"),
        ("auto", "status_inverse"), ("label", "name_values"),
        ("color", "color_values"),
    )
    NON_PEAK_FIELDS = (
        ("initial_center", "initial_center_values"), ("min", "min_values"),
        ("max", "max_values"), ("order", "function_orde"),
        ("axis", "axis_selected"), ("transform", "transform_selected"),
        ("label", "name_values"), ("color", "color_values"),
    )

    def __init__(self, view):
        self.view = view
        processing_layout = self.view.configurationlayout.processinglayout
        processing_layout.save_fitting_configuration_button.clicked.connect(self.save_fitting_configuration)
        processing_layout.load_fitting_configuration_button.clicked.connect(self.load_fitting_configuration)

    def _fitting_layouts(self):
        processing_layout = self.view.configurationlayout.processinglayout
        return {
            "peak_position": {
                "gaussian": (processing_layout.shiftpeaklayout.gaussianpeakfittinglayout, self.POSITION_FIELDS),
                "lorentzian": (processing_layout.shiftpeaklayout.lorentzianpeakfittinglayout, self.POSITION_FIELDS),
                "polynomial": (processing_layout.shiftpeaklayout.polynomialpeakfittinglayout, self.POLYNOMIAL_POSITION_FIELDS),
                "poly_peak": (processing_layout.shiftpeaklayout.polypeakfittinglayout, self.POLY_PEAK_FIELDS),
            },
            "peak_width": {
                "gaussian": (processing_layout.shiftpeakwidthlayout.gaussianpeakwidthfittinglayout, self.WIDTH_FIELDS),
                "lorentzian": (processing_layout.shiftpeakwidthlayout.lorentzianpeakwidthfittinglayout, self.WIDTH_FIELDS),
                "polynomial": (processing_layout.shiftpeakwidthlayout.polynomialpeakwidthfittinglayout, self.POLYNOMIAL_WIDTH_FIELDS),
            },
            "non_peak": {
                "polynomial": (processing_layout.shiftlayout.polynomialfittinglayout, self.NON_PEAK_FIELDS),
            },
        }

    def _serialize_rows(self, fitting_layout, fields):
        row_count = len(fitting_layout.num_fitting)
        for json_name, attribute in fields:
            if len(getattr(fitting_layout, attribute)) < row_count:
                raise ValueError(f"Incomplete {json_name} values in the fitting editor.")

        rows = []
        for row_index in range(row_count):
            row = {}
            for json_name, attribute in fields:
                value = getattr(fitting_layout, attribute)[row_index]
                if json_name == "color":
                    row[json_name] = value.name()
                elif json_name in {"axis", "descriptor", "transform", "order"}:
                    row[json_name] = int(value)
                else:
                    row[json_name] = value
            rows.append(row)
        return rows

    def _configuration_document(self):
        fittings = {}
        for section, fitting_types in self._fitting_layouts().items():
            fittings[section] = {
                fitting_type: self._serialize_rows(fitting_layout, fields)
                for fitting_type, (fitting_layout, fields) in fitting_types.items()
            }
        return {"format": self.CONFIG_FORMAT, "version": self.CONFIG_VERSION, "fittings": fittings}

    def save_fitting_configuration(self):
        filename, _ = QFileDialog.getSaveFileName(
            self.view, "Save Fitting Configuration", "fitting-configuration.json",
            "Fitting configuration (*.json)",
        )
        if not filename:
            return
        if not filename.lower().endswith(".json"):
            filename += ".json"

        try:
            with open(filename, "w", encoding="utf-8") as configuration_file:
                json.dump(self._configuration_document(), configuration_file, indent=2)
        except (OSError, TypeError, ValueError) as error:
            QMessageBox.critical(
                self.view, "Save failed", f"The fitting configuration could not be saved.\n\n{error}"
            )
            return
        QMessageBox.information(self.view, "Configuration saved", "Fitting configuration saved successfully.")

    def load_fitting_configuration(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.view, "Load Fitting Configuration", "",
            "Fitting configuration (*.json);;All files (*)",
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as configuration_file:
                configuration = self._validate_configuration(json.load(configuration_file))
        except (OSError, json.JSONDecodeError, ValueError, TypeError) as error:
            QMessageBox.critical(
                self.view, "Load failed", f"The selected file is not a valid fitting configuration.\n\n{error}"
            )
            return

        result = QMessageBox.question(
            self.view, "Replace fitting configuration?",
            "Loading will replace all active fitting configurations. Continue?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if result != QMessageBox.Yes:
            return

        loaded_fitting_layouts = []
        for section, fitting_types in self._fitting_layouts().items():
            for fitting_type, (fitting_layout, fields) in fitting_types.items():
                rows = configuration[section][fitting_type]
                self._restore_rows(fitting_layout, fields, rows)
                if hasattr(fitting_layout, "table_widget"):
                    fitting_layout.populate_table(fitting_layout.table_widget)
                fitting_layout.dialog_open = True
                if rows:
                    loaded_fitting_layouts.append(fitting_layout)

        self._open_loaded_fitting_windows(loaded_fitting_layouts)
        # QMessageBox.information(self.view, "Configuration loaded", "Fitting configuration loaded successfully.")

    def _validate_configuration(self, document):
        if not isinstance(document, dict):
            raise ValueError("The configuration root must be an object.")
        if document.get("format") != self.CONFIG_FORMAT:
            raise ValueError("This file is not a PySpectrace fitting configuration.")
        if document.get("version") != self.CONFIG_VERSION:
            raise ValueError(f"Unsupported configuration version: {document.get('version')!r}.")

        fitting_document = document.get("fittings")
        layouts = self._fitting_layouts()
        if not isinstance(fitting_document, dict) or set(fitting_document) != set(layouts):
            raise ValueError("The file does not contain the complete set of fitting sections.")

        validated = {}
        for section, fitting_types in layouts.items():
            section_document = fitting_document[section]
            if not isinstance(section_document, dict) or set(section_document) != set(fitting_types):
                raise ValueError(f"Invalid fitting types in {section}.")
            validated[section] = {}
            for fitting_type, (_, fields) in fitting_types.items():
                rows = section_document[fitting_type]
                if not isinstance(rows, list):
                    raise ValueError(f"{section}.{fitting_type} must be a list of fitting rows.")
                validated[section][fitting_type] = [
                    self._validate_row(row, fields, f"{section}.{fitting_type}") for row in rows
                ]
        return validated

    def _validate_row(self, row, fields, fitting_name):
        expected_names = {json_name for json_name, _ in fields}
        if not isinstance(row, dict) or set(row) != expected_names:
            raise ValueError(f"Invalid fields in {fitting_name}.")

        normalized = {}
        numeric_names = {"initial_center", "min", "max", "span"}
        index_names = {"axis", "descriptor", "transform", "order"}
        for json_name, _ in fields:
            value = row[json_name]
            if json_name == "color":
                if not isinstance(value, str) or not QColor(value).isValid():
                    raise ValueError(f"Invalid color in {fitting_name}.")
                normalized[json_name] = QColor(value).name()
            elif json_name == "label":
                if not isinstance(value, str):
                    raise ValueError(f"Invalid label in {fitting_name}.")
                normalized[json_name] = value
            elif json_name == "auto":
                if not isinstance(value, bool):
                    raise ValueError(f"Invalid Auto value in {fitting_name}.")
                normalized[json_name] = value
            elif json_name in numeric_names:
                try:
                    numeric_value = float(value)
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid {json_name} value in {fitting_name}.")
                if not math.isfinite(numeric_value):
                    raise ValueError(f"Invalid {json_name} value in {fitting_name}.")
                normalized[json_name] = str(value)
            elif json_name in index_names:
                if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                    raise ValueError(f"Invalid {json_name} value in {fitting_name}.")
                normalized[json_name] = value
        return normalized

    def _restore_rows(self, fitting_layout, fields, rows):
        row_count = len(rows)
        fitting_layout.num_fitting = [None] * row_count
        if hasattr(fitting_layout, "num_shiftpeak"):
            fitting_layout.num_shiftpeak = [None] * row_count
        if hasattr(fitting_layout, "num_widthpeak"):
            fitting_layout.num_widthpeak = [None] * row_count

        if row_count == 0:
            for _, attribute in fields:
                if attribute not in {
                    "initial_center_values", "min_values", "max_values",
                    "function_orde", "span_values",
                }:
                    setattr(fitting_layout, attribute, [])
            return

        for json_name, attribute in fields:
            values = [row[json_name] for row in rows]
            if json_name == "color":
                values = [QColor(color) for color in values]
            setattr(fitting_layout, attribute, values)

    def _open_loaded_fitting_windows(self, fitting_layouts):
        """Open the editor for every fitting type restored with one or more rows.
        For trigger another logic purpose, a click on the fitting button of each layout to open the corresponding editor window."""
        for fitting_layout in fitting_layouts:
            fitting_layout.button.click()
