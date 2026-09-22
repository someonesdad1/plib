'''
Library for solar system planetary data.  Class Planet instances have their
attributes given in base SI units.  Run as a script to print data to
stdout.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Library for solar system planetary data oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2023 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ sci oo>
        <oo test ∞ notest oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        import getopt
        import os
        import sys
    if 1:  # Custom imports
        import f
        import trm
        import wrap
        from f import flt
    if 1:  # Global variables
        t = trm.Trm()
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        AU_to_m = 1.495978707e11  # Astronomical unit to m
        yr_to_s = 31556925.9746784  # Year to seconds
        day_to_s = 86400  # Day to seconds
        t.r = t.ornl
        t.nr = t.trql
if 1:  # Classes
    # Planetary data from
    # https://en.wikipedia.org/wiki/List_of_gravitationally_rounded_objects_of_the_Solar_System#Planets
    class Planet:
        def __init__(self):
            # Physical units are in base SI units
            # Angles are in radians
            self.name = None  # Name of planet
            self.semimajor = None  # Semimajor axis of orbit
            self.eccentricity = None  # Eccentricity of orbit
            self.inclination = None  # Inclination of orbit to ecliptic, radians
            self.eq_radius = None  # Equatorial radius
            self.orbital_period = None  # Time to orbit the sun
            self.mass = None
            self.orbital_speed = None
            self.moons = None
            self.gravity = None  # Equatorial gravitational acceleration m/s²
            self.esc_vel = None  # Escape velocity km/s
            self.tilt = None  # Axial tilt
            self.rot_per = None  # Rotation period, days
        def calc(self):
            # Calculate other attributes
            self.circum = 2 * f.pi * self.eq_radius
            self.area = 4 * f.pi * self.eq_radius**2
            self.vol = 4 / 3 * f.pi * self.eq_radius**3
            self.spgr = self.mass * 1000 / (self.vol * 1e6)  # Convert to g/cc
        def __str__(self):
            if d["-r"] is not None:
                p = planets[trans[d["-r"]]]
                return wrap.dedent(f'''
                {self.name} 
                    Semimajor axis              {t.r}{self.semimajor / p.semimajor}{t.n}
                    Eccentricity                {t.nr}{self.eccentricity}{t.n}
                    Orbital speed (mean)        {t.r}{self.orbital_speed / p.orbital_speed}{t.n}
                    Orbital period              {t.r}{self.orbital_period / p.orbital_period}{t.n}
                    Inclination to ecliptic     {t.nr}{f.degrees(self.inclination)}°{t.n}
                    Equatorial radius           {t.r}{self.eq_radius / p.eq_radius}{t.n}
                    Circumference               {t.r}{self.circum / p.circum}{t.n}
                    Area                        {t.r}{self.area / p.area}{t.n}
                    Volume                      {t.r}{self.vol / p.vol}{t.n}
                    Mass                        {t.r}{self.mass / p.mass}{t.n}
                    Specific gravity            {t.r}{self.spgr / p.spgr}{t.n}
                    Moons                       {t.nr}{self.moons}{t.n}
                    Equatorial gravity          {t.r}{self.gravity / p.gravity}{t.n}
                    Escape velocity             {t.r}{self.esc_vel / p.esc_vel}{t.n}
                    Axial tilt                  {t.nr}{f.degrees(self.tilt)}°{t.n}
                    Rotation period             {t.r}{self.rot_per / p.rot_per}{t.n}
                ''')
            else:
                return wrap.dedent(f'''
                {self.name}
                    Semimajor axis              {self.semimajor.engsi}m = {self.semimajor.sci} m
                    Eccentricity                {self.eccentricity}
                    Orbital speed (mean)        {self.orbital_speed.engsi}m/s
                    Orbital period              {self.orbital_period.engsi}s = {(self.orbital_period / yr_to_s).engsi}yr
                    Inclination to ecliptic     {f.degrees(self.inclination)}° 
                    Equatorial radius           {self.eq_radius.engsi}m = {self.eq_radius.sci} m
                    Circumference               {self.circum.engsi}m = {self.circum.sci} m
                    Area                        {self.area.engsi}m² = {self.area.sci} m²
                    Volume                      {self.vol.engsi}m³ = {self.vol.sci} m³
                    Mass                        {self.mass.sci} kg 
                    Specific gravity            {self.spgr}
                    Moons                       {self.moons}
                    Equatorial gravity          {self.gravity} m/s²
                    Escape velocity             {self.esc_vel} km/s
                    Axial tilt                  {f.degrees(self.tilt)}°
                    Rotation period             {self.rot_per.engsi}s = {self.rot_per / day_to_s} days
                ''')
        def __repr__(self):
            return str(self)
    class Mercury(Planet):
        def __init__(self):
            self.name = "Mercury"
            self.semimajor = f.flt(0.38709893 * AU_to_m)
            self.eccentricity = f.flt(0.20563069)
            self.inclination = f.flt(f.radians(7))
            self.eq_radius = f.flt(2440.53e3)
            self.orbital_period = f.flt(0.2408467 * yr_to_s)
            self.mass = f.flt(3.302e23)
            self.orbital_speed = f.flt(47.8725 * 1e3)
            self.calc()
            self.moons = 0
            self.gravity = f.flt(3.7)
            self.esc_vel = f.flt(4.25)
            self.tilt = f.flt(f.radians(0))
            self.rot_per = f.flt(58.646225) * day_to_s
    class Venus(Planet):
        def __init__(self):
            self.name = "Venus"
            self.semimajor = f.flt(0.72333199 * AU_to_m)
            self.eccentricity = f.flt(0.00677323)
            self.inclination = f.flt(f.radians(3.39))
            self.eq_radius = f.flt(6051.8e3)
            self.orbital_period = f.flt(0.61519726 * yr_to_s)
            self.mass = f.flt(4.869e24)
            self.orbital_speed = f.flt(35.0214 * 1e3)
            self.calc()
            self.moons = 0
            self.gravity = f.flt(8.87)
            self.esc_vel = f.flt(10.36)
            self.tilt = f.flt(f.radians(177.3))
            self.rot_per = f.flt(243.0187) * day_to_s
    class Earth(Planet):
        def __init__(self):
            self.name = "Earth"
            self.semimajor = f.flt(149597890 * AU_to_m)
            self.eccentricity = f.flt(0.01671022)
            self.inclination = f.flt(f.radians(0))
            self.eq_radius = f.flt(6378.1366e3)
            self.orbital_period = f.flt(1.0000174 * yr_to_s)
            self.mass = f.flt(5.972e24)
            self.orbital_speed = f.flt(29.7859 * 1e3)
            self.calc()
            self.moons = 1
            self.gravity = f.flt(9.8)
            self.esc_vel = f.flt(11.18)
            self.tilt = f.flt(f.radians(23.44))
            self.rot_per = f.flt(0.99726968) * day_to_s
    class Mars(Planet):
        def __init__(self):
            self.name = "Mars"
            self.semimajor = f.flt(227936640 * AU_to_m)
            self.eccentricity = f.flt(0.09341233)
            self.inclination = f.flt(f.radians(1.85))
            self.eq_radius = f.flt(3396.19e3)
            self.orbital_period = f.flt(1.8808476 * yr_to_s)
            self.mass = f.flt(6.419e23)
            self.orbital_speed = f.flt(24.1309 * 1e3)
            self.calc()
            self.moons = 2
            self.gravity = f.flt(3.71)
            self.esc_vel = f.flt(5.02)
            self.tilt = f.flt(f.radians(25.19))
            self.rot_per = f.flt(1.02595675) * day_to_s
    class Jupiter(Planet):
        def __init__(self):
            self.name = "Jupiter"
            self.semimajor = f.flt(778412010 * AU_to_m)
            self.eccentricity = f.flt(0.04839266)
            self.inclination = f.flt(f.radians(1.31))
            self.eq_radius = f.flt(71492e3)
            self.orbital_period = f.flt(11.862615 * yr_to_s)
            self.mass = f.flt(1.8987e27)
            self.orbital_speed = f.flt(13.0697 * 1e3)
            self.calc()
            self.moons = 95
            self.gravity = f.flt(24.79)
            self.esc_vel = f.flt(59.54)
            self.tilt = f.flt(f.radians(3.12))
            self.rot_per = f.flt(0.41354) * day_to_s
    class Saturn(Planet):
        def __init__(self):
            self.name = "Saturn"
            self.semimajor = f.flt(1426725400 * AU_to_m)
            self.eccentricity = f.flt(0.05415060)
            self.inclination = f.flt(f.radians(2.48))
            self.eq_radius = f.flt(60268e3)
            self.orbital_period = f.flt(29.447498 * yr_to_s)
            self.mass = f.flt(5.6851e26)
            self.orbital_speed = f.flt(9.6724 * 1e3)
            self.calc()
            self.moons = 146
            self.gravity = f.flt(10.44)
            self.esc_vel = f.flt(35.49)
            self.tilt = f.flt(f.radians(26.73))
            self.rot_per = f.flt(0.44401) * day_to_s
    class Uranus(Planet):
        def __init__(self):
            self.name = "Uranus"
            self.semimajor = f.flt(2870972200 * AU_to_m)
            self.eccentricity = f.flt(0.04716771)
            self.inclination = f.flt(f.radians(0.76))
            self.eq_radius = f.flt(25559e3)
            self.orbital_period = f.flt(84.016846 * yr_to_s)
            self.mass = f.flt(8.6849e25)
            self.orbital_speed = f.flt(6.8352 * 1e3)
            self.calc()
            self.moons = 27
            self.gravity = f.flt(8.87)
            self.esc_vel = f.flt(21.29)
            self.tilt = f.flt(f.radians(97.86))
            self.rot_per = f.flt(0.71833) * day_to_s
    class Neptune(Planet):
        def __init__(self):
            self.name = "Neptune"
            self.semimajor = f.flt(4498252900 * AU_to_m)
            self.eccentricity = f.flt(0.00858587)
            self.inclination = f.flt(f.radians(1.77))
            self.eq_radius = f.flt(24764e3)
            self.orbital_period = f.flt(164.79132 * yr_to_s)
            self.mass = f.flt(1.0244e26)
            self.orbital_speed = f.flt(5.4778 * 1e3)
            self.calc()
            self.moons = 14
            self.gravity = f.flt(11.15)
            self.esc_vel = f.flt(23.71)
            self.tilt = f.flt(f.radians(28.32))
            self.rot_per = f.flt(0.67125) * day_to_s
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(wrap.dedent('''
        Data from https://en.wikipedia.org/wiki/List_of_gravitationally_rounded_objects_of_the_Solar_System#Planets
        
        Semimajor axis
            Though this is related to the orbital ellipse, it's essentially the mean
            distance of the planet from the sun, as the planets' orbits are not very
            eccentric except for Mercury.
        Eccentricity
            A dimensionless number on [0, 1) that measures how much a planet's
            elliptical orbit deviates from a circle.  A circle has an eccentricity of
            0.
        Orbital speed (mean)
            Average speed of the planet around the sun.
        Orbital period
            How long it takes to make a complete orbit around the sun.
        Inclination to ecliptic
            How much a planet's orbit is tilted to the ecliptic, the plane of the
            Earth's orbit around the sun.
        Equatorial radius
            Radius of the planet at its equator.
        Circumference
            2π times the equatorial radius.
        Area
            Surface area, calculated from the equatorial radius and assuming the
            planet is a sphere.
        Volume
            Calculated from the equatorial radius and assuming the planet is a
            sphere.
        Mass
            A measure of the quantity of matter in the planet.
        Specific gravity
            The average mass density of the planet divided by the density of water at
            0 °C and 1 atmosphere pressure.
        Moons
            Recognized "natural" satellites orbiting the planet.
        Equatorial gravity
            Acceleration of the planet's gravity at its equator.
        Escape velocity
            A minimum speed required for a non-propelled body to escape the
            gravitational field of the planet.
        Axial tilt
            Angle of tilt of the rotation axis of the planet relative to its orbital
            plane.
        Rotation period (sidereal)
            Time for one rotation about its rotation axis of the planet with respect
            to the fixed stars.
        ''')
        )
        exit(0)
    def Usage(status=1):
        print(wrap.dedent(f'''
        Usage:  {sys.argv[0]} [options] [planet_letters]
          Print out planetary data.  Planet letters are the first letter of
          the planet's name (use h for Mercury).  Use 'a' to show all
          planets.  Examples:
            '-e s' shows Saturn's data relative to Earth
            '-r s e' shows Earth's data relative to Saturn
        Options:
            -d n    Number of figures in output [{d["-d"]}]
            -e      Relative to Earth (short for '-r e')
            -h      Print a manpage
            -r p    Print numbers relative to planet p (first letter)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3  # Number of significant digits
        d["-e"] = False  # Relative to Earth
        d["-r"] = None  # Relative to this planet
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:ehr:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("e"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-r",):
                if len(a) > 1 or a not in "hvemjsun":
                    Error("-r option's letter must be in 'hvemjsun'")
                d["-r"] = a
            elif o == "-h":
                Manpage()
        x = f.flt(0)
        x.N = d["-d"]
        x.rtz = False
        x.u = True
        x.high = 1e5
        if d["-e"]:
            d["-r"] = "e"
        if not args:
            Usage()
        return args
if 1:  # Core functionality
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
    d: dict[object, object] = {}  # Options dictionary
    args = ParseCommandLine(d)
    print("Physical data on the planets")
    print(f"  Data to {d['-d']} figures (use -d option to change)")
    if d["-r"]:
        t.print(f"  {t.r}Relative to {planets[trans[d['-r']]].name}{t.n} "  # type: ignore
                f"{t.nr}(this color means not relative)")
    print()
    if "a" in args:
        for p in planets:
            print(str(planets[p]))
    else:
        letters = "".join(args)
        for letter in letters:
            if letter not in trans:
                continue
            print(str(planets[trans[letter]]))
