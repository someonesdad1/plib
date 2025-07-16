'''

ToDo
    - Use termtables to print output reports
        - Colorize units:  mm: blu, inch: yel
    - For interactive use, print results then prompt for new output units & steps
    - Look at using g.x global variables instead of those in dict d
    - Support uncertainity in the bucket measurements
    - Supply a formatting option for the output length measurements.  I usually use my
      metric tape measure and the practical limit of marking with an ultrafine Sharpie
      is about 1 mm.  Thus, I'd want to specify ".0f" as the formatting spec.  Or, this
      can be an integer for the round() function.
        - Default behavior:  mm rounds to nearest mm, inch rounds to 0.05 inches

Print out volume calibration marks for a bucket
    See the bucket.pdf document for a derivation of the formula used.
    Run with the -h option to see a help statement (the default behavior
    is to prompt you for the needed variables).
    
    28 Oct 2023:  I removed the dependency on the sig module and instead
    used f.flt objects.  I set the default number of displayed figures at
    4, as few applications can use more figures without precision measuring
    equipment.
    
    19 Feb 2012 Validation data using Nalgene 1000 ml graduated
    cylinder.  These tests were done carefully and are probably at
    around 0.5% uncertainty levels.
    
    - Ropak 4 gallon cat litter square bucket:  (inches)
        D=9.10, d=8.16, h=13, r=1.25, offset=0.12
        
      Measured 5 liters into bucket, water level at 118 mm from bottom;
      program calculates 117.3.  Measured 9 liters into bucket, water
      level at 201 mm from bottom; program calculates 202.8 mm.
      
    - Rheem 5 gallon round bucket:  (inches) D=11.34, d=10.42, h=14,
      offset=0.47.
        Measured, liters    Actual distance, mm     Program calculates, mm
        ----------------    -------------------     ----------------------
               5                    103.5                   100.9
              10                    186.5                   186.2
              15                   267-268                  268.1
              
      The 15 liter actual distance was a bit hard to measure, as a rib
      of the bucket was in the way, disguising where the water level
      was.
      
    I used a flashlight inside the bucket to illuminate the water level and
    then measured the height of the water level up the side from the
    countertop with either a machinist's rule or a Starrett tape measure
    calibrated in mm.  Estimated length uncertainty is 0.25 mm.
    
    Comment:  I made these measurements carefully and this demonstrated
    to me that the script produces correct results (this wasn't an
    experimental goal, as the formula itself is exact).  However, real
    molded buckets are not geometrically perfect and exhibit e.g.
    elliptical or other shapes when you measure them carefully.  Thus,
    you should probably expect your calibration marks be, at best, one
    to a few percent within the correct values.  If you need better than
    this, find a smaller container of known unit volume and use it to
    calibrate the marks on the larger bucket.
    
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2012 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Calculate volume calibration marks for a bucket
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import sys
        import getopt
        from time import asctime
        from math import pi
        from pprint import pprint as pp
    if 1:  # Custom imports
        from u import u, to, fromto, ParseUnit
        from get import GetNumber
        from uncertainties import ufloat, ufloat_fromstr, UFloat
        from uncertainties.umath import sqrt, acos
        from f import flt
        from wrap import dedent
        from color import t
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        ii = isinstance
        required_keys = set(("D", "d", "h", "input_units", "offset", "shape"))
        optional_keys = set(("title",))
        separator = "-"*70
        # Control how numbers with uncertainties are printed
        if 0:
            unc = ".1uS"    # E.g. 275(2)
        else:
            unc = ".1uP"    # E.g. 275±2
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [datafile...]
          Calculate volume calibration marks for square and round bucket shapes.  The
          program will prompt you for the required quantities.  If one or more datafiles
          are given, then input is taken from them rather than by prompting the user.  A
          separate report is printed to stdout for each datafile.
        Options:
          -d n    Number of significant figures in report. [{d["-d"]}]
          -f      Print a sample datafile
          -h      Print this help
          -m      Use mm for input and output length measurements
          -r s    Formatting spec for length output (example:  '.0f' prints lengths in
                  mm to the nearest mm)
          -u      Allow uncertainty expressions in numerical values
        Note:
            If you use -u and use interactive input mode, if you type in e.g. '9 m' for
            a value, it will have the standard uncertainty of 1, as this is how the
            python uncertainties library works.  If you use a datafile, you can write
            numbers with uncertainties as e.g. '10+/-1' or '10(1)' and no -u option is
            needed.
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 4     # Number of display digits
        d["-m"] = False # Use mm
        d["-r"] = None  # Length formatting string
        d["-u"] = False # Allow uncertainties
        try:
            opts, datafiles = getopt.getopt(sys.argv[1:], "d:fhmr:u")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "mu":
                d[o] = not d[o]
            if o in ("-d",):
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-f",):
                SampleDataFile(d)
            elif o in ("-r",):
                d[o] = a
            elif o in ("-h",):
                Usage(d, status=0)
        x = flt(0)
        x.N = d["digits"] = d["-d"]
        x.rtz = x.rtdp = True
        return datafiles
if 1:  # Core functionality
    def RoundArea(D):
        "Area of a circle of diameter D"
        assert D >= 0
        return pi*D*D/4
    def SquareArea(a, r):
        "Area of a square with sides a with rounded edges of radius r"
        assert a >= 0 and r >= 0 and r <= a/2
        return a*a - r*r*(4 - pi)
    def Volume(d):
        '''Return volume in m3 of a frustum of height h in m with bottom area
        A0 in m2 and top area of A1 in m2.  d is a dictionary.
        '''
        h, A0, A1 = d["h"][0], d["A0"], d["A1"]
        assert h > 0 and A0 >= 0 and A1 >= 0 and A1 >= A0
        return h*(A0 + A1 + sqrt(A0*A1))/3
    def secant(sigma, D, h):
        assert h > 0 and D > 0 and sigma >= 0
        return sqrt(1 + (sigma*D/(2*h))**2)
    def PrintPercentCalibrations(A0, V):
        '''Print the calibration points that represent the fraction of the
        total bucket volume when filled to the brim.
        
        V is total bucket volume in in3.
        '''
        step_size = steps["fraction"]
        print("  Divisions for fraction of total volume")
        print("      Fraction     inches        mm")
        print("      --------     ------      ------")
        fmt, count = " %10s "*3, 0
        while True:
            fraction = count*step_size
            count += 1
            vx = V*fraction
            if fraction > 1:
                break
            mark = CalibrationMark(D, h, offset, vx, A0)
            f, i, m = "%6.2f" % fraction, "%8.2f" % mark, "%8.1f" % (mark*in2mm)
            print(fmt % (f, i, m))
        print()
    def SampleDataFile(d):
        print(
            dedent(f'''
        # Sample datafile for the bucket.py script.  The script will print a table
        # of bucket volume calibration marks that can be located with a tape
        # measure.  See the bucket.pdf file for details.
        
        # The bucket shape is either "round" (default) or "square".
        shape = "round"
        
        #title = ""         # Report title (optional)
        
        # Specify the default input units (required).  Most common length units are
        # supported (see the u.py module).
        input_units = "inches"
        
        # The following variables describe the bucket's geometry.  See the
        # bucket.pdf file for a diagram.  The numbers given are for a Rheem 5
        # gallon bucket used to check the program's calculations.  Note that offset
        # is given in different units, which demonstrates that these input
        # variables can be either numbers or strings that can be interpreted as a
        # number and an appended unit string.
        D = 11.34       # Diameter/width at top of bucket
        d = 10.42       # Diameter/width at bottom of bucket
        offset = "11.9 mm"  # Height of bucket bottom above ground
        h = 14          # Height of bucket
        
        # For square buckets, you must specify the radius of the corners.
        r = 0           # Square bucket corner radius
        
        # You can specify the number of decimal digits to print out in the
        # report.
        digits = {d["-d"]}
        
        # The report's output units and volume steps must be defined.
        output_volume_units = "liters"
        output_length_units = "mm"
        volume_steps = 1
        ''')
        )
        exit(0)
    def Interactive(d):
        Report.data = []
        if 0:
            # Use these as checks without having to enter data
            d["output_volume_units"] = "gallons"
            d["output_length_units"] = "mm"
            which = 0
            if which == 0:
                # Simplot 30 lb strawberries bucket 
                d["title"] = "Simplot 30 lb strawberries bucket"
                d["shape"] = "round"
                d["input_units"] = "mm"
                d["D"] = (270*u("mm"), "270", "mm")
                d["d"] = (247.5*u("mm"), "247.5", "mm")
                d["offset"] = (7*u("mm"), "7", "mm")
                d["h"] = (285*u("mm"), "285", "mm")
                Report("liters", "mm", 1)
                d["volume_fraction"] = 1
                Report("%", "mm", 10)
            elif which == 1:
                # Rheem round bucket; should print out:
                #     5 L, 100.9 mm)
                #    10 L, 186.2 mm)
                #    15 L, 268.1 mm)
                d["title"] = "Rheem round gray bucket"
                d["shape"] = "round"
                d["input_units"] = "mm"
                d["D"] = (11.34*u("in"), "11.34", "in")
                d["d"] = (10.42*u("in"), "10.42", "in")
                d["offset"] = (0.47*u("in"), "0.47", "in")
                d["h"] = (14*u("in"), "14", "in")
                Report("liters", "mm", 1)
                d["volume_fraction"] = 1
                Report("%", "mm", 10)
            elif which == 2:
                # Ropak square bucket; should print out:
                #     5 L, 117.3 mm)
                #     9 L, 202.8 mm)
                d["title"] = "Ropak square cat litter bucket"
                d["shape"] = "square"
                d["input_units"] = "mm"
                d["D"] = (9.10*u("in"), "9.10", "in")
                d["d"] = (8.16*u("in"), "8.16", "in")
                d["offset"] = (0.12*u("in"), "0.12", "in")
                d["h"] = (13*u("in"), "13", "in")
                d["r"] = (1.25*u("in"), "1.25", "in")
                Report("liters", "mm", 1)
        else:
            # Prompt the user for the required variables and put them in the
            # options dictionary d.
            default_length_unit = "mm"
            print(dedent('''
            Use the -h option for more information on how to run the script.
             
            This script will print volume calibration marks for square and round bucket
            shapes.  Read the bucket.pdf file for details on the geometry and the
            calculation.  You can quit at any time by entering the letter 'q'.
            '''))
            print()
            emsg = "Error:  you must input a number and optional unit"
            # Input length units
            msg = f"Input length units? [{default_length_unit}] "
            while True:
                default_unit = input(msg).strip()
                if default_unit == "q":
                    exit(0)
                if not default_unit:
                    default_unit = default_length_unit
                    break
                try:
                    u(default_unit)
                    break
                except ValueError:
                    print("'{}' is not a valid length unit".format(default_unit))
            d["input_units"] = default_unit
            # Output length units
            msg = "Output length units? [{}] ".format(d["input_units"])
            while True:
                default_unit = input(msg).strip()
                if default_unit == "q":
                    exit(0)
                if not default_unit:
                    default_unit = d["input_units"]
                    break
                try:
                    u(default_unit)
                    break
                except ValueError:
                    print("'{}' is not a valid length unit".format(default_unit))
            output_length_units = default_unit
            # Output volume units
            default_volume_unit = "liters"
            msg = "Output volume units? [{}] ".format(default_volume_unit)
            while True:
                default_unit = input(msg).strip()
                if default_unit == "q":
                    exit(0)
                if not default_unit:
                    default_unit = default_volume_unit
                    break
                try:
                    u(default_unit)
                    break
                except ValueError:
                    if default_unit == "%":
                        # Get volume_fraction
                        d["volume_fraction"] = GetNumber("Volume fraction? ", low=0, low_open=True, high=1, default=1)
                        break
                    else:
                        print("'{}' is not a valid volume unit".format(default_unit))
            output_volume_units = default_unit
            # Output volume steps
            volume_steps = GetNumber("Output volume steps? ", low=0, low_open=True, default=1)
            Report.data.append((output_volume_units, output_length_units, volume_steps))
            # Bucket shape
            default_shape = "round"
            msg = "Bucket shape (round or square)? [{}] ".format(default_shape)
            while True:
                shape = input(msg).strip().lower()
                if shape == "q":
                    exit(0)
                if not shape:
                    shape = default_shape
                    break
                if "round".startswith(shape):
                    shape = "round"
                    break
                if "square".startswith(shape):
                    shape = "square"
                    break
                print(
                    "'{}' is not a valid shape (must be square or round)".format(unit)
                )
            d["shape"] = shape
            # Top diameter/width
            while True:
                try:
                    num, unit = GetNumber(
                        "What is the top diameter/width D? ",
                        low=0,
                        low_open=True,
                        use_unit=True,
                        use_unc=d["-u"],
                    )
                    break
                except ValueError:
                    print(emsg)
            if unit:
                d["D"] = (num*u(unit), num, unit)
            else:
                d["D"] = (num*u(d["input_units"]), num, unit)
            # Bottom diameter/width
            D_val, D_num, D_unit = d["D"]
            while True:
                try:
                    num, unit = GetNumber(
                        "What is the bottom diameter/width d? ",
                        low=0,
                        low_open=True,
                        use_unit=True,
                        use_unc=d["-u"],
                    )
                    if unit:
                        d_m = num*u(unit)
                    else:
                        d_m = num*u(d["input_units"])
                    if d_m > D_val:
                        raise RuntimeError()
                    break
                except ValueError:
                    print(emsg)
                except RuntimeError:
                    print("  The value must be <= {} {}".format(D_num, D_unit))
            if unit:
                d["d"] = (num*u(unit), num, unit)
            else:
                d["d"] = (num*u(d["input_units"]), num, unit)
            # Offset
            while True:
                try:
                    num, unit = GetNumber("What is the offset? ", low=0, use_unit=True, use_unc=d["-u"])
                    break
                except ValueError:
                    print(emsg)
            if unit:
                d["offset"] = (num*u(unit), num, unit)
            else:
                d["offset"] = (num*u(d["input_units"]), num, unit)
            # Height
            while True:
                try:
                    num, unit = GetNumber( "What is the height h? ", low=0, low_open=True, use_unit=True, use_unc=d["-u"])
                    break
                except ValueError:
                    print(emsg)
            if unit:
                d["h"] = (num*u(unit), num, unit)
            else:
                d["h"] = (num*u(d["input_units"]), num, unit)
            # Radius for square buckets (note 0 is allowed)
            if d["shape"] == "square":
                rmax_m = min(d["D"][0], d["d"][0])/2
                while True:
                    try:
                        num, unit = GetNumber("What is the corner radius? ", low=0, use_unit=True)
                        val_m = num*u(unit)
                        if val_m > rmax_m:
                            raise RuntimeError()
                        break
                    except ValueError:
                        print(emsg)
                    except RuntimeError:
                        print("  The value must be <= min(D, d)/2")
                if unit:
                    d["r"] = (num*u(unit), num, unit)
                else:
                    d["r"] = (num*u(d["input_units"]), num, unit)
        print()
        # Verify we have the needed input keys in d
        missing = CheckForNeededKeys(d)
        if missing:
            print("Program bug:  missing keys:")
            for key in missing:
                print("  ", key)
    def CheckForNeededKeys(opts):
        '''Check that the required keys in opts are present; return a list of
        the ones that are missing.
        '''
        missing = []
        for key in required_keys:
            if key not in opts:
                missing.append(key)
        if opts["shape"] == "square":
            key = "r"
            if key not in opts:
                missing.append(key)
        return missing
    def PrintInputValues(opts):
        indent = " "*3
        print(indent, "Default units =", opts["input_units"])
        print(indent, "Bucket shape =", opts["shape"])

        if ii(opts["D"][1], (float, flt, int)):
            print(indent, "D =", flt(opts["D"][1]), opts["D"][2])
        else:
            print(indent, f"D = {opts['D'][1]:{unc}} {opts['D'][2]}")
        if ii(opts["d"][1], (float, flt, int)):
            print(indent, "d =", flt(opts["d"][1]), opts["d"][2])
        else:
            print(indent, f"d = {opts['d'][1]:{unc}} {opts['d'][2]}")
        if ii(opts["h"][1], (float, flt, int)):
            print(indent, "h =", flt(opts["h"][1]), opts["h"][2])
        else:
            print(indent, f"h = {opts['h'][1]:{unc}} {opts['h'][2]}")
        if ii(opts["offset"][1], (float, flt, int, str)):
            print(indent, "offset =", flt(opts["offset"][1]), opts["offset"][2])
        else:
            print(indent, f"offset = {opts['offset'][1]:{unc}} {opts['offset'][2]}")
        print(indent, "digits =", opts["digits"])
        x = flt(0)
        x.N = opts["digits"]
        if opts["shape"] == "square":
            print(indent, "r =", flt(opts["r"][1]), opts["r"][2])
            if ii(opts["r"][1], (float, flt, int)):
                print(indent, "r =", flt(opts["r"][1]), opts["r"][2])
            else:
                print(indent, f"r = {opts['r'][1]:{unc}} {opts['r'][2]}")
        # Print total volume in some common units
        if ii(opts["V"], (float, flt)):
            V = flt(opts["V"])
            print(indent, "Volume:")
            for unit in ("liters", "gallons", "ft3", "in3"):
                u = unit[:-1] + "³" if unit in "ft3 in3".split() else unit
                print(indent, " "*3, V*to(unit), u)
        else:
            V = opts["V"]
            print(indent, "Volume:")
            for unit in ("liters", "gallons", "ft3", "in3"):
                u = unit[:-1] + "³" if unit in "ft3 in3".split() else unit
                print(indent, " "*3, f"{V*to(unit):{unc}} {u}")
        print()
    def CalculateVolume(opts):
        '''Set opts["V"] equal to the volume of the bucket in m3.  Also
        calculate the areas A0 of bottom and A1 of top in m2.
        '''
        d, D, h = opts["d"][0], opts["D"][0], opts["h"][0]
        if opts["shape"] == "square":
            r = opts["r"][0]
            A0 = opts["A0"] = SquareArea(d, r)
            A1 = opts["A1"] = SquareArea(D, r)
        elif opts["shape"] == "round":
            A0 = opts["A0"] = RoundArea(d)
            A1 = opts["A1"] = RoundArea(D)
        else:
            raise ValueError("Unknown shape")
        opts["V"] = h*(A0 + A1 + sqrt(A0*A1))/3
    def PrintHeader(d):
        if "title" in d:
            print(d["title"])
            print()
        s = asctime().replace("  ", " ")
        print("Bucket volume calibration (", s, ")", sep="")
        if d["datafile"] is not None:
            print(" "*3, "Datafile =", d["datafile"])
    def PrintReport(d):
        PrintHeader(d)
        PrintInputValues(d)
        for vu, lu, s in Report.data:
            d["output_volume_units"] = vu
            d["output_length_units"] = lu
            d["volume_steps"] = s
            PrintCalibrations(d)
    def PrintCalibrations(d):
        '''Print a table of calibrations in units of d["output_volume_units"]
        and in steps of d["steps"].  The linear distance measure will be in
        units of d["output_length_units"].
        
        This function also handles the case where d["output_volume_units"] is
        "%", which means to print the calibration marks to reach a given
        percentage of the bucket volume (or a fraction of the bucket volume
        given in the datafile as the variable volume_fraction).
        '''
        def NotDone(V, v, eps=1e-14):
            # Determines when to stop printing table
            if v <= V:
                return True
            try:
                return abs(v - V) < eps
            except TypeError:
                # V is uncertain
                return abs(v - (V.n + 2*V.s)) < eps    # A judgment call of 2 uncertainties
        Vtotal_m3 = d["V"]  # Total volume in m3
        percent = d["output_volume_units"] == "%"
        # Get the volume step size in m3
        if percent:
            Vbase = flt(Vtotal_m3*d["volume_fraction"])
            v_step_m3 = flt(d["volume_steps"]/100*Vbase)
        else:
            v_step_m3 = flt(fromto(d["volume_steps"], d["output_volume_units"], "m3"))
        vx_m3 = v_step_m3
        # Set up some print formatting variables
        d["Volume"], d["Length"] = "Volume", "Length"
        a = 3/4
        d["wv"], d["wl"] = 20, 20
        d["Vhyphens"], d["Lhyphens"] = "-"*int(a*d["wv"]), "-"*int(a*d["wl"])
        d["indent"] = " "*0
        print(dedent(f'''
            Calibration table (volume in {d['output_volume_units']}, length in {d['output_length_units']})
            {d['indent']}{d['Volume']:^{d['wv']}}{d['Length']:^{d['wl']}}
            {d['indent']}{d['Vhyphens']:^{d['wv']}}{d['Lhyphens']:^{d['wl']}}
        '''))
        eps = 1e-14
        while NotDone(Vtotal_m3, vx_m3):
            d["vx"] = vx_m3
            mark_m = CalibrationMark(d)
            if percent:
                # Express V as a percent of Vbase
                V = vx_m3/Vbase*100
            else:
                V = vx_m3*to(d["output_volume_units"])
            L = mark_m*to(d["output_length_units"])
            d["v"] = str(V)
            d["l"] = str(L)
            if d["-r"] is not None:
                d["l"] = l = f"{L:{d['-r']}}"
                if ii(L, (float, flt)):
                    print(f"{d['indent']}{d['v']!s:^{d['wv']}s}{d['l']!s:^{d['wl']}s}")
                else:
                    s = f"{l:{unc}}"
                    print(f"{d['indent']}{d['v']!s:^{d['wv']}s}{s:^{d['wl']}s}")
            else:
                if ii(L, (float, flt)):
                    print(f"{d['indent']}{d['v']!s:^{d['wv']}s}{d['l']!s:^{d['wl']}s}")
                else:
                    s = f"{L:{unc}}"
                    print(f"{d['indent']}{d['v']!s:^{d['wv']}s}{s:^{d['wl']}s}")
            vx_m3 += v_step_m3
    def CalibrationMark(opts):
        # All length variables are in m
        d = opts["d"][0]
        D = opts["D"][0]
        h = opts["h"][0]
        offset = opts["offset"][0]
        vx = opts["vx"]
        A0 = opts["A0"]
        sigma = D/d - 1
        assert sigma >= 0
        try:
            x = ((1 + 3*sigma*vx/(A0*h))**(1/3) - 1)/sigma
        except ZeroDivisionError:
            x = vx/(A0*h)  # sigma is zero; use the limit
        return (x*h + offset)* secant(sigma, D, h)
    def InterpretUncertainty(line, exception):
        '''Return (a, b) where line is expected to be e.g. something like 'D = 270(1)'
        or 'D = 270 ± 1'.   a is the string 'D' and b will be "ufloat_fromstr('270(1)')"
        or "ufloat_fromstr('270 ± 1')".  This allows the calling context to get the
        variable D in its local namespace by using exec(f"{a} = {eval({b!r})}").
        '''
        msg1 = "object is not callable"
        msg2 = "invalid character '±'"
        s = str(exception)
        if msg1 in s or msg2 in s:
            # Short form uncertainty such as '270(2)' or '270.1(2)' or standard uncertainty
            # form such as '270 ± 1'
            f = line.split("=", maxsplit=2)
            if len(f) != 2:
                raise ValueError(f"Unrecognized number")
            name, value = f
            s = f"ufloat_fromstr(value)"
            try:
                x = eval(s)
                return name.strip(), f"ufloat_fromstr({value.strip()!r})"
            except Exception as e:
                raise ValueError(f"Unrecognized number: {e}")
        raise ValueError(f"Unrecognized number in line {line!r}")
    def ReadData(file, _opts):
        '''Read the data in from the given file and put the information into
        the _opts dictionary.
        '''
        # Note:  the underscores are to help with keeping the unwanted
        # variables out of _opts.
        if 0:   # Original method
            _s = open(file, "r").read()
            exec(_s)
        else:   # Allow uncertainties
            _lines = open(file, "r").read().split("\n")
            for _line in _lines:
                #t.print(f"{t.cynl}{_line}")
                if _line.strip().startswith("#"):
                    continue
                try:
                    exec(_line)
                except Exception as e:
                    _a, _b = InterpretUncertainty(_line, e)
                    _s = f"{_a} = eval({_b!r})"
                    try:
                        exec(_s)
                    except Exception as f:
                        msg = dedent(f'''
                            Got exception: {f}
                            Line = {_line!r}
                            File = {file!r}''')
                        Error(msg)
        # All lines read in, so add local variables to _opts
        _d = locals().copy()
        for _i in _d:
            if _i[0] != "_":
                _opts[_i] = _d[_i]
        if "digits" in _d:
            if not (1 <= _d["digits"] <= 15):
                Error("digits must be an integer between 1 and 15")
        Report(
            _opts["output_volume_units"],
            _opts["output_length_units"],
            _opts["volume_steps"],
        )
        InterpretData(_opts)
    def InterpretData(opts):
        '''The data from a datafile have been read into the opts dictionary.
        Change the variables into the same form as is used for the interactive
        input (i.e., parse the variables for units and construct the tuples).
        '''
        missing = CheckForNeededKeys(opts)
        if missing:
            print("Missing variables in '{}':".format(opts["file"]), file=sys.stderr)
            for i in missing:
                print("  ", i, file=sys.stderr)
            exit(1)
        # Check shape
        if opts["shape"] not in ("round", "square"):
            Error("'shape' variable must be 'round' or 'square'")
        # Check desired units
        key = "input_units"
        try:
            u(opts[key])
        except ValueError:
            Error("{} is an unrecognized input unit".format(key))
        for volume_unit, length_unit, step in Report.data:
            try:
                u(volume_unit)
            except ValueError:
                if volume_unit != "%":
                    Error("'{}' is an unrecognized unit".format(volume_unit))
            try:
                u(length_unit)
            except ValueError:
                Error("'{}' is an unrecognized unit".format(length_unit))
            try:
                float(step)
            except ValueError:
                Error("'{}' is not a valid volume step".format(step))
        # Frustum's geometric variables
        for key in ("D", "d", "h", "offset"):
            opts[key] = CheckVariable(key, opts)
        # Radius for square bucket
        if opts["shape"] == "square":
            opts["r"] = CheckVariable("r", opts)
        if "volume_fraction" in opts:
            if not (0 < opts["volume_fraction"] <= 1):
                Error("volume_fraction must be > 0 and <= 1")
        else:
            opts["volume_fraction"] = 1
    def CheckVariable(key, opts):
        '''Process a length in the string opts[key].  If it's a string, it may
        contain an optional unit.  Return a tuple (length in m, original number
        string, unit string).
        '''
        input_unit = opts["input_units"]
        if ii(opts[key], str):
            s = opts[key].strip()
            if not s:
                Error("Variable {} is an empty string".format(key))
            parsedunit = ParseUnit(s)
            if parsedunit is None:
                Error("No number found for variable {}".format(key))
            assert len(parsedunit) == 2
            num, unit = parsedunit
            try:
                val = float(num)
            except Exception:
                Error("'{}' in value for variable {} isn't a number".format(num, key))
            try:
                val = val*u(unit)
            except ValueError:
                Error(f"The unit '{unit}' for variable {key} isn't a proper unit")
            return (val, num, unit)
        else:
            x = opts[key]
            if ii(x, (int, float, flt)):
                try:
                    # Must be a number convertible to a float
                    val = float(opts[key])
                except Exception:
                    Error("Variable '{}' is not a suitable number".format(key))
            elif ii(x, UFloat):
                val = opts[key]
            return (val*u(input_unit), opts[key], input_unit)
    def Report(output_volume_units, output_length_units, volume_steps):
        '''Called from a datafile.  Cache the required report data in
        Report.data.
        '''
        Report.data.append((output_volume_units, output_length_units, volume_steps))
if __name__ == "__main__":
    d = {
        "output_volume_units": "m3",
        "output_length_units": "m",
    }  # Options dictionary
    datafiles = ParseCommandLine(d)
    d["datafile"] = None
    if datafiles:
        for file in datafiles:
            opts = d.copy()
            Report.data = []
            opts["datafile"] = file
            ReadData(file, opts)
            CalculateVolume(opts)
            PrintReport(opts)
            if len(datafiles) > 1:
                print(separator, sep="")
    else:
        Interactive(d)
        CalculateVolume(d)
        PrintReport(d)
