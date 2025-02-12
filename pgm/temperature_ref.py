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
        from collections import deque
        from pathlib import Path as P
        import bisect
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from dpprint import PP
        from temperature import ConvertTemperature
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        pp = PP()   # pprint tuned to current screen width
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
        0C Common STP at 1 atmosphere pressure
        288.1 Standard atmosphere at sea level
        284.2 Standard atmosphere at 2 kft
        268.3 Standard atmosphere at 10 kft
        248.6 Standard atmosphere at 20 kft
        228.8 Standard atmosphere at 30 kft
        216.7 Standard atmosphere at 40 kft
        216.7 Standard atmosphere at 50 kft
        227.0 Standard atmosphere at 100 kft

        380 Sulfur (gamma) melting point
        386 Sulfur (alpha) melting point
        392.2 Sulfur (beta) melting point
        455.9 Solder, 63 Sn, 37 Pb (eutectic) melting point
        463.1 Solder, 60 Sn, 40 Pb melting point
        465.4 Solder, 70 Sn, 30 Pb melting point
        489.3 Solder, 50 Sn, 50 Pb melting point
        683 Phosphorus (red, under pressure) melting point

        420F Faint yellow temper, (Knives, hammers)
        430F Very pale yellow temper, (Reamers)
        440F Light yellow temper, (Lathe tools, scrapers, milling cutters, reamers)
        450F Pale straw yellow temper, (Twist drills for hard use)
        460F Straw yellow temper, (Dies, punches, bits, reamers)
        470F Deep straw yellow temper
        480F Dark yellow temper, (Twist drills, large taps)
        490F Yellow brown temper
        500F Brown yellow temper, (Axes, wood chisels, drifts, taps >= 1/2", dies)
        510F Spotted red brown temper
        520F Brown purple temper, (Taps <= 1/4")
        530F Light purple temper
        540F Full purple temper, (Cold chisels, center punches)
        550F Dark purple temper
        560F Full blue temper, (Screwdrivers, springs, gears)
        570F Dark blue temper
        600F Medium blue temper, (Scrapers, spokeshaves)
        640F Light blue temper
        400C Red, visible at night (incandescent color)      
        474C Red, visible at twilight (incandescent color)   
        524C Red, visible in daylight (incandescent color)   
        580C Red, visible in sunlight (incandescent color)   
        660C Blood red (incandescent color)                  
        700C Dark red (incandescent color)                   
        800C Dull cherry red (incandescent color)            
        900C Cherry red (incandescent color)                 
        1000C Bright cherry red (incandescent color)          
        1100C Orange red (incandescent color)                 
        1200C Orange yellow (incandescent color)              
        1300C Yellow white (incandescent color)               
        1400C White (incandescent color)                      
        1500C Brilliant white (incandescent color)            
        1600C Blue white (incandescent color)                 
        2250C Acetylene flame (incandescent color)            
        3000C Induction furnace (incandescent color)          
        4000C Electric arc light (incandescent color)         

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
        20.271 Element 1 H hydrogen (H₂) boiling point
        4.222 Element 2 He helium boiling point
        1603 Element 3 Li lithium boiling point
        2742 Element 4 Be beryllium boiling point
        4200 Element 5 B boron boiling point
        4300 Element 6 C carbon (diamond) boiling point
        77.355 Element 7 N nitrogen (N₂) boiling point
        90.188 Element 8 O oxygen (O₂) boiling point
        85.04 Element 9 F fluorine (F₂) boiling point
        27.104 Element 10 Ne neon boiling point
        1156.090 Element 11 Na sodium boiling point
        1363 Element 12 Mg magnesium boiling point
        2743 Element 13 Al aluminum boiling point
        3538 Element 14 Si silicon boiling point
        550 Element 15 P phosphorus (white) boiling point
        717.8 Element 16 S sulfur (orthorhombic, alpha) boiling point
        717.8 Element 16 S sulfur (monoclinic, beta) boiling point
        717.87 Element 16 S sulfur (gamma) boiling point
        239.11 Element 17 Cl chlorine (Cl₂) boiling point
        87.302 Element 18 Ar argon boiling point
        1032 Element 19 K potassium boiling point
        1757 Element 20 Ca calcium boiling point
        3109 Element 21 Sc scandium boiling point
        3560 Element 22 Ti titanium (hexagonal) boiling point
        3680 Element 23 V vanadium boiling point
        2755 Element 24 Cr chromium boiling point
        2334 Element 25 Mn manganese boiling point
        3134 Element 26 Fe iron boiling point
        3200 Element 27 Co cobalt boiling point
        3003 Element 28 Ni nickel boiling point
        2835 Element 29 Cu copper boiling point
        1180 Element 30 Zn zinc boiling point
        2673 Element 31 Ga gallium boiling point
        3106 Element 32 Ge germanium boiling point
        887 Element 33 As arsenic (gray) boiling point
        958 Element 34 Se selenium (hexagonal, gray) boiling point
        332.0 Element 35 Br bromine (Br₂) boiling point
        119.735 Element 36 Kr krypton boiling point
        961 Element 37 Rb rubidium boiling point
        1650 Element 38 Sr strontium boiling point
        3203 Element 39 Y yttrium boiling point
        4650 Element 40 Zr zirconium boiling point
        5017 Element 41 Nb niobium boiling point
        4912 Element 42 Mo molybdenum boiling point
        4538 Element 43 Tc technetium (⁹⁸Tc?) boiling point
        4423 Element 44 Ru ruthenium boiling point
        3968 Element 45 Rh rhodium boiling point
        3236 Element 46 Pd palladium boiling point
        2483 Element 47 Ag silver boiling point
        1040 Element 48 Cd cadmium boiling point
        2345 Element 49 In indium boiling point
        2875 Element 50 Sn tin (white) boiling point
        1908 Element 51 Sb antimony boiling point
        1261 Element 52 Te tellurium boiling point
        457.4 Element 53 I iodine (I₂) boiling point
        165.051 Element 54 Xe xenon boiling point
        944 Element 55 Cs caesium boiling point
        1910 Element 56 Ba barium boiling point
        3737 Element 57 La lanthanum boiling point
        3716 Element 58 Ce cerium boiling point
        3403 Element 59 Pr praseodymium boiling point
        3347 Element 60 Nd neodymium boiling point
        3273 Element 61 Pm promethium (¹⁴⁷Pm?) boiling point
        2173 Element 62 Sm samarium boiling point
        1802 Element 63 Eu europium boiling point
        3546 Element 64 Gd gadolinium boiling point
        3396 Element 65 Tb terbium boiling point
        2840 Element 66 Dy dysprosium boiling point
        2873 Element 67 Ho holmium boiling point
        3141 Element 68 Er erbium boiling point
        2223 Element 69 Tm thulium boiling point
        1703 Element 70 Yb ytterbium boiling point
        3675 Element 71 Lu lutetium boiling point
        4876 Element 72 Hf hafnium boiling point
        5731 Element 73 Ta tantalum boiling point
        6203 Element 74 W tungsten boiling point
        5869 Element 75 Re rhenium boiling point
        5285 Element 76 Os osmium boiling point
        4403 Element 77 Ir iridium boiling point
        4098 Element 78 Pt platinum boiling point
        3243 Element 79 Au gold boiling point
        629.88 Element 80 Hg mercury boiling point
        1746 Element 81 Tl thallium boiling point
        2022 Element 82 Pb lead boiling point
        1837 Element 83 Bi bismuth boiling point
        1235 Element 84 Po polonium (alpha) boiling point
        211.5 Element 86 Rn radon boiling point
        890 Element 87 Fr francium boiling point
        2010 Element 88 Ra radium boiling point
        3471 Element 89 Ac actinium (²²⁷Ac?) boiling point
        5061 Element 90 Th thorium boiling point
        4404 Element 92 U uranium boiling point
        4273 Element 93 Np neptunium boiling point
        3501 Element 94 Pu plutonium boiling point
        2880 Element 95 Am americium boiling point
        3383 Element 96 Cm curium (²⁴⁴Cm?) boiling point

        # Melting point of elements https://en.wikipedia.org/wiki/List_of_chemical_elements
        14.01 Element 1 H Hydrogen melting point
        453.69 Element 3 Li Lithium melting point
        1560 Element 4 Be Beryllium melting point
        2349 Element 5 B Boron melting point
        >4000 Element 6 C Carbon melting point
        63.15 Element 7 N Nitrogen melting point
        54.36 Element 8 O Oxygen melting point
        53.53 Element 9 F Fluorine melting point
        24.56 Element 10 Ne Neon melting point
        370.87 Element 11 Na Sodium melting point
        923 Element 12 Mg Magnesium melting point
        933.47 Element 13 Al Aluminium melting point
        1687 Element 14 Si Silicon melting point
        317.30 Element 15 P Phosphorus melting point
        388.36 Element 16 S Sulfur melting point
        171.6 Element 17 Cl Chlorine melting point
        83.80 Element 18 Ar Argon melting point
        336.53 Element 19 K Potassium melting point
        1115 Element 20 Ca Calcium melting point
        1814 Element 21 Sc Scandium melting point
        1941 Element 22 Ti Titanium melting point
        2183 Element 23 V Vanadium melting point
        2180 Element 24 Cr Chromium melting point
        1519 Element 25 Mn Manganese melting point
        1811 Element 26 Fe Iron melting point
        1768 Element 27 Co Cobalt melting point
        1728 Element 28 Ni Nickel melting point
        1357.77 Element 29 Cu Copper melting point
        692.88 Element 30 Zn Zinc melting point
        302.9146 Element 31 Ga Gallium melting point
        1211.40 Element 32 Ge Germanium melting point
        1090 Element 33 As Arsenic melting point
        453 Element 34 Se Selenium melting point
        265.8 Element 35 Br Bromine melting point
        115.79 Element 36 Kr Krypton melting point
        312.46 Element 37 Rb Rubidium melting point
        1050 Element 38 Sr Strontium melting point
        1799 Element 39 Y Yttrium melting point
        2128 Element 40 Zr Zirconium melting point
        2750 Element 41 Nb Niobium melting point
        2896 Element 42 Mo Molybdenum melting point
        2430 Element 43 Tc Technetium melting point
        2607 Element 44 Ru Ruthenium melting point
        2237 Element 45 Rh Rhodium melting point
        1828.05 Element 46 Pd Palladium melting point
        1234.93 Element 47 Ag Silver melting point
        594.22 Element 48 Cd Cadmium melting point
        429.75 Element 49 In Indium melting point
        505.08 Element 50 Sn Tin melting point
        903.78 Element 51 Sb Antimony melting point
        722.66 Element 52 Te Tellurium melting point
        386.85 Element 53 I Iodine melting point
        161.4 Element 54 Xe Xenon melting point
        301.59 Element 55 Cs Caesium melting point
        1000 Element 56 Ba Barium melting point
        1193 Element 57 La Lanthanum melting point
        1068 Element 58 Ce Cerium melting point
        1208 Element 59 Pr Praseodymium melting point
        1297 Element 60 Nd Neodymium melting point
        1315 Element 61 Pm Promethium melting point
        1345 Element 62 Sm Samarium melting point
        1099 Element 63 Eu Europium melting point
        1585 Element 64 Gd Gadolinium melting point
        1629 Element 65 Tb Terbium melting point
        1680 Element 66 Dy Dysprosium melting point
        1734 Element 67 Ho Holmium melting point
        1802 Element 68 Er Erbium melting point
        1818 Element 69 Tm Thulium melting point
        1097 Element 70 Yb Ytterbium melting point
        1925 Element 71 Lu Lutetium melting point
        2506 Element 72 Hf Hafnium melting point
        3290 Element 73 Ta Tantalum melting point
        3695 Element 74 W Tungsten melting point
        3459 Element 75 Re Rhenium melting point
        3306 Element 76 Os Osmium melting point
        2719 Element 77 Ir Iridium melting point
        2041.4 Element 78 Pt Platinum melting point
        1337.33 Element 79 Au Gold melting point
        234.43 Element 80 Hg Mercury melting point
        577 Element 81 Tl Thallium melting point
        600.61 Element 82 Pb Lead melting point
        544.7 Element 83 Bi Bismuth melting point
        527 Element 84 Po Polonium melting point
        575 Element 85 At Astatine melting point
        202 Element 86 Rn Radon melting point
        281 Element 87 Fr Francium melting point
        973 Element 88 Ra Radium melting point
        1323 Element 89 Ac Actinium melting point
        2115 Element 90 Th Thorium melting point
        1841 Element 91 Pa Protactinium melting point
        1405.3 Element 92 U Uranium melting point
        917 Element 93 Np Neptunium melting point
        912.5 Element 94 Pu Plutonium melting point
        1449 Element 95 Am Americium melting point
        1613 Element 96 Cm Curium melting point

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
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [unit] regex1 [regex2...]

          Search for items in the temperature list that match the regexes.  If unit is present, it
          must be one of the letters c, f, k, r indicating the temperature unit to use (default is
          c).  Numbers will display items with temperatures close to the indicated one.  The
          regexes are ANDed together.

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
                Usage()
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
        remaining portion of the string.  Return K as the default temperature unit.
        '''
        default = (s, "k")
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

if __name__ == "__main__":
    g.data = sorted(GetData())
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        if IsTemperatureUnit(arg):
            g.unit = arg
        results = IsTemperature(arg)
        if results is not None:
            # The user gave a temperature to search for
            T, unit = results
            T_K = ConvertTemperature(T, unit, "k")
            results = GetTemperatureData(T_K)
            if results:
                print(f"Search for temperature {repr(arg)}")
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
        else:
            # arg is a regex
            pass
