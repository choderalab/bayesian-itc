import pymc
from bitc.report import analyze
from bitc.experiments import ExperimentMicroCal
from bitc.instruments import Instrument
from bitc.models import MultiExperimentModel
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

sns.set(style="white", palette="muted")
sns.despine(left=True)


datadir = 'examples/two-component-binding/dilution/'

autoitc = Instrument(itcfile='%sbufferbuffer.itc' % datadir)


# This will take a little while
experiments = dict(bufferbuffer=ExperimentMicroCal('%sbufferbuffer.itc' % datadir, 'buffer_into_buffer', autoitc),
                   buffertitrand=ExperimentMicroCal('%sbufferguest6.itc' % datadir, 'buffer_into_titrand', autoitc),
                   titrantbuffer=ExperimentMicroCal('%shostbuffer.itc' % datadir, 'titrant_into_buffer', autoitc),
                   titranttitrand=ExperimentMicroCal('%shostguest6.itc' % datadir, 'titrant_into_titrand', autoitc))

# for experiment in experiments.values():
#     analyze(experiment.name, experiment)

model = MultiExperimentModel(experiments)
mcmc = model.mcmc

map = pymc.MAP(model)
map.fit(iterlim=100000, verbose=1)
model.mcmc.sample(iter=1000000, burn=10000, thin=25, progress_bar=True)


# Plot individual terms.

data = dict()
for key in model.priors:
    if key == "log_sigma":
        data[key] = numpy.exp(model.mcmc.trace(key)[:])
    else:
        data[key] = model.mcmc.trace(key)[:]

colors = sns.color_palette("husl", len(data))

for index, (name, trace) in enumerate(data.items()):
    fig = plt.figure(num=None, figsize=(12,8), facecolor='w', edgecolor='k')

    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    ax2 = plt.subplot2grid((2, 2), (1, 0))
    ax3 = plt.subplot2grid((2, 2), (1, 1))

    ax1.set_title(name)
    ax2.set_title("Autocorrelation")
    ax3.set_title("Distribution")

    color = colors[index]
    ax1.plot(trace, color=color)
    maxlags = min(len(trace) - 1, 100)
    ax2.acorr(trace[:], detrend=mlab.detrend_mean, maxlags=maxlags, color=color)
    sns.distplot(trace, hist=True, color=color, ax=ax3)
    plt.setp(ax3, yticks=[])
    plt.tight_layout()
    plt.savefig(name + '_plot.pdf')
    plt.close()

# Graph out the model
# pymc.graph.dag(model.mcmc)

