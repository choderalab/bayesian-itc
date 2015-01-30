__author__ = 'bas'

from docopt import docopt
from schema import Schema, And, Or, Use
from .models import known_models
from .instruments import known_instruments
import sys
import os
import numpy as np
import pandas as pd
from units import Quantity

#  TODO add options for multiple types of output files
#  TODO implement license


def optparser(argv=sys.argv[1:]):
    __usage__ = """
Bayesian analysis of MicroCal .itc file data.



Usage:
  ITC.py <datafile> <workdir> [-n <name> | --name=<name>] [-q <file> | --heats=<file>] [-i <ins> | --instrument=<ins> ] [-v | -vv | -vvv] [-r <file> | --report=<file>] [ -l <logfile> | --log=<logfile>]
  ITC.py mcmc <datafile> <workdir> (-m <model> | --model=<model>) [-n <name> | --name=<name>] [-q <file> | --heats=<file>] [-i <ins> | --instrument=<ins> ] [ -l <logfile> | --log=<logfile>] [-v | -vv | -vvv] [-r <file> | --report=<file>] [options]
  ITC.py (-h | --help)
  ITC.py --license
  ITC.py --version

Options:
  -h, --help                     Show this screen
  --version                      Show version
  --license                      Show license
  -l <logfile>, --log=<logfile>  File to write logs to. Will be placed in workdir.
  -v,                            Verbose output level. Multiple flags increase verbosity.
  <datafile>                     A .itc file to perform the analysis on
  <workdir>                      Directory for output files
  -n <name>, --name=<name>       Name for the experiment. Will be used for output files. Defaults to inputfile name.
  -i <ins>, --instrument=<ins>   The name of the instrument used for the experiment. Overrides .itc file instrument.
  -q <file>, --heats=<file>      Origin format integrated heats file. (From NITPIC use .dat file)
  -m <model>, --model=<model>    Model to use for mcmc sampling                  [default: TwoComponent]
  --nfit=<n>                     No. of iteration for maximum a posteriori fit   [default: 20000]
  --niters=<n>                   No. of iterations for mcmc sampling             [default: 2000000]
  --nburn=<n>                    No. of Burn-in iterations for mcmc sampling     [default: 500000]
  --nthin=<n>                    Thinning period for mcmc sampling               [default: 250]
  -r <file>, --report=<file>     Output file with summary in markdown
"""
    arguments = docopt(__usage__, argv=argv, version='ITC.py, pre-alpha')
    schema = Schema({'--heats': Or(None, And(str, os.path.isfile, Use(os.path.abspath))),  # str, verify that it exists
                     '--help': bool,  # True or False are accepted
                     '--license': bool,  # True or False are accepted
                     '-v': And(int, lambda n: 0 <= n <= 3),  # integer between 0 and 3
                     '--model': And(str, lambda m: m in known_models),  # str and found in this dict
                     '--nfit':And(Use(int), lambda n: n > 0),
                     # Convert str to int, make sure that it is larger than 0
                     '--nburn': And(Use(int), lambda n: n > 0),
                     # Convert str to int, make sure that it is larger than 0
                     '--niters': And(Use(int), lambda n: n > 0),
                     # Convert str to int, make sure that it is larger than 0
                     '--nthin': And(Use(int), lambda n: n > 0),
                     # Convert str to int, make sure that it is larger than 0
                     '--name': Or(None, And(str, len)),  # Not an empty string
                     '--instrument': Or(None, And(str, lambda m: m in known_instruments)),
                     # None, or str and found in this dict
                     '--version': bool,  # True or False are accepted
                     '<workdir>': str,
                     # Check if directory exists, or make the directory
                     '<datafile>': And(str, os.path.isfile, Use(os.path.abspath)),  # str, and ensure it is an existing file
                     'mcmc': bool,  # True or False are accepted
                     '--report': Or(None, Use(lambda f: open(f, 'w'))),
                     # Don't use, or open file with writing permissions
                     '--log': Or(None, str),  # Don't use, or str
                    })

    return schema.validate(arguments)

def origin_heats_parser(input_file, unit=Quantity('microcalorie')):
    """
    Parse an origin heats file and return the heats as array with pint units
    :param input_file:
    :type input_file:
    :param unit:
    :type unit:
    :return:
    :rtype:
    """

    assert isinstance(input_file, str)
    dataframe = pd.read_table(input_file, skip_footer=1, engine='python') # Need python engine for skip_footer
    heats = np.array(dataframe['DH'])
    return Quantity(heats, unit)

