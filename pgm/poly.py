'''

ToDo (higher priority items first)
    - Add option to generate and show a PostScript drawing for a particular number of
      sides.  This would be handy for shop documentation.

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
    import readline
    readline.set_startup_hook(input)
    import sys
    import os
    import getopt
    # Custom imports
    import termtables as tt     # Used for printing tables
    from cmddecode import CommandDecode
    from wrap import dedent
    from lwtest import Assert
    from color import TRM as t
    from f import (flt, acos, acosh, asin, asinh, atan, atanh, atan2, ceil, copysign,
        cos, cosh, degrees, e, erf, erfc, exp, expm1, fabs, factorial, floor, fmod,
        frexp, fsum, gamma, gcd, hypot, inf, isclose, isfinite, isinf, isnan, ldexp,
        lgamma, log, log10, log1p, log2, modf, nan, pi, pow, radians, remainder, sin,
        sinh, sqrt, tan, tanh, tau, trunc)
    try:
        from uncertainties import ufloat, ufloat_fromstr, UFloat
        from uncertainties.umath import sin as usin, sqrt as usqrt
        have_unc = True
    except ImportError:
        have_unc = False
    if 0:
        import debug
        debug.SetDebugger()
    # Global variables
    class g:
        pass
    π = pi
    g.width = int(os.environ.get("COLUMNS", 80)) - 1
    g.w = None      # Used for maximum column width of table
    g.dbg = False   # Print Dbg messages
    ii = isinstance
    # Used to indicate Convert() couldn't convert a string to a number
    class NotANumber(Exception): pass
if 1:  # Utility
    def GetColors(on):
        x = sys.stdout.isatty() if on else False
        t.ti = t("wht", attr="ul") if x else ""
        t.hi = t.brnl if x else ""
        t.hdr = t.redl if x else ""
        t.insc = t.purl if x else ""
        t.circ = t.trq if x else ""
        t.dbg = t.cyn if x else ""
        t.err = t.redl if x else ""
        t.warn = t.ornl if x else ""
        t.N = t.n if x else ""
        # Variables' colors
        t.d = t.ornl if x else ""
        t.D = t.cynl if x else ""
        t.r = t.royl if x else ""
        t.R = t.purl if x else ""
        t.s = t.yell if x else ""
        t.p = t.grnl if x else ""
        t.n_ = t.redl if x else ""
        t.A = t.magl if x else ""
        t.t = t.brnl if x else ""
        t.V = t.lipl if x else ""
        t.ϕ = t.cynl if x else ""
        t.θ = t.blul if x else ""
        # Dictionary to get symbol colors
        g.sym = {
            "n": f"{t.n_}n{t.n}",
            "d": f"{t.d}d{t.n}",
            "D": f"{t.D}D{t.n}",
            "r": f"{t.r}r{t.n}",
            "R": f"{t.R}R{t.n}",
            "s": f"{t.s}s{t.n}",
            "p": f"{t.p}p{t.n}",
            "A": f"{t.A}A{t.n}",
            "t": f"{t.t}t{t.n}",
            "V": f"{t.V}V{t.n}",
            "θ": f"{t.θ}θ{t.n}",
            "ϕ": f"{t.ϕ}ϕ{t.n}",
        }
    def C(sym):
        'Short name for getting symbol color'
        return g.sym[sym]
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        f = sys.stderr
        if hasattr(t, "err"):
            print(f"{t.err }", end="", file=f)
            t.print(*msg, file=f)
        else:
            print(*msg, file=f)
        exit(status)
    def Manpage():
        print(dedent(f'''

        This script calculates numerical properties of a regular polygon for diameters
        that you pass on the command line.  Because relevant diameters can be either the
        inscribed circle or the circumscribed circle, a report for both types is printed.
        You can input diameters as integers, floating point numbers, or fractions like
        '11/3' or '3-2/3'.

        If you have the python uncertainties library installed and a diameter is
        specified to have uncertainty (e.g. '3+-0.1', '3+/-0.1', '3±0.1', and '3.0(1)' are
        equivalent), the output will show the uncertainties in the computed numbers.

        Examples
            - Find the inscribed diameter of an octagon with area of 37.7 units.  A few
              iterations gives 6.746 and is accurate to about 4 figures.
                - Find this directly by using interactive mode with the -i option.  Type
                  'A' at the prompt, then enter 37.7.  Read d = 6.746 as the answer.
            - To two figures, when is the circumference of a regular polygon
              indistinguishable from one with one more side?  Use an inscribed diameter
              of 1.  "-n 'range(3, 100)' -d 2 1" shows it's 35 and 36 sides.

        Interactive mode (use -i option)
            
            This mode gives you an interactive calculator to solve for regular polygon
            characteristics.  

            Example:  find the side of a square with area 2.  
                - Start the program with the -i option.  
                - At the prompt 'd>>', type A.  This sets the variable to get the next
                  number typed in and you see the current values of the variables
                  printed out (they are all 0 and the number of sides is set to the
                  default of 4 (a square)).  
                - Enter the number 2 and the report will show that d, the inscribed
                  circle diameter is 1.41, which is the square root of 2 and the length
                  of the square's side.
                - To see more digits in the answer, type in 'N 6' and you'll see 1.41421
                  for d.  
                - To show that it's really the square root of 2, type in '!d**2' and
                  you'll get 2.  '!' evaluates the following expression and you can use
                  the problem's variables and the math functions like sin, cos, etc.

            If you type in a number with uncertainty, all the numbers of the problem are
            converted to have uncertainty (some may have a zero uncertainty until a new
            number is typed in to force a recalculation).  To go back to arithmetic with
            floats, use the 'C' command to revert to the initial state.

            Example:  I have some plate steel with a density of 7.86(5) g/mL.  The steel
            thickness is 14.1(2) mm.  If I make a hexagon with a side length of 420(5) mm
            (I'm cutting it with a torch), what will be the plate's mass?
                - Start the program with the -i option.  
                - At the prompt 'd>>', type s
                - Enter 420(5)
                - Enter t
                - Enter 14.1(2)
                

        '''))
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dia1 [dia2...]
          Print dimensions of regular polygons for given diameter(s) as either the
          inscribed or circumscribed circle diameter.  Read the manpage for the
          supported numbers.
         
          You can also use words like 'triangle', 'hexagon', etc. to identify the
          polygon(s) you're interested in.  The first three letters of the word are what
          are used for identification.  Thus, '{sys.argv[0]} 1.3 tri' causes the script
          to print out results for a triangle only; you'll see the inscribed and
          circumscribed diameters and radii, length of a side, perimeter, and area.
        Options:
          -a    Abbreviate numbers (remove trailing 0's and decimal point) [{opts["-a"]}]
          -C    Do not use color highlighting
          -D    Show debugging messages
          -d n  Number of digits to print [{opts["-d"]}]
          -H    Print a manpage
          -i    Start interactive session
          -n l  Which sides to print; must be a space-separated list of integers.
                [{opts["-n"]}]
          -r    For the -t option, divide by r and R
          -t    Produce a table of useful factors allowing you to calculate
                various parameters of polygons given certain dimensions.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Abbreviate numbers
        d["-C"] = False     # Do not use color highlighting
        d["-D"] = False     # Turn on debugging
        d["-d"] = 3         # Number of significant digits
        d["-i"] = False     # Start interactive session
        d["-n"] = "3-6 8"   # Number of sides to print
        d["-r"] = False     # Divide by r & R for -t
        d["-t"] = False     # Print the table
        try:
            opts, diameters = getopt.getopt(sys.argv[1:], "aCDd:hin:rt")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, arg in opts:
            if o[1] in "aCDirt":
                d[o] = not d[o]
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
                    d["-n"] = " ".join(str(i) for i in list(eval(arg)) if i > 2)
                else:
                    d["-n"] = arg
        if 1:   # Check all -n arguments
            o = []
            for i in d["-n"].split():
                try:
                    o.append(int(i))
                except Exception:
                    Error(f"{i!r} is bad -n option")
            d["-n"] = o
        GetColors(not d["-C"])
        if 1:   # Set up flt behavior
            x = flt(0)
            x.N = d["-d"]
            x.rtz = False
            x.rtdp = True
            if d["-a"] or d["-i"]:
                x.rtz = x.rtdp = True
            x.low = 1e-4
            x.high = 1e6
        if not d["-i"]:
            if not d["-t"] and not diameters:
                Usage()
        if d["-D"]:
            g.dbg = True
        if d["-i"]:
            Interactive()
            exit(0)
        return diameters
if 1:  # Regular polygon formulas
    '''This section contains the relevant formulas with definition of the symbols.
    It also contains test routines that validate the formulas.

    Angles are measured in radians.  My analytic geometry document is the reference
    along with the table in Marks, "Standard Handbook for Mechanical Engineers",
    McGraw-Hill, 7th ed., pg 1-39, 1967.  Symbols are

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

    Let T be the right triangle that is half the isoceles triangle formed by the
    circle's center and one side, with the radius making a right angle with the side.

    For practical work, r and R aren't convenient because they can't be conveniently
    measured unless you're working on a surface where you can use dividers and you can
    locate the center of the polygon's inscribed or circumscribed circle.  Thus, the
    formulas will be in terms of the diameters d and D.  If n is odd, you can't easily
    measure d or D either:  consider the pentagon like in a Penta-nut.  You use
    electronic or dial calipers and measure the distance from an internal vertex to the
    perpendicular point of the opposite side, which is r + R.  You'd do the same thing
    with the external jaws on a pentagon that would fit into this recess.  The formulas
    give r + R = R*(1 + cos(ϕ)) = r*(1 + 1/cos(ϕ)).

    Basic formula for length of side:  s = d*tan(ϕ)

        From triangle T, we get s = d*tan(ϕ).  There are 2*n of these basic triangles
        T making up the regular polygon.

    p = perimeter = n*s = n*d*tan(ϕ)

    A = area = n*s*d/4 = p*d/4

        The area of T is half the base times the height, or (1/2)*r*(s/2) = s*r/4.  The area
        of two of these triangles is s*r/2, which is the area of 1/n of the polyon
        because there are n of these triangles that make up the polygon.  Thus, the
        polygon's area is n*s*r/2 = n*s*d/4.

    Circumscribed diameter = D = s/sin(ϕ) = d/cos(ϕ)

    Inscribed diameter = d = s/tan(ϕ) = D*cos(ϕ)

    Table (like that in Marks)
        ϕ = π/n
        A/s² = n/(4*tan(ϕ))
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

    Use cases for an interactive polygon calculator
        - Polygon calculator
            - State allowed n values, e.g.:  3-6 8
                - !n gives default 3-12
                - n+ adds values
                - n- removes values
            - Enter one of d, D, r, R, s, p, A and see the calculated variables.
                - r and R are not shown by default unless you specify them.
                - Use !x to not show variable x, !! to show all variables
            - At the prompt, you enter new values of the last variable and see the
              changes.  Enter a new variable name and that variable gets the focus.
              This will let you iterate to find a desired solution.

        - Mass problem
            - Choose material.  Given t = thickness and n, enter one of d, D, s, p, A.
              Calculate resulting mass.

    Equations
        ϕ = π/n = 2*θ
        cos(ϕ) = d/D
        d = 2*r = s/tan(ϕ) = D*cos(ϕ)
        D = 2*R = s/sin(ϕ) = d/cos(ϕ)
        A = n*s*d/4 = p*d/4 = n*D**2*sin(2*ϕ)/8
          = n*d**2*tan(ϕ)/4 = n*s**2/(4*tan(ϕ))
        p = n*s = n*d*tan(ϕ)
        s = d*tan(ϕ) = D*sin(ϕ)

    Functional forms
        ϕ: (n), (d, D), (d, s), (D, s), (n, D, A), (n, d, A), (n, s, A) (n, d, p)

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
     1 d, s     tan(ϕ) = s/d
     2 d, p     p = n*d*tan(ϕ)
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
    def Convert(s):
        '''Return the string s as a flt or ufloat.  The string form can be an integer,
        flt, or fraction of e.g. the forms 7/8 or 1-7/8.  A ufloat can be e.g.:
            1+-.1
            1+/-.1
            1±.1
            1.0(1)
        '''
        try:
            if "+-" in s:    # It's a ufloat
                return ufloat_fromstr(s.replace("+-", "+/-"))
            elif "+/-" in s or "±" in s or ("(" in s and ")" in s): # It's a ufloat
                return ufloat_fromstr(s)
            elif "/" in s:   # It's a fraction
                ip = 0
                num, denom = s.split("/")
                if "-" in num:
                    ip, num = num.split("-")
                num, denom, ip = [int(i) for i in (num, denom, ip)]
                return flt(Fraction(num + ip*denom, denom))
            else:   # It's a float
                return flt(s)
        except ZeroDivisionError:
            raise
        except Exception:
            raise NotANumber
    def FormulaTable():
        '''Print a table similar to the table on page 1-39 of Mark's "Standard Handbook
        for Mechanical Engineers", 7th ed., 1967.
        
        Check of formulas:  I drew a 6" diameter circle and used a 30-60-90 triangle
        to draw a hexagon around it.  The measurements agreed with the values
        calculated with the table to better than 0.1%.
        '''
        # Header
        print(dedent(f'''
                             {t.ti}Regular polygons{t.n}
        {C('d')} = inscribed circle diameter       
        {C('D')} = circumscribed circle diameter
        {C('A')} = area     {C('p')} = perimeter     {C('s')} = length of one side
        {C('θ')} = angle subtended by side = 2{C('ϕ')}
        '''))
        print()
        # Print table body
        if opts["-r"]:
            header = f'''{C('n')} {C('θ')},° {C('ϕ')},° {C('A')}/{C('r')}²
                            {C('A')}/{C('R')}² {C('A')}/{C('s')}² {C('s')}/{C('r')}
                            {C('s')}/{C('R')} {C('p')}/{C('r')} {C('p')}/{C('R')}'''.split()
        else:
            header = f'''{C('n')} {C('θ')},° {C('ϕ')},° {C('A')}/{C('d')}²
                            {C('A')}/{C('D')}² {C('A')}/{C('s')}² {C('s')}/{C('d')}
                            {C('s')}/{C('D')} {C('p')}/{C('d')} {C('p')}/{C('D')}'''.split()
        o, use_r = [], opts["-r"]
        # In the table, we assume the inscribed circle is a unit circle
        r = flt(1)
        for n in [int(i) for i in opts["-n"].split()]:
            colorize = n in opts["-c"]
            row = []
            ϕ = π/n
            R = r/cos(ϕ)
            d = 2*r
            D = 2*R
            s = D*sin(ϕ)
            A = n*s*r/2
            p = n*s
            if 0 and n == 3:
                # Debug print
                print(f"{t.sky}n = {n}, ϕ = {degrees(ϕ)}, r = {r}, R = {R}, d = {d}, D = {D}, s = {s}, A = {A}, p = {p}")
                if use_r:
                    print(f"A/r² = {A/r**2}, A/R² = {A/R**2}, A/s² = {A/s**2}, s/r = {s/r}, s/R = {s/R}, p/r = {p/r}, p/R = {p/R}")
                else:
                    print(f"A/d² = {A/d**2}, A/D² = {A/D**2}, A/s² = {A/s**2}, s/d = {s/d}, s/D = {s/D}, p/d = {p/d}, p/D = {p/D}")
                t.print()
            row.append(f"{n}")              # n
            row.append(f"{2*degrees(ϕ)}")   # θ in °
            row.append(f"{degrees(ϕ)}")     # ϕ in °
            if use_r:
                row.append(f"{A/r**2}")     # A/r^2
                row.append(f"{A/R**2}")     # A/R^2
                row.append(f"{A/s**2}")     # A/s^2
                row.append(f"{s/r}")        # s/r
                row.append(f"{s/R}")        # s/R
                row.append(f"{p/r}")        # p/r
                row.append(f"{p/R}")        # p/R
            else:
                row.append(f"{A/d**2}")     # A/d^2
                row.append(f"{A/D**2}")     # A/D^2
                row.append(f"{A/s**2}")     # A/s^2
                row.append(f"{s/d}")        # s/d
                row.append(f"{s/D}")        # s/D
                row.append(f"{p/d}")        # p/d
                row.append(f"{p/D}")        # p/D
            o.append(row)
        tt.print(o, header=header, padding=(0, 0), style=tt.styles.thin_double, alignment="c"*10)
        # Print formulas
        print()
        if 0:
            print(dedent(f'''
            Formulas:           {C('ϕ')} = π/{C('n')} = {C('θ')}/2
            {C('s')}/{C('d')} = tan({C('ϕ')})                      {C('A')}/{C('d')}² = {C('n')}*tan({C('ϕ')}/4)
            {C('s')}/{C('D')} = sin({C('ϕ')})                      {C('A')}/{C('D')}² = {C('n')}*sin(2*{C('ϕ')}/8)
            {C('d')}/{C('D')} = cos({C('ϕ')})                      {C('A')}/{C('s')}² = 4*{C('n')}/tan({C('ϕ')})

            {C('s')} = {C('d')}*tan({C('ϕ')}) = {C('D')}*sin({C('ϕ')})
            {C('r')} = {C('d')}/2 = sqrt({C('R')}² - {C('s')}²/4) = {C('s')}/(2*tan({C('ϕ')})) = {C('R')}*cos({C('ϕ')})
            {C('R')} = {C('D')}/2 = sqrt({C('r')}² + {C('s')}²/4) = {C('s')}/(2*sin({C('ϕ')})) = {C('r')}/cos({C('ϕ')})
            {C('A')} = {C('n')}*{C('s')}*{C('r')}/2 = {C('n')}*{C('s')}/2*sqrt(({C('D')}² - {C('s')}²)/4)
                = {C('n')}*{C('s')}²*cot({C('ϕ')}/4) = {C('n')}*{C('r')}²*tan({C('ϕ')}) = {C('n')}*{C('R')}²*sin(2*{C('ϕ')}/2)
            {C('p')} = 2*sqrt({C('R')}^2 - {C('r')}^2) = 2*{C('r')}*tan({C('ϕ')})
            '''))
        else:
            # The above comes out looking like fruit salad
            print(dedent(f'''
            {t.ti}Formulas{t.n}:           ϕ = π/n = θ/2
            s/d = tan(ϕ)                      A/d² = n*tan(ϕ/4)
            s/D = sin(ϕ)                      A/D² = n*sin(2*ϕ/8)
            d/D = cos(ϕ)                      A/s² = 4*n/tan(ϕ)

            s = d*tan(ϕ) = D*sin(ϕ)
            r = d/2 = sqrt(R² - s²/4) = s/(2*tan(ϕ)) = R*cos(ϕ)
            R = D/2 = sqrt(r² + s²/4) = s/(2*sin(ϕ)) = r/cos(ϕ)
            A = n*s*r/2 = n*s/2*sqrt((D² - s²)/4)
                = n*s²*cot(ϕ/4) = n*r²*tan(ϕ) = n*R²*sin(2*ϕ/2)
            p = 2*sqrt(R^2 - r^2) = 2*r*tan(ϕ)
            '''))
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
    def Title():
        print(dedent(f'''
        {t.ti}Properties of regular polygons{t.n}
            {C('d')} = inscribed diameter      {C('r')} = inscribed radius
            {C('D')} = circumscribed diameter  {C('R')} = circumscribed radius
            {C('s')} = length of side   {C('A')} = area   {C('p')} = perimeter
        '''))
    def Report(dstr):
        '''Print the calculated values assuming the diameter string in dstr is first an
        inscribed diameter, then the circumscribed diameter.
        '''
        try:
            dia = Convert(dstr)
        except Exception:
            dia = flt(eval(dstr))
        table_lines, v = [], " "*2
        style = "               "
        number_of_sides = opts["-n"]
        if 1:  # Print inscribed diameter
            if isinstance(dia, flt):
                print(f"\n{v}{t.d}d{t.n} = {dstr!r} = {dia}, r = {dia/2}")
            else:
                print(f"\n{v}{t.d}d{t.n} = {dstr!r} = {dia:.1uS}, r = {dia/2:.1uS}")
            # Now print the table
            hdr = [f"{C('n')}", f"{C('D')}", f"{C('s')}", f"{C('A')}", f"{C('p')}"]
            for n in number_of_sides:
                u = tuple([" " + i + " " for i in Poly(dstr, n, circumscribed=False)])
                table_lines.append(u)
            tt.print(table_lines, header=hdr, padding=(0, 0), style=style, alignment="c"*5)

        if 1:  # Print circumscribed diameter
            if isinstance(dia, flt):
                print(f"\n{v}{t.D}D{t.n} = {dstr!r} = {dia}, r = {dia/2}")
            else:
                print(f"\n{v}{t.D}D{t.n} = {dstr!r} = {dia:.1uS}, r = {dia/2:.1uS}")
            # Now print the table
            hdr = [f"{C('n')}", f"{C('d')}", f"{C('s')}", f"{C('A')}", f"{C('p')}"]
            table_lines.clear()
            for n in number_of_sides:
                u = tuple([" " + i + " " for i in Poly(dstr, n, circumscribed=False)])
                table_lines.append(u)
            tt.print(table_lines, header=hdr, padding=(0, 0), style=style, alignment="c"*5)
    def Poly(dia, n, circumscribed=False):
        '''Return (n, d or D, s, A, p) where each element is the corresponding variable's
        string.  dia is a flt and is the inscribed circle diameter if circumscribed is
        False and the circumscribed circle diameter if True.  n is the integer number of
        sides.  
        
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
            θ = 2*π/n = central angle subtended by side
            ϕ = θ/2
            s = length of side = d*tan(ϕ) = D*sin(ϕ)
            r = sqrt(R^2 - s^2/4) = s*cot(ϕ)/2 = R*cos(ϕ)
            R = sqrt(r^2 + s^2/4) = s*csc(ϕ)/2 = r*sec(ϕ) = r/cos(ϕ)
            A = n*s*r/2 = n*s/2*sqrt((D^2 - s^2)/4)
              = n*s^2*cot(ϕ)/4 = n*r^2*tan(ϕ) = n*R^2*sin(2*ϕ)/2
            p = 2*sqrt(R^2 - r^2) = 2*r*tan(ϕ)
        '''
        try:
            diameter = Convert(dia)
        except Exception:
            Error(f"'{s}' is not a valid number")
        if 1:   # Check assumptions
           Assert(ii(diameter, (flt, int, Fraction, UFloat)))
           Assert(ii(n, int))
           Assert(n > 0)
        is_uncertain = True if ii(diameter, UFloat) else False
        # Calculate regular polygon's properties
        ϕ = π/n
        d = diameter    # d is inscribed diameter
        D = d/cos(ϕ)
        if circumscribed:
            D = d
            d = D*cos(ϕ)
        s = d*tan(ϕ)
        A = n*s*d/4
        p = n*s
        # 
        o = []
        o.append(f"{n}")
        if circumscribed:
            o.append(f"{d:.1uS}" if ii(d, UFloat) else f"{d}")
        else:
            o.append(f"{D:.1uS}" if ii(D, UFloat) else f"{D}")
        o.append(f"{s:.1uS}" if ii(s, UFloat) else f"{s}")
        o.append(f"{A:.1uS}" if ii(A, UFloat) else f"{A}")
        o.append(f"{p:.1uS}" if ii(p, UFloat) else f"{p}")
        return tuple(o)
if 1:  # Interactive
    def Help(cmd):
        print(f"Help on {cmd!r}")
    def Process(cmd, args, vars):
        print(f"Process {cmd!r} {args!r}")
    def Print(vars):
        'Print the current variables'
        current = vars["current"]
        n = vars["n"]
        ϕ = vars["phi"] = phi = π/n
        Cos, S, T = cos(ϕ), sin(ϕ), tan(ϕ)
        if current == "d":
            d = vars["d"]
            t_ = vars["t"]
            r = d/2
            D = d/Cos
            R = D/2
            s = d*T
            p = n*s
            A = p*d/4
            V = A*t_
        elif current == "D":
            D = vars["D"]
            t_ = vars["t"]
            R = D/2
            d = D*Cos
            r = d/2
            s = d*T
            p = n*s
            A = p*d/4
            V = A*t_
        elif current == "r":
            r = vars["r"]
            t_ = vars["t"]
            d = 2*r
            D = d/Cos
            R = D/2
            s = d*T
            p = n*s
            A = p*d/4
            V = A*t_
        elif current == "R":
            R = vars["R"]
            t_ = vars["t"]
            D = 2*r
            d = D*Cos
            r = d/2
            s = d*T
            p = n*s
            A = p*d/4
            V = A*t_
        elif current == "A":
            A = vars["A"]
            t_ = vars["t"]
            D = usqrt(8*A/(n*usin(2*ϕ))) if vars["unc"] else sqrt(8*A/(n*sin(2*ϕ)))
            R = D/2
            d = D*Cos
            r = d/2
            s = d*T
            p = n*s
            V = A*t_
        elif current == "s":
            s = vars["s"]
            t_ = vars["t"]
            p = n*s
            d = s/T
            D = d/Cos
            r = d/2
            R = D/2
            A = n*s*d/4
            V = A*t_
        elif current == "p":
            p = vars["p"]
            t_ = vars["t"]
            s = p/n
            d = s/T
            D = d/Cos
            r = d/2
            R = D/2
            A = n*s*d/4
            V = A*t_
        elif current == "t":
            t_ = vars["t"]
            A = vars["A"]
            if A:
                V = A*t_
                D = usqrt(8*A/(n*usin(2*ϕ))) if vars["unc"] else sqrt(8*A/(n*sin(2*ϕ)))
                R = D/2
                d = D*Cos
                r = d/2
                s = d*T
                p = n*s
            else:
                V = D = R = d = r = s = p = 0
        elif current == "V":
            t_ = vars["t"]
            V = vars["V"]
            if V:
                A = V*t_
                D = usqrt(8*A/(n*usin(2*ϕ))) if vars["unc"] else sqrt(8*A/(n*sin(2*ϕ)))
                R = D/2
                d = D*Cos
                r = d/2
                s = d*T
                p = n*s
            else:
                A = D = R = d = r = s = p = 0
        else:
            Error(f"{current!r} is an invalid current variable in Print()")
        # Update the vars dict
        for i in "d D r R s p A".split():
            exec(f"vars['{i}'] = {i}")
        # Print the values of the variables
        o = []
        pad = lambda x, n: " "*n + x + " "*n
        # In the following, note that t is the color.TRM instance and t_ is the local
        # variable for thickness.
        def f(x, name):
            'Return x colored & formatted'
            a = "t." + name
            if name == "n":
                a = "t.n_"
            c = eval(a)
            if ii(x, UFloat):
                s = f"{x:.1uS}"
            else:
                s = f"{x}"
            return f"{c}{name}{t.whtl} = {s}{t.n}"

        # Make table
        # Row 1:  d, D, r, R
        row = []
        row.append(f(d, "d"))
        row.append(f(D, "D"))
        row.append(f(r, "r"))
        row.append(f(R, "R"))
        row = [pad(i, 2) for i in row]
        o.append(row)

        # Row 2:  n, A, s, p
        row = []
        row.append(f(n, "n"))
        row.append(f(A, "A"))
        row.append(f(s, "s"))
        row.append(f(p, "p"))
        row = [pad(i, 2) for i in row]
        o.append(row)
        # Row 3:  t, V, r+R
        row = []
        row.append(f(t_, "t"))
        row.append(f(V, "V"))
        if n % 2:
            # This case has to be handled specially
            s = f"{C('r')}+{C('R')} = "
            x = r + R
            s += f"{x:.1uS}" if ii(x, UFloat) else f"{x}"
            row.append(s)
        else:
            row.append("")
        row.append("")
        row = [pad(i, 2) for i in row]
        o.append(row)
        # Print the table
        tt.print(o, header=None, padding=(0, 0), style=" "*15, alignment="l"*4)
    def Variables():
        print(dedent(f'''
          {C('d')} Diameter of inscribed circle         {C('n')} Number of sides in polygon
          {C('D')} Diameter of circumscribed circle     {C('A')} Area
          {C('r')} Radius of inscribed circle           {C('s')} Length of side
          {C('R')} Radius of circumscribed circle       {C('p')} Perimeter
          {C('t')} Thickness of polygon plate           {C('V')} Volume of plate
        '''))
        print()
    def Interactive():
        'Start an interactive session'
        z, one = flt(0), flt(1)
        init = {    # Dictionary of regular polygon's variables
            "unc": False,   # Flags using numbers with uncertainty
            "current": "d",
            "d": z,     # Inscribed diameter
            "D": z,     # Circumscribed diameter
            "r": z,     # Inscribed radius
            "R": z,     # Inscribed radius
            "n": 6,     # Number of sides
            "A": z,     # Area
            "s": z,     # Side
            "p": z,     # Perimeter
            "t": z,     # Thickness of polygon plate
            "V": z      # Volume of polygon plate
            }
        vars = init.copy()
        prompt = ">> "
        print(f"{t(attr='ul')}Calculation of regular polygon properties{t.n}    Use ? for help")
        if 0:
            exit()#xx
        while True:
            user_input = input(f"{C(vars['current'])}" + prompt).strip()
            match user_input.split():
                case ["d"] | ["D"] | ["r"] | ["R"] | ["A"] | ["s"] | ["p"] | ["t"] | ["V"]:
                    # Switch the current variable that gets the input focus
                    Dbg(f"command = {user_input!r}")
                    vars["current"] = user_input[0]
                    Print(vars)
                case ["n", arg]:    # Set number of sides of polygon
                    Dbg(f"command = {user_input!r}")
                    try:
                        n = int(arg)
                        if n < 3:
                            t.print(f"{t.err}n must be 3 or greater")
                        else:
                            vars["n"] = n
                        Print(vars)
                    except Exception:
                        t.print(f"{t.err}{arg!r} is not an integer")
                case ["N", arg]:    # Set number of digits in floating point numbers
                    Dbg(f"command = {user_input!r}")
                    try:
                        n = int(arg)
                        if not (1 <= n <= 15):
                            t.print(f"{t.err}N must be an integer between 1 and 15")
                        else:
                            vars["d"].N = n
                        Print(vars)
                    except ValueError:
                        t.print(f"{t.err}{arg!r} is not an integer")
                case ["C"]:     # Set vars to initial state
                    Dbg("command = clear")
                    vars = init.copy()
                    Print(vars)
                case ["z"]:     # Toggle whether flt instances remove trailing zeros
                    Dbg("command = z")
                    x = flt(0)
                    x.rtz = not x.rtz
                    Print(vars)
                case ["q"]:     # Quit
                    exit(0)
                case ["."]:     # Show the current value of the variables
                    Dbg("command = .")
                    Print(vars)
                case ["?"]:     # Show help
                    Dbg("command = ?")
                    Variables()
                    print("Command summary:")
                    print("  d  D  r  R  A  s  p     Set variable that gets next entered number")
                    print("  n integer               Set number of polygon sides")
                    print("  C                       Reset to starting state")
                    print("  .                       Print values of variables")
                    print("  N digits                Set number of digits to show")
                    print("  z                       Toggle remove trailing zeros")
                    print("  ! expr                  Evaluate an expression")
                    print("  ? cmd                   Help on cmd")
                    print("  q                       Quit")
                case ["?", arg]:    # Show help on a command
                    Dbg(f"command = ? {arg}")
                    Help(arg)
                case _:
                    if user_input[0] == "!":    # Expression to evaluate
                        Dbg(f"command = {user_input}")
                        try:
                            print(f"{eval(user_input[1:], globals(), vars)}")
                        except Exception as e:
                            print(f"{t.err}Exception:  {e}")
                    elif user_input[0] == "=":  # Set current variable to expression
                        try:
                            x = eval(user_input[1:].strip(), globals(), vars)
                            if ii(x, flt):
                                if x <= 0:
                                    print(f"{t.err}Expression result must be > 0")
                                else:
                                    vars[vars["current"]] = x
                            else:
                                if x.n <= 0:
                                    print(f"{t.err}Expression result must be > 0")
                                else:
                                    vars[vars["current"]] = x
                                    ConvertToUfloat(vars)
                        except Exception as e:
                            print(f"{t.err}Exception:  {e}")
                        Print(vars)
                    else:
                        try:
                            # See if it's a number
                            number = Convert(user_input)
                            Dbg(f"Got number = {number}")
                            if ii(number, UFloat):
                                if number.n <= 0:
                                    t.print(f"{t.err}Number must be 0 or larger")
                                vars[vars["current"]] = number
                                ConvertToUfloat(vars)
                            else:
                                if number <= 0:
                                    t.print(f"{t.err}Number must be 0 or larger")
                                else:
                                    if ii(vars["current"], UFloat):
                                        # Keep it a ufloat but make the uncertainty zero
                                        vars[vars["current"]] = ufloat(number, 0)
                                    else:
                                        vars[vars["current"]] = number
                            Print(vars)
                        except ZeroDivisionError:
                            print(f"{t.err}Exception:  division by zero")
                        except NotANumber:
                            Dbg(f"command = _ = {user_input!r} fall through")
                            print(f"{t.warn}{user_input!r} not recognized")
    def ConvertToUfloat(vars):
        'Convert all of vars to ufloats (current already is one)'
        # Note this is OK, as current was just set and we'll recalculate everything else
        Assert(ii(vars[vars["current"]], UFloat))
        names = set("d D r R A s p t V".split())
        names.remove(vars["current"])
        for i in names:
            x = vars[i]
            if not ii(x, UFloat):
                vars[i] = ufloat(x, 0)
        vars["unc"] = True  # Flag that we're using uncertainty

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
    else:
        Title()
        for d in diameters:
            Report(d)
            if len(diameters) > 1:
                print()
