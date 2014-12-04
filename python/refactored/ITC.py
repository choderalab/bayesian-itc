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

from os.path import basename, splitext
import numpy
import logging
from units import ureg, Quantity
import pymc
from report import Report, analyze
from parser import parser
from experiments import Injection, Experiment
from instruments import known_instruments, Instrument
from models import RescalingStep, known_models
import sys

# TODO Find out if this is still used
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

try:
    validated = parser('mcmc ../../data/SAMPL4/CB7/082213b15.itc workdir -q heats.txt -m TwoComponent -vvv -n test.exp')

    # Arguments to variables
    # Set the logfile
    if validated['--log']:
        logfile = '%(<workdir>)s/%(--log)s' % validated
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

    # Files for processing
    filename = validated['<datafile>']  # .itc file to process
    working_directory = validated['<workdir>']
    integrated_heats_file = validated['--heats']  # file with integrated heats

    if not validated['--name']:
        # Name of the experiment, and output files
        experiment_name, file_extension = splitext(basename(filename))
    else:
        experiment_name = validated['--name']

    if validated['mcmc']:
        # MCMC settings
        niters = validated['--niters']  # number of iterations
        nburn = validated['--nburn']    # number of burn-in iterations
        nthin = validated['--nthin']    # thinning period
        Model = known_models[validated['--model']]  # Model type for mcmc

    if validated['--instrument']:
        # Use an instrument from the brochure
        instrument = known_instruments[validated['--instrument']]()
    else:
        # Read instrument properties from the .itc file
        instrument = Instrument(itcfile=filename)

    logging.debug("Received this input from the user:")
    logging.debug(str(validated))
    logging.debug("Current state:")
    logging.debug(str(locals()))

    # TODO update code below this point

    # Close all figure windows.
    import pylab
    pylab.close('all')
    logging.info("Reading ITC data from %s" % filename)

    experiment = Experiment(filename)
    logging.debug(str(experiment))
    #  TODO work on a markdown version for generating reports. Perhaps use sphinx
    analyze(experiment_name, experiment)
    # Write Origin-style integrated heats.
    filename = experiment_name + '-integrated.txt'
    experiment.write_integrated_heats(filename)

    # Write baseline fit information.
    filename = experiment_name + '-baseline.png'
    experiment.plot_baseline(filename)

    # MCMC inference
    if not validated['mcmc']:
        sys.exit(0)

    # Construct a Model from Experiment object.
    import traceback
    try:

        model = Model(experiment, instrument)
    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())
        raise ValueError("MCMC model could not me constructed!\n" + e)

    # First fit the model.
    # TODO This should be incorporated in the model. Perhaps as a model.getSampler() method?
    print "Fitting model..."
    map = pymc.MAP(model)
    map.fit(iterlim=20000)
    print map

    mcmc = pymc.MCMC(model, db='ram')

    mcmc.use_step_method(pymc.Metropolis, model['DeltaG'])
    mcmc.use_step_method(pymc.Metropolis, model['DeltaH'])
    mcmc.use_step_method(pymc.Metropolis, model['DeltaH_0'])
    mcmc.use_step_method(pymc.Metropolis, model['log_sigma'])

    if experiment.cell_concentration > 0.0:
        mcmc.use_step_method(pymc.Metropolis, model['P0'])
    if experiment.syringe_concentration > 0.0:
        mcmc.use_step_method(pymc.Metropolis, model['Ls'])

    if (experiment.cell_concentration > 0.0) and (experiment.syringe_concentration > 0.0):
        mcmc.use_step_method(RescalingStep, [model['Ls'], model['P0'], model['DeltaH'], model['DeltaG'], model['DeltaH_0']], model['beta'])

    print "Sampling..."
    mcmc.sample(iter=niters, burn=nburn, thin=nthin, progress_bar=True)
    #pymc.Matplot.plot(mcmc)

    # Plot individual terms.
    if experiment.cell_concentration > 0.0:
        pymc.Matplot.plot(mcmc.trace('P0')[:] / (ureg.millimole/ ureg.liter), '%s-P0' % experiment_name)
    if experiment.syringe_concentration > 0.0:
        pymc.Matplot.plot(mcmc.trace('Ls')[:] / (ureg.micromole/ ureg.liter), '%s-Ls' % experiment_name)
    pymc.Matplot.plot(mcmc.trace('DeltaG')[:] / (ureg.kilocalorie/ureg.mole), '%s-DeltaG' % experiment_name)
    pymc.Matplot.plot(mcmc.trace('DeltaH')[:] / (ureg.kilocalorie/ureg.mole), '%s-DeltaH' % experiment_name)
    pymc.Matplot.plot(mcmc.trace('DeltaH_0')[:] / (ureg.microcalorie/ureg.microliter), '%s-DeltaH_0' % experiment_name)
    pymc.Matplot.plot(numpy.exp(mcmc.trace('log_sigma')[:]) * ureg.calorie / ureg.second**0.5, '%s-sigma' % experiment_name)

    #  TODO: Plot fits to enthalpogram.
    experiment.plot(model=mcmc, filename='sampl4/%s-enthalpogram.png' % experiment_name)

    # Compute confidence intervals in thermodynamic parameters.
    outfile = open('sampl4/confidence-intervals.out','a')
    outfile.write('%s\n' % experiment_name)
    [x, dx, xlow, xhigh] = compute_normal_statistics(mcmc.trace('DeltaG')[:] / (ureg.kilocalorie/ureg.mole))
    outfile.write('DG:     %8.2f +- %8.2f kcal/mol     [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
    [x, dx, xlow, xhigh] = compute_normal_statistics(mcmc.trace('DeltaH')[:] / (ureg.kilocalorie/ureg.mole))
    outfile.write('DH:     %8.2f +- %8.2f kcal/mol     [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
    [x, dx, xlow, xhigh] = compute_normal_statistics(mcmc.trace('DeltaH_0')[:] / (ureg.microcalorie/ureg.microliter))
    outfile.write('DH0:    %8.2f +- %8.2f ucal         [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
    [x, dx, xlow, xhigh] = compute_normal_statistics(mcmc.trace('Ls')[:] / (ureg.micromole/ ureg.liter))
    outfile.write('Ls:     %8.2f +- %8.2f uM           [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
    [x, dx, xlow, xhigh] = compute_normal_statistics(mcmc.trace('P0')[:] / (ureg.micromole / ureg.liter))
    outfile.write('P0:     %8.2f +- %8.2f uM           [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
    [x, dx, xlow, xhigh] = compute_normal_statistics(numpy.exp(mcmc.trace('log_sigma')[:]) * ureg.calorie / ureg.second**0.5)
    outfile.write('sigma:  %8.5f +- %8.5f ucal/s^(1/2) [%8.5f, %8.5f] \n' % (x, dx, xlow, xhigh))
    outfile.write('\n')
    outfile.close()

except ValueError:
    # review Always return successful if the error is in the model definition (helps with debugging)
    sys.exit(0)
