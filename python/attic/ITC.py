# Bayesian analysis of ITC data.
import Units

# An ITC experiment, which may consist of one or more runs.
class Experiment:
    title = None                   # title of experiment
    calorimeter = None             # type of calorimeter (Calorimeter object)
    runs = list()                  # list of runs (Run object)
    protein = None                 # name of protein (string)
    ligands = list()               # list of ligands that bind competetively (strings)

# A single ITC run, used for defining the injection data.
class Run:
    # concentrations of species in the syringe
    syringe = dict()

    # concentrations of species in the cell
    cell = dict()

    # injection volumes
    injection_volumes = None

    # measured heat per injection, in kcal/(mol injectant)
    heat_per_injection = None

# Methods


def analyze(experiment):
    """Analyze an ITC experiment.

    ARGUMENTS
      experiment - the ITC experiment to analyze
    
    """

    print "experiment:"
    print experiment.title

    print "runs:"
    for run in experiment.runs:
        print run.title
    
