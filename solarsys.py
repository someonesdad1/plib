'''

TODO
    - Use -x option to force using SI prefixes in printing
    - When -r is used, relative values are printed in color.  When you
      don't see color, the relative value was zero.

Module that contains basic data on solar system objects
    When run as a script, produces tables and plots.

    Core information from
    https://en.wikipedia.org/wiki/List_of_gravitationally_rounded_objects_of_the_Solar_System
    These data were gotten by screen scraping the tables and getting rid of
    the extra numbers.

    The global dictionary solarsys contains the following keys:
        name    Object's name
        name_lc Object's name (all lower case)
        sym     Symbol
        d       Distance from primary, m
        r       Mean radius, m
        m       Mass, kg
        g       Equatorial gravitational acceleration, m/s2
        ev      Escape velocity, m/s
        rot     Rotation period, s
        orb     Orbital period, s
        vel     Orbital speed, m/s
        ecc     Eccentricity
        inc     Inclination, degrees
        tilt    Axial tilt, degrees
        moons   Number of moons
        T       Mean surface temperature, K


'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import defaultdict
        from pprint import pprint as pp
        import getopt
        import math
        import os
        import re
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        import f as F
        from u import u
        from columnize import Columnize
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colors
        t.name = t("ornl")
        t.rel = t("grnl")
        t.notrel = t("lipl")
        t.nan = t("redl")
if 1:   # Solar system data
    # https://en.wikipedia.org/wiki/List_of_gravitationally_rounded_objects_of_the_Solar_System
    scrape_date = "18 Feb 2023"
    names = '''
        Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune
        Ceres Pluto Haumea Makemake Eris
        Orcus Salacia Quaoar Gonggong Sedna
        Moon Io Europa Ganymede Callisto Mimas Enceladus Tethys Dione Rhea
        Titan Iapetus Miranda Ariel Umbriel Titania Oberon Triton Charon Dysnomia
    '''.split()
    symbols = '''
        None None None None None None None None
        None None None None None
        None None None None None
        E1 J1 J2 J3 J4 S1 S2 S3 S4 S5
        S6 S8 U5 U1 U2 U3 U4 N1 P1 None
    '''.split()
    dist_km = '''
        57909175 108208930 149597890 227936640 778412010 1426725400 2870972200 4498252900
        413700000 5906380000 6484000000 6850000000 10210000000
        5896946000 6310600000 6535930000 10072433340 78668000000
        384399 421600 670900 1070400 1882700 185520 237948 294619 377396 527108
        1221870 3560820 129390 190900 266000 436300 583519 354759 17536 37300
    '''.split()
    radius_km = '''
        2440.53 6051.8 6378.1366 3396.19 71492 60268 25559 24764
        473 1188.3 816 715 1163
        458.5 423 560.5 615 497.5
        1737.1 1815 1569 2634.1 2410.3 198.30 252.1 533 561.7 764.3
        2576 735.60 235.8 578.9 584.7 788.9 761.4 1353.4 603.5 350
    '''.split()
    mass_kg = '''
        3.302e23 4.8690e24 5.972e24 6.4191e23 1.8987e27 5.6851e26 8.6849e25 1.0244e26
        9.39e20 1.30e22 4.0e21 3.1e21 1.65e22
        6.32e20 4.9e20 1.41e21 1.75e21 ?
        7.3477e22 8.94e22 4.80e22 14.819e22 10.758e22 0.00375e22 0.0108e22 0.06174e22 0.1095e22 0.2306e22
        13.452e22 0.18053e22 0.00659e22 0.135e22 0.12e22 0.35e22 0.3014e22 2.14e22 0.152e22 0.03e22-0.05e22
    '''.split()
    gravity_ms2 = '''
        3.70 8.87 9.8 3.71 24.79 10.44 8.87 11.15
        0.27 0.62 0.63 0.40 0.82
        0.27 0.18 0.24 0.285 ?
        1.622 1.796 1.314 1.428 1.235 0.0636 0.111 0.145 0.231 0.264
        1.35 0.22 0.08 0.27 0.23 0.39 0.35 0.78 0.28 0.16-0.27
    '''.split()
    escape_kmps = '''
        4.25 10.36 11.18 5.02 59.54 35.49 21.29 23.71
        0.51 1.21 0.91 0.54 1.37
        0.50 0.39 0.45 0.604 ?
        2.38 2.56 2.025 2.741 2.440 0.159 0.239 0.393 0.510 0.635
        2.64 0.57 0.19 0.56 0.52 0.77 0.73 1.46 0.58 0.34-0.44
    '''.split()
    rotate_days = '''
        58.646225 243.0187 0.99726968 1.02595675 0.41354 0.44401 0.71833 0.67125
        0.3781 6.3872 0.1631 0.9511 15.7859
        ? ? 0.3683 0.9333 0.4280
        27.321582 1.7691378 3.551181 7.154553 16.68902 0.942422 1.370218 1.887802 2.736915 4.518212
        15.945 79.322 1.414 2.52 4.144 8.706 13.46 5.877 6.387 15.786
    '''.split()
    orbit_days = '''
        87.969 224.701 365.256363 686.971 4332.59 10759.22 30688.5 60182
        4.599*365.25 247.9*365.25 283.8*365.25 306.2*365.25 559*365.25
        247.49*365.25 273.98*365.25 287.97*365.25 552.52*365.25 12059*365.25
        27.32158 1.769138 3.551181 7.154553 16.68902 0.942422 1.370218 1.887802 2.736915 4.518212
        15.945 79.322 1.4135 2.520 4.144 8.706 13.46 5.877 6.387 15.786
    '''.split()
    orbit_speed_kmps = '''
        47.8725 35.0214 29.7859 24.1309 13.0697 9.6724 6.8352 5.4778
        17.882 4.75 4.48 4.40 3.44
        4.68 4.57 4.52 3.63 1.04
        1.022 17.34 13.740 10.880 8.204 14.32 12.63 11.35 10.03 8.48
        5.57 3.265 6.657 5.50898 4.66797 3.644 3.152 4.39 0.2 0.172
    '''.split()
    eccentricity = '''
        0.20563069 0.00677323 0.01671022 0.09341233 0.04839266 0.05415060 0.04716771 0.00858587
        0.080 0.249 0.195 0.161 0.436
        0.226 0.106 0.038 0.506 0.855
        0.0549 0.0041 0.009 0.0013 0.0074 0.0202 0.0047 0.02 0.002 0.001
        0.0288 0.0286 0.0013 0.0012 0.005 0.0011 0.0014 0.00002 0.0022 0.0062
    '''.split()
    incl_deg = '''
        7.00 3.39 0 1.85 1.31 2.48 0.76 1.77
        10.59 17.14 28.21 28.98 44.04
        20.59 23.92 7.99 30.74 11.93
        18.29-28.58 0.04 0.47 1.85 0.2 1.51 0.02 1.51 0.019 0.345
        0.33 14.72 4.22 0.31 0.36 0.14 0.10 157 0.001 ≈0
    '''.split()
    axial_tilt_deg = '''
        0.0 177.3 23.44 25.19 3.12 26.73 97.86 28.32
        4 119.6 ≈126 ? ≈78
        None None None None None
        6.68 0.000405±0.00076 0.0965±0.0069 0.155±0.065 0-2 ≈0 ≈0 ≈0 ≈0 ≈0
        ≈0.3 ≈0 ≈0 ≈0 ≈0 ≈0 ≈0 ≈0.7 ≈0 ≈0
    '''.split()
    number_moons = '''
        0 0 1 2 92 83 27 14
        0 5 2 1 1
        1 1 1 1 0
        0 0 0 0 0 0 0 0 0 0  
        0 0 0 0 0 0 0 0 0 0  
    '''.split()
    surface_temp_K = '''
        440-100 730 287 227 152 134 76 73
        167 40 <50 30 30
        ≈42 ≈43 ≈41 ≈30 ≈12
        220 130 102 110 134 64 75 64 87 76
        93.7 130 59 58 61 60 61 38 53 34
    '''.split()
if 1:   # Get data
    def ToFlt(lst, mult=1):
        f = F.FltDerived
        return [f(i)*mult for i in lst]
    def BuildDataDict():
        '''Construct a dict that has lists of the data.  We use the keys
            name    Object's name
            name_lc Object's name (all lower case)
            sym     Symbol
            d       Distance from primary, m
            r       Mean radius, m
            m       Mass, kg
            g       Equatorial gravitational acceleration, m/s2
            ev      Escape velocity, m/s
            rot     Rotation period, s
            orb     Orbital period, s
            vel     Orbital speed, m/s
            ecc     Eccentricity
            inc     Inclination, degrees
            tilt    Axial tilt, degrees
            moons   Number of moons
            T       Mean surface temperature, K
        All objects not strings are flts or objects derived from flt.
        moons is an integer.
        '''
        # Check for consistency in list lengths
        n = len(names)
        for i in (symbols, dist_km, radius_km, mass_kg, gravity_ms2,
                  escape_kmps, rotate_days, orbit_days, orbit_speed_kmps,
                  eccentricity, incl_deg, axial_tilt_deg, number_moons,
                  surface_temp_K):
            assert(len(i) == n)
        # Build dict
        di = {}
        di["name"] = names
        di["sym"] = symbols
        di["d"] = ToFlt(dist_km, 1000)
        di["r"] = ToFlt(radius_km, 1000)
        di["m"] = ToFlt(mass_kg)
        di["g"] = ToFlt(gravity_ms2)
        di["ev"] = ToFlt(escape_kmps, 1000)
        di["rot"] = ToFlt(rotate_days, 86400)
        di["orb"] = ToFlt(orbit_days, 86400)
        di["vel"] = ToFlt(orbit_speed_kmps, 1000)
        di["ecc"] = ToFlt(eccentricity)
        di["inc"] = ToFlt(incl_deg)
        di["tilt"] = ToFlt(axial_tilt_deg)
        di["moons"] = number_moons
        di["T"] = ToFlt(surface_temp_K)
        # Now convert things to the desired units
        di["moons"] = [int(i) for i in di["moons"]]     # To integer
        if 0:
            # Dump to 1 figure to check things
            x = flt(0)
            x.N,x.high, x.low = 1, 1000, 0.01
            for i in di:
                s = [str(j) for j in di[i]]
                print(f"{i:5s}: {' '.join(s)}")
        # Check a few values for consistency
        i = 2   # Values for Earth
        assert(di["name"][i] == "Earth")
        assert(di["sym"][i] == "None")
        assert(di["d"][i] == 149597890*1000)
        assert(di["r"][i] == 6378.1366*1000)
        assert(di["m"][i] == 5.972e24)
        assert(di["g"][i] == 9.8)
        assert(di["ev"][i] == 11.18*1000)
        assert(di["rot"][i] == 0.99726968*86400)
        assert(di["orb"][i] == 365.256363*86400)
        assert(di["vel"][i] == 29.7859*1000)
        assert(di["ecc"][i] == 0.01671022)
        assert(di["inc"][i] == 0)
        assert(di["tilt"][i] == 23.44)
        assert(di["moons"][i] == 1)
        assert(di["T"][i] == 287)
        i = -1   # Values for Dysnomia
        assert(di["name"][i] == "Dysnomia")
        assert(di["sym"][i] == "None")
        assert(di["d"][i] == 37300*1000)
        assert(di["r"][i] == 350*1000)
        assert(di["m"][i] == 0.04e22)
        assert(di["g"][i] == 0.215)
        assert(di["ev"][i] == 0.39*1000)
        assert(di["rot"][i] == 15.786*86400)
        assert(di["orb"][i] == 15.786*86400)
        assert(di["vel"][i] == 0.172*1000)
        assert(di["ecc"][i] == 0.0062)
        assert(di["inc"][i] == 0)
        assert(di["tilt"][i] == 0)
        assert(di["moons"][i] == 0)
        assert(di["T"][i] == 34)
        # Make lower case names
        di["name_lc"] = [i.lower() for i in di["name"]]
        return di
    solarsys = BuildDataDict()
if 1:   # Utility
    def Manpage():
        print(dedent(f'''
        This script prints out wikipedia's information on the major solar
        system bodies as of {scrape_date}.

        Here's example output for Titan (the table mapping index numbers to
        body is omitted):

        Titan (index = 28) S6
            d         1.2e9 m = 1.2 Gm          Distance from primary
            r         2.6e6 m = 2.6 Mm          Mean radius
            m         1.3e23 kg = 130 Yg        Mass
            g         1.4 m/s² = 1.4 m/s²       Equatorial gravitational acceleration
            ev        2.6 m/s = 2.6 m/s         Escape velocity
            rot       1.4e6 s = 1.4 Ms          Rotation period
            orb       1.4e6 s = 1.4 Ms          Orbital period
            vel       5.6e3 m/s = 5.6 km/s      Orbital speed
            ecc       0.029                     Eccentricity
            inc       0.33° = 330m°             Inclination
            tilt      ≈0.30° = 300m°            Axial tilt
            moons     0                         Number of moons
            T         94 K = 94 K               Mean surface temperature

        Because SI prefixes can be useful in interpreting results, the
        values are followed by the significant with an appended SI prefix
        to the units.

        d is the distance to the primary.  Thus, for a planet like Mars,
        this means the distance to the sun.  For a moon like Ganymede, it
        means the distance to Jupiter.

        The index number lets you use either that number or "Titan" as the
        command line argument to get the report.  The command line
        arguments will also be interpreted as case-insensitive regular
        expressions, so e.g. "^t" will show you the bodies with names that
        start with the letter t.

        The variables are explained in the usage statement.

        When you use the -r option, you specify a reference body.  Then the
        report's parameters are printed to the reference body's values.
        Example:  'solarsys.py -r earth venus' shows Venus' values in terms of
        Earth's.  You should see Venus' mass is 0.82 of Earth's and its
        surface temperature is 2.5 times that of Earth's.

        If you use Earth as the -r argument, you won't get quite the same
        numbers as seen in the wikipedia table because the Earth's mean
        distance from the sun is 1.00000011 AU, not unity as you'd expect.
        If you use this correction, you should get the table values to
        within about 7 or 8 digits.

        The default number of digits printed is 2.  You can change this in
        the ParseCommandLine() function if you wish, but I find 2 digits
        nice for getting a feel for the size of things.

        '''))
        exit(0)
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [s1 [s2...]]
          Print data for solar system objects s1, s2, etc.  You can specify
          either the index number (e.g., Earth is 2) or a regular
          expression for the names (e.g. '^ti' will show Titan's and
          Titania's data).
 
          The parameters printed are:
            sym     Symbol (e.g. 'S6' means 6th moon of Saturn)
            d       Distance from primary, m
            r       Mean radius, m
            m       Mass, kg
            g       Equatorial gravitational acceleration, m/s²
            ev      Escape velocity, m/s
            rot     Rotation period, s
            orb     Orbital period, s
            vel     Orbital speed, m/s
            ecc     Eccentricity
            inc     Inclination, degrees
            tilt    Axial tilt, degrees
            moons   Number of moons
            T       Mean surface temperature, K
          Note units are base SI units except for angles, which are in
          degrees.
        Options:
          -d n    Number of significant digits [{d['-d']}]
          -h      Print a manpage
          -l      List the objects and their numbers at end of report
          -r n    Print relative to named object n's values
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 2         # Number of significant digits
        d["-l"] = False     # Show object names
        d["-r"] = None      # Object to use as reference
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hlr:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("l"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-r":
                d["-r"] = a
            elif o == "-h":
                Manpage()
        x = F.flt(0)
        x.N = d["-d"]
        x.rtz = False
        x.low, x.high = 0.01, 1000
        if not args:
            Usage()
        return args
if 1:   # Core functionality
    def GetObjDict():
        'Return dict indexed by integer number'
        di = {}
        for i, name in enumerate(solarsys["name"]):
            di[i] = name
        return di
    num2name = GetObjDict()
    def ListObjects():
        a, di = [], GetObjDict()
        for i in di:
            s = f"{i:2d} {di[i]}"
            a.append(s)
        for i in Columnize(a):
            print(i)
        exit(0)
    def PrintItem(num):
        'Print indicated item.  num must be an integer.'
        assert(ii(num, int))
        di, u = GetObjDict(), " "*4
        if num not in di:
            print(f"Item {num!r} not found")
            return
        # Print this object's data
        ss = solarsys
        sym = ss["sym"][num]
        print(f"{t.name}{ss['name'][num]} (index = {num}) {'' if sym == 'None' else sym}{t.n}")
        w = 10
        # Put data in local variables
        D = ss['d'][num]
        r = ss['r'][num]
        m = ss['m'][num]
        g = ss['g'][num]
        ev = ss['ev'][num]
        rot = ss['rot'][num]
        orb = ss['orb'][num]
        vel = ss['vel'][num]
        ecc = ss['ecc'][num]
        inc = ss['inc'][num]
        tilt = ss['tilt'][num]
        moons = ss['moons'][num]
        T = ss['T'][num]
        if d["-r"]:
            # Get reference data
            n = MatchName(d["-r"])
            if len(n) == 1:
                num0 = n[0]
            else:
                Error(f"-r option has too many numbers: {n}")
            D0 = ss['d'][num0]
            r0 = ss['r'][num0]
            m0 = ss['m'][num0]
            g0 = ss['g'][num0]
            ev0 = ss['ev'][num0]
            rot0 = ss['rot'][num0]
            orb0 = ss['orb'][num0]
            vel0 = ss['vel'][num0]
            ecc0 = ss['ecc'][num0]
            inc0 = ss['inc'][num0]
            tilt0 = ss['tilt'][num0]
            moons0 = ss['moons'][num0]
            T0 = ss['T'][num0]
            # Calculate ratios
            def GetRatio(value, ref, units):
                '''Calculate value/ref as flt and return it as a formatted
                string, but if ref is 0, then return value with units.
                '''
                try:
                    ratio = F.flt(value/ref)
                    if str(ratio) == "nan":
                        return f"{t.nan}{'?'}{t.n}"
                    else:
                        return f"{t.rel}{ratio}{t.n}"
                except ZeroDivisionError:
                    return f"{t.notrel}{F.flt(value)}{units}{t.n}"
            r_D = GetRatio(D, D0, " m")
            r_r = GetRatio(r, r0, " m")
            r_m = GetRatio(m, m0, " kg")
            r_g = GetRatio(g, g0, " m/s²")
            r_ev = GetRatio(ev, ev0, " m/s")
            r_rot = GetRatio(rot, rot0, " s")
            r_orb = GetRatio(orb, orb0, " s")
            r_vel = GetRatio(vel, vel0, " s")
            r_ecc = GetRatio(ecc, ecc0, "")
            r_inc = GetRatio(inc, inc0, "°")
            r_tilt = GetRatio(tilt, tilt0, "°")
            r_moons = GetRatio(moons, moons0, "°")
            r_T = GetRatio(T, T0, "")
            print(f"{u}{'d':{w}s}{r_D}")
            print(f"{u}{'r':{w}s}{r_r}")
            print(f"{u}{'m':{w}s}{r_m}")
            print(f"{u}{'g':{w}s}{r_g}")
            print(f"{u}{'ev':{w}s}{r_ev}")
            print(f"{u}{'rot':{w}s}{r_rot}")
            print(f"{u}{'orb':{w}s}{r_orb}")
            print(f"{u}{'vel':{w}s}{r_vel}")
            print(f"{u}{'ecc':{w}s}{r_ecc}")
            print(f"{u}{'inc':{w}s}{r_inc}")
            print(f"{u}{'tilt':{w}s}{r_tilt}")
            print(f"{u}{'moons':{w}s}{r_moons}")
            print(f"{u}{'T':{w}s}{r_T}")
        else:
            def SI(val, unit, cuddle=False):
                s = f"{val.engsi}"
                if "e" in s: # No SI prefix
                    return f"{s}{' '*(not cuddle)}{unit}"
                else:
                    return f"{s}{unit}"
            print(f"{u}{'d':{w}s}{D} m = {SI(D, 'm')}")
            print(f"{u}{'r':{w}s}{r} m = {SI(r, 'm')}")
            print(f"{u}{'m':{w}s}{m} kg = {SI(1000*m, 'g')}")
            print(f"{u}{'g':{w}s}{g} m/s² = {SI(g, 'm/s²')}")
            print(f"{u}{'ev':{w}s}{ev} m/s = {SI(ev, 'm/s')}")
            print(f"{u}{'rot':{w}s}{rot} s = {SI(rot, 's')}")
            print(f"{u}{'orb':{w}s}{orb} s = {SI(orb, 's')}")
            print(f"{u}{'vel':{w}s}{vel} m/s = {SI(vel, 'm/s')}")
            print(f"{u}{'ecc':{w}s}{ecc}")
            print(f"{u}{'inc':{w}s}{inc}°")
            print(f"{u}{'tilt':{w}s}{tilt}°")
            print(f"{u}{'moons':{w}s}{moons}")
            print(f"{u}{'T':{w}s}{T} K = {SI(T, 'K')}")
    def MatchName(regex):
        'Return a list of matched names by index number'
        ss = solarsys["name"]
        # See if it's an integer
        try:
            num = int(regex)
            if 0 <= num < len(ss):
                return [num]
            else:
                print(f"{num!r} is an out-of-range number")
                return None
        except ValueError:
            pass
        o = []
        r = re.compile(rf"{regex}", re.I)
        for i, name in enumerate(ss):
            if r.search(name):
                o.append(i)
        return list(sorted(set(o)))
    def PrintItems(*names):
        o = []
        for name in names:
            o.extend(MatchName(name))
        for i in list(sorted(set(o))):
            PrintItem(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    objects = ParseCommandLine(d)
    if d["-r"] is not None:
        nums = MatchName(d["-r"])
        if len(nums) == 1:
            name = solarsys["name"][nums[0]]
            print(f"Numbers are relative to {name}'s values")
            t.print(f"  Colors:  {t.rel}ratio{t.n}  {t.notrel}regular value  {t.nan}unknown")
        else:
            Error(f"-r argument not specific enough:  {nums}")
    for name in objects:
        num = MatchName(name)
        if num is None:
            continue
        elif ii(num, list):
            for i in num:
                PrintItem(i)
        else:
            PrintItem(num)
    if d["-l"]:
        print()
        ListObjects()
