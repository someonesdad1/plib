'''
ToDo
    - Add -m option for metric output
    - Only print inch or metric
    - For both Cain & Johansson methods, show clearances in red & green

Calculate shaft/hole fits
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Calculate shaft/hole fits
        #∞what∞#
        #∞test∞# ignore #∞test∞#
        pass
    if 1:   # Imports
        import sys
        import os
        import getopt
        from pdb import set_trace as xx 
        from fractions import Fraction as F
    if 1:   # Custom imports
        from wrap import dedent
        from f import flt
        from u import u, ParseUnit
        from color import t
    if 1:   # Global variables
        class G:
            pass
        in2mm = u("inches")/u("mm")
        # Colors
        t.int = t("redl")
        t.cl = t("grnl")
        t.msg = t("cynl", attr="ul")
        t.warn = t("magl")
        t.matl = t("ornl")
        t.meth = t("purl")
if 1:  # Utility
    def Manpage():
        print(dedent(f'''
        Example
 
            I have a shaft with a measured OD of 0.9937 inches.  I'd like to
            make this shaft a driving fit into a hole.  What should I bore the
            mating hole size to?
 
            Run the script with an argument of 0.9937.  In the report, look
            under the heading "Shaft size is basic".  Next to "Drive", the
            required hole size is 0.9930, which has an interference of 0.75
            mils with the shaft.
 
        The fit names and associated numbers are from page 5.18 of Tubal Cain's
        (Tom Walshaw) "Model Engineers Handbook", 3rd ed.  Here's the text and
        table from the book [sic]:
        
            Shaft/hole fits
            
            The following figures indicate the difference between hole and shaft
            size for the named classes of fit.  These apply from shafts from
            1/8" to 2" dia.  Where the 'hole' is in a wheel boss some
            consideration must be given to the strength of this -- a test
            assembly is advised.  Normally the hole should be made dead to size
            and the shaft diameter adjusted to get the fit desired.  The figures
            are in thousandths of an inch per inch of diameter, to which must be
            added the constant 'C'.  Thus, for a 1" push fit the shaft must be
            0.35 + 0.15 = 0.5 thousandths smaller than the hole ('+' means the
            shaft is larger and '-' , smaller than the hole.) 'C' may be
            converted directly to mm (divide by 25 is near enough) and 'thou/in'
            = micron/mm.
            
                                        'C'
                    Fit             (0.001")    thou/in.
                --------------      --------    --------
                Shrink              +0.5        +1.5
                Force               +0.5        +0.75
                Drive               +0.3        +0.45
                Wheel keying        0           0
                Push                -0.15       -0.35
                Slide               -0.3        -0.45
                Prec. run           -0.5        -0.65
                Close run           -0.6        -0.8
                Normal run          -1.0        -1.5
                Easy run            -1.5        -2.25
                Small clearance     -2          -3
                Large clearance     -3          -5
            
            An allowance for thermal expansion must be made on engine pistons.
 
        In the script, the constant under the 'C' column is called c and the
        constant under the thou/in column is called m, both divided by 1000 to
        give units in inches and inches/inch, respectively.  Given the hole
        diameter d, the shaft diameter D should be
 
            D = d - (m*d + c) = d*(1 - m) - c
 
        Temperature differential for shrink fit

            The table after Walshaw's method gives the temperature needed to get
            a shrink fit as given in the tables for different materials.  These
            are calculated based on the thermal coefficient of expansion and
            it's assumed the expansion is linear.  You'll probably want to add 5
            or 10 degrees to make sure things fit.

            Check:  The formula is D = d*(1 + α*ΔT), so ΔT = (D/d - 1)/α.  The
            shrink size for the above 0.9937 inch shaft was an interference of
            1.99 mils, so we need the ΔT to get this expansion.  We thus have ΔT
            = 1.99×10⁻³/(12×10⁻⁶) = 166 K, which is the temperature given in the
            table under °C.

        Adjusting the fit for other materials

            The -f option is used to adjust fits to other situations.  The basic
            formulas are good for metallic materials like steel and brass.  For
            other materials like plastic, you may want more of an interference
            fit; for such cases, set the n value to a number larger than 1.  For
            very stiff materials, you may want to use n values less than 1.  The
            factor n multiplies the interference calculated for metals.
 
        Johansson system of fits

            Machinery's Handbook 19th edition 1971 (page 1514) gives the
            Johansson system for fits.  This is a table that fits onto one page
            and covers diameters of 0.03 to 15.75 inches.  Use the -j option to
            use this system.  

            For the example given above for the shaft of 0.9937 inches, the
            Johansson method gives a hole size of 0.9930-0.9934 for an easy
            driving fit compared to the 0.9930 of Tubal Cain's method.
 
        '''.rstrip()))
        exit(0)
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def ParseCommandLine(opt):
        opt["-f"] = 1         # Adjustment for material (1 = metal)
        opt["-j"] = False     # Use Johansson method
        opt["-m"] = False     # Output in mm
        if len(sys.argv) < 2:
            Usage(opt)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "f:hjm")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "jm":
                opt[o] = not opt[o]
            elif o == "-f":
                opt[o] = x = flt(a)
                if x <= 0:
                    Error("-f option must be > 0")
            elif o == "-h":
                Manpage()
        return ' '.join(args)
    def Usage(opt, status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] diameter [unit]
          Print a table showing fits for hole and shaft sizes (inches by
          default).  The command line can include python expressions; the math
          module's symbols are in scope.  
        Options
          -h    Print manpage
          -f n  Use material factor n (defaults to 1)
          -j    Use the Johansson system of fits
          -m    Output in mm instead of inches
        '''))
        exit(status)
if 1:  # Core functionality
    def GetDiameter(arg, opt):
        '''Given the command line arguments collapsed into a space-separated
        string, return the command and the diameter in inches that the user
        requested data for.
        '''
        try:
            s, unit = ParseUnit(arg, allow_expr=True)
            if not s:
                Usage(opt)
        except ValueError as e:
            Error(e)
        try:
            diam = float(eval(s))
        except Exception:
            Error(f"Can't evaluate '{s}'")
        if diam <= 0:
            Error("Negative or zero diameter is meaningless.")
        unit = unit if unit else "inches"
        diam_inches = flt(diam*u(unit)/u("inches"))
        return arg, diam_inches
if 1:  # Tubal Cain functionality
    if 1:  # Global variables
        tc = G()
        tc.fits = (
            # Class of fit, c (in mils), m (in mils/inch)
            # For a given hole diameter d, machine the shaft diameter D to d - x
            # where x = (m/1000)*d + c/1000.
            ("Shrink", flt(0.5), flt(1.5)),
            ("Force", flt(0.5), flt(0.75)),
            ("Drive", flt(0.3), flt(0.45)),
           #("Wheel keying", flt(0), flt(0)),
            ("Push", flt(-0.15), flt(-0.35)),
            ("Slide", flt(-0.3), flt(-0.45)),
            ("Precision running", flt(-0.5), flt(-0.65)),
            ("Close running", flt(-0.6), flt(-0.8)),
            ("Normal running", flt(-1.0), flt(-1.5)),
            ("Easy running", flt(-1.5), flt(-2.25)),
            ("Small clearance", flt(-2.0), flt(-3.0)),
            ("Large clearance", flt(-3.0), flt(-5.0)),
        )
        tc.thermal_expansion = (   # Units are 1/K
            ("Aluminum", flt(23e-6)),
            ("Brass", flt(19e-6)),
            ("Copper", flt(17e-6)),
            ("Iron", flt(11e-6)),
            ("Steel", flt(12e-6)),
        )
    def TubalCain(cmdline, D, opt):
        def HoleBasic(D, opt):
            'D is hole size in inches'
            f = opt["-f"]
            shaft_size_in = D
            shaft_size_mm = D*in2mm
            t.print(f"{t.msg}Hole size is basic")
            hole_size_in = float(D)
            hole_size_mm = in2mm*D
            i = "mm" if opt["-m"] else "in"
            c = "mm" if opt["-m"] else "mils"
            print(f'''
                           {t.meth}Tom Walshaw's (Tubal Cain) Method{t.n}
                          Shaft size, {i}       Clearance, {c}
                          --------------       ---------------
            '''[1:].rstrip())
            for name, constant, allowance in tc.fits:
                correction = f*(allowance*hole_size_in + constant)/1000
                shaft_size_in = hole_size_in + correction
                shaft_size_mm = shaft_size_in*in2mm
                clearance_mils = f*(hole_size_in - shaft_size_in)*1000
                clearance_mm = clearance_mils*in2mm/1000
                q = f"{t.int if clearance_mm < 0 else t.cl}"
                if opt["-m"]:
                    print(f"  {name:18s} {shaft_size_mm:16.3f}", end=" ")
                    print(f"{q}{clearance_mm:19.2f}{t.n}")
                else:
                    print(f"  {name:18s} {shaft_size_in:15.4f}", end=" ")
                    print(f"{q}{clearance_mils:19.2f}{t.n}")
        def ShaftBasic(D, opt):
            'D is hole size in inches'
            f = opt["-f"]
            shaft_size_in = float(D)
            shaft_size_mm = in2mm*D
            i = "mm" if opt["-m"] else "in"
            c = "mm" if opt["-m"] else "mils"
            t.print(f"\n{t.msg}Shaft size is basic")
            print(f'''
                           Hole size, {i}       Clearance, {c}
                           -------------       ---------------
            '''[1:].rstrip())
            for name, constant, allowance in tc.fits:
                correction = -f*(allowance*shaft_size_in + constant)/1000
                hole_size_in = shaft_size_in + correction
                hole_size_mm = hole_size_in*in2mm
                clearance_mils = f*(hole_size_in - shaft_size_in)*1000
                clearance_mm = clearance_mils*in2mm/1000
                q = f"{t.int if clearance_mm < 0 else t.cl}"
                if opt["-m"]:
                    print(f"  {name:18s} {hole_size_mm:16.3f}", end=" ")
                    print(f"{q}{clearance_mm:19.2f}{t.n}")
                else:
                    print(f"  {name:18s} {hole_size_in:15.4f}", end=" ")
                    print(f"{q}{clearance_mils:19.2f}{t.n}")
        def CalculateFit(cmdline, D, opt):
            '''hole_size_inches is diameter of hole in inches.  opt is the
            settings dictionary.
            '''
            Dmm = D*in2mm
            if opt["-f"] != 1:
                t.print(f"{t.matl}Material factor is", opt["-f"])
            print("Diameter = " + cmdline)
            print(f"         = {D:.4f} inches")
            print(f"         = {Dmm:.3f} mm")
            if not 0.125 <= D <= 2:
                t.print(f"    {t.warn}Warning:  diameter is outside [1/8, 2] inches")
            print()
            HoleBasic(D, opt)
            ShaftBasic(D, opt)
        def Temperatures(D, opt):
            'Show temperatures needed to get a shrink fit'
            hole_size_in = float(D)
            hole_size_mm = in2mm*D
            name, constant, allowance = tc.fits[0]
            f = opt["-f"]
            assert(name == "Shrink")
            correction = f*(allowance*hole_size_in + constant)/1000
            shaft_size_in = hole_size_in + correction
            clearance_in = f*(hole_size_in - shaft_size_in)
            print(dedent(f'''
            
            {t.msg}Temperature differential for shrink fit:{t.n}
              Material    alpha, 1/MK            °C         °F
              --------    -----------           -----      -----'''))
            for material, alpha in tc.thermal_expansion:
                δd = abs(clearance_in/hole_size_in)
                # Calculate ΔT in K
                ΔT = int(δd/alpha)
                print(f"  {material:12s} {int(alpha*1e6):6d} {ΔT:18d} {int(ΔT*9/5):10d}")
        CalculateFit(cmdline, D, opt)
        Temperatures(D, opt)
if 1:  # Johansson functionality
    '''
    Logic of the Johansson system
 
    The tables give the hole as basic.  Let's take an example, a hole of
    diameter 0.85 inches.  Suppose we want a push fit.  
 
    We use the tables to calculate the clearance, which will be a pair of
    numbers (a, b).  
 
        - When the hole is basic, we add these to the diameter to get the needed
          shaft diameter.
        - When the shaft is basic, we subtract these from the diameter to get
          the hole diameters.
 
    The diameter 0.85 gives index 4.  Thus, in dict jo.fit["p"], we get the
    tuple (-24, +31).  The units are 10⁻⁵ inches, so this is (-0.00024,
    +0.00031).  
 
    Thus, the shaft dimensions must be 0.84976 to 0.85031 inches.
    The script would print this out as 0.8498 to 0.8503 inches.
 
    Hole is basic [0.8498, 0.8503]

        Add 0.85 to (-0.00024, +0.00031) to get (0.84976, 0.85031).  The shaft
        diameter is thus (0.8498, 0.8503) inches.  Tubal Cain's method gives
        0.8496 for the shaft diameter, 0.2 mils below Johansson's method.
 
    Shaft is basic [0.8497, 0.8502]
 
        Subtract (-0.00024, +0.00031) from 0.85 to get (0.84969, 0.85024).  The
        hole diameter is thus (0.8497, 0.8502) inches.  Tubal Cain's method gives
        0.8504 for the hole diameter, 0.2 mils above Johansson's method.
    '''
    if 1:  # Global variables
        jo = G()
        # Table data:  Machinery's Handbook, 19th ed., pg 1514
        jo.min = 1/32
        jo.max = 15 + 3/4
        jo.fits = "l r s p e c f".split()
        jo.fit_names = {
            "l": "Light running",
            "r": "Running",
            "s": "Sliding",
            "p": "Push",
            "e": "Easy driving",
            "c": "Close driving",
            "f": "Forced",
        }
        jo.sizes = (
            # 11 ranges
            (flt(1/32), flt(1/8)),            #  0:  0.0312-0.125
            (flt(1/8), flt(1/4)),             #  1:  0.125-0.25
            (flt(1/4), flt(13/32)),           #  2:  0.25-0.406
            (flt(13/32), flt(23/32)),         #  3:  0.406-0.719
            (flt(23/32), flt(1 + 1/8)),       #  4:  0.719-1.12
            (flt(1 + 1/8), flt(1 + 7/8)),     #  5:  1.12-1.88
            (flt(1 + 7/8), flt(2 + 15/16)),   #  6:  1.88-2.94
            (flt(2 + 15/16), flt(4 + 17/32)), #  7:  2.94-4.53
            (flt(4 + 17/32), flt(6 + 7/8)),   #  8:  4.53-6.88
            (flt(6 + 7/8), flt(10 + 7/16)),   #  9:  6.88-10.4
            (flt(10 + 7/16), flt(15 + 3/4)),  # 10:  10.4-15.8
        )
        assert jo.sizes[0][0] == jo.min
        assert jo.sizes[10][1] == jo.max
        # Units in these tables are 10⁻⁵ inches
        jo.fit = {
            "l": (
                ( -83,  -43),   # 0
                (-122,  -63),   # 1
                (-165,  -87),   # 2
                (-217, -118),   # 3
                (-276, -157),   # 4
                (-335, -197),   # 5
                (-402, -236),   # 6
                (-473, -276),   # 7
                (-551, -315),   # 8
                (-630, -354),   # 9
                (-709, -394),   # 10
            ),
            "r": (
                ( -43,  -20),   # 0
                ( -63,  -31),   # 1
                ( -87,  -43),   # 2
                (-118,  -59),   # 3
                (-157,  -79),   # 4
                (-197,  -98),   # 5
                (-236, -118),   # 6
                (-276, -138),   # 7
                (-315, -157),   # 8
                (-354, -177),   # 9
                (-394, -197),   # 10
            ),
            "s": (
                ( -20,   -8),   # 0
                ( -31,  -12),   # 1
                ( -43,  -16),   # 2
                ( -59,  -20),   # 3
                ( -79,  -24),   # 4
                ( -98,  -31),   # 5
                (-118,  -39),   # 6
                (-138,  -47),   # 7
                (-157,  -55),   # 8
                (-177,  -67),   # 9
                (-197,  -75),   # 10
            ),
            "p": (
                (  -8,  +12),   # 0
                ( -12,  +20),   # 1
                ( -16,  +28),   # 2
                ( -20,  +31),   # 3
                ( -24,  +31),   # 4
                ( -31,  +31),   # 5
                ( -39,  +28),   # 6
                ( -47,  +24),   # 7
                ( -55,  +20),   # 8
                ( -67,  +20),   # 9
                ( -75,  +20),   # 10
            ),
            "e": (
                ( +12,  +24),   # 0
                ( +20,  +35),   # 1
                ( +28,  +47),   # 2
                ( +31,  +59),   # 3
                ( +31,  +71),   # 4
                ( +31,  +87),   # 5
                ( +28, +102),   # 6
                ( +24, +118),   # 7
                ( +20, +138),   # 8
                ( +20, +157),   # 9
                ( +20, +177),   # 10
            ),
            "c": (
                ( +24,  +39),   # 0
                ( +35,  +59),   # 1
                ( +47,  +83),   # 2
                ( +59, +110),   # 3
                ( +71, +142),   # 4
                ( +87, +177),   # 5
                (+102, +213),   # 6
                (+118, +256),   # 7
                (+138, +303),   # 8
                (+157, +354),   # 9
                (+177, +414),   # 10
            ),
            "f": (
                ( +39,  +59),   # 0
                ( +59,  +98),   # 1
                ( +83, +146),   # 2
                (+110, +197),   # 3
                (+142, +252),   # 4
                (+177, +319),   # 5
                (+213, +394),   # 6
                (+256, +481),   # 7
                (+303, +579),   # 8
                (+354, +689),   # 9
                (+414, +808),   # 10
            ),
        }
    def Johansson(cmdline, D, opt):
        '''cmdline is the string on the command line.  D is the calculated
        diameter in inches and opt is the options dictionary.
        '''
        if not jo.min <= D <= jo.max:
            msg = f"Diameter {cmdline!r} must be between {jo.min} and {jo.max} inches"
            Error(msg)
        print(f"Diameter = {cmdline!r} = {D:.4f} in = {D*25.4:.3f} mm")
        t.print(f"{t.meth}  Johansson's method")
        mm = 25.4
        hdrh = " "*31 + "Shaft Diameter"
        hdrs = " "*32 + "Hole Diameter"
        hdr1 = "                         Inches            Millimeters"
        hdr2 = f"{t.msg}Hole is basic{t.n}         Min      Max         Min      Max"
        hdr3 = f"{t.msg}Shaft is basic{t.n}        Min      Max         Min      Max"
        # Decimal digits of decimal numbers
        win = 4 
        wmm = win - 1
        if 1:   # Hole is basic
            print()
            print(hdrh)
            print(hdr1)
            print(hdr2)
            w = 15
            for i, letter in enumerate(jo.fits):
                print(f"  {jo.fit_names[letter]:{w}s}", end=" ")
                a, b = [j/1e5 for j in jo.fit[letter][i]]
                # Print diameter in inches
                dlo, dhi = D + a, D + b
                print(f"{dlo:8.{win}f} {dhi:8.{win}f}", end=" "*4)
                # Print diameter in mm
                print(f"{dlo*mm:8.{wmm}f} {dhi*mm:8.{wmm}f}")
        if 1:   # Shaft is basic
            print()
            print(hdrs)
            print(hdr1)
            print(hdr3)
            w = 15
            for i, letter in enumerate(jo.fits):
                print(f"  {jo.fit_names[letter]:{w}s}", end=" ")
                a, b = [-j/1e5 for j in jo.fit[letter][i]]
                # Print diameter in inches
                dlo, dhi = D + a, D + b
                print(f"{dhi:8.{win}f} {dlo:8.{win}f}", end=" "*4)
                # Print diameter in mm
                print(f"{dlo*mm:8.{wmm}f} {dhi*mm:8.{wmm}f}")

if __name__ == "__main__":
    opt = {}  # Options dictionary
    arg = ParseCommandLine(opt)
    cmdline, D = GetDiameter(arg, opt)
    if opt["-j"]:
        Johansson(cmdline, D, opt)
    else:
        TubalCain(cmdline, D, opt)
