"""
TODO

* Change reduced stuff in brackets to be % of sea level.  Using the SI
  prefixes unadorned is confusing.

----------------------------------------------------------------------
Calculate atmospheric properties
    Adapted from http://www.pdas.com/programs/atmos.f90 (included below).

    The equations are taken from the NASA publication "U.S. Standard
    Atmosphere 1976".  A PDF can be downloaded from
    http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19770009539_1977009539.pdf
    (Defunct as of 13 Jun 2021)

    The "hydrostatic constant" is g0'*M0/R, where g0' is a constant that
    relates geopotential meters to geometric height (units of
    m^2/(s^2*m') where m' is a geopotential meter, M0 is the sea-level
    mean molar mass of the air, and R is the universal gas constant in
    J/(mol*K).  See equation 33b in the NASA paper.

    [eq 33] is equation 33 in the paper and [5] refers to page 5.
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2010 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # <science> Calculate standard atmosphere characteristics.
        # Equations taken from a 1976 NASA document.
        ##∞what∞#
        ##∞test∞# --test #∞test∞#
        pass
    if 1:  # Imports
        import getopt
        import os
        import sys
        from math import exp, sqrt, pi
    if 1:  # Custom imports
        from lwtest import assert_equal, Assert
        from wrap import dedent
        from fpformat import FPFormat
        from u import u
        from f import flt
        from color import t as T
        from pdb import set_trace as xx
        from sig import sig
    if 1:  # Global variables
        ii = isinstance
        fp = FPFormat()
        radius_earth = 6369.0  # Radius of the Earth (km)
        gmr = 34.163195  # Hydrostatic constant
        P0 = 101325  # Standard sea-level atmospheric pressure in Pa
        T0 = 288.15  # Standard sea-level temperature, K
        M0 = 28.9644 / 1000  # Mean molecular weight for air, kg/mol
        rho0 = 1.225  # Sea-level density in kg/m^3
        R = 8.32432  # Universal gas constant N*m/(mol*K) [3]
        sigma = 3.65e-10  # Effective collision diameter, m [17]
        gamma = 1.40  # Specific heat ratio cp/cv
        Na = 6.022169e23  # Avogadro's constant, 1/mol [2]
        # Standard sea-level acceleration of gravity at a latitude of 45.5425
        # degrees. [3]
        g0 = 9.80665
if 1:  # Original FORTRAN code

    def _Code():
        """Original FORTRAN90 code from http://www.pdas.com/programs/atmos.f90.
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
        """


if 1:  # Utility

    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)

    def Usage(d, status=1):
        name = sys.argv[0]
        digits = d["-d"]
        print(
            dedent(
                f"""
        Usage:  {name} altitude [unit]
          Prints the density, pressure, and temperature for altitudes between
          -5 and 86 km.  From the 1976 NASA standard atmosphere.
        
          Note:  you can include an optional unit for the altitude (any common
          unit will work).  The number is interpreted in km if no unit is given.
        Options:
          -d n      Number of significant figures. [{digits}]
          -t        Print a table of the standard atmosphere in km heights
        """[1:-1]
            )
        )
        exit(status)

    def ParseCommandLine(d):
        d["-t"] = False  # Print table
        d["-d"] = 4  # Number of significant digits
        d["--test"] = False  # Number of significant digits
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
                    msg = "-d option's argument must be an integer between 1 and 15"
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


if 1:  # Core functionality

    def atm(altitude_km):
        """Returns a dictionary of the SI properties of air at the given
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
        """
        z_km = float(altitude_km)
        if not (-5 <= z_km <= 86):
            raise ValueError("altitude_km must be between -5 and 86 km")
        results = {}
        htab = (0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0, 84.852)
        ttab = (288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946)
        ptab = (
            1.0,
            2.233611e-1,
            5.403295e-2,
            8.5666784e-3,
            1.0945601e-3,
            6.6063531e-4,
            3.9046834e-5,
            3.68501e-6,
        )
        gtab = (-6.5, 0.0, 1.0, 2.8, 0.0, -2.8, -2.0, 0.0)
        # Geometric to geopotential altitude
        h = z_km * radius_earth / (z_km + radius_earth)
        i, j = 0, 7  # Set up binary search
        while 1:
            k = (i + j) // 2
            if h < htab[k]:
                j = k
            else:
                i = k
            if j <= i + 1:
                break
        tgrad = gtab[i]
        tbase = ttab[i]
        deltah = h - htab[i]
        tlocal = tbase + tgrad * deltah
        tr = tlocal / ttab[0]  # Reduced temperature
        if tgrad == 0.0:  # Reduced pressure
            pr = ptab[i] * exp(-gmr * deltah / tbase)
        else:
            pr = ptab[i] * (tbase / tlocal) ** (gmr / tgrad)
        rhor = pr / tr  # Reduced density
        T = T0 * tr
        results["density"] = rho0 * rhor
        results["pressure"] = P0 * pr
        results["temperature"] = T0 * tr
        results["g"] = g0 * (radius_earth / (radius_earth + z_km)) ** 2
        results["speed of sound"] = sqrt(gamma * R * T / M0)
        results["dynamic viscosity"] = 1.458e-6 * T ** (1.5) / (T + 110.4)
        results["mean free path"] = sqrt(2) * R * T / (2 * pi * Na * sigma**2 * P0 * pr)
        return results

    def GetHeight_km(args):
        to_km = 1
        if len(args) == 2:
            try:
                to_km = u(args[1]) / u("km")
            except Exception:
                print("Unit '{}' is not recognized".format(args[1]))
                exit(1)
        z_km = float(args[0]) * to_km
        if z_km < -5 or z_km > 86:
            print("Altitude must be between -5 and 86 km.")
            exit(1)
        return z_km

    def PrintHeight(args, opts):
        def F(a, b):
            "Return 100*a/prop0[b] in %"
            return sig(100 * a / prop0[b], 3) + "%"

        digits = opts["-d"]
        e = fp.engsi
        # Height
        z_km = GetHeight_km(args)
        Z_km = sig(z_km)
        Z_ft = sig(1000 * z_km / u("ft"))
        Z_mi = sig(1000 * z_km / u("mi"))
        prop = atm(z_km)
        prop0 = atm(0)
        # Density
        d = prop["density"]
        d0 = F(d, "density")
        D_SI = sig(d)
        D_lbpin3 = e(d / u("lbm/in3"))
        D_lbpft3 = e(d / u("lbm/ft3"))
        # Pressure
        p = prop["pressure"]
        p0 = F(p, "pressure")
        P_kPa = sig(p / 1000)
        P_psi = e(p / u("psi"))
        P_torr = e(p / u("torr"))
        P_atm = e(p / u("atm"))
        # Temperature
        t = prop["temperature"]
        t0 = F(t, "temperature")
        T_SI = sig(t)
        T_C = t - 273.15
        T_degC = sig(T_C)
        T_degF = sig(9 / 5 * T_C + 32)
        # Gravity
        g = prop["g"]
        g0 = F(g, "g")
        G_SI = sig(g)
        # Speed of sound
        Cs = prop["speed of sound"]
        CS_SI = sig(Cs)
        CS_mph = sig(Cs / u("mph"))
        # Viscosity
        mu = prop["dynamic viscosity"]
        nu = mu / float(d)  # Kinematic viscosity
        MU_SI = e(mu)
        NU_SI = e(nu)
        # Mean free path
        mfp = prop["mean free path"]
        mfp0 = F(mfp, "mean free path")
        MFP_SI = e(mfp)
        # Print results
        T.c = T("ornl")
        print(
            dedent(f"""
        1976 Standard atmosphere properties at {Z_km} km ({Z_ft} ft, {Z_mi} mi):
          [Reduced values with respect to sea level are in color]
          Density                 = {D_SI} kg/m^3             [{T.c}{d0}{T.n}]
                                  = {D_lbpin3}lbm/in^3
                                  = {D_lbpft3}lbm/ft^3
          Pressure                = {P_kPa} kPa                [{T.c}{p0}{T.n}]
                                  = {P_psi}psi
                                  = {P_torr}torr
                                  = {P_atm}atm
          Temperature             = {T_SI} K                     [{T.c}{t0}{T.n}]
                                  = {T_degC} °C
                                  = {T_degF} °F
          Acceleration of gravity = {G_SI} m/s^2                 [{T.c}{g0}{T.n}]
          Speed of sound          = {CS_SI} m/s
                                  = {CS_mph} mi/hr
          Dynamic viscosity       = {MU_SI}(N*s/m^2)
          Kinematic viscosity     = {NU_SI}(m^2/s)
          Mean free path          = {MFP_SI}m                    [{T.c}{mfp0}{T.n}]
        """)
        )

    def PrintTable(args, d):
        n = d["-d"] + 8
        e = fp.engsic
        fmt = "{z_km:5d} {d:^{n}s} {p:^{n}s} {t:^{n}s} {g:^{n}s} {Cs:^{n}s}"
        header = dedent("""
        Height  Density      Pressure      Temp      Acc. grav.   Speed of Sound
          km     kg/m3          Pa          K            m/s2         m/s
        """)
        print(header)
        for z_km in range(-5, 31):
            prop = atm(z_km)
            d = e(prop["density"])
            p = e(prop["pressure"])
            t = e(prop["temperature"])
            g = e(prop["g"])
            Cs = e(prop["speed of sound"])
            print(fmt.format(**locals()))
        print(header)


if 1:  # Another properties function

    def atm2(hm):
        """Return (T, p, ρ) where
            T is absolute temperature in K
            p is pressure in Pa
            ρ is density in kg/m³
        for the standard atmosphere at height hm in meters above sea level.

        The height hm can either be a flt (from f.py) instance with optional length dimensions or
        can be a number convertible to a float.  The allowed range for hm is 0 to 85 km.
        """
        # Formulas from http://nebula.wsimg.com/ab321c1edd4fa69eaa94b5e8e769b113?AccessKeyId=AF1D67CEBF3A194F66A3&disposition=0&alloworigin=1
        """
        Calculation of Earth's atmospheric properties
 
        Text from the web page:
 
        The "standard atmosphere" is a hypothetical vertical distribution of atmospheric properties
        which, by international agreement, is roughly representative of year-round, mid-latitude
        conditions.  Typical usages include altimeter calibrations and aircraft design and
        performance calculations. It should be recognized that actual conditions may vary
        considerably from this standard.
 
        The most recent definition is the "US Standard Atmosphere, 1976" developed jointly by NOAA,
        NASA, and the USAF. It is an idealized, steady state representation of the earth's
        atmosphere from the surface to 1000 km, as it is assumed to exist during a period of
        moderate solar activity. The 1976 model is identical with the earlier 1962 standard up to
        51 km, and with the International Civil Aviation Organization (ICAO) standard up to 32 km.
 
        Up to 86 km, the model assumes a constant mean molecular weight, and comprises of a series
        of six layers, each defined by a linear temperature gradient (lapse rate). (The assumption
        of linearity conveniently avoids the need for numerical integration in the computation of
        properties.) The bottom layer, with a negative lapse rate, represents the earth's
        troposphere, a region where most clouds form, and with generally turbulent conditions.
        Higher layers form part of the earth's stratosphere, where winds may be high, but
        turbulence is generally low.
 
        The model is derived by assuming a constant value for g (gravitational acceleration).
        Strictly speaking, altitudes in this model should therefore be referred to as "geopotential
        altitudes" rather than "geometric altitudes" (physical height above mean sea level). The
        relationship between these altitudes is given by:
 
        hgeometric = hgeopotential x Rearth / (Rearth - hgeopotential)
 
        where Rearth is the earth's effective radius. The difference is small, with geometric
        altitude and geopotential altitude differing from by less than 0.5% at 30 km (~100,000 ft).
 
        The standard is defined in terms of the International System of Units (SI). The air is
        assumed to be dry and to obey the perfect gas law and hydrostatic equation, which, taken
        together, relate temperature, pressure and density with geopotential altitude.
 
        It should also be noted that since the standard atmosphere model does not include humidity,
        and since water has a lower molecular weight than air, its presence produces a lower
        density. Under extreme circumstances, this can amount to as much as a 3% reduction, but
        typically is less than 1% and may be neglected.
 
        Symbols
 
        The following symbols are used to define the relationships between variables in the model.
        Subscript n indicates conditions at the base of the nth layer (or at the top of the (n-1)th
        layer) or refers to the constant lapse rate in the nth layer.  The first layer is
        considered to be layer 0, hence subscript 0 indicates standard, sea level conditions, or
        lapse rate in the bottom layer.
 
            h = Pressure/Geopotential Altitude
            T = Temperature
            p = Pressure
            ρ = Density
            θ = T/T0 (Temperature Ratio)
            δ = p/p0 (Pressure Ratio)
            σ = ρ/ρ0 (Density Ratio)
            μ = Dynamic Viscosity
            ν = μ/ρ = Kinematic Viscosity
        """
        # Sea level values
        T0 = flt(288.15, "K")  # Temperature (15 °C)
        p0 = flt(101325, "Pa")  # Pressure
        ρ0 = flt(1.225, "kg/m3")  # Density
        # Check incoming height
        e = TypeError("hm must be >= 0")
        if ii(hm, flt):
            if hm.u is not None:
                try:
                    h = float(hm.to("ft").val)
                except Exception:
                    raise TypeError("hm must be a length dimension")
            else:
                h = flt(float(hm), "m").to("ft")
            if h < 0:
                raise e
        else:
            h = flt(float(hm), "m").to("ft")
            if h < 0:
                raise e
        # Note:  I used the web page's numerical solutions where h is
        # converted to feet because the formulas can be pasted in and
        # fixed with minor editing.
        #
        # θ = T/T0 temperature ratio to sea level
        # δ = p/p0 pressure ratio to sea level
        # σ = ρ/ρ0 density ratio to sea level
        if h <= 36089:
            θ = 1 - h / 145442
            δ = (1 - h / 145442) ** 5.255876
            σ = (1 - h / 145442) ** 4.255876
        elif 36089 < h <= 65617:  # Isothermal
            θ = 0.751865
            δ = 0.223361 * exp(-(h - 36089) / 20806)
            σ = 0.297076 * exp(-(h - 36089) / 20806)
        elif 65617 < h <= 104987:  # Inversion
            θ = 0.682457 + h / 945374
            δ = (0.988626 + h / 652600) ** (-34.16320)
            σ = (0.978261 + h / 659515) ** (-35.16320)
        elif 104987 < h <= 154199:  # Inversion
            θ = 0.482561 + h / 337634
            δ = (0.898309 + h / 181373) ** (-12.20114)
            σ = (0.857003 + h / 190115) ** (-13.20114)
        elif 154199 < h <= 167323:  # Isothermal
            θ = 0.939268
            δ = 0.00109456 * exp(-(h - 154199) / 25992)
            σ = 0.00116533 * exp(-(h - 154199) / 25992)
        elif 167323 < h <= 232940:
            θ = 1.434843 - h / 337634
            δ = (0.838263 - h / 577922) ** 12.20114
            σ = (0.798990 - h / 606330) ** 11.20114
        elif 232940 < h <= 278386:
            θ = 1.237723 - h / 472687
            δ = (0.917131 - h / 637919) ** 17.08160
            σ = (0.900194 - h / 649922) ** 16.08160
        else:
            raise ValueError("h must be <= 84852 m")
        if 0:
            print(f"θ δ σ = {flt(θ)} {flt(δ)._sci()} {flt(σ)._sci()}")
        T = θ * T0
        p = δ * p0
        ρ = σ * ρ0
        assert T.u == "K"
        assert p.u == "Pa"
        assert ρ.u == "kg/m3"
        return (T, p, ρ)

    def Compare_atm2_to_atm():
        dev = ["Height      kFeet      Temp_dev%      Press_dev%    Density_dev%"]

        def f(x, y):
            str(flt(100 * (x - y) / y))

        for km in range(0, 85, 2):
            Z = flt(km, "km")
            z = flt(km * 1000, "m")
            Tnew, pnew, rhonew = atm2(z)
            old = atm(km)
            Told, pold, rhoold = (
                flt(old["temperature"], "K"),
                flt(old["pressure"], "Pa"),
                flt(old["density"], "kg/m3"),
            )
            s = []
            with Z:
                Z.n = 2
                t = str(Z).replace("\xa0", " ")
            kft = Z.to("kft").val
            kft = str(flt(kft))
            n = 14
            s.append(f"{t:8s}")
            s.append(f"{kft:>8s}")
            with Z:
                Z.n = 2
                s.append(f"   {f(Tnew, Told):^{n}s}")
                s.append(f"{f(pnew, pold):^{n}s}")
                s.append(f"{f(rhonew, rhoold):^{n}s}")
            dev.append(" ".join(s))
        for i in dev:
            print(i)


if 1:  # Unit tests

    def GetReferenceData():
        """Return the altitude in km, along with sigma = reduced density,
        delta = reduced pressure, theta = reduced temperature (reduced means
        divided by the sea level values).

        The expected form of the output data of the atm command is:
            NASA reference atmosphere function by R. Carmichael
            Reduced atmosphere values at    5.00000000     km
            sigma = reduced density     =  0.601166010
            delta = reduced pressure    =  0.533414602
            theta = reduced temperature =  0.887300014
        """
        # Note:  this script used to run the atm command, which was the
        # atm.f90 code.  Now it just returns the above numbers.
        h_km, sigma, delta, theta = 5, 0.601166010, 0.533414602, 0.887300014
        return h_km, sigma, delta, theta

    def Test_atm_1():
        altitude_km, sigma, delta, theta = GetReferenceData()
        d = atm(altitude_km)
        rho = sigma * rho0
        P = delta * P0
        T = theta * T0
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

    def Test_atm_2():
        """The following data came from table 1 in "U.S. Standard
        Atmosphere 1976" published by NASA.  The columns used in the
        table are
            2       Z, geometrical height in m
            3       T in K
            6       P, pressure in mbar = 100 Pa
            9       Density in kg/m3
        Maximum relative diff in % for the data below was 0.0078%.
        Thus, the atm() function fits the NASA paper's data to better
        than 1 part in 10,000 at the tested points; this is a pretty
        good indication that the algorithm is correct.
        """

        def RelDiffPct(a, b):
            return 100 * (a - b) / b

        data = """
        # Col  2       3            6         9
            -4996   320.65      1.7768e3    1.9305e0
            -3997   314.15      1.5955e3    1.7693e0
            -1999   301.15      1.2777e3    1.4781e0
                0   288.15      1.01325e3   1.2250e0
             1000   281.65      8.9874e2    1.1116e0
             5004   255.65      5.4019e2    7.3612e-1
            10016   223.15      2.6436e2    4.1271e-1
            20063   216.65      5.4748e1    8.8035e-2
            30041   226.55      1.1896e1    1.8294e-2
            49990   270.65      7.9877e-1   1.0281e-3
        #  100389   199.53      2.3144e-4   3.935e-7
        """[1:].rstrip()
        flt(0).n = 2
        rd = RelDiffPct
        o = []
        for line in data.split("\n"):
            L = line.strip()
            if not L or L[0] == "#":
                continue
            f = L.split()
            Z = flt(f[0])  # m
            T = flt(f[1])  # K
            P = flt(f[2]) * 100  # Pa (f[2] in mbar)
            ρ = flt(f[3])  # kg/m3
            d = atm(Z / 1000)  # atm arg is in km
            Td = flt(d["temperature"])  # K
            Pd = flt(d["pressure"])  # Pa
            ρd = flt(d["density"])  # kg/m3
            o.extend([rd(Td, T), rd(Pd, P), rd(ρd, ρ)])
            Assert(rd(Pd, P) < 0.01)
            Assert(rd(ρd, ρ) < 0.01)
            Assert(rd(Td, T) < 0.01)
            Assert(rd(Pd, P) < 0.01)
            Assert(rd(ρd, ρ) < 0.01)
        if 0:
            m = max([abs(i) for i in o])
            print(f"Max % relative diff = {m}")


if __name__ == "__main__":
    # Run the self tests
    Test_atm_1()
    Test_atm_2()
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if d["-t"]:
        PrintTable(args, d)
    else:
        PrintHeight(args, d)
