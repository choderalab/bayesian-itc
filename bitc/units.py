import logging

from pint import UnitRegistry

logger = logging.getLogger(__name__)

ureg = UnitRegistry()
Quantity = ureg.Quantity

logger.debug("Using custom pint definition for molar unit.")
ureg.define('molar = 1 * mole / liter = M')
ureg.define('standard_concentration = 1 M')
