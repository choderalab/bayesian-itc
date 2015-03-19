import pymc
from bitc.experiments import ExperimentMicroCal
from bitc.instruments import Instrument
from bitc.models import MultiExperimentModel
import sys

try:
    import seaborn
except ImportError:
    pass

datadir='examples/two-component-binding/dilution/'

autoitc=Instrument(itcfile='%sbufferbuffer.itc'%datadir)


# This will take a little while
experiments = dict(bufferbuffer=ExperimentMicroCal('%sbufferbuffer.itc'%datadir, 'buffer_into_buffer', autoitc),
                   buffertitrand=ExperimentMicroCal('%sbufferguest6.itc'%datadir, 'buffer_into_titrand', autoitc),
                   titrantbuffer=ExperimentMicroCal('%shostbuffer.itc'%datadir, 'titrant_into_buffer', autoitc),
                   titranttitrand=ExperimentMicroCal('%shostguest6.itc'%datadir, 'titrant_into_titrand', autoitc))

model = MultiExperimentModel(experiments)

print(model.observables)
print(model.stochastics)



