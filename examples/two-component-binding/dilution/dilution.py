import pymc
from bitc.report import analyze
from bitc.experiments import ExperimentMicroCal
from bitc.instruments import Instrument
from bitc.models import MultiExperimentModel
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

sns.set(style="whitegrid")
sns.despine(left=True)


datadir = 'examples/two-component-binding/dilution/'

autoitc = Instrument(itcfile='%sbufferbuffer.itc' % datadir)


# This will take a little while
experiments = dict(bufferbuffer=ExperimentMicroCal('%sbufferbuffer.itc' % datadir, 'buffer_into_buffer', autoitc),
                   buffertitrand=ExperimentMicroCal('%sbufferguest6.itc' % datadir, 'buffer_into_titrand', autoitc),
                   titrantbuffer=ExperimentMicroCal('%shostbuffer.itc' % datadir, 'titrant_into_buffer', autoitc),
                   titranttitrand=ExperimentMicroCal('%shostguest6.itc' % datadir, 'titrant_into_titrand', autoitc))
# experiments = dict(titranttitrand=ExperimentMicroCal('%shostguest6.itc' % datadir, 'titrant_into_titrand', autoitc))


# for experiment in experiments.values():
#     analyze(experiment.name, experiment)

model = MultiExperimentModel(experiments)
mcmc = model.mcmc

map = pymc.MAP(model)
map.fit(iterlim=100000, verbose=1)
model.mcmc.sample(iter=10000, burn=1000, thin=2, progress_bar=True)


# Plot individual terms.

data = dict()
for key in model.priors:
    if key == "log_sigma":
        data[key] = numpy.exp(model.mcmc.trace(key)[:])
    else:
        data[key] = model.mcmc.trace(key)[:]

predictions = dict()
for key in model.predictives:
    predictions[key] = model.mcmc.trace(key)[:]

observables = dict()
for key, value in model.observables.items():
    observables[key] = value._value


colors = sns.color_palette("husl", len(data))


def _one_two_subplot_grid():
    """
      Layout like
    |   1   |
    | 2 | 3 |
    """
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    ax2 = plt.subplot2grid((2, 2), (1, 0))
    ax3 = plt.subplot2grid((2, 2), (1, 1))
    return ax1, ax2, ax3


def plot_trace_accor_dist(trace, name, color='k', filename='', **figargs):
    """
    trace - one dim array of data
    name - name of data to plot
    index - if part of a set, used for color matching

    Additional parameters are passed onto plt.figure definition:
    see http://matplotlib.org/api/figure_api.html.

    """
    fig = plt.figure(**figargs)
    ax1, ax2, ax3 = _one_two_subplot_grid()

    ax1.set_title(name)
    ax2.set_title("Autocorrelation")
    ax3.set_title("Distribution")

    ax1.plot(trace, color=color)
    maxlags = min(len(trace) - 1, 100)
    ax2.acorr(trace[:], detrend=mlab.detrend_mean, maxlags=maxlags, color=color)
    sns.distplot(trace, hist=True, color=color, ax=ax3)
    "_predictive"

    plt.setp(ax3, yticks=[])

    if filename == '':
        plt.savefig(name + '_trace_plot.pdf')
    else:
        plt.savefig(filename)

    plt.close()


#TODO candle plots, idea by Sonya Hanson

def plot_posterior_predictive_enthalpogram(prediction, observable, name):
    colors = sns.color_palette("hls", prediction.shape[1])
    ax1 = plt.axes()
    ax1.set_title(name)
    sns.violinplot(prediction, color=colors)
    # for index, injection in enumerate(prediction.transpose()):
    #     sns.distplot(injection, hist=True, color=colors[index], ax=ax1)
    ax1.plot(range(1, len(observable)+1), observable, marker='h', c='lightgray', markersize=8, color='w')
    plt.show()
    plt.close()


for index, (name, trace) in enumerate(data.items()):
    color = colors[index]
    plot_trace_accor_dist(trace, name, color=color, figsize=(12,8), tight_layout=True)

for index, (name, prediction) in enumerate(predictions.items()):
    observable = observables[name[:-11]]
    plot_posterior_predictive_enthalpogram(prediction, observable, name)


# Graph out the model
# pymc.graph.dag(model.mcmc)
