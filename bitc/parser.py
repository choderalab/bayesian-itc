import sys
import os

from docopt import docopt
from schema import Schema, And, Or, Use

from bitc.models import known_models
from bitc.instruments import known_instruments


#  TODO add options for multiple types of output files
#  TODO implement license


def optparser(argv=sys.argv[1:]):
    __usage__ = """
Bayesian analysis of ITC data. Uses MicroCal .itc files, or custom format .yml files for analysing experiments.

Usage:
  ITC.py <datafiles>... [-w <workdir> | --workdir=<workdir>] [-n <name> | --name=<name>] [-q <file> | --heats=<file>] [-i <ins> | --instrument=<ins> ] [-v | -vv | -vvv] [-r <file> | --report=<file>] [ -l <logfile> | --log=<logfile>]
  ITC.py mcmc <datafiles>...  (-m <model> | --model=<model>) [-w <workdir> | --workdir=<workdir>] [ -r <receptor> | --receptor=<receptor>] [-n <name> | --name=<name>] [-q <file> | --heats=<file>] [-i <ins> | --instrument=<ins> ] [ -l <logfile> | --log=<logfile>] [-v | -vv | -vvv] [--report=<file>] [options]
  ITC.py (-h | --help)
  ITC.py --license
  ITC.py --version

Options:
  -h, --help                            Show this screen
  --version                              Show version
  --license                              Show license
  -l <logfile>, --log=<logfile>          File to write logs to. Will be placed in workdir.
  -v,                                    Verbose output level. Multiple flags increase verbosity.
  <datafiles>                            Datafile(s) to perform the analysis on, .itc, .yml
  -w <workdir>, --workdir=<workdir>      Directory for output files                      [default: ./]
  -r <receptor> | --receptor=<receptor>  The name of the receptor for a Competitive Binding model.
  -n <name>, --name=<name>               Name for the experiment. Will be used for output files. Defaults to inputfile name.
  -i <ins>, --instrument=<ins>           The name of the instrument used for the experiment. Overrides .itc file instrument.
  -q <file>, --heats=<file>              Origin format integrated heats file. (From NITPIC use .dat file)
  -m <model>, --model=<model>            Model to use for mcmc sampling                  [default: TwoComponent]
  --nfit=<n>                             No. of iteration for maximum a posteriori fit   [default: 20000]
  --niters=<n>                           No. of iterations for mcmc sampling             [default: 2000000]
  --nburn=<n>                            No. of Burn-in iterations for mcmc sampling     [default: 500000]
  --nthin=<n>                            Thinning period for mcmc sampling               [default: 250]
  --report=<file>                        Output file with summary in markdown
"""
    arguments = docopt(__usage__, argv=argv, version='ITC.py, pre-alpha')
    schema = Schema({'--heats': Or(None, And(str, os.path.isfile, Use(os.path.abspath))),  # str, verify that it exists
                     '--help': bool,  # True or False are accepted
                     '--license': bool,  # True or False are accepted
                     # integer between 0 and 3
                     '-v': And(int, lambda n: 0 <= n <= 3),
                     # str and found in this dict
                     '--model': And(str, lambda m: m in known_models),
                     '--nfit': And(Use(int), lambda n: n > 0),
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
                     '--receptor': Or(None, str),  # str or None
                     '--workdir': str,  # str
                     # list and ensure it contains existing files
                     '<datafiles>': And(list, lambda inpfiles: [os.path.isfile(inpfile) for inpfile in inpfiles], Use(lambda inpfiles: [os.path.abspath(inpfile) for inpfile in inpfiles])),
                     'mcmc': bool,  # True or False are accepted
                     '--report': Or(None, Use(lambda f: open(f, 'w'))),
                     # Don't use, or open file with writing permissions
                     '--log': Or(None, str),  # Don't use, or str
                     })

    return schema.validate(arguments)
