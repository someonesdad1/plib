'''
Temperature conversion utility
'''
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
    from math import fabs
    from pdb import set_trace as xx
if 1:   # Custom imports
    from u import ParseUnit
    useflt = True
    from sig import GetSigFig
    if useflt:
        from f import flt
    else:
        from sig import sig
    import color as C
    from wrap import dedent
if 1:   # Global variables
    # Colors
    c = {
        "k": C.lred,
        "f": C.white,
        "c": C.lgreen,
        "r": C.lblue,
    }
    # Units
    uK = " K"
    uC = " °C"
    uF = " °F"
    uR = " °R"
    # Conversions
    p0, c0, k0, r0 = 9/5, 32, 273.15, 459.67
def f2c(t):
    return flt((t - c0)/p0)
def k2c(t):
    return flt(t - k0)
def r2c(t):
    return flt(r2f(f2c(t)))
def c2f(t):
    return flt(p0*t + c0)
def k2f(t):
    return flt(c2f(k2c(t)))
def r2f(t):
    return flt(t - r0)
def c2k(t):
    return flt(t + k0)
def f2k(t):
    return flt(c2k(f2c(t)))
def r2k(t):
    return flt(t/p0)
def f2r(t):
    return flt(c2r(f2c(t)))
def k2r(t):
    return flt(p0*t)
def c2r(t):
    return flt(c2f(t) + r0)
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def NumberOfFigures(s):
    '''Return the number of significant figures in s.
    '''
    return 5 if s == "0" else max(GetSigFig(s), 3)
def Usage(d):
    print(dedent(f'''
    Usage:  {sys.argv[0]} temperature1 [temperature2 ...]
      Utility to convert between common temperatures.  The number of digits
      in the conversions is determined from the number of significant
      figures in the command line arguments (will be 3 or more) if the -d
      option isn't used.
    Options:
        -c      Don't use color in output
        -d n    Set number of significant figures
        -f      Show the formulas
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
    return args
def P(s):
    'Print with no newline'
    print(s, end=" ")
def K(s=""):
    'Set the appropriate color'
    if d["-c"]:
        C.fg(c[s]) if s else C.normal()
def ShowFormulas():
    print(dedent(f'''
    Temperature conversion formulas:
        °C = 5/9*(°F - 32) = K - 273.15
        °F = 9/5*(°C + 32) 
        °R = °F + 459.67'''))
def Report(t, include_nl=False):
    n = d["-d"]
    try:
        T = int(t)
    except Exception:
        T = flt(t)
    if useflt:
        z = flt(0)
        z.N = n if n else NumberOfFigures(t)
        z.rtz = True
        z.rtdp = True
        z.rtz = False
    else:
        sig.digits = n if n else NumberOfFigures(t)
        sig.rtz = True
    # It's °F
    if T >= -r0:
        K("f")
        P(f"{T}{uF}")
        K()
        P("=")
        K("c")
        if useflt:
            P(f"{f2c(T)}{uC}")
        else:
            P(f"{sig(f2c(T))}{uC}")
        K()
        P("=")
        K("k")
        if useflt:
            P(f"{f2k(T)}{uK}")
        else:
            P(f"{sig(f2k(T))}{uK}")
        K()
        if d["-r"]:
            P("=")
            K("r")
            if useflt:
                P(f"{f2r(T)}{uR}")
            else:
                P(f"{sig(f2r(T))}{uR}")
            K()
        print()
    # It's °C
    if T >= -k0:
        K("c")
        P(f"{T}{uC}")
        K()
        P("=")
        K("f")
        if useflt:
            P(f"{c2f(T)}{uF}")
        else:
            P(f"{sig(c2f(T))}{uF}")
        K()
        P("=")
        K("k")
        if useflt:
            P(f"{c2k(T)}{uK}")
        else:
            P(f"{sig(c2k(T))}{uK}")
        K()
        if d["-r"]:
            P("=")
            K("r")
            if useflt:
                P(f"{c2r(T)}{uR}")
            else:
                P(f"{sig(c2r(T))}{uR}")
            K()
        print()
    # It's K
    if T >= 0:
        K("k")
        P(f"{T}{uK}")
        K()
        P("=")
        K("f")
        if useflt:
            P(f"{k2f(T)}{uF}")
        else:
            P(f"{sig(k2f(T))}{uF}")
        K()
        P("=")
        K("c")
        if useflt:
            P(f"{k2c(T)}{uC}")
        else:
            P(f"{sig(k2c(T))}{uC}")
        K()
        if d["-r"]:
            P("=")
            K("r")
            if useflt:
                P(f"{k2r(T)}{uR}")
            else:
                P(f"{sig(k2r(T))}{uR}")
            K()
        print()
    # It's R
    if T >= 0 and d["-r"]:
        K("r")
        P(f"{T}{uR}")
        K()
        P("=")
        K("f")
        if useflt:
            P(f"{r2f(T)}{uF}")
        else:
            P(f"{sig(r2f(T))}{uF}")
        K()
        P("=")
        K("c")
        if useflt:
            P(f"{r2c(T)}{uC}")
        else:
            P(f"{sig(r2c(T))}{uC}")
        K()
        P("=")
        K("k")
        if useflt:
            P(f"{r2k(T)}{uK}")
        else:
            P(f"{sig(r2k(T))}{uK}")
        K()
        print()
    if include_nl:
        print()
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for temperature in args:
        Report(temperature, include_nl=len(args) > 1)
    ShowFormulas()
