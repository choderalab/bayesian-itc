# Bayesian ITC 
[![Build Status](https://travis-ci.org/choderalab/bayesian-itc.svg)](https://travis-ci.org/choderalab/bayesian-itc)  
A python library for the Bayesian analysis of isothermal titration calorimetry experiments. This library is currently under heavy development, and API changes are frequent. Not all of the available command line options have been implemented yet.



## Manifest

* `scripts/bitc_util.py`, A command line utility that provides a streamlined way to interact with the library. 
  
* `bitc/` - the library with underlying tools.


## Requirements
Python2.7+, python3.3+ . We recommend using [`Anaconda`](https://store.continuum.io/cshop/anaconda/) as your python distribution. Some of the requirements will need to be installed using pip.
```
numpy
nose
pandas
pymc
pint
docopt
schema
scikit-learn
```

## Usage instructions and command line options:
```
Bayesian analysis of ITC data. Uses MicroCal .itc files, or custom format .yml files for analysing experiments.

Usage:
  ITC.py <datafiles>... [-w <workdir> | --workdir=<workdir>] [-n <name> | --name=<name>] [-q <file> | --heats=<file>] [-i <ins> | --instrument=<ins> ] [-v | -vv | -vvv] [-r <file> | --report=<file>] [ -l <logfile> | --log=<logfile>]
  ITC.py mcmc <datafiles>...  (-m <model> | --model=<model>) [-w <workdir> | --workdir=<workdir>] [ -r <receptor> | --receptor=<receptor>] [-n <name> | --name=<name>] [-q <file> | --heats=<file>] [-i <ins> | --instrument=<ins> ] [ -l <logfile> | --log=<logfile>] [-v | -vv | -vvv] [--report=<file>] [options]
  ITC.py (-h | --help)
  ITC.py --license
  ITC.py --version

Options:
  -h, --help                             Show this screen
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
```

Sample files have been included to test if the library is functional. You can find them under `bitc/testdata`.

### Usage example:

An example for a two-component binding model 
```
bitc_util.py mcmc bitc/testdata/sample.itc -w workdir -v -m TwoComponent --niters=20000 --nburn=1000 --nthin=10 --nfit=100
```

Analyse `.itc` files without mcmc

```
bitc_util.py bitc/testdata/sample.itc bitc/testdata/sample2.itc -w workdir
```

An example for a competitive binding model.
```
bitc_util.py mcmc bitc/testdata/acetyl_pepstatin.yml testdata/kni10033.yml bitc/testdata/kni10075.yml -w workdir -v -m Competitive -r "HIV protease" --niters=20000 --nburn=1000 --nthin=10 --nfit=100
```
