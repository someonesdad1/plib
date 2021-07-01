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
    # Program description string
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
    from sig import sig, GetSigFig
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
    f2c = lambda t: (t - c0)/p0
    k2c = lambda t: t - k0
    r2c = lambda t: r2f(f2c(t))
    c2f = lambda t: p0*t + c0
    k2f = lambda t: c2f(k2c(t))
    r2f = lambda t: t - r0
    c2k = lambda t: t + k0
    f2k = lambda t: c2k(f2c(t))
    r2k = lambda t: t/p0
    f2r = lambda t: c2r(f2c(t))
    k2r = lambda t: p0*t
    c2r = lambda t: c2f(t) + r0
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
      Utility to convert between common temperatures.
     
    Options:
        -c      Don't use color in output
        -f      Show the formulas
        -r      Include Rankine temperatures
    '''))
    exit(0)
def ParseCommandLine(d):
    d["-c"] = True      # Use color in output
    d["-r"] = False     # Include Rankine in output
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cr")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("cr"):
            d[o] = not d[o]
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
    try:
        T = int(t)
    except Exception:
        T = float(t)
    sig.digits = NumberOfFigures(t)
    sig.rtz = True
    # It's °F
    if T >= -r0:
        K("f"); P(f"{T}{uF}"); K()
        P("="); K("c"); P(f"{sig(f2c(T))}{uC}"); K()
        P("="); K("k"); P(f"{sig(f2k(T))}{uK}"); K()
        if d["-r"]:
            P("="); K("r"); P(f"{sig(f2r(T))}{uR}"); K()
        print()
    # It's °C
    if T >= -k0:
        K("c"); P(f"{T}{uC}"); K()
        P("="); K("f"); P(f"{sig(c2f(T))}{uF}"); K()
        P("="); K("k"); P(f"{sig(c2k(T))}{uK}"); K()
        if d["-r"]:
            P("="); K("r"); P(f"{sig(c2r(T))}{uR}"); K()
        print()
    # It's K
    if T >= 0:
        K("k"); P(f"{T}{uK}"); K()
        P("="); K("f"); P(f"{sig(k2f(T))}{uF}"); K()
        P("="); K("c"); P(f"{sig(k2c(T))}{uC}"); K()
        if d["-r"]:
            P("="); K("r"); P(f"{sig(k2r(T))}{uR}"); K()
        print()
    # It's R
    if T >= 0 and d["-r"]:
        K("r"); P(f"{T}{uR}"); K()
        P("="); K("f"); P(f"{sig(r2f(T))}{uF}"); K()
        P("="); K("c"); P(f"{sig(r2c(T))}{uC}"); K()
        P("="); K("k"); P(f"{sig(r2k(T))}{uK}"); K()
        print()
    if include_nl:
        print()
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for temperature in args:
        Report(temperature, include_nl=len(args) > 1)
    ShowFormulas()
