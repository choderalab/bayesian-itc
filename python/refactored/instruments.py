"""Contains Isothermal titration calorimeter instrument classes."""

#=========================================================================
# Isothermal titration calorimeter instrument class.
#=========================================================================
from units import ureg,Quantity

class Instrument(object):

    """
    An isothermal titration calorimeter instrument.
    An instrument object consists of several types of data:

    * the manufacturer and model of the instrument
    * properties of the instrument (sample cell volume)
    """

    def __init__(self):
        self.V0 = None  # volume of calorimeter sample cell
        pass


class VPITC(Instrument):

    """
    The MicroCal VP-ITC.
    """

    def __init__(self):
        self.V0 = 1.4301 * ureg.milliliter  # volume of calorimeter sample cell
        # Tellinghuisen volume correction for VP-ITC
        self.V0 = self.V0 - 0.044 * ureg.milliliter
        return
