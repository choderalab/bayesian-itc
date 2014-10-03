"""Contains Report class for presenting summary of data in organized fashion."""
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
  
