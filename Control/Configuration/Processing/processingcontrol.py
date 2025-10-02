from Control.Configuration.Processing.Shift.PolynomialFitting.polynomialfittingcontrol import PolynomialFittingControl
from Control.Configuration.Processing.ShiftPeak.GaussianPeakFitting.gaussianpeakfittingcontrol import GaussianPeakFittingControl
from Control.Configuration.Processing.ShiftPeak.LorentzianPeakFitting.lorentzianpeakfittingcontrol import LorentzianPeakFittingControl
from Control.Configuration.Processing.ShiftPeak.PolynomialPeakFitting.polynomialpeakfittingcontrol import PolynomialPeakFittingControl
from Control.Configuration.Processing.ShiftPeak.PolyPeakFitting.polypeakfittingcontrol import PolyPeakFittingControl
from Control.Configuration.Processing.ShiftWidthPeak.LorentzianWidthPeakFitting.lorentzianwidthpeakfittingcontrol import LorentzianWidthPeakFittingControl
from Control.Configuration.Processing.ShiftWidthPeak.GaussianWidthPeakFitting.gaussianwidthpeakfittingcontrol import GaussianWidthPeakFittingControl
from Control.Configuration.Processing.ShiftWidthPeak.PolynomialWidthPeakFitting.polynomialwidthpeakfittingcontrol import PolynomialWidthPeakFittingControl

class ProcessingControl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.polynomialfittingcontrol = PolynomialFittingControl(model, view)
        self.gaussianfittingcontrol = GaussianPeakFittingControl(model, view)
        self.lorentzianfittingcontrol = LorentzianPeakFittingControl(model, view)
        self.polypeakfittingcontrol = PolyPeakFittingControl(model, view)
        self.polynomialpeakfittingcontrol = PolynomialPeakFittingControl(model, view)
        self.lorentzianwidthpeakfittingcontrol = LorentzianWidthPeakFittingControl(model, view)
        self.gaussianwidthpeakfittingcontrol = GaussianWidthPeakFittingControl(model, view)
        self.polynomialwidthpeakfittingcontrol = PolynomialWidthPeakFittingControl(model, view)