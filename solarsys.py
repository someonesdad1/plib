'''
Module that contains basic data on solar system objects

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
    - Inclination, °
    - Axial titl, °
    - Mean surface temperature, K
    - Atmospheric composition
    - Number of moons

Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune
mean distance from sun km: 57909175 108208930 149597890 227936640 778412010 1426725400 2870972200 4498252900
equatorial radius km: 2440.53 6051.8 6378.1366 3396.19 71492 60268 25559 24764
mass kg:  3.302e23 4.8690e24 5.972e24 6.4191e23 1.8987e27 5.6851e26 8.6849e25 1.0244e26
equatorial gravity m/s2:  3.70 8.87 9.8 3.71 24.79 10.44 8.87 11.15
escape velocity km/s: 4.25 10.36 11.18 5.02 59.54 35.49 21.29 23.71
rotation period days: 58.646225 243.0187 0.99726968 1.02595675 0.41354 0.44401 0.71833 0.67125
orbital period days: 87.969 224.701 365.256363 686.971 4332.59 10759.22 30688.5 60182
mean orbital speed km/s: 47.8725 35.0214 29.7859 24.1309 13.0697 9.6724 6.8352 5.4778
eccentricity: 0.20563069 0.00677323 0.01671022 0.09341233 0.04839266 0.05415060 0.04716771 0.00858587
inclination °: 7.00 3.39 0 1.85 1.31 2.48 0.76 1.77
axial tilt °: 0.0 177.3 23.44 25.19 3.12 26.73 97.86 28.32
number of moons:  0 0 1 2 92 83 27 14

When run as a script, produces tables and plots.

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
