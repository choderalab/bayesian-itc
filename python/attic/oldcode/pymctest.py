#!/usr/bin/env python

"""
A test of pymc for ITC.

"""

#=============================================================================================
# IMPORTS
#=============================================================================================

import numpy
import pymc

#=============================================================================================
# Model
#=============================================================================================

import pymcmodel as model

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
#=============================================================================================
# MCMC inference
#=============================================================================================

niters = 20000 # number of iterations
nburn = 5000 # number of burn-in iterations
nthin = 5 # thinning period

#mcmc = pymc.MCMC(model, db='pickle')
#mcmc = pymc.MCMC(model, db='sqlite')
mcmc = pymc.MCMC(model, db='hdf5')
#mcmc = pymc.MCMC(model, db='ram')

mcmc.use_step_method(pymc.Metropolis, model.DeltaG)
mcmc.use_step_method(pymc.Metropolis, model.DeltaH)
mcmc.use_step_method(pymc.Metropolis, model.DeltaH_0)
mcmc.use_step_method(pymc.Metropolis, model.P0)
mcmc.use_step_method(pymc.Metropolis, model.Ls)

mcmc.use_step_method(RescalingStep, [model.Ls, model.P0, model.DeltaH, model.DeltaG, model.DeltaH_0], model.beta)

mcmc.sample(iter=niters, burn=nburn, thin=nthin)
pymc.Matplot.plot(mcmc)
