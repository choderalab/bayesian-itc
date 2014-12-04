__author__ = 'bas'

from docopt import docopt
from schema import Schema, And, Or, Use
from models import known_models
from instruments import known_instruments
import sys
import os

#  TODO add options for multiple types of output files
#  TODO implement license


def parser(argv=sys.argv):
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
  -n <name>, --name=<name>       Name for the experiment. Will be used for output files. [default: '']
  -i <ins>, --instrument=<ins>   The name of the instrument used for the experiment. Overrides .itc file instrument.
  -q <file>, --heats=<file>      Integrated heats (q_n) from file
  -m <model>, --model=<model>    Model to use for mcmc sampling                  [default: TwoComponent]
  --niters=<n>                   No. of iterations for mcmc sampling             [default: 2000000]
  --nburn=<n>                    No. of Burn-in iterations for mcmc sampling     [default: 500000]
  --nthin=<n>                    Thinning period for mcmc sampling               [default: 250]
  -r <file>, --report=<file>     Output file with summary in markdown
"""
    arguments = docopt(__usage__, argv=argv, version='ITC.py, pre-alpha')
    schema = Schema({'--heats': Or(None, And(str, os.path.isfile)),  # str, verify that it exists
                     '--help': bool,  # True or False are accepted
                     '--license': bool,  # True or False are accepted
                     '-v': And(int, lambda n: 0 <= n <= 3),  # integer between 0 and 3
                     '--model': And(str, lambda m: m in known_models),  # str and found in this dict
                     '--nburn': And(Use(int), lambda n: n > 0),
                     # Convert str to int, make sure that it is larger than 0
                     '--niters': And(Use(int), lambda n: n > 0),
                     # Convert str to int, make sure that it is larger than 0
                     '--nthin': And(Use(int), lambda n: n > 0),
                     # Convert str to int, make sure that it is larger than 0
                     '--name': And(str, len),  # Not an empty string
                     '--instrument': Or(None, And(str, lambda m: m in known_instruments)),
                     # None, or str and found in this dict
                     '--version': bool,  # True or False are accepted
                     '<workdir>': Or(os.path.exists, Use(lambda p: os.mkdir(p))),
                     # Check if directory    exists, or make the directory
                     '<datafile>': And(str, os.path.isfile),  # str, and ensure it is an existing file
                     'mcmc': bool,  # True or False are accepted
                     '--report': Or(None, Use(lambda f: open(f, 'w'))),
                     # Don't use, or open file with writing permissions
                     '--log': Or(None, str),  # Don't use, or str
                    })


    return schema.validate(arguments)
