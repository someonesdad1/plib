'''
Calculate atmospheric properties
    Adapted from http://www.pdas.com/programs/atmos.f90 (included below).

    The equations are taken from the NASA publication "U.S. Standard
    Atmosphere 1976".  A PDF can be downloaded from
    http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19770009539_1977009539.pdf

    The "hydrostatic constant" is g0'*M0/R, where g0' is a constant that
    relates geopotential meters to geometric height (units of
    m^2/(s^2*m') where m' is a geopotential meter, M0 is the sea-level
    mean molar mass of the air, and R is the universal gas constant in
    J/(mol*K).  See equation 33b in the NASA paper.
  
    [eq 33] is equation 33 in the paper and [5] refers to page 5.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2010 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <science> Calculate standard atmosphere characteristicx
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    from math import exp, sqrt, pi
if 1:  # Custom imports
    from wrap import dedent
    from fpformat import FPFormat
    from u import u
    from pdb import set_trace as xx
    from sig import sig
if 1:  # Global variables
    fp = FPFormat()
    radius_earth = 6369.0   # Radius of the Earth (km)
    gmr = 34.163195         # Hydrostatic constant
    P0 = 101325             # Standard sea-level atmospheric pressure in Pa
    T0 = 288.15             # Standard sea-level temperature, K
    M0 = 28.9644/1000       # Mean molecular weight for air, kg/mol
    rho0 = 1.225            # Sea-level density in kg/m^3
    R = 8.32432             # Universal gas constant N*m/(mol*K) [3]
    sigma = 3.65e-10        # Effective collision diameter, m [17]
    gamma = 1.40            # Specific heat ratio cp/cv
    Na = 6.022169e23        # Avogadro's constant, 1/mol [2]
    # Standard sea-level acceleration of gravity at a latitude of 45.5425
    # degrees. [3]
    g0 = 9.80665
if 1:  # Original FORTRAN code
    def _Code():
        '''Original FORTRAN90 code from http://www.pdas.com/programs/atmos.f90.
        See http://www.pdas.com/atmos.htm.
        !+
        SUBROUTINE Atmosphere(alt, sigma, delta, theta)
        !   -------------------------------------------------------------------------
        ! PURPOSE - Compute the properties of the 1976 standard atmosphere to 86 km.
        ! AUTHOR - Ralph Carmichael, Public Domain Aeronautical Software
        ! NOTE - If alt > 86, the values returned will not be correct, but they will
        !   not be too far removed from the correct values for density.
        !   The reference document does not use the terms pressure and temperature
        !   above 86 km.
        IMPLICIT NONE
        !============================================================================
        !     A R G U M E N T S                                                     |
        !============================================================================
        REAL,INTENT(IN)::  alt        ! geometric altitude, km.
        REAL,INTENT(OUT):: sigma      ! density/sea-level standard density
        REAL,INTENT(OUT):: delta      ! pressure/sea-level standard pressure
        REAL,INTENT(OUT):: theta      ! temperature/sea-level standard temperature
        !============================================================================
        !     L O C A L   C O N S T A N T S                                         |
        !============================================================================
        REAL,PARAMETER:: REARTH = 6369.0                 ! radius of the Earth (km)
        REAL,PARAMETER:: GMR = 34.163195                     ! hydrostatic constant
        INTEGER,PARAMETER:: NTAB=8       ! number of entries in the defining tables
        !============================================================================
        !     L O C A L   V A R I A B L E S                                         |
        !============================================================================
        INTEGER:: i,j,k                                                  ! counters
        REAL:: h                                       ! geopotential altitude (km)
        REAL:: tgrad, tbase      ! temperature gradient and base temp of this layer
        REAL:: tlocal                                           ! local temperature
        REAL:: deltah                             ! height above base of this layer
        !============================================================================
        !     L O C A L   A R R A Y S   ( 1 9 7 6   S T D.  A T M O S P H E R E )   |
        !============================================================================
        REAL,DIMENSION(NTAB),PARAMETER:: htab= &
                                (/0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0, 84.852/)
        REAL,DIMENSION(NTAB),PARAMETER:: ttab= &
                (/288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946/)
        REAL,DIMENSION(NTAB),PARAMETER:: ptab= &
                    (/1.0, 2.233611E-1, 5.403295E-2, 8.5666784E-3, 1.0945601E-3, &
                                            6.6063531E-4, 3.9046834E-5, 3.68501E-6/)
        REAL,DIMENSION(NTAB),PARAMETER:: gtab= &
                                        (/-6.5, 0.0, 1.0, 2.8, 0.0, -2.8, -2.0, 0.0/)
        !----------------------------------------------------------------------------
        h=alt*REARTH/(alt+REARTH)      ! convert geometric to geopotential altitude
        
        i=1
        j=NTAB                                       ! setting up for binary search
        DO
            k=(i+j)/2                                              ! integer division
            IF (h < htab(k)) THEN
            j=k
            ELSE
            i=k
            END IF
            IF (j <= i+1) EXIT
        END DO
        
        tgrad=gtab(i)                                     ! i will be in 1...NTAB-1
        tbase=ttab(i)
        deltah=h-htab(i)
        tlocal=tbase+tgrad*deltah
        theta=tlocal/ttab(1)                                    ! temperature ratio
        
        IF (tgrad == 0.0) THEN                                     ! pressure ratio
            delta=ptab(i)*EXP(-GMR*deltah/tbase)
        ELSE
            delta=ptab(i)*(tbase/tlocal)**(GMR/tgrad)
        END IF
        
        sigma=delta/theta                                           ! density ratio
        RETURN
        END Subroutine Atmosphere   ! -----------------------------------------------
        '''
def atm(altitude_km):
    '''Returns a dictionary of the SI properties of air at the given
    geometric height, which is 0 for sea-level.  The returned
    dictionary is
        {
            "density"           : d,     # kg/m^3
            "pressure"          : p,     # Pa
            "temperature"       : t,     # K
            "g"                 : g,     # m/s^2
            "speed of sound"    : Cs,    # m/s
            "dynamic viscosity" : nu,    # N*s/m^2
            "mean free path"    : mfp,   # m
        }
    The values returned will be floating point numbers.
    '''
    results = {}
    htab = (0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0, 84.852)
    ttab = (288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946)
    ptab = (1.0, 2.233611e-1, 5.403295e-2, 8.5666784e-3, 1.0945601e-3,
            6.6063531e-4, 3.9046834e-5, 3.68501e-6)
    gtab = (-6.5, 0.0, 1.0, 2.8, 0.0, -2.8, -2.0, 0.0)
    # Geometric to geopotential altitude
    h = altitude_km*radius_earth/(altitude_km + radius_earth)
    i, j = 0, 7   # Set up binary search
    while 1:
        k = (i + j)//2
        if h < htab[k]:
            j = k
        else:
            i = k
        if j <= i+1:
            break
    tgrad = gtab[i]
    tbase = ttab[i]
    deltah = h - htab[i]
    tlocal = tbase + tgrad*deltah
    tr = tlocal/ttab[0]     # Reduced temperature
    if tgrad == 0.0:        # Reduced pressure
        pr = ptab[i]*exp(-gmr*deltah/tbase)
    else:
        pr = ptab[i]*(tbase/tlocal)**(gmr/tgrad)
    rhor = pr/tr            # Reduced density
    T = T0*tr
    results["density"] = rho0*rhor
    results["pressure"] = P0*pr
    results["temperature"] = T0*tr
    results["g"] = g0*(radius_earth/(radius_earth + altitude_km))**2
    results["speed of sound"] = sqrt(gamma*R*T/M0)
    results["dynamic viscosity"] = 1.458e-6*T**(1.5)/(T + 110.4)
    results["mean free path"] = sqrt(2)*R*T/(2*pi*Na*sigma**2*P0*pr)
    return results
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    digits = d["-d"]
    print(dedent(f'''
    Usage:  {name} altitude [unit]
    Prints the density, pressure, and temperature for altitudes between
    -5 and 86 km.  From the 1976 NASA standard atmosphere.
    
    Note:  you can include an optional unit for the altitude (any common
    unit will work).  The number is interpreted in km if no unit is given.

    Options:
        -d digits
            Specify the number of significant figures. [{digits}]
        -t
            Print a table of the standard atmosphere in km heights.
    '''[1:-1]))
    exit(status)
def ParseCommandLine(d):
    d["-t"] = False         # Print table
    d["-d"] = 4             # Number of significant digits
    d["--test"] = False     # Number of significant digits
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:t", "test")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = ("-d option's argument must be an integer between "
                       "1 and 15")
                Error(msg)
        elif o in ("-t",):
            d["-t"] = not d["-t"]
        elif o in ("--test",):
            exit(run(globals(), halt=1)[0])
    if not args and not d["-t"]:
        Usage(d)
    fp.digits(d["-d"])
    sig.digits = d["-d"]
    return args
def GetHeight_km(args):
    to_km = 1
    if len(args) == 2:
        try:
            to_km = u(args[1])/u("km")
        except Exception:
            print("Unit '{}' is not recognized".format(args[1]))
            exit(1)
    z_km = float(args[0])*to_km
    if z_km < -5 or z_km > 86:
        print("Altitude must be between -5 and 86 km.")
        exit(1)
    return z_km
def PrintHeight(args, opts):
    digits = opts["-d"]
    fmt = lambda x, digits: ("%%.%dg" % digits) % x
    e = fp.engsi
    # Height
    z_km = GetHeight_km(args)
    Z_km = sig(z_km)
    Z_ft = sig(1000*z_km/u("ft"))
    Z_mi = sig(1000*z_km/u("mi"))
    prop = atm(z_km)
    prop0 = atm(0)
    # Density
    d = prop["density"]
    d0 = e(d/prop0["density"]).strip()
    D_SI = sig(d)
    D_lbpin3 = e(d/u("lbm/in3"))
    D_lbpft3 = e(d/u("lbm/ft3"))
    # Pressure
    p = prop["pressure"]
    p0 = e(p/prop0["pressure"]).strip()
    P_kPa = sig(p/1000)
    P_psi = e(p/u("psi"))
    P_torr = e(p/u("torr"))
    P_atm = e(p/u("atm"))
    # Temperature
    t = prop["temperature"]
    t0 = e(t/prop0["temperature"]).strip()
    T_SI = sig(t)
    T_C = t - 273.15
    T_degC = sig(T_C)
    T_degF = sig(9/5*T_C + 32)
    # Gravity
    g = prop["g"]
    g0 = e(g/prop0["g"]).strip()
    G_SI = sig(g)
    # Speed of sound
    Cs = prop["speed of sound"]
    CS_SI = sig(Cs)
    CS_mph = sig(Cs/u("mph"))
    # Viscosity
    mu = prop["dynamic viscosity"]
    nu = mu/float(d)   # Kinematic viscosity
    MU_SI = e(mu)
    NU_SI = e(nu)
    # Mean free path
    mfp = prop["mean free path"]
    mfp0 = e(prop0["mean free path"]/mfp).strip()
    MFP_SI = e(mfp)
    # Print results
    print(dedent(f'''
    1976 Standard atmosphere properties at {Z_km} km ({Z_ft} ft, {Z_mi} mi):
      [Reduced values with respect to sea level are in square brackets]
      Density                 = {D_SI} kg/m^3             [{d0}]
                              = {D_lbpin3}lbm/in^3
                              = {D_lbpft3}lbm/ft^3
      Pressure                = {P_kPa} kPa                [{p0}]
                              = {P_psi}psi
                              = {P_torr}torr
                              = {P_atm}atm
      Temperature             = {T_SI} K                  [{t0}]
                              = {T_degC} °C
                              = {T_degF} °F
      Acceleration of gravity = {G_SI} m/s^2              [{g0}]
      Speed of sound          = {CS_SI} m/s
                              = {CS_mph} mi/hr
      Dynamic viscosity       = {MU_SI}(N*s/m^2)
      Kinematic viscosity     = {NU_SI}(m^2/s)
      Mean free path          = {MFP_SI}m                 [{mfp0}]
    '''))
def PrintTable(args, d):
    n = d["-d"] + 8
    e = fp.engsic
    fmt = "{z_km:5d} {d:^{n}s} {p:^{n}s} {t:^{n}s} {g:^{n}s} {Cs:^{n}s}"
    header = dedent('''
    Height  Density      Pressure      Temp      Acc. grav.   Speed of Sound
      km     kg/m3          Pa          K            m/s2         m/s
    ''')
    print(header)
    #for z_km in range(-5, 87):
    for z_km in range(-5, 31):
        prop = atm(z_km)
        d = e(prop["density"])
        p = e(prop["pressure"])
        t = e(prop["temperature"])
        g = e(prop["g"])
        Cs = e(prop["speed of sound"])
        print(fmt.format(**locals()))
    print(header)
if __name__ == "__main__":
    # Unit test stuff
    import subprocess
    from time import sleep
    from lwtest import run, assert_equal, raises
    def GetReferenceData():
        '''Return the altitude in km, along with sigma = reduced density,
        delta = reduced pressure, theta = reduced temperature (reduced means
        divided by the sea level values).
    
        The expected form of the output data of the atm command is:
            NASA reference atmosphere function by R. Carmichael
            Reduced atmosphere values at    5.00000000     km
            sigma = reduced density     =  0.601166010    
            delta = reduced pressure    =  0.533414602    
            theta = reduced temperature =  0.887300014    
        '''
        # Note:  this script used to run the atm command, which was the
        # atm.f90 code.  Now it just returns the above numbers.
        h_km, sigma, delta, theta = 5, 0.601166010, 0.533414602, 0.887300014
        return h_km, sigma, delta, theta
    def Test():
        altitude_km, sigma, delta, theta = GetReferenceData()
        d = atm(altitude_km)
        rho = sigma*rho0
        P = delta*P0
        T = theta*T0
        if 0:
            print("Density =", rho)
            print("Pressure =", P)
            print("Temperature =", T)
            from pprint import pprint as pp
            pp(d)
        eps = 1e-6
        assert_equal(rho, d["density"], reltol=eps)
        assert_equal(P, d["pressure"], reltol=eps)
        assert_equal(T, d["temperature"], reltol=eps)
if __name__ == "__main__": 
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-t"]:
        PrintTable(args, d)
    else:
        PrintHeight(args, d)
