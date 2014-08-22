#!/usr/bin/python

#=============================================================================================
# A module implementing Bayesian analysis of isothermal titration calorimentry (ITC) experiments
#
# Written by John D. Chodera <jchodera@gmail.com>, Pande lab, Stanford, 2008.
#
# Copyright (c) 2008 Stanford University.  All Rights Reserved.
#
# All code in this repository is released under the GNU General Public License.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#  
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#=============================================================================================

#=============================================================================================
# NOTES
# * Throughout, quantities with associated units employ the Units.py class to store quantities
# in references units.  Multiplication or division by desired units should ALWAYS be used to
# store or extract quantities in the desired units.
#=============================================================================================

#=============================================================================================
# TODO
# * Use simtk.unit instead of Units.py?
# * Create subclass of Instrument for VP-ITC.
#=============================================================================================

#=============================================================================================
# IMPORTS
#=============================================================================================

import os
import Units
import Constants

import numpy
import scipy.stats
#from numpy import *
import pymc

#=============================================================================================
# Isothermal titration calorimeter instrument class.
#=============================================================================================

class Instrument(object):
    """
    An isothermal titration calorimeter instrument.

    An instrument object consists of several types of data:

    * the manufacturer and model of the instrument
    * properites of the instrument (sample cell volume)
    
    """

    def __init__(self):
        self.V0 = None # volume of calorimeter sample cell
        pass

class VPITC(Instrument):
    """
    The MicroCal VP-ITC.

    """

    def __init__(self):
        self.V0 = 1.4301 * Units.mL # volume of calorimeter sample cell
        self.V0 = self.V0 - 0.044 * Units.mL # Tellinghuisen volume correction for VP-ITC
        return
    
#=============================================================================================
# Injection class.
#=============================================================================================

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
    
    #=============================================================================================
    # Class data.
    #=============================================================================================

    number = None # sequence number of injection
    volume = None # programmed volume of injection
    duration = None # duration of injection 
    spacing = None # time between beginning of injection and beginning of next injection
    filter_period = None # time over which data channel is averaged to produce a single measurement of applied power

    def __init__(self):
        pass

#=============================================================================================
# ITC Experiment class
#=============================================================================================

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

    #=============================================================================================
    # Class data.
    #=============================================================================================
    
    #=============================================================================================
    # Methods.
    #=============================================================================================
    
    def __init__(self, data_filename):
        """
        Initialize an experiment from a Microcal VP-ITC formatted .itc file.

        ARGUMENTS
          data_filename (String) - the filename of the Microcal VP-ITC formatted .itc file to initialize the experiment from

        TODO
          * Add support for other formats of datafiles (XML, etc.).

        """

        # Initialize.
        self.data_filename = None # the source filename from which data is read
        self.instrument = None # the instrument that was used
        self.number_of_injections = None # number of syringe injections
        self.target_temperature = None # target temperature
        self.equilibration_time = None # initial equilibration (delay) time before injections 
        self.stir_speed = None # rate of stirring
        self.reference_power = None # power applied to reference cell
        self.syringe_contents = list() # concentrations of various species in syringe
        self.sample_cell_contents = list() # concentrations of various species in sample cell
        self.cell_volume = None # volume of liquid in sample cell        
        self.injections = list() # list of injections (and their associated data)        
        self.filter_period_end_time = None      # time at end of filtering period
        self.filter_period_midpoint_time = None # time at midpoint of filtering period
        self.differential_power = None          # "differential" power applied to sample cell
        self.cell_temperature = None            # cell temperature
        
        # Check to make sure we can access the file.
        if not os.access(data_filename, os.R_OK):
            raise "The file '%s' cannot be opened." % data_filename
        
        # Open the file and read is contents.
        infile = open(data_filename, 'r')
        lines = infile.readlines()
        infile.close()

        # Check the header to make sure it is a VP-ITC text-formatted .itc file.
        if lines[0][0:4] != '$ITC':
            raise "File '%s' doesn't appear to be a Microcal VP-ITC data file." % filename

        # Store the datafile filename.
        self.data_filename = data_filename

        # Extract and store data about the experiment.
        self.number_of_injections = int(lines[1][1:].strip()) 
        self.target_temperature = (int(lines[3][1:].strip())) * Units.K + Constants.absolute_zero # convert from C to K
        self.equilibration_time = int(lines[4][1:].strip()) * Units.s
        self.stir_rate = int(lines[5][1:].strip()) * Units.RPM # revolutions per minute
        self.reference_power = float(lines[6][1:].strip()) * Units.ucal / Units.s

#        # Injection 0 is just power measurements before first injection begins.
#        injection = dict()
#        injection['number'] = 0
#        injection['volume'] = 0.0 * Units.ul # volume of injection
#        injection['duration'] = 0.0 * Units.s # duration of injection 
#        injection['spacing'] = 0.0 * Units.s # time between beginning of injection and beginning of next injection
#        injection['filter_period'] = 0.0 * Units.s # time over which data channel is averaged to produce a single measurement        
#        self.injections.append(injection)
        
        # Extract and store metadata about injections.
        injection_number = 0
        for line in lines[10:]:
            if line[0]=='$':
                # Increment injection counter.
                injection_number += 1
            
                # Read data about injection.
                (injection_volume, injection_duration, spacing, filter_period) = line[1:].strip().split(",")

#                # Extract data for injection, applying appropriate unit conversions.
#                injection = Injection()
#                injection.number = injection_number # sequence number of injection
#                injection.volume = float(injection_volume) * Units.ul # volume of injection
#                injection.duration = float(injection_duration) * Units.s # duration of injection 
#                injection.spacing = float(spacing) * Units.s # time between beginning of injection and beginning of next injection
#                injection.filter_period = float(filter_period) * Units.s # time over which data channel is averaged to produce a single measurement
#
#                # Store the injection
#                self.injections.append(injection)
                
                # Extract data for injection and apply appropriate unit conversions.                
                injection = dict()
                injection['number'] = injection_number
                injection['volume'] = float(injection_volume) * Units.ul # volume of injection
                injection['duration'] = float(injection_duration) * Units.s # duration of injection 
                injection['spacing'] = float(spacing) * Units.s # time between beginning of injection and beginning of next injection
                injection['filter_period'] = float(filter_period) * Units.s # time over which data channel is averaged to produce a single measurement

                # Store injection.
                self.injections.append(injection)

            else:
                break

        # Store additional data about experiment.
        parsecline = 11 + self.number_of_injections
        self.syringe_concentration = float(lines[parsecline][1:].strip()) * Units.mM # supposed concentration of compound in syringe
        self.cell_concentration = float(lines[parsecline+1][1:].strip()) * Units.mM # supposed concentration of receptor in cell
        self.cell_volume = float(lines[parsecline+2][1:].strip()) * Units.ml # cell volume
        self.injection_tick = [0] 

        # Allocate storage for power measurements.
        self.time = list() 
        self.heat = list()
        self.temperature = list()

        # Extract lines containing heat measurements.
        for (index,line) in enumerate(lines):
            if line[:2]=='@0':
                break
        measurement_lines = lines[index:]

        # Count number of power measurements.
        nmeasurements = 0
        for line in measurement_lines:
            if line[0] != '@':
                nmeasurements += 1
        print "There are %d power measurements." % nmeasurements
                            
        # Store data about measured heat liberated during each injection.
        self.filter_period_end_time = numpy.zeros([nmeasurements], numpy.float64) # time at end of filtering period (s)
        self.differential_power = numpy.zeros([nmeasurements], numpy.float64) # "differential" power applied to sample cell (ucal/s)
        self.cell_temperature = numpy.zeros([nmeasurements], numpy.float64) # cell temperature (K)
        self.jacket_temperature = numpy.zeros([nmeasurements], numpy.float64) # adiabatic jacket temperature (K)

        # Process data.
        nmeasurements = 0
        injection_labels = list()
        for (index,line) in enumerate(measurement_lines):
            if line[0]=='@':
                injection_labels.append(nmeasurements)
            else:
                # Extract data for power measurement.
                # TODO: Auto-detect file format?
                #
                jacket_temperature = 0.0
                try:
                    (time, power, temperature, a, jacket_temperature, c, d, e, f) = line.strip().split(",") # Berkeley Auto iTC-200
                except:
                    try:
                        (time, power, temperature, a, jacket_temperature, c, d) = line.strip().split(",") # works with Shoichet lab VP-ITC .itc files---what are other readings (a,b,c,d)?
                    except:                                                                               # b looks like adiabatic jacket temperature (~1 degree C below sample temperature)
                        (time, power, temperature) = line.strip().split(",") # works with David Minh's VP-ITC .itc files                
                
                # Store data about this measurement.
                self.filter_period_end_time[nmeasurements] = float(time) * Units.s 
                self.differential_power[nmeasurements] = float(power) * Units.ucal/Units.s 
                self.cell_temperature[nmeasurements] = float(temperature) + Constants.absolute_zero  # in Kelvin
                self.jacket_temperature[nmeasurements] = float(jacket_temperature) + Constants.absolute_zero  # in Kelvin

                nmeasurements += 1
        number_of_injections_read = len(injection_labels) - 1# number of injections read, not including @0

        print injection_labels
                        
        # Perform a self-consistency check on the data to make sure all injections are accounted for.        
        if (number_of_injections_read != self.number_of_injections):
            print 'WARNING'
            print 'Number of injections read (%d) is not equal to number of injections declared (%d).' % (number_of_injections_read, self.number_of_injections)
            print 'This is usually a sign that the experimental run was terminated prematurely.'
            print 'The analysis will not include the final %d injections declared.' % (self.number_of_injections - number_of_injections_read)

            # Remove extra injections.
            self.injections = self.injections[0:number_of_injections_read]
            self.number_of_injections = number_of_injections_read

        # DEBUG
        print "self.injections has %d elements" % (len(self.injections))
        
        # Annotate list of injections.
        for injection in self.injections:
            injection_number = injection['number']
            print "%5d %8d" % (injection_number, injection_labels[injection_number])
            injection['first_index'] = injection_labels[injection_number]
            if (injection_number < len(injection_labels)-1):
                injection['last_index'] = injection_labels[injection_number+1] - 1
            else:
                injection['last_index'] = nmeasurements - 1

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
        
        import scipy.optimize    

        def _eNegX_(p,x):
            [x0,y0,c,k] = p
            y = (c * numpy.exp(-k*(x-x0))) + y0
            return y

        def _eNegX_residuals(p,x,y):
            return y - _eNegX_(p,x)

        def _eNegX_error(p,x,y):
            return numpy.sum( (y - _eNegX_(p,x))**2 )

        def Get_eNegX_Coefficients(x,y,p_guess):
            # Calls the leastsq() function, which calls the residuals function with an initial
            # guess for the parameters and with the x and y vectors.  Note that the residuals
            # function also calls the _eNegX_ function.  This will return the parameters p that
            # minimize the least squares error of the _eNegX_ function with respect to the original
            # x and y coordinate vectors that are sent to it.
            #[p, cov, infodict, mesg, ier] = scipy.optimize.leastsq(_eNegX_residuals,p_guess,args=(x,y),full_output=1,warning=True) # works with older scipy
            [p, cov, infodict, mesg, ier] = scipy.optimize.leastsq(_eNegX_residuals,p_guess,args=(x,y),full_output=1) # works with EPD 7.0 scipy

            return p

        # Form list of data to fit.
        x = list()
        y = list()
        fit_indices = list()
        # Add data prior to first injection
        for index in range(0, self.injections[0]['first_index']):
            x.append(self.filter_period_end_time[index])
            y.append(self.differential_power[index])
        # Add last 5% of each injection.
        for injection in self.injections:
            start_index = injection['first_index']
            end_index = injection['last_index'] + 1
            start_index = end_index - int((end_index - start_index) * 0.05)
            for index in range(start_index,end_index):                
                x.append(self.filter_period_end_time[index])
                y.append(self.differential_power[index])
                fit_indices.append(index)
        x = numpy.array(x)
        y = numpy.array(y)

        # Store list of data to which base line was fitted.
        self.baseline_fit_data = { 'x' : x, 'y' : y, 'indices' : fit_indices }

        print "Fitting data:"
        print x
        print y

        # Perform nonlinear fit using multiple guesses.
        # Parameters are [x0, y0, c, k].
        p_guesses = list()
        p_guesses.append( (numpy.median(x), numpy.min(y), numpy.max(y), 0.01) )
        p_guesses.append( (numpy.median(x), numpy.min(y), -numpy.max(y), -0.01) )
        p_guesses.append( (numpy.median(x), numpy.min(y), numpy.max(y), -0.01) )
        p_guesses.append( (numpy.median(x), numpy.min(y), -numpy.max(y), 0.01) )        
        p_fits = list()
        for p_guess in p_guesses:
            p = Get_eNegX_Coefficients(x,y,p_guess)
            p_fits.append(p)
        # Find best fit.
        minimal_error = _eNegX_error(p_fits[0], x, y)
        minimal_error_index = 0
        for index in range(1,len(p_fits)):
            error = _eNegX_error(p_fits[index], x, y)
            if (error < minimal_error):
                minimal_error = error
                minimal_error_index = index
        p = p_fits[minimal_error_index]
        # Unpack fit parameters
        [x0,y0,c,k] = p
        xfit = self.filter_period_end_time[:]
        yfit = _eNegX_(p,xfit)

        # DEBUG
        print "Fit parameters: [x0, y0, c, k]"
        print p        

        # Store baseline fit parameters.
        self.baseline_fit_parameters = p

        # Store baseline
        self.baseline_power = numpy.array(yfit)        
        
        return 

    def integrate_heat(self):
        """
        Compute the heat evolved from each injection from differental power timeseries data.

        """

        # Integrate heat produced by each injection.
        for injection in self.injections:
            # determine initial and final samples for injection i
            first_index = injection['first_index'] # index of timepoint for first filtered differential power measurement
            last_index  = injection['last_index']  # index of timepoint for last filtered differential power measurement
            
            # Determine excess energy input into sample cell (with respect to reference cell) throughout this injection and measurement period.
            #excess_energy_input = injection['filter_period'] * (self.differential_power[first_index:(last_index+1)] - self.reference_power + self.baseline_power[first_index:(last_index+1)]).sum()
            excess_energy_input = injection['filter_period'] * (self.differential_power[first_index:(last_index+1)] - self.baseline_power[first_index:(last_index+1)]).sum()            

            # DEBUG
            print "injection %d, filter period %f s, integrating sample %d to %d" % (injection['number'], injection['filter_period'] / Units.s, first_index, last_index)
            
            # Determine total heat evolved.
            evolved_heat = - excess_energy_input
            
            # Store heat evolved from this injection.
            injection['evolved_heat'] = evolved_heat
            
        return

    def __str__(self):
        """
        Show details of experiment in human-readable form.

        """
        
        string = ""
        string += "EXPERIMENT\n"
        string += "\n"
        string += "Source filename: %s\n" % self.data_filename
        string += "Number of injections: %d\n" % self.number_of_injections
        string += "Target temperature: %.1f K\n" % (self.target_temperature / Units.K)
        string += "Equilibration time before first injection: %.1f s\n" % (self.equilibration_time / Units.s)
        string += "Syringe concentration: %.3f mM\n" % (self.syringe_concentration / Units.mM)
        string += "Cell concentration: %.3f mM\n" % (self.cell_concentration / Units.mM)
        string += "Cell volume: %.3f ml\n" % (self.cell_volume / Units.ml)
        string += "Reference power: %.3f ucal/s\n" % (self.reference_power / (Units.ucal/Units.s))

        string += "\n"
        string += "INJECTIONS\n"
        string += "\n"
        string += "%16s %24s %24s %24s %24s %24s\n" % ('injection', 'volume (uL)', 'duration (s)', 'collection time (s)', 'time step (s)', 'evolved heat (ucal)')
#        for injection in range(self.number_of_injections):
#            string += "%16d %16.3f %16.3f %16.3f %16.3f" % (injection, self.injection_volume[injection] / Units.ul, self.injection_duration[injection] / Units.s, self.collection_time[injection] / Units.s, self.time_step[injection] / Units.s)
        for injection in self.injections:
            string += "%16d %24.3f %24.3f %24.3f %24.3f %24.3f\n" % (injection['number'], injection['volume'] / Units.ul, injection['duration'] / Units.s, injection['spacing'] / Units.s, injection['filter_period'] / Units.s, injection['evolved_heat'] / Units.ucal)    

        return string

    def write_integrated_heats(self, filename):
        """
        Write integrated heats in a format similar to that used by Origin.
        
        """

        DeltaV = self.injections[0]['volume']
        V0 = self.cell_volume
        P0 = self.cell_concentration
        Ls = self.syringe_concentration
        
        string = "%12s %5s %12s %12s %12s %12s\n" % ("DH", "INJV", "Xt", "Mt", "XMt", "NDH")
        for (n, injection) in enumerate(self.injections):
            # Instantaneous injection model (perfusion)
#            d = 1.0 - (DeltaV / V0) # dilution factor (dimensionless)
#            P = V0 * P0 * d**(n+1) # total quantity of protein in sample cell after n injections (mol)
#            L = V0 * Ls * (1. - d**(n+1)) # total quantity of ligand in sample cell after n injections (mol)
#            PLn = 0.5/V0 * ((P + L + Kd*V0) - numpy.sqrt((P + L + Kd*V0)**2 - 4*P*L));  # complex concentration (M)
#            Pn = P/V0 - PLn; # free protein concentration in sample cell after n injections (M)
#            Ln = L/V0 - PLn; # free ligand concentration in sample cell after n injections (M)

            Pn = 0.0
            Ln = 0.0
            PLn = 0.0
            NDH = 0.0 # Not sure what this is

            # Form string.
            string += "%12.5f %5.1f %12.5f %12.5f %12.5f %12.5f\n" % (injection['evolved_heat'] / Units.ucal, injection['volume'] / Units.ul, Pn / Units.mM, Ln / Units.mM, PLn / Units.mM, NDH)

        # Final line.
        string += "        --      %12.5f %12.5f --\n" % (Pn, Ln)

        # Write file contents.
        outfile = open(filename, 'w')
        outfile.write(string)
        outfile.close()

        return

    def write_power(self, filename):
        """
        DEBUG: Write power.

        """

        outfile = open(filename, 'w')
        outfile.write("%%%7s %16s %16s\n" % ('time (s)', 'heat (ucal/s)', 'temperature (K)'))
        for index in range(len(self.filter_period_end_time)):
            outfile.write("%8.1f %16.8f %16.8f\n" % (self.filter_period_end_time[index] / Units.s, self.differential_power[index] / (Units.ucal/Units.s), self.cell_temperature[index] / Units.K))
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
        pylab.plot(self.filter_period_end_time / Units.s, self.baseline_power / (Units.ucal/Units.s), 'g-')
        
        # Plot differential power.
        pylab.plot(self.filter_period_end_time / Units.s, self.differential_power / (Units.ucal/Units.s), 'k.', markersize=markersize)

        # Plot injection time markers.
        [xmin, xmax, ymin, ymax] = pylab.axis()
        for injection in self.injections:
            last_index = injection['first_index'] # timepoint at start of syringe injection
            t = self.filter_period_end_time[last_index] / Units.s
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
        injection_end_times = numpy.zeros([len(self.injections)], numpy.float64)
        for (index, injection) in enumerate(self.injections):
            # determine initial and final samples for injection 
            first_index = injection['first_index'] # index of timepoint for first filtered differential power measurement
            last_index  = injection['last_index']  # index of timepoint for last filtered differential power measurement
            # determine time at end of injection period
            injection_end_times[index] = self.filter_period_end_time[last_index] / Units.s

        # Plot model fits, if specified.
        if model:            
            P0_n = model.trace('P0')[:]
            Ls_n = model.trace('Ls')[:]            
            DeltaG_n = model.trace('DeltaG')[:]
            DeltaH_n = model.trace('DeltaH')[:]
            DeltaH0_n = model.trace('DeltaH_0')[:]
            N = DeltaG_n.size
            for n in range(N):
                expected_injection_heats = mcmc.q_n.parents['mu']._eval_fun
                q_n = expected_injection_heats(DeltaG=DeltaG_n[n], DeltaH=DeltaH_n[n], DeltaH_0=DeltaH0_n[n], P0=P0_n[n], Ls=Ls_n[n])
                pylab.plot(injection_end_times/ Units.s, q_n / Units.ucal, 'r-', linewidth=1)

        # Plot integrated heats.
        for (index, injection) in enumerate(self.injections):
            # determine time at end of injection period
            t = injection_end_times[index] / Units.s
            # plot a point there to represent total heat evolved in injection period
            y = injection['evolved_heat'] / Units.ucal
            pylab.plot(t, y, 'k.', markersize=markersize)
            #pylab.plot([t, t], [0, y], 'k-') # plot bar from zero line
            # label injection
            pylab.text(t, y, '%d' % injection['number'], fontsize=6)        

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
        pylab.plot(experiment.filter_period_end_time / Units.s, 0.0*experiment.filter_period_end_time / (Units.ucal/Units.s), 'g-') # plot zero line

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

        if (filename != None):
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
        
        #pylab.subplot(212)
        pylab.hold(True)

        # Plot baseline fit.
        pylab.plot(self.filter_period_end_time / Units.s, self.baseline_power / (Units.ucal/Units.s), 'g-')
        
        # Plot differential power.
        indices = list(set(range(len(self.differential_power))) - set(self.baseline_fit_data['indices']))
        pylab.plot(self.filter_period_end_time[indices] / Units.s, self.differential_power[indices] / (Units.ucal/Units.s), 'k.', markersize=markersize)
        
        # Plot differential power.
        indices = self.baseline_fit_data['indices']
        pylab.plot(self.filter_period_end_time[indices] / Units.s, self.differential_power[indices] / (Units.ucal/Units.s), 'r.', markeredgecolor='r', markersize=markersize)

        # Plot injection time markers.
        [xmin, xmax, ymin, ymax] = pylab.axis()
        for injection in self.injections:
            last_index = injection['first_index'] # timepoint at start of syringe injection
            t = self.filter_period_end_time[last_index] / Units.s
            pylab.plot([t, t], [ymin, ymax], 'r-')    

        # Adjust axis to zoom in on baseline.
        ymax = self.baseline_power.max() / (Units.ucal/Units.s)
        ymin = self.baseline_power.min() / (Units.ucal/Units.s)
        width = ymax - ymin
        ymax += width/2
        ymin -= width/2
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

        if (filename != None):
            # Save the plot to the specified file.
            pylab.savefig(filename, dpi=150)
        else:
            # Show plot.
            pylab.show()
              
        return

#=============================================================================================
# Report class
#=============================================================================================

class Report(object):
    """
    Report summary of Bayesian inference procedure applied to ITC data.

    """

    # LaTeX report source template.
    latex_template = \
r"""
\documentclass[11pt]{report}
\usepackage{graphicx}
\usepackage{cite}
\usepackage{url} 
\usepackage{ifthen}
\usepackage{multicol}

\setlength{\topmargin}{0.0cm} \setlength{\textheight}{21.5cm}
\setlength{\oddsidemargin}{0cm}  \setlength{\textwidth}{16.5cm}
\setlength{\columnsep}{0.6cm}

\urlstyle{rm}
\newboolean{publ}

\newcommand{\Prob}{\mathrm{Pr}}

\newenvironment{report}{\fussy\setboolean{publ}{true}}{\fussy}

%% \renewcommand{\section}{\@startsection{section}{1}{\vspace{0.2cm}}}

%% Different font in captions
\newcommand{\captionfonts}{\small \sffamily}

\makeatletter
\long\def\@makecaption#1#2{
  \vskip\abovecaptionskip
  \sbox\@tempboxa{{\captionfonts #1: #2}}
  \ifdim \wd\@tempboxa >\hsize
    {\captionfonts #1: #2\par}
  \else
    \hbox to\hsize{\hfil\box\@tempboxa\hfil}
  \fi
  \vskip\belowcaptionskip}
\makeatother

\begin{document}

\begin{report}

\title{Bayesian ITC analysis report}
\author{Project {\bf %(project_name)s}, created by user {\bf \tt %(user_name)s}, \today\\Created with {\sc bayesian-itc} version %(version_string)s.\\{\sc bayesian-itc} is freely available from \url{http://www.simtk.org/home/bayesian-itc}}
\address{}
\maketitle
\vspace{-1cm}
\begin{abstract}
This document is an automatically-generated summary report for the Bayesian analysis of one or more ITC datasets by the {\sc bayesian-itc} package.
\end{abstract}
\vspace*{-1.5cm}
\section*{References}
\vspace*{0.2cm}
If you use {\sc bayesian-itc}, please cite reference \ref{chodera:2008:bayesian-itc}.

{\sffamily
\tableofcontents
}
\section{ITC datasets}
\vspace*{0.2cm}
\begin{table}[t]
  \begin{center}
  \begin{tabular}[t]{ll}
  %(table_overview_datasets)s
  \hline
  \end{tabular}
  \caption{{\bf ITC datasets used in the Bayesian inference calculation.}}
  \label{table:overview-datasets}
\end{center}
\end{table}
This section summarises the datasets that have been used during the calculation. Table \ref{table:overview-datasets} gives an overview.

\begin{thebibliography}{1}
\bibitem{chodera:2008:bayesian-itc}
J.~D.~Chodera, P.~A.~Novick, K.~Branson, and V.~S.~Pande.
\newblock {Bayesian analysis of isothermal titration calorimetry data}.
\newblock {\em In preparation}, 2008

\end{thebibliography}
\bibliographystyle{unsrt}
\end{report}
\end{document}
"""
    experiments = list() # list of experiments to be described in this report

    #=============================================================================================
    # Methods.
    #=============================================================================================
    
    def __init__(self, experiments):
        """
        Initialize report with one or more experiments.

        @param experiments one or more experiments to include in report
        @paramtype experiments either a single Experiment or a list of Experiment objects

        """

        # Store experiments in list.
        if isinstance(experiments, list):
            # TODO: Deep copy.
            self.experiments += experiments
        else:
            self.experiments = [experiments]

        return

    def writeLaTeX(self, filename):
        """
        Generate LaTeX source for report.

        @param filename name of LaTeX file to be written
        @paramtype filename Python string
        
        """
                
        # Populate LaTeX report template.
        project_name = 'test project'
        user_name = 'jchodera'
        version_string = '0.1'

        # Construct entries or table of datasets
        dataset_summary_template = r"""\
\hline datafile & {\tt %(data_filename)s} \\
number of injections & %(number_of_injections)s \\
target temperature & %(target_temperature).3f C \\
equilibration time & %(equilibration_time).1f s \\
syringe concentration & %(syringe_concentration).3f mM \\
cell concentration & %(cell_concentration).3f mM \\
cell volume & %(cell_volume).3f mL \\
reference power & %(reference_power).3f $\mu$cal/s \\
"""        
        table_overview_datasets = ""
        for experiment in self.experiments:
            dataset_name = experiment.data_filename
            table_overview_datasets += dataset_summary_template % {
                'data_filename' : experiment.data_filename,
                'number_of_injections' : experiment.number_of_injections,
                'target_temperature' : (experiment.target_temperature / Units.K - Constants.absolute_zero),
                'equilibration_time' : (experiment.equilibration_time / Units.s),
                'syringe_concentration' : (experiment.syringe_concentration / Units.mM),
                'cell_concentration' : (experiment.cell_concentration / Units.mM),
                'cell_volume' : (experiment.cell_volume / Units.ml),
                'reference_power' : (experiment.reference_power / (Units.ucal/Units.s)) }
             
        latex_source = self.latex_template % vars()

        # Create report file.
        report_file = open(filename, 'w')
        report_file.write(latex_source)        
        report_file.close()
        
        return
    
def analyze(name, experiment):
    
    # Write text-based rendering of experimental data.
    for (index, experiment) in enumerate(experiments):
        print "EXPERIMENT %d" % index
        print str(experiment)

    # DEBUG: Write power
    #experiment.write_power('realtime.dat')

    #=============================================================================================
    # Make plots
    #=============================================================================================

#    # Test whether the samples prior to the first injection are normally-distributed.
#    index = experiment.injections[0]['first_index']
#    x = experiment.differential_power[0:index]
#    print x
#    print "P-value for normality:"
#    print scipy.stats.normaltest(x)
#    # DEBUG
#    import pylab
#    pylab.figure()
#    pylab.subplot(111)    
#    pylab.plot(experiment.filter_period_end_time[0:index] / Units.s, experiment.differential_power[0:index] / (Units.ucal/Units.s), 'k.')
#    pylab.show()
    
    # Create a LaTeX report file.
    report = Report([experiment])
    #report.writeLaTeX('report.tex')
    #exit(1)

    # Plot the raw measurements of differential power versus time and the enthalpogram.
    import pylab
    pylab.figure()

    fontsize = 8

    # Plot differential power versus time.
    pylab.subplot(411)

    # plot baseline fit
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / Units.s, experiment.baseline_power / (Units.ucal/Units.s), 'g-') # plot baseline fit

    # differential power
    pylab.plot(experiment.filter_period_end_time / Units.s, experiment.differential_power / (Units.ucal/Units.s), 'k.', markersize=1)
    # plot red vertical line to mark injection times
    pylab.hold(True)    
    [xmin, xmax, ymin, ymax] = pylab.axis()

    # DEBUG
#    ymax = experiment.differential_power.max() / (Units.ucal/Units.s)
#    ymin = ymax - 0.3
#    pylab.axis([xmin, xmax, ymin, ymax]) 
    
    for injection in experiment.injections:
        last_index = injection['first_index'] # timepoint at start of syringe injection
        t = experiment.filter_period_end_time[last_index] / Units.s
        pylab.plot([t, t], [ymin, ymax], 'r-')    
    pylab.hold(False)
    xlabel = pylab.xlabel('time / s')
    xlabel.set_fontsize(fontsize)
    ylabel = pylab.ylabel('differential power / ucal/s')
    ylabel.set_fontsize(fontsize)

    ax = pylab.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

    # title plot
    title = pylab.title(name)
    title.set_fontsize(fontsize)
    
    # Plot enthalpogram.
    pylab.subplot(412)
    pylab.hold(True)
    for injection in experiment.injections:
        # determine initial and final samples for injection i
        first_index = injection['first_index'] # index of timepoint for first filtered differential power measurement
        last_index  = injection['last_index']  # index of timepoint for last filtered differential power measurement
        # determine time at end of injection period
        t = experiment.filter_period_end_time[last_index] / Units.s
        # plot a point there to represent total heat evolved in injection period
        y = injection['evolved_heat'] / Units.ucal
        pylab.plot([t, t], [0, y], 'k-')
        # label injection
        pylab.text(t, y, '%d' % injection['number'], fontsize=6)        
    # adjust axes to match first plot
    [xmin_new, xmax_new, ymin, ymax] = pylab.axis()
    pylab.axis([xmin, xmax, ymin, ymax])    
    pylab.hold(False)
    #pylab.title('evolved heat per injection')
    xlabel = pylab.xlabel('time / s')
    xlabel.set_fontsize(fontsize)
    ylabel = pylab.ylabel('evolved heat / ucal')
    ylabel.set_fontsize(fontsize)
    # plot zero
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / Units.s, 0.0*experiment.filter_period_end_time / (Units.ucal/Units.s), 'g-') # plot zero line


    ax = pylab.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
                    
    # Plot cell temperature.
    pylab.subplot(413)
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / Units.s, experiment.cell_temperature/Units.K - Constants.absolute_zero, 'r.', markersize=1)
    # adjust axes to match first plot
    [xmin_new, xmax_new, ymin, ymax] = pylab.axis()
    pylab.axis([xmin, xmax, ymin, ymax])    
    pylab.hold(False)
    #pylab.title('evolved heat per injection')
    xlabel = pylab.xlabel('time / s')
    xlabel.set_fontsize(fontsize)
    ylabel = pylab.ylabel('cell temperature / C')
    ylabel.set_fontsize(fontsize)

    ax = pylab.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

    # Plot adiabatic jacket temperature.
    pylab.subplot(414)
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / Units.s, experiment.jacket_temperature/Units.K - Constants.absolute_zero, 'b.', markersize=1)    
    # adjust axes to match first plot
    [xmin_new, xmax_new, ymin, ymax] = pylab.axis()
    pylab.axis([xmin, xmax, ymin, ymax])    
    pylab.hold(False)
    #pylab.title('evolved heat per injection')
    xlabel = pylab.xlabel('time / s')
    xlabel.set_fontsize(fontsize)
    ylabel = pylab.ylabel('jacket temperature / C')
    ylabel.set_fontsize(fontsize)
    
    ax = pylab.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

    # show plot
    #pylab.show()
    pylab.savefig('%s.pdf' % name, orientation='landscape', papertype='letter', format='pdf')

    #=============================================================================================
    # Binding model.
    #=============================================================================================

#    import models

#    #model = TwoComponentBindingModel(Ls_stated, P0_stated, q_n, DeltaV, temperature, V0)
#    model = models.CompetitiveBindingModel(experiments, '148_w_DD1', experiment.cell_volume, verbose=True)
    
    #=============================================================================================
    # Run MCMC inference on model.
    #=============================================================================================

#    niters = 10000 # number of iterations
#    nburn = 1000 # number of burn-in iterations
#    nthin = 1 # thinning period
#    
#    model.mcmc.isample(iter=niters, burn=nburn, thin=nthin)
#    pymc.Matplot.plot(model.mcmc)

    return



#=============================================================================================
# Model
#=============================================================================================
def buildModel(experiment):
    """
    Create a PyMC model from one or more Experiment objects.

    ARGUMENTS
        experiment (Experiment) - the experiment to analyze

    RETURNS
        model (pymc.model) - a PyMC model

    """

    # Determine number of injections.
    N = experiment.number_of_injections

    # Physical constants
    Na = 6.02214179e23 # Avogadro's number (number/mol)
    kB = Na * 1.3806504e-23 / 4184.0 * Units.kcal / Units.mol / Units.K # Boltzmann constant (kcal/mol/K)
    C0 = 1.0 * Units.M # standard concentration (M)

    temperature = 298.15 * Units.K# temperature (K)
    beta = 1.0 / (kB * temperature) # inverse temperature 1/(kcal/mol)

    # Store sample cell volume and injection volume.
    Ls_stated = experiment.syringe_concentration # syringe concentration (M)
    P0_stated = experiment.cell_concentration # cell concentration (M)
    V0 = experiment.cell_volume # cell volume (L)

    V0 = V0 - 0.044*Units.ml # Tellinghuisen volume correction for VP-ITC (L) # not sure for iTC-200
    
    # Uncertainties in concentrations.
    dP0 = 0.10 * P0_stated # uncertainty in protein stated concentration (M) - 10% error 
    dLs = 0.10 * Ls_stated # uncertainty in ligand stated concentration (M) - 10% error 

    # For CAII:CBS
    dP0 = 0.10 * P0_stated # uncertainty in protein stated concentration (M) 
    dLs = 0.01 * Ls_stated # uncertainty in ligand stated concentration (M) 
    
    # Extract evolved injection heats.
    injection_heats = numpy.zeros([N], numpy.float64)
    for (n, injection) in enumerate(experiment.injections):
        injection_heats[n] = injection['evolved_heat']
        
    print "injection heats"
    print injection_heats / Units.ucal

    # Determine guesses for initial values
    nlast = 4 # number of injections to use
    duration_n = numpy.zeros([N], numpy.float64) # duration_n[n] is the duration of injection n
    for n in range(N):
        duration_n[n] = experiment.injections[n]['duration']    
    sigma2 = injection_heats[N-nlast:N].var() / duration_n[N-nlast:N].sum()
    log_sigma_guess = numpy.log(numpy.sqrt(sigma2 / Units.cal**2 * Units.second)) # cal/s # TODO: Use std of individual filtered measurements instead

    try:
        DeltaG_guess = -5.0 * Units.kcal/Units.mol
        print "Ls_stated = %f uM" % (Ls_stated / Units.uM)
        print "final injection volume = %f uL" % (experiment.injections[N-1]['volume'] / Units.ul)
        DeltaH_0_guess = - injection_heats[N-1] / (Ls_stated * experiment.injections[N-1]['volume'])
        DeltaH_guess = - (injection_heats[0] / (Ls_stated * experiment.injections[0]['volume']) - DeltaH_0_guess)
    except:
        DeltaG_guess = 0.0
        DeltaH_0_guess = 0.0
        DeltaH_guess = 0.0

    # DEBUG
    print ""
    print ""
    print "INITIAL GUESS"
    print "DeltaH_0_guess = %.3f ucal/uL" % (DeltaH_0_guess / (Units.ucal/Units.ul))
    first_index = 0
    last_index = experiment.injections[0]['first_index']
    filter_time = experiment.injections[0]['filter_period']
    print "Computing sigma2"
    sigma2 = (experiment.differential_power[first_index:last_index] - experiment.baseline_power[first_index:last_index]).var() / filter_time
    print sigma2
    log_sigma_guess = numpy.log(numpy.sqrt(sigma2 / Units.cal**2 * Units.second)) # cal/s # TODO: Use std of individual filtered measurements instead
    print log_sigma_guess
    print ""
    print ""
    print ""
    print ""

    # Determine min and max range for log_sigma
    log_sigma_min = log_sigma_guess - 10.0
    log_sigma_max = log_sigma_guess + 10.0

    # Determine range for priors for thermodynamic parameters.
    DeltaG_min = -40. * Units.kcal/Units.mol # 
    DeltaG_max = +40. * Units.kcal/Units.mol # 
    DeltaH_min = -100. * Units.kcal/Units.mol # 
    DeltaH_max = +100. * Units.kcal/Units.mol # 
    heat_interval = injection_heats.max() - injection_heats.min()
    DeltaH_0_min = injection_heats.min() - heat_interval # 
    DeltaH_0_max = injection_heats.max() + heat_interval # 

    # Create model.
    model = dict()

    # Define constants.
    model['beta'] = beta

    # Define priors.
    @pymc.deterministic
    def zero():
        return 0.0

    if (P0_stated > 0.0):
        model['P0'] = pymc.Lognormal('P0', mu=numpy.log(P0_stated), tau=1.0/numpy.log(1.0+(dP0/P0_stated)**2), value=P0_stated) # true cell concentration (M)
    else:
        model['P0'] = zero

    if (Ls_stated > 0.0):
        model['Ls'] = pymc.Lognormal('Ls', mu=numpy.log(Ls_stated), tau=1.0/numpy.log(1.0+(dLs/Ls_stated)**2), value=Ls_stated) # true syringe concentration (M)
    else:
        model['Ls'] = zero

    model['log_sigma'] = pymc.Uniform('log_sigma', lower=log_sigma_min, upper=log_sigma_max, value=log_sigma_guess) # natural logarithm of std dev of integrated injection heat divided by 1 cal
    model['DeltaG'] = pymc.Uniform('DeltaG', lower=DeltaG_min, upper=DeltaG_max, value=DeltaG_guess) # DeltaG (kcal/mol)
    model['DeltaH'] = pymc.Uniform('DeltaH', lower=DeltaH_min, upper=DeltaH_max, value=DeltaH_guess) # DeltaH (kcal/mol)
    model['DeltaH_0'] = pymc.Uniform('DeltaH_0', lower=DeltaH_0_min, upper=DeltaH_0_max, value=DeltaH_0_guess) # heat of mixing and mechanical injection (cal/volume)

    @pymc.deterministic
    def zero():
        return 0.0

    @pymc.deterministic
    def expected_injection_heats(DeltaG=model['DeltaG'], DeltaH=model['DeltaH'], DeltaH_0=model['DeltaH_0'], P0=model['P0'], Ls=model['Ls']):
        """
        Expected heats of injection for two-component binding model.

        ARGUMENTS

        DeltaG - free energy of binding (kcal/mol)
        DeltaH - enthalpy of binding (kcal/mol)
        DeltaH_0 - heat of injection (cal/mol)

        """

        debug = False

        Kd = numpy.exp(beta * DeltaG) * C0 # dissociation constant (M)

        # Compute dilution factor for instantaneous injection model (perfusion).
        d_n = numpy.zeros([N], numpy.float64) # d_n[n] is the dilution factor for injection n
        dcum_n = numpy.ones([N], numpy.float64) # dcum_n[n] is the cumulative dilution factor for injection n
        if debug: print "%5s %24s %24s" % ('n', 'd_n', 'dcum_n')
        for n in range(N):
            d_n[n] = 1.0 - (experiment.injections[n]['volume'] / V0) # dimensionless dilution factor for injection n
            dcum_n[n:] *= d_n[n]
            if debug: print "%5d %24f %24f" % (n, d_n[n], dcum_n[n])
        if debug: print ""
        
        # Compute complex concentrations.
        Pn = numpy.zeros([N], numpy.float64) # Pn[n] is the protein concentration in sample cell after n injections (M)
        Ln = numpy.zeros([N], numpy.float64) # Ln[n] is the ligand concentration in sample cell after n injections (M)
        PLn = numpy.zeros([N], numpy.float64) # PLn[n] is the complex concentration in sample cell after n injections (M)
        if debug: print "%5s %24s %24s %24s %24s %24s" % ('n', 'P (umol)', 'L (umol)', 'Pn (uM)', 'Ln (uM)', 'PLn (uM)')
        for n in range(N):
            # Instantaneous injection model (perfusion)
            P = V0 * P0 * dcum_n[n] # total quantity of protein in sample cell after n injections (mol)
            L = V0 * Ls * (1. - dcum_n[n]) # total quantity of ligand in sample cell after n injections (mol)
            PLn[n] = 0.5/V0 * ((P + L + Kd*V0) - numpy.sqrt((P + L + Kd*V0)**2 - 4*P*L));  # complex concentration (M)
            Pn[n] = P/V0 - PLn[n]; # free protein concentration in sample cell after n injections (M)
            Ln[n] = L/V0 - PLn[n]; # free ligand concentration in sample cell after n injections (M)
            if debug: print "%5d %24f %24f %24f %24f %24f" % (n, P / Units.umol, L / Units.umol, Pn[n] / Units.uM, Ln[n] / Units.uM, PLn[n] / Units.uM)
            
        # Compute expected injection heats.
        q_n = numpy.zeros([N], numpy.float64) # q_n_model[n] is the expected heat from injection n
        q_n[0] = (-DeltaH) * V0 * (PLn[0] - d_n[0]*0.0) + (-DeltaH_0) * experiment.injections[0]['volume'] # first injection
        for n in range(1,N):
            q_n[n] = (-DeltaH) * V0 * (PLn[n] - d_n[n]*PLn[n-1]) + (-DeltaH_0) * experiment.injections[n]['volume'] # subsequent injections

        # Debug output
        if debug:
            print "DeltaG = %6.1f kcal/mol ; DeltaH = %6.1f kcal/mol ; DeltaH_0 = %6.1f ucal/injection" % (DeltaG / (Units.kcal/Units.mol), DeltaH / (Units.kcal/Units.mol), DeltaH_0 / Units.ucal)
            for n in range(N):
                print "%6.1f" % (PLn[n] / Units.uM),
            print ""
            for n in range(N):
                print "%6.1f" % (q_n[n] / Units.ucal),
            print ""
            for n in range(N):
                print "%6.1f" % (injection_heats[n] / Units.ucal),
            print ""
            print ""

        return q_n

    @pymc.deterministic
    def tau(log_sigma=model['log_sigma']):
        """
        Injection heat measurement precision.
        
        """
        return numpy.exp(-2.0*log_sigma)/(Units.cal**2 / Units.second) * numpy.sqrt(duration_n)

    # Define observed data.
    print N
    print expected_injection_heats
    print tau
    print injection_heats
    #model['q_n'] = pymc.Normal('q_n', size=[N], mu=expected_injection_heats, tau=tau, observed=True, value=injection_heats)
    model['q_n'] = pymc.Normal('q_n', mu=expected_injection_heats, tau=tau, observed=True, value=injection_heats)

    return model              

#=============================================================================================
# Efficient step method
#=============================================================================================

class RescalingStep(pymc.StepMethod):
   def __init__(self, stochastic, beta, max_scale=1.03, verbose=0, interval=100):
      # Verbosity flag
      self.verbose = verbose

      # Store stochastics.
      if not numpy.iterable(stochastic):
         stochastic = [stochastic]
      # Initialize superclass.
      pymc.StepMethod.__init__(self, stochastic, verbose)

      self._id = 'RescalingMetropolis_'+'_'.join([p.__name__ for p in self.stochastics])
      # State variables used to restore the state in a later session.
      self._state += ['max_scale', '_current_iter', 'interval']

      self.max_scale = max_scale
      self.beta = beta

      self._current_iter = 0
      self.interval = interval

      # Keep track of number of accepted moves.
      self.accepted = 0
      self.rejected = 0

      # Store dict of stochastic names.
      self.stochastic_index = dict()
      for p in self.stochastics:
         self.stochastic_index[str(p)] = p

      # Report
      if self.verbose:
         print "Initialization..."
         print "max_scale: ", self.max_scale

   def propose(self):
      # Choose trial scaling factor or its inverse with equal probability, so that proposal move is symmetric.
      factor = (self.max_scale - 1) * numpy.random.rand() + 1;
      if (numpy.random.rand() < 0.5): 
         factor = 1./factor;

      # Scale thermodynamic parameters and variables with this factor.   
      self.stochastic_index['Ls'].value = self.stochastic_index['Ls'].value * factor
      self.stochastic_index['P0'].value = self.stochastic_index['P0'].value * factor
      self.stochastic_index['DeltaH'].value = self.stochastic_index['DeltaH'].value / factor
      self.stochastic_index['DeltaG'].value = self.stochastic_index['DeltaG'].value + (1./self.beta) * numpy.log(factor);
      self.stochastic_index['DeltaH_0'].value = self.stochastic_index['DeltaH_0'].value

      return                                                                    

   def step(self):
      # Probability and likelihood for stochastic's current value:
      logp = sum([stochastic.logp for stochastic in self.stochastics])
      loglike = self.loglike
      if self.verbose > 1:
         print 'Current likelihood: ', logp+loglike
         
      # Sample a candidate value
      self.propose()

      # Metropolis acception/rejection test
      accept = False
      try:
         # Probability and likelihood for stochastic's proposed value:
         logp_p = sum([stochastic.logp for stochastic in self.stochastics])
         loglike_p = self.loglike
         if self.verbose > 2:
            print 'Current likelihood: ', logp+loglike
            
         if numpy.log(numpy.random.rand()) < logp_p + loglike_p - logp - loglike:
            accept = True
            self.accepted += 1
            if self.verbose > 2:
               print 'Accepted'
         else:
            self.rejected += 1
            if self.verbose > 2:
               print 'Rejected'
      except pymc.ZeroProbability:
         self.rejected += 1
         logp_p = None
         loglike_p = None
         if self.verbose > 2:
            print 'Rejected with ZeroProbability error.'

      if (not self._current_iter % self.interval) and self.verbose > 1:
         print "Step ", self._current_iter
         print "\tLogprobability (current, proposed): ", logp, logp_p
         print "\tloglike (current, proposed):      : ", loglike, loglike_p
         for stochastic in self.stochastics:
            print "\t", stochastic.__name__, stochastic.last_value, stochastic.value
         if accept:
            print "\tAccepted\t*******\n"
         else:
            print "\tRejected\n"
         print "\tAcceptance ratio: ", self.accepted/(self.accepted+self.rejected)
         
      if not accept:
         self.reject()

      self._current_iter += 1
      
      return

   @classmethod
   def competence(self, stochastic):
      if str(stochastic) in ['DeltaG', 'DeltaH', 'DeltaH_0', 'Ls', 'P0']:
         return 1
      return 0
         
   def reject(self):
      for stochastic in self.stochastics:
         # stochastic.value = stochastic.last_value
         stochastic.revert()

   def tune(self, verbose):
      return False                                                                                                                                                                                                                                                                   

def compute_statistics(x_t):

    # Compute mean.
    x = x_t.mean()

    # Compute stddev.
    dx = x_t.std()

    # Compute 95% confidence interval.
    ci = 0.95
    N = x_t.size
    x_sorted = numpy.sort(x_t)
    low_index = round((0.5-ci/2.0)*N)
    high_index = round((0.5+ci/2.0)*N)    
    xlow = x_sorted[low_index]
    xhigh = x_sorted[high_index]

    return [x, dx, xlow, xhigh]

#=============================================================================================
# MAIN AND TESTS
#=============================================================================================

if __name__ == "__main__":
    # Run doctests.
    import doctest
    doctest.testmod()

    #=============================================================================================
    # Load experimental data.
    #=============================================================================================

    experiments = list()

    # Create a new ITC experiment object from the VP-ITC file.
    #filename = '../examples/two-component-binding/T4-lysozyme-L99A/toluene.itc'
    #filename = '../examples/111108/BenzamineTrypsin1.itc'
    #filename = '../examples/gudrun-spitzer/141_w_A3T3.itc'    
    #filename = '../examples/gudrun-spitzer/149_w_DD1.itc'
    #filename = '../examples/gudrun-spitzer/148_w_DD1.itc'

    # Create an Experiment object from VP-ITC data.
    #filename = '../data/Mg2-EDTA/Mg2EDTA/Mg1EDTAp08a.itc' # Mg2+:EDTA sample dataset
    #names = ['Mg1EDTAp1a', 'Mg1EDTAp1b', 'Mg1EDTAp1c', 'Mg1EDTAp1d', 'Mg1EDTAp1e']
    #names = ['Mgp5EDTAp05a', 'Mgp5EDTAp05b', 'Mgp5EDTAp05c', 'Mgp5EDTAp05d', 'Mgp5EDTAp05e', 'Mgp5EDTAp05f', 'Mgp5EDTAp05g', 'Mgp5EDTAp05h', 'Mgp5EDTAp05i', 'Mgp5EDTAp05j']    
    #names = ['Mg1EDTAp1a']
    #directory = '../data/NAD2ADh'
    #directory = '../data/CaM'
    #directory = '../data/CAII-CBS/'
    #directory = '../data/'
    import commands
    #filenames = commands.getoutput('ls %s/Mgp5EDTAp05*.itc' % directory).split('\n')
    #filenames = commands.getoutput('ls %s/042711*.itc' % directory).split('\n')
    #filenames = commands.getoutput('ls %s/CAII-10uM/original-data/*.itc' % directory).split('\n')
    #filenames = commands.getoutput('ls %s/VP-ITC-controls/pbs-into-pbs/*.itc' % directory).split('\n')
    #directory = '../data/Mg2-EDTA/Mg2EDTA'
    #directory = '../data/hCAII-CBS/hCAII-10uM/'
    #directory = '../data/CAII-CBS/062111/'
    #directory = '../data/SAMPL3/'
    #directory = '../data/VP-ITC-controls/tris-buffer-mismatch'
    #directory = '../data/CAII-CBS/CAII-40uM'
    #directory = '../data/auto-iTC-200/JDC/'
    #directory = '../data/auto-iTC-200/Rockefeller\ AutoiTC\ 082513/'
    #directory = '../data/auto-iTC-200/082713'
    #directory = '../data/SAMPL4/CB7/111213'
    directory = '../data/auto-iTC-200/053014/'

    filenames = commands.getoutput('ls %s/*.itc' % directory).split('\n')
    #filenames = commands.getoutput('ls %s/0822*b*.itc' % directory).split('\n')

    # DEBUG
    #filenames = ['../data/SAMPL3//PIIIB08vstrypsin2203114.itc']
    #filenames = ['../data/VP-ITC-controls/tris-buffer-mismatch/022912a.itc']

    print filenames
    for filename in filenames:

        # Close all figure windows.
        import pylab
        pylab.close('all')
        
        #filename = '../data/Mg2-EDTA/Mg2EDTA/%s.itc' % name # Mg2+:EDTA sample dataset
        #filename = os.path.join(directory, name)

        name = os.path.splitext(os.path.split(filename)[1])[0]

        print "\n"
        print "Reading ITC data from %s" % filename
        experiment = Experiment(filename)
        #experiments.append(experiment)
        print experiment
        analyze(name, experiment)

        # Write Origin-style integrated heats.
        filename = name + '-integrated.txt'
        experiment.write_integrated_heats(filename)
        
        # Write baseline fit information.
        filename = name + '-baseline.png'
        experiment.plot_baseline(filename)

        continue # DEBUG        

        #=============================================================================================
        # MCMC inference
        #=============================================================================================

        # Construct a Model from Experiment object.
        import traceback
        try:
            model = buildModel(experiment)
        except Exception as e:
            print str(e)
            print traceback.format_exc()
            stop
            continue

        # First fit the model.
        print "Fitting model..."
        map = pymc.MAP(model)
        map.fit(iterlim=20000)
        print map

        niters = 2000000 # number of iterations
        nburn  = 500000 # number of burn-in iterations
        nthin  = 250 # thinning period
        
        #niters = 200000
        #nburn = 500
        #nthin = 10

        #mcmc = pymc.MCMC(model, db='pickle')
        #mcmc = pymc.MCMC(model, db='sqlite')
        #mcmc = pymc.MCMC(model, db='hdf5')
        mcmc = pymc.MCMC(model, db='ram')

        mcmc.use_step_method(pymc.Metropolis, model['DeltaG'])
        mcmc.use_step_method(pymc.Metropolis, model['DeltaH'])
        mcmc.use_step_method(pymc.Metropolis, model['DeltaH_0'])
        mcmc.use_step_method(pymc.Metropolis, model['log_sigma'])
        
        if (experiment.cell_concentration > 0.0):
            mcmc.use_step_method(pymc.Metropolis, model['P0'])
        if (experiment.syringe_concentration > 0.0):
            mcmc.use_step_method(pymc.Metropolis, model['Ls'])
        
        if (experiment.cell_concentration > 0.0) and (experiment.syringe_concentration > 0.0):
            mcmc.use_step_method(RescalingStep, [model['Ls'], model['P0'], model['DeltaH'], model['DeltaG'], model['DeltaH_0']], model['beta'])
        
        print "Sampling..."
        mcmc.sample(iter=niters, burn=nburn, thin=nthin, progress_bar=True)
        #pymc.Matplot.plot(mcmc)

        # Plot individual terms.
        if (experiment.cell_concentration > 0.0):
            pymc.Matplot.plot(mcmc.trace('P0')[:] / Units.uM, '%s-P0' % name)
        if (experiment.syringe_concentration > 0.0):
            pymc.Matplot.plot(mcmc.trace('Ls')[:] / Units.uM, '%s-Ls' % name)
        pymc.Matplot.plot(mcmc.trace('DeltaG')[:] / (Units.kcal/Units.mol), '%s-DeltaG' % name)
        pymc.Matplot.plot(mcmc.trace('DeltaH')[:] / (Units.kcal/Units.mol), '%s-DeltaH' % name)
        pymc.Matplot.plot(mcmc.trace('DeltaH_0')[:] / (Units.ucal/Units.ul), '%s-DeltaH_0' % name)
        pymc.Matplot.plot(numpy.exp(mcmc.trace('log_sigma')[:]) * Units.cal / Units.second**0.5, '%s-sigma' % name)
        
        # TODO: Plot fits to enthalpogram.
        experiment.plot(model=mcmc, filename='sampl4/%s-enthalpogram.png' % name)
        
        # Compute confidence intervals in thermodynamic parameters.
        outfile = open('sampl4/confidence-intervals.out','a')
        outfile.write('%s\n' % name)        
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('DeltaG')[:] / (Units.kcal/Units.mol))         
        outfile.write('DG:     %8.2f +- %8.2f kcal/mol     [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('DeltaH')[:] / (Units.kcal/Units.mol))         
        outfile.write('DH:     %8.2f +- %8.2f kcal/mol     [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('DeltaH_0')[:] / (Units.ucal/Units.ul))         
        outfile.write('DH0:    %8.2f +- %8.2f ucal         [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('Ls')[:] / Units.uM)         
        outfile.write('Ls:     %8.2f +- %8.2f uM           [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(mcmc.trace('P0')[:] / Units.uM)         
        outfile.write('P0:     %8.2f +- %8.2f uM           [%8.2f, %8.2f] \n' % (x, dx, xlow, xhigh))
        [x, dx, xlow, xhigh] = compute_statistics(numpy.exp(mcmc.trace('log_sigma')[:]) * Units.cal / Units.second**0.5)
        outfile.write('sigma:  %8.5f +- %8.5f ucal/s^(1/2) [%8.5f, %8.5f] \n' % (x, dx, xlow, xhigh))        
        outfile.write('\n')
        outfile.close()

