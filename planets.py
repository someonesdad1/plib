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
        from f import flt, radians, degrees
        from u import u
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        AU_to_m = 1.495978707e9     # Astronomical unit to m
        yr_to_s = 31556925.9746784  # Year to seconds
        t.r = t("sky")
if 1:   # Classes
    # Planetary data from 
    # https://en.wikipedia.org/wiki/List_of_gravitationally_rounded_objects_of_the_Solar_System#Planets
    class Planet:
        def __init__(self):
            # Physical units are in base SI units
            # Angles are in radians
            self.name = None            # Name of planet
            self.semimajor = None       # Semimajor axis of orbit
            self.eccentricity = None    # Eccentricity of orbit
            self.inclination = None     # Inclination of orbit to ecliptic, radians
            self.eq_radius = None       # Equatorial radius
            self.orbital_period = None  # Time to orbit the sun
        def __str__(self):
            scale = 1
            if d["-p"] is not None:
                p = planets[trans[d["-p"]]]
                return dedent(f'''
                {self.name} ({t.r}relative to {p.name}{t.n})
                    Orbit semimajor axis        {t.r}{self.semimajor/p.semimajor}{t.n}
                    Orbit eccentricity          {self.eccentricity}
                    Inclination to ecliptic     {degrees(self.inclination)}°
                    Equatorial radius           {t.r}{self.eq_radius/p.eq_radius}{t.n}
                    Orbital period              {t.r}{self.orbital_period/p.orbital_period}{t.n}
                    Mass                        {t.r}{self.mass/p.mass}{t.n}
                ''')
            else:
                return dedent(f'''
                {self.name}
                    Orbit semimajor axis        {self.semimajor.engsi}m
                    Orbit eccentricity          {self.eccentricity}
                    Inclination to ecliptic     {degrees(self.inclination)}° 
                    Equatorial radius           {self.eq_radius.engsi}m
                    Orbital period              {self.orbital_period.engsi}s = {(self.orbital_period/yr_to_s).engsi}yr
                    Mass                        {(self.mass*1e3).sci} g
                ''')
        def __repr__(self):
            return str(self)
    class Mercury(Planet):
        def __init__(self):
            self.name = "Mercury"
            self.semimajor = flt(0.38709893*AU_to_m)
            self.eccentricity = flt(0.20563069)
            self.inclination = flt(radians(7))
            self.eq_radius = flt(2440.53e3)
            self.orbital_period = flt(0.2408467*yr_to_s)
            self.mass = flt(3.302e23)
    class Venus(Planet):
        def __init__(self):
            self.name = "Venus"
            self.semimajor = flt(0.72333199*AU_to_m)
            self.eccentricity = flt(0.00677323)
            self.inclination = flt(radians(3.39))
            self.eq_radius = flt(6051.8e3)
            self.orbital_period = flt(0.61519726*yr_to_s)
            self.mass = flt(4.869e24)
    class Earth(Planet):
        def __init__(self):
            self.name = "Earth"
            self.semimajor = flt(149597890*AU_to_m)
            self.eccentricity = flt(0.01671022)
            self.inclination = flt(radians(0))
            self.eq_radius = flt(6378.1366e3)
            self.orbital_period = flt(1.0000174*yr_to_s)
            self.mass = flt(5.972e24)
    class Mars(Planet):
        def __init__(self):
            self.name = "Mars"
            self.semimajor = flt(227936640*AU_to_m)
            self.eccentricity = flt(0.09341233)
            self.inclination = flt(radians(1.85))
            self.eq_radius = flt(3396.19e3)
            self.orbital_period = flt(1.8808476*yr_to_s)
            self.mass = flt(6.419e23)
    class Jupiter(Planet):
        def __init__(self):
            self.name = "Jupiter"
            self.semimajor = flt(778412010*AU_to_m)
            self.eccentricity = flt(0.04839266)
            self.inclination = flt(radians(1.31))
            self.eq_radius = flt(71492e3)
            self.orbital_period = flt(11.862615*yr_to_s)
            self.mass = flt(1.8987e27)
    class Saturn(Planet):
        def __init__(self):
            self.name = "Saturn"
            self.semimajor = flt(1426725400*AU_to_m)
            self.eccentricity = flt(0.05415060)
            self.inclination = flt(radians(2.48))
            self.eq_radius = flt(60268e3)
            self.orbital_period = flt(29.447498*yr_to_s)
            self.mass = flt(5.6851e26)
    class Uranus(Planet):
        def __init__(self):
            self.name = "Uranus"
            self.semimajor = flt(2870972200*AU_to_m)
            self.eccentricity = flt(0.04716771)
            self.inclination = flt(radians(0.76))
            self.eq_radius = flt(25559e3)
            self.orbital_period = flt(84.016846*yr_to_s)
            self.mass = flt(8.6849e25)
    class Neptune(Planet):
        def __init__(self):
            self.name = "Neptune"
            self.semimajor = flt(4498252900*AU_to_m)
            self.eccentricity = flt(0.00858587)
            self.inclination = flt(radians(1.77))
            self.eq_radius = flt(24764e3)
            self.orbital_period = flt(164.79132*yr_to_s)
            self.mass = flt(1.0244e26)
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] 
          Print out planetary data.
        Options:
            -r p    Print numbers relative to planet p (first letter, use h
                    for Mercury))
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 2         # Number of significant digits
        d["-p"] = None      # Relative to this planet
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hp:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
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
            elif o in ("-p",):
                if len(a) > 1 or a not in "hvemjsun":
                    Error("-p option's letter must be in 'hvemjsun'")
                d["-p"] = a
            elif o in ("-h", "--help"):
                Usage(status=0)
        x = flt(0)
        x.N = d["-d"]
        x.rtz = False
        return args
if 1:   # Core functionality
    planets = {
        "Mercury": Mercury(),
        "Venus": Venus(),
        "Earth": Earth(),
        "Mars": Mars(),
        "Jupiter": Jupiter(),
        "Saturn": Saturn(),
        "Uranus": Uranus(),
        "Neptune": Neptune(),
    }
    trans = {
        "h": "Mercury",
        "v": "Venus",
        "e": "Earth",
        "m": "Mars",
        "j": "Jupiter",
        "s": "Saturn",
        "u": "Uranus",
        "n": "Neptune",
    }

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        print(f"Data to {d['-d']} figures")
        for p in planets:
            print(str(planets[p]))
