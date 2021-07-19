'''
Print out a profit vs. markup table
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Print out a profit vs. markup table
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from os import environ
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from f import flt
    from color import C
if 1:   # Global variables
    class g: pass
    g.m = C.lyel
    g.P = C.lgrn
    g.M = C.lmag
    g.n = C.norm
    flt(0).n = 3
    # Global formatting stuff
    width = 7
    o = 1       # Offset
    R = range(10)
    f = "{{:<{}}}".format(width)
def HeaderFormats(wide=False):
    '''Return two formatting specifiers for the header; the first is for
    the single digit % numbers and the second is for the hyphens.  If
    wide is True, it means the column under the % sign will be 3 digits
    instead of 2.
    '''
    hdr = (" %" + " "*bool(wide) + " "*(width - o - 3 - bool(wide)) +
           "{{:^{}}}".format(width)*10)
    h = "-"*(2 + bool(wide)) + " "*(3 - bool(wide))
    hyph = h + " " + ("-"*(width - 2) + "  ")*10
    return hdr, hyph
def Header(clr, wide=False):
    hdr, hyphens = HeaderFormats(wide)
    print(clr + hdr.format(*R) + g.n)
    print(clr + hyphens + g.n)
def Dezero(x, n=4):
    '''Convert flt x to a string, then remove any trailing zeros
    up to and including the decimal point.  Also remove the leading
    zero.
    '''
    s = str(x)
    while s[-1] == "0":
        s = s[:-1]
    if s[-1] == ".":
        s = s[:-1]
    if s.startswith("0."):
        s = s[1:]
    return s
def Multiplier_vs_Profit():
    print(f"{g.m}Multiplier{g.n} vs. {g.P}profit{g.n} in %    "
          f"({g.m}m{g.n} = 1/(1 - {g.P}P{g.n}))")
    Header(g.P)
    for row in range(0, 100, 10):
        s = " "*(width - o - 2)
        r = [f"{g.P}{row:2d}{g.n}{s}"]
        for col in R:
            p = flt((row + col)/100)
            m = 1/(1 - p)
            r.append(g.m + f.format(Dezero(m)) + g.n)
        print(''.join(r))
    print()
def Markup_vs_Profit():
    print(f"{g.M}Markup{g.n} in % vs. {g.P}profit{g.n} in %    "
          f"({g.M}M{g.n} = {g.P}P{g.n}/(1 - {g.P}P{g.n}))")
    Header(g.P)
    for row in range(0, 100, 10):
        s = " "*(width - o - 2)
        r = [f"{g.P}{row:2d}{g.n}{s}"]
        for col in R:
            p = flt((row + col)/100)
            M = 100*p/(1 - p)
            r.append(g.M + f.format(Dezero(M)) + g.n)
        print(''.join(r))
    print()
def Profit_vs_Markup():
    print(f"{g.P}Profit{g.n} in % vs. {g.M}markup{g.n} in %    "
          f"({g.P}P{g.n} = {g.M}M{g.n}/(1 + {g.M}M{g.n}))")
    Header(g.M, wide=True)
    for row in range(0, 201, 10):
        s = " "*(width - o - 3)
        r = [f"{g.M}{row:3d}{g.n}{s}"]
        for col in R:
            M = flt((row + col)/100)
            P = 100*M/(1 + M)
            r.append(g.P + f.format(Dezero(P)) + g.n)
        print(''.join(r))
if __name__ == "__main__":
    Multiplier_vs_Profit()
    Markup_vs_Profit()
    Profit_vs_Markup()
