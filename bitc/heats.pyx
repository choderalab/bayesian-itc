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


@cython.wraparound(False)
@cython.cdivision(True)
@cython.boundscheck(False)
cpdef numpy.ndarray cython_equilibrium_concentrations(numpy.ndarray k_assoc, double receptor_conc_tot, numpy.ndarray lig_conc_tot, float cell_volume):
    """
    Compute the equilibrium concentrations of each complex species for N ligands competitively binding to a receptor.

    ARGUMENTS

    k_assoc  - k_assoc[n] is the association constant for receptor and ligand species n (1/M)
    receptor_conc_tot - the total number of moles of receptor in the sample volume
    lig_conc_tot - lig_conc_tot[n] is the total number of moles of ligand species n in the sample volume
    cell_volume - the total sample volume (L)

    RETURNS

    complex_conc (numpy N-array of float) - complex_conc[n] is the concentration of complex of receptor with ligand species n

    NOTES

    Each complex concentration must obey the relation

    k_assoc[n] = complex_conc[n] / (receptor_conc * lig_conc[n])           for n = 1..N

    with conservation of mass constraints

    cell_volume * (lig_conc[n] + complex_conc[n]) = lig_moles_tot[n]             for n = 1..N

    and

    cell_volume * (receptor_conc + complex_conc.sum()) = receptor_moles_tot

    along with the constraints

    0 <= cell_volume * complex_conc[n] <= min(lig_moles_tot[n], receptor_moles_tot)         for n = 1..N
    cell_volume * complex_conc.sum() <= receptor_moles_tot

    We can rearrange these expressions to give

    cell_volume * receptor_conc * lig_conc[n] * k_assoc[n] - cell_volume * complex_conc[n] = 0

    and eliminate lig_conc[n] and receptor_conc to give

    cell_volume * (receptor_moles_tot/cell_volume - complex_conc.sum()) * (lig_moles_tot[n]/cell_volume - complex_conc[n]) * k_assoc[n] - cell_volume * complex_conc[n] = 0    for n = 1..N

    """

    cdef double receptor_moles_tot = receptor_conc_tot * cell_volume
    cdef numpy.ndarray[FLOAT64DATATYPE_t, ndim=1] lig_moles_tot = lig_conc_tot * cell_volume
    cdef int nspecies = k_assoc.size
    cdef numpy.ndarray[FLOAT64DATATYPE_t, ndim=1] complex_conc = numpy.zeros([nspecies], dtype=FLOAT64DATATYPE)
    cdef numpy.ndarray[INTDATATYPE_t, ndim=1] sorted_indices = numpy.argsort(-lig_moles_tot)

    for n in range(nspecies):
        complex_conc[sorted_indices[0:n+1]] = scipy.optimize.fsolve(ode, complex_conc[sorted_indices[0:n+1]], fprime=odegrad, args=(k_assoc[sorted_indices[0:n+1]], lig_moles_tot[sorted_indices[0:n+1]], receptor_moles_tot, cell_volume), xtol=1.0e-6)

    return complex_conc


cpdef numpy.ndarray ode(numpy.ndarray complex_conc, numpy.ndarray k_assoc, numpy.ndarray lig_moles_tot, double receptor_moles_tot, double cell_volume):
    """ODE for the change in complex concentration"""
    cdef numpy.ndarray[FLOAT64DATATYPE_t, ndim=1] d_complex_conc = - complex_conc + k_assoc * (lig_moles_tot / cell_volume - complex_conc) * (receptor_moles_tot / cell_volume - complex_conc.sum())
    return d_complex_conc

cpdef numpy.ndarray odegrad(numpy.ndarray complex_conc, numpy.ndarray k_assoc, numpy.ndarray lig_moles_tot, double receptor_moles_tot, double cell_volume):
    """Gradient calculation for the ODE"""
    cdef int ncomplexes = complex_conc.size
    cdef numpy.ndarray[FLOAT64DATATYPE_t, ndim=2] d2_complex_conc = numpy.zeros([ncomplexes, ncomplexes], dtype=FLOAT64DATATYPE)
    for n in range(ncomplexes):
        d2_complex_conc[n, :] = -k_assoc[n] * (lig_moles_tot[n] / cell_volume - complex_conc[n])
        d2_complex_conc[n, n] += -(k_assoc[n] * (receptor_moles_tot / cell_volume - complex_conc.sum()) + 1.0)
    return d2_complex_conc
