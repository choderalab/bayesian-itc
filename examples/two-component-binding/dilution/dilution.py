import pymc
from bitc.report import analyze
from bitc.experiments import ExperimentMicroCal
from bitc.instruments import Instrument
from bitc.models import MultiExperimentModel
from bitc.units import ureg, Quantity
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

sns.despine(left=True)

datadir = 'examples/two-component-binding/dilution/'
autoitc = Instrument(itcfile='%sbufferbuffer.itc' % datadir)

# This will take a little while
# experiments = dict(bufferbuffer=ExperimentMicroCal('%sbufferbuffer.itc' % datadir, 'buffer_into_buffer', autoitc),
#                    buffertitrand=ExperimentMicroCal('%sbufferguest6.itc' % datadir, 'buffer_into_titrand', autoitc),
#                    titrantbuffer=ExperimentMicroCal('%shostbuffer.itc' % datadir, 'titrant_into_buffer', autoitc),
#                    titranttitrand=ExperimentMicroCal('%shostguest6.itc' % datadir, 'titrant_into_titrand', autoitc))
experiments = dict(titrantbuffer=ExperimentMicroCal('%shostbuffer.itc' % datadir, 'titrant_into_buffer', autoitc))


# for experiment in experiments.values():
# analyze(experiment.name, experiment)

model = MultiExperimentModel(experiments)
mcmc = model.mcmc

map = pymc.MAP(model)
map.fit(iterlim=1000000, verbose=0)
model.mcmc.sample(iter=50000, burn=20000, thin=20, progress_bar=True)

# Plot individual terms.

traces = dict()
for key in model.priors:
    if key == "log_sigma":
        traces[key] = numpy.exp(model.mcmc.trace(key)[:])
    else:
        traces[key] = model.mcmc.trace(key)[:]

predictions = dict()
for key in model.predictives:
    predictions[key] = model.mcmc.trace(key)[:]

observables = dict()
for key, value in model.observables.items():
    observables[key] = value._value

deterministics = dict()
for key in model.deterministics:
    deterministics[key] = model.mcmc.trace(key)[:]


def _one_two_subplot_grid():
    """
      Layout like
    |   1   |
    | 2 | 3 |

    returns axes objects, panels ordered as (1,2,3)
    """
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    ax2 = plt.subplot2grid((2, 2), (1, 0))
    ax3 = plt.subplot2grid((2, 2), (1, 1))
    return ax1, ax2, ax3


def plot_trace_accor_dist(trace, name, color='white', filename='', **figargs):
    """
    trace - one dim array of data
    name - name of data to plot
    color - color for plots
    filename - optional, if given will store plot instead of showing

    Additional parameters are passed onto plt.figure definition:
    see http://matplotlib.org/api/figure_api.html.
    """
    # Set figure parameters
    fig = plt.figure(**figargs)

    # Obtain a grid of plots
    ax1, ax2, ax3 = _one_two_subplot_grid()

    # Titles for plots
    ax1.set_title(name)
    ax2.set_title("Autocorrelation")
    ax3.set_title("Distribution")

    # Plots the trace from mcmc sampling
    ax1.plot(trace, color=color)

    # Lags for the autocorrelation function
    maxlags = min(len(trace) - 1, 100)

    # Mean trend is removed before plotting autocorrelation
    ax2.acorr(trace[:], detrend=mlab.detrend_mean, maxlags=maxlags, color=color)

    # Plots the distribution using a kde, and histogram is enabled
    sns.distplot(trace, hist=True, color=color, ax=ax3)

    # No y-ticks on the histogram
    plt.setp(ax3, yticks=[])

    # If filename was not given, it will show, else save as file
    if filename == '':
        plt.show()
    else:
        plt.savefig(filename)

    plt.close(fig)

    return


def nyandle(nyandle_coordinate, axes):
    """
    Supersecret bonus feature.

    nyandle_coordinate - 1D array, top of candlesticks
    axes - axes object to plot into

    Original idea by Sonya M. Hanson.
    """
    bottom = axes.get_ylim()[0] * numpy.ones(nyandle_coordinate.size)
    axes.bar(range(1, nyandle_coordinate.size + 1), bottom=nyandle_coordinate, height=bottom, color='w', align='center')


def plot_model_traces(heats_per_sample, axis, alpha=0.3, lw=0.2, color='black'):
    """
    Plot traces as lines
    heats_per_sample - ndarray (n,m) n models, m measurements/injections
    axis - matplotlib axis object to add traces to.
    alpha - float between 0,1, alpha of plot
    lw - float, linewidth of traces
    color - str, name of color for traces
    """

    # Adds one line plot for each individual trace
    for index, trace in enumerate(heats_per_sample):
        axis.plot(range(1, len(trace) + 1), trace, ls=':', lw=lw, color=color, alpha=alpha)

    return


def plot_posterior_predictive_enthalpogram(violin_data, measurement_data, traces_data=None, name='Posterior', nyandles=False,
                                           filename='', **figargs):
    """
    Plot posterior_predictive distribution as violins, observed measurements as line, plot deterministic (heats) model as line traces

    violin_data - numpy.ndarray (n,m) n samples from posterior predictive distribution, m measurements/injections
    measurement_data - numpy.ndarray (m), m measurements/injections
    traces_data - (n,m) n model traces, m measurements/injections
    name - str, plot title
    filename - str, if empty, show, else, save as filename

    Additional parameters are passed onto plt.figure definition:
    see http://matplotlib.org/api/figure_api.html.

    """
    # Set figure parameters
    fig = plt.figure(**figargs)
    sns.set(style="white")
    # Defining one main plot
    ax1 = plt.axes()
    ax1.set_title(name)

    if nyandles:
        violin_color = 'orange'
    else:
        violin_color = 'lightgray'

    # The posterior predictive distribution is plotted as a violin for each injection
    sns.violinplot(violin_data, color=violin_color)
    sns.despine(offset=10, trim=True);

    # If fitted model traces are supplied, plot them as black lines
    if traces_data is not None:
        plot_model_traces(traces_data, ax1)

    # This is a super secret bonus feature
    if nyandles:
        nyandle(measurement_data, ax1)
    # Plot the measurement data as a line graph
    else:
        ax1.plot(range(1, len(measurement_data) + 1), measurement_data, label='observation', marker='8', markersize=8, color='r', linestyle='')

    # If name not supplied, just show plot, else save figure under name supplied
    if filename == '':
        plt.show()
    else:
        plt.savefig(filename)

    plt.close(fig)

    return


def plot_cumulative_heat(model_heats, model_concentrations, integrated_heats, stated_concentrations, name, filename='', **figargs):
    """Plot cumulative heat vs ligand concentration"""
    fig = plt.figure(**figargs)
    sns.set(style="white")
    # Defining one main plot
    axis = plt.axes()
    axis.set_title(name)
    cum_model_heats = numpy.cumsum(model_heats)
    cum_integrated_heats = numpy.cumsum(integrated_heats)
    axis.plot(model_concentrations*1000, cum_model_heats, 'o', color='black', label='Model')
    axis.plot(stated_concentrations*1000, cum_integrated_heats, 'o', color='red', label='Observed')
    axis.legend(loc='best')
    axis.set_ylabel(r'Q ($\mu$cal)')
    axis.set_xlabel(r'[X$_s$] (mM)')
    if filename:
        plt.savefig(filename)
    else:
        plt.show()

    merged_table=numpy.column_stack((stated_concentrations,integrated_heats,model_concentrations,model_heats))
    numpy.savetxt("cumulative.txt", merged_table)

@ureg.wraps(ret=None,args=[None, ureg.liter,ureg.liter, None])
def titrant_concentrations(Xs, DeltaVn, V0, N):
    Xn=numpy.empty(N)
    vcum = 0.0  # cumulative injected volume (liter)
    for n in range(N):
        # Instantaneous injection model (perfusion)
        # dilution factor for this injection (dimensionless)
        vcum += DeltaVn[n]
        vfactor = vcum / V0  # relative volume factor
        # total concentration of ligand in sample cell after n injections (converted from mM to M)
        Xn[n] = 1.e-3 * Xs * (1 - numpy.exp(-vfactor))
    return Xn

def get_heats_concentrations_from_model(model, experiment):
    injection_heats, injection_volumes, n, name, temperature, beta, cell_volume = MultiExperimentModel._get_experimental_conditions(experiment)
    key = name + '_model'
    deterministic =  model.mcmc.trace(key)[:]

    heats = numpy.mean(deterministic, axis=0)

    syringe_concentration=numpy.mean(model.mcmc.trace('Xs')[:])
    concentrations = titrant_concentrations(syringe_concentration, injection_volumes,cell_volume, n)

    return heats, concentrations

def get_heats_concentrations_from_experiment(experiment):
    """Get data from experiment object"""
    injection_heats, injection_volumes, n, name, temperature, beta, cell_volume = MultiExperimentModel._get_experimental_conditions(experiment)
    syringe_concentration = next(iter(experiment.syringe_concentration.values()))
    concentrations = titrant_concentrations(syringe_concentration/(ureg.millimole / ureg.liter), injection_volumes,cell_volume, n)

    return injection_heats,concentrations


colors = sns.color_palette("husl", len(traces))
for index, (name, trace) in enumerate(traces.items()):
    color = colors[index]
    plot_trace_accor_dist(trace, name, color=color, figsize=(12, 8), tight_layout=True, filename=name+'.png')

for index, (name, observable) in enumerate(observables.items()):
    predictive = predictions[name + "_predictive"]
    deterministic = deterministics[name + "_model"]
    plot_posterior_predictive_enthalpogram(predictive, observable, traces_data=deterministic, name=name, tight_layout=True, filename=name+'.png')

heats, concentrations = get_heats_concentrations_from_model(model, model.experiments['titrantbuffer'])
integrated_heats, stated_concentrations = get_heats_concentrations_from_experiment(model.experiments['titrantbuffer'])
plot_cumulative_heat(heats,concentrations,integrated_heats, stated_concentrations,'titrant_buffer', filename=name+'_cum.png')

# Graph out the model
# pymc.graph.dag(model.mcmc)
