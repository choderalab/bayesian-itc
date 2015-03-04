"""Contains Isothermal titration calorimeter instrument classes."""

import re
import logging

from bitc.units import ureg

logger = logging.getLogger(__name__)


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
            raise ValueError(
                "Correction was specified, but volume is not set.")

        self.V_correction = V_correction
        self.V0 = V0 - V_correction  # volume of calorimeter sample cell
        self.description = description
        if itcfile:
            self.instrument_from_file(itcfile)

    def instrument_from_file(self, filename):
        """Grab the calibrated volume from a .itc file
        The volume is assumed to be the fourth   line in the block that starts with a #.
        This format is valid for at least the Auto-iTC200 and VPITC."""
        try:
            if type(filename) == str:
                dotitc = open(filename, 'r')
            else:
                dotitc = filename

            logger.info("Reading volumes from a .itc file.")
            lines = dotitc.readlines()
            hash_count = 1
            for line in lines:
                # Fourth line of hash block has volume
                if hash_count == 4:
                    logger.info("Read current field as V0: %s" % line)
                    self.V0 = float(line[2:]) * ureg.milliliter - self.V_correction

                if re.match('#', line):
                    hash_count += 1
                # First line in % block describes device
                elif re.match('%', line) and self.description == "":
                    logger.debug("Read current field as instrument description: %s" % line)
                    self.description = line[2:]
        finally:
            dotitc.close()


class VPITC(Instrument):

    """
    The MicroCal VP-ITC.

    Volumes from brochure used. http://www.malvern.com/Assets/MRK2058.pdf
    If possible, we recommend using the calibrated volume for the .itc file.
    """

    def __init__(self):
        super(VPITC, self).__init__(V0=1.400 * ureg.milliliter, V_correction=0.044 * ureg.milliliter, itcfile=None, description="MicroCal VP-iTC")


class ITC200(Instrument):

    """
    The MicroCal (Auto-)iTC200

    Volumes from brochure used. http://www.malvern.com/Assets/MRK2058.pdf
    If possible, we recommend using the calibrated volume for the .itc file.
    """

    def __init__(self):
        super(ITC200, self).__init__(V0=200 * ureg.microliter, V_correction=0, itcfile=None, description="MicroCal Auto-iTC200")

AutoITC200 = ITC200

# Container for all instruments that this module provides
known_instruments = dict()
known_instruments.update(dict.fromkeys(['VPITC', 'VPiTC', 'VP-iTC', 'vpitc', 'vp-itc'], VPITC))
known_instruments.update(dict.fromkeys(['ITC200', 'iTC200', 'ITC200', 'itc200'], ITC200))
known_instruments.update(dict.fromkeys(['autoitc', 'auto-itc', 'auto-itc200', 'AUTOITC',  'AUTO-ITC', 'AUTO-ITC200',
                                        'AUTOITC200', 'AutoiTC', 'Auto-iTC', 'Auto-ITC',  'Auto-iTC200', 'Auto-ITC200',
                                        ],
                                       AutoITC200))
