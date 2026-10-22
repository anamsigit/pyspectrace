import numpy as np


class FittingMetricsControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.r2_values = {}

    def calculate_and_print(self, fitting_data):
        """Calculate R2 for each fitting result, print it, and update the table."""
        self.r2_values = {}
        table_rows = []

        for fitting_names, observed_values, fitted_values in fitting_data:
            observed_values = self._as_fitting_list(observed_values)
            fitted_values = self._as_fitting_list(fitted_values)
            fitting_names = list(fitting_names)

            for index, (observed, fitted) in enumerate(zip(observed_values, fitted_values)):
                fitting_name = fitting_names[index] if index < len(fitting_names) else ""
                r2_value = self.calculate_r2(observed, fitted)
                self.r2_values[fitting_name] = r2_value
                table_rows.append((fitting_name, f"{r2_value:.6f}"))

        fitting_metrics_layout = self.view.menusbarlayout.toollayout.fittingmetricslayout
        fitting_metrics_layout.set_rows(table_rows)

    @staticmethod
    def _as_fitting_list(values):
        """Convert one ROI or a list of ROIs into a list of fitting results."""
        if isinstance(values, np.ndarray):
            return [values]

        if isinstance(values, (list, tuple)):
            if not values:
                return []
            if np.isscalar(values[0]):
                return [values]
            return list(values)

        return [values]

    @staticmethod
    def calculate_r2(y_true, y_fit):
        """Return R2 for equally sized observed and fitted intensity arrays."""
        y_true = np.asarray(y_true, dtype=float)
        y_fit = np.asarray(y_fit, dtype=float)

        if y_true.size == 0 or y_fit.size == 0 or y_true.shape != y_fit.shape:
            return np.nan

        valid_values = np.isfinite(y_true) & np.isfinite(y_fit)
        if not np.any(valid_values):
            return np.nan

        y_true = y_true[valid_values]
        y_fit = y_fit[valid_values]
        ss_res = np.sum((y_true - y_fit) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)

        if ss_tot == 0:
            return np.nan

        return float(1 - (ss_res / ss_tot))
