#!/usr/bin/env python

"""
A test of pymc for ITC.

"""

#=============================================================================================
# IMPORTS
#=============================================================================================

import numpy
import pymc

from math import sqrt, exp, log

#=============================================================================================
# Physical constants
#=============================================================================================

Na = 6.02214179e23 # Avogadro's number (number/mol)
kB = Na * 1.3806504e-23 / 4184 # Boltzmann constant (kcal/mol/K)
C0 = 1.0 # standard concentration (M)

#=============================================================================================
# Experimental parameters and data
#=============================================================================================

# ABRF-MIRG'02 dataset 10
V0 = 1.4301e-3 # volume of calorimeter sample cell (L)
V0 = V0 - 0.044e-3 # Tellinghuisen volume correction for VP-ITC (L)
DeltaV = 8e-6 # injection volume (L)
P0_stated = 32e-6 # protein stated concentration (M)
Ls_stated = 384e-6 # ligand syringe stated concentration (M)
temperature = 298.15 # temperature (K)
dP0 = 0.1 * P0_stated # uncertainty in protein stated concentration (M)
dLs = 0.001 * Ls_stated # uncertainty in ligand stated concentration (M)
q_n = numpy.array([
    -13.343, -13.417, -13.279, -13.199, -13.118, -12.781, -12.600, -12.124, -11.633, -10.921, -10.009, -8.810, 
    -7.661, -6.272, -5.163, -4.228, -3.519, -3.055, -2.599, -2.512, -2.197, -2.096, -2.087, -1.959, -1.776, -1.879,
    -1.894, -1.813, -1.740, -1.810]) # integrated heats of injection (cal/mol injectant)

# Proces experimental parameters
q_n = q_n * DeltaV * Ls_stated * 1000.0 # convert injection heats to cal/injection
N = q_n.size
beta = 1.0 / (kB * temperature) # inverse temperature 1/(kcal/mol)

#=============================================================================================
# Model
#=============================================================================================

class TwoComponentBindingModel(object):

    @pymc.deterministic
    def expected_injection_heats(self, DeltaG=self.DeltaG, DeltaH=self.DeltaH, DeltaH_0=self.DeltaH_0):
        """
        Expected heats of injection for two-component binding model.

        ARGUMENTS

        DeltaG - free energy of binding (kcal/mol)
        DeltaH - enthalpy of binding (kcal/mol)
        DeltaH_0 - heat of injection (cal/mol)
        
        """
        
        # Convenience constants
        N = self.N # number of injections
        V0 = self.V0 # sample cell volume
        DeltaV = self.DeltaV # injection volume
        
        # Compute complex concentrations.
        Pn = numpy.zeros([N], numpy.float64) # Pn[n] is the protein concentration in sample cell after n injections (M)
        Ln = numpy.zeros([N], numpy.float64) # Ln[n] is the ligand concentration in sample cell after n injections (M)
        PLn = numpy.zeros([N], numpy.float64) # PLn[n] is the complex concentration in sample cell after n injections (M)
        for n in range(N):
            # Instantaneous injection model (perfusion)
            d = 1.0 - (DeltaV / V0) # dilution factor (dimensionless)
            P = V0 * P0 * d**n # total quantity of protein in sample cell after n injections (mol)
            L = V0 * Ls * (1. - d**n) # total quantity of ligand in sample cell after n injections (mol)
            PLn[n] = 0.5/V0 * ((P + L + Kd*V0) - sqrt((P + L + Kd*V0)**2 - 4*P*L));  # complex concentration (M)
            Pn[n] = P/V0 - PLn[n]; # free protein concentration in sample cell after n injections (M)
            Ln[n] = L/V0 - PLn[n]; # free ligand concentration in sample cell after n injections (M)

        # Compute expected injection heats.
        q_n_model = numpy.zeros([N], numpy.float64) # q_n_model[n] is the expected heat from injection n
        for n in range(N):
            # Instantaneous injection model (perfusion)
            d = 1.0 - (DeltaV / V0) # dilution factor (dimensionless)
            q_n[0] = (1000.0*DeltaH) * V0 * PLn[0] + DeltaH_0 # first injection
            for n in range(1,N):
                q_n[n] = (1000.0*DeltaH) * V0 * (PLn[n] - d*PLn[n-1]) + DeltaH_0 # subsequent injections

        return q_n

    def __init__(self, P0_stated, dP0, Ls_stated, dLs, q_n, V0, DeltaV):
        # Determine number of observations.
        self.N = q_n.size

        # Store sample cell volume and injection volume.
        self.V0 = V0
        self.DeltaV = DeltaV

        self.dP0 = dP0
        self.dLs = dLs

        # Determine min and max range for log_sigma
        sigma_guess = abs(q_n(self.N-1))
        log_sigma_min = log(sigma_guess) - 5.0
        log_sigma_max = log(sigma_guess) + 5.0

        # Determine range for priors for thermodynamic parameters.
        DeltaG_min = -40. # (kcal/mol)
        DeltaG_max = +40. # (kcal/mol)
        DeltaH_min = -100. # (kcal/mol)
        DeltaH_max = +100. # (kcal/mol)
        DeltaH_0_min = -1000. # (cal/mol)
        DeltaH_0_max = +1000. # (cal/mol)
        
        # Define priors.
        self.P0 = pymc.Normal('P0', mu=P0_stated, tau=1.0/dP0**2)
        self.Ls = pymc.Normal('Ls', mu=Ls_stated, tau=1.0/dLs**2)
        self.log_sigma = pymc.Uniform('log_sigma', lower=log_sigma_min, upper=log_sigma_max)
        self.DeltaG = pymc.Uniform('DeltaG', lower=DeltaG_min, upper=DeltaG_max)
        self.DeltaH = pymc.Unifrom('DeltaH', lower=DeltaH_min, upper=DeltaH_max)
        self.DeltaH_0 = pymc.Uniform('DeltaH_0', lower=DeltaH_0_min, upper=DeltaH_0_max)
        
        # Define observed data.
        self.q_n = pymc.Normal('q_n', n=N, mu=q_n_model(self.DeltaG, self.DeltaH, self.DeltaH0), tau=exp(-2*log_sigma), observed=True, value=q_n)
        
        return

# Define model
model = TwoComponentBindingModel(P0_stated, Ls_stated, q_n, V0, DeltaV)

#=============================================================================================
# Initial guess for thermodynaic parameters
#=============================================================================================

# INITIAL GUESSES FOR THERMODYNAMIC PARAMETERS FOR ABRF-MIRG'02
DeltaG = -8.3 # free energy of binding (kcal/mol)
DeltaH = 10.0 # enthalpy of binding (kcal/mol)
DeltaH_0 = 0.0 # heat of dilution (cal/injection)
sigma = abs(q_n(N-1)) # noise parameter (cal/injection)
log_sigma = log(sigma)
P0 = P0_stated # titrate concentration (M)
Ls = Ls_stated # titrant concentration (M)

#=============================================================================================
# MCMC inference
#=============================================================================================

niters = 10000 # number of iterations
nburn = 5000 # number of burn-in iterations
nthin = 2 # thinning period

mcmc = pymc.MCMC(model, db='hdf5')
mcmc.sample(iter=niters, burn=nburn, thin=nthin)
pymc.Matplot.plot(mcmc)
