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



#=============================================================================================
# Model
#=============================================================================================
def buildModel(experiment):
    """
    Create a PyMC model from one or more Experiment objects.

    ARGUMENTS
        experiment (Experiment) - the experiment to analyze

    RETURNS
        model (pymc.model) - a PyMC model
    """

    # Determine number of injections.
    N = experiment.number_of_injections

    # Physical constants
    Na = 6.02214179e23 # Avogadro's number (number/mol)
    kB = Na * 1.3806504e-23 / 4184.0 * Units.kcal / Units.mol / Units.K # Boltzmann constant (kcal/mol/K)
    C0 = 1.0 * Units.M # standard concentration (M)

    temperature = 298.15 * Units.K# temperature (K)
    beta = 1.0 / (kB * temperature) # inverse temperature 1/(kcal/mol)

    # Store sample cell volume and injection volume.
    Ls_stated = experiment.syringe_concentration # syringe concentration (M)
    P0_stated = experiment.cell_concentration # cell concentration (M)
    V0 = experiment.cell_volume # cell volume (L)

    V0 = V0 - 0.044*Units.ml # Tellinghuisen volume correction for VP-ITC (L) # not sure for iTC-200
    
    # Uncertainties in concentrations.
    dP0 = 0.10 * P0_stated # uncertainty in protein stated concentration (M) - 10% error 
    dLs = 0.10 * Ls_stated # uncertainty in ligand stated concentration (M) - 10% error 

    # For CAII:CBS
    dP0 = 0.10 * P0_stated # uncertainty in protein stated concentration (M) 
    dLs = 0.01 * Ls_stated # uncertainty in ligand stated concentration (M) 
    
    # Extract evolved injection heats.
    injection_heats = numpy.zeros([N], numpy.float64)
    for (n, injection) in enumerate(experiment.injections):
        injection_heats[n] = injection['evolved_heat']
        
    print "injection heats"
    print injection_heats / Units.ucal

    # Determine guesses for initial values
    nlast = 4 # number of injections to use
    duration_n = numpy.zeros([N], numpy.float64) # duration_n[n] is the duration of injection n
    for n in range(N):
        duration_n[n] = experiment.injections[n]['duration']    
    sigma2 = injection_heats[N-nlast:N].var() / duration_n[N-nlast:N].sum()
    log_sigma_guess = numpy.log(numpy.sqrt(sigma2 / Units.cal**2 * Units.second)) # cal/s # TODO: Use std of individual filtered measurements instead

    try:
        DeltaG_guess = -5.0 * Units.kcal/Units.mol
        print "Ls_stated = %f uM" % (Ls_stated / Units.uM)
        print "final injection volume = %f uL" % (experiment.injections[N-1]['volume'] / Units.ul)
        DeltaH_0_guess = - injection_heats[N-1] / (Ls_stated * experiment.injections[N-1]['volume'])
        DeltaH_guess = - (injection_heats[0] / (Ls_stated * experiment.injections[0]['volume']) - DeltaH_0_guess)
    except:
        DeltaG_guess = 0.0
        DeltaH_0_guess = 0.0
        DeltaH_guess = 0.0

    # DEBUG
    print ""
    print ""
    print "INITIAL GUESS"
    print "DeltaH_0_guess = %.3f ucal/uL" % (DeltaH_0_guess / (Units.ucal/Units.ul))
    first_index = 0
    last_index = experiment.injections[0]['first_index']
    filter_time = experiment.injections[0]['filter_period']
    print "Computing sigma2"
    sigma2 = (experiment.differential_power[first_index:last_index] - experiment.baseline_power[first_index:last_index]).var() / filter_time
    print sigma2
    log_sigma_guess = numpy.log(numpy.sqrt(sigma2 / Units.cal**2 * Units.second)) # cal/s # TODO: Use std of individual filtered measurements instead
    print log_sigma_guess
    print ""
    print ""
    print ""
    print ""

    # Determine min and max range for log_sigma
    log_sigma_min = log_sigma_guess - 10.0
    log_sigma_max = log_sigma_guess + 10.0

    # Determine range for priors for thermodynamic parameters.
    DeltaG_min = -40. * Units.kcal/Units.mol # 
    DeltaG_max = +40. * Units.kcal/Units.mol # 
    DeltaH_min = -100. * Units.kcal/Units.mol # 
    DeltaH_max = +100. * Units.kcal/Units.mol # 
    heat_interval = injection_heats.max() - injection_heats.min()
    DeltaH_0_min = injection_heats.min() - heat_interval # 
    DeltaH_0_max = injection_heats.max() + heat_interval # 

    # Create model.
    model = dict()

    # Define constants.
    model['beta'] = beta

    # Define priors.
    @pymc.deterministic
    def zero():
        return 0.0

    if (P0_stated > 0.0):
        model['P0'] = pymc.Lognormal('P0', mu=numpy.log(P0_stated), tau=1.0/numpy.log(1.0+(dP0/P0_stated)**2), value=P0_stated) # true cell concentration (M)
    else:
        model['P0'] = zero

    if (Ls_stated > 0.0):
        model['Ls'] = pymc.Lognormal('Ls', mu=numpy.log(Ls_stated), tau=1.0/numpy.log(1.0+(dLs/Ls_stated)**2), value=Ls_stated) # true syringe concentration (M)
    else:
        model['Ls'] = zero

    model['log_sigma'] = pymc.Uniform('log_sigma', lower=log_sigma_min, upper=log_sigma_max, value=log_sigma_guess) # natural logarithm of std dev of integrated injection heat divided by 1 cal
    model['DeltaG'] = pymc.Uniform('DeltaG', lower=DeltaG_min, upper=DeltaG_max, value=DeltaG_guess) # DeltaG (kcal/mol)
    model['DeltaH'] = pymc.Uniform('DeltaH', lower=DeltaH_min, upper=DeltaH_max, value=DeltaH_guess) # DeltaH (kcal/mol)
    model['DeltaH_0'] = pymc.Uniform('DeltaH_0', lower=DeltaH_0_min, upper=DeltaH_0_max, value=DeltaH_0_guess) # heat of mixing and mechanical injection (cal/volume)

    @pymc.deterministic
    def zero():
        return 0.0

    @pymc.deterministic
    def expected_injection_heats(DeltaG=model['DeltaG'], DeltaH=model['DeltaH'], DeltaH_0=model['DeltaH_0'], P0=model['P0'], Ls=model['Ls']):
        """
        Expected heats of injection for two-component binding model.

        ARGUMENTS

        DeltaG - free energy of binding (kcal/mol)
        DeltaH - enthalpy of binding (kcal/mol)
        DeltaH_0 - heat of injection (cal/mol)
        """

        debug = False

        Kd = numpy.exp(beta * DeltaG) * C0 # dissociation constant (M)

        # Compute dilution factor for instantaneous injection model (perfusion).
        d_n = numpy.zeros([N], numpy.float64) # d_n[n] is the dilution factor for injection n
        dcum_n = numpy.ones([N], numpy.float64) # dcum_n[n] is the cumulative dilution factor for injection n
        if debug: print "%5s %24s %24s" % ('n', 'd_n', 'dcum_n')
        for n in range(N):
            d_n[n] = 1.0 - (experiment.injections[n]['volume'] / V0) # dimensionless dilution factor for injection n
            dcum_n[n:] *= d_n[n]
            if debug: print "%5d %24f %24f" % (n, d_n[n], dcum_n[n])
        if debug: print ""
        
        # Compute complex concentrations.
        Pn = numpy.zeros([N], numpy.float64) # Pn[n] is the protein concentration in sample cell after n injections (M)
        Ln = numpy.zeros([N], numpy.float64) # Ln[n] is the ligand concentration in sample cell after n injections (M)
        PLn = numpy.zeros([N], numpy.float64) # PLn[n] is the complex concentration in sample cell after n injections (M)
        if debug: print "%5s %24s %24s %24s %24s %24s" % ('n', 'P (umol)', 'L (umol)', 'Pn (uM)', 'Ln (uM)', 'PLn (uM)')
        for n in range(N):
            # Instantaneous injection model (perfusion)
            P = V0 * P0 * dcum_n[n] # total quantity of protein in sample cell after n injections (mol)
            L = V0 * Ls * (1. - dcum_n[n]) # total quantity of ligand in sample cell after n injections (mol)
            PLn[n] = 0.5/V0 * ((P + L + Kd*V0) - numpy.sqrt((P + L + Kd*V0)**2 - 4*P*L));  # complex concentration (M)
            Pn[n] = P/V0 - PLn[n]; # free protein concentration in sample cell after n injections (M)
            Ln[n] = L/V0 - PLn[n]; # free ligand concentration in sample cell after n injections (M)
            if debug: print "%5d %24f %24f %24f %24f %24f" % (n, P / Units.umol, L / Units.umol, Pn[n] / Units.uM, Ln[n] / Units.uM, PLn[n] / Units.uM)
            
        # Compute expected injection heats.
        q_n = numpy.zeros([N], numpy.float64) # q_n_model[n] is the expected heat from injection n
        q_n[0] = (-DeltaH) * V0 * (PLn[0] - d_n[0]*0.0) + (-DeltaH_0) * experiment.injections[0]['volume'] # first injection
        for n in range(1,N):
            q_n[n] = (-DeltaH) * V0 * (PLn[n] - d_n[n]*PLn[n-1]) + (-DeltaH_0) * experiment.injections[n]['volume'] # subsequent injections

        # Debug output
        if debug:
            print "DeltaG = %6.1f kcal/mol ; DeltaH = %6.1f kcal/mol ; DeltaH_0 = %6.1f ucal/injection" % (DeltaG / (Units.kcal/Units.mol), DeltaH / (Units.kcal/Units.mol), DeltaH_0 / Units.ucal)
            for n in range(N):
                print "%6.1f" % (PLn[n] / Units.uM),
            print ""
            for n in range(N):
                print "%6.1f" % (q_n[n] / Units.ucal),
            print ""
            for n in range(N):
                print "%6.1f" % (injection_heats[n] / Units.ucal),
            print ""
            print ""

        return q_n

    @pymc.deterministic
    def tau(log_sigma=model['log_sigma']):
        """
        Injection heat measurement precision.
        
        """
        return numpy.exp(-2.0*log_sigma)/(Units.cal**2 / Units.second) * numpy.sqrt(duration_n)

    # Define observed data.
    print N
    print expected_injection_heats
    print tau
    print injection_heats
    #model['q_n'] = pymc.Normal('q_n', size=[N], mu=expected_injection_heats, tau=tau, observed=True, value=injection_heats)
    model['q_n'] = pymc.Normal('q_n', mu=expected_injection_heats, tau=tau, observed=True, value=injection_heats)

    return model              

#=============================================================================================
# Efficient step method
#=============================================================================================

class RescalingStep(pymc.StepMethod):
   def __init__(self, stochastic, beta, max_scale=1.03, verbose=0, interval=100):
      # Verbosity flag
      self.verbose = verbose

      # Store stochastics.
      if not numpy.iterable(stochastic):
         stochastic = [stochastic]
      # Initialize superclass.
      pymc.StepMethod.__init__(self, stochastic, verbose)

      self._id = 'RescalingMetropolis_'+'_'.join([p.__name__ for p in self.stochastics])
      # State variables used to restore the state in a later session.
      self._state += ['max_scale', '_current_iter', 'interval']

      self.max_scale = max_scale
      self.beta = beta

      self._current_iter = 0
      self.interval = interval

      # Keep track of number of accepted moves.
      self.accepted = 0
      self.rejected = 0

      # Store dict of stochastic names.
      self.stochastic_index = dict()
      for p in self.stochastics:
         self.stochastic_index[str(p)] = p

      # Report
      if self.verbose:
         print "Initialization..."
         print "max_scale: ", self.max_scale

   def propose(self):
      # Choose trial scaling factor or its inverse with equal probability, so that proposal move is symmetric.
      factor = (self.max_scale - 1) * numpy.random.rand() + 1;
      if (numpy.random.rand() < 0.5): 
         factor = 1./factor;

      # Scale thermodynamic parameters and variables with this factor.   
      self.stochastic_index['Ls'].value = self.stochastic_index['Ls'].value * factor
      self.stochastic_index['P0'].value = self.stochastic_index['P0'].value * factor
      self.stochastic_index['DeltaH'].value = self.stochastic_index['DeltaH'].value / factor
      self.stochastic_index['DeltaG'].value = self.stochastic_index['DeltaG'].value + (1./self.beta) * numpy.log(factor);
      self.stochastic_index['DeltaH_0'].value = self.stochastic_index['DeltaH_0'].value

      return                                                                    

   def step(self):
      # Probability and likelihood for stochastic's current value:
      logp = sum([stochastic.logp for stochastic in self.stochastics])
      loglike = self.loglike
      if self.verbose > 1:
         print 'Current likelihood: ', logp+loglike
         
      # Sample a candidate value
      self.propose()

      # Metropolis acception/rejection test
      accept = False
      try:
         # Probability and likelihood for stochastic's proposed value:
         logp_p = sum([stochastic.logp for stochastic in self.stochastics])
         loglike_p = self.loglike
         if self.verbose > 2:
            print 'Current likelihood: ', logp+loglike
            
         if numpy.log(numpy.random.rand()) < logp_p + loglike_p - logp - loglike:
            accept = True
            self.accepted += 1
            if self.verbose > 2:
               print 'Accepted'
         else:
            self.rejected += 1
            if self.verbose > 2:
               print 'Rejected'
      except pymc.ZeroProbability:
         self.rejected += 1
         logp_p = None
         loglike_p = None
         if self.verbose > 2:
            print 'Rejected with ZeroProbability error.'

      if (not self._current_iter % self.interval) and self.verbose > 1:
         print "Step ", self._current_iter
         print "\tLogprobability (current, proposed): ", logp, logp_p
         print "\tloglike (current, proposed):      : ", loglike, loglike_p
         for stochastic in self.stochastics:
            print "\t", stochastic.__name__, stochastic.last_value, stochastic.value
         if accept:
            print "\tAccepted\t*******\n"
         else:
            print "\tRejected\n"
         print "\tAcceptance ratio: ", self.accepted/(self.accepted+self.rejected)
         
      if not accept:
         self.reject()

      self._current_iter += 1
      
      return

   @classmethod
   def competence(self, stochastic):
      if str(stochastic) in ['DeltaG', 'DeltaH', 'DeltaH_0', 'Ls', 'P0']:
         return 1
      return 0
         
   def reject(self):
      for stochastic in self.stochastics:
         # stochastic.value = stochastic.last_value
         stochastic.revert()

   def tune(self, verbose):
      return False                                                                                                                                                                                                                                                                   

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

