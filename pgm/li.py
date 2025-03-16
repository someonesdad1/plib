'''

LiFePO₄ battery characteristics:  prints the % charge as a function of open circuit
rested voltage.  The information from the web is poor, as it doesn't attribute sources
and it appears that everyone copies everyone else.  The information I used is:

     %     V
     0   10.00
    10   12.00
    20   12.80
    30   12.88
    40   13.00
    50   13.04
    60   13.08
    70   13.20
    80   13.28
    90   13.40
    100  13.60

and the printed data are gotten through linear interpolation using scipy's
interpolate.interp1d.

'''
_pgminfo = '''
<oo desc 
    LiFePO₄ battery characteristics
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat elec oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
        from scipy.interpolate import interp1d
    if 1:   # Custom imports
        from f import flt
        from frange import frange
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        from columnize import Columnize
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetColors(on=False):
        t.ten = t.grn if on else ""
        t.five = t.whtl if on else ""
        t.err = t.redl
        t.dbg = t.skyl if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [%step]
          Print out LiFePO₄ battery characteristics for a 1% step in capacity.  Change
          the step percentage by a command line argument.
        Options:
            -h      Print a manpage
            -n c    Number of cells [{d["-n"]}]
            -p      Plot the data (requires matplotlib)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Use colors
        d["-n"] = 4         # Number of cells
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chn:p") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("c"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
            elif o == "-n":
                try:
                    d[o] = int(a)
                    if d[o] < 1:
                        raise ValueError
                except ValueError:
                    Error(f"-n option's argument must be an integer > 0")
            elif o == "-p":
                PlotData()
        GetColors(d["-c"])
        return args
if 1:   # Core functionality
    def PlotData():
        '''This is used to show various forms of the plotted charge level vs. open
        circuit voltage.  Alas, there's no attribution and this doesn't look like
        carefully-taken data.

        The linear plot was the most useful, as I printed it on a sheet of paper using a
        cubic spline interpolation plot and got 5 intervals that are usefully
        approximated by straight lines:

            (0, 2.5) to (0.33, 2.86)
            (0.33, 2.86) to (11.9, 3.06)
            (11.9, 3.06) to (20, 3.20)
            (20, 3.20) to (84.4, 3.33)
            (84.4, 3.33) to (100, 3.40)

        '''
        from pylab import plot, semilogy, semilogx, loglog, legend
        from pylab import show, grid, title, xlabel, ylabel, savefig
        from scipy.interpolate import CubicSpline
        from frange import frange
        pct, V = Data()
        f = interp1d(pct, V)        # Linear interp
        cs = CubicSpline(pct, V)    # Cubic spline interp
        dec = "-"
        if 0:   # Exploratory plotting to find decent approximation
            # Plot the data
            step = ".10"
            pct = list(frange("0", "100.01", step))
            typ = "semilogy"
            typ = "linear"
            if typ == "linear":
                plot(pct, [cs(i) for i in pct], dec)
            elif typ == "loglog":
                loglog(pct, [cs(i) for i in pct], dec)
            elif typ == "semilogy":
                semilogy(pct, [cs(i) for i in pct], dec)
            elif typ == "semilogx":
                semilogx(pct, [cs(i) for i in pct], dec)
            else:
                raise ValueError(f"Bad typ = {typ!r}")
            title("LiFePO₄ battery OC voltage vs % of charge")
            xlabel("% of charge")
            xlabel("Open circuit voltage, V")
            grid()
            savefig("lifepo4.png", dpi=200)
            show()
        else:   # Plot cubic spline approx versus linear approx
            def GetLinearInterp():
                # Get linear interpolation function derived from plot
                x = (0, 6.39, 11.9, 20, 84.4, 100)
                y = (2.5, 2.86, 3.06, 3.20, 3.33, 3.4)
                return interp1d(x, y)
            # Cubic spline plot
            pct = list(frange("0", "100.01", "0.1"))
            plot(pct, [cs(i) for i in pct], dec, label="Cubic spline") # 
            # Our linear approximation
            line = GetLinearInterp()
            plot(pct, [line(i) for i in pct], dec, label="Linear approx.") # 
            title("LiFePO₄ battery OC voltage vs % of charge")
            xlabel("% of charge")
            xlabel("Open circuit voltage, V")
            grid()
            legend()
            #savefig("lifepo4.png", dpi=200)
            show()
        exit(0)
    def Data():
        'Return [[%chg, OCVoltage], ...]'
        pct = [int(i) for i in reversed("100 90 80 70 60 50 40 30 20 10 0".split())]
        V = [flt(i) for i in reversed("3.40 3.35 3.32 3.30 3.27 3.26 3.25 3.22 3.20 3.00 2.50".split())]
        return pct, V
    def GetInterpolationFunction():
        pct, V = Data()
        f = interp1d(pct, V)
        finv = interp1d(V, pct)
        return f, finv
    def PrintBatteryDetails(pct_step):
        print(dedent(f'''
        LiFePO₄ battery ({d["-n"]} cells)
        % charge vs. rested open circuit voltage
        '''))
        f, finv = GetInterpolationFunction()
        flt(0).rtz = False
        w1, w2, ten, five = 5, 5, flt(10), flt(5)
        o = [f"{'%':^{w1}s} {'V':^{w2}s}"]
        try:
            step = float(pct_step)
        except ValueError:
            Error(f"{str(pct_step)!r} is not a valid percentage step")
        for p in frange("0", "100", str(float(pct_step)), impl=flt, include_end=True):
            with p:
                p.rtz = p.rtdp = True
                ps = f"{p!s:^{w1}s}"
            try:
                V = flt(d["-n"]*f(p))
            except ValueError:
                continue
            with V:
                V.rtz = V.rtdp = False
                V.N = 4
                Vs = f"{V!s:^{w2}s}"
            c = ""
            if not (p % ten):
                c = t.ten
            elif not (p % five):
                c = t.five
            o.append(f"{c}{ps} {Vs}{t.n}")
        if step < 5:
            for i in Columnize(o, columns=5, sep=" "*5):
                print(i)
        else:
            for i in o:
                print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if args:
        for arg in args:
            try:
                p = flt(arg)
                if p <= 0:
                    Error("%step must be a number > 0")
                PrintBatteryDetails(p)
            except ValueError:
                Error(f"{arg!r} isn't a valid integer")
    else:
        PrintBatteryDetails(1)
