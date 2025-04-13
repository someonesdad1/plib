'''

ToDo
    - Add option to generate and show a PostScript drawing for a particular number of
      sides.  This would be handy for shop documentation.
    - Add -i option for interactive solution
        - Variables:
            - n = number of sides
            - θ = central angle
            - β = interior angle between sides
            - s = length of side
            - p = perimeter
            - A = area
            - r = radius for inscribed circle
            - R = radius for circumscribed circle
            - d = diameter for inscribed circle
            - D = diameter for circumscribed circle
        - Here are the functions given in the analytic geometry document
            - ρ means one of r, R, d, D
            - θ(n)
            - β(n)
            - s(ρ, n)
            - p(s, n)
            - A(s, n), A(ρ, n)
            - r(s, n), r(R, n)
            - d(s, n), d(D, n)
        - Also solve for r + R for n odd (like was needed to get the inscribed diameter
          of the Penta-nut's recess)
            
'''
if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Calculate parameters of a regular polygon
    ##∞what∞#
    ##∞test∞# #∞test∞#
    # Standard imports
    from fractions import Fraction
    import sys
    import os
    import getopt
    # Custom imports
    from wrap import dedent
    from lwtest import Assert
    from color import TRM as t
    from f import flt, pi, sqrt, sin, cos, tan
    from uncertainties import ufloat, ufloat_fromstr, UFloat
    # Global variables
    class g:
        pass
    g.width = int(os.environ.get("COLUMNS", 80)) - 1
    g.w = None      # Used for maximum column width of table
    ii = isinstance
    isatty = sys.stdout.isatty()
    t.ti = t("ornl") if isatty else ""
    t.hi = t("brnl") if isatty else ""
    t.hdr = t("redl") if isatty else ""
    t.insc = t("purl") if isatty else ""
    t.circ = t("trq") if isatty else ""
    t.N = t.n if isatty else ""
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dia1 [dia2...]
          Print dimensions of regular polygons for given diameter(s) as either the
          inscribed or circumscribed circle diameter.  The diameters can be strings like
          '47', '4.7', '7/16', or '1-7/16'.
         
          You can also use words like 'triangle', 'hexagon', etc. to identify the
          polygon(s) you're interested in.  The first three letters of the word are what
          are used for identification.  Thus, '{sys.argv[0]} 1.3 tri' causes the script
          to print out results for a triangle only.
        Options:
          -a    Abbreviate numbers (remove trailing 0's and decimal point) [{opts["-a"]}]
          -c l  Color highlight the sides in the list l [{opts["-c"]}]
          -d n  Number of significant digits to print [{opts["-d"]}]
          -n l  Which sides to print; must be a comma-separated list of
                integers or a range() call.  [{opts["-n"]}]
          -t    Produce a table of useful factors allowing you to calculate
                various parameters of polygons given certain dimensions.
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Abbreviate numbers
        d["-c"] = ""        # Which lines to highlight
        d["-d"] = 4         # Number of significant digits
        d["-n"] = ",".join(str(i) for i in range(3, 13))
        d["-t"] = False     # Print the table
        try:
            opts, diameters = getopt.getopt(sys.argv[1:], "ac:d:hn:t")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, arg in opts:
            if o[1] in "at":
                d[o] = not d[o]
            elif o in ("-c",):
                d["-c"] = arg
            elif o in ("-d",):
                try:
                    d["-d"] = int(arg)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h",):
                Usage()
            elif o in ("-n",):
                if "range" in arg:
                    d["-n"] = ",".join(str(i) for i in list(eval(arg)) if i > 2)
                else:
                    d["-n"] = arg
        x = flt(0)
        x.N = d["-d"]
        x.rtz = False
        x.rtdp = True
        if d["-a"]:
            x.rtz = x.rtdp = True
        x.low = 1e-4
        x.high = 1e6
        if not d["-t"] and not diameters:
            Usage()
        # Convert d["-c"] to a set of integers
        if d["-c"]:
            s = d["-c"].split(",")
            d["-c"] = set([int(i) for i in s])
        else:
            d["-c"] = set()
        return diameters
if 1:  # Regular polygon formulas
    '''This section contains the relevant formulas with definition of the symbols.
    Angles are measured in radians.  My analytic geometry document is the reference,
    along with Marks, "Standard Handbook for Mechanical Engineers", McGraw-Hill, 7th
    ed., pg 1-39, 1967.  Symbols are

        d = inscribed circle diameter
        D = circumscribed circle diameter
        r = inscribed circle radius = apothem = d/2
        R = circumscribed circle radius = D/2
        A = area
        p = perimeter
        s = length of one side
        θ = 2*π/n = angle subtended by one side
        ϕ = θ/2 = π/n = the angle for solving polygon properties because you can use
            the formulas for right triangles.

    For practical work, r and R aren't convenient because they can't be conveniently
    measured unless you're working on a surface you can e.g. use dividers and you can
    locate the center of the polygon's inscribed or circumscribed circle.  Thus, the
    formulas will be in terms of the diameters d and D.  If n is odd, you can't easily
    measure d or D either:  consider the pentagon like in a Penta-nut.  You use
    electronic or dial calipers and measure the distance from an internal vertex to the
    perpendicular point of the opposite side, which is r + R.  You'd do the same thing
    with the external jaws on a pentagon that would fit into this recess.  The formulas
    give r + R = R*(1 + cos(ϕ)) = r*(1 + 1/cos(ϕ)).

    Basic formula = length of side = s = d*tan(ϕ)

        The basic triangle T of the n-sided regular polygon is half of the isoceles
        triangle formed by the circle's center and one side, with the radius making a
        right angle with the side.  We thus get s = d*tan(ϕ).  There are n of these
        basic triangles making up the regular polygon.

    p = perimeter = n*s = n*d*tan(ϕ)

    A = area = n*s*d/4 = p*d/4

        The area of T is half the base times the height, or (s/2)*r/2 = s*r/4.  The area
        of two of these triangles is s*r/2, which is the area of 1/n of the polyon
        because there are n of these triangles that make up the polygon.  Thus, the
        polygon's area is n*s*r/2 = n*s*d/4.

    Circumscribed diameter = D = s/sin(ϕ) = d/cos(ϕ)

    Inscribed diameter = d = s/tan(ϕ) = D*cos(ϕ)

    Table (like that in Marks)
        ϕ = π/n
        A/s² = n/[4*tan(ϕ)]
        A/D² = n*sin(2*ϕ)/8
        A/d² = n*tan(ϕ)/4
        s/D  = sin(ϕ)
        s/d  = tan(ϕ)
        d/D  = cos(ϕ)
        p/d  = n*tan(ϕ)
        p/D  = n*sin(ϕ)

        tan(ϕ) = n*s**2/(4*A) = 4*A/(n*d**2) = s/d = p/(n*d)
        sin(ϕ) = s/D = p/(n*D)
        cos(ϕ) = d/D

    Use cases for an interactive solver
        - One of d, D, r, R, s, p, A scale the problem.  Then the problem can be solved
          by knowing n.
        - Given A or p, find n and d/D that give the closest value.  Allow the user to
          constrain n to allowed values.
        - For most problems, you can probably assume you'll be given n.
        - Given a desired mass and material, find best n and d.  Allow user to constrain
          n to allowed values.

    Equations
        
        ϕ = π/n
        cos(ϕ) = d/D
        d = 2*r = s/tan(ϕ) = D*cos(ϕ)
        D = 2*R = s/sin(ϕ) = d/cos(ϕ)
        A = n*s*d/4 = p*d/4 = n*D**2*sin(2*ϕ)/8
          = n*d**2*tan(ϕ)/4 = n*s**2/(4*tan(ϕ))
        p = n*s = n*d*tan(ϕ)
        s = d*tan(ϕ) = D*sin(ϕ)

    Should be able to solve for the following two variable cases:

            d   D   r   R   s   p   A   n
        d   x   x   x   x   1   2   3   4
        D   x   x   x   x   5   6   7   8
        r   x   x   x   x   9   10  11  12
        R   x   x   x   x   13  14  15  16
        s   17  18  19  20  x   21  22  23
        p   24  25  26  27  28  x   29  30
        A   31  32  33  34  35  36  x   37
        n   38  39  40  41  42  43  44  x

    Case
     1 d, s
     2 d, p
     3 d, A
     4 d, n
     5 D, s
     6 D, p
     7 D, A
     8 D, n
     9 r, s
    10 r, p
    11 r, A
    12 r, n
    13 R, s
    14 R, p
    15 R, A
    16 R, n

    17 s, d
    18 s, D
    19 s, r
    20 s, R
    21 s, p
    22 s, A
    23 s, n

    24 p, d
    25 p, D
    26 p, r
    27 p, R
    28 p, s
    29 p, A
    30 p, n

    31 A, d
    32 A, D
    33 A, r
    34 A, R
    35 A, s
    36 A, p
    37 A, n

    38 n, d
    39 n, D
    40 n, r
    41 n, R
    42 n, s
    43 n, p
    44 n, A
     
    °F °C Ω θ μ Δ% π · ×✕✗ ÷ √ α β ɣ δ ɛ ϵ ϶ ν ξ ψ φ ϕ ζ λ ρ σ τ χ ω Γ Φ Ξ Λ Σ ℝ ℂ ℤ ℕ ℚ ℐ ℛ
    ∞ ± ∓ ¢ ≤ ≥ = ≠ ≡ ≢ † ‡ ∂ ∫ ∇ ∼ ≅ ≈ ∝ ∍ ∊ ∈ ∉ ∅ ∃ « » ∀ ∡ ∠ ∟ ∥ ∦ ⊙ ⊗ ⊕ ⊉ ⊈ ⊇ ⊆ ⊅ ⊄ ⊃ ⊂ ∪ ∩
    Superscripts: ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁱⁿ Subscripts: ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓᵦᵩ
    '''
if 1:  # Core functionality
    def Convert(size):
        '''Convert the string size to a flt or ufloat.  Can be an integer, flt,
        or fraction of e.g. the forms 7/8 or 1-7/8.  A ufloat can be either
        '1+-.1' or '1.0(1)' forms.
        '''
        if "+-" in size:    # It's a ufloat
            return ufloat_fromstr(size.replace("+-", "+/-"))
        elif "+/-" in size: # It's a ufloat
            return ufloat_fromstr(size)
        elif "±" in size:   # It's a ufloat
            return ufloat_fromstr(size)
        elif "(" in size and ")" in size:   # It's a ufloat
            return ufloat_fromstr(size)
        elif "/" in size:   # It's a fraction
            ip = 0
            num, denom = size.split("/")
            if "-" in num:
                ip, num = num.split("-")
            num, denom, ip = [int(i) for i in (num, denom, ip)]
            return flt(Fraction(num + ip * denom, denom))
        else:   # It's a float
            return flt(size)
    def FormulaTable():
        '''Print a table similar to the table on page 1-39 of Mark's
        "Standard Handbook for Mechanical Engineers", 7th ed., 1967.
        '''
        def F(x, w=None):
            '''str of flt x with leading 0 removed.  If w is not None, it's a
            width to center the string of x in.
            '''
            s = str(x)
            if s[0] == "0" and s[1] == ".":
                s = s[1:]
            if w is None:
                return s
            return f"{s:^{w}s}"
        # Check of formulas:  I drew a 6" diameter circle and used a
        # 30-60-90 triangle to draw a hexagon around it.  The measurements
        # agreed with the values calculated with the table to better than
        # 0.1%.
        print(dedent('''
        Regular polygons
        d = inscribed circle diameter, D = circumscribed circle diameter, A = area
        s = perimeter, a = length of one side, θ = angle subtended by side
        '''))
        if 1:   # Print table header
            # Width of printout:  the column for n is 2 wide and the remaining 9
            # columns are the width of a flt at current significance.  The smallest
            # number (and thus the longest) will be a/D for n=64.  This thus
            # defines the width w for each column.
            s = F(sin(pi/64))
            w = len(s)
            # There are 9 columns for flt and we want to fit into g.width if possible
            def f(x):
                return 4 + 9*x + 3
            while True:
                if f(w + 1) < g.width:
                    w += 1
                else:
                    break
            print(f"{'n':^2s}", end=" ")
            for s in "θ,° A/d² A/D² A/a² d/a D/a a/d a/D D/d".split():
                print(f"{s:^{w}s}", end=" ")
            print()
        if 1:   # Print table body
            # Get which sizes to print
            if opts["-n"]:
                sizes = list(sorted(int(i) for i in opts["-n"].split(",")))
            else:
                sizes = list(range(3, 11)) + [12, 15, 16, 20, 24, 32, 48, 60, 64]
            for n in sizes:
                colorize = n in opts["-c"]
                res = []
                K = pi/n
                res.append("{0:^2d}".format(n))
                res.append(F(2*K*180/pi, w))  # T
                res.append(F(n*tan(K)/4, w))  # A/d^2
                res.append(F(n*sin(2*K)/8, w))  # A/D^2
                res.append(F(n/(tan(K)*4), w))  # A/a^2
                doa, Doa = 1/tan(K), 1/sin(K)
                res.append(F(doa, w))  # d/a
                res.append(F(Doa, w))  # D/a
                res.append(F(1/doa, w))  # a/d
                res.append(F(1/Doa, w))  # a/D
                res.append(F(Doa/doa, w))  # D/d
                if colorize:
                    print(f"{t.hi}", end="")
                print(" ".join(res).rstrip())
                if colorize:
                    print(f"{t.N}", end="")
        if 1:  # Print formulas
            print()
            print(dedent('''
            Formulas:
            k = π/n                           T = 360*k/π
            a/d = tan(k)                      A/d² = n*tan(k)/4
            a/D = sin(k)                      A/D² = n*sin(2*k)/8
            D/d = 1/cos(k)                    A/a² = 4*n/tan(k)
    
            a = d*tan(k) = D*sin(k)
            r = d/2 = sqrt(R² - a²/4) = a/(tan(k)*2) = R*cos(k)
            R = D/2 = sqrt(r² + a²/4) = a/(sin(k)*2) = r/cos(k)
            A = n*a*r/2 = n*a/2*sqrt((D² - a²)/4)
                = n*a²*cot(k)/4 = n*r²*tan(k) = n*R²*sin(2*k)/2
            s = 2*sqrt(R^2 - r^2) = 2*r*tan(k)
            '''))
        print('\nRef:  Marks, "Std Hdbk for Mech Engrs", pg 1-39, 7th ed., 1967')
        exit(0)
    def LookForWords(diameters):
        '''Look for strings like 'tri', 'quad', etc. in the list of
        diameters and set the appropriate values in the -n option.  Remove
        these words and return the resultant remaining diameters.
        '''
        nums = {
            "tri": 3,
            "tet": 4,
            "qua": 4,
            "pen": 5,
            "hex": 6,
            "hep": 7,
            "sep": 7,
            "oct": 8,
            "non": 9,
            "dec": 10,
            "dod": 12,
        }
        found, dia = [], []
        for d in diameters:
            got_one = False
            for word in nums:
                if d.startswith(word):
                    found.append(nums[word])
                    got_one = True
                    break
            if not got_one:
                dia.append(d)
        if 0:
            print(f"diameters = {diameters}")
            print(f"found = {found}")
            print(f"dia   = {dia}")
            exit()
        if found:
            opts["-n"] = ",".join(str(i) for i in found)
        return dia
    def Title():
        print(dedent(f'''
        {t.ti}Properties of regular polygons to {opts["-d"]} figures{t.N}
            {t.insc}d = inscribed diameter{t.N}      r = inscribed radius
            {t.circ}D = circumscribed diameter{t.N}  R = circumscribed radius
            s = length of side   A = area   p = perimeter
        ''')
        )
    def GetColumnWidth(dstr):
        '''Put the column width necessary to print the table's columns in g.w.  The
        algorithm is to use opts["-d"] + 5, the number of decimal places + 5.  However,
        if dstr contains uncertainty, then each of the values to be printed must be
        examined.
        '''
        d = Convert(dstr)   # Convert to flt or ufloat
        if isinstance(d, flt):
            g.w = opts["-d"] + 5
        else:
            w = 0
            number_of_sides = [int(i) for i in opts["-n"].split(",")]
            for n in number_of_sides:
                w = max(w, Poly(dstr, n, leave_out="d", noprint=True))
            g.w = w
    def Report(dstr):
        '''Print the calculated values assuming the diameter string in dstr
        is first an inscribed diameter, then the circumscribed diameter.
        '''
        GetColumnWidth(dstr)
        def Header(circumscribed=False, leave_out=""):
            for s in "Sides d D s A p".split():
                if s == leave_out:
                    continue
                print(f"{t.hdr}{s:^{g.w}s}", end=" ")
            t.print()
            for n in number_of_sides:
                Poly(dstr, n, circumscribed, leave_out=leave_out)
        try:
            number_of_sides = [int(i) for i in opts["-n"].split(",")]
        except Exception:
            Error("'{0}' is bad -n option".format(opts["-n"]))
        try:
            dia = Convert(dstr)
        except Exception:
            dia = flt(eval(dstr))
        if 1:  # Print inscribed diameter
            if isinstance(dia, flt):
                print(f"\n{t.insc}d = {dstr!r} = {dia}, r = {dia/2}{t.N}")
            else:
                print(f"\n{t.insc}d = {dstr!r} = {dia:.1uS}, r = {dia/2:.1uS}{t.N}")
            Header(circumscribed=False, leave_out="d")
        if 1:  # Print circumscribed diameter
            if isinstance(dia, flt):
                print(f"\n{t.circ}d = {dstr!r} = {dia}, r = {dia/2}{t.N}")
            else:
                print(f"\n{t.circ}d = {dstr!r} = {dia:.1uS}, r = {dia/2:.1uS}{t.N}")
            Header(circumscribed=True, leave_out="D")
    def Poly1(s, n, circumscribed=False, leave_out="", noprint=False):
        '''Given the diameter in the string s, number of sides n, and options dictionary
        opts, calculate the parameters and print the table.  Leave out the indicated
        column (only will be d or D).  If noprint is True, return the calculated
        variables' maximum width.
        
        Definitions are:
            d = inscribed circle diameter
            D = circumscribed circle diameter
            s = perimeter
            A = area or surface area
            a = length of side
            r = radius of inscribed circle = d/2
            R = radius of circumscribed circle = D/2
            n = number of sides
        Equations are:
            theta = 2*pi/n = central angle subtended by side
            K = theta/2
            a = length of side = d*tan(K) = D*sin(K)
            r = sqrt(R^2 - a^2/4) = a*cot(K)/2 = R*cos(K)
            R = sqrt(r^2 + a^2/4) = a*csc(K)/2 = r*sec(K) = r/cos(K)
            A = n*a*r/2 = n*a/2*sqrt((D^2 - a^2)/4)
              = n*a^2*cot(K)/4 = n*r^2*tan(K) = n*R^2*sin(2*K)/2
            s = 2*sqrt(R^2 - r^2) = 2*r*tan(K)
        '''
        try:
            d = Convert(s)
        except Exception:
            Error(f"'{s}' is not a valid number")
        if 1:   # Check assumptions
            Assert(ii(d, (flt, int, Fraction, UFloat)))
            Assert(ii(n, int))
            Assert(n > 0)
        K = pi/n
        D = d/cos(K)
        if circumscribed:
            D = d
            d = D*cos(K)
        a = d*tan(K)
        A = n*a*d/4
        s = n*a
        colorize = n in opts["-c"]
        if colorize and not noprint:
            print(f"{t.hi}", end="")
        if leave_out == "d":
            L = (n, D, a, A, s)
        elif leave_out == "D":
            L = (n, d, a, A, s)
        else:
            Error(f"Program bug: leave_out = {leave_out!r}")
        if noprint:
            if "+/-" in str(d):
                # It's a ufloat, so use the shorthand string interpolation
                return max(len(f"{i:^.1uS}") for i in (d, D, a, A, s))
            else:
                # It's a flt
                return max(len(str(i)) for i in (d, D, a, A, s))
        # Now print the line
        for i, x in enumerate(L):
            w = opts["-d"] + 5
            if ii(x, UFloat):
                print(f"{x:^{g.w}.1uS}", end=" ")
            else:
                print(f"{x!s:^{g.w}s}", end=" ")
        if colorize:
            print(f"{t.N}", end="")
        print()
    def Poly(dia, n, circumscribed=False, leave_out="", noprint=False):
        '''Given the diameter in the string dia, number of sides n, and options dictionary
        opts, calculate the parameters and print the table.  Leave out the indicated
        column (only will be d or D).  If noprint is True, return the calculated
        variables' maximum width.
        
        Definitions are:
            d = inscribed circle diameter
            D = circumscribed circle diameter
            p = perimeter
            A = area or surface area
            s = length of side
            r = radius of inscribed circle = d/2
            R = radius of circumscribed circle = D/2
            n = number of sides
        Equations are:
            theta = 2*pi/n = central angle subtended by side
            K = theta/2
            s = length of side = d*tan(K) = D*sin(K)
            r = sqrt(R^2 - s^2/4) = s*cot(K)/2 = R*cos(K)
            R = sqrt(r^2 + s^2/4) = s*csc(K)/2 = r*sec(K) = r/cos(K)
            A = n*s*r/2 = n*s/2*sqrt((D^2 - s^2)/4)
              = n*s^2*cot(K)/4 = n*r^2*tan(K) = n*R^2*sin(2*K)/2
            p = 2*sqrt(R^2 - r^2) = 2*r*tan(K)
        '''
        try:
            diameter = Convert(dia)
        except Exception:
            Error(f"'{s}' is not a valid number")
        if 1:   # Check assumptions
            Assert(ii(diameter, (flt, int, Fraction, UFloat)))
            Assert(ii(n, int))
            Assert(n > 0)
        K = pi/n
        d = diameter    # d is inscribed diameter
        D = d/cos(K)
        if circumscribed:
            D = d
            d = D*cos(K)
        s = d*tan(K)
        A = n*s*d/4
        p = n*s
        colorize = n in opts["-c"]
        if colorize and not noprint:
            print(f"{t.hi}", end="")
        if leave_out == "d":
            L = (n, D, s, A, p)
        elif leave_out == "D":
            L = (n, d, s, A, p)
        else:
            Error(f"Program bug: leave_out = {leave_out!r}")
        if noprint:
            if "+/-" in str(d):
                # It's a ufloat, so use the shorthand string interpolation
                return max(len(f"{i:^.1uS}") for i in (d, D, s, A, p))
            else:
                # It's a flt
                return max(len(str(i)) for i in (d, D, s, A, p))
        # Now print the line
        for i, x in enumerate(L):
            w = opts["-d"] + 5
            if ii(x, UFloat):
                print(f"{x:^{g.w}.1uS}", end=" ")
            else:
                print(f"{x!s:^{g.w}s}", end=" ")
        if colorize:
            print(f"{t.N}", end="")
        print()

if __name__ == "__main__":
    opts = {}
    diameters = ParseCommandLine(opts)
    diameters = LookForWords(diameters)
    # Make sure we can convert the diameters
    for dia in diameters:
        try:
            d = Convert(dia)
        except Exception:
            Error(f"'{dia}' is not a valid number")
    if opts["-t"]:
        FormulaTable()
    Title()
    for d in diameters:
        Report(d)
        if len(diameters) > 1:
            print()
