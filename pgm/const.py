"""
Display values of physical constants
    Requires /plib/pgm/constants.codata.2018 for data
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Display values of physical constants
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from functools import partial
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from get import GetLines
        from lwtest import Assert
        from uncertainties import ufloat, UFloat, ufloat_fromstr
        from u import u, FormatUnit
        from roundoff import SigFig
    if 1:  # Global variables

        class G:
            pass

        g = G()  # Storage for global variables as attributes
        if 1:  # Debugging helpers
            g.dbg = False
            t.dbg = t("lill") if g.dbg else ""
        ii = isinstance
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
        # Hold the data: key = number in list, value = (name, constant, physical_unit)
        g.data = {}
        # Most important constants to print by default
        g.important = set(
            int(i)
            for i in """
            1 9 22 37 42 43 48 49 53 73 83 94 111 119 121 191 236 243 253
            258 265 275 296 317 318 319 320 321 347 348 
        """.split()
        )
if 1:  # Utility

    def GetColors():
        c = bool(d["-c"])
        if c:
            t.always = True
        t.nodim = t("skyl") if c else ""  # Dimensionless numbers
        t.exact = t("grnb") if c else ""  # Exact numbers
        t.err = t("redl") if c else ""  # Error
        t.N = t.n if c else ""

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Manpage():
        print(
            dedent(
                f"""
        The constants come from [1] and were downloaded 28 Aug 2021; they represent the 2018
        CODATA adjustments.
 
        The number of digits given in the constants are controlled by the -d option.  Its default
        value of {d["-d"]} is what I use the most, as I rarely need more figures.  However, the
        numbers that are not defined as exact have an associated uncertainty.  You can see the
        constant with its uncertainty in the standard short form by setting the -d option to 0.
        I have arbitrarily limited the maximum value of the -d option to 10.  If you ask for more,
        it's equivalent to setting the -d option to 0.
 
        The units are in SI and you can use the -u option to see them formatted in different
        forms.  Form number 3 is handy as long as you remember that everything to the right of the
        double solidus is in the denominator.  Form number 1 is useful when you need a python
        expression.  Form number 2 is commonly seen in technical papers.
 
        If you use the -e option, you'll see numbers like '1.23e7 m' written as '12.3 Mm'.  You
        may see some non-SI forms, such as '602 Z1/mol' for Avogadro's constant (the correct form
        would be '1/zmol', but the meaning should be clear.  Though it's incorrect SI syntax,
        you'll also see SI prefixes for dimensionless numbers because it's handy to quickly get a
        feel for the magnitude.  If you use the -E option, the absolute power of 10 of the number
        must be 12 or less for an SI prefix to be used.  This is because it's sometimes hard to
        remember some of the SI prefixes that are very small or large.

        Color coding is used to flag exact and dimensionless values.  Warning:  if -d is not set
        to 0, the values flagged as exact are only exact to the number of digits in -d.  Set -d to
        0 to see the exact number.
 
        References
            [1] https://physics.nist.gov/cuu/Constants/Table/allascii.txt

        """.rstrip()
            )
        )
        exit(0)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [regex1 [regex2...]]
          With no arguments, print out common physical constants.  If arguments are given, they
          are regular expressions to print out constants that the regexs match (they are OR'd
          together and the search is case-insensitive).
        Options:
            -a      Show all constants
            -c      Use color in output
            -d n    Set number of digits [{d["-d"]}].  Use 0 to see uncertainty.
            -H      Print a manpage
            -u n    Select units format [{d["-u"]}]
                      0 = kg·m/(s²·K)
                      1 = kg*m/(s**2*K)
                      2 = kg·m·s⁻²·K⁻¹
                      3 = kg·m//s²·K
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Show all constants
        d["-c"] = False  # Use color in output
        d["-d"] = 3  # Digits
        d["-u"] = 0  # Unit formatting
        try:
            opts, args = getopt.getopt(sys.argv[1:], "acd:Hhu:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ac"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if d[o] > 10:
                        d[o] = 0
                    else:
                        if not (0 <= d[o] <= 10):
                            raise ValueError()
                except ValueError:
                    Error("-d option's argument must between 0 and 10")
            elif o == "-u":
                try:
                    d[o] = int(a)
                    if not (0 <= d[o] <= 3):
                        raise ValueError()
                except ValueError:
                    Error("-u option's argument must between 0 and 3")
            elif o == "-H":
                Manpage()
            elif o == "-h":
                Usage(status=0)
        x = flt(0)
        x.low = 0.01
        x.high = 99999.99999
        x.u = True
        if not d["-d"]:
            flt(0).N = 1  # Avoid a software problem
        GetColors()
        return args


if 1:  # Core functionality

    def GetData():
        """Split into the following fields:
        Name of constant    0-59
        Value               60-84
        Uncertainty         85-109
        Unit                110-end
        """
        file = "/plib/pgm/constants.codata.2018"
        lines = GetLines(file, script=True, ignore_empty=True, strip=True, nonl=True)
        # Put data into dict g.data
        for line in lines:
            # Strip off integer
            num, line = line.split("\t")
            num = int(num)
            name = line[0:60].strip()
            value = line[60:85].strip().replace(" ", "").replace("...", "")
            unc = line[85:110].strip().replace(" ", "").replace("(exact)", "0")
            unit = line[110:].strip().replace("^", "")
            sigfig = SigFig(float(value), clamp=False)
            x = ufloat(float(value), float(unc))
            if unit:
                if 1:  # Function to format the unit
                    choice = d["-u"]
                    if choice == 0:  # Standard form                     kg·m/(s²·K)
                        F = partial(FormatUnit)
                    elif choice == 1:  # Expression form (valid python)    kg*m/(s**2*K)
                        F = partial(FormatUnit, expr=True)
                    elif choice == 2:  # Flat formatting as used by NIST   kg·m·s⁻²·K⁻¹
                        F = partial(FormatUnit, flat=True)
                    elif choice == 3:  # Solidus form                      kg·m//s²·K
                        F = partial(FormatUnit, solidus=True)
                if unit == "u":
                    unit = "amu"
                un = u(unit)  # Will get exception on bad unit string
                g.data[num] = (name, x, F(unit), sigfig)
            else:
                g.data[num] = (name, x, "", sigfig)

    def Fmt(item):
        """Format the constant item to be a left-justified string with
        attached unit.  item is a tuple (name, x, unit, sigfig) with
        name a string, x a ufloat, unit a string, and sigfig an int.

        If d["-d"] is zero, then x will remain a ufloat and with be printed
        in standard short form.  If the uncertainty is zero, it will be the
        string form of a standard float.

        If d["-d"] is not zero, then the value is given to that many
        decimal places by converting the ufloat's nominal value to a flt.
        """

        def Fix(s):
            # Need to fix units like rkg mkg ykg nkg akg qkg μkg
            s = s.replace("rkg", "yg")
            s = s.replace("mkg", "kg")
            s = s.replace("ykg", "zg")
            s = s.replace("nkg", "μg")
            s = s.replace("akg", "fg")
            s = s.replace("qkg", "rg")
            s = s.replace("μkg", "mg")
            return s

        name, x, unit, sigfig = item
        unit = "Ω" if unit == "ohm" else unit
        Assert(ii(x, UFloat))
        if d["-d"]:
            # Display as a flt
            n = min(d["-d"], sigfig)
            y = flt(x.n)
            y.n = n
            y.rtz = False
            y.rtdp = True
            s = f"{y} {unit}"
            if not s.startswith("-"):
                s = " " + s
            return s
        else:
            # Keep the uncertainty
            if x.s:
                # Hack to get a number with uncertainty expressed as
                # 5.1(2)✕10⁻¹ instead of 5.1(2)e-1.
                s = f"{x:.1uS}"
                if "e" in s:
                    a, b = s.split("e")
                    x = flt(f"1e{b}").sci
                    loc = x.find("✕")
                    y = a + x[loc:]
                    s = f"{y} {unit}"
                    if not s.startswith("-"):
                        s = " " + s
                    return s
                else:
                    s = f"{x:.1uS} {unit}"
                    if not s.startswith("-"):
                        s = " " + s
                    return s
            else:
                y = flt(x.n)
                y.n = sigfig
                s = f"{y!s} {unit}"
                if not s.startswith("-"):
                    s = " " + s
                return s

    def PrintData(items):
        """Dump the data; items is a sequence of the integer numbers of the constants that should
        be shown.  These integers are the keys in g.data.

        g.data is a dict with keys of list number and the values are
            (name, value, formatted_unit, significant_figures).
        """
        # Get max column width needed
        w = 0
        for item in items:
            name = g.data[item][0]
            w = max(w, len(name))
        for item in items:
            name, value, un, sigfig = g.data[item]
            # Get colorizing string c
            c = ""
            if not un:
                c = t.nodim
            if not value.s:
                c = t.exact
            t.print(f"{name:{w}s}  {c}{Fmt(g.data[item])}")
        # Show number of digits
        if d["-d"]:
            print(f"Values given to {d['-d']} figures")
        # Color key
        if d["-c"]:
            t.print(f"Colors:  {t.exact}Exact value{t.n}     {t.nodim}Dimensionless")


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    GetData()
    if args:
        # Get a list of the constant numbers whose descriptions contain the desired regexes
        items = set()
        for regex in args:
            r = re.compile(regex, re.I)
            for num in g.data:
                name = g.data[num][0]
                mo = r.search(name)
                if mo:
                    items.add(num)
        PrintData(items)
    else:
        if d["-a"]:
            PrintData(g.data.keys())
        else:
            PrintData(g.important)
