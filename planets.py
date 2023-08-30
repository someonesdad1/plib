'''
Library for solar system planetary data.

Eccentricities

Glenda commented about the moon last night being closer.  She had been
reading some "marketing" information somewhere; no doubt some news writer
had to exaggerate things to get readership.  I explained that most of the
planets and their moons have low eccentricity orbits, meaning their
geometrical sizes won't change all that much.  At least for the inner
planets, the sizes will be most affected by the relative positions in the
orbits.

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
        from wrap import dedent
        from color import t
        from f import flt, radians
        from u import u
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        AU_to_m = 1.495978707e9     # Astronomical unit to m
        yr_to_s = 31556925.9746784  # Year to seconds

if 1:   # Classes
    # Planetary data from 
    # https://en.wikipedia.org/wiki/List_of_gravitationally_rounded_objects_of_the_Solar_System#Planets
    class Planet:
        def __init__(self):
            # Physical units are in base SI units
            # Angles are in radians
            self.semimajor = None       # Semimajor axis of orbit
            self.eccentricity = None    # Eccentricity of orbit
            self.inclination = None     # Inclination of orbit to ecliptic, radians
            self.eq_radius = None       # Equatorial radius
            self.orbital_period = None  # Time to orbit the sun
    class Mercury:
        def __init__(self):
            self.semimajor = 0.38709893*AU_to_m
            self.eccentricity = 0.20563069
            self.inclination = radians(7)
            self.eq_radius = 2440.53e3
            self.orbital_period = 0.2408467*yr_to_s
    class Venus:
        def __init__(self):
            self.semimajor = 0.72333199*AU_to_m
            self.eccentricity = 0.00677323
            self.inclination = radians(3.39)
            self.eq_radius = 6051.8e3
            self.orbital_period = 0.61519726*yr_to_s
    class Mars:
        def __init__(self):
            self.semimajor = 1.52366231*AU_to_m
            self.eccentricity = 0.09341233
            self.inclination = radians(1.85)
            self.eq_radius = 3396.19e3
            self.orbital_period = 1.8808476*yr_to_s
    class Jupiter:
        def __init__(self):
            self.semimajor = 778412010*AU_to_m
            self.eccentricity = 0.04839266
            self.inclination = radians(1.31)
            self.eq_radius = 71492e3
            self.orbital_period = 11.862615*yr_to_s
    class Saturn:
        def __init__(self):
            self.semimajor = 1426725400*AU_to_m
            self.eccentricity = 0.05415060
            self.inclination = radians(2.48)
            self.eq_radius = 60268e3
            self.orbital_period = 29.447498*yr_to_s
    class Uranus:
        def __init__(self):
            self.semimajor = 2870972200*AU_to_m
            self.eccentricity = 0.04716771
            self.inclination = radians(0.76)
            self.eq_radius = 25559e3
            self.orbital_period = 84.016846*yr_to_s
    class Neptune:
        def __init__(self):
            self.semimajor = 4498252900*AU_to_m
            self.eccentricity = 0.00858587
            self.inclination = radians(1.77)
            self.eq_radius = 24764e3
            self.orbital_period = 164.79132*yr_to_s

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
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
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
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
