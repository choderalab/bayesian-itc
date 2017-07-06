# Bayesian ITC
[![Build Status](https://travis-ci.org/choderalab/bayesian-itc.svg)](https://travis-ci.org/choderalab/bayesian-itc)  
A python library for the Bayesian analysis of isothermal titration calorimetry experiments. This library is currently under heavy development, and API changes are frequent. Not all of the available command line options have been implemented yet.


## Manifest

* `scripts/bitc_integrate.py`, a command line utility that integrates data from .itc files using Gaussian process regression.
* `scripts/bitc_mcmc.py`, a command line utility to run MCMC using one of two available models.
* `bitc/` - the library with underlying tools.
* `scripts/bitc_util.py`, a deprecated command line utility that can be used to both integrate, and analyze data


## Requirements
Python2.7+, python3.4+ . We recommend using [`Anaconda`](https://store.continuum.io/cshop/anaconda/) as your python distribution. Some of the requirements will need to be installed using pip.
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

### Integrating ITC peaks.

The `bitc_integrate.py` script can integrate the data from .itc files using [Gaussian process regression](http://scikit-learn.org/stable/modules/gaussian_process.html). Below are the options that the program accepts.

```
Integrate ITC data using Gaussian process regression. Uses MicroCal .itc files, or custom format .yml files for analysing experiments.

Usage:
  bitc_integrate.py <datafiles>... [-w <workdir> | --workdir=<workdir>] [-v | -vv | -vvv] [options]
  bitc_integrate.py (-h | --help)
  bitc_integrate.py --license
  bitc_integrate.py --version

Options:
  -h, --help                             Show this screen
  --version                              Show version
  --license                              Show license
  -l <logfile>, --log=<logfile>          File to write logs to. Will be placed in workdir.
  -v,                                    Verbose output level. Multiple flags increase verbosity.
  <datafiles>                            Datafile(s) to perform the analysis on, .itc, .yml
  -w <workdir>, --workdir=<workdir>      Directory for output files                      [default: ./]
  -n <name>, --name=<name>               Name for the experiment. Will be used for output files. Defaults to input file name-integrated.dat.
  -i <ins>, --instrument=<ins>           The name of the instrument used for the experiment. Overrides .itc file instrument.
  -f <frac>, --fraction=<frac>           The fraction of the injection to fit, measured from the end [default: 0.2]
  --theta0=<theta0>                      The parameters in the autocorrelation model. [default: 5.0]
  --nugget=<nugget>                      Size of nugget effect to allow smooth predictions from noisy data. [default: 1.0]
  --plot                                 Generate plots of the baseline fit

```
Sample files have been included to test if the library is functional. You can find them under `bitc/testdata`.


This example command shows how to integrate a `.itc` file using default settings
```
bitc_integrate.py bitc/testdata/sample.itc -w workdir -v
```
.


### Bayesian inference using Markov chain Monte Carlo

The `bitc_mcmc.py` script runs Markov chain Monte Carlo (MCMC) on the supplied data, using a predefined model.
Below are the options that the program accepts.

```
Analyze ITC data using Markov chain Monte Carlo (MCMC). Uses MicroCal .itc files, or custom format .yml files for modeling experiments.
When running the program, you can select one of two options:

competitive
  A competitive binding model. Requires multiple experiments to be specified.

twocomponent
  A twocomponent binding model. Analyzes only a single experiment

Usage:
  bitc_mcmc.py twocomponent <datafile> <heatsfile> [-v | -vv | -vvv] [options]
  bitc_mcmc.py competitive (<datafile> <heatsfile>)... (-r <receptor> | --receptor <receptor>) [-v | -vv | -vvv] [options]
  bitc_mcmc.py (-h | --help)
  bitc_mcmc.py --license
  bitc_mcmc.py --version

Options:
  -h, --help                             Show this screen
  --version                              Show version
  --license                              Show license
  -l <logfile>, --log=<logfile>          File to write logs to. Will be placed in workdir.
  -v,                                    Verbose output level. Multiple flags increase verbosity.
  -w <workdir>, --workdir <workdir>      Directory for output files                      [default: ./]
  -r <receptor> | --receptor <receptor>  The name of the receptor for a competitive binding model.
  -n <name>, --name <name>               Name for the experiment. Will be used for output files. Defaults to inputfile name.
  -i <ins>, --instrument <ins>           The name of the instrument used for the experiment. Overrides .itc file instrument.
  --nfit=<n>                             No. of iteration for maximum a posteriori fit   [default: 20000]
  --niters=<n>                           No. of iterations for mcmc sampling             [default: 2000000]
  --nburn=<n>                            No. of Burn-in iterations for mcmc sampling     [default: 500000]
  --nthin=<n>                            Thinning period for mcmc sampling               [default: 500]
```

Sample files have been included to test if the library is functional. You can find them under `bitc/testdata`.

For example, here is how to run MCMC on an experiment using a two-component binding model:

```
python .\scripts\bitc_mcmc.py twocomponent bitc/testdata/sample.itc bitc/testdata/sample-integrated.dat
```

### Legacy examples:

Below are some examples of using the old `bitc_util.py` script.

An example for a two-component binding model
```
python scripts/bitc_util.py mcmc bitc/testdata/sample.itc -w workdir -v -m TwoComponent --niters=20000 --nburn=1000 --nthin=10 --nfit=100
```

UNDER CONSTRUCTION: Calculate the mean and standard deviation of the log likelihood of your data given previously saved samples from a posterior.

```
python scripts/bitc_util.py bitc/testdata/sample.itc -w workdir -v -m TwoComponent --calc_logp workdir/sample.h5
```

Analyze `.itc` files without mcmc

```
python scripts/bitc_util.py bitc/testdata/sample.itc bitc/testdata/sample2.itc -w workdir
```

An example for a competitive binding model.
```
bitc_util.py mcmc bitc/testdata/acetyl_pepstatin.yml testdata/kni10033.yml bitc/testdata/kni10075.yml -w workdir -v -m Competitive -r "HIV protease" --niters=20000 --nburn=1000 --nthin=10 --nfit=100
```
