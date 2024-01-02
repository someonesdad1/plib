'''
Construct a copy of Barlow's tables
    This script will produce a table that will fit in 80 columns.  The
    square, cube, square root, cube root, reciprocal, and base 10 logarithm
    of the integers are given.  This simulates the stunning book produced
    by Barlow in the early 1800's that stayed in print for around 150
    years.  In fact, in the early 1900's the original printing plates wore
    out, so new plates had to be generated.
 
    See https://en.wikipedia.org/wiki/Peter_Barlow_(mathematician)
 
    The original work took a lot of effort to produce, both calculation of
    the numbers and the dreary task of checking the printer's typesetting.
    The edition edited by de Morgan in 1840 was known to be nearly error
    free.  Today, such a table can be generated in less than a second by a
    script like this.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Produce a replica of Barlow's Tables
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pprint import pprint as pp
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from lwtest import Assert
        from f import flt, log10
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] n [m]
          Prints out Barlow's table from 1 to n with an additional column
          for the logarithm.  If m is given, the table goes from n to m.
        Options:
            -c      Color escapes always on
            -h      Print a manpage
            -l      Omit the logarithm
            -t      Separate output by tabs
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Always color coding
        d["-l"] = False     # Omit logarithm printing
        d["-t"] = False     # Tab separator
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chl") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cl"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if d["-c"]:
            t.always = True
        if not args:
            Usage()
        return args
if 1:   # Core functionality
    def GetColors():
        a = sys.stdout.isatty() or d["-c"]
        t.num = t("wht") if a else ""
        t.sq = t("trq") if a else ""
        t.cu = t("olvl") if a else ""
        t.sqrt = t("yell") if a else ""
        t.curt = t("denl") if a else ""
        t.recip = t("redl") if a else ""
        t.log = t("cynl") if a else ""
        t.N = t.n if a else ""
    def Row(n):
        return (n, n**2, n**3, n**(1/2), n**(1/3), 1/n, log10(n))
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
                lambda x: x**(1/2),
                lambda x: x**(1/3),
                lambda x: 1/x,
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
            o.append(f"{u[i]}{hy*w[i]:^{w[i]}s}{t.N}")
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
        print(f"\nColor code: {t.num}num{t.N} "
              f"{t.sq}Square{t.N} "
              f"{t.cu}Cube{t.N} "
              f"{t.sqrt}SquareRoot{t.N} "
              f"{t.curt}CubeRoot{t.N} "
              f"{t.recip}Reciprocal{t.N} ", end="")
        if not d["-l"]:
            print(f"{t.log}Log10{t.N}")
        else:
            print()

if __name__ == "__main__":
    d = {}      # Options dictionary
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
