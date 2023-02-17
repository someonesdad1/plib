'''
Module that contains basic data on solar system objects
    When run as a script, produces tables and plots.

Core information from https://en.wikipedia.org/wiki/List_of_gravitationally_rounded_objects_of_the_Solar_System
    - Mean distance from primary, km
    - Mean radius, km
    - Mass, kg
    - Equatorial gravity, m/s2
    - Escape velocity, km/s
    - Rotation period, days
    - Orbital period, years
    - Mean orbital speed, km/s
    - Eccentricity
    - Inclination, deg
    - Axial titl, deg
    - Mean surface temperature, K
    - Atmospheric composition
    - Number of moons

'''
# PLANETS
p = '''
Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune
Symbol: None None None None None None None None
Mean distance from primary km: 57909175 108208930 149597890 227936640 778412010 1426725400 2870972200 4498252900
Mean radius km: 2440.53 6051.8 6378.1366 3396.19 71492 60268 25559 24764
Mass kg:  3.302e23 4.8690e24 5.972e24 6.4191e23 1.8987e27 5.6851e26 8.6849e25 1.0244e26
Equatorial gravity m/s2:  3.70 8.87 9.8 3.71 24.79 10.44 8.87 11.15
Escape velocity km/s: 4.25 10.36 11.18 5.02 59.54 35.49 21.29 23.71
Rotation period days: 58.646225 243.0187 0.99726968 1.02595675 0.41354 0.44401 0.71833 0.67125
Orbital period days: 87.969 224.701 365.256363 686.971 4332.59 10759.22 30688.5 60182
Mean orbital speed km/s: 47.8725 35.0214 29.7859 24.1309 13.0697 9.6724 6.8352 5.4778
Eccentricity: 0.20563069 0.00677323 0.01671022 0.09341233 0.04839266 0.05415060 0.04716771 0.00858587
Inclination deg: 7.00 3.39 0 1.85 1.31 2.48 0.76 1.77
Axial tilt deg: 0.0 177.3 23.44 25.19 3.12 26.73 97.86 28.32
Number of moons:  0 0 1 2 92 83 27 14
Mean surface temperature K: 440-100 730 287 227 152 134 76 73
'''

# DWARF PLANETS
dp1 = '''
Ceres Pluto Haumea Makemake Eris
Symbol: None None None None None
Mean distance from primary km: 413700000 5906380000 6484000000 6850000000 10210000000
Mean radius km: 473 1188.3 816 715 1163
Mass kg:  9.39e20 1.30e22 4.0e21 3.1e21 1.65e22
Equatorial gravity m/s2: 0.27 0.62 0.63 0.40 0.82
Escape velocity km/s: 0.51 1.21 0.91 0.54 1.37
Rotation period days: 0.3781 6.3872 0.1631 0.9511 15.7859
Orbital period days: 4.599*365.25 247.9*365.25 283.8*365.25 306.2*365.25 559*365.25
Mean orbital speed km/s: 17.882 4.75 4.48 4.40 3.44
Eccentricity: 0.080 0.249 0.195 0.161 0.436
Inclination deg: 10.59 17.14 28.21 28.98 44.04
Axial tilt deg: 4 119.6 ≈126 ? ≈78
Number of moons:  0 5 2 1 1
Mean surface temperature K: 167 40 <50 30 30
'''

dp2 = '''
Orcus Salacia Quaoar Gonggong Sedna
Symbol: None None None None None
Mean distance from primary km: 5896946000 6310600000 6535930000 10072433340 78668000000
Mean radius km: 458.5 423 560.5 615 497.5
Mass kg: 6.32e20 4.9e20 1.41e21 1.75×21 ?
Equatorial gravity m/s2: 0.27 0.18 0.24 0.285 ?
Escape velocity km/s:  0.50 0.39 0.45 0.604 ?
Rotation period days: ? ? 0.3683 0.9333 0.4280
Orbital period days: 247.49*365.25 273.98*365.25 287.97*365.25 552.52*365.25 12059*365.25
Mean orbital speed km/s: 4.68 4.57 4.52 3.63 1.04
Eccentricity: 0.226 0.106 0.038 0.506 0.855
Inclination deg: 20.59 23.92 7.99 30.74 11.93
Axial tilt deg: None None None None None
Number of moons: 1 1 1 1 0
Mean surface temperature K: ≈42 ≈43 ≈41 ≈30 ≈12
'''
# MOONS
m1 = '''
Moon Io Europa Ganymede Callisto Mimas Enceladus Tethys Dione Rhea
Symbol: E1 J1 J2 J3 J4 S1 S2 S3 S4 S5
Mean distance from primary km: 384399 421600 670900 1070400 1882700 185520 237948 294619 377396 527108
Mean radius km: 1737.1 1815 1569 2634.1 2410.3 198.30 252.1 533 561.7 764.3
Mass kg: 7.3477e22 8.94e22 4.80e22 14.819e22 10.758e22 0.00375e22 0.0108e22 0.06174e22 0.1095e22 0.2306e22
Equatorial gravity m/s2: 1.622 1.796 1.314 1.428 1.235 0.0636 0.111 0.145 0.231 0.264
Escape velocity km/s: 2.38 2.56 2.025 2.741 2.440 0.159 0.239 0.393 0.510 0.635
Rotation period days: 27.321582 1.7691378 3.551181 7.154553 16.68902 0.942422 1.370218 1.887802 2.736915 4.518212
Orbital period days: 27.32158 1.769138 3.551181 7.154553 16.68902 0.942422 1.370218 1.887802 2.736915 4.518212
Mean orbital speed km/s: 1.022 17.34 13.740 10.880 8.204 14.32 12.63 11.35 10.03 8.48
Eccentricity: 0.0549 0.0041 0.009 0.0013 0.0074 0.0202 0.0047 0.02 0.002 0.001
Inclination deg: 18.29-28.58 0.04 0.47 1.85 0.2 1.51 0.02 1.51 0.019 0.345
Axial tilt deg: 6.68 0.000405±0.00076 0.0965±0.0069 0.155±0.065 ≈0-2 ≈0 ≈0 ≈0 ≈0 ≈0
Mean surface temperature K: 220 130 102 110 134 64 75 64 87 76
'''

m2 = '''
Titan Iapetus Miranda Ariel Umbriel Titania Oberon Triton Charon Dysnomia
Symbol: S6 S8 U5 U1 U2 U3 U4 N1 P1 -
Mean distance from primary km: 1221870 3560820 129390 190900 266000 436300 583519 354759 17536 37300
Mean radius km: 2576 735.60 235.8 578.9 584.7 788.9 761.4 1353.4 603.5 350
Mass kg: 13.452e22 0.18053e22 0.00659e22 0.135e22 0.12e22 0.35e22 0.3014e22 2.14e22 0.152e22 0.03e22-0.05e22
Equatorial gravity m/s2: 1.35 0.22 0.08 0.27 0.23 0.39 0.35 0.78 0.28 0.16-0.27
Escape velocity km/s: 2.64 0.57 0.19 0.56 0.52 0.77 0.73 1.46 0.58 0.34-0.44
Rotation period days: 15.945 79.322 1.414 2.52 4.144 8.706 13.46 5.877 6.387 15.786
Orbital period days: 15.945 79.322 1.4135 2.520 4.144 8.706 13.46 5.877 6.387 15.786
Mean orbital speed km/s: 5.57 3.265 6.657 5.50898 4.66797 3.644 3.152 4.39 0.2 0.172
Eccentricity: 0.0288 0.0286 0.0013 0.0012 0.005 0.0011 0.0014 0.00002 0.0022 0.0062
Inclination deg: 0.33 14.72 4.22 0.31 0.36 0.14 0.10 157[h] 0.001 ≈0
Axial tilt deg: ≈0.3 ≈0 ≈0 ≈0 ≈0 ≈0 ≈0 ≈0.7[92] ≈0 ≈0
Mean surface temperature K: 93.7 130 59 58 61 60 61 38 53 34
'''
# Check that each item has equal number of fields
def Check():
    def CheckFields(s, name):
        l = []
        for i in s.strip().split("\n"):
            if ":" in i:
                loc = i.find(":")
                f = i[loc + 1:].split()
            else:
                f = i.split()
            l.append(len(f))
        if 0:
            from pprint import pprint as pp
            print(name)
            pp(l)
        return l
    assert(set(CheckFields(p, "p")) == {8})
    assert(set(CheckFields(dp1, "dp1")) == {5})
    assert(set(CheckFields(dp2, "dp2")) == {5})
    assert(set(CheckFields(m1, "m1")) == {10})
    assert(set(CheckFields(m2, "m2")) == {10})
    exit()
Check()

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
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
