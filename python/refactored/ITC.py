#!/usr/bin/python

#=============================================================================================
# A module implementing Bayesian analysis of isothermal titration calorimentry (ITC) experiments
#
# Written by John D. Chodera <jchodera@gmail.com>, Pande lab, Stanford, 2008.
#
# Copyright (c) 2008 Stanford University.  All Rights Reserved.
#
# All code in this repository is released under the GNU General Public License.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#  
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#=============================================================================================

#=============================================================================================
# NOTES
# * Throughout, quantities with associated units employ the Units.py class to store quantities
# in references units.  Multiplication or division by desired units should ALWAYS be used to
# store or extract quantities in the desired units.
#=============================================================================================

#=============================================================================================
# TODO
# * Use simtk.unit instead of Units.py?
# * Create subclass of Instrument for VP-ITC.
#=============================================================================================

#=============================================================================================
# IMPORTS
#=============================================================================================

import os
from simtk import unit
import Units
import Constants
import numpy
import scipy.stats
import pymc
from report import Report
from experiments import Injection, Experiment
from instruments import VPITC
from models import RescalingStep, TwoComponentBindingModel


#=============================================================================================
# Report class
#=============================================================================================

  
def analyze(name, experiment):
    
    # Write text-based rendering of experimental data.
    for (index, experiment) in enumerate(experiments):
        print "EXPERIMENT %d" % index
        print str(experiment)

    #=============================================================================================
    # Make plots
    #=============================================================================================
    
    # Create a LaTeX report file.
    report = Report([experiment])

    # Plot the raw measurements of differential power versus time and the enthalpogram.
    import pylab
    pylab.figure()

    fontsize = 8

    # Plot differential power versus time.
    pylab.subplot(411)

    # plot baseline fit
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / Units.s, experiment.baseline_power / (Units.ucal/Units.s), 'g-') # plot baseline fit

    # differential power
    pylab.plot(experiment.filter_period_end_time / Units.s, experiment.differential_power / (Units.ucal/Units.s), 'k.', markersize=1)
    # plot red vertical line to mark injection times
    pylab.hold(True)    
    [xmin, xmax, ymin, ymax] = pylab.axis()

    for injection in experiment.injections:
        last_index = injection['first_index'] # timepoint at start of syringe injection
        t = experiment.filter_period_end_time[last_index] / Units.s
        pylab.plot([t, t], [ymin, ymax], 'r-')    
    pylab.hold(False)
    xlabel = pylab.xlabel('time / s')
    xlabel.set_fontsize(fontsize)
    ylabel = pylab.ylabel('differential power / ucal/s')
    ylabel.set_fontsize(fontsize)

    ax = pylab.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

    # title plot
    title = pylab.title(name)
    title.set_fontsize(fontsize)
    
    # Plot enthalpogram.
    pylab.subplot(412)
    pylab.hold(True)
    for injection in experiment.injections:
        # determine initial and final samples for injection i
        first_index = injection['first_index'] # index of timepoint for first filtered differential power measurement
        last_index  = injection['last_index']  # index of timepoint for last filtered differential power measurement
        # determine time at end of injection period
        t = experiment.filter_period_end_time[last_index] / Units.s
        # plot a point there to represent total heat evolved in injection period
        y = injection['evolved_heat'] / Units.ucal
        pylab.plot([t, t], [0, y], 'k-')
        # label injection
        pylab.text(t, y, '%d' % injection['number'], fontsize=6)        
    # adjust axes to match first plot
    [xmin_new, xmax_new, ymin, ymax] = pylab.axis()
    pylab.axis([xmin, xmax, ymin, ymax])    
    pylab.hold(False)
    #pylab.title('evolved heat per injection')
    xlabel = pylab.xlabel('time / s')
    xlabel.set_fontsize(fontsize)
    ylabel = pylab.ylabel('evolved heat / ucal')
    ylabel.set_fontsize(fontsize)
    # plot zero
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / Units.s, 0.0*experiment.filter_period_end_time / (Units.ucal/Units.s), 'g-') # plot zero line


    ax = pylab.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
                    
    # Plot cell temperature.
    pylab.subplot(413)
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / Units.s, experiment.cell_temperature/Units.K - Constants.absolute_zero, 'r.', markersize=1)
    # adjust axes to match first plot
    [xmin_new, xmax_new, ymin, ymax] = pylab.axis()
    pylab.axis([xmin, xmax, ymin, ymax])    
    pylab.hold(False)
    #pylab.title('evolved heat per injection')
    xlabel = pylab.xlabel('time / s')
    xlabel.set_fontsize(fontsize)
    ylabel = pylab.ylabel('cell temperature / C')
    ylabel.set_fontsize(fontsize)

    ax = pylab.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

    # Plot adiabatic jacket temperature.
    pylab.subplot(414)
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / Units.s, experiment.jacket_temperature/Units.K - Constants.absolute_zero, 'b.', markersize=1)    
    # adjust axes to match first plot
    [xmin_new, xmax_new, ymin, ymax] = pylab.axis()
    pylab.axis([xmin, xmax, ymin, ymax])    
    pylab.hold(False)
    #pylab.title('evolved heat per injection')
    xlabel = pylab.xlabel('time / s')
    xlabel.set_fontsize(fontsize)
    ylabel = pylab.ylabel('jacket temperature / C')
    ylabel.set_fontsize(fontsize)
    
    ax = pylab.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

    # show plot
    #pylab.show()
    pylab.savefig('%s.pdf' % name, orientation='landscape', papertype='letter', format='pdf')

    return


def compute_statistics(x_t):

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

if __name__ == "__main__":
    # Run doctests.
    import doctest
    doctest.testmod()

    #=============================================================================================
    # Load experimental data.
    #=============================================================================================

    experiments = list()

    # Create a new ITC experiment object from the VP-ITC file.

    import commands
    directory = '../data/auto-iTC-200/053014/'
    filenames = commands.getoutput('ls %s/*.itc' % directory).split('\n')
    
    print "Reading these files:"
    print filenames
    for filename in filenames:
        # Close all figure windows.
        import pylab
        pylab.close('all')

        name = os.path.splitext(os.path.split(filename)[1])[0]
        print
        print "Reading ITC data from %s" % filename
        experiment = Experiment(filename)
        print experiment
        analyze(name, experiment)

        # Write Origin-style integrated heats.
        filename = name + '-integrated.txt'
        experiment.write_integrated_heats(filename)
        
        # Write baseline fit information.
        filename = name + '-baseline.png'
        experiment.plot_baseline(filename)

        # Comment out to proceed with PYMC sampling
        continue # DEBUG        

        #=============================================================================================
        # MCMC inference
        #=============================================================================================

        # Construct a Model from Experiment object.
        import traceback
        try:
            model = buildModel(experiment)
        except Exception as e:
            print str(e)
            print traceback.format_exc()
            stop
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
        
        if (experiment.cell_concentration > 0.0):
            mcmc.use_step_method(pymc.Metropolis, model['P0'])
        if (experiment.syringe_concentration > 0.0):
            mcmc.use_step_method(pymc.Metropolis, model['Ls'])
        
        if (experiment.cell_concentration > 0.0) and (experiment.syringe_concentration > 0.0):
            mcmc.use_step_method(RescalingStep, [model['Ls'], model['P0'], model['DeltaH'], model['DeltaG'], model['DeltaH_0']], model['beta'])
        
        print "Sampling..."
        mcmc.sample(iter=niters, burn=nburn, thin=nthin, progress_bar=True)
        #pymc.Matplot.plot(mcmc)

        # Plot individual terms.
        if (experiment.cell_concentration > 0.0):
            pymc.Matplot.plot(mcmc.trace('P0')[:] / Units.uM, '%s-P0' % name)
        if (experiment.syringe_concentration > 0.0):
            pymc.Matplot.plot(mcmc.trace('Ls')[:] / Units.uM, '%s-Ls' % name)
        pymc.Matplot.plot(mcmc.trace('DeltaG')[:] / (Units.kcal/Units.mol), '%s-DeltaG' % name)
        pymc.Matplot.plot(mcmc.trace('DeltaH')[:] / (Units.kcal/Units.mol), '%s-DeltaH' % name)
        pymc.Matplot.plot(mcmc.trace('DeltaH_0')[:] / (Units.ucal/Units.ul), '%s-DeltaH_0' % name)
        pymc.Matplot.plot(numpy.exp(mcmc.trace('log_sigma')[:]) * Units.cal / Units.second**0.5, '%s-sigma' % name)
        
        # TODO: Plot fits to enthalpogram.
        experiment.plot(model=mcmc, filename='sampl4/%s-enthalpogram.png' % name)
        
        # Compute confidence intervals in thermodynamic parameters.
        outfile = open('sampl4/confidence-intervals.out','a')
        outfile.write('%s\n' % name)        
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('DeltaG')[:] / (Units.kcal/Units.mol))         
        outfile.write('DG:     %8.2f +- %8.2f kcal/mol     [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('DeltaH')[:] / (Units.kcal/Units.mol))         
        outfile.write('DH:     %8.2f +- %8.2f kcal/mol     [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('DeltaH_0')[:] / (Units.ucal/Units.ul))         
        outfile.write('DH0:    %8.2f +- %8.2f ucal         [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('Ls')[:] / Units.uM)         
        outfile.write('Ls:     %8.2f +- %8.2f uM           [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('P0')[:] / Units.uM)         
        outfile.write('P0:     %8.2f +- %8.2f uM           [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(numpy.exp(mcmc.trace('log_sigma')[:]) * Units.cal / Units.second**0.5)
        outfile.write('sigma:  %8.5f +- %8.5f ucal/s^(1/2) [%8.5f, %8.5f] \n' % (x, dx, xlow, xhigh))        
        outfile.write('\n')
        outfile.close()

