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

        self._id = 'RescalingMetropolis_' + \
            '_'.join([p.__name__ for p in self.stochastics])
        # State variables used to restore the state in a later session.
        self._state += ['max_scale', '_current_iter', 'interval']

        self.max_scale = max_scale
        self.beta = beta

        self._current_iter = 0
        self.interval = interval

        self.accepted = 0
        self.rejected = 0

        # Report
        logger.info("Initialization...\n" +
                    "max_scale: %s" % self.max_scale)

    def propose(self):
        # Choose trial scaling factor or its inverse with equal probability, so
        # that proposal move is symmetric.
        factor = (self.max_scale - 1) * numpy.random.rand() + 1
        if numpy.random.rand() < 0.5:
            factor = 1. / factor

        # Scale thermodynamic parameters and variables with this factor.
        self.dictionary['Ls'].value = self.dictionary['Ls'].value * factor
        self.dictionary['P0'].value = self.dictionary['P0'].value * factor
        self.dictionary['DeltaH'].value = self.dictionary[
            'DeltaH'].value / factor
        self.dictionary['DeltaG'].value = self.dictionary[
            'DeltaG'].value + (1. / self.beta.magnitude) * numpy.log(factor)
        # calling magnitude seems flaky, where are the units here?

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


class TwoComponentBindingModel(BindingModel):

    """
    A binding model with two components (e.g. Protein and Ligand)
    """

    def __init__(self, experiment):

        # Determine number of observations.
        self.N = experiment.number_of_injections

        self.DeltaVn = Quantity(numpy.zeros(self.N), ureg.microliter)
        # Store injection volumes
        for inj, injection in enumerate(experiment.injections):
            self.DeltaVn[inj] = injection.volume

        # Store calorimeter properties.
        self.V0 = experiment.cell_volume

        # Extract properties from experiment
        self.experiment = experiment

        if not len(experiment.syringe_concentration) == 1:
            raise ValueError('TwoComponent model only supports one component in the syringe, found %d' % len(
                experiment.syringe_concentration))

        # python 2/3 compatibility
        try:
            Ls_stated = experiment.syringe_concentration.itervalues().next()
        except AttributeError:
            Ls_stated = next(iter(experiment.syringe_concentration.values()))

        if not len(experiment.cell_concentration) == 1:
            raise ValueError('TwoComponent model only supports one component in the cell, found %d' % len(
                experiment.cell_concentration))

        # python 2/3 compatibility
        try:
            P0_stated = experiment.cell_concentration.itervalues().next()
        except AttributeError:
            P0_stated = next(iter(experiment.cell_concentration.values()))

        # Store temperature.
        self.temperature = experiment.target_temperature  # (kelvin)
        # inverse temperature 1/(kcal/mol)
        self.beta = 1.0 / (ureg.molar_gas_constant * self.temperature)

        # Compute uncertainties in stated concentrations.
        # uncertainty in protein stated concentration (M) - 10% error
        dP0 = 0.10 * P0_stated
        # uncertainty in ligand stated concentration (M) - 10% error
        dLs = 0.10 * Ls_stated

        # Determine guesses for initial values
        q_n = Quantity(
            numpy.zeros(len(experiment.injections)), 'microcalorie / mole')
        for inj, injection in enumerate(experiment.injections):
            # TODO reduce to one titrant (from .itc file)
            q_n[inj] = injection.evolved_heat / (numpy.sum(injection.titrant))

        # TODO better initial guesses for everything
        # review: how can we do this better?
        log_sigma_guess = log(q_n[-4:].std() / (ureg.microcalorie / ureg.mole))
        # todo add option to supply literature values
        DeltaG_guess = -8.3 * ureg.kilocalorie / ureg.mol
        DeltaH_guess = -12.0 * ureg.kilocalorie / ureg.mol

        # Assume the last injection has the best guess for H0
        DeltaH_0_guess = q_n[-1]  # ucal/injection

        # Determine min and max range for log_sigma
        log_sigma_min = log_sigma_guess - 10
        log_sigma_max = log_sigma_guess + 5

        # Determine range for priors for thermodynamic parameters.
        DeltaG_min = -40. * ureg.kilocalorie / ureg.mol  # (kcal/mol)
        DeltaG_max = +40. * ureg.kilocalorie / ureg.mol  # (kcal/mol)
        DeltaH_min = -100. * ureg.kilocalorie / ureg.mol  # (kcal/mol)
        DeltaH_max = +100. * ureg.kilocalorie / ureg.mol  # (kcal/mol)
        # review dH = dQ, so is the unit of H0 cal, or cal/mol? Where does the
        # mol come into the equation.
        heat_interval = (q_n.max() - q_n.min())
        DeltaH_0_min = q_n.min() - heat_interval  # (cal/mol)
        DeltaH_0_max = q_n.max() + heat_interval  # (cal/mol)

        # Define priors for concentrations.
        # TODO convert everything to a consistent unit system
        # review check out all the units to make sure that they're appropriate
        self.P0 = pymc.Lognormal('P0', mu=log(P0_stated / ureg.micromolar), tau=1.0 / log(
            1.0 + (dP0 / P0_stated) ** 2), value=P0_stated / ureg.micromolar)
        self.Ls = pymc.Lognormal('Ls', mu=log(Ls_stated / ureg.micromolar), tau=1.0 / log(
            1.0 + (dLs / Ls_stated) ** 2), value=Ls_stated / ureg.micromolar)

        # Define priors for thermodynamic quantities.
        self.log_sigma = pymc.Uniform(
            'log_sigma', lower=log_sigma_min, upper=log_sigma_max, value=log_sigma_guess)
        self.DeltaG = pymc.Uniform('DeltaG', lower=DeltaG_min / (ureg.kilocalorie / ureg.mol), upper=DeltaG_max / (
            ureg.kilocalorie / ureg.mol), value=DeltaG_guess / (ureg.kilocalorie / ureg.mol))
        self.DeltaH = pymc.Uniform('DeltaH', lower=DeltaH_min / (ureg.kilocalorie / ureg.mol), upper=DeltaH_max / (
            ureg.kilocalorie / ureg.mol), value=DeltaH_guess / (ureg.kilocalorie / ureg.mol))
        # review make sure we get the units right on this.
        self.DeltaH_0 = pymc.Uniform('DeltaH_0', lower=DeltaH_0_min / ureg.microcalorie,
                                     upper=DeltaH_0_max / ureg.microcalorie, value=DeltaH_0_guess / ureg.microcalorie)

        q_n_model = pymc.Lambda('q_n_model', lambda P0=self.P0, Ls=self.Ls, DeltaG=self.DeltaG, DeltaH=self.DeltaH, DeltaH_0=self.DeltaH_0:
                                self.expected_injection_heats(self.V0, self.DeltaVn, P0, Ls, DeltaG, DeltaH, DeltaH_0, self.beta, self.N))
        tau = pymc.Lambda(
            'tau', lambda log_sigma=self.log_sigma: self.tau(log_sigma))

        # Review doublecheck equation
        q_ns = Quantity(
            numpy.zeros(experiment.number_of_injections), 'microcalorie / mole')
        for inj, injection in enumerate(experiment.injections):
            q_ns[inj] = injection.evolved_heat / injection.titrant

        # Define observed data.
        self.q_n_obs = pymc.Normal(
            'q_n', mu=q_n_model, tau=tau, observed=True, value=q_ns / Quantity('microcalorie / mole'))

        # Create sampler.

        mcmc = pymc.MCMC(self, db='ram')
        mcmc.use_step_method(pymc.Metropolis, self.DeltaG)
        mcmc.use_step_method(pymc.Metropolis, self.DeltaH)
        mcmc.use_step_method(pymc.Metropolis, self.DeltaH_0)

        if P0_stated > Quantity('0.0 molar') and Ls_stated > Quantity('0.0 molar'):
            mcmc.use_step_method(RescalingStep,
                                 {'Ls': self.Ls, 'P0': self.P0,
                                     'DeltaH': self.DeltaH, 'DeltaG': self.DeltaG},
                                 self.beta)
        elif experiment.cell_concentration > Quantity('0.0 molar'):
            mcmc.use_step_method(pymc.Metropolis, self.P0)
        elif experiment.syringe_concentration > Quantity('0.0 molar'):
            mcmc.use_step_method(pymc.Metropolis, self.Ls)

        self.mcmc = mcmc
        return

    @staticmethod
    @ureg.wraps(ret=ureg.kilocalorie, args=[ureg.milliliter, ureg.milliliter, None, None, None, None, None,  ureg.mole / ureg.kilocalories, None], strict=True)
    def expected_injection_heats(V0, DeltaVn, P0, Ls, DeltaG, DeltaH, DeltaH_0, beta, N):
        """
        Expected heats of injection for two-component binding model.

        ARGUMENTS

        DeltaG - free energy of binding (kcal/mol)
        DeltaH - enthalpy of binding (kcal/mol)
        DeltaH_0 - heat of injection (cal/mol)

        """

        # TODO this can be removed at some point, or exposed to logger
        debug = True

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
            # total quantity of protein in sample cell after n injections (mol)
            P = V0 * P0 * dcum
            # total quantity of ligand in sample cell after n injections (mol)
            L = V0 * Ls * (1. - dcum)
            # complex concentration (M)
            PLn[n] = (
                0.5 / V0 * ((P + L + Kd * V0) - ((P + L + Kd * V0) ** 2 - 4 * P * L) ** 0.5))
            # free protein concentration in sample cell after n injections (M)
            Pn[n] = P / V0 - PLn[n]
            # free ligand concentration in sample cell after n injections (M)
            Ln[n] = L / V0 - PLn[n]

        # Compute expected injection heats.
        # q_n_model[n] is the expected heat from injection n
        q_n = numpy.zeros([N])
        # Instantaneous injection model (perfusion)
        # first injection # review removed a factor 1000 here, presumably
        # leftover from a unit conversion
        q_n[0] = (DeltaH) * V0 * PLn[0] + DeltaH_0
        for n in range(1, N):
            d = 1.0 - (DeltaVn[n] / V0)  # dilution factor (dimensionless)
            # subsequent injections # review removed a factor 1000 here,
            # presumably leftover from a unit conversion
            q_n[n] = DeltaH * V0 * (PLn[n] - d * PLn[n - 1]) + DeltaH_0

        return q_n

    @staticmethod
    def tau(log_sigma):
        """
        Injection heat measurement precision.

        """
        return numpy.exp(-2.0 * log_sigma)

    # TODO Add specific createModel() for this binding model (move from
    # ITC.py).


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
        logging.info("species '%s' will be treated as receptor" %
                     self.receptor)

        # Make a list of names of all molecular species.
        self.species = set()  # all molecular species
        for experiment in experiments:
            self.species.update(experiment.cell_concentration.keys())
            self.species.update(experiment.syringe_concentration.keys())
        logging.info("species: %s" % self.species)

        # Make a list of all ligands.
        self.ligands = copy.deepcopy(self.species)
        self.ligands.remove(receptor)
        logging.info("ligands: %s" % self.ligands)

        # Create a list of all stochastics.
        self.stochastics = list()

        # Create a prior for thermodynamic parameters of binding for each
        # ligand-receptor interaction.
        DeltaG_min = -40.  # (kcal/mol)
        DeltaG_max = +40.  # (kcal/mol)
        DeltaH_min = -100.  # (kcal/mol)
        DeltaH_max = +100.  # (kcal/mol)
        self.thermodynamic_parameters = dict()
        for ligand in self.ligands:
            name = "DeltaG of %s * %s" % (self.receptor, ligand)
            x = pymc.Uniform(
                name, lower=DeltaG_min, upper=DeltaG_max, value=0.0)
            self.thermodynamic_parameters[name] = x
            self.stochastics.append(x)
            name = "DeltaH of %s * %s" % (self.receptor, ligand)
            x = pymc.Uniform(
                name, lower=DeltaH_min, upper=DeltaH_max, value=0.0)
            self.thermodynamic_parameters[name] = x
            self.stochastics.append(x)
        logging.debug("thermodynamic parameters:")
        logging.debug(self.thermodynamic_parameters)

        # TODO: add option to set initial thermodynamic parameters to literature values.
        # self.thermodynamic_parameters["DeltaG of protein * ligand"].value = -9.0
        # self.thermodynamic_parameters["DeltaH of HIV protease * acetyl pepstatin"].value = +6.8

        # Determine min and max range for log_sigma (log of instrument heat measurement error)
        # TODO: This should depend on a number of factors, like integration
        # time, heat signal, etc.?
        sigma_guess = 0.0
        for experiment in self.experiments:
            sigma_guess += experiment.observed_injection_heats[:-4].std()
        sigma_guess /= float(len(self.experiments))
        log_sigma_guess = log(
            sigma_guess / Quantity('microcalorie'))  # remove unit
        log_sigma_min = log_sigma_guess - 10
        log_sigma_max = log_sigma_guess + 5
        self.log_sigma = pymc.Uniform(
            'log_sigma', lower=log_sigma_min, upper=log_sigma_max, value=log_sigma_guess)
        self.stochastics.append(self.log_sigma)
        tau = pymc.Lambda(
            'tau', lambda log_sigma=self.log_sigma: exp(-2.0 * log_sigma))
        self.stochastics.append(tau)

        # Define priors for unknowns for each experiment.
        for (index, experiment) in enumerate(self.experiments):
            # Number of observations
            experiment.ninjections = experiment.observed_injection_heats.size
            logging.info("Experiment %d has %d injections" %
                         (index, experiment.ninjections))

            # Heat of dilution / mixing
            # We allow the heat of dilution/mixing to range in observed range
            # of heats, plus a larger margin of the range of oberved heats.
            max_heat = experiment.observed_injection_heats.max()
            min_heat = experiment.observed_injection_heats.min()
            heat_interval = max_heat - min_heat
            # last injection heat provides a good initial guess for heat of
            # dilution/mixing
            last_heat = experiment.observed_injection_heats[-1]
            experiment.DeltaH_0 = pymc.Uniform(
                "DeltaH_0 for experiment %d" % index, lower=min_heat - heat_interval, upper=max_heat + heat_interval, value=last_heat)
            self.stochastics.append(experiment.DeltaH_0)

            # True concentrations
            experiment.true_cell_concentration = dict()
            for species, concentration in experiment.cell_concentration.iteritems():
                x = pymc.Lognormal("initial sample cell concentration of %s in experiment %d" % (species, index),
                                   mu=log(concentration / Quantity('millimole per liter')), tau=1.0 / log(1.0 + concentration_uncertainty ** 2),
                                   value=concentration / Quantity('millimole per liter'))
                experiment.true_cell_concentration[species] = x
                self.stochastics.append(x)

            experiment.true_syringe_concentration = dict()
            for species, concentration in experiment.syringe_concentration.iteritems():
                x = pymc.Lognormal("initial syringe concentration of %s in experiment %d" % (species, index),
                                   mu=log(concentration / Quantity('millimole per liter')), tau=1.0 / log(1.0 + concentration_uncertainty ** 2),
                                   value=concentration / Quantity('millimole per liter'))
                experiment.true_syringe_concentration[species] = x
                self.stochastics.append(x)

            # Add species not explicitly listed with zero concentration.
            for species in self.species:
                if species not in experiment.true_cell_concentration:
                    experiment.true_cell_concentration[species] = 0.0
                if species not in experiment.true_syringe_concentration:
                    experiment.true_syringe_concentration[species] = 0.0

            # True injection heats
            experiment.true_injection_heats = pymc.Lambda("true injection heats for experiment %d" % index,
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
            self.stochastics.append(experiment.true_injection_heats)

            # Observed injection heats
            experiment.observation = pymc.Normal("observed injection heats for experiment %d" % index,
                                                 mu=experiment.true_injection_heats, tau=tau,
                                                 observed=True, value=experiment.observed_injection_heats)
            self.stochastics.append(experiment.observation)

        # Create sampler.
        print("Creating sampler...")
        mcmc = pymc.MCMC(self.stochastics, db='ram')

        for stochastic in self.stochastics:
            # print stochastic
            try:
                mcmc.use_step_method(pymc.Metropolis, stochastic)
            except:
                pass

        for experiment in self.experiments:
            for ligand in self.ligands:
                if isinstance(experiment.true_syringe_concentration[ligand], pymc.distributions.Lognormal):
                    mcmc.use_step_method(RescalingStep, {'Ls': experiment.true_syringe_concentration[ligand],
                                                         'P0': experiment.true_cell_concentration[receptor],
                                                         'DeltaH': self.thermodynamic_parameters['DeltaH of %s * %s' % (receptor, ligand)],
                                                         'DeltaG': self.thermodynamic_parameters['DeltaG of %s * %s' % (receptor, ligand)]}, self.beta)

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
            f_n = V * \
                (x_R / V - C_RLn[:].sum()) * \
                (x_Ln[:] / V - C_RLn[:]) * Ka_n[:] - V * C_RLn[:]
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
            f_n = V * (x_R / V - (s[:] ** 2).sum()) * \
                (x_Ln[:] / V - s[:] ** 2) * Ka_n[:] - V * s[:] ** 2
            return f_n

        def sfprime(s):
            nspecies = s.size
            # G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]
            G_nm = numpy.zeros([nspecies, nspecies], numpy.float64)
            for n in range(nspecies):
                G_nm[n, :] = - V * (x_Ln[:] / V - s[:] ** 2) * Ka_n[:]
                G_nm[n, n] -= V * \
                    (Ka_n[n] * (x_R / V - (s[:] ** 2).sum()) + 1.0)
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
            dc_n = - c_n[:] + Ka_n[:] * \
                (x_Ln[:] / V - c_n[:]) * (x_R / V - c_n[:].sum())
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
            c[indices] = scipy.optimize.fsolve(ode, c[indices], fprime=odegrad, args=(
                0.0, Ka_n[indices], x_Ln[indices], x_R), xtol=1.0e-6)
        C_RLn = c

        return C_RLn

    @staticmethod
    @ureg.wraps(ret=ureg.microcalorie, args=[None, None, ureg.microliter, None, ureg.microliter, ureg.mole / ureg.kilocalorie, None, None, None, None])
    def expected_injection_heats(ligands, receptor, V0, N, volumes, beta, true_cell_concentration, true_syringe_concentration, DeltaH_0, thermodynamic_parameters):
        """
        Expected heats of injection for two-component binding model.

        TODO

        - Make experiment a dict, or somehow tell it how to replace members of 'experiment'?

        ARGUMENTS

        true_cell_concentration (dict of floats) - concentrations[species] is the initial concentration of species in sample cell, or zero if absent (M)
        true_syringe_concentration (dict of floats) - concentrations[species] is the initial concentration of species in sample cell, or zero if absent (M)
        thermodynamic_parameters (dict of floats) - thermodynamic_parameters[parameter] is the value of thermodynamic parameter (kcal/mol)
          e.g. for parameter 'DeltaG of receptor * species'
        V_n (numpy array of floats) - V_n[n] is injection volume of injection n (L)

        """
        # Todo get rid of units to make this much faster
        # Todo Potentially, make this a static method
        debug = False

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
        # NOTE: These quantities are correct for a perfusion-type model.  This
        # would be modified for a cumulative model.
        # x_Ri[i] is the number of moles of receptor in sample cell after
        # injection i
        x_Ri = numpy.zeros([N], numpy.float64)
        # x_Lin[i,n] is the number of moles of ligand n in sample cell after
        # injection i
        x_Lin = numpy.zeros([N, nspecies], numpy.float64)
        dcum = 1.0  # cumulative dilution factor
        for index, volume in enumerate(volumes):
            d = 1.0 - (volume / V0)  # dilution factor (dimensionless)
            dcum *= d  # cumulative dilution factor (dimensionless)
            x_Ri[index] = true_cell_concentration[receptor] * dcum + \
                true_syringe_concentration[receptor] * (1.0 - dcum)
            for (n, ligand) in enumerate(ligands):
                x_Lin[index, n] = true_cell_concentration[ligand] * \
                    dcum + true_syringe_concentration[ligand] * (1.0 - dcum)

        # Solve for initial concentration.
        x_R0 = true_cell_concentration[receptor]
        x_L0n = numpy.zeros([nspecies], numpy.float64)
        C_RL0n = numpy.zeros([nspecies], numpy.float64)
        for (n, ligand) in enumerate(ligands):
            x_L0n[n] = true_cell_concentration[ligand]
        C_RL0n[:] = CompetitiveBindingModel.equilibrium_concentrations(
            Ka_n, x_R0, x_L0n[:], V0)

        # Compute complex concentrations after each injection.
        # NOTE: The total cell volume would be modified for a cumulative model.
        # C_RLin[i,n] is the concentration of complex RLn[n] after injection i
        C_RLin = numpy.zeros([N, nspecies], numpy.float64)
        for index in range(N):
            C_RLin[index, :] = CompetitiveBindingModel.equilibrium_concentrations(
                Ka_n, x_Ri[index], x_Lin[index, :], V0)

        # Compile a list of thermodynamic parameters.
        # DeltaH_n[n] is the enthalpy of association of ligand species n
        DeltaH_n = numpy.zeros([nspecies], numpy.float64)
        for (n, ligand) in enumerate(ligands):
            name = "DeltaH of %s * %s" % (receptor, ligand)
            DeltaH_n[n] = thermodynamic_parameters[name]

        # Compute expected injection heats.
        # NOTE: This is for an instantaneous injection / perfusion model.
        # q_n_model[n] is the expected heat from injection n
        q_n = DeltaH_0 * numpy.ones([N], numpy.float64)
        d = 1.0 - (volumes[0] / V0)  # dilution factor (dimensionless)
        for n in range(nspecies):
            # review doublecheck order of magnitude units
            q_n[0] += (1000.0 * DeltaH_n[n]) * (V0) * \
                (C_RLin[0, n] - d * C_RL0n[n])  # first injection
        for index, volume in enumerate(volumes[1:], start=1):
            d = 1.0 - (volume / V0)  # dilution factor (dimensionless)
            for n in range(nspecies):
                # review doublecheck units
                # subsequent injections
                q_n[index] += (1000.0 * DeltaH_n[n]) * (V0) * \
                    (C_RLin[index, n] - d * C_RLin[index - 1, n])

        return q_n


# Container of all models that this module provides for use
known_models = {'TwoComponent': TwoComponentBindingModel,
                'Competitive': CompetitiveBindingModel,
                }
