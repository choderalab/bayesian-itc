# Protocol for Bayesian analysis of ITC data.
from ITC import *
import Units

# Define the experiment.
experiment = Experiment()
experiment.title = "Determination of the binding affinity of KNI-764 by competition ITC"
experiment.temperature = 25 * Units.C
experiment.buffer = "10 mM acetate, pH 5, 2% DMSO"
experiment.calorimeter = Calorimeters.VPITC

# Define the ITC runs.
run = Run()
run.title = "Direct titration of KNI-764"
run.syringe['KNI-764'] = 300 * Units.uM
run.cell['HIV-1 protease'] = 20 * Units.uM
run.injection_volume = 10 * Units.uL
experiment.runs.append(run)

run = Run()
run.title = "Direct titration of acetyl pepstatin"
run.syringe['acetyl pepstatin'] = 200 * Units.uM
run.cell['HIV-1 protease'] = 20 * Units.uM
run.injection_volume = 10 * Units.uL
run.heat_per_injection = [7.347, 7.219, 7.024, 6.537, 5.470, 3.911, 2.258, 1.231, 0.744, 0.497, 0.302, 0.160, 0.087, 0.062, 0.062, 0.040, 0.017, -0.013, -0.013]
experiment.runs.append(run)

run = Run()
run.title = "Competition of acetyl pepstatin by KNI-764"
run.syringe['KNI-764'] = 250 * Units.uM
run.cell['HIV-1 protease'] = 20 * Units.uM
run.cell['acetyl pepstatin'] = 200 * Units.uM
run.injection_volume = 10 * Units.uL
experiment.runs.append(run)

# Run the analysis.
analyze(experiment)
