'''
Print out a sorted list of reference temperatures
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2025 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print out a sorted list of reference temperatures
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import bisect
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from temperature import ConvertTemperature
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = True
        g.data = None   # Holder of the list of temperature data
        g.unit = "c"    # Default temperature unit
        g.units = {"k": "K", "c": "°C", "f": "°F", "r": "°R"}
        g.get_color = {}
        g.allowed_units = set(list("cfkr"))
        # Printing constants
        g.indent = " "*2    # How much to indent the line
        g.T_width = 10      # Width of temperature column
        g.sep = " "*4       # Separation between temperature and description
        ii = isinstance
if 1:   # Data
    # First field is a temperature in K (with optional alternate unit letter of C, F, or R)
    # Remaining string is the description
    data = '''

        0 Absolute zero temperature on Kelvin scale
        1.41679e32 Planck temperature
        573-773 Mineral oil b.p.
        180C Mineral oil flash point
        0C Common STP at 1 atmosphere pressure
        288.1 Standard atmosphere at sea level
        284.2 Standard atmosphere at 2 kft
        268.3 Standard atmosphere at 10 kft
        248.6 Standard atmosphere at 20 kft
        228.8 Standard atmosphere at 30 kft
        216.7 Standard atmosphere at 40 kft
        216.7 Standard atmosphere at 50 kft
        227.0 Standard atmosphere at 100 kft

        380 Sulfur (gamma) m.p.
        386 Sulfur (alpha) m.p.
        392.2 Sulfur (beta) m.p.
        455.9 Solder, 63 Sn, 37 Pb (eutectic) m.p.
        463.1 Solder, 60 Sn, 40 Pb m.p.
        465.4 Solder, 70 Sn, 30 Pb m.p.
        489.3 Solder, 50 Sn, 50 Pb m.p.
        683 Phosphorus (red, under pressure) m.p.

        420F Faint yellow metal temper:  knives, hammers
        430F Very pale yellow metal temper:  reamers
        440F Light yellow metal temper:  lathe tools, scrapers, milling cutters, reamers
        450F Pale straw yellow metal temper:  twist drills for hard use
        460F Straw yellow metal temper:  dies, punches, bits, reamers
        470F Deep straw yellow metal temper:
        480F Dark yellow metal temper:  twist drills, large taps
        490F Yellow brown metal temper:
        500F Brown yellow metal temper:  axes, wood chisels, drifts, taps >= 1/2", dies
        510F Spotted red brown metal temper:
        520F Brown purple metal temper:  taps <= 1/4"
        530F Light purple metal temper:
        540F Full purple metal temper:  cold chisels, center punches
        550F Dark purple metal temper:
        560F Full blue metal temper:  screwdrivers, springs, gears
        570F Dark blue metal temper:
        600F Medium blue metal temper:  scrapers, spokeshaves
        640F Light blue metal temper:

        400C Red, visible at night (incandescence)      
        474C Red, visible at twilight (incandescence)   
        524C Red, visible in daylight (incandescence)   
        580C Red, visible in sunlight (incandescence)   
        660C Blood red (incandescence)                  
        700C Dark red (incandescence)                   
        800C Dull cherry red (incandescence)            
        900C Cherry red (incandescence)                 
        1000C Bright cherry red (incandescence)          
        1100C Orange red (incandescence)                 
        1200C Orange yellow (incandescence)              
        1300C Yellow white (incandescence)               
        1400C White (incandescence)                      
        1500C Brilliant white (incandescence)            
        1600C Blue white (incandescence)                 
        2250C Acetylene flame (incandescence)            
        3000C Induction furnace (incandescence)          
        4000C Electric arc light (incandescence)         

        5900 Surface of sun
        100C Boiling point of water at 1 atmosphere
        98.6F Body temperature
        40C Sweltering air temperature
        30C Warm to hot air temperature
        20C Comfortable air temperature
        10C Cold air temperature
        0C Freezing point of water at 1 atmosphere

        # https://www.nist.gov/pml/owm/culinary-temperature
        200F Cool oven temperature
        250F Very slow oven temperature
        300F-325F Slow oven temperature
        325F-350F Moderately slow oven temperature
        350F-375F Moderate oven temperature
        375F-400F Moderately hot oven temperature
        400F-450F Hot oven temperature
        450F-500F Very hot oven temperature

        # https://www.nist.gov/pml/owm/culinary-temperature
        220C Pie crust cooking temperature
        200C Quick breads cooking temperature
        190C Fried foods cooking temperature
        180C Apple crisp cooking temperature
        180C Banana bread cooking temperature
        180C Cakes cooking temperature
        180C Cookies cooking temperature
        180C Grilling steaks cooking temperature
        165C Roasting meat & poultry cooking temperature
        160C Macaroni and cheese cooking temperature
        150C Meringues cooking temperature
        120C Baked beans, custard cooking temperature
        100C Vegetables in water cooking temperature

        # https://en.wikipedia.org/wiki/Boiling_points_of_the_elements_(data_page)
        20.271 1 H Hydrogen (H₂) b.p.
        4.222 2 He Helium b.p.
        1603 3 Li Lithium b.p.
        2742 4 Be Beryllium b.p.
        4200 5 B Boron b.p.
        4300 6 C Carbon (diamond) b.p.
        77.355 7 N Nitrogen (N₂) b.p.
        90.188 8 O Oxygen (O₂) b.p.
        85.04 9 F Fluorine (F₂) b.p.
        27.104 10 Ne Neon b.p.
        1156.090 11 Na Sodium b.p.
        1363 12 Mg Magnesium b.p.
        2743 13 Al Aluminum b.p.
        3538 14 Si Silicon b.p.
        550 15 P Phosphorus (white) b.p.
        717.8 16 S Sulfur (orthorhombic, alpha) b.p.
        717.8 16 S Sulfur (monoclinic, beta) b.p.
        717.87 16 S Sulfur (gamma) b.p.
        239.11 17 Cl Chlorine (Cl₂) b.p.
        87.302 18 Ar Argon b.p.
        1032 19 K Potassium b.p.
        1757 20 Ca Calcium b.p.
        3109 21 Sc Scandium b.p.
        3560 22 Ti Titanium (hexagonal) b.p.
        3680 23 V Vanadium b.p.
        2755 24 Cr Chromium b.p.
        2334 25 Mn Manganese b.p.
        3134 26 Fe Iron b.p.
        3200 27 Co Cobalt b.p.
        3003 28 Ni Nickel b.p.
        2835 29 Cu Copper b.p.
        1180 30 Zn Zinc b.p.
        2673 31 Ga Gallium b.p.
        3106 32 Ge Germanium b.p.
        887 33 As Arsenic (gray) b.p.
        958 34 Se Selenium (hexagonal, gray) b.p.
        332.0 35 Br Bromine (Br₂) b.p.
        119.735 36 Kr Krypton b.p.
        961 37 Rb Rubidium b.p.
        1650 38 Sr Strontium b.p.
        3203 39 Y Yttrium b.p.
        4650 40 Zr Zirconium b.p.
        5017 41 Nb Niobium b.p.
        4912 42 Mo Molybdenum b.p.
        4538 43 Tc Technetium (⁹⁸Tc?) b.p.
        4423 44 Ru Ruthenium b.p.
        3968 45 Rh Rhodium b.p.
        3236 46 Pd Palladium b.p.
        2483 47 Ag Silver b.p.
        1040 48 Cd Cadmium b.p.
        2345 49 In Indium b.p.
        2875 50 Sn Tin (white) b.p.
        1908 51 Sb Antimony b.p.
        1261 52 Te Tellurium b.p.
        457.4 53 I Iodine (I₂) b.p.
        165.051 54 Xe Xenon b.p.
        944 55 Cs Cesium b.p.
        1910 56 Ba Barium b.p.
        3737 57 La Lanthanum b.p.
        3716 58 Ce Cerium b.p.
        3403 59 Pr Praseodymium b.p.
        3347 60 Nd Neodymium b.p.
        3273 61 Pm Promethium (¹⁴⁷Pm?) b.p.
        2173 62 Sm Samarium b.p.
        1802 63 Eu Europium b.p.
        3546 64 Gd Gadolinium b.p.
        3396 65 Tb Terbium b.p.
        2840 66 Dy Dysprosium b.p.
        2873 67 Ho Holmium b.p.
        3141 68 Er Erbium b.p.
        2223 69 Tm Thulium b.p.
        1703 70 Yb Ytterbium b.p.
        3675 71 Lu Lutetium b.p.
        4876 72 Hf Hafnium b.p.
        5731 73 Ta Tantalum b.p.
        6203 74 W Tungsten b.p.
        5869 75 Re Rhenium b.p.
        5285 76 Os Osmium b.p.
        4403 77 Ir Iridium b.p.
        4098 78 Pt Platinum b.p.
        3243 79 Au Gold b.p.
        629.88 80 Hg Mercury b.p.
        1746 81 Tl Thallium b.p.
        2022 82 Pb Lead b.p.
        1837 83 Bi Bismuth b.p.
        1235 84 Po Polonium (alpha) b.p.
        211.5 86 Rn Radon b.p.
        890 87 Fr Francium b.p.
        2010 88 Ra Radium b.p.
        3471 89 Ac Actinium (²²⁷Ac?) b.p.
        5061 90 Th Thorium b.p.
        4404 92 U Uranium b.p.
        4273 93 Np Neptunium b.p.
        3501 94 Pu Plutonium b.p.
        2880 95 Am Americium b.p.
        3383 96 Cm Curium (²⁴⁴Cm?) b.p.

        # Melting point of elements https://en.wikipedia.org/wiki/List_of_chemical_elements
        14.01 1 H Hydrogen m.p.
        453.69 3 Li Lithium m.p.
        1560 4 Be Beryllium m.p.
        2349 5 B Boron m.p.
        >4000 6 C Carbon m.p.
        63.15 7 N Nitrogen m.p.
        54.36 8 O Oxygen m.p.
        53.53 9 F Fluorine m.p.
        24.56 10 Ne Neon m.p.
        370.87 11 Na Sodium m.p.
        923 12 Mg Magnesium m.p.
        933.47 13 Al Aluminum m.p.
        1687 14 Si Silicon m.p.
        317.30 15 P Phosphorus m.p.
        388.36 16 S Sulfur m.p.
        171.6 17 Cl Chlorine m.p.
        83.80 18 Ar Argon m.p.
        336.53 19 K Potassium m.p.
        1115 20 Ca Calcium m.p.
        1814 21 Sc Scandium m.p.
        1941 22 Ti Titanium m.p.
        2183 23 V Vanadium m.p.
        2180 24 Cr Chromium m.p.
        1519 25 Mn Manganese m.p.
        1811 26 Fe Iron m.p.
        1768 27 Co Cobalt m.p.
        1728 28 Ni Nickel m.p.
        1357.77 29 Cu Copper m.p.
        692.88 30 Zn Zinc m.p.
        302.9146 31 Ga Gallium m.p.
        1211.40 32 Ge Germanium m.p.
        1090 33 As Arsenic m.p.
        453 34 Se Selenium m.p.
        265.8 35 Br Bromine m.p.
        115.79 36 Kr Krypton m.p.
        312.46 37 Rb Rubidium m.p.
        1050 38 Sr Strontium m.p.
        1799 39 Y Yttrium m.p.
        2128 40 Zr Zirconium m.p.
        2750 41 Nb Niobium m.p.
        2896 42 Mo Molybdenum m.p.
        2430 43 Tc Technetium m.p.
        2607 44 Ru Ruthenium m.p.
        2237 45 Rh Rhodium m.p.
        1828.05 46 Pd Palladium m.p.
        1234.93 47 Ag Silver m.p.
        594.22 48 Cd Cadmium m.p.
        429.75 49 In Indium m.p.
        505.08 50 Sn Tin m.p.
        903.78 51 Sb Antimony m.p.
        722.66 52 Te Tellurium m.p.
        386.85 53 I Iodine m.p.
        161.4 54 Xe Xenon m.p.
        301.59 55 Cs Cesium m.p.
        1000 56 Ba Barium m.p.
        1193 57 La Lanthanum m.p.
        1068 58 Ce Cerium m.p.
        1208 59 Pr Praseodymium m.p.
        1297 60 Nd Neodymium m.p.
        1315 61 Pm Promethium m.p.
        1345 62 Sm Samarium m.p.
        1099 63 Eu Europium m.p.
        1585 64 Gd Gadolinium m.p.
        1629 65 Tb Terbium m.p.
        1680 66 Dy Dysprosium m.p.
        1734 67 Ho Holmium m.p.
        1802 68 Er Erbium m.p.
        1818 69 Tm Thulium m.p.
        1097 70 Yb Ytterbium m.p.
        1925 71 Lu Lutetium m.p.
        2506 72 Hf Hafnium m.p.
        3290 73 Ta Tantalum m.p.
        3695 74 W Tungsten m.p.
        3459 75 Re Rhenium m.p.
        3306 76 Os Osmium m.p.
        2719 77 Ir Iridium m.p.
        2041.4 78 Pt Platinum m.p.
        1337.33 79 Au Gold m.p.
        234.43 80 Hg Mercury m.p.
        577 81 Tl Thallium m.p.
        600.61 82 Pb Lead m.p.
        544.7 83 Bi Bismuth m.p.
        527 84 Po Polonium m.p.
        575 85 At Astatine m.p.
        202 86 Rn Radon m.p.
        281 87 Fr Francium m.p.
        973 88 Ra Radium m.p.
        1323 89 Ac Actinium m.p.
        2115 90 Th Thorium m.p.
        1841 91 Pa Protactinium m.p.
        1405.3 92 U Uranium m.p.
        917 93 Np Neptunium m.p.
        912.5 94 Pu Plutonium m.p.
        1449 95 Am Americium m.p.
        1613 96 Cm Curium m.p.

    '''
if 1:   # Classes
    class Element:
        def __init__(self, T, name):
            self.Traw = T               # Raw string
            self.T = self.get_value(T)  # Numerical value
            self.name = name
        def __lt__(self, other):
            return self.T < other.T
        def __str__(self):
            s = g.indent
            # Convert self.T to requisite temperature unit
            T = ConvertTemperature(self.T, "k", g.unit)
            # Colorize the temperature
            s += f"{g.get_color[g.unit]}{T} {g.units[g.unit]}{t.n}{g.sep}"
            # Append the description
            s += self.name
            return f"{self.T} {self.name}"
        def __repr__(self):
            return str(self)
        def interpret(self, s):
            'Interpret s as a temperature converted to K'
            last = s[-1].lower()
            if last not in list("kcfr"):
                value = flt(s)
                last = "k"
            else:
                value = flt(s[:-1])
            T_K = ConvertTemperature(value, last, "k")
            return T_K
        def interpret_range(self, s):
            'Interpret "a-b" as a range; return the mean value in K'
            a, b = [self.interpret(i) for i in s.split("-")]
            return (a + b)/2
        def get_value(self, T):
            'T can have a single letter suffix denoting the temperature unit'
            if "-" in T:
                return self.interpret_range(T)
            elif T.startswith(">"):
                return self.interpret(T[1:])
            else:
                last = T[-1].lower()
                if last in list("kcfr"):
                    return self.interpret(T)
                else:
                    return flt(T)
if 1:   # Utility
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.k = t.roy if not d["-c"] else ""
        t.c = t.yel if not d["-c"] else ""
        t.f = t.grn if not d["-c"] else ""
        t.r = t.viol if not d["-c"] else ""
        t.N = t.n if not d["-c"] else ""
        g.get_color["k"] = t.k
        g.get_color["c"] = t.c
        g.get_color["f"] = t.f
        g.get_color["r"] = t.r
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.n}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''

        The basic use cases for this script are:  1) show various temperatures close to an entered
        temperature and 2) look up a temperature for a material.  

        Here's an example of the script's use.  I wanted to make an ad hoc electrical clamp from
        an office binder clip.  These would be cheap and have sufficient size to clamp on standard
        tapered lead-acid battery terminals, as I was building a battery charger for up to 8
        batteries and wanted a functional clip without having to buy 8 commercial clips at $5 to
        $10 each.  My design was to first sand off the blue oxide layer on the clamp's inner edges
        and solder a wire to a hole drilled in the top of the clip.  My concern was whether the
        heat of soldering would ruin the spring temper of the clip, ruining its clamping ability.
        If so, then I'd have to attach the wire with e.g. a rivet instead.  I used this script to
        get some temperatures:

            'python temperature_ref.py solder' gave me the melting point of eutectic tin-lead
            solder, which is 182 °C.

            'python temperature_ref.py temper:' gave me 293 °C, the tempering temperature of
            springs that give the characteristic blue oxide layer.

            My soldering iron is typically set to 350 °C, but I might set it higher if it doesn't
            replace the heat fast enough to melt the solder and heat the steel clamp well enough
            to melt the solder.  There appears to be a 100 °C margin, so I'm hoping I shouldn't
            have a problem.  I decided to proceed with the fabrication experiment.

            I felt a better design would be to take some solid copper wire, pound it flat, bend it
            around the sanded bottom of the clip and solder the copper to the steel clip so that
            the copper contacts the lead battery post instead of the sanded curved steel surface,
            giving better contact.  This is because I worry about the sanded bare steel rusting
            over time, leading to them needing periodic maintenance.  The copper strips will
            require less maintenance. 

        This script is intended to help you find temperatures near a chosen temperature.  The data
        comprising the script is included so you can edit the items to your tastes.  For example,
        the items contain the melting and boiling points of the elements.  To find the melting
        point of aluminum, use the regex 'aluminum' and you'll get the melting point (m.p) and
        boiling point (b.p.) of elemental aluminum.

        In the raw data, some temperatures are given as e.g. '300F-350F', which is a range of
        temperatures for archaic terms like 'moderately hot oven', which the script will print the
        mean of the two values.

        The first argument on the command line can optionally be a temperature unit (c f k r),
        case not important.  This establishes the default unit to use with numbers on the command
        line without a cuddled unit suffix and the temperature unit to produce the report.  Note
        the different temperature units are printed in different colors (they are the same as
        those used in the /plib/pgm/convert_temperature.py script).

        The elemental data are printed as e.g. '1414 °C       14 Si Silicon m.p.', which gives the
        atomic number, elemental symbol, and the element's name.

        The default temperature unit used is in the variable g.unit.

        '''))
        exit(0)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [unit] regex1 [regex2...]
          Search for items in the temperature list that match the regexes.  If unit is present, it
          must be one of the letters c, f, k, r indicating the temperature unit to use (default is
          c).  Numbers will display items with temperatures close to the indicated one.  Each
          regex is searched for separately.
        Examples
          temperature_ref.py c 200
            Show items with temperatures near 200 °C.
          temperature_ref.py aluminum
            Show items containing the string 'aluminum'.
        Options:
            -a      Show all entries
            -c      Don't use color
            -h      Print a manpage
            -i      Don't ignore case
            -n n    ± number of items to display [{d["-n"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all entries
        d["-c"] = False     # Don't use color
        d["-d"] = 4         # Number of digits
        d["-i"] = False     # Don't ignore case
        d["-n"] = 2         # Number of items to display on either side of found temperature items
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "acd:hin:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("aci"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-n":
                try:
                    d[o] = abs(int(a))
                except ValueError:
                    Error(f"-n option's argument must be an integer")
            elif o == "-h":
                Manpage()
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = True
        GetColors()
        return args
if 1:   # Core functionality
    def GetData():
        'Return a list of [T_K, Description] elements'
        o = []
        for line in data.split("\n"):
            line = line.strip()
            if not line or line[0] == "#":
                continue
            sp = line.find(" ")
            T, name = line[:sp], line[sp:]
            o.append(Element(T, name.strip()))
        return o
    def GetSuffix(s):
        '''Return (a, b) where b is the last character of s if it's c, f, k, or r and a is the
        remaining portion of the string.
        '''
        default = (s, "")
        if len(s) < 2:
            return default
        a, u = s[:-1], s[-1]
        if u in g.allowed_units:
            return (a, u)
        return default
    def GetRegexes(args):
        '''If the first argument is one of the letters c, f, k, r, then set g.unit using it.
        Otherwise, see if it's a number by seeing if it's a flt (it can have one of the unit
        letters as a suffix).  If not, then compile it as a regular expression.  Return
        (numbers_in_K, compiled_regexes).
        '''
        flags = re.X if d["-i"] else re.X | re.I
        # Check for first letter being a unit
        if len(args[0]) == 1:
            letter = args[0].lower()
            if letter in g.allowed_units:
                g.unit = letter
                args.pop(0)
        temperatures_in_K, regexes = [], []
        for item in args:
            # See if it's a number
            is_a_number = False
            mo = rnum.match(item)
            if mo:
                num, unit = GetSuffix(item)
                try:
                    T = flt(num)
                    is_a_number = True
                except ValueError:
                    pass
                if is_a_number:
                    T = ConvertTemperature(T, unit, "k")     # Convert it to K
                    temperatures_in_K.append(T)
                    continue
            # It's a regex; compile it
            try:
                r = re.compile(item, flags)
                regexes.append(r)
            except Exception as e:
                Error(f"{repr(item)} is a bad regular expression")
        return (temperatures_in_K, regexes)
        raise ValueError
    def IsTemperatureUnit(arg):
        "Return True if it's a single letter that's a temperature unit"
        return len(arg) == 1 and arg.lower() in g.allowed_units
    def IsTemperature(arg):
        'Return (temperature, unit) or None'
        flags = re.X if d["-i"] else re.X | re.I
        rnum = re.compile(r'''              # Regex to get integers or floats
            (?x)                            # Allow verbosity
            ^
            (                               # Group
                [+-]?                       # Optional sign
                \.\d+                       # Number like .345
                ([eE][+-]?\d+)?|            # Optional exponent
            # or
                [+-]?                       # Optional sign
                \d+\.?\d*                   # Number:  2.345
                ([eE][+-]?\d+)?             # Optional exponent
            )                               # End group
            ([cfkrCFKR])?                   # Optional temperature unit
            $
            ''', flags)
        mo = rnum.match(arg)
        if mo:
            is_a_number = False
            num, unit = GetSuffix(arg)
            try:
                T = flt(num)
                is_a_number = True
            except ValueError:
                pass
            if is_a_number:
                return (T, unit)
        return None
    def GetTemperatureData(T_K):
        '''g.data is sorted by temperature in K, so use binary search to find the closest matches
        to the given temperature in K; return a list of indexes into g.data.
        '''
        found, key, N = [], lambda x: x.T, len(g.data) - 1
        # This call to bisect_left finds the insertion point in the sequence where an
        # element with the temperature T could be inserted and the sequence sort order
        # would be maintained.  This gets us close enough and then we include the d["-n"]
        # number of items on either side of this location.
        i = bisect.bisect_left(g.data, T_K, key=lambda x: x.T)
        found.append(i)
        R = range(1, d["-n"] + 1)
        # Add -n indexes to found
        for j in R:
            if i - j < 0:
                continue
            found.append(i - j)
        # Increment i while g.data[i] == T_K
        while i < len(g.data) and g.data[i].T == T_K:
            i += 1
        # Add +n indexes to found
        for j in R:
            if i + j > N:
                continue
            found.append(i + j)
        found = list(sorted(set(found)))
        return found
    def PrintItems(results):
        for i in results:
            e = g.data[i]   # Element instance
            print(g.indent, end="")
            # Convert e.T to requisite temperature unit
            T = ConvertTemperature(e.T, "k", g.unit)
            # Print the colorized temperature
            s = f"{T} {g.units[g.unit]}"
            print(f"{g.get_color[g.unit]}{s:{g.T_width}s}{t.n}{g.sep}", end="")
            # Print the description
            print(e.name)

if __name__ == "__main__":
    g.data = sorted(GetData())
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    # See if first argument is a temperature unit
    if args and IsTemperatureUnit(args[0]):
        g.unit = args[0]
        args.pop(0)
    if d["-a"]:
        # Print all entries
        PrintItems(range(len(g.data)))
    else:
        if not args:
            Usage()
        for arg in args:
            results = IsTemperature(arg)
            if results is not None:
                # The user gave a temperature to search for
                T, unit = results
                #Dbg(f"T = {T}, unit = {unit!r}")
                if not unit:
                    unit = g.unit
                T_K = ConvertTemperature(T, unit, "k")
                results = GetTemperatureData(T_K)
                if results:     # List of matching item indexes
                    print(f"Search for temperature {repr(arg)}")
                    PrintItems(results)
            else:
                # arg is a regex
                flags = re.X if d["-i"] else re.X | re.I
                r = re.compile(arg, flags)
                results = []
                for i, item in enumerate(g.data):
                    mo = r.search(item.name)
                    if mo:
                        results.append(i)
                if results:
                    print(f"Search for regex {repr(arg)}")
                    PrintItems(results)
