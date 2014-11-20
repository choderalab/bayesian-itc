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

import numpy
import os
import logging
from units import ureg, Quantity
import scipy.stats
import pymc
from report import Report, analyze
from experiments import Injection, Experiment
from instruments import VPITC
from models import RescalingStep, TwoComponentBindingModel

# debug level logging at the moment
logging.basicConfig(format='%(levelname)s::%(pathname)s:L%(lineno)s\n%(message)s', level=logging.DEBUG)
# Use logger with name of module
logger = logging.getLogger(__name__)

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

#=============================================================================================
# MAIN AND TESTS
#=============================================================================================

__usage__ = """
Bayesian analysis of Microcal iTC200 data.

Usage:
  ITC.py analyze <file> [-q <file> | --heats=<file>]
  ITC.py analyze mcmc <file> [-q <file> | --heats=<file>] [-m <model> | --model=<model>] [options]
  ITC.py (-h | --help)
  ITC.py --license
  ITC.py --version

Options:
  -h, --help                    Show this screen
  --version                     Show version
  --license                     Show license
  -q <file>, --heats=<file>     Integrated heats (q_n) from file
  -m <model>, --model=<model>   Model to use for mcmc sampling                  [default: TwoComponent]
  --niters=<n>                  No. of iterations for mcmc sampling             [default: 2000000]
  --nburn=<n>                   No. of Burn-in iterations for mcmc sampling     [default: 500000]
  --nthin=<n>                   Thinning period for mcmc sampling               [default: 250]
"""

if __name__ == "__main__":
    from docopt import docopt
    arguments = docopt(__usage__, version='ITC.py development version, early pre-alpha')
    print(arguments)
    exit(0)
    vpitc = VPITC()
    experiments = list()

    # Obtain list of .itc data files to be processed
    from glob import glob
    from os.path import basename, splitext

    directory = '../../data/SAMPL4/CB7'
    filenames = glob('%s/*.itc' % directory)
    
    logger.info("Reading these files: \n" +
                ",\n".join(filenames))
    # Create Experiment instance from .itc files and analyze the data
    for filename in filenames:
        # Close all figure windows.
        import pylab
        pylab.close('all')

        experiment_name, file_extension = splitext(basename(filename))

        logger.info("Reading ITC data from %s" % filename)

        experiment = Experiment(filename)
        logger.debug(str(experiment))

        analyze(experiment_name, experiment)
        # Write Origin-style integrated heats.
        filename = experiment_name + '-integrated.txt'
        experiment.write_integrated_heats(filename)

        # Write baseline fit information.
        filename = experiment_name + '-baseline.png'
        experiment.plot_baseline(filename)

        #=============================================================================================
        # MCMC inference
        #=============================================================================================

        # Construct a Model from Experiment object.
        import traceback
        try:
            from models import TwoComponentBindingModel
            model = TwoComponentBindingModel(experiment, vpitc)
        except Exception as e:
            logger.error(str(e))
            logger.error(traceback.format_exc())
            # raise Exception(e)
            continue

        # First fit the model.
        print "Fitting model..."
        map = pymc.MAP(model)
        map.fit(iterlim=20000)
        print map

        niters = 2000000 # number of iterations
        nburn  = 500000 # number of burn-in iterations
        nthin  = 250 # thinning period
        
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
        
        # TODO: Plot fits to enthalpogram.
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

