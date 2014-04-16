#!/usr/bin/env python

"""
A test of pymc for ITC.

"""

#=============================================================================================
# IMPORTS
#=============================================================================================

import numpy
import pymc
import copy

import scipy.optimize
import scipy.integrate

from math import sqrt, exp, log

#=============================================================================================
# Physical constants
#=============================================================================================

Na = 6.02214179e23 # Avogadro's number (number/mol)
kB = Na * 1.3806504e-23 / 4184.0 # Boltzmann constant (kcal/mol/K)
C0 = 1.0 # standard concentration (M)

#=============================================================================================
# Rescaling StepMethod for sampling correlated changes in ligand and receptor concentration
#=============================================================================================

class RescalingStep(pymc.StepMethod):
   def __init__(self, dictionary, beta, max_scale=1.03, verbose=0, interval=100):
      """
      dictionary (dict) - must contain dictionary of objects for Ls, P0, DeltaH, DeltaG
      """

      # Verbosity flag
      self.verbose = verbose

      # Store stochastics.
      self.dictionary = dictionary
      
      # Initialize superclass.
      pymc.StepMethod.__init__(self, dictionary.values(), verbose)

      self._id = 'RescalingMetropolis_'+'_'.join([p.__name__ for p in self.stochastics])
      # State variables used to restore the state in a later session.
      self._state += ['max_scale', '_current_iter', 'interval']

      self.max_scale = max_scale
      self.beta = beta

      self._current_iter = 0
      self.interval = interval

      self.accepted = 0
      self.rejected = 0

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
      self.dictionary['Ls'].value = self.dictionary['Ls'].value * factor
      self.dictionary['P0'].value = self.dictionary['P0'].value * factor
      self.dictionary['DeltaH'].value = self.dictionary['DeltaH'].value / factor
      self.dictionary['DeltaG'].value = self.dictionary['DeltaG'].value + (1./self.beta) * numpy.log(factor);

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
# Binding models
#=============================================================================================

class BindingModel(object):
    """
    Abstract base class for reaction models.

    """

    def __init__(self):
        pass
    
#=============================================================================================
# Two-component binding model
#=============================================================================================

class TwoComponentBindingModel(BindingModel):
   def __init__(self, Ls_stated, P0_stated, q_n_observed, DeltaVn, temperature, V0):
      
      # Determine number of observations.
      self.N = q_n_observed.size

      # Store injection volumes
      if not numpy.iterable(DeltaVn):
         self.DeltaVn = numpy.ones([self.N], numpy.float64) * DeltaVn
      else:
         self.DeltaVn = numpy.array(DeltaVn)

      # Store calorimeter properties.
      self.V0 = V0

      # Store temperature.
      self.temperature = temperature # temperature (kelvin)
      self.beta = 1.0 / (kB * temperature) # inverse temperature 1/(kcal/mol)      

      # Compute uncertainties in stated concentrations.
      dP0 = 0.10 * P0_stated # uncertainty in protein stated concentration (M) - 10% error
      dLs = 0.10 * Ls_stated # uncertainty in ligand stated concentration (M) - 10% error

      # Determine guesses for initial values
      log_sigma_guess = log(q_n[-4:].std()) # cal/injection
      DeltaG_guess = -8.3 # kcal/mol
      DeltaH_guess = -12.0 # kcal/mol
      DeltaH_0_guess = q_n[-1] # cal/injection
      
      # Determine min and max range for log_sigma
      log_sigma_min = log_sigma_guess - 10
      log_sigma_max = log_sigma_guess + 5

      # Determine range for priors for thermodynamic parameters.
      DeltaG_min = -40. # (kcal/mol)
      DeltaG_max = +40. # (kcal/mol)
      DeltaH_min = -100. # (kcal/mol)
      DeltaH_max = +100. # (kcal/mol)
      heat_interval = q_n.max() - q_n.min()
      DeltaH_0_min = q_n.min() - heat_interval # (cal/mol)
      DeltaH_0_max = q_n.max() + heat_interval # (cal/mol)
      
      # Define priors for concentrations.
      #self.P0 = pymc.Normal('P0', mu=P0_stated, tau=1.0/dP0**2, value=P0_stated)
      #self.Ls = pymc.Normal('Ls', mu=Ls_stated, tau=1.0/dLs**2, value=Ls_stated)
      self.P0 = pymc.Lognormal('P0', mu=log(P0_stated), tau=1.0/log(1.0+(dP0/P0_stated)**2), value=P0_stated)
      self.Ls = pymc.Lognormal('Ls', mu=log(Ls_stated), tau=1.0/log(1.0+(dLs/Ls_stated)**2), value=Ls_stated)

      # Define priors for thermodynamic quantities.
      self.log_sigma = pymc.Uniform('log_sigma', lower=log_sigma_min, upper=log_sigma_max, value=log_sigma_guess)
      self.DeltaG = pymc.Uniform('DeltaG', lower=DeltaG_min, upper=DeltaG_max, value=DeltaG_guess)
      self.DeltaH = pymc.Uniform('DeltaH', lower=DeltaH_min, upper=DeltaH_max, value=DeltaH_guess)
      self.DeltaH_0 = pymc.Uniform('DeltaH_0', lower=DeltaH_0_min, upper=DeltaH_0_max, value=DeltaH_0_guess)

      # Deterministic functions.
      q_n_model = pymc.Lambda('q_n_model', lambda P0=self.P0, Ls=self.Ls, DeltaG=self.DeltaG, DeltaH=self.DeltaH, DeltaH_0=self.DeltaH_0, q_n_obs=self.DeltaH_0 :
                              self.expected_injection_heats(P0, Ls, DeltaG, DeltaH, DeltaH_0, q_n_obs))
      tau = pymc.Lambda('tau', lambda log_sigma=self.log_sigma : self.tau(log_sigma))

      # Define observed data.
      self.q_n_obs = pymc.Normal('q_n', mu=q_n_model, tau=tau, observed=True, value=q_n_observed)

      # Create sampler.
      mcmc = pymc.MCMC(self, db='ram')
      mcmc.use_step_method(pymc.Metropolis, self.DeltaG)
      mcmc.use_step_method(pymc.Metropolis, self.DeltaH)
      mcmc.use_step_method(pymc.Metropolis, self.DeltaH_0)
      mcmc.use_step_method(pymc.Metropolis, self.P0)
      mcmc.use_step_method(pymc.Metropolis, self.Ls)
      mcmc.use_step_method(RescalingStep, { 'Ls' : self.Ls, 'P0' : self.P0, 'DeltaH' : self.DeltaH, 'DeltaG' : self.DeltaG }, self.beta)
      self.mcmc = mcmc
      return
        
   def expected_injection_heats(self, P0, Ls, DeltaG, DeltaH, DeltaH_0, q_n_obs):
      """
      Expected heats of injection for two-component binding model.
      
      ARGUMENTS
      
      DeltaG - free energy of binding (kcal/mol)
      DeltaH - enthalpy of binding (kcal/mol)
      DeltaH_0 - heat of injection (cal/mol)
      
      """
      
      debug = False
      
      Kd = exp(self.beta * DeltaG) * C0 # dissociation constant (M)
      N = self.N
   
      # Compute complex concentrations.
      Pn = numpy.zeros([N], numpy.float64) # Pn[n] is the protein concentration in sample cell after n injections (M)
      Ln = numpy.zeros([N], numpy.float64) # Ln[n] is the ligand concentration in sample cell after n injections (M)
      PLn = numpy.zeros([N], numpy.float64) # PLn[n] is the complex concentration in sample cell after n injections (M)
      dcum = 1.0 # cumulative dilution factor (dimensionless)
      for n in range(N):
         # Instantaneous injection model (perfusion)
         # TODO: Allow injection volume to vary for each injection.
         d = 1.0 - (self.DeltaVn[n] / self.V0) # dilution factor for this injection (dimensionless)
         dcum *= d # cumulative dilution factor
         P = self.V0 * P0 * dcum # total quantity of protein in sample cell after n injections (mol)
         L = self.V0 * Ls * (1. - dcum) # total quantity of ligand in sample cell after n injections (mol)
         PLn[n] = 0.5/self.V0 * ((P + L + Kd*self.V0) - sqrt((P + L + Kd*self.V0)**2 - 4*P*L));  # complex concentration (M)
         Pn[n] = P/self.V0 - PLn[n]; # free protein concentration in sample cell after n injections (M)
         Ln[n] = L/self.V0 - PLn[n]; # free ligand concentration in sample cell after n injections (M)
         
      # Compute expected injection heats.
      q_n = numpy.zeros([N], numpy.float64) # q_n_model[n] is the expected heat from injection n
      # Instantaneous injection model (perfusion)
      q_n[0] = (1000.0*DeltaH) * self.V0 * PLn[0] + DeltaH_0 # first injection
      for n in range(1,N):
         d = 1.0 - (self.DeltaVn[n] / self.V0) # dilution factor (dimensionless)         
         q_n[n] = (1000.0*DeltaH) * self.V0 * (PLn[n] - d*PLn[n-1]) + DeltaH_0 # subsequent injections

      # Debug output
      if debug:
         print "DeltaG = %6.1f kcal/mol ; DeltaH = %6.1f kcal/mol ; DeltaH_0 = %6.1f ucal/injection" % (DeltaG, DeltaH, DeltaH_0*1e6)
         for n in range(N):
            print "%6.1f" % (PLn[n]*1e6),
         print ""
         for n in range(N):
            print "%6.1f" % (q_n[n]*1e6),
         print ""
         for n in range(N):
            print "%6.1f" % (q_n_obs[n]*1e6),
         print ""
         print ""
    
      return q_n

   def tau(self, log_sigma):
      """
      Injection heat measurement precision.
      
      """
      return exp(-2.0*log_sigma)

#=============================================================================================
# Titration experiment
#=============================================================================================

class Experiment(object):
   """
   A calorimetry experiment.

   """
   
   def __init__(self, sample_cell_concentrations, syringe_concentrations, injection_volumes, injection_heats, temperature):
      """
      Initialize a calorimetry experiment.
      
      ARGUMENTS
      
      sample_cell_concentrations (dict) - a dictionary of initial concentrations of each species in sample cell (M)
      syringe_concentrations (dict) - a dictionary of initial concentrations of each species in the syringe
      injection_volumes (list or numpy array of N floats) - injection volumes in L
      injection_heats (list or numpy array of N floats) - injection heats in cal/injection
      temperature (float) - temperature (K)

      EXAMPLES

      ABRF-MIRG'02 group 10

      >>> V0 = 1.4301e-3 # volume of calorimeter sample cell listed in manual (L)
      >>> V0 = V0 - 0.044e-3 # sample cell volume after Tellinghuisen volume correction for VP-ITC (L)
      >>> DeltaV = 8.e-6 # injection volume (L)
      >>> P0_stated = 32.e-6 # protein stated concentration (M)
      >>> Ls_stated = 384.e-6 # ligand syringe stated concentration (M)
      >>> injection_heats = numpy.array([-13.343, -13.417, -13.279, -13.199, -13.118, -12.781, -12.600, -12.124, -11.633, -10.921, -10.009, -8.810, -7.661, -6.272, -5.163, -4.228, -3.519, -3.055, -2.599, -2.512, -2.197, -2.096, -2.087, -1.959, -1.776, -1.879, -1.894, -1.813, -1.740, -1.810]) * DeltaV * Ls_stated * 1000.0 # integrated heats of injection (cal/injection)
      >>> temperature = 298.15
      >>> experiment = Experiment({'CA II' : P0_stated}, {'CBS' : Ls_stated}, injection_volumes, injection_heats, temperature)

      """

      # TODO: Do sanity checking to make sure number of injections matches up, etc.
      
      self.sample_cell_concentrations = sample_cell_concentrations
      self.syringe_concentrations = syringe_concentrations
      self.injection_volumes = numpy.array(injection_volumes)
      self.observed_injection_heats = numpy.array(injection_heats)
      self.temperature = temperature

      return

#=============================================================================================
# Competitive binding model
#=============================================================================================

class CompetitiveBindingModel(BindingModel):
   """
   Competitive binding model.
   
   """
   
   def __init__(self, experiments, receptor, V0, concentration_uncertainty=0.10, verbose=False):
      """
      ARGUMENTS

      experiments (list of Experiment) -
      receptor (string) - name of receptor species
      V0 (float) - calorimeter sample cell volume

      OPTIONAL ARGUMENTS
      
      concentration_uncertainty (float) - relative uncertainty in concentrations

      """

      self.verbose = verbose

      # Store temperature.
      # NOTE: Right now, there can only be one.
      self.temperature = experiments[0].temperature # temperature (kelvin)
      self.beta = 1.0 / (kB * self.temperature) # inverse temperature 1/(kcal/mol)      
      
      # Store copy of experiments.
      self.experiments = copy.deepcopy(experiments)
      if verbose: print "%d experiments" % len(self.experiments)

      # Store sample cell volume.
      self.V0 = V0
      
      # Store the name of the receptor.
      self.receptor = receptor
      if verbose: print "species '%s' will be treated as receptor" % self.receptor

      # Make a list of names of all molecular species.
      self.species = set() # all molecular species
      for experiment in experiments:
         self.species.update( experiment.sample_cell_concentrations.keys() )
         self.species.update( experiment.syringe_concentrations.keys() )
      if verbose: print "species: ", self.species
            
      # Make a list of all ligands.
      self.ligands = copy.deepcopy(self.species)
      self.ligands.remove(receptor)
      if verbose: print "ligands: ", self.ligands

      # Create a list of all stochastics.
      self.stochastics = list()

      # Create a prior for thermodynamic parameters of binding for each ligand-receptor interaction.
      DeltaG_min = -40. # (kcal/mol)
      DeltaG_max = +40. # (kcal/mol)
      DeltaH_min = -100. # (kcal/mol)
      DeltaH_max = +100. # (kcal/mol)
      self.thermodynamic_parameters = dict()
      for ligand in self.ligands:
         name = "DeltaG of %s * %s" % (self.receptor, ligand)
         x = pymc.Uniform(name, lower=DeltaG_min, upper=DeltaG_max, value=0.0)
         self.thermodynamic_parameters[name] = x
         self.stochastics.append(x)
         name = "DeltaH of %s * %s" % (self.receptor, ligand)
         x = pymc.Uniform(name, lower=DeltaH_min, upper=DeltaH_max, value=0.0)
         self.thermodynamic_parameters[name] = x
         self.stochastics.append(x)         
      if verbose:
         print "thermodynamic parameters:"
         print self.thermodynamic_parameters

      # DEBUG: Set initial thermodynamic parameters to literature values.
      self.thermodynamic_parameters["DeltaG of HIV protease * acetyl pepstatin"].value = -9.0
      self.thermodynamic_parameters["DeltaH of HIV protease * acetyl pepstatin"].value = +6.8
      self.thermodynamic_parameters["DeltaG of HIV protease * KNI-10033"].value = -14.870
      self.thermodynamic_parameters["DeltaH of HIV protease * KNI-10033"].value = -8.200
      self.thermodynamic_parameters["DeltaG of HIV protease * KNI-10075"].value = -14.620
      self.thermodynamic_parameters["DeltaH of HIV protease * KNI-10075"].value = -12.120
      
      # Determine min and max range for log_sigma (log of instrument heat measurement error)
      # TODO: This should depend on a number of factors, like integration time, heat signal, etc.?
      sigma_guess = 0.0
      for experiment in self.experiments:
         sigma_guess += experiment.observed_injection_heats[-4:].std()
      sigma_guess /= float(len(self.experiments))
      log_sigma_guess = log(sigma_guess)
      log_sigma_min = log_sigma_guess - 10
      log_sigma_max = log_sigma_guess + 5
      self.log_sigma = pymc.Uniform('log_sigma', lower=log_sigma_min, upper=log_sigma_max, value=log_sigma_guess)
      self.stochastics.append(self.log_sigma)
      tau = pymc.Lambda('tau', lambda log_sigma=self.log_sigma : exp(-2.0 * log_sigma))
      self.stochastics.append(tau)

      # Define priors for unknowns for each experiment.
      for (index, experiment) in enumerate(self.experiments):
         # Number of observations
         experiment.ninjections = experiment.observed_injection_heats.size
         if verbose: print "Experiment %d has %d injections" % (index, experiment.ninjections)

         # Heat of dilution / mixing
         # We allow the heat of dilution/mixing to range in observed range of heats, plus a larger margin of the range of oberved heats.
         max_heat = experiment.observed_injection_heats.max()
         min_heat = experiment.observed_injection_heats.min()
         heat_interval = max_heat - min_heat
         last_heat = experiment.observed_injection_heats[-1] # last injection heat provides a good initial guess for heat of dilution/mixing
         experiment.DeltaH_0 = pymc.Uniform("DeltaH_0 for experiment %d" % index, lower=min_heat-heat_interval, upper=max_heat+heat_interval, value=last_heat)
         self.stochastics.append(experiment.DeltaH_0)

         # True concentrations
         experiment.true_sample_cell_concentrations = dict()
         for species, concentration in experiment.sample_cell_concentrations.iteritems():
            x = pymc.Lognormal("initial sample cell concentration of %s in experiment %d" % (species, index),
                               mu=log(concentration), tau=1.0/log(1.0+concentration_uncertainty**2),
                               value=concentration)
            experiment.true_sample_cell_concentrations[species] = x
            self.stochastics.append(x)
            
         experiment.true_syringe_concentrations = dict()
         for species, concentration in experiment.syringe_concentrations.iteritems():
            x = pymc.Lognormal("initial syringe concentration of %s in experiment %d" % (species, index),
                               mu=log(concentration), tau=1.0/log(1.0+concentration_uncertainty**2),
                               value=concentration)
            experiment.true_syringe_concentrations[species] = x
            self.stochastics.append(x)
            
         # Add species not explicitly listed with zero concentration.
         for species in self.species:
            if species not in experiment.true_sample_cell_concentrations:
               experiment.true_sample_cell_concentrations[species] = 0.0
            if species not in experiment.true_syringe_concentrations:
               experiment.true_syringe_concentrations[species] = 0.0
         
         # True injection heats
         experiment.true_injection_heats = pymc.Lambda("true injection heats for experiment %d" % index,
                                                       lambda experiment=experiment,
                                                              sample_cell_concentrations=experiment.true_sample_cell_concentrations,
                                                              syringe_concentrations=experiment.true_syringe_concentrations,
                                                              DeltaH_0=experiment.DeltaH_0,
                                                              thermodynamic_parameters=self.thermodynamic_parameters :
                                                       self.expected_injection_heats(experiment, sample_cell_concentrations, syringe_concentrations, DeltaH_0, thermodynamic_parameters))
         self.stochastics.append(experiment.true_injection_heats)

         # Observed injection heats
         experiment.observation = pymc.Normal("observed injection heats for experiment %d" % index,
                                              mu=experiment.true_injection_heats, tau=tau,
                                              observed=True, value=experiment.observed_injection_heats)
         self.stochastics.append(experiment.observation)

      # Create sampler.
      print "Creating sampler..."
      mcmc = pymc.MCMC(self.stochastics, db='ram')
      #db = pymc.database.pickle.load('MCMC.pickle') # DEBUG
      #mcmc = pymc.MCMC(self.stochastics, db=db)
      for stochastic in self.stochastics:
         print stochastic
         try:
            mcmc.use_step_method(pymc.Metropolis, stochastic)
         except:
            pass
      mcmc.use_step_method(RescalingStep, { 'Ls' : self.experiments[0].true_syringe_concentrations['acetyl pepstatin'],
                                            'P0' : self.experiments[0].true_sample_cell_concentrations['HIV protease'],
                                            'DeltaH' : self.thermodynamic_parameters['DeltaH of HIV protease * acetyl pepstatin'],
                                            'DeltaG' : self.thermodynamic_parameters['DeltaG of HIV protease * acetyl pepstatin'] }, self.beta)

      mcmc.use_step_method(RescalingStep, { 'Ls' : self.experiments[1].true_syringe_concentrations['KNI-10033'],
                                            'P0' : self.experiments[1].true_sample_cell_concentrations['HIV protease'],
                                            'DeltaH' : self.thermodynamic_parameters['DeltaH of HIV protease * KNI-10033'],
                                            'DeltaG' : self.thermodynamic_parameters['DeltaG of HIV protease * KNI-10033'] }, self.beta)      

      mcmc.use_step_method(RescalingStep, { 'Ls' : self.experiments[2].true_syringe_concentrations['KNI-10075'],
                                            'P0' : self.experiments[2].true_sample_cell_concentrations['HIV protease'],
                                            'DeltaH' : self.thermodynamic_parameters['DeltaH of HIV protease * KNI-10075'],
                                            'DeltaG' : self.thermodynamic_parameters['DeltaG of HIV protease * KNI-10075'] }, self.beta)      

      self.mcmc = mcmc

   def equilibrium_concentrations(self, Ka_n, C0_R, C0_Ln, V, c0=None):
      """
      Compute the equilibrium concentrations of each complex species for N ligands competitively binding to a receptor.

      ARGUMENTS

      Ka_n (numpy N-array of float) - Ka_n[n] is the association constant for receptor and ligand species n (1/M)
      x_R (float) - the total number of moles of receptor in the sample volume
      x_n (numpy N-array of float) - x_n[n] is the total number of moles of ligand species n in the sample volume
      V (float) - the total sample volume (L)
      
      RETURNS

      C_n (numpy N-array of float) - C_n[n] is the concentration of complex of receptor with ligand species n

      EXAMPLES

      >>> V = 1.4303e-3 # volume (L)
      >>> x_R = V * 510.e-3 # receptor
      >>> x_Ln = numpy.array([V * 8.6e-6, 200.e-6 * 55.e-6]) # ligands
      >>> Ka_n = numpy.array([1./(400.e-9), 1./(2.e-11)]) # association constants
      >>> C_PLn = equilibrium_concentrations(Ka_n, x_R, x_Ln, V)

      NOTES
      
      Each complex concentration C_n must obey the relation
      
      Ka_n[n] = C_RLn[n] / (C_R * C_Ln[n])           for n = 1..N
      
      with conservation of mass constraints
      
      V * (C_Ln[n] + C_RLn[n]) = x_Ln[n]             for n = 1..N
      
      and
      
      V * (C_R + C_RLn[:].sum()) = x_R
      
      along with the constraints
      
      0 <= V * C_RLn[n] <= min(x_Ln[n], x_R)         for n = 1..N
      V * C_RLn[:].sum() <= x_R
      
      We can rearrange these expressions to give
      
      V * C_R * C_Ln[n] * Ka_n[n] - V * C_RLn[n] = 0
      
      and eliminate C_Ln[n] and C_R to give
      
      V * (x_R/V - C_RLn[:].sum()) * (x_Ln[n]/V - C_RLn[n]) * Ka_n[n] - V * C_RLn[n] = 0    for n = 1..N
      
      """

      x_R = C0_R * V
      x_Ln = C0_Ln * V
      
      nspecies = Ka_n.size
      #print "x_R = ", x_R
      #print "x_Ln = ", x_Ln
      #print "x_Ln / V = ", x_Ln / V
      #print "Ka_n = ", Ka_n

      # Define optimization functions
      def func(C_RLn):
         f_n = V * (x_R/V - C_RLn[:].sum()) * (x_Ln[:]/V - C_RLn[:]) * Ka_n[:] - V * C_RLn[:]
         #print "f_n = ", f_n
         return f_n
      
      def fprime(C_RLn):
         nspecies = C_RLn.size
         G_nm = numpy.zeros([nspecies,nspecies], numpy.float64) # G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]
         for n in range(nspecies):
            G_nm[n,:] = - V * (x_Ln[:]/V - C_RLn[:]) * Ka_n[:]
            G_nm[n,n] -= V * (Ka_n[n] * (x_R/V - C_RLn[:].sum()) + 1.0)
         return G_nm

      def sfunc(s):
         #print "s = ", s
         f_n = V * (x_R/V - (s[:]**2).sum()) * (x_Ln[:]/V - s[:]**2) * Ka_n[:] - V * s[:]**2
         #print "f_n = ", f_n
         return f_n
      
      def sfprime(s):
         nspecies = s.size
         G_nm = numpy.zeros([nspecies,nspecies], numpy.float64) # G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]
         for n in range(nspecies):
            G_nm[n,:] = - V * (x_Ln[:]/V - s[:]**2) * Ka_n[:] 
            G_nm[n,n] -= V * (Ka_n[n] * (x_R/V - (s[:]**2).sum()) + 1.0)
            G_nm[n,:] *= 2. * s[n]
         return G_nm

      # Allocate storage for complexes
      # Compute equilibrium concentrations.
      #x0 = numpy.zeros([nspecies], numpy.float64)
      #x0 = (x_Ln / V).copy()
      #x = scipy.optimize.fsolve(func, x0, fprime=fprime)
      #C_RLn = x
      
      #x0 = numpy.sqrt(x_Ln / V).copy()
      #x = scipy.optimize.fsolve(sfunc, x0, fprime=sfprime)         
      #C_RLn = x**2

      def objective(x):
         f_n = func(x)
         G_nm = fprime(x)

         obj = (f_n**2).sum()
         grad = 0.0 * f_n
         for n in range(f_n.size):
            grad += 2 * f_n[n] * G_nm[n,:]

         return (obj, grad)
         
      #x0 = numpy.zeros([nspecies], numpy.float64)      
      #bounds = list()
      #for n in range(nspecies):
      #   m = min(C0_R, C0_Ln[n])
      #   bounds.append( (0., m) )
      #[x, a, b] = scipy.optimize.fmin_l_bfgs_b(objective, x0, bounds=bounds)
      #C_RLn = x

      def ode(c_n, t, Ka_n, x_Ln, x_R):
         dc_n = - c_n[:] + Ka_n[:] * (x_Ln[:]/V - c_n[:]) * (x_R/V - c_n[:].sum())
         return dc_n
      
      def odegrad(c_n, t, Ka_n, x_Ln, x_R):
         N = c_n.size
         d2c = numpy.zeros([N,N], numpy.float64)
         for n in range(N):
            d2c[n,:] = -Ka_n[n] * (x_Ln[n]/V - c_n[n])
            d2c[n,n] += -(Ka_n[n] * (x_R/V - c_n[:].sum()) + 1.0)
         return d2c

      #if c0 is None: c0 = numpy.zeros([nspecies], numpy.float64)
      #maxtime = 100.0 * (x_R/V) / Ka_n.max()
      #time = [0, maxtime / 2.0, maxtime]
      #c = scipy.integrate.odeint(ode, c0, time, Dfun=odegrad, args=(Ka_n, x_Ln, x_R))
      #C_RLn = c[-1,:]

      #c = numpy.zeros([nspecies], numpy.float64)
      #maxtime = 1.0 / Ka_n.min()
      #maxtime = 1.0 / ((x_R/V) * Ka_n.min())
      #maxtime = 1.0
      #time = [0, maxtime]
      #c = scipy.optimize.fsolve(ode, c, fprime=odegrad, args=(0.0, Ka_n, x_Ln, x_R), xtol=1.0e-6)
      #c = scipy.integrate.odeint(ode, c, time, Dfun=odegrad, args=(Ka_n, x_Ln, x_R), mxstep=50000)
      #c = c[-1,:]
      #C_RLn = c

      #print "C_RLn = ", C_RLn 
      #print ""

      c = numpy.zeros([nspecies], numpy.float64)
      sorted_indices = numpy.argsort(-x_Ln)
      for n in range(nspecies):
         indices = sorted_indices[0:n+1]
         #c[indices] = scipy.optimize.fsolve(ode, c[indices], fprime=odegrad, args=(0.0, Ka_n[indices], x_Ln[indices], x_R), xtol=1.0e-6, warning=False)
         c[indices] = scipy.optimize.fsolve(ode, c[indices], fprime=odegrad, args=(0.0, Ka_n[indices], x_Ln[indices], x_R), xtol=1.0e-6)
      C_RLn = c
      
      return C_RLn
      
   def expected_injection_heats(self, experiment, true_sample_cell_concentrations, true_syringe_concentrations, DeltaH_0, thermodynamic_parameters):
      """
      Expected heats of injection for two-component binding model.

      TODO

      - Make experiment a dict, or somehow tell it how to replace members of 'experiment'?
      
      ARGUMENTS
      
      sample_cell_concentrations (dict of floats) - concentrations[species] is the initial concentration of species in sample cell, or zero if absent (M)
      syringe_concentrations (dict of floats) - concentrations[species] is the initial concentration of species in sample cell, or zero if absent (M)
      thermodynamic_parameters (dict of floats) - thermodynamic_parameters[parameter] is the value of thermodynamic parameter (kcal/mol)
        e.g. for parameter 'DeltaG of receptor * species'
      V_n (numpy array of floats) - V_n[n] is injection volume of injection n (L)
      
      """
      
      debug = False

      # Number of ligand species
      nspecies = len(self.ligands)

      # Compute association constants for receptor and each ligand species.
      DeltaG_n = numpy.zeros([nspecies], numpy.float64) # 
      for (n, ligand) in enumerate(self.ligands):
         name = "DeltaG of %s * %s" % (self.receptor, ligand) # determine name of free energy of binding for this ligand
         DeltaG_n[n] = thermodynamic_parameters[name] # retrieve free energy of binding

      Ka_n = numpy.exp(-self.beta * DeltaG_n[:]) / C0 # compute association constant (1/M)

      # Compute the quantity of each species in the sample cell after each injection.
      # NOTE: These quantities are correct for a perfusion-type model.  This would be modified for a cumulative model.
      x_Ri = numpy.zeros([experiment.ninjections], numpy.float64) # x_Ri[i] is the number of moles of receptor in sample cell after injection i
      x_Lin = numpy.zeros([experiment.ninjections, nspecies], numpy.float64) # x_Lin[i,n] is the number of moles of ligand n in sample cell after injection i
      dcum = 1.0 # cumulative dilution factor
      for i in range(experiment.ninjections):
         d = 1.0 - (experiment.injection_volumes[i] / self.V0) # dilution factor (dimensionless)
         dcum *= d # cumulative dilution factor (dimensionless)
         x_Ri[i] = true_sample_cell_concentrations[self.receptor] * dcum + true_syringe_concentrations[self.receptor] * (1.0 - dcum)
         for (n, ligand) in enumerate(self.ligands):
            x_Lin[i,n] = true_sample_cell_concentrations[ligand] * dcum + true_syringe_concentrations[ligand] * (1.0 - dcum)
      # DEBUG
      #print "true_sample_cell_concentrations: ", true_sample_cell_concentrations
      #print "true_syringe_concentrations: ", true_syringe_concentrations
      #print "x_R in mol:"
      #print x_Ri
      #print "x_Lin in mol: "
      #print x_Lin 

      # Solve for initial concentration.
      x_R0 = true_sample_cell_concentrations[self.receptor]      
      x_L0n = numpy.zeros([nspecies], numpy.float64)
      C_RL0n = numpy.zeros([nspecies], numpy.float64)       
      for (n, ligand) in enumerate(self.ligands):
         x_L0n[n] = true_sample_cell_concentrations[ligand]
      C_RL0n[:] = self.equilibrium_concentrations(Ka_n, x_R0, x_L0n[:], self.V0)
      #print "C_RL0n in uM:"
      #print C_RL0n * 1.e6
            
      # Compute complex concentrations after each injection.
      # NOTE: The total cell volume would be modified for a cumulative model.
      C_RLin = numpy.zeros([experiment.ninjections,nspecies], numpy.float64) # C_RLin[i,n] is the concentration of complex RLn[n] after injection i
      for i in range(experiment.ninjections):
         C_RLin[i,:] = self.equilibrium_concentrations(Ka_n, x_Ri[i], x_Lin[i,:], self.V0)
      #print "C_RLin in uM:"
      #print C_RLin * 1e6

      # Compile a list of thermodynamic parameters.
      DeltaH_n = numpy.zeros([nspecies], numpy.float64) # DeltaH_n[n] is the enthalpy of association of ligand species n
      for (n, ligand) in enumerate(self.ligands):
         name = "DeltaH of %s * %s" % (self.receptor, ligand)
         DeltaH_n[n] = thermodynamic_parameters[name]

      # Compute expected injection heats.
      # NOTE: This is for an instantaneous injection / perfusion model.
      q_n = DeltaH_0 * numpy.ones([experiment.ninjections], numpy.float64) # q_n_model[n] is the expected heat from injection n
      d = 1.0 - (experiment.injection_volumes[0] / self.V0) # dilution factor (dimensionless)
      for n in range(nspecies):      
         q_n[0] += (1000.0*DeltaH_n[n]) * V0 * (C_RLin[0,n] - d*C_RL0n[n])  # first injection
      for i in range(1,experiment.ninjections):
         d = 1.0 - (experiment.injection_volumes[i] / self.V0) # dilution factor (dimensionless)         
         for n in range(nspecies):
            q_n[i] += (1000.0*DeltaH_n[n]) * V0 * (C_RLin[i,n] - d*C_RLin[i-1,n]) # subsequent injections

      # Debug output
      debug = False
      if debug:
         print experiment.name
         print "DeltaG = ", DeltaG_n
         print "DeltaH = ", DeltaH_n
         print "DeltaH_0 = ", DeltaH_0
         print "model: ",
         for heat in q_n:
            print "%6.1f" % (heat*1e6),
         print ""
         print "obs  : ",         
         for heat in experiment.observed_injection_heats:
            print "%6.1f" % (heat*1e6),
         print ""
         print ""

      return q_n

#=============================================================================================
# MAIN AND TESTS
#=============================================================================================

if __name__ == "__main__":
    # Run doctests.
    import doctest
    doctest.testmod()

    #=============================================================================================
    # ABRF-MIRG'02 dataset 10
    #=============================================================================================

    V0 = 1.4301e-3 # volume of calorimeter sample cell (L)
    V0 = V0 - 0.044e-3 # Tellinghuisen volume correction for VP-ITC (L)
    DeltaV = 8.e-6 # injection volume (L)
    P0_stated = 32.e-6 # protein stated concentration (M)
    Ls_stated = 384.e-6 # ligand syringe stated concentration (M)
    temperature = 298.15 # temperature (K)
    q_n = numpy.array([
       -13.343, -13.417, -13.279, -13.199, -13.118, -12.781, -12.600, -12.124, -11.633, -10.921, -10.009, -8.810, 
       -7.661, -6.272, -5.163, -4.228, -3.519, -3.055, -2.599, -2.512, -2.197, -2.096, -2.087, -1.959, -1.776, -1.879,
       -1.894, -1.813, -1.740, -1.810]) # integrated heats of injection (kcal/mol injectant)
    q_n = q_n * DeltaV * Ls_stated * 1000.0 # convert injection heats to cal/injection
    beta = 1.0 / (kB * temperature) # inverse temperature 1/(kcal/mol)
    
    #=============================================================================================
    # Erensto Freire data for HIV protease inhibitors KNI-10033 and KNI-10075
    #=============================================================================================

    experiments = list()
    
    #
    # acetyl pepstatin
    #
    
    V0 = 1.4301e-3 # volume of calorimeter sample cell listed in manual (L)
    V0 = V0 - 0.044e-3; # Tellinghuisen volume correction for VP-ITC (L)
    sample_cell_concentrations = {'HIV protease' : 20.e-6}
    syringe_concentrations = {'acetyl pepstatin' : 300.e-6}
    Ls_stated = 300.e-6 # acetyl pepstatin concentration (M)
    DeltaV = 10.e-6 # injection volume (L)
    #injection_heats = numpy.array([1.6, 6.696, 6.695, 6.698, 6.617, 6.464, 6.336, 6.184, 5.652, 4.336, 2.970, 1.709, 0.947, 0.643, 0.441, 0.264, 0.269, 0.214, 0.138, 0.113, 0.062, 0.088, 0.016, 0.063, 0.012]) * 1000.0 * Ls_stated * DeltaV # first had to be estimated because it was omitted
    injection_heats = numpy.array([6.696, 6.695, 6.698, 6.617, 6.464, 6.336, 6.184, 5.652, 4.336, 2.970, 1.709, 0.947, 0.643, 0.441, 0.264, 0.269, 0.214, 0.138, 0.113, 0.062, 0.088, 0.016, 0.063, 0.012]) * 1000.0 * Ls_stated * DeltaV # first injection omitted
    N = len(injection_heats) # number of injections
    injection_volumes = 10.e-6 * numpy.ones([N], numpy.float64) # injection volumes (L)
    temperature = 298.15 # temperature (K)
    experiment = Experiment(sample_cell_concentrations, syringe_concentrations, injection_volumes, injection_heats, temperature)
    experiment.name = "acetyl pepstatin binding to HIV protease"
    experiment.reference = "Nature Protocols 1:186, 2006; Fig. 1, left panel"
    experiments.append(experiment)
    
    #
    # KNI-10033
    #

    sample_cell_concentrations = {'HIV protease' : 8.6e-6, 'acetyl pepstatin' : 510.e-6} # initial sample cell concentrations (M)
    syringe_concentrations = {'KNI-10033' : 46.e-6}
    Ls_stated = 46.e-6 # KNI-10033 syringe concentration (M)
    DeltaV = 10.e-6 # injection volume (L)
    #injection_heats = numpy.array([-12.106, -19.889, -19.896, -19.889, -19.797, -20.182, -19.889, -19.880, -19.849, -19.985, -19.716, -19.790, -19.654, -19.745, -19.622, -19.457, -19.378, -18.908, -17.964, -16.490, -12.273, -7.370, -4.649, -3.626, -3.203, -2.987, -2.841, -2.906, -2.796, -2.927]) * DeltaV * Ls_stated * 1000.0
    injection_heats = numpy.array([-19.889, -19.896, -19.889, -19.797, -20.182, -19.889, -19.880, -19.849, -19.985, -19.716, -19.790, -19.654, -19.745, -19.622, -19.457, -19.378, -18.908, -17.964, -16.490, -12.273, -7.370, -4.649, -3.626, -3.203, -2.987, -2.841, -2.906, -2.796, -2.927]) * DeltaV * Ls_stated * 1000.0
    N = len(injection_heats) # number of injections
    injection_volumes = 10.e-6 * numpy.ones([N], numpy.float64) # injection volumes (L)
    experiment = Experiment(sample_cell_concentrations, syringe_concentrations, injection_volumes, injection_heats, temperature)
    experiment.name = "KNI-10033 displacement of acetyl pepstatin binding to HIV protease"
    experiments.append(experiment)
    
    #
    # KNI-10075
    #
    
    sample_cell_concentrations = {'HIV protease' : 8.8e-6, 'acetyl pepstatin' : 510.e-6} # initial sample cell concentrations (M)
    syringe_concentrations = {'KNI-10075' : 55.e-6}
    Ls_stated = 55.e-6 # KNI-10033 syringe concentration (M)
    DeltaV = 10.e-6 # injection volume (L)
    injection_heats = numpy.array([-21.012, -22.716, -22.863, -22.632, -22.480, -22.236, -22.314, -22.569, -22.231, -22.529, -22.529, -21.773, -21.866, -21.412, -20.810, -18.664, -14.339, -11.028, -5.219, -3.612, -3.611, -3.389, -3.354, -3.122, -3.049, -3.083, -3.253, -3.089, -3.146, -3.252]) * DeltaV * Ls_stated * 1000.0
    N = len(injection_heats) # number of injections
    injection_volumes = 10.e-6 * numpy.ones([N], numpy.float64) # injection volumes (L)
    experiment = Experiment(sample_cell_concentrations, syringe_concentrations, injection_volumes, injection_heats, temperature)
    experiment.name = "KNI-10075 displacement of acetyl pepstatin binding to HIV protease"
    experiments.append(experiment)
   
    #=============================================================================================
    # MCMC inference
    #=============================================================================================

    #model = TwoComponentBindingModel(Ls_stated, P0_stated, q_n, DeltaV, temperature, V0)    
    model = CompetitiveBindingModel(experiments, 'HIV protease', V0, verbose=True)
    
    niters = 10000 # number of iterations
    nburn = 1000 # number of burn-in iterations
    nthin = 1 # thinning period
    
    model.mcmc.sample(iter=niters, burn=nburn, thin=nthin, progress_bar=True)
    pymc.Matplot.plot(model.mcmc)


