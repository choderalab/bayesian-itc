import logging
import numpy
from pint import UnitRegistry

logger = logging.getLogger(__name__)

ureg = UnitRegistry()
Quantity = ureg.Quantity

logger.debug("Using custom pint definition for molar unit.")
ureg.define('molar = 1 * mole / liter = M')
ureg.define('standard_concentration = 1 M')


def mole_fraction(*concentrations, **options):
    """Returns the molefraction of a component.
    concentrations - positional arguments are concentrations for solution components
    options supported:
        index - zero-based index of component for which to calculate molefraction, 0 if not given
        volumes - if given, list of volumes per component, otherwise, same volume is assumed for each component
                    Needs to be of the same length as components!
    """
    for key in options:
        if key not in ['index', 'volumes']:
            raise NameError('Unexpected keyword argument: %s' % key)

    if 'volumes' in options:
        volumes = options['volumes']
        assert(len(concentrations) == len(volumes))
        moles = numpy.array(concentrations) * numpy.array(volumes)
    else:
        moles = concentrations

    if 'index' in options:
        index = options['index']
    else:
        index = 0

    return moles[index] / sum(moles)

def x_times_onemx(x):
    """
    x - number
    Returns x * (1 - x)
    """
    return x * (1 - x)
