#!/usr/bin/env python

"""
Test numerical solution of concentrations.

"""

#=============================================================================================
# IMPORTS
#=============================================================================================

import numpy
import pymc

from math import sqrt, exp, log

#=============================================================================================
# Physical constants
#=============================================================================================

Na = 6.02214179e23 # Avogadro's number (number/mol)
kB = Na * 1.3806504e-23 / 4184.0 # Boltzmann constant (kcal/mol/K)
C0 = 1.0 # standard concentration (M)

#=============================================================================================
# Test parameters
#=============================================================================================

Ka_ij = numpy.zeros([3,3], numpy.float64) # Ka_ij[i][j] is association constant of species i and j (1/M)
Ka_ij[0][1] = 1.0 / (1.0e-9) # 1 nM
Ka_ij[1][0] = Ka_ij[0][1]
Ka_ij[0][2] = 1.0 / (1.0e-6) # 1 uM
Ka_ij[2][0] = Ka_ij[0][2]
C_i = numpy.zeros([3], numpy.float64) # Ci[i] is initial concentration of species i (M)
C_i[0] = 40.0e-6 # 40 uM
C_i[1] = 20.0e-6 # 20 uM
C_i[2] = 300.0e-6 # 300 uM
V0 = 1.4e-3 # 1.4 mL

N = C_i.size # number of species
x_i = numpy.zeros([N], numpy.float64) # x_i[i] is the total number of moles of species i
x_i = V0 * C_i

#=============================================================================================
# Solve for equilibrium concentrations of different species
#=============================================================================================

def general_bimolecular_association(Ka_ij, x_i, V):
   """
   Solve for the equilibrium concentrations of all species that can form bimolecular heterocomplexes.

   ARGUMENTS

   Ka_ij (NxN numpy array) - Ka_ij[i,j] is the association constant between species i and j (1/M)
      NOTE: Ka_ij must be symmetric      
   x_i (N numpy array) - x_i[i] is the total number of moles of species i present
   V (float) - total volume of the container (L)

   RETURNS

   C_i (N numpy array) - C_i[i] is the concentration of unassociated species i (M)
   C_ij (NxN numpy array) - C_ij[i,j] is the concentration of associated species (i,j) (M)   

   NOTES
   
   All pairs (i,j) where i != j must obey the relation

   Ka_ij[i,j] = C_ij[i,j] / (C_i[i] * C_j[j])     for i,j = 1..N

   subject to the conservation of mass constraints

   x_i[i] = V * (C_i[i] + C_ij[i,:].sum())        for i = 1..N

   and the positivity constraints

   C_i[i] >= 0                                    for i = 1..N
   C_ij[i,j] >= 0                                 for i,j = 1..N

   We can rearrange these expressions as

   A_ij[i,j]  = V * (C_i[i] * C_j[j] * Ka_ij[i,j] - C_ij[i,j]) = 0
   B_i[i]     = x_i[i] - V * (C_i[i] + C_ij[i,:].sum())        = 0

   Derivatives are

   dA_ij[i,j] / dC_i[k]
      = V * C_j[j] * Ka_ij[k,j]                   if k = i and k != j
      = V * C_j[i] * Ka_ij[k,i]                   if k != i and k = j
      = 2 * V * C_i[i] * Ka_ij[i,i]               if k = i and k = j
      = 0                                         else
      
   dA_ij[i,j] / dC_ij[k,l]
      = -V                                        if (i=k and j=l) or (i=l and j=k)
      = 0                                         else

   dB_i[i] / dC_i[k]
      = -V                                        if i = k
      = 0                                         else

   dB_i[i] / dC_i[k,l]
      = -V                                        if i=k or i=l
      = 0                                         else

   """

   # Determine number of species.
   N = x_i.size

   # Create target function.

   
   # Allocate storage for equilibrium concentrations.
   C_i = numpy.zeros([N], numpy.float64) # C_i[i] is the concentration of unassociated species i (M)   
   C_ij = numpy.zeros([N,N], numpy.float64) # C_ij[i,j] is the concentration of associated species (i,j) (M)   

   

   return (C_i, C_ij)


