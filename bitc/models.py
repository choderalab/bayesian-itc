#!/usr/bin/env python
"""
PyMC models to describe ITC binding experiments
"""

import copy
import logging
from math import exp, log

import numpy
import pymc
import scipy.integrate

from bitc.units import ureg, Quantity

# Use module name for logger
logger = logging.getLogger(__name__)

# TODO check if rescaling step is still necessary


class RescalingStep(pymc.StepMethod):

    """
    Rescaling StepMethod for sampling correlated changes in ligand and receptor concentration

    """

    def __init__(self, dictionary, beta, max_scale=1.03, interval=100, verbose=0):
        """
        dictionary (dict) - must contain dictionary of objects for Ls, P0, DeltaH, DeltaG
        """

        # Verbosity flag for pymc
        self.verbose = verbose

        # Store stochastics.
        self.dictionary = dictionary

        # Initialize superclass.
        pymc.StepMethod.__init__(self, dictionary.values(), verbose)

        self._id = 'RescalingMetropolis_' + '_'.join([p.__name__ for p in self.stochastics])

        # State variables used to restore the state in a later session.
        self._state += ['max_scale', '_current_iter', 'interval']

        self.max_scale = max_scale
        self.beta = beta

        self._current_iter = 0
        self.interval = interval

        self.accepted = 0
        self.rejected = 0

        # Report
        logger.info("Initialization...\n" + "max_scale: %s" % self.max_scale)

    def propose(self):
        # Choose trial scaling factor or its inverse with equal probability, so
        # that proposal move is symmetric.
        factor = (self.max_scale - 1) * numpy.random.rand() + 1
        if numpy.random.rand() < 0.5:
            factor = 1. / factor

        # Scale thermodynamic parameters and variables with this factor.
        self.dictionary['Ls'].value = self.dictionary['Ls'].value * factor
        self.dictionary['P0'].value = self.dictionary['P0'].value * factor
        self.dictionary['DeltaH'].value = self.dictionary['DeltaH'].value / factor
        # calling magnitude seems flaky, where are the units here?
        self.dictionary['DeltaG'].value = self.dictionary['DeltaG'].value + (1. / self.beta.magnitude) * numpy.log(factor)

        return

    def step(self):
        # Probability and likelihood for stochastic's current value:
        logp = sum([stochastic.logp for stochastic in self.stochastics])
        loglike = self.loglike
        logger.info('Current likelihood: %f, %f' % (logp, loglike))

        # Sample a candidate value
        self.propose()

        # Metropolis acception/rejection test
        accept = False
        try:
            # Probability and likelihood for stochastic's proposed value:
            logp_p = sum([stochastic.logp for stochastic in self.stochastics])
            loglike_p = self.loglike
            logger.debug('Current likelihood: %f, %f ' % (logp, loglike))

            if numpy.log(numpy.random.rand()) < logp_p + loglike_p - logp - loglike:
                accept = True
                self.accepted += 1
                logger.debug('Accepted')
            else:
                self.rejected += 1
                logger.debug('Rejected')
        except pymc.ZeroProbability:
            self.rejected += 1
            logp_p = None
            loglike_p = None
            logger.debug('Rejected with ZeroProbability error.')

        if not self._current_iter % self.interval:
            logger.info("Step %d \n"
                        "Logprobability (current, proposed): %s, %s \n"
                        "loglike (current, proposed):  %s, %s    :" % (self._current_iter,
                                                                       logp,
                                                                       logp_p,
                                                                       loglike,
                                                                       loglike_p
                                                                       )
                        )

            for stochastic in self.stochastics:
                logger.info("\t" + str(stochastic.__name__) +
                            str(stochastic.last_value) + str(stochastic.value))
            if accept:
                logger.info("\tAccepted\t*******\n")
            else:
                logger.info("\tRejected\n")
            logger.info(
                "\tAcceptance ratio: " + str(self.accepted / (self.accepted + self.rejected)))

        if not accept:
            self.reject()

        self._current_iter += 1

        return

    @classmethod
    def competence(cls, stochastic):
        if str(stochastic) in ['DeltaG', 'DeltaH', 'DeltaH_0', 'Ls', 'P0']:
            return 1
        return 0

    def reject(self):
        for stochastic in self.stochastics:
            # stochastic.value = stochastic.last_value
            stochastic.revert()

    @staticmethod
    def tune(verbose):
        return False

# TODO Move generation of the pymc sampler into a method in this base
# class: createSampler()?




class BindingModel(object):
    """
    Abstract base class for reaction models.
    """

    def __init__(self):
        pass

    @staticmethod
    def _add_unit_to_guesses(value, maximum, minimum, unit):
        """
        Add units to inital guesses for priors

        :param value: mean value of the guess
        :type value: float
        :param maximum: maximum for the guess
        :type maximum: float
        :param minimum: minimum value of the guess
        :type minimum: float
        :param unit: unit to add to the supplied numbers
        :type unit: Quantity
        :return: value, maximum and minimum, with units added
        :rtype: (Quantity,Quantity,Quantity)
        """
        value *= unit
        maximum *= unit
        minimum *= unit
        return value, maximum, minimum

    @staticmethod
    def _deltaH0_guesses(q_n):
        """
        Provide guesses for deltaH_0 from the last injection in the list of injection heats
        """
        # Assume the last injection has the best guess for H0
        DeltaH_0_guess = q_n[-1]
        heat_interval = (q_n.max() - q_n.min())
        DeltaH_0_min = q_n.min() - heat_interval
        DeltaH_0_max = q_n.max() + heat_interval
        return DeltaH_0_guess, DeltaH_0_max, DeltaH_0_min

    @staticmethod
    def _get_syringe_concentration(experiment):
        """Return the syringe concentration from an experiment
           for python 2/3 compatibility
        """
        try:
            Ls_stated = experiment.syringe_concentration.itervalues().next()
        except AttributeError:
            Ls_stated = next(iter(experiment.syringe_concentration.values()))
        return Ls_stated

    @staticmethod
    def _get_cell_concentration(experiment):
        """Return the cell concentration from an experiment
            for python 2/3 compatibility
        """
        try:
            P0_stated = experiment.cell_concentration.itervalues().next()
        except AttributeError:
            P0_stated = next(iter(experiment.cell_concentration.values()))

        return P0_stated

    @staticmethod
    def _lognormal_concentration_prior(name, stated_concentration, uncertainty, unit):
        """Define a pymc prior for a concentration, using micromolar units
        :rtype : pymc.Lognormal
        """
        return pymc.Lognormal(name,
                              mu=log(stated_concentration / unit),
                              tau=1.0 / log(1.0 + (uncertainty / stated_concentration) ** 2),
                              value=stated_concentration / unit
        )

    @staticmethod
    def _normal_observation_with_units(name, q_n_model, q_ns, tau, unit):
        """Define a set of normally distributed observations, while stripping units
        :rtype : pymc.Normal
        """
        return pymc.Normal(name, mu=q_n_model, tau=tau, observed=True, value=q_ns / unit)

    @staticmethod
    def _uniform_prior(name, value, maximum, minimum):
        """Define a uniform prior without units
           Added for consistency with other Bindingmodel

        :rtype : pymc.Uniform
        """
        return pymc.Uniform(name,
                            lower=minimum,
                            upper=maximum,
                            value=value
        )

    @staticmethod
    def _uniform_prior_with_units(name, value, maximum, minimum, unit):
        """Define a uniform prior, while stripping units

        :rtype : pymc.Uniform
        """
        return pymc.Uniform(name,
                            lower=minimum / unit,
                            upper=maximum / unit,
                            value=value / unit
        )

    @staticmethod
    def _uniform_prior_with_guesses_and_units(name, value, maximum, minimum, prior_unit, guess_unit=None):
        """
        Take initial values, add units or convert units to the right type,
        returns a pymc uniform prior

        :rtype : pymc.Uniform
        """
        # Guess has units
        if guess_unit is True:
            pass
        # guess provided has no units, but should be same as prior
        elif guess_unit in {None, False}:
            guess_unit = prior_unit
            value, maximum, minimum = BindingModel._add_unit_to_guesses(value, maximum, minimum, guess_unit)
        # guess unit is a unit and needs to be assigned to the guesses first
        else:
            value, maximum, minimum = BindingModel._add_unit_to_guesses(value, maximum, minimum, guess_unit)

        return BindingModel._uniform_prior_with_units(name, value, maximum, minimum, prior_unit)


class BaselineModel(BindingModel):
    """A Model for a calibration with no injections, just baseline.
       This is just a dummy and the implementation is probably wrong."""

    def __init__(self, experiment):

        # Determine number of observations.
        self.N = experiment.number_of_injections

        # Store calorimeter properties.
        self.V0 = experiment.cell_volume.to('liter')

        # Extract properties from experiment
        self.experiment = experiment

        # Store temperature.
        self.temperature = experiment.target_temperature  # (kelvin)
        # inverse temperature 1/(kcal/mol)
        self.beta = 1.0 / (ureg.molar_gas_constant * self.temperature)

        # Guess for the noise parameter log(sigma)
        self.log_sigma = BindingModel._uniform_prior('log_sigma', *self._logsigma_guesses(experiment))

        # Define the model
        tau = self._lambda_tau_model()

        # Create sampler.
        self.mcmc = self._create_metropolis_sampler()


    @staticmethod
    def tau(log_sigma):
        """
        Injection heat measurement precision.
        """
        return numpy.exp(-2.0 * log_sigma)

    def _create_metropolis_sampler(self):
        mcmc = pymc.MCMC(self, db='ram')
        return mcmc


    def _lambda_tau_model(self):
        """Model for tau implemented using lambda function"""
        return pymc.Lambda('tau', lambda log_sigma=self.log_sigma: self.tau(log_sigma))

    @staticmethod
    def _logsigma_guesses(experiment):
        """
        Estimate sigma from the gausian process baseline
        """
        log_sigma_guess = log(experiment.sigma.sum() / experiment.sigma.size)
        log_sigma_min = log(experiment.sigma.min())
        log_sigma_max = log(experiment.sigma.max())
        return log_sigma_guess, log_sigma_max, log_sigma_min


class BufferBufferModel(BindingModel):
    """A Model for a calibration titration, using only blanks (e.g. buffer or water) in the syringe and cell."""

    def __init__(self, experiment):

        # Determine number of observations.
        self.N = experiment.number_of_injections

        # Store injection volumes
        self.DeltaVn = Quantity(numpy.zeros(self.N), ureg.liter)
        for inj, injection in enumerate(experiment.injections):
            self.DeltaVn[inj] = injection.volume

        # Store calorimeter properties.
        self.V0 = experiment.cell_volume.to('liter')

        # Extract properties from experiment
        self.experiment = experiment

        # Store temperature.
        self.temperature = experiment.target_temperature  # (kelvin)
        # inverse temperature 1/(kcal/mol)
        self.beta = 1.0 / (ureg.molar_gas_constant * self.temperature)

        # Extract heats from experiment
        q_n = Quantity(numpy.zeros(len(experiment.injections)), 'microcalorie')
        for inj, injection in enumerate(experiment.injections):
            q_n[inj] = injection.evolved_heat

        # Guess for the noise parameter log(sigma)
        self.log_sigma = BindingModel._uniform_prior('log_sigma', *self._logsigma_guesses(q_n, 4, ureg.microcalorie))
        self.DeltaH_0 = BindingModel._uniform_prior_with_guesses_and_units('DeltaH_0', *self._deltaH0_guesses(q_n), prior_unit=ureg.microcalorie, guess_unit=True)

        # Define the model
        q_n_model = self._lambda_heats_model()
        tau = self._lambda_tau_model()

        # Set observation
        self.q_n_obs = BindingModel._normal_observation_with_units('q_n', q_n_model, q_n, tau, ureg.microcalorie)

        # Create sampler.
        self.mcmc = self._create_metropolis_sampler()

    @staticmethod
    @ureg.wraps(ret=ureg.microcalorie, args=[None, None], strict=True)
    def expected_injection_heats(DeltaH_0, N):
        """
        Expected heats of injection for a calibration titration
        ARGUMENTS
        DeltaH_0 - heat of injection (ucal)

        """
        # Compute expected injection heats.
        q_n = numpy.zeros([N])  # q_n_model[n] is the expected heat from injection n

        for n in range(N):
            # q_n and DeltaH_0 both have the same unit (ucal)
            q_n[n] = DeltaH_0
        return q_n

    @staticmethod
    def tau(log_sigma):
        """
        Injection heat measurement precision.
        """
        return numpy.exp(-2.0 * log_sigma)

    def _create_metropolis_sampler(self):
        mcmc = pymc.MCMC(self, db='ram')
        mcmc.use_step_method(pymc.Metropolis, self.DeltaH_0)
        return mcmc

    def _lambda_heats_model(self, q_name='q_n_model'):
        """Model the heat using expected_injection_heats, providing all input by using a lambda function
            q_name is the name for the model
        """
        return pymc.Lambda(q_name,
                           lambda
                               DeltaH_0=self.DeltaH_0,
                               N=self.N:
                           self.expected_injection_heats(
                               DeltaH_0,
                               self.N
                           )
        )

    def _lambda_tau_model(self):
        """Model for tau implemented using lambda function"""
        return pymc.Lambda('tau', lambda log_sigma=self.log_sigma: self.tau(log_sigma))

    @staticmethod
    def _logsigma_guesses(q_n, number_of_inj, standard_unit):
        """
        q_n: list/array of heats
        number_of_inj: number of injections at end of protocol to use for estimating sigma
        standard_unit: unit by which to correct the magnitude of sigma
        """
        # review: how can we do this better?
        log_sigma_guess = log(q_n[-number_of_inj:].std() / standard_unit)
        log_sigma_min = log_sigma_guess - 10
        log_sigma_max = log_sigma_guess + 5
        return log_sigma_guess, log_sigma_max, log_sigma_min


class TellinghuisenDilutionModel(BindingModel):
    """
    A binding model with titrant (syringe) but no titrand (cell) concentration.

    Using eq 12 from doi:10.1016/j.ab.2006.10.015
    """

    def __init__(self, experiment):

        # Determine number of observations.
        self.N = experiment.number_of_injections

        # Store injection volumes
        self.DeltaVn = Quantity(numpy.zeros(self.N), ureg.liter)
        for inj, injection in enumerate(experiment.injections):
            self.DeltaVn[inj] = injection.volume

        # Store calorimeter properties.
        self.V0 = experiment.cell_volume.to('liter')

        # Extract properties from experiment
        self.experiment = experiment

        # Store temperature.
        self.temperature = experiment.target_temperature  # (kelvin)
        # inverse temperature 1/(kcal/mol)
        self.beta = 1.0 / (ureg.molar_gas_constant * self.temperature)

        # Syringe concentration
        if not len(experiment.syringe_concentration) == 1:
            raise ValueError('Dilution model only supports one component in the syringe, found %d' % len(experiment.syringe_concentration))

        Xs_stated = self._get_syringe_concentration(experiment)
        # Uncertainty
        dXs = 0.10 * Xs_stated


        # Define priors for concentration
        self.Xs = BindingModel._lognormal_concentration_prior('Xs', Xs_stated, dXs, ureg.millimolar)
        # Extract heats from experiment
        q_n = Quantity(numpy.zeros(len(experiment.injections)), 'microcalorie')
        for inj, injection in enumerate(experiment.injections):
            q_n[inj] = injection.evolved_heat

        # Determine range for priors for thermodynamic parameters.
        # TODO add literature value guesses
        # review check out all the units to make sure that they're appropriate

        # Enthalpy of the syringe solution per injection
        # TODO this is a different number for the throwaway injection
        self.H_s = BindingModel._uniform_prior_with_guesses_and_units('H_s', * self._deltaH0_guesses(q_n), prior_unit=ureg.microcalorie, guess_unit=True)

        # Molar enthalpy as a function of the concentrations
        L_phi_max = numpy.ones(self.N) * 1.e4
        self.L_phi = BindingModel._uniform_prior_with_guesses_and_units('L_phi', numpy.zeros(self.N), L_phi_max, -L_phi_max, ureg.calorie/ureg.mole)

        # Prior for the noise parameter log(sigma)
        self.log_sigma = BindingModel._uniform_prior('log_sigma', *self._logsigma_guesses(q_n, 4, ureg.microcalorie))

        # Define the model
        q_n_model = self._lambda_heats_model()
        tau = self._lambda_tau_model()

        # Set observation
        self.q_n_obs = BindingModel._normal_observation_with_units('q_n', q_n_model, q_n, tau, ureg.microcalorie / ureg.mole)

        # Create sampler.
        self.mcmc = self._create_metropolis_sampler(Xs_stated)

        return


    @staticmethod
    @ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None], strict=True)
    def expected_injection_heats(V0, DeltaVn, Xs, L_phi, H_s, N):
        """
        Expected heats of injection for two-component binding model.

        ARGUMENTS
        V0 - cell volume (liter)
        DeltaVn - injection volumes (liter)
        Xs - Syringe concentration (millimolar)
        L_phi - molar enthalpy at concentration [X] (cal/mol)
        H_s - enthalpy in the syringe per injection (ucal) assumed same for every injection (wrong for throwaway!)
        N - number of injections

        Returns
        -------
        expected injection heats (ucal)


        """
        # Ln[n] is the ligand concentration in sample cell after n injections
        Xn = numpy.zeros([N])

        # Equation 8 of Tellinghuisen Calibration in isothermal titration calorimetry:
        # heat and cell volume from heat of dilution of NaCl(aq).
        # http://dx.doi.org/10.1016/j.ab.2006.10.015
        vcum = 0.0  # cumulative injected volume (liter)
        for n in range(1,N):
            # Instantaneous injection model (perfusion)
            # dilution factor for this injection (dimensionless)
            vcum += DeltaVn[n]
            vfactor = vcum / V0  # relative volume factor
            # total concentration of ligand in sample cell after n injections (converted from mM to M)
            Xn[n] = 1.e-3 * Xs * (1 - numpy.exp(-vfactor))

        # Equation 12 of same paper as above

        # Compute expected injection heats.
        # q_n_model[n] is the expected heat from injection n
        q_n = numpy.zeros([N])
        r = DeltaVn[0] / (2* V0)
        # Instantaneous injection model (perfusion)
        # first injection
        # converted from cal/mol to ucal
        q_n[0] = V0 * 1.e6 * (L_phi[0] * Xn[0] * (1 + r)) - H_s
        # next injections
        for n in range(1, N):
            r = DeltaVn[n] / (2 * V0)
            # converted from cal/mol to ucal
            q_n[n] = V0 * 1.e6 * (L_phi[n] * Xn[n] * (1 + r) - L_phi[n-1] * Xn[n-1] * (1 - r)) - H_s

        return q_n

    @staticmethod
    def tau(log_sigma):
        """
        Injection heat measurement precision.
        """
        return numpy.exp(-2.0 * log_sigma)

    def _create_metropolis_sampler(self, Ls_stated):
        """Create an MCMC sampler for the two component model.
        """
        mcmc = pymc.MCMC(self, db='ram')
        mcmc.use_step_method(pymc.Metropolis, self.L_phi)
        mcmc.use_step_method(pymc.Metropolis, self.H_s)
        mcmc.use_step_method(pymc.Metropolis, self.Xs)
        return mcmc


    def _lambda_heats_model(self, q_name='q_n_model'):
        """Model the heat using expected_injection_heats, providing all input by using a lambda function
            q_name is the name for the model
        """
        return pymc.Lambda(q_name,
                           lambda
                               V0=self.V0,
                               DeltaVn=self.DeltaVn,
                               Xs=self.Xs,
                               L_phi=self.L_phi,
                               H_s=self.H_s,
                               N=self.N:
                           self.expected_injection_heats(
                               V0,
                               DeltaVn,
                               Xs,
                               L_phi,
                               H_s,
                               N
                           )
        )

    def _lambda_tau_model(self):
        """Model for tau implemented using lambda function"""
        return pymc.Lambda('tau', lambda log_sigma=self.log_sigma: self.tau(log_sigma))

    @staticmethod
    def _logsigma_guesses(q_n, number_of_inj, standard_unit):
        """
        q_n: list/array of heats
        number_of_inj: number of injections at end of protocol to use for estimating sigma
        standard_unit: unit by which to correct the magnitude of sigma
        """
        # review: how can we do this better?
        log_sigma_guess = log(q_n[-number_of_inj:].std() / standard_unit)
        log_sigma_min = log_sigma_guess - 10
        log_sigma_max = log_sigma_guess + 5
        return log_sigma_guess, log_sigma_max, log_sigma_min


class TitrantBufferModel(BindingModel):
    """
    A binding model with titrant (syringe) but no titrand (cell) concentration.

    """

    def __init__(self, experiment):

        # Determine number of observations.
        self.N = experiment.number_of_injections

        # Store injection volumes
        self.DeltaVn = Quantity(numpy.zeros(self.N), ureg.liter)
        for inj, injection in enumerate(experiment.injections):
            self.DeltaVn[inj] = injection.volume

        # Store calorimeter properties.
        self.V0 = experiment.cell_volume.to('liter')

        # Extract properties from experiment
        self.experiment = experiment

        # Store temperature.
        self.temperature = experiment.target_temperature  # (kelvin)
        # inverse temperature 1/(kcal/mol)
        self.beta = 1.0 / (ureg.molar_gas_constant * self.temperature)

        # Syringe concentration
        if not len(experiment.syringe_concentration) == 1:
            raise ValueError('TitrantBuffer model only supports one component in the syringe, found %d' % len(experiment.syringe_concentration))

        Xs_stated = self._get_syringe_concentration(experiment)
        # Uncertainty
        dXs = 0.10 * Xs_stated


        # Define priors for concentration
        self.Xs = BindingModel._lognormal_concentration_prior('Xs', Xs_stated, dXs, ureg.millimolar)
        # Extract heats from experiment
        q_n = Quantity(numpy.zeros(len(experiment.injections)), 'microcalorie')
        for inj, injection in enumerate(experiment.injections):
            q_n[inj] = injection.evolved_heat

        # Determine range for priors for thermodynamic parameters.
        # TODO add literature value guesses
        # review check out all the units to make sure that they're appropriate

        # Enthalpy of the syringe solution per injection
        # TODO this is a different number for the throwaway injection
        self.H_0 = BindingModel._uniform_prior_with_guesses_and_units('H_0', * self._deltaH0_guesses(q_n), prior_unit=ureg.microcalorie, guess_unit=True)

        # Total enthalp of dilution
        self.DeltaH = BindingModel._uniform_prior_with_guesses_and_units('DeltaH', 0., 1000., -1000., ureg.calorie/ureg.mole)

        # Prior for the noise parameter log(sigma)
        self.log_sigma = BindingModel._uniform_prior('log_sigma', *self._logsigma_guesses(q_n, 4, ureg.microcalorie))

        # Define the model
        q_n_model = self._lambda_heats_model()
        tau = self._lambda_tau_model()

        # Set observation
        self.q_n_obs = BindingModel._normal_observation_with_units('q_n', q_n_model, q_n, tau, ureg.microcalorie / ureg.mole)

        # Create sampler.
        self.mcmc = self._create_metropolis_sampler(Xs_stated)

        return


    @staticmethod
    @ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None], strict=True)
    def expected_injection_heats(V0, DeltaVn, Xs, DeltaH, H_0, N):
        """
        Expected heats of injection for two-component binding model.

        ARGUMENTS
        V0 - cell volume (liter)
        DeltaVn - injection volumes (liter)
        Xs - Syringe concentration (millimolar)
        DeltaH - total enthalpy of dilution (cal/mol)
        H_0 - mechanical heat of injection (ucal)
        N - number of injections

        Returns
        -------
        expected injection heats (ucal)


        """
        # Ln[n] is the ligand concentration in sample cell after n injections
        Xn = numpy.zeros([N])

        # Equation 8 of Tellinghuisen Calibration in isothermal titration calorimetry:
        # heat and cell volume from heat of dilution of NaCl(aq).
        # http://dx.doi.org/10.1016/j.ab.2006.10.015
        vcum = 0.0  # cumulative injected volume (liter)
        for n in range(1, N):
            # Instantaneous injection model (perfusion)
            # dilution factor for this injection (dimensionless)
            vcum += DeltaVn[n]
            vfactor = vcum / V0  # relative volume factor
            # total concentration of ligand in sample cell after n injections (converted from mM to M)
            Xn[n] = 1.e-3 * Xs * (1 - numpy.exp(-vfactor))

        # Compute expected injection heats.
        # q_n_model[n] is the expected heat from injection n
        q_n = numpy.zeros([N])
        # Instantaneous injection model (perfusion)
        # first injection
        # From units of cal/mole to ucal
        q_n[0] = 1.e6 * (DeltaH * V0 * Xn[0]) + H_0
        for n in range(1, N):
            d = 1.0 - (DeltaVn[n] / V0)  # dilution factor (dimensionless)
            # subsequent injections
            # From units of cal/mole to ucal
            q_n[n] = 1.e6 * (DeltaH * V0 * (Xn[n] - Xn[n - 1]))  + H_0

        return q_n


    @staticmethod
    def tau(log_sigma):
        """
        Injection heat measurement precision.
        """
        return numpy.exp(-2.0 * log_sigma)

    def _create_metropolis_sampler(self, Ls_stated):
        """Create an MCMC sampler for the two component model.
        """
        mcmc = pymc.MCMC(self, db='ram')
        mcmc.use_step_method(pymc.Metropolis, self.DeltaH)
        mcmc.use_step_method(pymc.Metropolis, self.H_0)
        mcmc.use_step_method(pymc.Metropolis, self.Xs)
        return mcmc


    def _lambda_heats_model(self, q_name='q_n_model'):
        """Model the heat using expected_injection_heats, providing all input by using a lambda function
            q_name is the name for the model
        """
        return pymc.Lambda(q_name,
                           lambda
                               V0=self.V0,
                               DeltaVn=self.DeltaVn,
                               Xs=self.Xs,
                               DeltaH=self.DeltaH,
                               H_0=self.H_0,
                               N=self.N:
                           self.expected_injection_heats(
                               V0,
                               DeltaVn,
                               Xs,
                               DeltaH,
                               H_0,
                               N
                           )
        )

    def _lambda_tau_model(self):
        """Model for tau implemented using lambda function"""
        return pymc.Lambda('tau', lambda log_sigma=self.log_sigma: self.tau(log_sigma))

    @staticmethod
    def _logsigma_guesses(q_n, number_of_inj, standard_unit):
        """
        q_n: list/array of heats
        number_of_inj: number of injections at end of protocol to use for estimating sigma
        standard_unit: unit by which to correct the magnitude of sigma
        """
        # review: how can we do this better?
        log_sigma_guess = log(q_n[-number_of_inj:].std() / standard_unit)
        log_sigma_min = log_sigma_guess - 10
        log_sigma_max = log_sigma_guess + 5
        return log_sigma_guess, log_sigma_max, log_sigma_min


class BufferTitrandModel(BindingModel):
    """
    A binding model with buffer (syringe) and titrand (cell) concentration.

    """

    def __init__(self, experiment):

        # Determine number of observations.
        self.N = experiment.number_of_injections

        # Store injection volumes
        self.DeltaVn = Quantity(numpy.zeros(self.N), ureg.liter)
        for inj, injection in enumerate(experiment.injections):
            self.DeltaVn[inj] = injection.volume

        # Store calorimeter properties.
        self.V0 = experiment.cell_volume.to('liter')

        # Extract properties from experiment
        self.experiment = experiment

        # Store temperature.
        self.temperature = experiment.target_temperature  # (kelvin)
        # inverse temperature 1/(kcal/mol)
        self.beta = 1.0 / (ureg.molar_gas_constant * self.temperature)

        # Syringe concentration
        if not len(experiment.cell_concentration) == 1:
            raise ValueError('BufferTitrand model only supports one component in the cell, found %d' % len(experiment.syringe_concentration))

        Mc_stated = self._get_cell_concentration(experiment)
        # Uncertainty
        dMc = 0.10 * Mc_stated


        # Define priors for concentration
        self.Mc = BindingModel._lognormal_concentration_prior('Mc', Mc_stated, dMc, ureg.millimolar)
        # Extract heats from experiment
        q_n = Quantity(numpy.zeros(len(experiment.injections)), 'microcalorie')
        for inj, injection in enumerate(experiment.injections):
            q_n[inj] = injection.evolved_heat

        # Determine range for priors for thermodynamic parameters.
        # TODO add literature value guesses
        # review check out all the units to make sure that they're appropriate

        # Enthalpy of the syringe solution per injection
        # TODO this is a different number for the throwaway injection
        self.H_0 = BindingModel._uniform_prior_with_guesses_and_units('H_0', * self._deltaH0_guesses(q_n), prior_unit=ureg.microcalorie, guess_unit=True)

        # Total enthalp of dilution
        self.DeltaH = BindingModel._uniform_prior_with_guesses_and_units('DeltaH', 0., 1000., -1000., ureg.calorie/ureg.mole)

        # Prior for the noise parameter log(sigma)
        self.log_sigma = BindingModel._uniform_prior('log_sigma', *self._logsigma_guesses(q_n, 4, ureg.microcalorie))

        # Define the model
        q_n_model = self._lambda_heats_model()
        tau = self._lambda_tau_model()

        # Set observation
        self.q_n_obs = BindingModel._normal_observation_with_units('q_n', q_n_model, q_n, tau, ureg.microcalorie / ureg.mole)

        # Create sampler.
        self.mcmc = self._create_metropolis_sampler(Mc_stated)

        return


    @staticmethod
    @ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None], strict=True)
    def expected_injection_heats(V0, DeltaVn, Mc, DeltaH, H_0, N):
        """
        Expected heats of injection for two-component binding model.

        ARGUMENTS
        V0 - cell volume (liter)
        DeltaVn - injection volumes (liter)
        Mc - cell_concentration (millimolar)
        DeltaH - total enthalpy of dilution (cal /mol)
        H_0 - mechanical heat of injection (ucal)
        N - number of injections

        Returns
        -------
        expected injection heats (ucal)


        """
        # Mn[n] is the macromolecule concentration in sample cell after n injections
        Mn = numpy.zeros([N])

        dcum = 1.0  # cumulative dilution factor (dimensionless)
        for n in range(N):
            # Instantaneous injection model (perfusion)
            # dilution factor for this injection (dimensionless)
            d = 1.0 - (DeltaVn[n] / V0)
            dcum *= d  # cumulative dilution factor
            # total quantity of protein in sample cell after n injections (converted from mM to M)
            Mn[n] = Mc * 1.e-3 * dcum

        # Compute expected injection heats.
        # q_n_model[n] is the expected heat from injection n
        q_n = numpy.zeros([N])
        # Instantaneous injection model (perfusion)
        # first injection
        # converted from cal/mol to ucal
        d = 1.0 - (DeltaVn[0] / V0)  # dilution factor (dimensionless)
        q_n[0] = V0 * 1.e6 * (DeltaH * (Mn[0] - Mc)) + H_0
        for n in range(1, N):
            d = 1.0 - (DeltaVn[n] / V0)  # dilution factor (dimensionless)
            # subsequent injections
            # converted from cal/mol to ucal
            q_n[n] = V0 * 1.e6 * (DeltaH * (Mn[n] - Mn[n - 1])) + H_0

        return q_n


    @staticmethod
    def tau(log_sigma):
        """
        Injection heat measurement precision.
        """
        return numpy.exp(-2.0 * log_sigma)

    def _create_metropolis_sampler(self, Ls_stated):
        """Create an MCMC sampler for the two component model.
        """
        mcmc = pymc.MCMC(self, db='ram')
        mcmc.use_step_method(pymc.Metropolis, self.DeltaH)
        mcmc.use_step_method(pymc.Metropolis, self.H_0)
        mcmc.use_step_method(pymc.Metropolis, self.Mc)
        return mcmc


    def _lambda_heats_model(self, q_name='q_n_model'):
        """Model the heat using expected_injection_heats, providing all input by using a lambda function
            q_name is the name for the model
        """
        return pymc.Lambda(q_name,
                           lambda
                               V0=self.V0,
                               DeltaVn=self.DeltaVn,
                               Mc=self.Mc,
                               DeltaH=self.DeltaH,
                               H_0=self.H_0,
                               N=self.N:
                           self.expected_injection_heats(
                               V0,
                               DeltaVn,
                               Mc,
                               DeltaH,
                               H_0,
                               N
                           )
        )

    def _lambda_tau_model(self):
        """Model for tau implemented using lambda function"""
        return pymc.Lambda('tau', lambda log_sigma=self.log_sigma: self.tau(log_sigma))

    @staticmethod
    def _logsigma_guesses(q_n, number_of_inj, standard_unit):
        """
        q_n: list/array of heats
        number_of_inj: number of injections at end of protocol to use for estimating sigma
        standard_unit: unit by which to correct the magnitude of sigma
        """
        # review: how can we do this better?
        log_sigma_guess = log(q_n[-number_of_inj:].std() / standard_unit)
        log_sigma_min = log_sigma_guess - 10
        log_sigma_max = log_sigma_guess + 5
        return log_sigma_guess, log_sigma_max, log_sigma_min

class TwoComponentBindingModel(BindingModel):
    """
    A binding model with two components (e.g. Protein and Ligand)
    """

    def __init__(self, experiment):

        # Determine number of observations.
        self.N = experiment.number_of_injections

        # Store injection volumes
        self.DeltaVn = Quantity(numpy.zeros(self.N), ureg.liter)
        for inj, injection in enumerate(experiment.injections):
            self.DeltaVn[inj] = injection.volume

        # Store calorimeter properties.
        self.V0 = experiment.cell_volume.to('liter')

        # Extract properties from experiment
        self.experiment = experiment

        # Store temperature.
        self.temperature = experiment.target_temperature  # (kelvin)
        # inverse temperature 1/(kcal/mol)
        self.beta = 1.0 / (ureg.molar_gas_constant * self.temperature)

        # Syringe concentration
        if not len(experiment.syringe_concentration) == 1:
            raise ValueError('TwoComponent model only supports one component in the syringe, found %d' % len(experiment.syringe_concentration))

        Ls_stated = self._get_syringe_concentration(experiment)
        # Uncertainty
        dLs = 0.10 * Ls_stated

        #Cell concentrations
        if not len(experiment.cell_concentration) == 1:
            raise ValueError('TwoComponent model only supports one component in the cell, found %d' % len(experiment.cell_concentration))

        P0_stated = self._get_cell_concentration(experiment)
        # Uncertainty
        dP0 = 0.10 * P0_stated

        # Define priors for concentrations.
        self.P0 = BindingModel._lognormal_concentration_prior('P0', P0_stated, dP0, ureg.millimolar)
        self.Ls = BindingModel._lognormal_concentration_prior('Ls', Ls_stated, dLs, ureg.millimolar)

        # Extract heats from experiment
        q_n = Quantity(numpy.zeros(len(experiment.injections)), 'microcalorie')
        for inj, injection in enumerate(experiment.injections):
            q_n[inj] = injection.evolved_heat

        # Determine range for priors for thermodynamic parameters.
        # TODO add literature value guesses
        # review check out all the units to make sure that they're appropriate

        self.DeltaH_0 = BindingModel._uniform_prior_with_guesses_and_units('DeltaH_0', *self._deltaH0_guesses(q_n), prior_unit=ureg.microcalorie, guess_unit=True)
        self.DeltaG = BindingModel._uniform_prior_with_guesses_and_units('DeltaG', 0., 40., -40., ureg.kilocalorie/ureg.mole)
        self.DeltaH = BindingModel._uniform_prior_with_guesses_and_units('DeltaH', 0., 100., -100., ureg.kilocalorie/ureg.mole)

        # Prior for the noise parameter log(sigma)
        self.log_sigma = BindingModel._uniform_prior('log_sigma', *self._logsigma_guesses(q_n, 4, ureg.microcalorie))

        # Define the model
        q_n_model = self._lambda_heats_model()
        tau = self._lambda_tau_model()

        # Set observation
        self.q_n_obs = BindingModel._normal_observation_with_units('q_n', q_n_model, q_n, tau, ureg.microcalorie / ureg.mole)

        # Create sampler.
        self.mcmc = self._create_metropolis_sampler(Ls_stated, P0_stated, experiment)

        return


    @staticmethod
    @ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None, None,  ureg.mole / ureg.kilocalories, None], strict=True)
    def expected_injection_heats(V0, DeltaVn, P0, Ls, DeltaG, DeltaH, DeltaH_0, beta, N):
        """
        Expected heats of injection for two-component binding model.

        ARGUMENTS
        V0 - cell volume (liter)
        DeltaVn - injection volumes (liter)
        P0 - Cell concentration (millimolar)
        Ls - Syringe concentration (millimolar)
        DeltaG - free energy of binding (kcal/mol)
        DeltaH - enthalpy of binding (kcal/mol)
        DeltaH_0 - heat of injection (ucal)
        beta - inverse temperature * gas constant (mol/kcal)
        N - number of injections

        Returns
        -------
        expected injection heats - ucal


        """
        # TODO Units that go into this need to be verified
        # TODO update docstring with new input

        Kd = exp(beta * DeltaG)   # dissociation constant (M)
        N = N

        # Compute complex concentrations.
        # Pn[n] is the protein concentration in sample cell after n injections
        # (M)
        Pn = numpy.zeros([N])
        # Ln[n] is the ligand concentration in sample cell after n injections
        # (M)
        Ln = numpy.zeros([N])
        # PLn[n] is the complex concentration in sample cell after n injections
        # (M)
        PLn = numpy.zeros([N])
        dcum = 1.0  # cumulative dilution factor (dimensionless)
        for n in range(N):
            # Instantaneous injection model (perfusion)
            # TODO: Allow injection volume to vary for each injection.
            # dilution factor for this injection (dimensionless)
            d = 1.0 - (DeltaVn[n] / V0)
            dcum *= d  # cumulative dilution factor
            # total quantity of protein in sample cell after n injections (converted from mM to mole)
            P = V0 * P0 * 1.e-3 * dcum
            # total quantity of ligand in sample cell after n injections (converted from mM to mole)
            L = V0 * Ls * 1.e-3 * (1. - dcum)
            # complex concentration (M)
            PLn[n] = (0.5 / V0 * ((P + L + Kd * V0) - ((P + L + Kd * V0) ** 2 - 4 * P * L) ** 0.5))
            # free protein concentration in sample cell after n injections (M)
            Pn[n] = P / V0 - PLn[n]
            # free ligand concentration in sample cell after n injections (M)
            Ln[n] = L / V0 - PLn[n]

        # Compute expected injection heats.
        # q_n_model[n] is the expected heat from injection n
        q_n = numpy.zeros([N])
        # Instantaneous injection model (perfusion)
        # first injection
        # converted from kcal/mol to ucal
        q_n[0] = 1.e9 * (DeltaH * V0 * PLn[0]) + DeltaH_0
        for n in range(1, N):
            d = 1.0 - (DeltaVn[n] / V0)  # dilution factor (dimensionless)
            # subsequent injections
            # converted from kcal/mol to ucal
            q_n[n] = 1.e9 * (DeltaH * V0 * (PLn[n] - d * PLn[n - 1])) + DeltaH_0

        return q_n

    @staticmethod
    def tau(log_sigma):
        """
        Injection heat measurement precision.
        """
        return numpy.exp(-2.0 * log_sigma)



    def _create_rescaling_sampler(self, Ls_stated, P0_stated, experiment):
        """Create an MCMC sampler for the two component model.
           Uses rescalingstep only when concentrations exist for both P and L."""
        mcmc = self._create_metropolis_sampler(Ls_stated, P0_stated, experiment)
        if P0_stated > Quantity('0.0 molar') and Ls_stated > Quantity('0.0 molar'):
            mcmc.use_step_method(RescalingStep,
                                 {'Ls': self.Ls,
                                  'P0': self.P0,
                                  'DeltaH': self.DeltaH,
                                  'DeltaG': self.DeltaG},
                                 self.beta
            )

        return mcmc

    def _create_metropolis_sampler(self, Ls_stated, P0_stated, experiment):
        """Create an MCMC sampler for the two component model.
        """
        mcmc = pymc.MCMC(self, db='ram')
        mcmc.use_step_method(pymc.Metropolis, self.DeltaG)
        mcmc.use_step_method(pymc.Metropolis, self.DeltaH)
        mcmc.use_step_method(pymc.Metropolis, self.DeltaH_0)
        if P0_stated > Quantity('0.0 molar'):
            mcmc.use_step_method(pymc.Metropolis, self.P0)
        if Ls_stated > Quantity('0.0 molar'):
            mcmc.use_step_method(pymc.Metropolis, self.Ls)

        return mcmc


    def _lambda_heats_model(self, q_name='q_n_model'):
        """Model the heat using expected_injection_heats, providing all input by using a lambda function
            q_name is the name for the model
        """
        return pymc.Lambda(q_name,
                           lambda
                               P0=self.P0,
                               Ls=self.Ls,
                               DeltaG=self.DeltaG,
                               DeltaH=self.DeltaH,
                               DeltaH_0=self.DeltaH_0:
                           self.expected_injection_heats(
                               self.V0,
                               self.DeltaVn,
                               P0,
                               Ls,
                               DeltaG,
                               DeltaH,
                               DeltaH_0,
                               self.beta,
                               self.N
                           )
        )

    def _lambda_tau_model(self):
        """Model for tau implemented using lambda function"""
        return pymc.Lambda('tau', lambda log_sigma=self.log_sigma: self.tau(log_sigma))

    @staticmethod
    def _logsigma_guesses(q_n, number_of_inj, standard_unit):
        """
        q_n: list/array of heats
        number_of_inj: number of injections at end of protocol to use for estimating sigma
        standard_unit: unit by which to correct the magnitude of sigma
        """
        # review: how can we do this better?
        log_sigma_guess = log(q_n[-number_of_inj:].std() / standard_unit)
        log_sigma_min = log_sigma_guess - 10
        log_sigma_max = log_sigma_guess + 5
        return log_sigma_guess, log_sigma_max, log_sigma_min


class CompetitiveBindingModel(BindingModel):
    """
    Competitive binding model.
    """

    def __init__(self, experiments, receptor, concentration_uncertainty=0.10):
        """
        ARGUMENTS

        experiments (list of Experiment) -
        instrument Instrument that experiment was carried out in (has to be one)
        receptor (string) - name of receptor species
        OPTIONAL ARGUMENTS
        concentration_uncertainty (float) - relative uncertainty in concentrations
        """

        # Store temperature.
        # NOTE: Right now, there can only be one.
        self.temperature = experiments[0].temperature  # temperature (kelvin)
        # inverse temperature 1/(kcal/mol)
        self.beta = 1.0 / (ureg.molar_gas_constant * self.temperature)

        # Store copy of experiments.
        self.experiments = experiments
        logging.info("%d experiments" % len(self.experiments))

        # Store sample cell volume.
        self.V0 = self.experiments[0].cell_volume

        # Store the name of the receptor.
        self.receptor = receptor
        logging.info("species '%s' will be treated as receptor" % self.receptor)

        # Make a list of names of all molecular species.
        self.species = self._species_from_experiments(experiments)
        logging.info("species: %s" % self.species)

        # Make a list of all ligands.
        self.ligands = copy.deepcopy(self.species)
        self.ligands.remove(receptor)
        logging.info("ligands: %s" % self.ligands)

        # Create a list of all stochastics.
        self.stochastics = list()

        # Create a prior for thermodynamic parameters of binding for each ligand-receptor interaction.

        self.thermodynamic_parameters = dict()
        # TODO: add option to set initial thermodynamic parameters to literature values.
        for ligand in self.ligands:
            # define the name and prior for each receptor ligand combination

            # delta G of binding
            dg_name = "DeltaG of %s * %s" % (self.receptor, ligand)
            prior_deltag = BindingModel._uniform_prior_with_guesses_and_units(dg_name, 0., 40., -40., ureg.kilocalorie / ureg.mole)

            # delta H of binding
            dh_name = "DeltaH of %s * %s" % (self.receptor, ligand)
            prior_deltah = BindingModel._uniform_prior_with_guesses_and_units(dh_name, 0., 100., -100., ureg.kilocalorie / ureg.mole)

            self.thermodynamic_parameters[dg_name] = prior_deltag
            self.thermodynamic_parameters[dh_name] = prior_deltah

            self.stochastics.append(prior_deltag)
            self.stochastics.append(prior_deltah)

        logging.debug("thermodynamic parameters:")
        logging.debug(self.thermodynamic_parameters)

        log_sigma_guess, log_sigma_max, log_sigma_min = self._logsigma_guesses_from_multiple_experiments(ureg.microcalorie)
        self.log_sigma = BindingModel._uniform_prior('log_sigma', log_sigma_guess, log_sigma_max, log_sigma_min)
        self.stochastics.append(self.log_sigma)

        tau = pymc.Lambda('tau', lambda log_sigma=self.log_sigma: exp(-2.0 * log_sigma))
        self.stochastics.append(tau)

        # Define priors for unknowns for each experiment.
        for (index, experiment) in enumerate(self.experiments):
            # Number of observations
            experiment.ninjections = experiment.observed_injection_heats.size
            logging.info("Experiment %d has %d injections" %
                         (index, experiment.ninjections))

            dh0_name = "DeltaH_0 for experiment %d" % index
            experiment.DeltaH_0 = BindingModel._uniform_prior_with_guesses_and_units(dh0_name, *self._deltaH0_guesses(experiment.observed_injection_heats), prior_unit=ureg.microcalorie, guess_unit=True)
            self.stochastics.append(experiment.DeltaH_0)

            # Define priors for the true concentration of each component
            experiment.true_cell_concentration = dict()
            for species, concentration in experiment.cell_concentration.iteritems():
                name = "initial sample cell concentration of %s in experiment %d" % (species, index)
                cell_concentration_prior = BindingModel._lognormal_concentration_prior(name, concentration, concentration_uncertainty * concentration, ureg.millimole / ureg.liter)
                experiment.true_cell_concentration[species] = cell_concentration_prior
                self.stochastics.append(cell_concentration_prior)

            experiment.true_syringe_concentration = dict()
            for species, concentration in experiment.syringe_concentration.iteritems():
                name = "initial syringe concentration of %s in experiment %d" % (species, index)
                syringe_concentration_prior = BindingModel._lognormal_concentration_prior(name, concentration, concentration_uncertainty * concentration, ureg.millimole / ureg.liter)
                experiment.true_cell_concentration[species] = syringe_concentration_prior
                self.stochastics.append(syringe_concentration_prior)

            # Add species not explicitly listed with zero concentration.
            self._zero_for_missing__concentrations(experiment)

            # True injection heats
            q_name = "true injection heats for experiment %d" % index
            experiment.true_injection_heats = self._lambda_heats_model(experiment, q_name)
            self.stochastics.append(experiment.true_injection_heats)

            # Observed injection heats
            q_n_obs_name = "observed injection heats for experiment %d" % index
            experiment.observation = self._normal_observation_with_units(q_n_obs_name, experiment.true_injection_heats, experiment.observed_injection_heats, tau, ureg.microcalorie)
            self.stochastics.append(experiment.observation)

        # Create sampler.
        logger.info("Creating sampler...")
        mcmc = self._create_metropolis_sampler()

        self.mcmc = mcmc

    @staticmethod
    def equilibrium_concentrations(Ka_n, C0_R, C0_Ln, V, c0=None):
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

        # Define optimization functions
        def func(C_RLn):
            f_n = V * (x_R / V - C_RLn[:].sum()) * (x_Ln[:] / V - C_RLn[:]) * Ka_n[:] - V * C_RLn[:]
            return f_n

        def fprime(C_RLn):
            nspecies = C_RLn.size
            # G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]
            G_nm = numpy.zeros([nspecies, nspecies], numpy.float64)
            for n in range(nspecies):
                G_nm[n, :] = - V * (x_Ln[:] / V - C_RLn[:]) * Ka_n[:]
                G_nm[n, n] -= V * (Ka_n[n] * (x_R / V - C_RLn[:].sum()) + 1.0)
            return G_nm

        def sfunc(s):
            f_n = V * (x_R / V - (s[:] ** 2).sum()) * (x_Ln[:] / V - s[:] ** 2) * Ka_n[:] - V * s[:] ** 2
            return f_n

        def sfprime(s):
            nspecies = s.size
            # G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]
            G_nm = numpy.zeros([nspecies, nspecies], numpy.float64)
            for n in range(nspecies):
                G_nm[n, :] = - V * (x_Ln[:] / V - s[:] ** 2) * Ka_n[:]
                G_nm[n, n] -= V * (Ka_n[n] * (x_R / V - (s[:] ** 2).sum()) + 1.0)
                G_nm[n, :] *= 2. * s[n]
            return G_nm

        def objective(x):
            f_n = func(x)
            G_nm = fprime(x)

            obj = (f_n ** 2).sum()
            grad = 0.0 * f_n
            for n in range(f_n.size):
                grad += 2 * f_n[n] * G_nm[n, :]

            return (obj, grad)

        def ode(c_n, t, Ka_n, x_Ln, x_R):
            dc_n = - c_n[:] + Ka_n[:] * (x_Ln[:] / V - c_n[:]) * (x_R / V - c_n[:].sum())
            return dc_n

        def odegrad(c_n, t, Ka_n, x_Ln, x_R):
            N = c_n.size
            d2c = numpy.zeros([N, N], numpy.float64)
            for n in range(N):
                d2c[n, :] = -Ka_n[n] * (x_Ln[n] / V - c_n[n])
                d2c[n, n] += -(Ka_n[n] * (x_R / V - c_n[:].sum()) + 1.0)
            return d2c

        c = numpy.zeros([nspecies], numpy.float64)
        sorted_indices = numpy.argsort(-x_Ln)
        for n in range(nspecies):
            indices = sorted_indices[0:n + 1]
            c[indices] = scipy.optimize.fsolve(ode, c[indices], fprime=odegrad, args=(0.0, Ka_n[indices], x_Ln[indices], x_R), xtol=1.0e-6)
        C_RLn = c

        return C_RLn

    @staticmethod
    @ureg.wraps(ret=ureg.microcalorie, args=[None, None, ureg.liter, None, ureg.liter, ureg.mole / ureg.kilocalorie, None, None, None, None])
    def expected_injection_heats(ligands, receptor, V0, N, volumes, beta, true_cell_concentration, true_syringe_concentration, DeltaH_0, thermodynamic_parameters):
        """
        Expected heats of injection for two-component binding model.
        ligands - set of strings containing ligand name
        receptor - string with receptor name
        V0 - cell volume in liters
        N - int number of injections
        volumes - injection volumes in liters
        beta = 1 over temperature * R, in mole / kcal
        true_cell_concentration - (dict of floats) - concentrations[species] is the initial concentration of species in sample cell, or zero if absent (mM)
        true_syringe_concentration (dict of floats) - concentrations[species] is the initial concentration of species in sample cell, or zero if absent (mM)
        DeltaH_0, heat of injection (ucal)
        thermodynamic_parameters (dict of floats) - thermodynamic_parameters[parameter] is the value of thermodynamic parameter (kcal/mol)
          e.g. for parameter 'DeltaG of receptor * species'

        Returns
        -------
        expected_injection_heats (ucal)
        """
        # Number of ligand species
        nspecies = len(ligands)

        # Compute association constants for receptor and each ligand species.
        DeltaG_n = numpy.zeros([nspecies], numpy.float64)
        for (n, ligand) in enumerate(ligands):
            # determine name of free energy of binding for this ligand
            name = "DeltaG of %s * %s" % (receptor, ligand)
            # retrieve free energy of binding
            DeltaG_n[n] = thermodynamic_parameters[name]

        # compute association constant (1/M)
        Ka_n = numpy.exp(-beta * DeltaG_n[:])

        # Compute the quantity of each species in the sample cell after each injection.
        # NOTE: These quantities are correct for a perfusion-type model.  This would be modified for a cumulative model.
        # x_Ri[i] is the number of moles of receptor in sample cell after injection i
        x_Ri = numpy.zeros([N], numpy.float64)
        # x_Lin[i,n] is the number of moles of ligand n in sample cell after injection i
        x_Lin = numpy.zeros([N, nspecies], numpy.float64)
        dcum = 1.0  # cumulative dilution factor
        for index, volume in enumerate(volumes):
            d = 1.0 - (volume / V0)  # dilution factor (dimensionless)
            dcum *= d  # cumulative dilution factor (dimensionless)
            # converted from mM to M
            x_Ri[index] = true_cell_concentration[receptor] * 1.e-3 * dcum + true_syringe_concentration[receptor] * 1.e-3 * (1.0 - dcum)
            for (n, ligand) in enumerate(ligands):
                # converted from mM to M
                x_Lin[index, n] = true_cell_concentration[ligand] * 1.e-3 * dcum + true_syringe_concentration[ligand] * 1.e-3 * (1.0 - dcum)

        # Solve for initial concentration.
        # converted from mM to M
        x_R0 = true_cell_concentration[receptor] * 1.e-3
        x_L0n = numpy.zeros([nspecies], numpy.float64)
        C_RL0n = numpy.zeros([nspecies], numpy.float64)
        for (n, ligand) in enumerate(ligands):
            # converted from mM to M
            x_L0n[n] = true_cell_concentration[ligand] * 1.e-3
        C_RL0n[:] = CompetitiveBindingModel.equilibrium_concentrations(Ka_n, x_R0, x_L0n[:], V0)

        # Compute complex concentrations after each injection.
        # NOTE: The total cell volume would be modified for a cumulative model.
        # C_RLin[i,n] is the concentration of complex RLn[n] after injection i
        C_RLin = numpy.zeros([N, nspecies], numpy.float64)
        for index in range(N):
            C_RLin[index, :] = CompetitiveBindingModel.equilibrium_concentrations(Ka_n, x_Ri[index], x_Lin[index, :], V0)

        # Compile a list of thermodynamic parameters.
        # DeltaH_n[n] is the enthalpy of association of ligand species n
        DeltaH_n = numpy.zeros([nspecies], numpy.float64)
        for (n, ligand) in enumerate(ligands):
            name = "DeltaH of %s * %s" % (receptor, ligand)
            DeltaH_n[n] = thermodynamic_parameters[name]

        # Compute expected injection heats.
        # NOTE: This is for an instantaneous injection / perfusion model.
        q_n = DeltaH_0 * numpy.ones([N], numpy.float64)
        d = 1.0 - (volumes[0] / V0)  # dilution factor (dimensionless)
        for n in range(nspecies):
            # converted from kcal/mol to ucal
            q_n[0] += (1.e9 * DeltaH_n[n]) * V0 * (C_RLin[0, n] - d * C_RL0n[n])  # first injection
        for index, volume in enumerate(volumes[1:], start=1):
            d = 1.0 - (volume / V0)  # dilution factor (dimensionless)
            for n in range(nspecies):
                # subsequent injections
                # converted from kcal/mol to ucal
                q_n[index] += (1.e9 * DeltaH_n[n]) * V0 * (C_RLin[index, n] - d * C_RLin[index - 1, n])

        return q_n

    def _create_rescaling_sampler(self, receptor):
        """
        Create a sampler that uses RescalingStep for correlated variables
        """
        mcmc = self._create_metropolis_sampler()

        for experiment in self.experiments:
            for ligand in self.ligands:
                if isinstance(experiment.true_syringe_concentration[ligand], pymc.distributions.Lognormal):
                    mcmc.use_step_method(RescalingStep, {'Ls': experiment.true_syringe_concentration[ligand],
                                                         'P0': experiment.true_cell_concentration[receptor],
                                                         'DeltaH': self.thermodynamic_parameters[
                                                             'DeltaH of %s * %s' % (receptor, ligand)],
                                                         'DeltaG': self.thermodynamic_parameters[
                                                             'DeltaG of %s * %s' % (receptor, ligand)]}, self.beta)
        return mcmc

    def _create_metropolis_sampler(self):
        """Create a simple metropolis sampler for each stochastic"""
        mcmc = pymc.MCMC(self.stochastics, db='ram')
        for stochastic in self.stochastics:
            # print stochastic
            try:
                mcmc.use_step_method(pymc.Metropolis, stochastic)
            except Exception:
                pass

        return mcmc


    def _lambda_heats_model(self, experiment, q_name):
        """
        Model the heat using expected_injection_heats, providing all input by using a lambda function
        q_name is the name for the model
        """
        return pymc.Lambda(q_name,
                           lambda
                               ligands=self.ligands,
                               receptor=self.receptor,
                               V0=self.V0,
                               N=experiment.ninjections,
                               volumes=experiment.injection_volumes,
                               beta=self.beta,
                               cell_concentration=experiment.true_cell_concentration,
                               syringe_concentration=experiment.true_syringe_concentration,
                               DeltaH_0=experiment.DeltaH_0,
                               thermodynamic_parameters=self.thermodynamic_parameters:
                           self.expected_injection_heats(
                               ligands,
                               receptor,
                               V0,
                               N,
                               volumes,
                               beta,
                               cell_concentration,
                               syringe_concentration,
                               DeltaH_0,
                               thermodynamic_parameters
                           )
        )

    def _logsigma_guesses_from_multiple_experiments(self, standard_unit):
        """
        standard_unit: unit by which to correct the magnitude of sigma
        """
        # Determine min and max range for log_sigma (log of instrument heat measurement error)
        # TODO: This should depend on a number of factors, like integration time, heat signal, etc.?
        sigma_guess = 0.0
        for experiment in self.experiments:
            sigma_guess += experiment.observed_injection_heats[:-4].std()
        sigma_guess /= float(len(self.experiments))
        log_sigma_guess = log(sigma_guess / standard_unit)
        log_sigma_min = log_sigma_guess - 10
        log_sigma_max = log_sigma_guess + 5
        return log_sigma_guess, log_sigma_max, log_sigma_min

    @staticmethod
    def _species_from_experiments(experiments):
        species = set()  # all molecular species
        for experiment in experiments:
            species.update(experiment.cell_concentration.keys())
            species.update(experiment.syringe_concentration.keys())
        return species

    def _zero_for_missing__concentrations(self, experiment):
        for species in self.species:
            if species not in experiment.true_cell_concentration:
                experiment.true_cell_concentration[species] = 0.0
            if species not in experiment.true_syringe_concentration:
                experiment.true_syringe_concentration[species] = 0.0


# Container of all models that this module provides for use
known_models = {'TwoComponent': TwoComponentBindingModel,
                'Competitive': CompetitiveBindingModel,
                'BufferBuffer': BufferBufferModel,
                'WaterWater': BufferBufferModel,
                'Baseline': BaselineModel,
                'Dilution': TellinghuisenDilutionModel,
                'TitrantBuffer': TitrantBufferModel,
                'BufferTitrand': BufferTitrandModel,
                }
