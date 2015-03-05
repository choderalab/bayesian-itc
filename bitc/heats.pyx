cimport cython
import numpy
cimport numpy
import scipy.optimize


# Define numpy datatype
FLOAT64DATATYPE = numpy.float64
INTDATATYPE = numpy.int

# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef numpy.float64_t FLOAT64DATATYPE_t
ctypedef numpy.int_t INTDATATYPE_t



@cython.cdivision(True)
@cython.boundscheck(False)
cpdef numpy.ndarray equilibrium_concentrations(numpy.ndarray k_assoc, double receptor_conc_tot, numpy.ndarray lig_conc_tot, float cell_volume):
    """
    Compute the equilibrium concentrations of each complex species for N ligands competitively binding to a receptor.

    ARGUMENTS

    k_assoc  - k_assoc[n] is the association constant for receptor and ligand species n (1/M)
    receptor_conc_tot - the total number of moles of receptor in the sample volume
    lig_conc_tot - lig_conc_tot[n] is the total number of moles of ligand species n in the sample volume
    cell_volume - the total sample volume (L)

    RETURNS

    C_n (numpy N-array of float) - C_n[n] is the concentration of complex of receptor with ligand species n

    NOTES

    Each complex concentration C_n must obey the relation

    Ka_n[n] = C_RLn[n] / (C_R * C_Ln[n])           for n = 1..N

    with conservation of mass constraints

    V * (C_Ln[n] + C_RLn[n]) = lig_moles_tot[n]             for n = 1..N

    and

    V * (C_R + C_RLn[:].sum()) = receptor_moles_tot

    along with the constraints

    0 <= V * C_RLn[n] <= min(lig_moles_tot[n], receptor_moles_tot)         for n = 1..N
    V * C_RLn[:].sum() <= receptor_moles_tot

    We can rearrange these expressions to give

    V * C_R * C_Ln[n] * Ka_n[n] - V * C_RLn[n] = 0

    and eliminate C_Ln[n] and C_R to give

    V * (receptor_moles_tot/V - C_RLn[:].sum()) * (lig_moles_tot[n]/V - C_RLn[n]) * Ka_n[n] - V * C_RLn[n] = 0    for n = 1..N

    """

    cdef double receptor_moles_tot = receptor_conc_tot * cell_volume
    cdef numpy.ndarray lig_moles_tot = lig_conc_tot * cell_volume

    cdef int nspecies = k_assoc.size

    cdef numpy.ndarray complex_conc = numpy.zeros([nspecies], dtype=FLOAT64DATATYPE)
    cdef numpy.ndarray sorted_indices = numpy.argsort(-lig_moles_tot, dtype=INTDATATYPE)


    for n in range(nspecies):
        complex_conc[sorted_indices[0:n + 1]] = scipy.optimize.fsolve(ode, complex_conc[sorted_indices[0:n + 1]], fprime=odegrad, args=(k_assoc[sorted_indices[0:n + 1]], lig_moles_tot[sorted_indices[0:n + 1]], receptor_moles_tot, cell_volume), xtol=1.0e-6)

    return complex_conc

# Define optimization functions
# def func(C_RLn):
#     f_n = V * (x_R / V - C_RLn[:].sum()) * (x_Ln[:] / V - C_RLn[:]) * Ka_n[:] - V * C_RLn[:]
#     return f_n
#
# def fprime(C_RLn):
#     nspecies = C_RLn.size
#     # G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]
#     G_nm = numpy.zeros([nspecies, nspecies], numpy.float64)
#     for n in range(nspecies):
#         G_nm[n, :] = - V * (x_Ln[:] / V - C_RLn[:]) * Ka_n[:]
#         G_nm[n, n] -= V * (Ka_n[n] * (x_R / V - C_RLn[:].sum()) + 1.0)
#     return G_nm
#
# def sfunc(s):
#     f_n = V * (x_R / V - (s[:] ** 2).sum()) * (x_Ln[:] / V - s[:] ** 2) * Ka_n[:] - V * s[:] ** 2
#     return f_n
#
# def sfprime(s):
#     nspecies = s.size
#     # G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]
#     G_nm = numpy.zeros([nspecies, nspecies], numpy.float64)
#     for n in range(nspecies):
#         G_nm[n, :] = - V * (x_Ln[:] / V - s[:] ** 2) * Ka_n[:]
#         G_nm[n, n] -= V * (Ka_n[n] * (x_R / V - (s[:] ** 2).sum()) + 1.0)
#         G_nm[n, :] *= 2. * s[n]
#     return G_nm
#
# def objective(x):
#     f_n = func(x)
#     G_nm = fprime(x)
#
#     obj = (f_n ** 2).sum()
#     grad = 0.0 * f_n
#     for n in range(f_n.size):
#         grad += 2 * f_n[n] * G_nm[n, :]
#
#     return (obj, grad)

cpdef numpy.ndarray ode(numpy.ndarray complex_conc, numpy.ndarray k_assoc, numpy.ndarray lig_moles_tot, double receptor_moles_tot, double cell_volume):
    """ODE for the change in complex concentration"""
    cdef numpy.ndarray d_complex_conc = - complex_conc[:] + k_assoc[:] * (lig_moles_tot[:] / cell_volume - complex_conc[:]) * (receptor_moles_tot / cell_volume - complex_conc[:].sum())
    return d_complex_conc

cpdef numpy.ndarray odegrad(numpy.ndarray complex_conc, numpy.ndarray k_assoc, numpy.ndarray lig_moles_tot, double receptor_moles_tot, double cell_volume):
    """Gradient calculation for the ODE"""
    cdef int n = len(complex_conc)
    cdef numpy.ndarray d2_complex_conc = numpy.zeros([n, n], dtype=FLOAT64DATATYPE)
    for n in range(n):
        d2_complex_conc[n, :] = -k_assoc[n] * (lig_moles_tot[n] / cell_volume - complex_conc[n])
        d2_complex_conc[n, n] += -(k_assoc[n] * (receptor_moles_tot / cell_volume - complex_conc[:].sum()) + 1.0)
    return d2_complex_conc
