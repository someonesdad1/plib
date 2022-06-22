'''
- Water properties (density and dynamic viscosity as functions of
  temperature).
- Colebrook correlation
- Darcy friction factor
- ParseUnit:  get a number and optional unit; the number can also
  contain uncertainty if the python uncertainties library is installed.

'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Water properties, Darcy friction factor
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import sys
        import math
        import re
        from functools import partial
    # Custom imports
        from u import u, fromto
        from wrap import wrap, dedent
        from color import Color, TRM as t
        import f as F
        # Import the python uncertainties library if it is available.
        _have_unc = False
        try:
            _pi = math.pi
            import uncertainties as unc
            import uncertainties.umath as math
            math.pi = _pi
            del _pi
            _have_unc = True
        except ImportError:
            pass
    # Global variables
        ii = isinstance
        __all__ = [
            "Colebrook",
            "FrictionFactor",
            "GetQuantity",
            "ParseUnit",
            "ShowPipeRoughness",
            "ShowUSPipeSizes",
            "WaterDensity",
            "WaterDynamicViscosity",
        ]
        # Regular expression that will match an integer or floating point
        # number in its string representation.
        num_regexp = re.compile(r'''
                ^                       # Must match at beginning
                (                       # Group
                    [+-]?               # Optional sign
                    \.\d+               # Number like .345
                    ([eE][+-]?\d+)?|    # Optional exponent
                # or
                    [+-]?               # Optional sign
                    \d+\.?\d*           # Number e.g. 2.345 or 2345
                    ([eE][+-]?\d+)?     # Optional exponent
                )                       # End group
        ''', re.X)
        # Colors
        ia = sys.stdout.isatty()
        t.ti = t("ornl") if ia else ""
        t.so = t("trq") if ia else ""
        t.nn = t.n if ia else ""
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
    def _ParseUnit(s, allow_unc=False):
        '''Separate a number string followed by a unit string and return them
        as a tuple (F.flt, unit_string).  If the uncertainties library is
        present and s contains '+/-', '+-', or '(' and ')' (indicating a
        short form uncertainty), then s will be a UFloat object.
        
        Examples:
            ParseUnit("47.3e-88m/s") and ParseUnit("47.3e-88 m/s") both
            return (4.73e-87, 'm/s').
    
            ParseUnit("47.3e-88*1.23 m/s") returns ("47.3e-88*1.23", "m/s").
            ParseUnit("4") returns (4.0, "").
            ParseUnit("4+/-1 m") returns (ufloat(4, 1), "m").
        '''
        if allow_unc and not _have_unc:
            raise ValueError("uncertainties library not available")
        s = s.strip()
        # We allow the string "+-" to represent "+/-" (this is an
        # enhancement to the uncertainties package's syntax).
        s = s.replace("+-", "+/-")
        is_unc = "+/-" in s or ("(" in s and ")" in s)
        f = s.split()
        if allow_unc and is_unc:
            if len(f) not in (1, 2):
                raise ValueError("s is not a proper string")
            try:
                x = unc.ufloat_fromstr(f[0])
            except Exception:
                raise ValueError("Cannot parse '{}'".format(f[0]))
            u = f[1] if len(f) == 2 else ""
            return (x, u)
        else:
            if is_unc:
                raise ValueError("Uncertainties not allowed in string")
            mo = num_regexp.search(s)
            if mo:
                x, unit = s[:mo.end()].rstrip(), s[mo.end():].lstrip()
                y = F.flt(x)
                return (y, unit)
            return None
    if _have_unc:
        ParseUnit = partial(_ParseUnit, allow_unc=True)
    else:
        ParseUnit = _ParseUnit
    ParseUnit.__doc__ = _ParseUnit.__doc__
    def RecommendedFluidVelocities():
        print(dedent(f'''
                  {t.ti}Recommended fluid velocities in m/s{t.nn}
        Application                                 Velocity        Ref.
        -----------------------------------         --------        ---
        Tap water, low noise                        0.5-0.7          1
        Tap water                                   1-2.5            1
        Cooling water                               1.5-2.5          1
        Heating water circulation                   1-3              1
        Hydraulic oil, suction/intake               0.6-1.2          2
                                                    0.6-2.4          3
        Hydraulic oil, return lines                 1.5-4            2
                                                    3-4.5            3
        Hydraulic oil, high pressure supply lines   2-5.5            2
                                                    < 10             3
        Fluids with dynamic viscosity <= 10 mPa*s   0.9-4.5          3
        Irrigation water                            1.5              5
        Gravity-fed water system (various sources)  1

        {t.so}References:{t.nn}
            1.  http://www.engineeringtoolbox.com/flow-velocity-water-pipes-d_385.html
            2.  http://4wings.com/tip/vpdp.html
            3.  http://www.sidenereng.com/formulas.php
            4.  http://www.mycheme.com/recommended-pipeline-velocities/
            5.  Univ. of Washington
                http://irrigation.wsu.edu/Content/Select-Calculators.php (I can't
                find the original page on which I found this recommendation)
            6.  http://asahi-america.com/images/x-assets/PDF/engineer_theory.pdf
        '''[:-1]))
    def ShowUSPipeSizes():
        print(dedent('''
        US Pipe Sizes
                Schedule 40 PVC pipe                    Schedule 80 PVC pipe
          Nominal                                 Nominal
           Size      OD      Wall      ID          Size      OD      Wall      ID
          -------   -----    -----    -----       -------   -----    -----    -----
           1/2      0.840    0.109    0.622        1/2      0.840    0.147    0.546
           3/4      1.050    0.113    0.824        3/4      1.050    0.154    0.742
           1        1.315    0.133    1.049        1        1.315    0.179    0.957
           1-1/4    1.660    0.140    1.380        1-1/4    1.660    0.191    1.278
           1-1/2    1.900    0.145    1.610        1-1/2    1.900    0.200    1.500
           2        2.375    0.154    2.067        2        2.375    0.218    1.939
                              PVC roughness is 1.5-7 μm
         
          Schedule 40 steel pipe
          ----------------------
              Taper = 3/4 per foot on diameter
                    = 1 deg 47' [1.783 deg = atan(3/(4*12*2))] wrt centerline
              Taper = 1 in 16 on diameter = 3.576 deg = 2*atan(1/32)
              PD measured at start of external thread
              Roughness is about 45 μm
         
          Nominal
          Pipe        Pipe     Pipe                      Thread       Pitch
          Size         OD       ID      Wall   tpi       Pitch       diameter
          -----       ------   ------  -----   ---       ------      --------
          1/8         0.405    0.269   0.070   27        0.0370       0.364
          1/4         0.540    0.364   0.090   18        0.0556       0.477
          3/8         0.675    0.493   0.090   18        0.0556       0.612
          1/2         0.840    0.622   0.109   14        0.0714       0.758
          3/4         1.050    0.824   0.113   14        0.0714       0.968
          1           1.315    1.049   0.133   11.5      0.0870       1.214
          1 1/4       1.660    1.380   0.140   11.5      0.0870       1.557
          1 1/2       1.900    1.610   0.145   11.5      0.0870       1.796
          2           2.375    2.067   0.154   11.5      0.0870       2.269
          2 1/2       2.875    2.469   0.203   8         0.1250       2.720
          3           3.500    3.068   0.216   8         0.1250       3.341
          3 1/2       3.000    3.548   0.226   8         0.1250       3.838
          4           4.500    4.026   0.237   8         0.1250       4.334
          5           5.563    5.047   0.258   8         0.1250       5.391
          6           6.625    6.065   0.280   8         0.1250       6.446
    '''[1:-1]))
    def GetQuantity(s, err="'{}' isn't a number with optional unit", dim=None):
        '''From the string s, return either a F.flt or ufloat converted
        to base SI units.  err is used to provide an error message.  If dim
        is given, it must be a unit string; the unit parsed from s must have
        the same dimensions.
     
        Examples:
          GetQuantity("1.2") --> 1.2
          GetQuantity("1.2 in") --> 0.030479999999999997
          The following all return 0.0305+/-0.0025:
              GetQuantity("1.2+-0.1 in")
              GetQuantity("1.2+/-0.1 in")
              GetQuantity("1.2(1) in")
        '''
        try:
            q, unit = ParseUnit(s)
            conv = 1
            if unit:
                conv = u(unit)
                if conv is None:
                    raise ValueError(f"The unit in {s!r} is not recognized")
                if dim:
                    try:
                        if u.dim(unit) != u.dim(dim):
                            raise TypeError(f"The unit in {s!r} does not have dimensions {dim!r}")
                    except TypeError:
                        raise
                    except Exception:
                        raise ValueError("The unit in {s!r} is not recognized")
            if isinstance(q, str):
                return F.flt(q)*conv
            else:
                return q*conv       # q is a ufloat
        except TypeError:
            raise
        except Exception:
            raise ValueError(err.format(s))
    def ShowPipeRoughness():
        print(dedent(f'''
                            {t.ti}Pipe roughness{t.nn}
                    Pipe type                   Roughness, um
        -----------------------------------     -------------
        Cast iron, new                          250-800
        Cast iron, worn                         800-1600
        Cast iron, rusty                        1500-2500
        Cast iron, asphalted                    10-15
        Cement, smoothed                        300
        Concrete, ordinary                      300-1000
        Concrete, coarse                        300-5000
        Copper, lead, brass, aluminum (new)     1.5-10
        Epoxy, vinyl ester, esophthalic         5
        Fiberglass                              5
        PVC and plastic pipes                   1.5-10
        Rubber tubing, smooth                   6-70
        Steel, commercial pipe                  45-90
        Steel, cold-finished                    15
        Steel, welded                           45
        Steel, galvanized                       150
        Steel, riveted                          900-9000
        Steel, slight corrosion                 50-150
        Steel, moderate corrosion               150-1000
        Steel, severe corrosion                 1000-4000
        Steel, stainless                        15
        Wood, well-planed                       180-900
        Wood, ordinary                          5000
  
        {t.so}Sources:{t.nn}
            http://www.engineeringtoolbox.com/major-loss-ducts-tubes-d_459.html
            http://www.enggcyclopedia.com/2011/09/absolute-roughness/
            http://www.efunda.com/formulae/fluids/roughness.cfm 
            http://www.pumpfundamentals.com/download-free/pipe_rough_values.pdf
            https://neutrium.net/fluid_flow/absolute-roughness/ 
        '''[:-1]))
    def _Interpolate(T_C, A, scl):
        '''A is an array from 0 to 100.  Linearly interpolate for the
        temperature in °C T_C.  scl is the number to scale the interpolated
        value by.  See use in WaterDensity() to get water's density.
        '''
        # This function is particular to the functions for water density and
        # viscosity.
        assert(len(A) == 101)
        if not (0 <= T_C <= 100):
            raise ValueError(f"'{T_C}' is an out-of-range temperature")
        if T_C == 100:
            return F.flt(A[100]*scl)
        else:
            try:
                i = int(T_C)
            except TypeError:
                i = int(T_C.nominal_value)
            a0, a1 = A[i], A[i + 1]
            if T_C == i:
                return F.flt(a0*scl)
            return F.flt((a0 + (T_C - i)*(a1 - a0))*scl)
    def WaterDensity(T_C):
        '''Return the water density in kg/m3 for water at a temperature of
        T_C degrees C.  Data from http://webbook.nist.gov/chemistry/fluid,
        downloaded 28 Mar 2016 09:38:09 AM.  NIST doesn't specify the
        accuracy of their data.
        '''
        # The array's first and last points are for 0 degC and 100 degC.
        # These extreme points are taken from pg 3-71 of Perry, "Chemical
        # Engineer's Handbook", 5th ed., 1973; Perry's data in turn are
        # taken from "Smithsonian Physical Tables", 9th revised edition,
        # 1954.  Perry's table gives the density of water at 4 degC as 1
        # g/ml to 8 significant figures.  The corresponding NIST value in
        # the array below is 0.999975 g/ml.  The discrepancy is probably
        # related to small changes in the Celsius temperature scale.  See
        # https://en.wikipedia.org/wiki/International_Temperature_Scale_of_1990.
        # For practical pipe calculations, these differences are irrelevant,
        # as 2 to 3 digits are at best typically significant.
        return _Interpolate(T_C, WaterDensity.rho, 1e-3)
    WaterDensity.rho = (  # Multiply by 1e-3 to get kg/m3
        999868, 999902, 999943, 999967, 999975, 999967, 999943, 999904,
        999851, 999784, 999702, 999608, 999500, 999380, 999247, 999103,
        998946, 998778, 998599, 998408, 998207, 997995, 997773, 997541,
        997299, 997048, 996786, 996516, 996236, 995947, 995649, 995343,
        995028, 994705, 994373, 994033, 993685, 993330, 992966, 992595,
        992216, 991830, 991437, 991036, 990628, 990213, 989791, 989362,
        988926, 988484, 988035, 987579, 987117, 986649, 986174, 985693,
        985206, 984712, 984213, 983707, 983196, 982678, 982155, 981626,
        981091, 980551, 980005, 979453, 978896, 978333, 977765, 977191,
        976612, 976028, 975438, 974843, 974243, 973637, 973027, 972411,
        971790, 971165, 970534, 969898, 969257, 968611, 967961, 967305,
        966645, 965980, 965310, 964635, 963955, 963271, 962582, 961888,
        961189, 960486, 959778, 959066, 958380)
    def WaterDynamicViscosity(T_C):
        '''Return the dynamic viscosity of water in Pa*s for T_C, the
        temperature in degrees C.  Data from
        http://webbook.nist.gov/chemistry/fluid downloaded 28 Mar 2016
        09:38:09 AM.  NIST doesn't specify the accuracy of their data.
        '''
        # The array's first and last points are for 0 degC and 100 degC (and
        # are taken from other places on the web, not the NIST data).
        return _Interpolate(T_C, WaterDynamicViscosity.Mu, 1e-8)
    WaterDynamicViscosity.Mu = (  # Multiply by 1e-8 to get Pa*s
        178700, 173090, 167340, 161890, 156720, 151810, 147140, 142700,
        138470, 134440, 130590, 126910, 123400, 120039, 116830, 113750,
        110810, 107979, 105270, 102659, 100160, 97755, 95442, 93216, 91073,
        89008, 87018, 85099, 83248, 81460, 79735, 78067, 76456, 74898,
        73390, 71932, 70519, 69152, 67827, 66543, 65298, 64090, 62918,
        61782, 60678, 59607, 58564, 57554, 56571, 55615, 54685, 53779,
        52899, 52044, 51210, 50398, 49607, 48836, 48085, 47353, 46640,
        45944, 45265, 44603, 43957, 43326, 42710, 42109, 41523, 40949,
        40389, 39842, 39307, 38785, 38274, 37774, 37285, 36807, 36340,
        35882, 35435, 34997, 34568, 34148, 33737, 33334, 32940, 32553,
        32175, 31804, 31441, 31085, 30735, 30393, 30057, 29728, 29405,
        29088, 28778, 28473, 28219)
    def Colebrook(D, Re, eps, rel_diff=1e-6):
        '''Returns the Darcy friction factor f for a pipe flow situation
        where D is the pipe diameter, eps is the pipe's roughness, and Re is
        the Reynolds number.  

        The Colebrook equation is an implicit phenomenological equation
        that fits the experimental data of turbulent flow in pipes.  Its
        functional form is 

            a = log(eps/D + a/Re)

        where a is 1/sqrt(f), D is the hydraulic diameter, and Re is the
        Reynolds number, assumed > 4000.  Note numerical constants were
        left out in this expression.
     
        The Colebrook equation is put into a form suitable for iteration;
        practical problems will take 2 to 5 iterations.  Stop iterating when
        the relative difference is less than rel_diff.  It doesn't make
        practical sense to try for more than 2 significant figures in f.
        Because of this, the F.flt type is used for calculations from the
        /plib/f.py module and these numbers use 3 significant figures by
        default for string interpolation.
        '''
        assert(Re >= 4000)
        # Initial estimate from the Haaland equation
        f0 = F.flt(1/(-1.8*F.log10((eps/(3.7*D))**1.11 + 6.9/Re))**2)
        count = 0
        while count <= 50:
            count += 1
            f = F.flt(0.25/(F.log10(eps/(3.7*D) + 2.51/(Re*F.sqrt(f0))))**2)
            if abs((f - f0)/f0) < rel_diff:
                if not (0.001 <= f <= 1):
                    raise ValueError(f"Friction factor of {f} is outside practical bounds")
                return f
            f0 = f
        raise ValueError("Exceeded allowed number of iterations")
    def FrictionFactor(D, Re, eps, rel_diff=1e-6):
        '''Calculate the Darcy friction Factor for turbulent flow in a completely
        full pipe.  The input variables are:
            D   = hydraulic diameter.  For round pipe, it's the inside
                  diameter. (length units)
            Re  = Reynolds number (dimensionless)
            eps = pipe's roughness (length units)
        Examples:
            FrictionFactor(1, 1e6, 0.01) = 0.038
            FrictionFactor(1, 1e4, 0.1) = 0.10
        '''
        assert(Re > 0)
        assert(D > 0)
        assert(rel_diff > 0)
        assert(eps >= 0)
        if eps > D:
            raise ValueError(f"eps = {F.flt(eps)} m is larger than pipe diameter")
        re1, re2, lam = 2300, 4000, lambda Re: 64/Re
        if Re < re1:                # Laminar flow
            return F.flt(lam(Re))
        elif re1 <= Re < re2:       # Transition flow
            # Linearly interpolate between the laminar and turbulent flow
            # values using Re as the independent variable.
            f1, f2 = lam(re1), Colebrook(D, re2, eps, rel_diff=rel_diff)
            return F.flt((f2 - f1)*(Re - re1)/(re2 - re1) + f1)
        else:                       # Turbulent flow
            return F.flt(Colebrook(D, Re, eps))
if __name__ == "__main__":
    from lwtest import run, raises, assert_equal, Assert
    def TestFrictionFactor():
        x = F.flt(0)
        x.n = 2
        Assert(str(FrictionFactor(1, 1e6, 0.01)) == "0.038")
        Assert(str(FrictionFactor(1, 1e4, 0.1)) == "0.10")
    def TestParseUnit():
        # No unit
        x, u = ParseUnit("0")
        Assert(x == 0)
        Assert(ii(x, F.flt))
        Assert(u == "")
        # With float
        a = 4.73e-87, 'm/s'
        b = ParseUnit("47.3e-88m/s")
        Assert(a == b)
        Assert(ii(b[0], F.flt))
        b = ParseUnit("47.3e-88 m/s")
        Assert(a == b)
        Assert(ii(b[0], F.flt))
        # With uncertainties
        if _have_unc:
            a = "4.73(2) m/s"
            b, c = ParseUnit(a)
            Assert(b.nominal_value == 4.73)
            Assert(b.std_dev == 0.02)
            Assert(c == "m/s")
    def TestGetQuantity():
        x = GetQuantity("1.2")
        Assert(x == 1.2)
        Assert(ii(x, F.flt))
        x = GetQuantity("1.2 in")
        Assert(x == 0.030479999999999997)
        Assert(ii(x, F.flt))
        # With uncertainties
        if _have_unc:
            s = "0.0305+/-0.0025"
            x = GetQuantity("1.2+-0.1 in")
            Assert(str(x) == s)
            x = GetQuantity("1.2+/-0.1 in")
            Assert(str(x) == s)
            x = GetQuantity("1.2(1) in")
            Assert(str(x) == s)
    def TestWaterDensity():
        a = WaterDensity(0)
        Assert(a == 999.868)
        Assert(ii(a, F.flt))
        #
        a = WaterDensity(4)
        Assert(a == 999.975)
        Assert(ii(a, F.flt))
        #
        a = WaterDensity(100)
        Assert(a == 958.380)
        Assert(ii(a, F.flt))
        #
        raises(ValueError, WaterDensity, -0.001)
        raises(ValueError, WaterDensity, 100.001)
    def TestWaterDynamicViscosity():
        a = WaterDynamicViscosity(0)
        c = 1e-8
        Assert(a == 178700*c)
        Assert(ii(a, F.flt))
        #
        a = WaterDynamicViscosity(4)
        Assert(a == 156720*c)
        Assert(ii(a, F.flt))
        #
        a = WaterDynamicViscosity(100)
        Assert(a == 28219*c)
        Assert(ii(a, F.flt))
        #
        raises(ValueError, WaterDynamicViscosity, -0.001)
        raises(ValueError, WaterDynamicViscosity, 100.001)
    def TestNumberRegexp():
        for s in '''0 0.e0 0.0e1 1 -1 0. -0. 0.0 -0.0 -1. -1.0 .1 -.1
            3.14159260937538957393874397534739472390
            -3.14159260937538957393874397534739472390
            3.14159260937538957393874397534739472390e3953503375
            -3.14159260937538957393874397534739472390e-3953503375
            '''.split():
            mo = num_regexp.match(s)
            Assert(mo)
        for s in "a0 a0e3 .a a.a".split():
            mo = num_regexp.match(s)
            Assert(not mo)
    exit(run(globals(), halt=True)[0])
