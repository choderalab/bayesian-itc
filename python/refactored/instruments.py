"""Contains Isothermal titration calorimeter instrument classes."""

from units import ureg,Quantity
import re

class Instrument(object):

    """
    An isothermal titration calorimeter instrument.
    An instrument object consists of several types of data:

    * the manufacturer and model of the instrument
    * properties of the instrument (sample cell volume)

    For best results, it is recommended to extract the volumes from a .itc file.
    """

    def __init__(self, V0=0., V_correction=0., itcfile=None, description=""):
        """Initialize an instrument from file or setting volumes and description manually.

        :rtype : object
        V0 : Volume of the cell (ureg.Quantity)
        V_correction, a volume correction (e.g. the Tellinghuisen correction for the VP-ITC)
        itcfile: a .itc file from which to extract the V0, and possibly the description.
        description: Description of the instrument. If this is set, it won't be read from file.
        """
        if not (V0 or itcfile):
            raise ValueError("No V0 or input file specified for Instrument!")
        elif V_correction and not (V0 or itcfile):
            raise ValueError("Correction was specified, but volume is not set.")

        self.V_correction = V_correction
        self.V0 = float(V0) - float(V_correction)  # volume of calorimeter sample cell
        self.description = description
        if itcfile:
            self.instrument_from_file(itcfile)

    def instrument_from_file(self, filename):
        """Grab the calibrated volume from a .itc file
        The volume is assumed to be the fourth   line in the block that starts with a #.
        This format is valid for at least the Auto-iTC200 and VPITC."""
        with open(filename, 'r') as dotitc:
            lines = dotitc.readlines()
            hash_count = 1
            for line in lines:
                # Fourth line of hash block has volume
                if hash_count == 4:
                    print line
                    self.V0 = float(line[2:]) * ureg.milliliter - self.V_correction

                if re.match('#', line):
                    hash_count += 1
                # First line in % block describes device
                elif re.match('%', line) and self.description == "":
                    self.description = line[2:]


class VPITC(Instrument):
    """
    The MicroCal VP-ITC.

    Volumes from brochure used. http://www.malvern.com/Assets/MRK2058.pdf
    If possible, we recommend using the calibrated volume for the .itc file.
    """
    def __init__(self):
        super(VPiTC, self).__init__(V0=1.400 * ureg.milliliter, V_correction=0.044 * ureg.milliliter, itcfile=None, description="MicroCal VP-iTC")



class ITC200(Instrument):
    """
    The MicroCal (Auto-)iTC200

    Volumes from brochure used. http://www.malvern.com/Assets/MRK2058.pdf
    If possible, we recommend using the calibrated volume for the .itc file.
    """
    def __init__(self):
        super(AutoiTC200, self).__init__(V0=200 * ureg.microliter, V_correction=0, itcfile=None, description="MicroCal Auto-iTC200")

AutoITC200 = ITC200

