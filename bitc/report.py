"""Contains Report class for presenting summary of data in organized fashion."""

# TODO work on a markdown version of the report
from bitc.units import ureg


class Report(object):
    """
    Report summary of Bayesian inference procedure applied to ITC data.

    """

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
                'target_temperature' : (experiment.target_temperature / ureg.kelvin - 273.15),
                'equilibration_time' : (experiment.equilibration_time / ureg.second),
                'syringe_concentration' : (experiment.syringe_concentration / ureg.millimolar),
                'cell_concentration' : (experiment.cell_concentration / ureg.millimolar),
                'cell_volume' : (experiment.cell_volume / ureg.milliliter),
                'reference_power' : (experiment.reference_power / (ureg.microcalorie/ureg.second)),
            }

        latex_source = self.latex_template % vars()

        # Create report file.
        report_file = open(filename, 'w')
        report_file.write(latex_source)
        report_file.close()

        return

# TODO this function name is too vague, rename. Make modular
def plot_experiment(name, experiment):

    #=============================================================================================
    # Make plots
    #=============================================================================================

    # Create a LaTeX report file.
    report = Report([experiment])

    # Plot the raw measurements of differential power versus time and the enthalpogram.
    import pylab
    pylab.figure()

    fontsize = 8

    # Plot differential power versus time.
    pylab.subplot(411)

    # plot baseline fit
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / ureg.second, experiment.baseline_power / (ureg.microcalorie/ureg.second), 'g-')  # plot baseline fit

    # differential power
    pylab.plot(experiment.filter_period_end_time / ureg.second, experiment.differential_power / (ureg.microcalorie/ureg.second), 'k.', markersize=1)
    # plot red vertical line to mark injection times
    pylab.hold(True)
    [xmin, xmax, ymin, ymax] = pylab.axis()

    for injection in experiment.injections:
        last_index = injection.first_index # timepoint at start of syringe injection
        t = experiment.filter_period_end_time[last_index] / ureg.second
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
        first_index = injection.first_index # index of timepoint for first filtered differential power measurement
        last_index  = injection.last_index  # index of timepoint for last filtered differential power measurement
        # determine time at end of injection period
        t = experiment.filter_period_end_time[last_index] / ureg.second
        # plot a point there to represent total heat evolved in injection period
        y = injection.evolved_heat / ureg.microcalorie
        pylab.plot([t, t], [0, y], 'k-')
        # label injection
        pylab.text(t, y, '%d' % injection.number, fontsize=6)
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
    pylab.plot(experiment.filter_period_end_time / ureg.second, 0.0*experiment.filter_period_end_time / (ureg.microcalorie/ureg.second), 'g-') # plot zero line


    ax = pylab.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

    # Plot cell temperature.
    pylab.subplot(413)
    pylab.hold(True)
    pylab.plot(experiment.filter_period_end_time / ureg.second, experiment.cell_temperature/ureg.kelvin - 273.15, 'r.', markersize=1)
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
    pylab.plot(experiment.filter_period_end_time / ureg.second, experiment.jacket_temperature/ureg.kelvin - 273.15, 'b.', markersize=1)
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
    # It seems that the Report class currently is broken (won't compile to pdf).
    # report.writeLaTeX("%s.tex" % name)
    return
