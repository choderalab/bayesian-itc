"""Example of translating experimental data into a correctly structured yaml file."""
import yaml
from glob import glob
import pprint

abrf_mirg10 = dict(
    experiment_name='abrf_mirg10',
    instrument='VPITC',
    concentration_unit='mole / liter',
    heat_unit='kilocalorie per mole',
    volume_unit='liter',
    temperature_unit='kelvin',
    sample_cell_concentrations={'carbonic anhydrase II': 32.e-6},
    syringe_concentrations={'4-carboxybenzenesulfonamide': 384.e-6},
    injection_heats=[-13.343, -13.417, -13.279, -13.199, -13.118, -12.781, -12.600, -12.124, -11.633, -10.921, -10.009, -8.810,
                     -7.661, -6.272, -5.163, -4.228, -3.519, -3.055, -2.599, -
                     2.512, -2.197, -2.096, -2.087, -1.959, -1.776, -1.879,
                     -1.894, -1.813, -1.740, -1.810],
    injection_volumes=[8.e-6] * 29,
    temperature=298.15
)

acetyl_pepstatin = dict(
    experiment_name='acetyl_pepstatin',
    instrument='VPITC',
    concentration_unit='mole / liter',
    heat_unit='kilocalorie per mole',
    volume_unit='liters',
    temperature_unit='kelvin',
    sample_cell_concentrations={'HIV protease': 20.e-6},
    syringe_concentrations={'acetyl pepstatin': 300.e-6},
    injection_heats=[6.696, 6.695, 6.698, 6.617, 6.464, 6.336, 6.184, 5.652, 4.336, 2.970, 1.709, 0.947, 0.643, 0.441, 0.264, 0.269,
                     0.214, 0.138, 0.113, 0.062, 0.088, 0.016, 0.063, 0.012],
    injection_volumes=[10.e-6] * 24,
    temperature=298.15
)

kni10033 = dict(
    experiment_name='kni10033',
    instrument='VPITC',
    concentration_unit='mole / liter',
    heat_unit='kilocalorie per mole',
    volume_unit='liters',
    temperature_unit='kelvin',
    sample_cell_concentrations={
        'HIV protease': 8.6e-6, 'acetyl pepstatin': 510.e-6},
    syringe_concentrations={'KNI-10033': 46.e-6},
    injection_heats=[-19.889, -19.896, -19.889, -19.797, -20.182, -19.889, -19.880, -19.849, -19.985, -19.716, -19.790, -19.654, -19.745, -
                     19.622, -19.457, -19.378, -18.908, -17.964, -16.490, -12.273, -7.370, -4.649, -3.626, -3.203, -2.987, -2.841, -2.906, -2.796, -2.927],
    injection_volumes=[10.e-6] * 29,
    temperature=298.15
)

kni10075 = dict(
    experiment_name='kni10075',
    instrument='VPITC',
    concentration_unit='mole / liter',
    heat_unit='kilocalorie per mole',
    volume_unit='liters',
    temperature_unit='kelvin',
    sample_cell_concentrations={
        'HIV protease': 8.6e-6, 'acetyl pepstatin': 510.e-6},
    syringe_concentrations={'KNI-10075': 46.e-6},
    injection_heats=[-21.012, -22.716, -22.863, -22.632, -22.480, -22.236, -22.314, -22.569, -22.231, -22.529, -22.529, -21.773, -21.866, -
                     21.412, -20.810, -18.664, -14.339, -11.028, -5.219, -3.612, -3.611, -3.389, -3.354, -3.122, -3.049, -3.083, -3.253, -3.089, -3.146, -3.252],
    injection_volumes=[10.e-6] * 30,
    temperature=298.15
)

for experiment in [abrf_mirg10, acetyl_pepstatin, kni10033, kni10075]:

    with open('{experiment_name}.yml'.format(**experiment), 'w') as outfile:
        outfile.write(yaml.dump(experiment, explicit_start=True))

pp = pprint.PrettyPrinter(indent=4)

for yml in glob("*.yml"):
    with open(yml, 'r') as ymlstream:
        pp.pprint(yaml.load(ymlstream))

    try:
        raw_input("Press Return to continue to the next file.")
    except NameError:
        input("Press Return to continue to the next file")
