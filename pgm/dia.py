"""

- To do
    - This script and de.py need to have functionalities combined
    - Options
        - Option to get a diameter, meaning output only sockets, bushings,
        - Need an option to get rid of the more esoteric sizes.  Things I
          won't use much are:  Birmingham Gauge, Stub's, knitting needle,
          Brit Std wire, Mfr's gauge, Washburn & Moen, music wire gauge,
          Galvanized sheet gauge, Zinc sheet gauge
        - -r for regex search
    - Update sockets with newer impact socket sizes
    - Use flt, get rid of sig drills, etc.
    - Include dimensionless numbers too
    - Instead of tolerance, shoot for getting e.g. 20 numbers on either
      side of the target value.
    - Update color
        - Change the printout to show negative deviations in red and
          positive deviations in green

General-purpose diameter/length finding utility.
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Identifies dimensions that might be close to some "standard" size
    # ∞what∞#
    # ∞test∞# #∞test∞#
    # Standard imports
    import sys
    import getopt
    import re
    from fractions import Fraction
    from math import *
    from decimal import Decimal
    from pdb import set_trace as xx

    # Custom imports
    from wrap import dedent
    from u import u, ParseUnit
    from frange import frange, Sequence
    from sig import sig
    from f import flt

    if 1:
        have_color = True
        from color import Color, TRM as t

        t.always = True
    else:
        try:
            import color as c

            have_color = True
        except ImportError:
            have_color = False
    # Global variables
    ii = isinstance
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Manpage():
        print(
            dedent(f"""
        I use this script as a helper for shop tasks.  Here are some examples:
 
            - Form a circle from wire: I have some music wire that I want to form into a circle of
              1.78 inches in diameter.  I run this script to get a suitable mandrel with the
              command line '1.78 inches'.  The best match is 1.768 inches, the outside diameter of
              a Snap-On 1-3/8 half-inch drive socket.  I clamp this socket in the vise and wind a
              chunk of wire around the socket body.  After the wire is relaxed, it will expand to a
              larger size because it is heat treated.  Suppose the relaxed size is 2.04 inches.
              This is 15% over the desired value, so I run the script again with the command line
              '-s 15 1.78 inches' to correct for the 15% spring-back and get the size 1.512 inches,
              which is the smaller Snap-On 7/8 inch socket.  Another trial gets me a suitable
              circle of wire.
 
            - Need to shim something up by 2.7 inches:  The script recommends a no-name brand 13/16
              inch spark plug socket, whose length is 2.733 inches, 1.2% from the desired value.
              If I need to be under the 2.7 inch value, a 50 mm 3/4" drive socket has a diameter
              that's 2.2% low.
 
        The things like sockets and other things in the script will be special to my environment,
        so you will want to edit the GetData() function to reflect your own stuff.  
 
        Color coding is used to identify common classes of things.  For example, if you enter '8
        mm' on the command line, you'll see inch-based fractions in brown, inch-based SHCS sizes in
        light blue, inch-based hex nut wrench sizes in orange, millimeters in blue, and AWG sizes
        in light brown.  You can change the color coding used in the GetData() function.
 
        Exact size matches are flagged with a '*' character.
        
        If you want to change default behavior, examine the options' default values in
        ParseCommandLine().
        
        The Sockets() function defines on-hand sockets, bushings, etc.  If you want it to reflect
        the sizes you have, you'll have to measure your sockets and edit the function's data.
        
        Synonyms
            US Steel Wire Gauge same as
                Washburn & Moen
                American Steel and Wire Company Gauge
                Roebling Wire Gauge
        
        Birmingham Gauge same as
            Stub's Iron Wire Gauge (don't confuse with Stub's Steel Wire Gauge)
        
        Abbreviations:
            SHCS        Socket head cap screw
        
        Reference information was taken from:
            MH    "Machinery's Handbook", 19th ed., 1971 (1973 printing)
            TAD   "Universal Reference Calculator", TAD Inc., 1964
        or various web sites attributed in the code.
        """)
        )
        exit(0)

    def Usage(d, status=1):
        name, tol = sys.argv[0], d["-t"]
        print(
            dedent(f"""
        Usage:  {name} [options] diameter [unit]
          Identifies dimensions that might be close to some "standard" size, such as fractions of
          an inch, numbered drills, millimeters, or on-hand socket sizes.  Use -f to include the
          full set of different size systems.
        
          'diameter' is a length and may contain an optional trailing unit (size is in {d["-u"]} if
          no unit is given).  Expressions for the diameter are allowed and the math module's
          symbols are in scope.
        Examples:
          {name} 1
            Show things within {tol}% of 1 inch in diameter.
          {name} -t 10 pi/10 mm
            Show things that are within 10% of pi/10 mm in diameter.  Note output diameters are in
            mm.
        Options:
            -a      Show all of the dimensions stored in the script
            -c      Don't show results in color
            -d      The diameter is a dimensionless number; show numbers such as
                    Renard, E series, etc. that are close to it.
            -f      Include full set of sizes
            -h      More detailed help
            -k      List of on-hand sockets
            -n n    Number of significant digits [{d["-n"]}]
            -o u    Output unit (default is same unit as used for input)
            -s p    Spring-back percentage.  The diameter used will be reduced by 
                    the indicated percentage.
            -t p    Tolerance in % for searching [{tol}]
            -u u    Default measurement unit [{d["-u"]}]
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Show all dimensions
        d["-c"] = True  # Show results in color
        d["-d"] = False  # Dimensionless
        d["-f"] = False  # Use full set of sizes
        d["-k"] = False  # Show sockets
        d["-n"] = 4  # Significant digits
        d["-o"] = None  # Output unit
        d["-s"] = 0  # Spring-back percentage
        d["-t"] = 5  # Tolerance in %
        d["-u"] = "inches"  # Default unit
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "acdfhkn:o:s:t:u:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        msg = "'{}' is an unrecognized unit"
        for o, a in opts:
            if o[1] in "acdfk":
                d[o] = not d[o]
            elif o in ("-h",):
                Manpage()
            elif o in ("-n",):
                try:
                    d["-n"] = int(a)
                except Exception:
                    Error("'{}' is a bad number of digits".format(a))
                if not (1 <= d["-n"] <= 15):
                    Error("Number of significant digits must be between 1 and 15")
            elif o in ("-o",):
                d["-o"] = a
                _, dim = u(a, dim=True)
                if dim is None:
                    Error(msg.format(a))
            elif o in ("-s",):
                try:
                    d["-s"] = float(a)
                except Exception:
                    Error("'{}' is a bad percentage".format(a))
                if d["-s"] < 0:
                    Error("A spring-back percentage must be >= 0")
            elif o in ("-t",):
                try:
                    d["-t"] = float(a)
                except Exception:
                    Error("'{}' is an improper tolerance percentage".format(a))
            elif o in ("-u",):
                d["-u"] = a
                _, dim = u(a, dim=True)
                if dim is None:
                    Error(msg.format(a))
        if not have_color:
            d["-c"] = False
        Size.tolerance_pct = d["-t"]
        if not (d["-a"] or d["-k"]) and not args:
            Usage(d)
        return args

    def RoundOff(number, digits=14):
        """Round the significand of number to the indicated number of digits
        and return the number suitably rounded (integers are return
        untransformed).  The desire is to round things such as:
            745.6998719999999  --> 745.699872
            4046.8726100000003 --> 4046.87261
            0.0254*12 = 0.30479999999999996 --> 0.3048
        so that printing the floating point representations can be more
        pleasing to the eye.  This should be mostly harmless (harmful == loss
        of significance) for unit conversion factors, as virtually no one works
        with measurements to 14 significant figures (there are only a few
        physical constants listed at NIST to about 14 significant figures).
        However, be careful if you set digits to much less than 15, as you may
        lose some significance in some of the conversion factors.
        """
        # Format the number to a string using scientific notation and pick off
        # the significand, which will be a string representing a number between
        # 1 and 10.  This is converted to a Decimal, which is then passed to
        # python's round() function.  The number is reconstituted with its
        # exponent using Decimal arithmetic, then returned as a float.
        if isinstance(number, int):
            return number
        if not isinstance(number, float):
            raise TypeError("number must be a float or integer")
        if not (1 <= digits <= 15):
            raise ValueError("digits must be between 1 and 15")
        x, sign = abs(number), -1 if number < 0 else 1
        significand_str, exponent_str = "{:.16e}".format(x).split("e")
        significand_dec = Decimal(significand_str)
        significand = Decimal(str(round(significand_dec, digits)))
        e = int(exponent_str)
        factor = Decimal(10) ** abs(e)
        if e < 0:
            return float(significand / factor)
        return float(significand * factor)

    def SignSignificandExponent(x, digits=15):
        """Returns a tuple (sign, mantissa, exponent) of a floating point
        number x.
        """
        s = ("%%.%de" % digits) % abs(float(x))
        return (1 - 2 * (x < 0), float(s[0 : digits + 2]), int(s[digits + 3 :]))

    def SignificantFiguresS(value, digits=3, exp_compress=True):
        """Returns a string representing the number value rounded to
        a specified number of significant figures.  The number is
        converted to a string, then rounded and returned as a string.
        If you want it back as a number, use float() on the string.
        If exp_compress is true, the exponent has leading zeros
        removed.

        The following types of printouts can be gotten using this function
        and native python formats:

                A              B               C               D
            3.14e-12       3.14e-012       3.14e-012       3.14e-012
            3.14e-11       3.14e-011       3.14e-011       3.14e-011
            3.14e-10       3.14e-010       3.14e-010       3.14e-010
            3.14e-9        3.14e-009       3.14e-009       3.14e-009
            3.14e-8        3.14e-008       3.14e-008       3.14e-008
            3.14e-7        3.14e-007       3.14e-007       3.14e-007
            3.14e-6        3.14e-006       3.14e-006       3.14e-006
            3.14e-5        3.14e-005       3.14e-005       3.14e-005
            3.14e-4        3.14e-004        0.000314        0.000314
            3.14e-3        3.14e-003         0.00314         0.00314
            3.14e-2        3.14e-002          0.0314          0.0314
            3.14e-1        3.14e-001           0.314           0.314
            3.14e+0        3.14e+000            3.14            3.14
            3.14e+1        3.14e+001            31.4            31.4
            3.14e+2        3.14e+002             314           314.0
            3.14e+3        3.14e+003       3.14e+003          3140.0
            3.14e+4        3.14e+004       3.14e+004         31400.0
            3.14e+5        3.14e+005       3.14e+005        314000.0
            3.14e+6        3.14e+006       3.14e+006       3140000.0
            3.14e+7        3.14e+007       3.14e+007      31400000.0
            3.14e+8        3.14e+008       3.14e+008     314000000.0
            3.14e+9        3.14e+009       3.14e+009    3140000000.0
            3.14e+10       3.14e+010       3.14e+010   31400000000.0
            3.14e+11       3.14e+011       3.14e+011  314000000000.0
            3.14e+12       3.14e+012       3.14e+012       3.14e+012

        A:  SignificantFiguresS(x, 3)
        B:  SignificantFiguresS(x, 3, 0)
        C:  "%.3g" % x
        D:  float(SignificantFiguresS(x, 3))
        """
        if digits < 1 or digits > 15:
            msg = "Number of significant figures must be >= 1 and <= 15"
            raise ValueError(msg)
        sign, significand, exponent = SignSignificandExponent(float(value))
        fmt = "%%.%df" % (digits - 1)
        neg = "-" if sign < 0 else ""
        e = "e%+d" % exponent if exp_compress else "e%+04d" % exponent
        return neg + (fmt % significand) + e

    def SignificantFigures(value, figures=3):
        """Rounds a value to specified number of significant figures.
        Returns a float.
        """
        return float(SignificantFiguresS(value, figures))


if 1:  # Size information

    class Size(object):
        """Encapsulate a diameter or length of something in meters."""

        tolerance_pct = None
        # Set to a dictionary of string to color conversions to get color
        # console printing.
        colors = None

        def __init__(self, category, size, dia):
            """category and size are strings; dia is a float or int that is the
            diameter in m.
            """
            assert ii(category, str)
            assert ii(size, str)
            assert ii(dia, (int, float))
            self._category = category
            self._size = size
            self._dia = dia
            if not dia or dia < 0:
                raise ValueError("dia must be > 0")
            self._allowed = (Size, int, float)

        def color(self):
            """Set a color to use for printing out."""
            if 1:
                if Size.colors is not None:
                    if " skt" in self._category:
                        print(Size.colors["socket"], end="")
                    elif self._category in Size.colors:
                        print(Size.colors[self._category], end="")
                    else:
                        print(t.n, end="")
            else:
                if Size.colors is not None:
                    if " skt" in self._category:
                        c.fg(Size.colors["socket"])
                    elif self._category in Size.colors:
                        c.fg(Size.colors[self._category])
                    else:
                        c.normal()

        @property
        def category(self):
            return self._category

        @property
        def size(self):
            return self._size

        @property
        def dia(self):
            return self._dia

        def _check_type(self, other):
            if not ii(other, self._allowed):
                raise TypeError("'other' must be a Size object or number")

        def __lt__(self, other):
            self._check_type(other)
            if ii(other, Size):
                return self._dia < other._dia
            else:
                return self._dia < other

        def __le__(self, other):
            self._check_type(other)
            if ii(other, Size):
                return self._dia <= other._dia
            else:
                return self._dia <= other

        def __eq__(self, other):
            self._check_type(other)
            if ii(other, Size):
                return self._dia == other._dia
            else:
                return self._dia == other

        def __ne__(self, other):
            return not (self._dia == other._dia)

        def __str__(self):
            return "Size(" + self._category + ", " + self._size + ")"

        def __repr__(self):
            return str(self)

        def within(self, x):
            """Return True if x is within the set tolerance of this object's
            diameter.
            """
            tol = Size.tolerance_pct / 100
            low, high = (1 - tol) * self._dia, (1 + tol) * self._dia
            return low <= x <= high

    def GetData(opts):
        'Create a list of Size objects and put in opts["sizes"]'
        # MH = Machinery's Handbook, 19th ed.
        if opts["-c"]:
            if 1:
                Size.colors = {
                    "Millimeters": t("royl"),
                    "Number drill": t("yel"),
                    "AWG": t("brnl"),
                    "Fractions": t("orn"),
                    "US pipe": t("magl"),
                    "Sheet steel gauge": t("purl"),
                    "Number-sized machine screw": t("cynl"),
                    "socket": t("seal"),
                    "SPI pin gauge (inches)": t("sea"),
                    "SHCS head diameter": t("sky"),
                    "SHCS head height": t("sky"),
                    "SHCS Allen wrench size": t("sky"),
                    "Hex nut wrench size": t("ornl"),
                    "HF bushing": t("pnk"),
                    "HF bending fixture dies": t("pnk"),
                }
            else:
                Size.colors = {
                    "Millimeters": c.lblue,
                    "Number drill": c.lred,
                    "AWG": c.brown,
                    "Fractions": c.lgreen,
                    "US pipe": c.yellow,
                    "Sheet steel gauge": c.lmagenta,
                    "Number-sized machine screw": c.lcyan,
                    "socket": c.lwhite,
                }
        else:
            Size.colors = None
        d = []  # List of Size objects
        Check.debug = True  # If True, do simple checking of entered data
        # Number drills 1-80
        sizes = Check(
            (
                0,
                2280,
                2210,
                2130,
                2090,
                2055,
                2040,
                2010,
                1990,
                1960,
                1935,
                1910,
                1890,
                1850,
                1820,
                1800,
                1770,
                1730,
                1695,
                1660,
                1610,
                1590,
                1570,
                1540,
                1520,
                1495,
                1470,
                1440,
                1405,
                1360,
                1285,
                1200,
                1160,
                1130,
                1110,
                1100,
                1065,
                1040,
                1015,
                995,
                980,
                960,
                935,
                890,
                860,
                820,
                810,
                785,
                760,
                730,
                700,
                670,
                635,
                595,
                550,
                520,
                465,
                430,
                420,
                410,
                400,
                390,
                380,
                370,
                360,
                350,
                330,
                320,
                310,
                293,
                280,
                260,
                250,
                240,
                225,
                210,
                200,
                180,
                160,
                145,
                135,
            )
        )
        for i, sz in enumerate(sizes):
            if not i:
                continue
            dia_m = RoundOff(1e-4 * sz * u("inches"))
            s = Size("Number drill", str(i), dia_m)
            d.append(s)
        # AWG (MH pg 464), units are 1e-5 inches.  Also known as the Brown &
        # Sharpe Gauge.
        sizes = Check(
            (
                32490,
                28930,
                25760,
                22940,
                20430,
                18190,
                16200,
                14430,
                12850,
                11440,
                10190,
                9070,
                8080,
                7200,
                6410,
                5710,
                5080,
                4530,
                4030,
                3590,
                3200,
                2850,
                2530,
                2260,
                2010,
                1790,
                1590,
                1420,
                1260,
                1130,
                1000,
                893,
                795,
                708,
                630,
                561,
                500,
                445,
                396,
                353,
                314,
                280,
                249,
                222,
                198,
                176,
                157,
                140,
                124,
                111,
                99,
            )
        )
        for i, sz in enumerate(sizes):
            dia_m = RoundOff(1e-5 * sz * u("inches"))
            s = Size("AWG", str(i), dia_m)
            d.append(s)
        if 1:
            # Extra gauge numbers
            dia_m = RoundOff(0.3648 * u("inches"))
            d.append(Size("AWG", "2/0", dia_m))
            dia_m = RoundOff(0.4096 * u("inches"))
            d.append(Size("AWG", "3/0", dia_m))
            dia_m = RoundOff(0.4600 * u("inches"))
            d.append(Size("AWG", "4/0", dia_m))
            dia_m = RoundOff(0.5165 * u("inches"))
            d.append(Size("AWG", "5/0", dia_m))
            dia_m = RoundOff(0.5800 * u("inches"))
            d.append(Size("AWG", "6/0", dia_m))
        # US Steel wire gauge [MH pg 463, 464] (also known as Washburn & Moen,
        # American Steel and Wire Company gauge, and Roebling Wire Gauge).
        sizes = Check(
            (
                3065,
                2830,
                2625,
                2437,
                2253,
                2070,
                1920,
                1770,
                1620,
                1483,
                1350,
                1205,
                1055,
                915,
                800,
                720,
                625,
                540,
                475,
                410,
                348,
                317,
                286,
                258,
                230,
                204,
                181,
                173,
                162,
                150,
                140,
                132,
                128,
                118,
                104,
                95,
                90,
                85,
                80,
                75,
                70,
                66,
                62,
                60,
                58,
                55,
                52,
                50,
                48,
                46,
                44,
            )
        )
        name = "Washburn & Moen wire gauge"
        for i, sz in enumerate(sizes):
            dia_m = RoundOff(1e-4 * sz * u("inches"))
            s = Size(name, str(i), dia_m)
            if full:
                d.append(s)
        if full:
            # Extra gauge numbers
            dia_m = RoundOff(0.49 * u("inches"))
            d.append(Size(name, "7/0", dia_m))
            dia_m = RoundOff(0.4615 * u("inches"))
            d.append(Size(name, "6/0", dia_m))
            dia_m = RoundOff(0.4305 * u("inches"))
            d.append(Size(name, "5/0", dia_m))
            dia_m = RoundOff(0.3938 * u("inches"))
            d.append(Size(name, "4/0", dia_m))
            dia_m = RoundOff(0.3625 * u("inches"))
            d.append(Size(name, "3/0", dia_m))
            dia_m = RoundOff(0.331 * u("inches"))
            d.append(Size(name, "2/0", dia_m))
        # Sheet steel 3-27
        sizes = Check(
            (
                0,
                0,
                0,
                2391,
                2242,
                2092,
                1943,
                1793,
                1644,
                1495,
                1345,
                1196,
                1046,
                897,
                747,
                673,
                598,
                538,
                478,
                418,
                359,
                329,
                299,
                269,
                239,
                209,
                179,
                164,
            )
        )
        for i, sz in enumerate(sizes):
            if i < 3:
                continue
            dia_m = RoundOff(1e-4 * sz * u("inches"))
            s = Size("Sheet steel gauge", str(i), dia_m)
            if full:
                d.append(s)
        # Birmingham Gauge [MH pg 463, 464] (aka Stub's Iron Wire Gauge; do not
        # confuse with Stub's Steel Wire Gauge).
        sizes = Check(
            (
                3400,
                3000,
                2840,
                2590,
                2380,
                2200,
                2030,
                1800,
                1650,
                1480,
                1340,
                1200,
                1090,
                950,
                830,
                720,
                650,
                580,
                490,
                420,
                350,
                320,
                280,
                250,
                220,
                200,
                180,
                160,
                140,
                130,
                120,
                100,
                90,
                80,
                70,
                50,
                40,
            )
        )
        name = "Birmingham Gauge"
        for i, sz in enumerate(sizes):
            dia_m = RoundOff(1e-4 * sz * u("inches"))
            s = Size(name, str(i), dia_m)
            if full:
                d.append(s)
        if full:
            # Extra gauge numbers
            dia_m = RoundOff(0.5 * u("inches"))
            d.append(Size(name, "5/0", dia_m))
            dia_m = RoundOff(0.454 * u("inches"))
            d.append(Size(name, "4/0", dia_m))
            dia_m = RoundOff(0.425 * u("inches"))
            d.append(Size(name, "3/0", dia_m))
            dia_m = RoundOff(0.38 * u("inches"))
            d.append(Size(name, "2/0", dia_m))
        # Stubs Steel Wire Gauge [MH pg 463, 464]
        sizes = Check(
            (
                227,
                219,
                212,
                207,
                204,
                201,
                199,
                197,
                194,
                191,
                188,
                185,
                182,
                180,
                178,
                175,
                172,
                168,
                164,
                161,
                157,
                155,
                153,
                151,
                148,
                146,
                143,
                139,
                134,
                127,
                120,
                115,
                112,
                110,
                108,
                106,
                103,
                101,
                99,
                97,
                95,
                92,
                88,
                85,
                81,
                79,
                77,
                75,
                72,
                69,
                66,
                63,
                58,
                55,
                50,
                45,
                42,
                41,
                40,
                39,
                38,
                37,
                36,
                35,
                33,
                32,
                31,
                30,
                29,
                27,
                26,
                24,
                23,
                22,
                20,
                18,
                16,
                15,
                14,
                13,
            )
        )
        name = "Stub's Steel Wire Gauge"
        for i, sz in enumerate(sizes):
            dia_m = RoundOff(1e-3 * sz * u("inches"))
            s = Size(name, str(i), dia_m)
            if full:
                d.append(s)
        # Music Wire Gauge [MH pg 464] (also known as Piano Wire Gauge)
        sizes = Check(
            (
                9,
                10,
                11,
                12,
                13,
                14,
                16,
                18,
                20,
                22,
                24,
                26,
                29,
                31,
                33,
                35,
                37,
                39,
                41,
                43,
                45,
                47,
                49,
                51,
                55,
                59,
                63,
                67,
                71,
                75,
                80,
                85,
                90,
                95,
                100,
                106,
                112,
                118,
                124,
                130,
                138,
                146,
                154,
                162,
                170,
                180,
            ),
            neg_slope=False,
        )
        name = "Music Wire Gauge"
        for i, sz in enumerate(sizes):
            dia_m = RoundOff(1e-3 * sz * u("inches"))
            s = Size(name, str(i), dia_m)
            if full:
                d.append(s)
        if full:
            # Extra gauge numbers
            dia_m = RoundOff(0.004 * u("inches"))
            d.append(Size(name, "6/0", dia_m))
            dia_m = RoundOff(0.005 * u("inches"))
            d.append(Size(name, "5/0", dia_m))
            dia_m = RoundOff(0.006 * u("inches"))
            d.append(Size(name, "4/0", dia_m))
            dia_m = RoundOff(0.007 * u("inches"))
            d.append(Size(name, "3/0", dia_m))
            dia_m = RoundOff(0.008 * u("inches"))
            d.append(Size(name, "2/0", dia_m))
        # Manufacturer's standard gauge for steel sheet [MH pg 466]
        sizes = Check(
            (
                0,
                0,
                0,
                2391,
                2242,
                2092,
                1943,
                1793,
                1644,
                1495,
                1345,
                1196,
                1046,
                897,
                747,
                673,
                598,
                538,
                478,
                418,
                359,
                329,
                299,
                269,
                239,
                209,
                179,
                164,
                149,
                135,
                120,
                105,
                97,
                90,
                82,
                75,
                67,
                64,
                60,
            )
        )
        name = "Mfr's standard gauge for steel sheet"
        for i, sz in enumerate(sizes):
            if i < 3:
                continue
            dia_m = RoundOff(1e-4 * sz * u("inches"))
            s = Size(name, str(i), dia_m)
            if full:
                d.append(s)
        # Galvanized sheet gauge [MH pg 466]
        sizes = Check(
            (
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1681,
                1532,
                1382,
                1233,
                1084,
                934,
                785,
                710,
                635,
                575,
                516,
                456,
                396,
                366,
                336,
                306,
                276,
                247,
                217,
                202,
                187,
                172,
                157,
                142,
                134,
            )
        )
        name = "Galvanized sheet gauge"
        for i, sz in enumerate(sizes):
            if i < 8:
                continue
            dia_m = RoundOff(1e-4 * sz * u("inches"))
            s = Size(name, str(i), dia_m)
            if full:
                d.append(s)
        # Zinc sheet gauge [MH pg 466]
        sizes = Check(
            (
                0,
                0,
                0,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
                24,
                28,
                32,
                36,
                40,
                45,
                50,
                55,
                60,
                70,
                80,
                90,
                100,
                125,
            ),
            neg_slope=False,
        )
        name = "Zinc sheet gauge"
        for i, sz in enumerate(sizes):
            if i < 3:
                continue
            dia_m = RoundOff(1e-3 * sz * u("inches"))
            s = Size(name, str(i), dia_m)
            if full:
                d.append(s)
        # British standard wire gauge [MH pg 464]
        sizes = Check(
            (
                3240,
                3000,
                2760,
                2520,
                2320,
                2120,
                1920,
                1760,
                1600,
                1440,
                1280,
                1160,
                1040,
                920,
                800,
                720,
                640,
                560,
                480,
                400,
                360,
                320,
                280,
                240,
                220,
                200,
                180,
                164,
                148,
                136,
                124,
                116,
                108,
                100,
                92,
                84,
                76,
                68,
                60,
                52,
                48,
                44,
                40,
                36,
                32,
                28,
                24,
                20,
                16,
                12,
                10,
            )
        )
        name = "British Standard Wire Gauge"
        for i, sz in enumerate(sizes):
            dia_m = RoundOff(1e-4 * sz * u("inches"))
            s = Size(name, str(i), dia_m)
            if full:
                d.append(s)
        if full:
            # Extra gauge numbers
            dia_m = RoundOff(0.5 * u("inches"))
            d.append(Size(name, "7/0", dia_m))
            dia_m = RoundOff(0.464 * u("inches"))
            d.append(Size(name, "6/0", dia_m))
            dia_m = RoundOff(0.432 * u("inches"))
            d.append(Size(name, "5/0", dia_m))
            dia_m = RoundOff(0.4 * u("inches"))
            d.append(Size(name, "4/0", dia_m))
            dia_m = RoundOff(0.372 * u("inches"))
            d.append(Size(name, "3/0", dia_m))
            dia_m = RoundOff(0.348 * u("inches"))
            d.append(Size(name, "2/0", dia_m))
        # Hypodermic needles, 7-34 (is equal to the Birminham gauge)
        # From https://en.wikipedia.org/wiki/Needle_gauge_comparison_chart
        sizes = Check(
            (
                0.18,
                0.165,
                0.148,
                0.134,
                0.12,
                0.109,
                0.095,
                0.083,
                0.072,
                0.065,
                0.058,
                0.050,
                0.042,
                0.03575,
                0.03225,
                0.02825,
                0.02525,
                0.02225,
                0.02025,
                0.01825,
                0.01625,
                0.01425,
                0.01325,
                0.01225,
                0.01025,
                0.00925,
                0.00825,
                0.00725,
            )
        )
        name = "Hypodermic needle"
        for i, sz in enumerate(sizes):
            dia_m = RoundOff(sz * u("inches"))
            s = Size(name, str(i + 7), dia_m)
            if full:
                d.append(s)
        # US knitting needles (sizes in mm).  From
        # https://en.wikipedia.org/wiki/Knitting_needle#Needle_sizes_and_conversions
        for sz, mm in {
            "6/0": 0.7,
            "5/0": 1,
            "4/0": 1.2,
            "3/0": 1.5,
            "2/0": 1.75,
            "0": 2.0,
            "1": 2.25,
            "2": 2.75,
            "3": 3.25,
            "4": 3.5,
            "5": 3.75,
            "6": 4.0,
            "7": 4.5,
            "8": 5.0,
            "9": 5.5,
            "10": 6.0,
            "10 1/2": 6.5,
            "11": 8.0,
            "13": 9.0,
            "15": 10.0,
            "17": 12.0,
            "19": 16.0,
            "35": 19.0,
            "50": 25.0,
        }.items():
            dia_m = RoundOff(mm * u("mm"))
            s = Size("US knitting needle", sz, dia_m)
            if full:
                d.append(s)
        # British knitting needles (sizes in mm).  From
        # https://en.wikipedia.org/wiki/Knitting_needle#Needle_sizes_and_conversions
        for sz, mm in {
            "14": 2.0,
            "13": 2.25,
            "12": 2.75,
            "3": 3.0,
            "10": 3.25,
            "9": 3.75,
            "8": 4.0,
            "7": 4.5,
            "6": 5.0,
            "5": 5.5,
            "4": 6.0,
            "3": 6.5,
            "2": 7.0,
            "1": 7.5,
            "0": 8.0,
            "2/0": 9.0,
            "3/0": 10.0,
        }.items():
            dia_m = RoundOff(mm * u("mm"))
            s = Size("UK knitting needle", sz, dia_m)
            if full:
                d.append(s)
        # Japanese knitting needles (sizes in mm) From
        # https://en.wikipedia.org/wiki/Knitting_needle#Needle_sizes_and_conversions
        for sz, mm in {
            "0": 2.1,
            "1": 2.4,
            "2": 2.7,
            "3": 3.0,
            "4": 3.3,
            "5": 3.6,
            "6": 3.9,
            "7": 4.2,
            "8": 4.5,
            "9": 4.8,
            "10": 5.1,
            "11": 5.4,
            "12": 5.7,
            "13": 6.0,
            "14": 6.3,
            "15": 6.6,
        }.items():
            dia_m = RoundOff(mm * u("mm"))
            s = Size("Japanese knitting needle", sz, dia_m)
            if full:
                d.append(s)
        # Fractions of an inch
        for i in Sequence("1/64:1:1/64 17/16:2:1/16 17/8:3:1/8 13/4:6:1/4"):
            dia_m = RoundOff(float(i) * u("in"))
            s = Size("Fractions", ImproperFraction(i), dia_m)
            d.append(s)
        # US pipe sizes
        for sz, OD in (
            ("1/8", 0.405),
            ("1/4", 0.540),
            ("3/8", 0.675),
            ("1/2", 0.840),
            ("3/4", 1.050),
            ("1", 1.315),
            ("1-1/4", 1.660),
            ("1-1/2", 1.900),
            ("2", 2.375),
        ):
            dia_m = RoundOff(OD * u("in"))
            s = Size("US pipe", sz, dia_m)
            d.append(s)
        # Millimeters
        for i in Sequence("""0.1:1:0.1 1.5:25:0.5 26:50 55:100:5 110:300:10
                        350:1000:50"""):
            dia_m = float(i) * u("mm")
            s = Size("Millimeters", str(i), dia_m)
            d.append(s)
        # Numbered thread diameters
        for i in (0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14):
            dia_in = 0.013 * i + 0.06
            dia_m = RoundOff(dia_in * u("in"))
            s = Size("Number-sized machine screw", str(i), dia_m)
            d.append(s)
        # SHCS diameters, inch fasteners [TAD]
        for sz, OD in (
            ("#0", 0.096),
            ("#1", 0.118),
            ("#2", 0.140),
            ("#3", 0.161),
            ("#4", 0.183),
            ("#5", 0.205),
            ("#6", 0.226),
            ("#8", 0.270),
            ("#10", 5 / 16),
            ("1/4", 3 / 8),
            ("5/16", 15 / 32),
            ("3/8", 9 / 16),
            ("7/16", 21 / 32),
            ("1/2", 3 / 4),
            ("5/8", 15 / 16),
            ("3/4", 9 / 8),
            ("7/8", 21 / 16),
            ("1", 3 / 2),
        ):
            dia_m = RoundOff(OD * u("in"))
            s = Size("SHCS head diameter", sz, dia_m)
            d.append(s)
        # SHCS head height, inch fasteners [TAD]
        for sz, OD in (
            ("#0", 0.06),
            ("#1", 0.073),
            ("#2", 0.086),
            ("#3", 0.099),
            ("#4", 0.112),
            ("#5", 0.125),
            ("#6", 0.138),
            ("#8", 0.164),
            ("#10", 0.190),
            ("1/4", 1 / 4),
            ("5/16", 5 / 16),
            ("3/8", 3 / 8),
            ("7/16", 7 / 16),
            ("1/2", 1 / 2),
            ("5/8", 5 / 8),
            ("3/4", 3 / 4),
            ("7/8", 7 / 8),
            ("1", 1),
        ):
            dia_m = RoundOff(OD * u("in"))
            s = Size("SHCS head height", sz, dia_m)
            d.append(s)
        # SHCS Allen hex wrench size, inch fasteners [TAD]
        for sz, OD in (
            ("#0", 0.05),
            ("#1", 1 / 16),
            ("#2", 5 / 64),
            ("#3", 5 / 64),
            ("#4", 3 / 32),
            ("#5", 3 / 32),
            ("#6", 7 / 64),
            ("#8", 9 / 64),
            ("#10", 5 / 32),
            ("1/4", 3 / 16),
            ("5/16", 1 / 4),
            ("3/8", 5 / 16),
            ("7/16", 3 / 8),
            ("1/2", 3 / 8),
            ("5/8", 1 / 2),
            ("3/4", 5 / 8),
            ("7/8", 3 / 4),
            ("1", 3 / 4),
        ):
            dia_m = RoundOff(OD * u("in"))
            s = Size("SHCS Allen wrench size", sz, dia_m)
            d.append(s)
        # Hex nut wrench size, inch fasteners [TAD]
        for sz, OD in (
            ("#0", 5 / 32),
            ("#1", 5 / 32),
            ("#2", 3 / 16),
            ("#3", 3 / 16),
            ("#4", 1 / 4),
            ("#5", 5 / 16),
            ("#6", 5 / 16),
            ("#8", 11 / 32),
            ("#10", 3 / 8),
            ("1/4", 7 / 16),
            ("5/16", 1 / 2),
            ("3/8", 9 / 16),
            ("7/16", 11 / 16),
            ("1/2", 3 / 4),
            ("5/8", 15 / 16),
            ("3/4", 9 / 8),
            ("7/8", 21 / 16),
            ("1", 3 / 2),
        ):
            dia_m = RoundOff(OD * u("in"))
            s = Size("Hex nut wrench size", sz, dia_m)
            d.append(s)
        # SPI pin gauge set
        for OD in range(61, 250):
            dia_m = RoundOff(OD / 1000 * u("in"))
            sz = "{:.3f}".format(OD / 1000)
            s = Size("SPI pin gauge (inches)", sz, dia_m)
            d.append(s)
        opts["sizes"] = d
        Sockets(opts)

    def Sockets(opts):
        """Add the measured diameters of my shop's sockets, bushings, etc. to
        the list.
        """
        d = []
        # Harbor Freight bushing set
        sizes = [
            # (nominal_size_string, actual_diameter_in_inches)
            ("7/8 x 47/64", 0.964),
            ("7/8 x 47/64", 0.734),
            ("13/16 x 11/16", 0.811),
            ("13/16 x 11/16", 0.675),
            ("7/16 x 3/8", 0.433),
            ("7/16 x 3/8", 0.368),
            ("1/2 x 7/16", 0.501),
            ("1/2 x 7/16", 0.436),
            ("15/16 x 13/16", 0.934),
            ("15/16 x 13/16", 0.792),
            ("3/4 x 5/8", 0.746),
            ("3/4 x 5/8", 0.647),
            ("11/16 x 39/64", 0.670),
            ("11/16 x 39/64", 0.592),
            ("5/8 x 9/16", 0.632),
            ("5/8 x 9/16", 0.550),
            ("9/16 x 1/2", 0.553),
            ("9/16 x 1/2", 0.490),
            ("1 x 55/64", 0.985),
            ("1 x 55/64", 0.827),
            ("1-1/16 x 15/16", 1.061),
            ("1-1/16 x 15/16", 0.896),
            ("1-3/16 x 1-1/16", 1.182),
            ("1-3/16 x 1-1/16", 1.038),
            ("1-1/4 x 1-1/8", 1.257),
            ("1-1/4 x 1-1/8", 1.107),
            ("1-1/8 x 1", 1.126),
            ("1-1/8 x 1", 0.966),
            ("1-5/16 x 1-3/16", 1.310),
            ("1-5/16 x 1-3/16", 1.158),
            ("1-3/8 x 1-1/4", 1.369),
            ("1-3/8 x 1-1/4", 1.202),
        ]
        name = "HF bushing"
        for sz, dia in sizes:
            dia_m = dia * u("inches")
            d.append(Size(name, sz, dia_m))
        # Harbor Freight bending fixture's dies
        sizes = [
            # (nominal_size_string, actual_diameter_in_inches)
            ("1-1/2", 1.489),
            ("1", 0.997),
            ("1-1/4", 1.239),
            ("1", 0.979),
            ("5/8", 0.625),
            ("1-3/4", 1.737),
            ("2", 1.996),
            ("2-1/2", 2.503),
            ("3", 3.008),
        ]
        name = "HF bending fixture dies"
        for sz, dia in sizes:
            dia_m = dia * u("inches")
            d.append(Size(name, sz, dia_m))
        # Sockets (all measured in mid-Sep 2015 with Mitutoyo 6" dial
        # calipers, Fowler 6" electronic calipers, and Mitutoyo 12" vernier
        # height gauge).
        nn = "(? brand)"
        if 1:
            # Longer names
            so, ch, ma, cr = "Snap-On", "Challenger", "Mac", "Craftsman"
            th, wr, wm, mt, sk = "Thorsen", "Wright", "Williams", "Matco", "SK"
            hf, ac, pr = "HF", "Action", "Proto"
            du, sx = "Duro", "Sunex"
        else:
            # Abbreviations
            so, ch, ma, cr = "SO", "Ch", "Mc", "Cr"
            th, wr, wm, mt, sk = "Th", "Wr", "Wm", "Mt", "SK"
            hf, ac, pr = "HF", "Ac", "Pr"
            du, sx = "Du", "Sx"
        sh, st, md, dp = "short skt", "std skt", "mid skt", "deep skt"
        shi, sti = "short impact skt", "std impact skt"
        mdi, dpi = "mid impact skt", "deep impact skt"
        # Number after 'sq' is size in 1/8 inches
        sq2, sq3, sq4, sq6 = [i + " sq dr" for i in ("1/4", "3/8", "1/2", "3/4")]
        if 1:  # 1/4 inch drive sockets
            sizes = [
                # (Brand, square_drive, type, nominal_size, dia_inches, len_inches)
                # **** 1/4 square drive ****
                (cr, sq2, st, "5/32", 0.452, 0.867),
                (so, sq2, st, "3/16", 0.478, 0.882),
                (so, sq2, st, "7/32", 0.479, 0.878),
                (so, sq2, st, "1/4", 0.478, 0.877),
                (so, sq2, st, "9/32", 0.478, 0.877),
                (so, sq2, st, "5/16", 0.478, 0.877),
                (so, sq2, st, "11/32", 0.494, 0.879),
                (so, sq2, st, "3/8", 0.540, 0.879),
                (so, sq2, st, "7/16", 0.603, 0.878),
                (so, sq2, st, "1/2", 0.676, 0.872),
                (so, sq2, st, "9/16", 0.740, 0.860),
                (so, sq2, st, "5/8", 0.824, 0.979),
                #
                (cr, sq2, dp, "3/16", 0.448, 1.988),
                (so, sq2, dp, "7/32", 0.447, 1.987),
                (so, sq2, dp, "1/4", 0.434, 1.980),
                (so, sq2, dp, "9/32", 0.478, 2.001),
                (so, sq2, dp, "5/16", 0.429, 1.985),
                (so, sq2, dp, "11/32", 0.495, 2.008),
                (so, sq2, dp, "3/8", 0.547, 1.992),
                (so, sq2, dp, "7/16", 0.620, 2.003),
                (so, sq2, dp, "1/2", 0.683, 1.988),
                (so, sq2, dp, "9/16", 0.740, 1.985),
                #
                (cr, sq2, st, "4 mm", 0.473, 0.834),
                (cr, sq2, st, "5 mm", 0.473, 0.840),
                (cr, sq2, st, "6 mm", 0.475, 0.837),
                (cr, sq2, st, "7 mm", 0.449, 0.876),
                (cr, sq2, st, "8 mm", 0.477, 0.840),
                (cr, sq2, st, "9 mm", 0.558, 0.824),
                (cr, sq2, st, "10 mm", 0.539, 0.869),
                (cr, sq2, st, "11 mm", 0.620, 0.844),
                (cr, sq2, st, "12 mm", 0.656, 0.837),
                (cr, sq2, st, "13 mm", 0.683, 0.883),
                #
                (so, sq2, dp, "5 mm", 0.476, 2.005),
                (so, sq2, dp, "5.5 mm", 0.477, 2.009),
                (so, sq2, dp, "6 mm", 0.479, 2.007),
                (so, sq2, dp, "7 mm", 0.477, 2.006),
                (so, sq2, dp, "8 mm", 0.478, 1.994),
                (so, sq2, dp, "9 mm", 0.501, 2.003),
                (so, sq2, dp, "10 mm", 0.549, 2.001),
                (so, sq2, dp, "11 mm", 0.604, 2.002),
                (so, sq2, dp, "12 mm", 0.650, 2.002),
                (so, sq2, dp, "13 mm", 0.693, 2.003),
                (so, sq2, dp, "14 mm", 0.740, 2.001),
                #
                # SK stuff in green metal box
                (sk, sq2, st, "4 mm", 0.469, 0.863),
                (sk, sq2, st, "5 mm", 0.469, 0.863),
                (sk, sq2, st, "5.5 mm", 0.471, 0.873),
                (sk, sq2, st, "6.35 mm", 0.472, 0.869),
                (sk, sq2, st, "8 mm", 0.472, 0.870),
                (sk, sq2, st, "9 mm", 0.502, 0.871),
                (sk, sq2, st, "10 mm", 0.563, 0.861),
                (sk, sq2, st, "11 mm", 0.627, 0.865),
                (sk, sq2, dp, "6 mm", 0.471, 1.994),
                (sk, sq2, dp, "6.35 mm", 0.472, 1.986),
                (sk, sq2, dp, "7 mm", 0.469, 1.997),
                (sk, sq2, dp, "8 mm", 0.470, 1.991),
                (sk, sq2, dp, "9 mm", 0.500, 1.995),
                (sk, sq2, dp, "10 mm", 0.552, 2.013),
                (sk, sq2, dp, "11 mm", 0.626, 2.010),
                #
                # Miscellaneous/no name stuff
                (ac, sq2, st, "1/4", 0.492, 0.987),
                (ac, sq2, st, "1/4sq", 0.490, 1.002),
                (ac, sq2, st, "5/16sq", 0.559, 0.993),
                (ac, sq2, st, "3/8sq", 0.619, 0.982),
                (so, sq2, st, "1/2", 0.677, 0.862),
                (so, sq2, st, "9/16", 0.743, 0.879),
                (nn, sq2, st, "15/32", 0.617, 0.783),
                (nn, sq2, st, "1/2", 0.662, 0.792),
                (nn, sq2, st, "7/16", 0.617, 0.785),
                (nn, sq2, st, "3/8", 0.541, 0.803),
                (nn, sq2, st, "11/32", 0.500, 0.794),
                (nn, sq2, st, "9/32", 0.464, 0.794),
                (nn, sq2, st, "1/4", 0.455, 0.762),
                (nn, sq2, st, "5/16", 0.462, 0.780),
                (pr, sq2, st, "12 mm", 0.621, 0.870),
                (ma, sq2, dp, "11/32", 0.551, 1.999),
            ]
        if 1:  # 3/8 inch drive sockets
            sizes.extend(
                [
                    (so, sq3, st, "1/4", 0.664, 0.913),
                    (so, sq3, st, "5/16", 0.664, 0.903),
                    (so, sq3, st, "3/8", 0.664, 0.908),
                    (so, sq3, st, "7/16", 0.658, 0.902),
                    (so, sq3, st, "1/2", 0.714, 0.934),
                    (so, sq3, st, "9/16", 0.772, 1.004),
                    (so, sq3, st, "5/8", 0.837, 1.038),
                    (so, sq3, st, "11/16", 0.927, 1.097),
                    (so, sq3, st, "3/4", 0.990, 1.111),
                    (so, sq3, st, "13/16", 1.077, 1.149),
                    (so, sq3, st, "7/8", 1.151, 1.150),
                    (ch, sq3, st, "15/16", 1.237, 1.318),
                    (ch, sq3, st, "1", 1.307, 1.373),
                    #
                    (so, sq3, dp, "7/16", 0.663, 2.120),
                    (so, sq3, dp, "1/2", 0.709, 2.125),
                    (so, sq3, dp, "9/16", 0.770, 2.379),
                    (so, sq3, dp, "5/8", 0.836, 2.377),
                    (so, sq3, dp, "11/16", 0.927, 2.637),
                    (so, sq3, dp, "3/4", 0.986, 2.627),
                    (so, sq3, dp, "13/16", 1.045, 2.744),
                    (so, sq3, dp, "7/8", 1.147, 2.750),
                    #
                    (ma, sq3, st, "6 mm", 0.683, 1.083),
                    (ma, sq3, st, "7 mm", 0.686, 1.097),
                    (ma, sq3, st, "8 mm", 0.680, 1.099),
                    (ma, sq3, st, "9 mm", 0.682, 1.090),
                    (cr, sq3, st, "10 mm", 0.656, 0.934),
                    (ma, sq3, st, "11 mm", 0.684, 1.101),
                    (ma, sq3, st, "12 mm", 0.680, 1.098),
                    (ma, sq3, st, "13 mm", 0.713, 1.087),
                    (ma, sq3, st, "14 mm", 0.776, 1.105),
                    (ma, sq3, st, "15 mm", 0.809, 1.104),
                    (ma, sq3, st, "16 mm", 0.876, 1.131),
                    (ma, sq3, st, "17 mm", 0.932, 1.106),
                    (ma, sq3, st, "18 mm", 0.987, 1.127),
                    (ma, sq3, st, "19 mm", 1.014, 1.090),
                    #
                    (cr, sq3, st, "9 mm", 0.656, 0.930),
                    (cr, sq3, st, "10 mm", 0.677, 1.023),
                    (th, sq3, st, "12 mm", 0.724, 1.005),
                    (cr, sq3, st, "13 mm", 0.702, 0.935),
                    (cr, sq3, st, "15 mm", 0.795, 0.965),
                    (cr, sq3, st, "17 mm", 0.897, 1.040),
                    (cr, sq3, st, "19 mm", 0.977, 1.031),
                    #
                    (cr, sq3, dp, "9 mm", 0.651, 2.492),
                    (cr, sq3, dp, "10 mm", 0.651, 2.514),
                    (cr, sq3, dp, "11 mm", 0.649, 2.496),
                    (cr, sq3, dp, "12 mm", 0.674, 2.504),
                    (cr, sq3, dp, "13 mm", 0.693, 2.502),
                    (cr, sq3, dp, "14 mm", 0.750, 2.492),
                    (cr, sq3, dp, "15 mm", 0.790, 2.502),
                    (cr, sq3, dp, "16 mm", 0.839, 2.495),
                    (cr, sq3, dp, "17 mm", 0.895, 2.505),
                    #
                    (sk, sq3, dp, "3/4", 0.992, 2.503),
                    (mt, sq3, dpi, "3/4", 1.060, 2.503),
                    #
                    (so, sq3, dpi, "9 mm", 0.679, 2.103),
                    (so, sq3, dpi, "10 mm", 0.679, 2.115),
                    (so, sq3, dpi, "11 mm", 0.679, 2.099),
                    (so, sq3, dpi, "12 mm", 0.708, 2.130),
                    (so, sq3, dpi, "13 mm", 0.769, 2.131),
                    (so, sq3, dpi, "14 mm", 0.803, 2.377),
                    (so, sq3, dpi, "15 mm", 0.831, 2.371),
                    (so, sq3, dpi, "16 mm", 0.895, 2.378),
                    (so, sq3, dpi, "17 mm", 0.958, 2.620),
                    (so, sq3, dpi, "18 mm", 0.988, 2.624),
                    (so, sq3, dpi, "19 mm", 1.050, 2.623),
                    #
                    (so, sq3, dpi, "3/8", 0.678, 2.109),
                    (so, sq3, dpi, "7/16", 0.740, 2.120),
                    (so, sq3, dpi, "1/2", 0.739, 2.129),
                    (so, sq3, dpi, "9/16", 0.805, 2.378),
                    (so, sq3, dpi, "5/8", 0.894, 2.382),
                    (so, sq3, dpi, "11/16", 0.959, 2.626),
                    (so, sq3, dpi, "3/4", 1.053, 2.620),
                    #
                    (mt, sq3, st, "3/8", 0.682, 1.028),
                    (mt, sq3, st, "7/16", 0.682, 1.026),
                    (mt, sq3, st, "1/2", 0.727, 1.026),
                    (mt, sq3, st, "9/16", 0.785, 1.002),
                    (mt, sq3, st, "5/8", 0.859, 1.014),
                    (mt, sq3, st, "11/16", 0.942, 1.061),
                    (mt, sq3, st, "3/4", 1.021, 1.102),
                    (mt, sq3, st, "13/16", 1.094, 1.134),
                    (mt, sq3, st, "7/8", 1.179, 1.140),
                    # Spark plug sockets
                    (sk, sq3, dp, "18 mm spk plug", 0.996, 2.365),
                    (so, sq3, dp, "13/16 spk plug", 1.050, 2.440),
                    (nn, sq3, dp, "13/16 spk plug", 1.069, 2.733),
                    (cr, sq3, dp, "5/8 spk plug", 0.868, 2.357),
                    #
                    # Miscellaneous/no name stuff
                    (pr, sq3, st, "1/4W", 0.774, 1.008),
                    (so, sq3, st, "7/16sq", 0.771, 0.996),
                    (so, sq3, st, "1/2sq", 0.869, 1.001),
                    (so, sq3, st, "9/16sq", 0.994, 1.117),
                    (so, sq3, st, "5/8sq", 1.052, 1.117),
                    (du, sq3, st, "11/16sq", 1.117, 1.466),
                    (pr, sq3, st, "3/4sq", 1.264, 1.499),
                ]
            )
        if 1:  # 1/2 inch drive sockets
            sizes.extend(
                [
                    (th, sq4, dp, "7/16", 0.866, 3.022),
                    (th, sq4, dp, "1/2", 0.870, 3.095),
                    (th, sq4, dp, "9/16", 0.866, 3.046),
                    #
                    (nn, sq4, dpi, "10 mm", 0.933, 3.025),
                    (nn, sq4, dpi, "11 mm", 0.932, 3.060),
                    (nn, sq4, dpi, "13 mm", 0.952, 3.075),
                    (nn, sq4, dpi, "14 mm", 0.928, 3.076),
                    (nn, sq4, dpi, "16 mm", 0.984, 3.068),
                    (nn, sq4, dpi, "17 mm", 1.036, 3.075),
                    (nn, sq4, dpi, "19 mm", 1.093, 3.080),
                    (nn, sq4, dpi, "21 mm", 1.166, 3.092),
                    (nn, sq4, dpi, "23 mm", 1.319, 3.082),
                    (nn, sq4, dpi, "24 mm", 1.300, 3.073),
                    #
                    (ch, sq4, st, "9/16", 0.878, 1.425),
                    (ch, sq4, st, "5/8", 0.862, 1.523),
                    (ch, sq4, st, "11/16", 0.933, 1.503),
                    (ch, sq4, st, "3/4", 1.050, 1.489),
                    (ch, sq4, st, "7/8", 1.176, 1.552),
                    (ch, sq4, st, "15/16", 1.235, 1.599),
                    (ch, sq4, st, "1", 1.303, 1.561),
                    (ch, sq4, st, "1-1/16", 1.426, 1.647),
                    (ch, sq4, st, "1-1/8", 1.494, 1.755),
                    (ch, sq4, st, "1-1/4", 1.617, 1.734),
                    #
                    (so, sq4, st, "3/8W", 0.992, 1.502),
                    (so, sq4, st, "7/8", 1.175, 1.512),
                    (so, sq4, st, "15/16", 1.269, 1.503),
                    (so, sq4, st, "1", 1.333, 1.508),
                    (so, sq4, st, "1-1/16", 1.421, 1.626),
                    (so, sq4, st, "1-1/8", 1.487, 1.747),
                    (so, sq4, st, "1-3/16", 1.600, 1.755),
                    (so, sq4, st, "1-1/4", 1.675, 1.880),
                    (so, sq4, st, "1-5/16", 1.734, 1.862),
                    (so, sq4, st, "1-3/8", 1.797, 2.063),
                    (so, sq4, st, "1-7/16", 1.922, 2.246),
                    (so, sq4, st, "1-1/2", 1.989, 2.234),
                    #
                    (wr, sq4, sti, "24 mm", 1.391, 1.701),
                    #
                ]
            )
        if 1:  # 3/4 inch drive sockets
            sizes.extend(
                [
                    (wm, sq6, st, "1-3/8", 1.875, 2.370),
                    (nn, sq6, st, "1-1/4", 1.768, 2.028),
                    (nn, sq6, st, "1-1/2", 2.039, 2.225),
                    #
                    # The following lengths were measured with a height gauge, as
                    # standard calipers for these big sockets doesn't work very well.
                    # Because of dings, bumps, etc., I estimate the length uncertainty
                    # at around 0.003 inches or so (i.e., bounded by a half-width of
                    # +/- 0.01 inches).
                    (hf, sq6, st, "19 mm", 1.425, 1.982),
                    (hf, sq6, st, "22 mm", 1.418, 1.992),
                    (hf, sq6, st, "24 mm", 1.389, 1.964),
                    (hf, sq6, st, "26 mm", 1.436, 1.981),
                    (hf, sq6, st, "27 mm", 1.466, 2.067),
                    (hf, sq6, st, "28 mm", 1.532, 2.052),
                    (hf, sq6, st, "30 mm", 1.616, 2.067),
                    (hf, sq6, st, "32 mm", 1.713, 2.252),
                    (hf, sq6, st, "34 mm", 1.835, 2.271),
                    (hf, sq6, st, "36 mm", 1.963, 2.396),
                    (hf, sq6, st, "38 mm", 2.012, 2.360),
                    (hf, sq6, st, "41 mm", 2.209, 2.495),
                    (hf, sq6, st, "42 mm", 2.220, 2.437),
                    (hf, sq6, st, "45 mm", 2.411, 2.560),
                    (hf, sq6, st, "46 mm", 2.419, 2.608),
                    (hf, sq6, st, "48 mm", 2.496, 2.824),
                    (hf, sq6, st, "50 mm", 2.640, 2.749),
                ]
            )
        in2m = u("inches")
        for brand, sqdr, tp, sz, dia, length in sizes:
            dia_m, length_m = dia * in2m, length * in2m
            name = "{} {} {},".format(brand, sqdr, tp)
            d.append(Size(name, sz, dia_m))
            d.append(Size("(length) " + name, sz, length_m))
        opts["sizes"].extend(d)

    def Renard(s):
        """Return the Renard series for s where s is one of R5, R10, R20,
        R40, R80, R'10, R'20, R'40, R"5, R"10, R"20.  The R' numbers are
        "medium rounded" and the R" numbers are "most rounded".

        See https://en.wikipedia.org/wiki/Renard_series.  Charles Renard
        proposed the system in 1877.  It was adopted in 1952 as standard
        ISO 3.

        The nominal formula for series with number n is 10**(i/n) for i from 0
        to n; the values need to be rounded and it's not a simple rounding
        algorithm.
        """
        d = {
            "R5": [1, 1.6, 2.5, 4, 6.3],
            "R10": [1, 1.25, 1.6, 2, 2.5, 3.15, 4, 5, 6.3, 8],
            "R20": [
                1,
                1.25,
                1.6,
                2,
                2.5,
                3.15,
                4,
                5,
                6.3,
                8,
                1.12,
                1.4,
                1.8,
                2.24,
                2.8,
                3.55,
                4.5,
                5.6,
                7.1,
                9,
            ],
            "R40": [
                1,
                1.25,
                1.6,
                2,
                2.5,
                3.15,
                4,
                5,
                6.3,
                8,
                1.06,
                1.32,
                1.7,
                2.12,
                2.65,
                3.35,
                4.25,
                5.3,
                6.7,
                8.5,
                1.12,
                1.4,
                1.8,
                2.24,
                2.8,
                3.55,
                4.5,
                5.6,
                7.1,
                9,
                1.18,
                1.5,
                1.9,
                2.36,
                3,
                3.75,
                4.75,
                6,
                7.5,
                9.5,
            ],
            "R80": [
                1,
                1.25,
                1.6,
                2,
                2.5,
                3.15,
                4,
                5,
                6.3,
                8,
                1.03,
                1.28,
                1.65,
                2.06,
                2.58,
                3.25,
                4.12,
                5.15,
                6.5,
                8.25,
                1.06,
                1.32,
                1.7,
                2.12,
                2.65,
                3.35,
                4.25,
                5.3,
                6.7,
                8.5,
                1.09,
                1.36,
                1.75,
                2.18,
                2.72,
                3.45,
                4.37,
                5.45,
                6.9,
                8.75,
                1.12,
                1.4,
                1.8,
                2.24,
                2.8,
                3.55,
                4.5,
                5.6,
                7.1,
                9,
                1.15,
                1.45,
                1.85,
                2.3,
                2.9,
                3.65,
                4.62,
                5.8,
                7.3,
                9.25,
                1.18,
                1.5,
                1.9,
                2.36,
                3,
                3.75,
                4.75,
                6,
                7.5,
                9.5,
                1.22,
                1.55,
                1.95,
                2.43,
                3.07,
                3.87,
                4.87,
                6.15,
                7.75,
                9.75,
            ],
            # Medium rounded
            "R'10": [1, 1.25, 1.6, 2, 2.5, 3.2, 4, 5, 6.3, 8],
            "R'20": [
                1,
                1.25,
                1.6,
                2,
                2.5,
                3.2,
                4,
                5,
                6.3,
                8,
                1.1,
                1.4,
                1.8,
                2.2,
                2.8,
                3.6,
                4.5,
                5.6,
                7.1,
                9,
            ],
            "R'40": [
                1,
                1.25,
                1.6,
                2,
                2.5,
                3.2,
                4,
                5,
                6.3,
                8,
                1.05,
                1.3,
                1.7,
                2.1,
                2.6,
                3.4,
                4.2,
                5.3,
                6.7,
                8.5,
                1.1,
                1.4,
                1.8,
                2.2,
                2.8,
                3.6,
                4.5,
                5.6,
                7.1,
                9,
                1.2,
                1.5,
                1.9,
                2.4,
                3,
                3.8,
                4.8,
                6,
                7.5,
                9.5,
            ],
            # Most rounded
            'R"5': [1, 1.5, 2.5, 4, 6],
            'R"10': [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8],
            'R"20': [
                1,
                1.2,
                1.5,
                2,
                2.5,
                3,
                4,
                5,
                6,
                8,
                1,
                1.2,
                1.5,
                2,
                2.5,
                3,
                4,
                5,
                6,
                8,
            ],
        }
        u = d[s]
        u.sort()
        return u

    def E_Series(n):
        e24 = [
            10,
            12,
            15,
            18,
            22,
            27,
            33,
            39,
            47,
            56,
            68,
            82,
            11,
            13,
            16,
            20,
            24,
            30,
            36,
            43,
            51,
            62,
            75,
            91,
        ]
        e192 = [
            100,
            121,
            147,
            178,
            215,
            261,
            316,
            383,
            464,
            562,
            681,
            825,
            101,
            123,
            149,
            180,
            218,
            264,
            320,
            388,
            470,
            569,
            690,
            835,
            102,
            124,
            150,
            182,
            221,
            267,
            324,
            392,
            475,
            576,
            698,
            845,
            104,
            126,
            152,
            184,
            223,
            271,
            328,
            397,
            481,
            583,
            706,
            856,
            105,
            127,
            154,
            187,
            226,
            274,
            332,
            402,
            487,
            590,
            715,
            866,
            106,
            129,
            156,
            189,
            229,
            277,
            336,
            407,
            493,
            597,
            723,
            876,
            107,
            130,
            158,
            191,
            232,
            280,
            340,
            412,
            499,
            604,
            732,
            887,
            109,
            132,
            160,
            193,
            234,
            284,
            344,
            417,
            505,
            612,
            741,
            898,
            110,
            133,
            162,
            196,
            237,
            287,
            348,
            422,
            511,
            619,
            750,
            909,
            111,
            135,
            164,
            198,
            240,
            291,
            352,
            427,
            517,
            626,
            759,
            920,
            113,
            137,
            165,
            200,
            243,
            294,
            357,
            432,
            523,
            634,
            768,
            931,
            114,
            138,
            167,
            203,
            246,
            298,
            361,
            437,
            530,
            642,
            777,
            942,
            115,
            140,
            169,
            205,
            249,
            301,
            365,
            442,
            536,
            649,
            787,
            953,
            117,
            142,
            172,
            208,
            252,
            305,
            370,
            448,
            542,
            657,
            796,
            965,
            118,
            143,
            174,
            210,
            255,
            309,
            374,
            453,
            549,
            665,
            806,
            976,
            120,
            145,
            176,
            213,
            258,
            312,
            379,
            459,
            556,
            673,
            816,
            988,
        ]
        e24.sort()
        e192.sort()
        e24 = [RoundOff(i / 10) for i in e24]
        e192 = [RoundOff(i / 100) for i in e192]
        if n == 6:
            return e24[::2][::2]
        elif n == 12:
            return e24[::2]
        elif n == 24:
            return e24
        elif n == 48:
            return e192[::2][::2]
        elif n == 96:
            return e192[::2]
        elif n == 192:
            return e192
        else:
            raise ValueError("'{}' is bad n value".format(n))


if 1:  # Core functionality

    def ImproperFraction(f):
        """Return a string form of an improper faction."""
        if ii(f, int):
            return str(f)
        if not ii(f, Fraction):
            raise TypeError("Argument must be an integer or Fraction")
        if f.numerator < f.denominator:
            return str(f)
        ip, remainder = divmod(f.numerator, f.denominator)
        return "{}-{}/{}".format(ip, remainder, f.denominator)

    def Check(seq, neg_slope=True):
        """If Check.debug is True, check that the sequence is monotonic (used
        to detect typing errors).
        """
        if not Check.debug:
            return seq
        for i, num in enumerate(seq):
            if not num or not i:
                continue
            if neg_slope and seq[i - 1]:
                if num >= seq[i - 1]:
                    msg = str(num) + " is >= " + str(seq[i - 1])
                    raise ValueError(msg)
            else:
                if num <= seq[i - 1]:
                    msg = str(num) + " is <= " + str(seq[i - 1])
                    raise ValueError(msg)
        return seq

    def Search(dia_in_m, d):
        """Return a sorted container of all the sizes that match the indicated
        diameter.
        """
        found = []
        for sz in d["sizes"]:
            if sz.within(dia_in_m):
                found.append(sz)
        found.sort()
        return found

    def DimensionlessNumbers():
        """Return a list of the dimensionless numbers.  Note they'll be Size
        objects.
        """
        d = []
        # Renard numbers
        for series, name in (
            ("R5", "Renard 5"),
            ('R"5', 'Renard 5"'),
            ("R10", "Renard 10"),
            ("R'10", "Renard 10'"),
            ('R"10', 'Renard 10"'),
            ("R20", "Renard 20"),
            ("R'20", "Renard 20'"),
            ('R"20', 'Renard 20"'),
            ("R40", "Renard 40"),
            ("R'40", "Renard 40'"),
            ("R80", "Renard 80"),
        ):
            for i in Renard(series):
                sz = Size(name, str(i), i)
                d.append(sz)
        # E-series numbers
        for n in (6, 12, 24, 48, 96, 192):
            for i in E_Series(n):
                sz = Size("E{} series".format(n), str(i), i)
                d.append(sz)
        # Binary factors
        for i in range(17):
            n = 2**i
            s = str(n)
            ip, fp = s[0], s[1:]
            descr = ip + "." + fp if fp else ip
            val = int(ip) + int(fp) / 10 ** len(fp) if fp else int(ip)
            sz = Size("Power of 2:  2**{} = {} -->".format(i, n), descr, val)
            d.append(sz)
        # Square roots of 2
        sr2 = sqrt(2)
        for i in range(1, 11):
            val = i * sr2
            while val > 10:
                val /= 10
            val = round(val, 5)
            sz = Size("sqrt(2)**{}".format(i), str(val), val)
            d.append(sz)
        return d

    def Dimensionless(value, d):
        """value is a dimensionless number.  Get its exponent and significand
        and print dimensionless numbers that are close to it.
        """
        u = "{:.15e}".format(abs(value))
        s, e = u.split("e")
        exponent = int(e)
        significand = RoundOff(float(s))
        assert 1 <= significand <= 10
        # Build a list of the dimensionless numbers
        d["sizes"] = DimensionlessNumbers()
        # Find matches
        found = Search(significand, d)
        # Print report
        tolerance = d["-t"]
        print(
            dedent(f"""
        Search for dimensionless number = {value}
        Significand = {significand}
        Search tolerance = {tolerance}%
        Found values:""")
        )
        # Get maximum size of size strings
        maxsz = 0
        for item in found:
            maxsz = max(maxsz, len(str(RoundOff(item.dia))))
        # Now print
        for item in found:
            sz = RoundOff(item.dia)
            print("  ", "{0:{1}}".format(str(sz), maxsz), end=" " * 4)
            print(item.category)
        exit()

    def Report(value, unit, d):
        """Print a report of the nearest numbers."""
        if d["-d"]:
            Dimensionless(value, d)
            return
        if d["-a"]:
            ShowAll(d)
            return
        dia_in_m = value * u(unit)
        found = Search(dia_in_m, d)
        to_output_units = 1 / u(unit)
        print("Size searched for =", value, unit)
        if d["-o"] is not None:
            print("  Output units are", d["-o"])
            to_output_units = 1 / u(d["-o"])
            print("  Size =", RoundOff(dia_in_m * to_output_units), d["-o"])
        print(f"Matches within {d['-t']}%:")
        # Get maximum size of size strings
        maxsz = 0
        for item in found:
            sz = StringForm(item.dia * to_output_units, d)
            maxsz = max(maxsz, len(sz))
        # Now print
        sig.sign = True
        for item in found:
            dev = (item.dia - dia_in_m) / dia_in_m
            sgn = +1 if dev >= 0 else -1
            pct_deviation = 100 * abs(dev)
            if pct_deviation < 1e-6:
                pct_deviation = 0
            pct_deviation *= sgn
            sz = StringForm(item.dia * to_output_units, d)
            item.color()
            print(f"  {sz:{maxsz}s}", end=" " * 4)
            print(" " if pct_deviation else "*", end=" ")
            print(item.category, item.size, end=" ")
            if pct_deviation:
                c = t("redl") if pct_deviation < 0 else t("grnl")
                s = sig(pct_deviation, 2)
                print(f"{c}[{s}%]")
            else:
                print()
            if 1:
                print(t.n, end="")
            else:
                c.normal()

    def ShowAll(d):
        if d["-d"]:
            # Show the dimensionless numbers
            for sz in sorted(DimensionlessNumbers()):
                print("  {:<25} {} {}".format(sz.dia, sz.category, sz.size))
        else:
            unit = d["-o"] if d["-o"] is not None else d["-u"]
            to_output_units = 1 / u(unit)
            all = d["sizes"]
            all.sort()
            unit = "inches" if d["-o"] is None else d["-o"]
            print("All sizes available to script ({}):".format(unit))
            # Get maximum size of size strings
            maxsz = 0
            for item in all:
                sz = StringForm(item.dia * to_output_units, d)
                maxsz = max(maxsz, len(sz))
            for item in all:
                dia = StringForm(item.dia * to_output_units, d)
                # dia = str(int(dia)) if "." not in dia else dia
                if d["-c"]:
                    item.color()
                print("  {0:{1}} {2} {3}".format(dia, maxsz, item.category, item.size))
                if d["-c"]:
                    if 1:
                        print(t.n, end="")
                    else:
                        c.normal()

    def StringForm(number, d):
        """Return the string form of the number rounded to the indicated number
        of significant figures.
        """
        val = RoundOff(SignificantFigures(number, d["-n"]))
        s = str(val)
        # Remove trailing zeros
        while s[-1] == "0":
            s = s[:-1]
        # Remove a trailing decimal point
        if s[-1] == ".":
            s = s[:-1]
        return s

    def ShowSockets(d):
        all = d["sizes"]
        all.sort()
        unit = "inches" if d["-o"] is None else d["-o"]
        print("Sockets:")
        for sz in all:
            dia = RoundOff(sz.dia / u(unit))
            dia = int(dia) if int(dia) == dia else dia
            if d["-c"]:
                sz.color()
            if " skt" in sz.category:
                print("  {:<25} {} {}".format(dia, sz.category, sz.size))
            if d["-c"]:
                if 1:
                    print(t.n, end="")
                else:
                    c.normal()


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    full = d["-f"]
    GetData(d)
    if d["-a"]:
        ShowAll(d)
    elif d["-k"]:
        ShowSockets(d)
    else:
        cmd = " ".join(args)
        dia, unit = ParseUnit(cmd, allow_expr=True)
        if not unit:
            unit = d["-u"]
        value = eval(dia, globals())
        if d["-s"]:
            value = float(value) * (1 - d["-s"] / 100)
        Report(RoundOff(float(value)), unit, d)
