'''
Temperature conversion utility
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2001 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Temperature conversion utility
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import getopt
        import sys
    if 1:   # Custom imports
        from temperature import ConvertTemperature
        from u import ParseUnit
        from sig import GetSigFig
        from f import flt
        from color import t
        from wrap import dedent
        from lwtest import Assert, assert_equal
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.sep = 5   # Column separation
        g.w = 15    # Column width
        if 0:   # Old stuff
            # Colors:  gotten by e.g. clr["c"]
            clr = {}
        if 0:   # Old stuff
            # Unit symbols
            uK, uC, uF, uR = " K", " °C", " °F", " °R"
            # Denote conversion types
            K, C, F, R = 1, 2, 3, 4
            # Conversion factors
            p0, c0, k0, r0 = 9/5, 32, 273.15, 459.67
if 1:  # Utility
    def GetColors():
        uc = d["-c"]
        if 1:   # New colors
            t.k = t.roy  if uc else ""
            t.f = t.grn  if uc else ""
            t.c = t.yel  if uc else ""
            t.r = t.viol if uc else ""
            t.w = t("redl", attr="it") if uc else ""
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d):
        print(dedent(f'''
        Usage:  {sys.argv[0]} temperature1 [temperature2 ...]
          Utility to convert between common temperatures.  The number of digits in the conversions
          is determined from the number of significant figures in the command line arguments (will
          be 3 or more if the -d option isn't used).
        Options:
            -c      Don't use color in output
            -d n    Set number of significant figures
            -r      Include Rankine temperatures
        '''))
        exit(0)
    def ParseCommandLine(d):
        d["-c"] = True      # Use color in output
        d["-d"] = None      # Manually set sig figs
        d["-r"] = False     # Include Rankine in output
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cd:r")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cr"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                except Exception:
                    Error("-d argument must be integer > 0")
        # Set up flt characteristics
        z = flt(0)
        z.rtdp = True   # Remove a bare trailing decimal point
        z.rtz = False   # Remove trailing '0' characters
        GetColors()
        return args
if 1:  # Core functionality
    def NumberOfFigures(s):
        'Return the number of significant figures in s'
        return 5 if s == "0" else max(GetSigFig(s), 3)
    def ShowFormulas():
        print()
        print(dedent(f'''
        Formulas:
            {t.c}C{t.n} = 5/9*({t.f}F{t.n} - 32) = {t.k}K{t.n} - 273.15
            {t.f}F{t.n} = 9/5*{t.c}C{t.n} + 32'''))
        if d["-r"]:
            print(f"    {t.r}R{t.n} = {t.f}F{t.n} + 459.67")
    def Header():
        'Print a report header'
        w = g.w  # Column width
        sep = " "*g.sep
        # Print temperature units
        t.print(f"{t.c}{'°C':^{w}s}{sep}"
                f"{t.f}{'°F':^{w}s}{sep}"
                f"{t.k}{'K':^{w}s}",
                end="")
        t.print(f"{sep}{t.r}{'°R':^{w}s}") if d["-r"] else t.print()
        # Print underlines
        s = "─"*w
        t.print(f"{t.c}{s:^{w}s}{sep}"
                f"{t.f}{s:^{w}s}{sep}"
                f"{t.k}{s:^{w}s}",
                end="")
        t.print(f"{sep}{t.r}{s:^{w}s}") if d["-r"] else t.print()
    def Report(temp):
        'temp is the string on the command line'
        w = g.w  # Column width
        sep = " "*g.sep
        T = flt(temp)
        if d["-d"] is None:
            n = max(GetSigFig(temp), 3)
        else:
            n = d["-d"]
        with T:
            T.N = n
            # Assume it's °C
            From = "c"
            print(f"{t.w}{T!s:^{w}s}{sep}", end="")
            print(f"{t.f}{ConvertTemperature(T, From, 'f')!s:^{w}s}{sep}", end="")
            print(f"{t.k}{ConvertTemperature(T, From, 'k')!s:^{w}s}{sep}", end="")
            t.print(f"{t.r}{ConvertTemperature(T, From, 'r')!s:^{w}s}") if d["-r"] else t.print()
            # Assume it's °F
            From = "f"
            print(f"{t.c}{ConvertTemperature(T, From, 'c')!s:^{w}s}{sep}", end="")
            print(f"{t.w}{T!s:^{w}s}{sep}", end="")
            print(f"{t.k}{ConvertTemperature(T, From, 'k')!s:^{w}s}{sep}", end="")
            t.print(f"{t.r}{ConvertTemperature(T, From, 'r')!s:^{w}s}") if d["-r"] else t.print()
            # Assume it's K
            From = "k"
            print(f"{t.c}{ConvertTemperature(T, From, 'c')!s:^{w}s}{sep}", end="")
            print(f"{t.f}{ConvertTemperature(T, From, 'f')!s:^{w}s}{sep}", end="")
            print(f"{t.w}{T!s:^{w}s}{sep}", end="")
            t.print(f"{t.r}{ConvertTemperature(T, From, 'r')!s:^{w}s}") if d["-r"] else t.print()
            # Assume it's °R
            if d["-r"]:
                From = "r"
                print(f"{t.c}{ConvertTemperature(T, From, 'c')!s:^{w}s}{sep}", end="")
                print(f"{t.f}{ConvertTemperature(T, From, 'f')!s:^{w}s}{sep}", end="")
                print(f"{t.k}{ConvertTemperature(T, From, 'k')!s:^{w}s}{sep}", end="")
                t.print(f"{t.w}{T!s:^{w}s}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    assert(args)
    Header()
    for temperature in args:
        Report(temperature)
    ShowFormulas()
