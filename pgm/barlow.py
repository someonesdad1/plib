'''
Construct a copy of Barlow's tables

    This script will produce a table that will fit in 80 columns, assuming the argument
    isn't too large.  The square, cube, square root, cube root, reciprocal, and base 10
    logarithm of the integers are given.  This reproduces the contents of the book
    produced by Barlow in the early 1800's that stayed in print for around 150 years.
    In the early 1900's the original printing plates wore out, so new plates had to be
    generated.  See https://en.wikipedia.org/wiki/Peter_Barlow_(mathematician).
    
    Barlow's work was important for many years to people who needed to do manual
    arithmetic calculations.  Barlow acknowledged that there was little of mathematical
    merit in the publication to impress mathematicians, yet the enormous contribution of
    the book was the care of its publication, the checking and double checking, and care
    of both author and printer to ensure the accuracy of the printed works.  How many
    books are you aware of that the printing plates were used so much that they wore out
    and had to be replaced?  Using flawed math tables (i.e., tables with errors) is like
    building a house with a tool you don't know is faulty and getting poor results.  You
    can waste a lot of time finding the problem and folks who have been burned look for
    consistently along the way, not wanting to repeat the pain or rework.
    
    The original work took much effort to produce, both calculation of the numbers
    (aided by algebraic checks) and checking the printer's typesetting; typesetting was
    a notorious source of errors.  The edition edited by de Morgan in 1840 was known to
    be nearly error free.  These types of tables were made obsolete by electronic
    calculators and computers, which can produce an equivalent table on the order of 1
    second.

    I'm of the last generation of people who had to utilize manual calculation, log
    tables, and slide rules to do their technical calculations, as electronic
    calculators appeared in the mid-1970's and became commonly and cheaply available by
    about 1980 (I went to college in the 1960's).  Yet I am embarrassed to say I had
    never used Barlow's tables, nor seen it until a few decades later (and I'm surprised
    that none of my teachers recommended it, as I have no doubt a few of them would have
    been aware of it).  If we had to do a calculation that couldn't be done on a slide
    rule, then it was done with the 5 place log tables in e.g. the CRC math tables or
    Handbook of Chemistry and Physics.  My CRC math tables, a cloth-bound book, got used
    so much it fell apart in the 1970's and I had to buy another copy.  Yet in the
    1980's and 1990's I reflected on the powerful calculators we had and what drudgery
    manual calculation was -- and recognized that using Barlow's tables would have made
    things more convenient when I was doing manual calculations.  Much of this comes
    from the need to work with squares and square roots, particularly with trigonometric
    calculations.

    One thing these laborious manual calculations did was give you an awareness
    calculations that gave you both a more intuitive understanding of a problem as well
    as a sense for when things weren't quite right.  This happened by necessity as long
    as you paid attention and learned from your mistakes.  This contrasts to today's
    common user who just punches numbers into a keyboard and doesn't even check their
    work.  Checking is as important today with computers and calculators as it was with
    manual calculations, but, again, you don't learn this important lesson easily.

'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Produce a replica of Barlow's Tables
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pprint import pprint as pp
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from lwtest import Assert
        from f import flt, log10
        if 1:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(
            dedent(f'''
        Usage:  {sys.argv[0]} [options] n [m]
          Prints out Barlow's table from 1 to n with an additional column
          for the logarithm.  If m is given, the table goes from n to m.
        Options:
            -c      Color escapes always on
            -l      Omit the logarithm
            -t      Separate output by tabs
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-C"] = False  # No color coding
        d["-c"] = False  # Always color coding
        d["-l"] = False  # Omit logarithm printing
        d["-t"] = False  # Tab separator
        try:
            opts, args = getopt.getopt(sys.argv[1:], "Cchl")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("Ccl"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if d["-c"]:
            t.always = True
        if not args:
            Usage()
        return args
if 1:  # Core functionality
    def GetColors():
        a = sys.stdout.isatty() or d["-c"]
        if d["-C"]:
            a = False
        t.num = t.grn if a else ""
        t.sq = t.lill if a else ""
        t.cu = t.wht if a else ""
        t.sqrt = t.brnl if a else ""
        t.curt = t.wht if a else ""
        t.recip = t.pnk if a else ""
        t.log = t.whtl if a else ""
        t.N = t.n if a else ""
    def Row(n):
        return (n, n**2, n**3, n ** (1 / 2), n ** (1 / 3), 1 / n, log10(n))
    def GenerateTable(n, m):
        Assert(n < m)
        big = True if m > 10000 else False
        w = [5, 9, 13, 11, 10, 12, 12]
        if big:
            # Get widths from largest string of each type of number
            R = range(n, m + 1)
            def P(func, j):
                mx = 0
                for i in R:
                    mx = max(mx, len(repr(func(i))))
                return mx
            f = (
                lambda x: x,
                lambda x: x**2,
                lambda x: x**3,
                lambda x: x ** (1 / 2),
                lambda x: x ** (1 / 3),
                lambda x: 1 / x,
                lambda x: log10(x),
            )
            for i in range(7):
                w[i] = P(f[i], i)
        # Colors for columns
        u = (t.num, t.sq, t.cu, t.sqrt, t.curt, t.recip, t.log)
        sep = "\t" if d["-t"] else " "
        # Print header
        o = []
        o.append(f"{u[0]}{'n':^{w[0]}s}{t.N}")
        o.append(f"{u[1]}{'Square':^{w[1]}s}{t.N}")
        o.append(f"{u[2]}{'Cube':^{w[2]}s}{t.N}")
        o.append(f"{u[3]}{'Sq. Root':^{w[3]}s}{t.N}")
        o.append(f"{u[4]}{'Cube Root':^{w[4]}s}{t.N}")
        o.append(f"{u[5]}{'Reciprocal':^{w[5]}s}{t.N}")
        if not d["-l"]:
            o.append(f"{u[6]}{'log10':^{w[6]}s}{t.N}")
        print(sep.join(o))
        o, hy = [], "-"
        for i in range(len(w) - d["-l"]):
            o.append(f"{u[i]}{hy * w[i]:^{w[i]}s}{t.N}")
        print(sep.join(o))
        # Get table rows
        for i in range(n, m + 1):
            o = []
            r = Row(i)
            if big:
                o.append(f"{u[0]}{r[0]:{w[0]}d}{t.N}")
                o.append(f"{u[1]}{r[1]:{w[1]}d}{t.N}")
                o.append(f"{u[2]}{r[2]:{w[2]}d}{t.N}")
                o.append(f"{u[3]}{r[3]!r:<{w[3]}s}{t.N}")
                o.append(f"{u[4]}{r[4]!r:<{w[4]}s}{t.N}")
                o.append(f"{u[5]}{r[5]!r:<{w[5]}s}{t.N}")
                if not d["-l"]:
                    o.append(f"{u[6]}{r[6]!r:<{w[6]}s}{t.N}")
            else:
                o.append(f"{u[0]}{r[0]:{w[0]}d}{t.N}")
                o.append(f"{u[1]}{r[1]:{w[1]}d}{t.N}")
                o.append(f"{u[2]}{r[2]:{w[2]}d}{t.N}")
                o.append(f"{u[3]}{r[3]:{w[3]}.7f}{t.N}")
                o.append(f"{u[4]}{r[4]:{w[4]}.7f}{t.N}")
                o.append(f"{u[5]}{r[5]:{w[5]}.10f}{t.N}")
                if not d["-l"]:
                    o.append(f"{u[6]}{r[6]:{w[6]}.10f}{t.N}")
            print(sep.join(o))
        # Print color code
        print(
            f"\nColor code: {t.num}num{t.N} "
            f"{t.sq}Square{t.N} "
            f"{t.cu}Cube{t.N} "
            f"{t.sqrt}SquareRoot{t.N} "
            f"{t.curt}CubeRoot{t.N} "
            f"{t.recip}Reciprocal{t.N} ",
            end="",
        )
        if not d["-l"]:
            print(f"{t.log}Log10{t.N}")
        else:
            print()
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    n = 1
    m = int(eval(args[0]))
    if len(args) > 1:
        n = int(eval(args[0]))
        m = int(eval(args[1]))
    if n > m:
        n, m = m, n
    GetColors()
    GenerateTable(n, m)
