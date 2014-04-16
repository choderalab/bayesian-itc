#!/usr/bin/env python

"""
Test numerical solution of concentrations.

"""

#=============================================================================================
# IMPORTS
#=============================================================================================

import numpy
import pymc

import scipy.optimize
import scipy.integrate

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
# Competitive binding to a single receptor
#=============================================================================================

def equilibrium_concentrations(Ka_n, C0_R, C0_Ln, V):
   """
   Compute the equilibrium concentrations of each complex species for N ligands competitively binding to a receptor.

   ARGUMENTS

   Ka_n (numpy N-array of float) - Ka_n[n] is the association constant for receptor and ligand species n (1/M)
   x_R (float) - the total number of moles of receptor in the sample volume
   x_n (numpy N-array of float) - x_n[n] is the total number of moles of ligand species n in the sample volume
   V (float) - the total sample volume (L)

   RETURNS

   C_n (numpy N-array of float) - C_n[n] is the concentration of complex of receptor with ligand species n

   EXAMPLES

   Simple one-component test

   >>> V = 1.0
   >>> x_R = 1.0
   >>> Ka_n = numpy.array([1.0])
   >>> for x in numpy.arange(0, 3.1, 0.1): print "%8.3f %8.5f" % (x, equilibrium_concentrations(Ka_n, x_R, numpy.array([x]), V))

   Simple one-component test wih a zero concentration of another species

   >>> V = 1.0
   >>> x_R = 1.0
   >>> Ka_n = numpy.array([1.0, 1.0])
   >>> for x in numpy.arange(0, 3.1, 0.1): print "%8.3f %s" % (x, equilibrium_concentrations(Ka_n, x_R, numpy.array([x, 0.0]), V))

   Realistic two-component test

   >>> V = 1.4303e-3 # volume (L)
   >>> x_R = V * 510.e-3 # receptor
   >>> x_Ln = numpy.array([8.6e-6, 0.2 * 55.e-6]) # ligands
   >>> Ka_n = numpy.array([1./(400.e-9), 1./(2.e-11)]) # association constants
   >>> print Ka_n
   >>> print equilibrium_concentrations(Ka_n, x_R, x_Ln, V)
   
   NOTES

   Each complex concentration C_n must obey the relation

   Ka_n[n] = C_RLn[n] / (C_R * C_Ln[n])           for n = 1..N

   with conservation of mass constraints

   V * (C_Ln[n] + C_RLn[n]) = x_Ln[n]             for n = 1..N

   and

   V * (C_R + C_RLn[:].sum()) = x_R

   along with the constraints

   0 <= V * C_RLn[n] <= min(x_Ln[n], x_R)         for n = 1..N
   V * C_RLn[:].sum() <= x_R

   We can rearrange these expressions to give

   V * C_R * C_Ln[n] * Ka_n[n] - V * C_RLn[n] = 0

   and eliminate C_Ln[n] and C_R to give

   V * (x_R/V - C_RLn[:].sum()) * (x_Ln[n]/V - C_RLn[n]) * Ka_n[n] - V * C_RLn[n] = 0    for n = 1..N

   """

   x_R = C0_R * V
   x_Ln = C0_Ln * V

   nspecies = Ka_n.size
   #print "x_Ln = ", x_Ln
   #print "x_Ln / V = ", x_Ln / V
   #print "Ka_n = ", Ka_n

   # Define optimization functions
   def func(C_RLn):
      f_n = V * (x_R/V - C_RLn[:].sum()) * (x_Ln[:]/V - C_RLn[:]) * Ka_n[:] - V * C_RLn[:]
      #print "f_n = ", f_n
      return f_n

   def fprime(C_RLn):
      nspecies = C_RLn.size
      G_nm = numpy.zeros([nspecies,nspecies], numpy.float64) # G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]
      for n in range(nspecies):
         G_nm[n,:] = - V * (x_Ln[:]/V - C_RLn[:]) * Ka_n[:]
         G_nm[n,n] -= V * (Ka_n[n] * (x_R/V - C_RLn[:].sum()) + 1.0)
      return G_nm

   def sfunc(s):
      #print "s = ", s
      f_n = V * (x_R/V - (s[:]**2).sum()) * (x_Ln[:]/V - s[:]**2) * Ka_n[:] - V * s[:]**2
      #print "f_n = ", f_n
      return f_n

   def sfprime(s):
      nspecies = s.size
      G_nm = numpy.zeros([nspecies,nspecies], numpy.float64) # G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]
      for n in range(nspecies):
         G_nm[n,:] = - V * (x_Ln[:]/V - s[:]**2) * Ka_n[:] 
         G_nm[n,n] -= V * (Ka_n[n] * (x_R/V - (s[:]**2).sum()) + 1.0)
         G_nm[n,:] *= 2. * s[n]
      return G_nm

   # Allocate storage for complexes
   # Compute equilibrium concentrations.
   #x0 = numpy.zeros([nspecies], numpy.float64)
   #x = scipy.optimize.fsolve(func, x0, fprime=fprime)
   #C_RLn = x

   #x0 = numpy.sqrt(x_Ln / V).copy()
   #x = scipy.optimize.fsolve(sfunc, x0, fprime=sfprime)         
   #C_RLn = x**2

   def objective(x):
      f_n = func(x)
      G_nm = fprime(x)
      
      obj = (f_n**2).sum()
      grad = 0.0 * f_n
      for n in range(f_n.size):
         grad += 2 * f_n[n] * G_nm[n,:]

      return (obj, grad)
         
#   x0 = numpy.zeros([nspecies], numpy.float64)
#   bounds = list()
#   for n in range(nspecies):
#      bounds.append( (0., min(x_Ln[n]/V, x_R/V)) )
#   [x, a, b] = scipy.optimize.fmin_l_bfgs_b(objective, x0, bounds=bounds)
#   C_RLn = x

   def ode(c_n,t):
      dc_n = - c_n[:] + Ka_n[:] * (x_Ln[:]/V - c_n[:]) * (x_R/V - c_n[:].sum())
      return dc_n
   c0 = numpy.zeros([nspecies], numpy.float64)
   maxtime = 10.0 * (x_R/V) / Ka_n.max()
   time = numpy.linspace(0, 10.0 / ((x_R/V) * Ka_n.min()), 10)
   c = scipy.integrate.odeint(ode, c0, time)
   print c
   C_RLn = c[1,:]

   #print "C_RLn = ", C_RLn 
   #print ""

   return C_RLn

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

#=============================================================================================
# MAIN AND TESTS
#=============================================================================================

if __name__ == "__main__":
   import doctest
   doctest.testmod()
