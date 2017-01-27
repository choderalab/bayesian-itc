#!/usr/bin/python
"""
This script integrates an ITC experiment using Gaussian process regression for baseline fitting.
"""
import logging
import os
from os.path import basename, splitext

from bitc.experiments import ExperimentMicroCal, ExperimentYaml
from bitc.instruments import known_instruments, Instrument
from bitc.parser import integrate_parser
from bitc.report import plot_experiment

user_input = integrate_parser()

# Process the arguments
working_directory = user_input['--workdir']

if not os.path.exists(working_directory):
    os.mkdir(working_directory)

os.chdir(working_directory)

# Set the logfile
if user_input['--log']:
    logfile = '%(--log)s' % user_input
else:
    logfile = None

# Level of verbosity in log
if user_input['-v'] == 3:
    loglevel = logging.DEBUG
elif user_input['-v'] == 2:
    loglevel = logging.INFO
elif user_input['-v'] == 1:
    loglevel = logging.WARNING
else:
    loglevel = logging.ERROR

# Set up the logger
logging.basicConfig(format='%(levelname)s::%(module)s:L%(lineno)s\n%(message)s', level=loglevel, filename=logfile)

# Files for procesysing
filenames = user_input['<datafiles>']  # .itc file to process
file_basenames, file_extensions = zip(*[splitext(basename(filename)) for filename in filenames])


if not user_input['--name']:
    # Name of the experiment, and output files
    experiment_name = file_basenames[0]
else:
    experiment_name = user_input['--name']

instruments = list()

# todo fix this flag for multiple files
if user_input['--instrument']:
    # Use an instrument from the brochure
    instrument = [known_instruments[user_input['--instrument']]()] * len(filenames)
else:
    # Read instrument properties from the .itc or yml file
    for index, (filename, file_extension) in enumerate(zip(filenames, file_extensions)):
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
logging.debug(str(user_input))
logging.debug("Current state:")
logging.debug(str(locals()))

# Close all figure windows.
import pylab

pylab.close('all')
logging.info("Reading ITC data from %s" % filename)

# TODO make this a parallel loop?
experiments = list()
for filename, experiment_name, file_extension, instrument in zip(filenames, file_basenames, file_extensions,
                                                                 instruments):
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
        #  TODO work on a markdown version for generating reports. Perhaps use sphinx
        experiment.fit_gaussian_process_baseline(fit_fraction=user_input['--fraction'], theta0=user_input['--theta0'],
                                                 nugget=user_input['--nugget'], plot=user_input['--plot'])
        experiment.integrate_heat()

        if user_input['--plot']:
            plot_experiment(experiment_name, experiment)

# Write Origin-style integrated heats.
for experiment, experiment_name in zip(experiments, file_basenames):
    filename = experiment_name + '-integrated.dat'
    experiment.write_integrated_heats(filename)
