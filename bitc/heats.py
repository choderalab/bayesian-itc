from math import exp
import numpy
from bitc.units import ureg, mole_fraction, x_times_onemx

@ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None, None, None, None, ureg.mole / ureg.kilocalorie, None])
def dilution_twocomponent_injection_heats(V0, DeltaVn, Xs, Mc, DeltaH_titrant, DeltaH_titrand, DeltaH_bind, DeltaG_bind, H_mech, beta, N):
    """
    Parameters
    ----------
    V0 - cell volume (liter)
    DeltaVn - injection volume (liter)
    Xs - Syringe concentration (mM)
    Mc - cell concentration (mM)
    DeltaH_titrant - heat of diluting titrant (kcal/mol)
    DeltaH_titrand - heat of diluting titrand (kcal/mol)
    DeltaH_bind - heat of binding (kcal/mol)
    DeltaG_bind - free energy of binding (kcal/mol)
    H_mech - mechanical heat of injection (ucal)
    beta - 1/kBT (mole/kcal)
    N - number of injections

    Returns
    -------
    numpy.ndarray - expected injection heats (ucal)
    """

    Kd = exp(beta * DeltaG_bind)   # dissociation constant (M)

    # Compute complex concentrations.
    # Mcn[n] is the protein concentration in sample cell after n injections
    # (M)
    Mcn = numpy.zeros([N])
    # Xcn[n] is the ligand concentration in sample cell after n injections
    # (M)
    Xcn = numpy.zeros([N])
    # MXcn[n] is the complex concentration in sample cell after n injections
    # (M)
    MXcn = numpy.zeros([N])
    dcum = 1.0  # cumulative dilution factor (dimensionless)
    for n in range(N):
        # Instantaneous injection model (perfusion)
        # dilution factor for this injection (dimensionless)
        d = 1.0 - (DeltaVn[n] / V0)
        dcum *= d  # cumulative dilution factor
        # total quantity of protein in sample cell after n injections
        # (converted from mM to mole)
        M = V0 * Mc * 1.e-3 * dcum
        # total quantity of ligand in sample cell after n injections (converted
        # from mM to mole)
        X = V0 * Xs * 1.e-3 * (1. - dcum)
        # complex concentration (M)
        MXcn[n] = (0.5 / V0 * ((M + X + Kd * V0) - ((M + X + Kd * V0) ** 2 - 4 * M * X) ** 0.5))
        # free protein concentration in sample cell after n injections (M)
        Mcn[n] = M / V0 - MXcn[n]
        # free ligand concentration in sample cell after n injections (M)
        Xcn[n] = X / V0 - MXcn[n]

    # Compute expected injection heats.
    # q_n_model[n] is the expected heat from injection n
    q_n = numpy.zeros([N])
    # Instantaneous injection model (perfusion)
    # first injection
    # from kcal/mole to kcal/liter
    DHd = DeltaH_titrand * (Mcn[0] - Mc)
    DHt = DeltaH_titrant * (Xcn[0])
    DHb = DeltaH_bind * (MXcn[0])
    # converter from kcal/liter to ucal
    q_n[0] = V0 * 1.e9 * (DHd + DHt + DHb) + H_mech
    for n in range(1, N):
        # subsequent injections
        DHd = DeltaH_titrand * (Mcn[n] - Mcn[n - 1])
        DHt = DeltaH_titrant * (Xcn[n] - Xcn[n - 1])
        DHb = DeltaH_bind * (MXcn[n] - MXcn[n - 1])
        # converted from kcal/liter to ucal
        q_n[n] = V0 * 1.e9 * (DHd + DHt + DHb) + H_mech

    return q_n


@ureg.wraps(ret=ureg.microcalorie, args=[None, None], strict=True)
def mechanical_injection_heats(DeltaH_0, N):
    """
    Expected heats of injection for a calibration titration
    ARGUMENTS
    DeltaH_0 - heat of injection (ucal)

    """
    # Compute expected injection heats.
    q_n = numpy.zeros([N])  # q_n_model[n] is the expected heat from injection n

    for n in range(N):
        # q_n and DeltaH_0 both have the same unit (ucal)
        q_n[n] = DeltaH_0
    return q_n


@ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None], strict=True)
def tellinghuisen_dilution_twocomponent_injection_heats(V0, DeltaVn, Xs, L_phi, H_s, N):
    """
    Expected heats of injection for two-component binding model.

    ARGUMENTS
    V0 - cell volume (liter)
    DeltaVn - injection volumes (liter)
    Xs - Syringe concentration (millimolar)
    L_phi - molar enthalpy at concentration [X] (cal/mol)
    H_s - enthalpy in the syringe per injection (ucal) assumed same for every injection (wrong for throwaway!)
    N - number of injections

    Returns
    -------
    expected injection heats (ucal)


    """
    # Ln[n] is the ligand concentration in sample cell after n injections
    Xn = numpy.zeros([N])

    # Equation 8 of Tellinghuisen Calibration in isothermal titration calorimetry:
    # heat and cell volume from heat of dilution of NaCl(aq).
    # http://dx.doi.org/10.1016/j.ab.2006.10.015
    vcum = 0.0  # cumulative injected volume (liter)
    for n in range(1,N):
        # Instantaneous injection model (perfusion)
        # dilution factor for this injection (dimensionless)
        vcum += DeltaVn[n]
        vfactor = vcum / V0  # relative volume factor
        # total concentration of ligand in sample cell after n injections (converted from mM to M)
        Xn[n] = 1.e-3 * Xs * (1 - numpy.exp(-vfactor))

    # Equation 12 of same paper as above

    # Compute expected injection heats.
    # q_n_model[n] is the expected heat from injection n
    q_n = numpy.zeros([N])
    r = DeltaVn[0] / (2* V0)
    # Instantaneous injection model (perfusion)
    # first injection
    # converted from cal/mol to ucal
    q_n[0] = V0 * 1.e6 * (L_phi[0] * Xn[0] * (1 + r)) - H_s
    # next injections
    for n in range(1, N):
        r = DeltaVn[n] / (2 * V0)
        # converted from cal/mol to ucal
        q_n[n] = V0 * 1.e6 * (L_phi[n] * Xn[n] * (1 + r) - L_phi[n-1] * Xn[n-1] * (1 - r)) - H_s

    return q_n


def fa(x): return x


def fb(x): return 1 - fa(x)


def fc(x): return 1 / fa(x)


def fd(x): return 1 / fb(x)


def fe(x): return numpy.log(fa(x))


def ff(x): return numpy.log(fb(x))


def fg(x): return numpy.log(fc(x))


def fh(x): return numpy.log(fd(x))


def fi(x): return fa(x) * fb(x)


def fj(x): return 1 - fi(x)


def fk(x): return 1 / fi(x)


def fl(x): return 1 / fj(x)


def fm(x): return numpy.log(fi(x))


def fn(x): return numpy.log(fj(x))


def fo(x): return numpy.log(fk(x))


def fp(x): return numpy.log(fl(x))


@ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None, None, ureg.mole/ureg.kilocal], strict=True)
def titrant_dilution_injection_heats(V0, DeltaVn, Xs, chi, DeltaH, H_0, N, beta):
    """
    Expected heats of injection for two-component binding model.

    ARGUMENTS
    V0 - cell volume (liter)
    DeltaVn - injection volumes (liter)
    Xs - Syringe concentration (millimolar)
    chi - exchange parameter (kcal/mol), (called beta according to Atkins, chi according to Dill)
    DeltaH - Generic dilution enthalpy
    H_0 - mechanical heat of injection (ucal)
    N - number of injections
    beta - 1/kBT (mol/kcal)
    Returns
    -------
    expected injection heats (ucal)


    """
    # Xn[n] is the ligand concentration in sample cell after n+1 injections
    Xn = numpy.zeros(N)
    # X_frac is the mole fraction of X * (1 - mole fraction of x) in the sample cell
    X_frac = numpy.zeros(N)
    X_mfrac = numpy.zeros(N)
    kt = 1/beta
    buffer_mass = 18.01528 # g / mol
    buffer_density = 999.97 # g / liter
    buffer_concentration = buffer_density / buffer_mass # mol /liter

    # Equation 8 of Tellinghuisen Calibration in isothermal titration calorimetry:
    # heat and cell volume from heat of dilution of NaCl(aq).
    # http://dx.doi.org/10.1016/j.ab.2006.10.015
    vcum = 0.0  # cumulative injected volume (liter)
    for n in range(N):
        # Instantaneous injection model (perfusion)
        # dilution factor for this injection (dimensionless)
        vcum += DeltaVn[n]
        vfactor = vcum / V0  # relative volume factor
        # total concentration of ligand in sample cell after n injections (converted from mM to M)
        Xn[n] = 1.e-3 * Xs * (1 - numpy.exp(-vfactor))
        X_frac[n] = mole_fraction(Xn[n], buffer_concentration) # (x * (1-x))
        X_mfrac[n] = x_times_onemx(X_frac[n])

    # Compute expected injection heats.
    # q_n_model[n] is the expected heat from injection n
    q_n = numpy.zeros([N])
    # Instantaneous injection model (perfusion)
    # first injection
    # From units of cal/mole to ucal
    # page 149 of Atkins physical chemistry, 8th edition, eq. 5.30 H^E = n* chi *RT * x_a * x_b


    q_n[0] = 1.e9 * V0 *  ( DeltaH * (fa(X_frac[0])) +  (buffer_concentration + Xn[0]) * chi * kt * (X_mfrac[0])) +  H_0
    for n in range(1, N):
        # subsequent injections
        # From units of cal/mole to ucal
        q_n[n] = 1.e9 * V0 * (DeltaH * (fa(X_frac[n])) + (buffer_concentration + Xn[n]) * chi * kt * (X_mfrac[n])) + ( 2 * H_0 ) - q_n[n-1]
    return q_n



@ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None, ureg.mole/ureg.kilocal], strict=True)
def titrant_exchange_injection_heats(V0, DeltaVn, Xs, chi, H_0, N, beta):
    """
    Expected heats of injection for titrant dilution using exchange parameter chi.

    ARGUMENTS
    V0 - cell volume (liter)
    DeltaVn - injection volumes (liter)
    Xs - Syringe concentration (millimolar)
    chi - exchange parameter (kcal/mol), (called beta according to Atkins, chi according to Dill)
    H_0 - mechanical heat of injection (ucal)
    N - number of injections
    beta - 1/kBT (mol/kcal)
    Returns
    -------
    expected injection heats (ucal)


    """
    # Xn[n] is the ligand concentration in sample cell after n+1 injections
    Xn = numpy.zeros([N])
    # X_frac is the mole fraction of X * (1 - mole fraction of x) in the sample cell
    X_frac = numpy.zeros([N])
    kt = 1/beta
    buffer_mass = 18.01528 # g / mol
    buffer_density = 999.97 # g / liter
    buffer_concentration = buffer_density / buffer_mass # mol /liter

    # Equation 8 of Tellinghuisen Calibration in isothermal titration calorimetry:
    # heat and cell volume from heat of dilution of NaCl(aq).
    # http://dx.doi.org/10.1016/j.ab.2006.10.015
    vcum = 0.0  # cumulative injected volume (liter)
    for n in range(N):
        # Instantaneous injection model (perfusion)
        # dilution factor for this injection (dimensionless)
        vcum += DeltaVn[n]
        vfactor = vcum / V0  # relative volume factor
        # total concentration of ligand in sample cell after n injections (converted from mM to M)
        Xn[n] = 1.e-3 * Xs * (1 - numpy.exp(-vfactor))
        X_frac[n] = x_times_onemx(mole_fraction(Xn[n], buffer_concentration)) # (x * (1-x))

    # Compute expected injection heats.
    # q_n_model[n] is the expected heat from injection n
    q_n = numpy.zeros([N])
    # Instantaneous injection model (perfusion)
    # first injection
    # From units of cal/mole to ucal
    # page 149 of Atkins physical chemistry, 8th edition, eq. 5.30 H^E = n* chi *RT * x_a * x_b
    q_n[0] = 1.e9 * V0 * (buffer_concentration + Xn[0]) * chi * kt * (X_frac[0]) + H_0
    for n in range(1, N):
        # subsequent injections
        # From units of cal/mole to ucal
        q_n[n] = 1.e9 * V0 * (buffer_concentration + Xn[n]) * chi * kt * (X_frac[n]) + (2 * H_0) - q_n[n-1]
    return q_n


@ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None], strict=True)
def deprecated_titrant_dilution_injection_heats(V0, DeltaVn, Xs, DeltaH, H_0, N):
    """
    Expected heats of injection for two-component binding model.

    ARGUMENTS
    V0 - cell volume (liter)
    DeltaVn - injection volumes (liter)
    Xs - Syringe concentration (millimolar)
    DeltaH - total enthalpy of dilution (kcal/mol)
    H_0 - mechanical heat of injection (ucal)
    N - number of injections

    Returns
    -------
    expected injection heats (ucal)


    """
    # Ln[n] is the ligand concentration in sample cell after n+1 injections
    Xn = numpy.zeros([N])

    # Equation 8 of Tellinghuisen Calibration in isothermal titration calorimetry:
    # heat and cell volume from heat of dilution of NaCl(aq).
    # http://dx.doi.org/10.1016/j.ab.2006.10.015
    vcum = 0.0  # cumulative injected volume (liter)
    for n in range(N):
        # Instantaneous injection model (perfusion)
        # dilution factor for this injection (dimensionless)
        vcum += DeltaVn[n]
        vfactor = vcum / V0  # relative volume factor
        # total concentration of ligand in sample cell after n injections (converted from mM to M)
        Xn[n] = 1.e-3 * Xs * (1 - numpy.exp(-vfactor))

    # Compute expected injection heats.
    # q_n_model[n] is the expected heat from injection n
    q_n = numpy.zeros([N])
    # Instantaneous injection model (perfusion)
    # first injection
    # From units of cal/mole to ucal
    q_n[0] = 1.e9 * (DeltaH * V0 * Xn[0]) + H_0
    for n in range(1, N):
        # subsequent injections
        # From units of cal/mole to ucal
        q_n[n] = 1.e9 * (DeltaH * V0 * (Xn[n] - Xn[n - 1]))  + H_0

    return q_n


@ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None], strict=True)
def titrand_dilution_injection_heats(V0, DeltaVn, Mc, DeltaH, H_0, N):
    """
    Expected heats of injection for two-component binding model.

    ARGUMENTS
    V0 - cell volume (liter)
    DeltaVn - injection volumes (liter)
    Mc - cell_concentration (millimolar)
    DeltaH - total enthalpy of dilution (kcal /mol)
    H_0 - mechanical heat of injection (ucal)
    N - number of injections

    Returns
    -------
    expected injection heats (ucal)


    """
    # Mn[n] is the macromolecule concentration in sample cell after n injections
    Mn = numpy.zeros([N])

    dcum = 1.0  # cumulative dilution factor (dimensionless)
    for n in range(N):
        # Instantaneous injection model (perfusion)
        # dilution factor for this injection (dimensionless)
        d = 1.0 - (DeltaVn[n] / V0)
        dcum *= d  # cumulative dilution factor
        # total quantity of protein in sample cell after n injections (converted from mM to M)
        Mn[n] = Mc * 1.e-3 * dcum

    # Compute expected injection heats.
    # q_n_model[n] is the expected heat from injection n
    q_n = numpy.zeros([N])
    # Instantaneous injection model (perfusion)
    # first injection
    # converted from cal/mol to ucal
    q_n[0] = V0 * 1.e9 * (DeltaH * (Mn[0] - Mc)) + H_0
    for n in range(1, N):
        # subsequent injections
        # converted from cal/mol to ucal
        q_n[n] = V0 * 1.e9 * (DeltaH * (Mn[n] - Mn[n - 1])) + H_0

    return q_n


@ureg.wraps(ret=ureg.microcalorie, args=[ureg.liter, ureg.liter, None, None, None, None, None,  ureg.mole / ureg.kilocalories, None], strict=True)
def twocomponent_injection_heats(V0, DeltaVn, P0, Ls, DeltaG, DeltaH, DeltaH_0, beta, N):
    """
    Expected heats of injection for two-component binding model.

    ARGUMENTS
    V0 - cell volume (liter)
    DeltaVn - injection volumes (liter)
    P0 - Cell concentration (millimolar)
    Ls - Syringe concentration (millimolar)
    DeltaG - free energy of binding (kcal/mol)
    DeltaH - enthalpy of binding (kcal/mol)
    DeltaH_0 - heat of injection (ucal)
    beta - inverse temperature * gas constant (mol/kcal)
    N - number of injections

    Returns
    -------
    expected injection heats - ucal


    """
    # TODO Units that go into this need to be verified
    # TODO update docstring with new input

    Kd = exp(beta * DeltaG)   # dissociation constant (M)
    N = N

    # Compute complex concentrations.
    # Pn[n] is the protein concentration in sample cell after n injections
    # (M)
    Pn = numpy.zeros([N])
    # Ln[n] is the ligand concentration in sample cell after n injections
    # (M)
    Ln = numpy.zeros([N])
    # PLn[n] is the complex concentration in sample cell after n injections
    # (M)
    PLn = numpy.zeros([N])
    dcum = 1.0  # cumulative dilution factor (dimensionless)
    for n in range(N):
        # Instantaneous injection model (perfusion)
        # TODO: Allow injection volume to vary for each injection.
        # dilution factor for this injection (dimensionless)
        d = 1.0 - (DeltaVn[n] / V0)
        dcum *= d  # cumulative dilution factor
        # total quantity of protein in sample cell after n injections (converted from mM to mole)
        P = V0 * P0 * 1.e-3 * dcum
        # total quantity of ligand in sample cell after n injections (converted from mM to mole)
        L = V0 * Ls * 1.e-3 * (1. - dcum)
        # complex concentration (M)
        PLn[n] = (0.5 / V0 * ((P + L + Kd * V0) - ((P + L + Kd * V0) ** 2 - 4 * P * L) ** 0.5))
        # free protein concentration in sample cell after n injections (M)
        Pn[n] = P / V0 - PLn[n]
        # free ligand concentration in sample cell after n injections (M)
        Ln[n] = L / V0 - PLn[n]

    # Compute expected injection heats.
    # q_n_model[n] is the expected heat from injection n
    q_n = numpy.zeros([N])
    # Instantaneous injection model (perfusion)
    # first injection
    # converted from kcal/mol to ucal
    q_n[0] = 1.e9 * (DeltaH * V0 * PLn[0]) + DeltaH_0
    for n in range(1, N):
        # subsequent injections
        # converted from kcal/mol to ucal
        q_n[n] = 1.e9 * (DeltaH * V0 * (PLn[n] - PLn[n - 1])) + DeltaH_0

    return q_n
