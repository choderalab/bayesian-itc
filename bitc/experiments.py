"""
Contains Experiment and Injection classes.
"""
import os
import logging

import numpy

from bitc.units import ureg,Quantity


# Use logger with name of module
logger = logging.getLogger(__name__)


class Injection(object):

    """
    Data from a single injection.

    Several types of information are stored about each injection:

    * the ordinal number of the injection
    * the programmed volume of the injection
    * duration of the injection
    * time between the beginning of the injection and the beginning of the next injection
    * filtering period over which data channel is averaged to produce a single measurement of applied power

    EXAMPLES

    """
    # TODO Add docstring examples.


    def __init__(self, number, volume, duration, spacing, filter_period, titrant_concentration=None):
        # sequence number of injection
        self.number = number
        # programmed volume of injection
        self.volume = volume
        # duration of injection
        self.duration = duration
        # time between beginning of injection and beginning of next injection
        self.spacing = spacing
        # time over which data channel is averaged to produce a single measurement
        # of applied power
        self.filter_period = filter_period

        # the quantity of compound(s) injected
        if titrant_concentration:
            self.contents(titrant_concentration)

    def contents(self, titrant_concentration):
        """
        Define the contents of what was injected

        Takes a list/array of concentrations
        """
        # Concentration of syringe contents
        self.titrant_concentration = Quantity(numpy.array(titrant_concentration), ureg.millimole / ureg.liter)

        self.titrant = Quantity(numpy.zeros(self.titrant_concentration.size), ureg.millimole)

        for titr in range(self.titrant_concentration.size):
            # Amount of titrant in the syringe (mole)
            if titr == 0:
                self.titrant[titr] = self.volume * self.titrant_concentration
            else:
                self.titrant[titr] = self.volume * self.titrant_concentration[titr]


class Experiment(object):

    """
    Data from an ITC experiment.

    The experiment consists of several types of data:

    * the instrument that was used
    * experimental conditions (temperature, stir speed, etc.)
    * concentrations of various components in syringe and sample cell
    * injection volumes and durations, collection times
    * time record of applied power and temperature difference

    """

    # TODO Add type verification

    def __init__(self, data_filename, experiment_name):
        """
        Initialize an experiment from a Microcal VP-ITC formatted .itc file.

        ARGUMENTS
          data_filename (String) - the filename of the Microcal VP-ITC formatted .itc file to initialize the experiment from

        TODO
          * Add support for other formats of datafiles (XML, etc.).

        """

        # Initialize.
        # the source filename from which data is read
        self.data_filename = None
        self.instrument = None  # the instrument that was used
        self.number_of_injections = None  # number of syringe injections
        self.target_temperature = None  # target temperature
        # initial equilibration (delay) time before injections
        self.equilibration_time = None
        self.stir_speed = None  # rate of stirring
        self.reference_power = None  # power applied to reference cell
        # concentrations of various species in syringe
        self.syringe_contents = list()
        # TODO syringe and cells could contain chemical contained objects
        # TODO as in chemicals.SimpleSolution in choderalab/itctools
        # concentrations of various species in sample cell
        self.sample_cell_contents = list()
        self.cell_volume = None  # volume of liquid in sample cell
        # list of injections (and their associated data)
        self.injections = list()
        # time at end of filtering period
        self.filter_period_end_time = None
        # time at midpoint of filtering period
        self.filter_period_midpoint_time = None
        # "differential" power applied to sample cell
        self.differential_power = None
        self.cell_temperature = None            # cell temperature
        self.name = experiment_name

        # Check to make sure we can access the file.
        if not os.access(data_filename, os.R_OK):
            raise IOError("The file '%s' cannot be opened." % data_filename)

        # Open the file and read is contents.
        infile = open(data_filename, 'r')
        lines = infile.readlines()
        infile.close()


        # Check the header to make sure it is a VP-ITC text-formatted .itc
        # file.
        if lines[0][0:4] != '$ITC':
            raise "File '%s' doesn't appear to be a Microcal VP-ITC data file." % data_filename

        # Store the datafile filename.
        self.data_filename = data_filename

        # Extract and store data about the experiment.
        self.number_of_injections = int(lines[1][1:].strip())
        self.target_temperature = (
            int(lines[3][1:].strip()) + 273.15 ) * ureg.kelvin   # convert from C to K
        self.equilibration_time = int(lines[4][1:].strip()) * ureg.second
        self.stir_rate = int(
            lines[5][
                1:].strip()) * ureg.revolutions_per_minute
        self.reference_power = float(
            lines[6][
                1:].strip()) * ureg.microcalorie / ureg.second

        # Extract and store metadata about injections.
        injection_number = 0
        for line in lines[10:]:
            if line[0] == '$':
                # Increment injection counter.
                injection_number += 1

                # Read data about injection.
                (injection_volume,
                 injection_duration,
                 spacing,
                 filter_period) = line[1:].strip().split(",")

                # Extract data for injection and apply appropriate unit
                # conversions.
                injectiondict = dict()
                injectiondict['number'] = injection_number
                injectiondict['volume'] = float(
                    injection_volume) * ureg.microliter  # volume of injection
                injectiondict['duration'] = float(
                    injection_duration) * ureg.second  # duration of injection
                # time between beginning of injection and beginning of next
                # injection
                injectiondict['spacing'] = float(spacing) * ureg.second
                # time over which data channel is averaged to produce a single
                # measurement
                injectiondict['filter_period'] = float(filter_period) * ureg.second

                # Store injection.
                self.injections.append(Injection(**injectiondict))

            else:
                break

        # Store additional data about experiment.
        parsecline = 11 + self.number_of_injections
        self.syringe_concentration = float(
            lines[parsecline][
                1:].strip()) * ureg.millimole / ureg.liter  # supposed concentration of compound in syringe
        for inj in self.injections:
            inj.contents(self.syringe_concentration) #TODO add support for multiple components
        # supposed concentration of receptor in cell
        self.cell_concentration = float(
            lines[parsecline + 1][1:].strip()) * ureg.millimole / ureg.liter

        self.cell_volume = float(
            lines[parsecline + 2][1:].strip()) * ureg.milliliter  # cell volume
        self.injection_tick = [0]

        # Allocate storage for power measurements.
        self.time = list()
        self.heat = list()
        self.temperature = list()

        # Extract lines containing heat measurements.
        for (index, line) in enumerate(lines):
            if line[:2] == '@0':
                break
        measurement_lines = lines[index:]

        # Count number of power measurements.
        nmeasurements = 0
        for line in measurement_lines:
            if line[0] != '@':
                nmeasurements += 1
        logger.info("There are %d power measurements." % nmeasurements)

        # Store data about measured heat liberated during each injection.
        self.filter_period_end_time = ureg.Quantity(numpy.zeros(
            [nmeasurements],
            numpy.float64), ureg.second)  # time at end of filtering period (s)
        self.differential_power = ureg.Quantity(numpy.zeros(
            [nmeasurements],
            numpy.float64), ureg.microcalorie / ureg.second)  # "differential" power applied to sample cell (ucal/s)
        self.cell_temperature = ureg.Quantity(numpy.zeros(
            [nmeasurements],
            numpy.float64), ureg.kelvin)  # cell temperature (K)
        self.jacket_temperature = ureg.Quantity(numpy.zeros(
            [nmeasurements],
            numpy.float64), ureg.kelvin)  # adiabatic jacket temperature (K)

        # Process data.
        # TODO this is a mess, need to clean up and do proper input verification
        nmeasurements = 0
        injection_labels = list()
        for (index, line) in enumerate(measurement_lines):
            if line[0] == '@':
                injection_labels.append(nmeasurements)
            else:
                # Extract data for power measurement.
                # TODO: Auto-detect file format?
                #
                jacket_temperature = 0.0
                try:
                    (time,
                     power,
                     temperature,
                     a,
                     jacket_temperature,
                     c,
                     d,
                     e,
                     f) = line.strip().split(",")  # Berkeley Auto iTC-200
                except:
                    try:
                        # works with Shoichet lab VP-ITC .itc files---what are
                        # other readings (a,b,c,d)?
                        (time,
                         power,
                         temperature,
                         a,
                         jacket_temperature,
                         c,
                         d) = line.strip().split(",")
                    # b looks like adiabatic jacket temperature (~1 degree C
                    # below sample temperature)
                    except:
                        # works with David Minh's VP-ITC .itc files
                        (time, power, temperature) = line.strip().split(",")

                # Store data about this measurement.
                self.filter_period_end_time[nmeasurements] = float(time) * ureg.second
                self.differential_power[nmeasurements] = float(power) * ureg.microcalorie / ureg.second
                self.cell_temperature[nmeasurements] = (float(temperature) + 273.15) * ureg.kelvin  # in Kelvin
                self.jacket_temperature[nmeasurements] = (float(jacket_temperature) + 273.15) * ureg.kelvin  # in Kelvin

                nmeasurements += 1
        # number of injections read, not including @0
        number_of_injections_read = len(injection_labels) - 1

        #print injection_labels

        # Perform a self-consistency check on the data to make sure all
        # injections are accounted for.
        if (number_of_injections_read != self.number_of_injections):
            logger.warning("Number of injections read (%d) is not equal to number of injections declared (%d)." % (number_of_injections_read, self.number_of_injections) +
                           "This is usually a sign that the experimental run was terminated prematurely." +
                           "The analysis will not include the final %d injections declared." % (self.number_of_injections - number_of_injections_read),
                            q)

            # Remove extra injections.
            self.injections = self.injections[0:number_of_injections_read]
            self.number_of_injections = number_of_injections_read

        # DEBUG
        logger.debug("self.injections has %d elements" % (len(self.injections)))

        # Annotate list of injections.
        for injection in self.injections:
            injection_number = injection.number
            logger.debug("%5d %8d" % (injection_number, injection_labels[injection_number]))
            injection.first_index = injection_labels[injection_number]
            if injection_number < len(injection_labels) - 1:
                injection.last_index = injection_labels[
                    injection_number + 1] - 1
            else:
                injection.last_index = nmeasurements - 1

        # Fit baseline.
        self.fit_gaussian_process_baseline()

        # Integrate heat evolved from each injection.
        self.integrate_heat()

        return

    @staticmethod
    def _plot_confidence_interval(axes, full_x, sigma, y_pred):
        # Confidence interval
        axes.fill(numpy.concatenate([full_x, full_x[::-1]]),
                  numpy.concatenate([y_pred - 1.9600 * sigma,
                                     (y_pred + 1.9600 * sigma)[::-1]]),
                  alpha=.7, fc='black', ec='None', label='95% confidence interval')


    def _plot_gaussian_baseline(self, full_x, full_y, sigma, x, y, y_pred):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

        figure = Figure()
        canvas = FigureCanvas(figure)
        axes = figure.add_subplot(1, 1, 1, axisbg='whitesmoke')

        # Adds a 95% confidence interval to the plot
        Experiment._plot_confidence_interval(axes, full_x, sigma, y_pred)
        # Entire set of data
        axes.plot(full_x, full_y, 'o', markersize=2, lw=1, color='deepskyblue', alpha=.5, label='Raw data')
        #Points for fit
        axes.plot(x, y, 'o', color='crimson', markersize=2, alpha=.8, label='Fitted data')
        # Prediction
        axes.plot(full_x, y_pred, 'o', markersize=1, mec='w', mew=1, color='k', alpha=.5, label='Predicted baseline')

        # Plot injection time markers.
        [ymin, ymax] = axes.get_ybound()
        for injection in self.injections:
            # timepoint at start of syringe injection
            last_index = injection.first_index
            t = self.filter_period_end_time[last_index] / ureg.second
            axes.plot([t, t], [ymin, ymax], '-', color='crimson')

        # Adjust axis to zoom in on baseline.
        ymax = self.baseline_power.max() / (ureg.microcalorie / ureg.second)
        ymin = self.baseline_power.min() / (ureg.microcalorie / ureg.second)
        width = ymax - ymin
        ymax += width / 2
        ymin -= width / 2
        axes.set_ybound(ymin, ymax)

        axes.set_xlabel('time (s)')
        axes.set_ylabel(r'differential power ($\mu$cal / s)')
        axes.legend(loc='upper center', bbox_to_anchor=(0.5, 0.1), ncol=4, fancybox=True, shadow=True, markerscale=3, prop={'size': 6})
        axes.set_title(self.data_filename)
        canvas.print_figure(self.name + '-baseline.png', dpi=500)

    def _plot_baseline_subtracted(self, x, y, raw=True, baseline=True):
        """Plot the baseline-subtracted data"""
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

        figure = Figure()
        canvas = FigureCanvas(figure)
        axes1 = figure.add_subplot(1, 1, 1, axisbg='whitesmoke')

        # Points for fit
        axes1.plot(x, y, 'o', color='deepskyblue', markersize=2, alpha=1, label='Baseline-subtracted data')
        axes1.set_xlabel('time (s)')
        axes1.set_ylabel(r' corr. differential power ($\mu$cal / s)')
        axes1.legend(loc='upper center', bbox_to_anchor=(0.2, 0.95), ncol=1, fancybox=True, shadow=True, markerscale=3,
                     prop={'size': 6})

        if raw:
            axes2 = axes1.twinx()
            axes2.plot(x, self.differential_power, 'o', color='gray', markersize=2, alpha=.3, label='Raw data')
            axes2.set_ylabel(r'raw differential power ($\mu$cal / s)')
            axes2.legend(loc='upper center', bbox_to_anchor=(0.8, 0.95), ncol=1, fancybox=True, shadow=True, markerscale=3,
                     prop={'size': 6})
            if baseline:
                axes2.plot(x, self.baseline_power, '-', color='black', alpha=.3, label='baseline')

        axes1.set_title(self.data_filename)
        canvas.print_figure(self.name + '-subtracted.png', dpi=500)

    def _retrieve_fit_indices(self, frac):
        """Form list of data to fit.
        """

        x = list()
        y = list()
        fit_indices = list()
        # Add data prior to first injection
        for index in range(0, self.injections[0].first_index):
            x.append(self.filter_period_end_time[index] / ureg.second)
            y.append(self.differential_power[index] / (ureg.microcalorie / ureg.second ))
            fit_indices.append(index)
        # Add last x% of each injection.
        for injection in self.injections:
            start_index = injection.first_index
            end_index = injection.last_index + 1
            start_index = end_index - int((end_index - start_index) * frac)
            for index in range(start_index, end_index):
                x.append(self.filter_period_end_time[index] / ureg.second)
                y.append(self.differential_power[index] / (ureg.microcalorie / ureg.second))
                fit_indices.append(index)

        x = numpy.array(x)
        y = numpy.array(y)
        fit_indices = numpy.array(fit_indices)
        return fit_indices, x, y

    def fit_gaussian_process_baseline(self, frac=0.1, theta0=4.7, nugget=1.0, plot=True):
        """
        Gaussian Process fit of baseline.

        frac = fraction of baseline to use for fit

        :return:
        :rtype:
        """
        from sklearn import gaussian_process

        # Retrieve a reduced set of data
        # (data up until first injection and x percent before every injection)
        fit_indices, x, y = self._retrieve_fit_indices(frac)

        # sklearn requires a 2d array, so make it pseudo 2d
        full_x = numpy.atleast_2d(self.filter_period_end_time).T
        x = numpy.atleast_2d(x).T

        full_y = numpy.array(self.differential_power).T
        y = numpy.array(y).T

        gp = gaussian_process.GaussianProcess(regr='quadratic', corr='squared_exponential', theta0=theta0, nugget=nugget,
                                              random_start=100)

        # Fit only based on the reduced set of the data
        gp.fit(x, y)
        y_pred, mean_squared_error = gp.predict(full_x, eval_MSE=True)
        sigma = numpy.sqrt(mean_squared_error)

        self.baseline_power = Quantity(y_pred, 'microcalories per second')
        self.baseline_fit_data = {'x': full_x, 'y': y_pred, 'indices': fit_indices}
        self.baseline_subtracted = self.differential_power - self.baseline_power

        if plot:
            self._plot_gaussian_baseline(full_x, full_y, sigma, x, y, y_pred)
            self._plot_baseline_subtracted(full_x, self.baseline_subtracted)

    def integrate_heat(self):
        """
        Compute the heat evolved from each injection from differental power timeseries data.

        """

        # Integrate heat produced by each injection.
        for injection in self.injections:
            # determine initial and final samples for injection i
            # index of timepoint for first filtered differential power
            # measurement
            first_index = injection.first_index
            # index of timepoint for last filtered differential power
            # measurement
            last_index = injection.last_index

            # Determine excess energy input into sample cell (with respect to reference cell) throughout this injection and measurement period.
            #excess_energy_input = injection['filter_period'] * (self.differential_power[first_index:(last_index+1)] - self.reference_power + self.baseline_power[first_index:(last_index+1)]).sum()
            excess_energy_input = injection.filter_period * (
                self.differential_power[
                    first_index:(
                        last_index + 1)] - self.baseline_power[
                    first_index:(
                        last_index + 1)]).sum()
            logger.debug("injection %d, filter period %f s, integrating sample %d to %d" % (injection.number, injection.filter_period / ureg.second, first_index, last_index))

            # Determine total heat evolved.
            evolved_heat = - excess_energy_input

            # Store heat evolved from this injection.
            injection.evolved_heat = evolved_heat


        return

    def __str__(self):
        """
        Show details of experiment in human-readable form.

        """
        # TODO Clean up this definition
        string = ""
        string += "EXPERIMENT\n"
        string += "\n"
        string += "Source filename: %s\n" % self.data_filename
        string += "Number of injections: %d\n" % self.number_of_injections
        string += "Target temperature: %.1f K\n" % (
            self.target_temperature / ureg.kelvin)
        string += "Equilibration time before first injection: %.1f s\n" % (
            self.equilibration_time / ureg.second)
        string += "Syringe concentration: %.3f mM\n" % (
            self.syringe_concentration / (ureg.millimole / ureg.liter))
        string += "Cell concentration: %.3f mM\n" % (
            self.cell_concentration / (ureg.millimole / ureg.liter))
        string += "Cell volume: %.3f ml\n" % (self.cell_volume / ureg.milliliter)
        string += "Reference power: %.3f ucal/s\n" % (
            self.reference_power / (ureg.microcalorie / ureg.second))

        string += "\n"
        string += "INJECTIONS\n"
        string += "\n"
        string += "%16s %24s %24s %24s %24s %24s\n" % (
            'injection', 'volume (uL)', 'duration (s)', 'collection time (s)',
            'time step (s)', 'evolved heat (ucal)')
#        for injection in range(self.number_of_injections):
#            string += "%16d %16.3f %16.3f %16.3f %16.3f" % (injection, self.injection_volume[injection] / unit.microliter, self.injection_duration[injection] / unit.second, self.collection_time[injection] / unit.second, self.time_step[injection] / unit.second)
        for injection in self.injections:
            string += "%16d %24.3f %24.3f %24.3f %24.3f %24.3f\n" % (
                injection.number,
                injection.volume / ureg.microliter, injection.duration / ureg.second,
                injection.spacing / ureg.second, injection.filter_period /
                ureg.second, injection.evolved_heat / ureg.microcalorie)

        return string

    def write_integrated_heats(self, filename):
        """
        Write integrated heats in a format similar to that used by Origin.
        """
        DeltaV = self.injections[0].volume
        V0 = self.cell_volume
        P0 = self.cell_concentration
        Ls = self.syringe_concentration

        string = "%12s %5s %12s %12s %12s %12s\n" % (
            "DH", "INJV", "Xt", "Mt", "XMt", "NDH")
        for (n, injection) in enumerate(self.injections):
            # Instantaneous injection model (perfusion)
            # d = 1.0 - (DeltaV / V0) # dilution factor (dimensionless)
            # P = V0 * P0 * d**(n+1) # total quantity of protein in sample cell after n injections (mol)
            # L = V0 * Ls * (1. - d**(n+1)) # total quantity of ligand in sample cell after n injections (mol)
            # PLn = 0.5/V0 * ((P + L + Kd*V0) - numpy.sqrt((P + L + Kd*V0)**2 - 4*P*L));  # complex concentration (M)
            # Pn = P/V0 - PLn; # free protein concentration in sample cell after n injections (M)
            # Ln = L/V0 - PLn; # free ligand concentration in sample cell after
            # n injections (M)

            Pn = 0.0 * (ureg.millimole / ureg.liter)
            Ln = 0.0 * (ureg.millimole / ureg.liter)
            PLn = 0.0 * (ureg.millimole / ureg.liter)
            NDH = 0.0  # review Not sure what this is

            # Form string.
            string += "%12.5f %5.1f %12.5f %12.5f %12.5f %12.5f\n" % (
                injection.evolved_heat / ureg.microcalorie, injection.volume /
                ureg.microliter, Pn / (ureg.millimole / ureg.liter), Ln / (ureg.millimole / ureg.liter), PLn / (ureg.millimole / ureg.liter), NDH)

        # Final line.
        string += "        --      %12.5f %12.5f --\n" % (Pn / (ureg.millimole / ureg.liter) , Ln / (ureg.millimole / ureg.liter))

        # Write file contents.
        outfile = open(filename, 'w')
        outfile.write(string)
        outfile.close()

        return

    def write_heats_csv(self, filename):
        """
         Write integrated heats in a csv format
        """
        DeltaV = self.injections[0].volume
        V0 = self.cell_volume
        P0 = self.cell_concentration
        Ls = self.syringe_concentration

        string = "%12s, %5s, %12s, %12s, %12s, %12s\n" % (
            "DH", "INJV", "Xt", "Mt", "XMt", "NDH")
        for (n, injection) in enumerate(self.injections):
            # Instantaneous injection model (perfusion)
            # d = 1.0 - (DeltaV / V0) # dilution factor (dimensionless)
            # P = V0 * P0 * d**(n+1) # total quantity of protein in sample cell after n injections (mol)
            # L = V0 * Ls * (1. - d**(n+1)) # total quantity of ligand in sample cell after n injections (mol)
            # PLn = 0.5/V0 * ((P + L + Kd*V0) - numpy.sqrt((P + L + Kd*V0)**2 - 4*P*L));  # complex concentration (M)
            # Pn = P/V0 - PLn; # free protein concentration in sample cell after n injections (M)
            # Ln = L/V0 - PLn; # free ligand concentration in sample cell after
            # n injections (M)

            Pn = 0.0 * (ureg.millimole / ureg.liter)
            Ln = 0.0 * (ureg.millimole / ureg.liter)
            PLn = 0.0 * (ureg.millimole / ureg.liter)
            NDH = 0.0  # review Not sure what this is

            # Form string.
            string += "%12.5f %5.1f %12.5f %12.5f %12.5f %12.5f\n" % (
                injection.evolved_heat / ureg.microcalorie, injection.volume /
                ureg.microliter, Pn / (ureg.millimole / ureg.liter), Ln / (ureg.millimole / ureg.liter),
                PLn / (ureg.millimole / ureg.liter), NDH)

        # Final line.
        string += "        --      %12.5f %12.5f --\n" % (
            Pn / (ureg.millimole / ureg.liter), Ln / (ureg.millimole / ureg.liter))

        # Write file contents.
        outfile = open(filename, 'w')
        outfile.write(string)
        outfile.close()

        return

    def read_integrated_heats(self, heats_file, unit='microcalorie'):
        """
        Read integrated heats from an origin file
        :param heats_file:
        :type heats_file:
        :return:
        :rtype:
        """
        heats = self._parse_heats(heats_file, unit)

        if heats.size != self.number_of_injections:
            raise ValueError("The number of injections does not match the number of integrated heats in %s" % heats_file)

        for inj, heat in enumerate(heats):
            self.injections[inj].evolved_heat = heat

    @staticmethod
    def _parse_heats(heats_file, unit):
        """
        Take as input a file with heats, format specification. Output a list of integrated heats in units of microcalorie

        :param heats_file:
        :type heats_file:
        :param write_heats_compatible:
        :type write_heats_compatible:
        :return:
        :rtype:
        """
        import pandas as pd

        assert isinstance(heats_file, str)
        dataframe = pd.read_table(heats_file, skip_footer=1, engine='python')  # Need python engine for skip_footer
        heats = numpy.array(dataframe['DH'])
        return Quantity(heats, unit)

    def write_power(self, filename):
        """
        DEBUG: Write power.

        """

        outfile = open(filename, 'w')
        outfile.write(
            "%%%7s %16s %16s\n" %
            ('time (s)', 'heat (ucal/s)', 'temperature (K)'))
        for index in range(len(self.filter_period_end_time)):
            outfile.write("%8.1f %16.8f %16.8f\n" %
                          (self.filter_period_end_time[index] /
                           ureg.second, self.differential_power[index] /
                           (ureg.microcalorie /
                            ureg.second), self.cell_temperature[index] /
                              ureg.kelvin))
        outfile.close()

        return




