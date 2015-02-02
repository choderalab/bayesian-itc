"""
Contains Experiment and Injection classes.
"""
import os
from .units import ureg,Quantity
from math import pi
import logging
import numpy

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

    def __init__(self, data_filename):
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

        # Check to make sure we can access the file.
        if not os.access(data_filename, os.R_OK):
            raise "The file '%s' cannot be opened." % data_filename

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
                self.filter_period_end_time[
                    nmeasurements] = float(time) * ureg.second
                self.differential_power[nmeasurements] = float(
                    power) * ureg.microcalorie / ureg.second
                self.cell_temperature[nmeasurements] = (float(
                    temperature) + 273.15) * ureg.kelvin  # in Kelvin
                self.jacket_temperature[nmeasurements] = (float(
                    jacket_temperature) + 273.15) * ureg.kelvin  # in Kelvin

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
        self.fit_baseline()

        # Integrate heat evolved from each injection.
        self.integrate_heat()

        return

    def fit_baseline(self):
        """
        Fit the baseline using a simple shifted exponential functional form:

        y = c * exp[-k*(x-x0)] + y0

        where parameters (c, k, x0, y0) are fit parameters.

        """
        # TODO look for linearly interpolated fits, or @pgrinaway 's implementation using Gaussian process
        # TODO expose baseline to BindingModel as parameters
        import scipy.optimize

        def _eNegX_(p, x):
            [x0, y0, c, k] = p
            y = (c * numpy.exp(-k * (x - x0))) + y0
            return y

        def _eNegX_residuals(p, x, y):
            return y - _eNegX_(p, x)

        def _eNegX_error(p, x, y):
            return numpy.sum((y - _eNegX_(p, x)) ** 2)

        def Get_eNegX_Coefficients(x, y, p_guess):
            # Calls the leastsq() function, which calls the residuals function with an initial
            # guess for the parameters and with the x and y vectors.  Note that the residuals
            # function also calls the _eNegX_ function.  This will return the parameters p that
            # minimize the least squares error of the _eNegX_ function with respect to the original
            # x and y coordinate vectors that are sent to it.
            # [p, cov, infodict, mesg, ier] = scipy.optimize.leastsq(_eNegX_residuals,p_guess,args=(x,y),full_output=1,warning=True) # works with older scipy
            [p, cov, infodict, mesg, ier] = scipy.optimize.leastsq(
                _eNegX_residuals, p_guess, args=(x, y),
                full_output=1)  # works with EPD 7.0 scipy

            return p

        # Form list of data to fit.
        x = list()
        y = list()
        fit_indices = list()
        # Add data prior to first injection
        for index in range(0, self.injections[0].first_index):
            x.append(self.filter_period_end_time[index] / ureg.second)
            y.append(self.differential_power[index] / (ureg.microcalorie / ureg.second ))
        # Add last 5% of each injection.
        for injection in self.injections:
            start_index = injection.first_index
            end_index = injection.last_index + 1
            start_index = end_index - int((end_index - start_index) * 0.05)
            for index in range(start_index, end_index):
                x.append(self.filter_period_end_time[index] / ureg.second )
                y.append(self.differential_power[index] / (ureg.microcalorie / ureg.second))
                fit_indices.append(index)
        x = numpy.array(x)
        y = numpy.array(y)

        # Store list of data to which base line was fitted.
        self.baseline_fit_data = {'x': x, 'y': y, 'indices': fit_indices}

        logger.info("Fitting data:\n%s\n%s" % (x, y))

        # Perform nonlinear fit using multiple guesses.
        # Parameters are [x0, y0, c, k].
        p_guesses = list()
        p_guesses.append((numpy.median(x), numpy.min(y), numpy.max(y), 0.01))
        p_guesses.append((numpy.median(x), numpy.min(y), -numpy.max(y), -0.01))
        p_guesses.append((numpy.median(x), numpy.min(y), numpy.max(y), -0.01))
        p_guesses.append((numpy.median(x), numpy.min(y), -numpy.max(y), 0.01))
        p_fits = list()
        for p_guess in p_guesses:
            p = Get_eNegX_Coefficients(x, y, p_guess)
            p_fits.append(p)
        # Find best fit.
        minimal_error = _eNegX_error(p_fits[0], x, y)
        minimal_error_index = 0
        for index in range(1, len(p_fits)):
            error = _eNegX_error(p_fits[index], x, y)
            if error < minimal_error:
                minimal_error = error
                minimal_error_index = index
        p = p_fits[minimal_error_index]
        # Unpack fit parameters
        [x0, y0, c, k] = p
        xfit = self.filter_period_end_time[:] / ureg.second
        yfit = _eNegX_(p, xfit)

        logger.debug("Fit parameters: [x0, y0, c, k]\n%s" % p)

        # Store baseline fit parameters.
        self.baseline_fit_parameters = p

        # Store baseline
        self.baseline_power = ureg.Quantity(numpy.array(yfit), ureg.microcalorie / ureg.second)

        return

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
        # TODO implement read_integrated_heats function that overrides values
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


    def read_integrated_heats(self, heats_file, format=False):
        """

        :param heats_file:
        :type heats_file:
        :param format:
        :type format:
        :return:
        :rtype:
        """
        with open(heats_file) as heats:
            heats = self._parse_heats(heats_file, write_heats_compatible=False)

        if heats.size() != self.number_of_injections:
            raise ValueError("The number of injections does not match the number of integrated heats in %s" % heats_file)

        for inj, heat in enumerate(heats):
            self.injections[inj].evolved_heat = heat

    def _parse_heats(self, heats_file, write_heats_compatible=False):
        """
        Take as input a file with heats, format specification. Output a list of integrated heats in units of microcalorie

        :param heats_file:
        :type heats_file:
        :param write_heats_compatible:
        :type write_heats_compatible:
        :return:
        :rtype:
        """
        raise NotImplementedError

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

    def plot(self, filename=None, model=None):
        """
        Generate an enthalpogram plot showing fitted models.

        OPTIONAL ARGUMENTS
          filename (String) - if specified, the plot will be written to the specified file instead of plotted to the screen.

        """

        #import matplotlib
        #if (filename != None): matplotlib.use('pdf')

        import pylab
        pylab.figure()
        fontsize = 8
        markersize = 5

        #
        # Plot the raw measurements of differential power versus time and the enthalpogram.
        #

        pylab.subplot(211)
        pylab.hold(True)

        # Plot baseline fit.
        pylab.plot(
            self.filter_period_end_time / ureg.second, self.baseline_power /
            (ureg.microcalorie / ureg.second),
            'g-')

        # Plot differential power.
        pylab.plot(
            self.filter_period_end_time / ureg.second, self.differential_power /
            (ureg.microcalorie / ureg.second),
            'k.', markersize=markersize)

        # Plot injection time markers.
        [xmin, xmax, ymin, ymax] = pylab.axis()
        for injection in self.injections:
            # timepoint at start of syringe injection
            last_index = injection.first_index
            t = self.filter_period_end_time[last_index] / ureg.second
            pylab.plot([t, t], [ymin, ymax], 'r-')

        # Label plot axes.
        xlabel = pylab.xlabel('time / s')
        xlabel.set_fontsize(fontsize)
        ylabel = pylab.ylabel('differential power / ucal/s')
        ylabel.set_fontsize(fontsize)

        # Change tick label font sizes.
        ax = pylab.gca()
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)

        # title plot
        title = pylab.title(self.data_filename)
        title.set_fontsize(fontsize)

        pylab.hold(False)

        #
        # Plot integrated heats and model fits.
        #

        pylab.subplot(212)
        pylab.hold(True)

        # Determine injection end times.
        injection_end_times = numpy.zeros(
            [len(self.injections)],
            numpy.float64)
        for (index, injection) in enumerate(self.injections):
            # determine initial and final samples for injection
            # index of timepoint for first filtered differential power
            # measurement
            first_index = injection.first_index
            # index of timepoint for last filtered differential power
            # measurement
            last_index = injection.last_index
            # determine time at end of injection period
            injection_end_times[index] = self.filter_period_end_time[
                last_index] / ureg.second

        # Plot model fits, if specified.
        if model:
            P0_n = model.mcmc.trace('P0')[:]
            Ls_n = model.mcmc.trace('Ls')[:]
            DeltaG_n = model.mcmc.trace('DeltaG')[:]
            DeltaH_n = model.mcmc.trace('DeltaH')[:]
            DeltaH0_n = model.mcmc.trace('DeltaH_0')[:]
            N = DeltaG_n.size
            q_n = model.expected_injection_heats(model.V0, model.DeltaVn, P0_n, Ls_n, DeltaG_n, DeltaH_n, DeltaH0_n, model.beta,N)
            pylab.plot(
                injection_end_times /
                ureg.second,
                q_n /
                ureg.microcalorie,
                'r-',
                linewidth=1)

        # Plot integrated heats.
        for (index, injection) in enumerate(self.injections):
            # determine time at end of injection period
            t = injection_end_times[index] / ureg.second
            # plot a point there to represent total heat evolved in injection
            # period
            y = injection.evolved_heat / ureg.microcalorie
            pylab.plot(t, y, 'k.', markersize=markersize)
            # pylab.plot([t, t], [0, y], 'k-') # plot bar from zero line
            # label injection
            pylab.text(t, y, '%d' % injection.number, fontsize=6)

        # Adjust axes to match first plot.
        [xmin_new, xmax_new, ymin, ymax] = pylab.axis()
        pylab.axis([xmin, xmax, ymin, ymax])

        # Label axes.
        #pylab.title('evolved heat per injection')
        xlabel = pylab.xlabel('time / s')
        xlabel.set_fontsize(fontsize)
        ylabel = pylab.ylabel('evolved heat / ucal')
        ylabel.set_fontsize(fontsize)

        # Plot zero line.
        pylab.plot(experiment.filter_period_end_time /
                   ureg.second, 0.0 *
                   experiment.filter_period_end_time /
                   (ureg.microcalorie /
                    ureg.second), 'g-')  # plot zero line

        # Adjust font sizes for tick labels.
        ax = pylab.gca()
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)

        pylab.hold(False)

        #
        # Send plot to appropriate output device.
        #

        if filename is not None:
            # Save the plot to the specified file.
            pylab.savefig(filename, dpi=150)
        else:
            # Show plot.
            pylab.show()

        return

    def plot_baseline(self, filename=None):
        """
        Generate an close-up view of the baseline.

        OPTIONAL ARGUMENTS
          filename (String) - if specified, the plot will be written to the specified file instead of plotted to the screen.

        """

        #import matplotlib
        #if (filename != None): matplotlib.use('pdf')

        import pylab
        pylab.figure()
        fontsize = 8
        markersize = 5

        #
        # Plot close-up of baseline.
        #

        # pylab.subplot(212)
        pylab.hold(True)

        # Plot baseline fit.
        pylab.plot(
            self.filter_period_end_time / ureg.second, self.baseline_power /
            (ureg.microcalorie / ureg.second),
            'g-')

        # Plot differential power.
        indices = list(
            set(range(len(self.differential_power))) -
            set(self.baseline_fit_data['indices']))
        pylab.plot(
            self.filter_period_end_time[indices] /
            ureg.second,
            self.differential_power[indices] /
            (
                ureg.microcalorie /
                ureg.second),
            'k.',
            markersize=markersize)

        # Plot differential power.
        indices = self.baseline_fit_data['indices']
        pylab.plot(
            self.filter_period_end_time[indices] /
            ureg.second,
            self.differential_power[indices] /
            (
                ureg.microcalorie /
                ureg.second),
            'r.',
            markeredgecolor='r',
            markersize=markersize)

        # Plot injection time markers.
        [xmin, xmax, ymin, ymax] = pylab.axis()
        for injection in self.injections:
            # timepoint at start of syringe injection
            last_index = injection.first_index
            t = self.filter_period_end_time[last_index] / ureg.second
            pylab.plot([t, t], [ymin, ymax], 'r-')

        # Adjust axis to zoom in on baseline.
        ymax = self.baseline_power.max() / (ureg.microcalorie / ureg.second)
        ymin = self.baseline_power.min() / (ureg.microcalorie / ureg.second)
        width = ymax - ymin
        ymax += width / 2
        ymin -= width / 2
        pylab.axis([xmin, xmax, ymin, ymax])

        # Label plot axes.
        xlabel = pylab.xlabel('time / s')
        xlabel.set_fontsize(fontsize)
        ylabel = pylab.ylabel('differential power / ucal/s')
        ylabel.set_fontsize(fontsize)

        # Change tick label font sizes.
        ax = pylab.gca()
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)

        # title plot
        title = pylab.title(self.data_filename)
        title.set_fontsize(fontsize)

        pylab.hold(False)

        #
        # Send plot to appropriate output device.
        #

        if filename is not None:
            # Save the plot to the specified file.
            pylab.savefig(filename, dpi=150)
        else:
            # Show plot.
            pylab.show()

        return
