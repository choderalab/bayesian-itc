import os
import sys

from docopt import docopt
from schema import Schema, And, Or, Use

from bayesitc.instruments import known_instruments
from bayesitc.models import known_models


#  TODO add options for multiple types of output files
#  TODO implement license


def bayesitc_util_parser(argv=sys.argv[1:]):
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
  --niters=<n>                           No. of iterations for mcmc sampling             [default: 6000]
  --nburn=<n>                            No. of Burn-in iterations for mcmc sampling     [default: 1000]
  --nthin=<n>                            Thinning period for mcmc sampling               [default: 5]
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
                     '<datafiles>': And(list, lambda inpfiles: [os.path.isfile(inpfile) for inpfile in inpfiles],
                                        Use(lambda inpfiles: [os.path.abspath(inpfile) for inpfile in inpfiles])),
                     'mcmc': bool,  # True or False are accepted
                     '--report': Or(None, Use(lambda f: open(f, 'w'))),
                     # Don't use, or open file with writing permissions
                     '--log': Or(None, str),  # Don't use, or str
                     })

    return schema.validate(arguments)


def integrate_parser(argv=sys.argv[1:]):
    __usage__ = """
Integrate ITC data using Gaussian process regression. Uses MicroCal .itc files, or custom format .yml files for analysing experiments.

Usage:
  bayesitc_integrate.py <datafiles>... [-w <workdir> | --workdir=<workdir>] [-v | -vv | -vvv] [options]
  bayesitc_integrate.py (-h | --help)
  bayesitc_integrate.py --license
  bayesitc_integrate.py --version

Options:
  -h, --help                             Show this screen
  --version                              Show version
  --license                              Show license
  -l <logfile>, --log=<logfile>          File to write logs to. Will be placed in workdir.
  -v,                                    Verbose output level. Multiple flags increase verbosity.
  <datafiles>                            Datafile(s) to perform the analysis on, .itc, .yml
  -w <workdir>, --workdir=<workdir>      Directory for output files                      [default: ./]
  -n <name>, --name=<name>               Name for the experiment. Will be used for output files. Defaults to input file name.
  -i <ins>, --instrument=<ins>           The name of the instrument used for the experiment. Overrides .itc file instrument.
  -f <frac>, --fraction=<frac>           The fraction of the injection to fit, measured from the end [default: 0.2]
  --theta0=<theta0>                      The parameters in the autocorrelation model. [default: 5.0]
  --nugget=<nugget>                      Size of nugget effect to allow smooth predictions from noisy data. [default: 1.0]
  --plot                                 Generate plots of the baseline fit
"""

    arguments = docopt(__usage__, argv=argv, version='bayesitc_integrate.py, pre-alpha')
    schema = Schema({'--help': bool,  # True or False are accepted
                     '--license': bool,  # True or False are accepted
                     # integer between 0 and 3
                     '-v': And(int, lambda n: 0 <= n <= 3),
                     # Float greater than 0
                     '--fraction': And(Use(float), lambda n: 0 < n <= 1.0),
                     '--nugget': And(Use(float), lambda n: n > 0),
                     '--theta0': And(Use(float), lambda n: n > 0),
                     # Convert str to int, make sure that it is larger than 0
                     '--name': Or(None, And(str, len)),  # Not an empty string
                     '--instrument': Or(None, And(str, lambda m: m in known_instruments)),
                     # None, or str and found in this dict
                     '--version': bool,  # True or False are accepted
                     '--plot': bool,  # True or False are accepted
                     '--workdir': str,  # str
                     # list and ensure it contains existing files
                     '<datafiles>': And(list, lambda inpfiles: [os.path.isfile(inpfile) for inpfile in inpfiles],
                                        Use(lambda inpfiles: [os.path.abspath(inpfile) for inpfile in inpfiles])),
                     # Don't use, or open file with writing permissions
                     '--log': Or(None, str),  # Don't use, or str
                     })

    return schema.validate(arguments)


def bayesitc_mcmc_parser(argv=sys.argv[1:]):
    __usage__ = """Analyze ITC data using Markov chain Monte Carlo (MCMC). Uses MicroCal .itc files, or custom format .yml files for modeling experiments.
    When running the program you can select one of two options:

    competitive
      A competitive binding model. Requires multiple experiments to be specified.

    twocomponent
      A twocomponent binding model. Analyzes only a single experiment

    Usage:
      bayesitc_mcmc.py twocomponent <datafile> <heatsfile> [-v | -vv | -vvv] [--cc=<c_cell>] [--cs=<c_syringe> ] [--dc=<dc_cell>] [--ds=<dc_syringe>] [options]
      bayesitc_mcmc.py competitive (<datafile> <heatsfile>)... (-r <receptor> | --receptor <receptor>) [-v | -vv | -vvv] [options]
      bayesitc_mcmc.py (-h | --help)
      bayesitc_mcmc.py --license
      bayesitc_mcmc.py --version

    Options:
      -h, --help                             Show this screen
      --version                              Show version
      --license                              Show license
      -l <logfile>, --log=<logfile>          File to write logs to. Will be placed in workdir.
      --cc <c_cell>                          Concentration of component in cell in mM. Defaults to value in input file
      --cs <c_syringe>                       Concentration of component in syringe in mM. Defaults to value in input file
      --dc <dc_cell>                         Relative uncertainty in cell concentration      [default: 0.1]
      --ds <dc_syringe>                      Relative uncertainty in syringe concentration   [default: 0.1]
      -v,                                    Verbose output level. Multiple flags increase verbosity.
      -w <workdir>, --workdir <workdir>      Directory for output files                      [default: ./]
      -r <receptor> | --receptor <receptor>  The name of the receptor for a competitive binding model.
      -n <name>, --name <name>               Name for the experiment. Will be used for output files. Defaults to inputfile name.
      -i <ins>, --instrument <ins>           The name of the instrument used for the experiment. Overrides .itc file instrument.
      --nfit=<n>                             No. of iteration for maximum a posteriori fit   [default: 20000]
      --niters=<n>                           No. of iterations for mcmc sampling             [default: 2000000]
      --nburn=<n>                            No. of Burn-in iterations for mcmc sampling     [default: 500000]
      --nthin=<n>                            Thinning period for mcmc sampling               [default: 500]
"""
    arguments = docopt(__usage__, argv=argv, version='bayesitc_mcmc.py, pre-alpha')
    schema = Schema({'--help': bool,  # True or False are accepted
                     '--license': bool,  # True or False are accepted
                     # integer between 0 and 3
                     '-v': And(int, lambda n: 0 <= n <= 3),
                     # str and found in this dict
                     'twocomponent': bool,
                     'competitive': bool,
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
                     # str and ensure file exists
                     # list and ensure it contains existing files
                     '<datafile>': And(list, lambda inpfiles: [os.path.isfile(inpfile) for inpfile in inpfiles],
                                        Use(lambda inpfiles: [os.path.abspath(inpfile) for inpfile in inpfiles])),
                     # list and ensure it contains existing files
                     '<heatsfile>': And(list, lambda inpfiles: [os.path.isfile(inpfile) for inpfile in inpfiles],
                                        Use(lambda inpfiles: [os.path.abspath(inpfile) for inpfile in inpfiles])),
                     # Don't use, or open file with writing permissions
                     '--log': Or(None, str),  # Don't use, or str
                     '--cc': Or(None, And(Use(float), lambda n:  n > 0.0)), # Not specified, or a float greater than 0
                     '--cs': Or(None, And(Use(float), lambda n:  n > 0.0)),  # Not specified, or a float
                     '--dc': And(Use(float), lambda n:  n > 0.0),  # a float greater than 0
                     '--ds': And(Use(float), lambda n:  n > 0.0),  # a float greater than 0

                     })

    return schema.validate(arguments)
