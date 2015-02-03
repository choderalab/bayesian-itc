# Bayesian ITC
A python library for the Bayesian analysis of isothermal titration calorimetry experiments. This library is currently under heavy development, and API changes are frequent. Not all of the available command line options have been implemented yet.



## Manifest

* `scripts/bitc_util.py`, A command line utility that provides a streamlined way to interact with the library. 
  
* `bitc/` - the library with underlying tools.


## Requirements
Python2.7. Necessary modules are listed in `requirements.txt`. We recommend using [`Anaconda`](https://store.continuum.io/cshop/anaconda/) as your python distribution. Some of the requirements will need to be installed using pip.  

## Usage instructions and command line options:
```
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

```

Sample files have been included to test if the library is functional. You can find them under `bitc/testdata`.

### Usage example:

```
python bitc_util.py mcmc bitc/testdata/sample.itc workdir -m TwoComponent -v -q bitc/testdata/sample.nitpic.dat
```
