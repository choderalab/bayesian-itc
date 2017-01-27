#!/usr/bin/python
"""
A module implementing Bayesian analysis of isothermal titration calorimetry (ITC) experiments

Written by John D. Chodera <jchodera@gmail.com>, Pande lab, Stanford, 2008.

Copyright (c) 2008 Stanford University.  All Rights Reserved.

All code in this repository is released under the GNU General Public License.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.

NOTES
* Throughout, quantities with associated units employ the pint Quantity class to store quantities
in references units.  Multiplication or division by desired units should ALWAYS be used to
store or extract quantities in the desired units.

"""
import os

from os.path import basename, splitext
import numpy
import logging
from bitc.units import ureg, Quantity
import pymc
from bitc.report import Report, plot_experiment
from bitc.parser import bitc_util_parser
from bitc.experiments import Injection, ExperimentMicroCal, ExperimentYaml
from bitc.instruments import known_instruments, Instrument
from bitc.models import RescalingStep, known_models
import sys

try:
    import seaborn
except ImportError:
    pass


def compute_normal_statistics(x_t):

    # Compute mean.
    x = x_t.mean()

    # Compute stddev.
    dx = x_t.std()

    # Compute 95% confidence interval.
    ci = 0.95
    N = x_t.size
    x_sorted = numpy.sort(x_t)
    low_index = round((0.5-ci/2.0)*N)
    high_index = round((0.5+ci/2.0)*N)
    xlow = x_sorted[low_index]
    xhigh = x_sorted[high_index]

    return [x, dx, xlow, xhigh]

validated = bitc_util_parser()

# Process the arguments
working_directory = validated['--workdir']

if not os.path.exists(working_directory):
    os.mkdir(working_directory)

os.chdir(working_directory)

# Set the logfile
if validated['--log']:
    logfile = '%(--log)s' % validated
else:
    logfile = None

# Level of verbosity in log
if validated['-v'] == 3:
    loglevel = logging.DEBUG
elif validated['-v'] == 2:
    loglevel = logging.INFO
elif validated['-v'] == 1:
    loglevel = logging.WARNING
else:
    loglevel = logging.ERROR

# Set up the logger
logging.basicConfig(format='%(levelname)s::%(module)s:L%(lineno)s\n%(message)s', level=loglevel, filename=logfile)

# Files for procesysing
filenames = validated['<datafiles>']  # .itc file to process
file_basenames, file_extensions = zip(*[splitext(basename(filename)) for filename in filenames])

# todo  fix names
if not validated['--name']:
    # Name of the experiment, and output files
    experiment_name = file_basenames[0]
else:
    experiment_name = validated['--name']

# If this is a file, it will attempt to read it like an origin file and override heats in experiment.
# todo fix this, wont work for multiple files
integrated_heats_file = validated['--heats']  # file with integrated heats

if validated['mcmc']:
    # MCMC settings
    nfit = validated['--nfit']      # number of iterations for maximum a posteriori fit
    niters = validated['--niters']  # number of iterations
    nburn = validated['--nburn']    # number of burn-in iterations
    nthin = validated['--nthin']    # thinning period
    Model = known_models[validated['--model']]  # Model type for mcmc

instruments = list()

# todo fix this flag for multiple files
if validated['--instrument']:
    # Use an instrument from the brochure
    instrument = [known_instruments[validated['--instrument']]()] * len(filenames)
else:
    # Read instrument properties from the .itc or yml file
    for index, (filename, file_extension) in enumerate(zip(filenames,file_extensions)):
        if file_extension in ['.yaml', '.yml']:
            import yaml

            with open(filename, 'r') as yamlfile:
                yamldict = yaml.load(yamlfile)
                instrument_name = yamldict['instrument']
                if instrument_name in known_instruments.keys():
                    import bitc.instruments
                    # Get the instrument class from bitc.instruments and instance it
                    instruments.append(getattr(bitc.instruments, instrument_name)())

        elif file_extension in ['.itc']:
            instruments.append(Instrument(itcfile=filename))

        else:
            raise ValueError("The instrument needs to be specified on the commandline for non-standard files")

logging.debug("Received this input from the user:")
logging.debug(str(validated))
logging.debug("Current state:")
logging.debug(str(locals()))

# Close all figure windows.
import pylab
pylab.close('all')
logging.info("Reading ITC data from %s" % filename)

# TODO make this a parallel loop?
experiments = list()
for filename, experiment_name, file_extension, instrument in zip(filenames, file_basenames, file_extensions, instruments):
    if file_extension in ['.yaml', '.yml']:
        logging.info("Experiment interpreted as literature data: %s" % experiment_name)
        experiments.append(ExperimentYaml(filename, experiment_name, instrument))
    elif file_extension in ['.itc']:
        logging.info("Experiment interpreted as raw .itc data: %s" % experiment_name)
        experiments.append(ExperimentMicroCal(filename, experiment_name, instrument))
    else:
        raise ValueError('Unknown file type. Check your file extension')

logging.debug(str(experiments))

# Only need to perform analysis for a .itc file.
for experiment, file_extension in zip(experiments, file_extensions):
    if file_extension in ['.itc']:
        experiment.fit_gaussian_process_baseline(fit_fraction=0.2, theta0=5.0, nugget=1.0, plot=True)
        #  TODO work on a markdown version for generating reports. Perhaps use sphinx
        plot_experiment(experiment_name, experiment)

# Write Origin-style integrated heats.
for experiment, experiment_name in zip(experiments, file_basenames):
    filename = experiment_name + '-integrated.txt'
    experiment.write_integrated_heats(filename)

# Override the heats if file specified.
# TODO deal with flag
# if integrated_heats_file:
#     experiment.read_integrated_heats(integrated_heats_file)

# MCMC inference
if not validated['mcmc']:
    sys.exit(0)

# Construct a Model from Experiment object.
import traceback
if validated['--model'] == 'TwoComponent':

    models = list()
    try:
        for experiment in experiments:
            models.append(Model(experiment))
    except Exception as e:
            logging.error(str(e))
            logging.error(traceback.format_exc())
            raise Exception("MCMC model could not me constructed!\n" + str(e))

    # First fit the model.
    # TODO This should be incorporated in the model. Perhaps as a model.getSampler() method?

    for model in models:
        logging.info("Fitting model...")
        map = pymc.MAP(model)
        map.fit(iterlim=nfit)
        logging.info(map)

        logging.info("Sampling...")
        model.mcmc.sample(iter=niters, burn=nburn, thin=nthin, progress_bar=True)
        #pymc.Matplot.plot(mcmc)

        # Plot individual terms.
        if sum(model.experiment.cell_concentration.values()) > Quantity('0.0 molar'):
            pymc.Matplot.plot(model.mcmc.trace('P0')[:], '%s-P0' % model.experiment.name)
        if sum(model.experiment.syringe_concentration.values()) > Quantity('0.0 molar'):
            pymc.Matplot.plot(model.mcmc.trace('Ls')[:], '%s-Ls' % model.experiment.name)
        pymc.Matplot.plot(model.mcmc.trace('DeltaG')[:], '%s-DeltaG' % model.experiment.name)
        pymc.Matplot.plot(model.mcmc.trace('DeltaH')[:], '%s-DeltaH' % model.experiment.name)
        pymc.Matplot.plot(model.mcmc.trace('DeltaH_0')[:], '%s-DeltaH_0' % model.experiment.name)
        pymc.Matplot.plot(numpy.exp(model.mcmc.trace('log_sigma')[:]), '%s-sigma' % model.experiment.name)

        #  TODO: Plot fits to enthalpogram.
        #experiment.plot(model=model, filename='%s-enthalpogram.png' %  experiment_name) # todo fix this

        # Compute confidence intervals in thermodynamic parameters.
        outfile = open('%s.confidence-intervals.out' % model.experiment.name, 'a+')
        outfile.write('%s\n' % model.experiment.name)
        [x, dx, xlow, xhigh] = compute_normal_statistics(model.mcmc.trace('DeltaG')[:] )
        outfile.write('DG:     %8.2f +- %8.2f kcal/mol     [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_normal_statistics(model.mcmc.trace('DeltaH')[:] )
        outfile.write('DH:     %8.2f +- %8.2f kcal/mol     [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_normal_statistics(model.mcmc.trace('DeltaH_0')[:] )
        outfile.write('DH0:    %8.2f +- %8.2f ucal         [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_normal_statistics(model.mcmc.trace('Ls')[:] )
        outfile.write('Ls:     %8.2f +- %8.2f uM           [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_normal_statistics(model.mcmc.trace('P0')[:] )
        outfile.write('P0:     %8.2f +- %8.2f uM           [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_normal_statistics(numpy.exp(model.mcmc.trace('log_sigma')[:]) )
        outfile.write('sigma:  %8.5f +- %8.5f ucal/s^(1/2) [%8.5f, %8.5f] \n' % (x, dx, xlow, xhigh))
        outfile.write('\n')
        outfile.close()

elif validated['--model'] == 'Competitive':
    if not validated['--receptor']:
        raise ValueError('Need to specify a receptor for Competitive model')
    else:
        receptor = validated['--receptor']
    try:
        for experiment in experiments:
            model = Model(experiments, receptor)
    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())
        raise Exception("MCMC model could not me constructed!\n" + str(e))

    logging.info("Fitting model...")
    map = pymc.MAP(model, verbose=10)
    map.fit(iterlim=nfit, verbose=10)
    logging.info(map)

    logging.info("Sampling...")
    model.mcmc.sample(iter=niters, burn=nburn, thin=nthin, progress_bar=True)
    pymc.Matplot.plot(model.mcmc, "MCMC.png")

pymc.graph.dag(model.mcmc)
