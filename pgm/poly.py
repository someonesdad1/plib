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
    import termtables as tt     # Used for printing tables
    from wrap import dedent
    from lwtest import Assert
    from color import TRM as t
    from f import flt, pi as π, sqrt, sin, cos, tan, degrees
    from uncertainties import ufloat, ufloat_fromstr, UFloat
    if 1:
        import debug
        debug.SetDebugger()
    # Global variables
    class g:
        pass
    g.width = int(os.environ.get("COLUMNS", 80)) - 1
    g.w = None      # Used for maximum column width of table
    ii = isinstance
if 1:  # Utility
    def GetColors():
        x = sys.stdout.isatty()
        t.ti = t.ornl if x else ""
        t.hi = t.brnl if x else ""
        t.hdr = t.redl if x else ""
        t.insc = t.purl if x else ""
        t.circ = t.trq if x else ""
        t.N = t.n if x else ""
        # Variables' colors
        t.n_ = t.redl if x else ""
        t.d = t.whtl if x else ""
        t.D = t.purl if x else ""
        t.r = t.royl if x else ""
        t.R = t.olvl if x else ""
        t.s = t.yell if x else ""
        t.p = t.grnl if x else ""
        t.A = t.magl if x else ""
        t.ϕ = t.cynl if x else ""
        t.θ = t.lipl if x else ""
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
            "θ": f"{t.θ}θ{t.n}",
            "ϕ": f"{t.ϕ}ϕ{t.n}",
        }
    def C(sym):
        'Short name for getting symbol color'
        return g.sym[sym]
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
          -n l  Which sides to print; must be a space-separated list of integers.
                [{opts["-n"]}]
          -r    For the -t option, divide by r and R
          -t    Produce a table of useful factors allowing you to calculate
                various parameters of polygons given certain dimensions.
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Abbreviate numbers
        d["-c"] = ""        # Which lines to highlight
        d["-d"] = 4         # Number of significant digits
        d["-n"] = " ".join(str(i) for i in range(3, 13))
        d["-r"] = False     # Divide by r & R for -t
        d["-t"] = False     # Print the table
        try:
            opts, diameters = getopt.getopt(sys.argv[1:], "ac:d:hn:rt")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, arg in opts:
            if o[1] in "art":
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
        GetColors()
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
        '''Print the calculated values assuming the diameter string in dstr
        is first an inscribed diameter, then the circumscribed diameter.
        '''
        try:
            number_of_sides = [int(i) for i in opts["-n"].split()]
        except Exception:
            Error("'{0}' is bad -n option".format(opts["-n"]))
        try:
            dia = Convert(dstr)
        except Exception:
            dia = flt(eval(dstr))
        if 0:
            # Original method
            GetColumnWidth(dstr)
            def Header(circumscribed=False, leave_out=""):
                for s in "n d D s A p".split():
                    if s == leave_out:
                        continue
                    print(f"{t.hdr}{s:^{g.w}s}", end=" ")
                t.print()
                for n in number_of_sides:
                    Poly(dstr, n, circumscribed, leave_out=leave_out)
            if 1:  # Print inscribed diameter
                if isinstance(dia, flt):
                    print(f"\n{t.d}d{t.n} = {dstr!r} = {dia}, r = {dia/2}")
                else:
                    print(f"\n{t.d}d{t.n} = {dstr!r} = {dia:.1uS}, r = {dia/2:.1uS}")
                Header(circumscribed=False, leave_out="d")
            if 1:  # Print circumscribed diameter
                if isinstance(dia, flt):
                    print(f"\n{t.D}D{t.n} = {dstr!r} = {dia}, r = {dia/2}")
                else:
                    print(f"\n{t.D}D{t.n} = {dstr!r} = {dia:.1uS}, r = {dia/2:.1uS}")
                Header(circumscribed=True, leave_out="D")
        else:   # Using texttable
            table_lines = []
            style = " │             "
            if 1:  # Print inscribed diameter
                if isinstance(dia, flt):
                    print(f"\n{t.d}d{t.n} = {dstr!r} = {dia}, r = {dia/2}")
                else:
                    print(f"\n{t.d}d{t.n} = {dstr!r} = {dia:.1uS}, r = {dia/2:.1uS}")
                # Now print the table
                hdr = [f"{C('n')}", f"{C('D')}", f"{C('s')}", f"{C('A')}", f"{C('p')}"]
                for n in number_of_sides:
                    u = tuple([" " + i + " " for i in Poly(dstr, n, circumscribed=False)])
                    table_lines.append(u)
                tt.print(table_lines, header=hdr, padding=(0, 0), style=style, alignment="c"*5)

            if 1:  # Print circumscribed diameter
                if isinstance(dia, flt):
                    print(f"\n{t.D}D{t.n} = {dstr!r} = {dia}, r = {dia/2}")
                else:
                    print(f"\n{t.D}D{t.n} = {dstr!r} = {dia:.1uS}, r = {dia/2:.1uS}")
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

    def Poly_(dia, n, circumscribed=False, leave_out="", noprint=False):
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
        ϕ = π/n
        d = diameter    # d is inscribed diameter
        D = d/cos(ϕ)
        if circumscribed:
            D = d
            d = D*cos(ϕ)
        s = d*tan(ϕ)
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
    else:
        Title()
        for d in diameters:
            Report(d)
            if len(diameters) > 1:
                print()
