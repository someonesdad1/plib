'''
Script to design tee and pi attenuators

    https://www.rfcafe.com/references/electrical/attenuators.htm has formulas for attenuators.
    
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2011, 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Design tee and pi attenuators
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    import os
if 1:  # Custom imports
    from wrap import dedent
    from lwtest import Assert
    from f import flt, sqrt
    import trm
    t = trm.TrmDP()
if 1:  # Global variables
    debug = 0  # Turns on debug printing
    nl = "\n"
    # Coloring for resistor size
    t.G = t.red
    t.M = t.orn
    t.k = t.grn
    t.o = t.wht
    t.m = t.yel
    schematic = '''
           Pi                                    Tee
           
    o--+---R3----+--o                    o---R1---+---R2---o
       |         |                                |
       R1        R2                               R3
       |         |                                |
    o--+---------+--o       Ground       o--------+--------o
    '''[1:]
def Dbg(msg, no_newline=0):
    if debug:
        print(msg, file=sys.stderr, end="")
        if not no_newline:
            print()
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} dB Zin [Zout]
      Prints the design of tee and pi attenuators for a given voltage attenuation in dB.
      Zin is the input impedance and Zout is the output impedance.  If you just give
      Zin, then the input and output impedance are the same.  The circuits are:
    '''))
    print(schematic)
    print(dedent(f'''
            Zin >= Zout                           Zin >= Zout
    Options
      -a        Attenuation is a decimal number instead of dB (must be between 0 and 1)
      -d n      Print n digits in the report [{d["-d"]}]
    Example:  
        Make an adapter from a 10 MΩ voltmeter input to a 1 MΩ scope probe.  Use units
        of MΩ.  Make it a 20 dB attenuator.  Arguments = '20 10M 1M'.  The results for
        the tee attenuator (most practical of my on-hand resistors) are R1 = 9.56 MΩ, R2
        = 381 kΩ, R3 = 639 kΩ.  This result was checked against the calculator at
        https://www.rfcafe.com/references/electrical/attenuators.htm.
    '''))
    exit(status)
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def ParseCommandLine(d):
    'Return d["dB"], d["Zin"], d["Zout"]'
    x = flt(0)
    d["-a"] = False     # dB argument is attenuation ratio as float
    d["-d"] = 3         # Number of decimal digits to display
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "ad:h")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "a":
            d[o] = not d[o]
        elif o == "-d":
            try:
                n = int(a)
            except ValueError:
                Error(f"'{a}' isn't a valid integer")
            if n < 1 or n > 15:
                Error("Number of digits must be between 1 and 15")
            d[o] = x.N = n
        elif o == "-h":
            Usage(0)
    if len(args) not in (2, 3):
        Usage()
    else:
        d["dB"] = flt(args[0])
        if d["dB"] <= 0:
            Error("dB must be > 0")
        d["Zin"] = GetZ(args[1])
        d["Zout"] = GetZ(args[2]) if len(args) == 3 else d["Zin"]
    if d["Zout"] > d["Zin"]:
        Error("Zin must be >= Zout")
    x.low = 0.001   # Use sci below this value
    x.high = 1e6    # Use sci above this value
    x.u = True      # Use Unicode to display scientific notation
def GetZ(s):
    "Get impedance in ohms; allow use of common SI prefixes as suffixes"
    if "m" in s:
        s = s.replace("m", "*0.001")
    elif "k" in s:
        s = s.replace("k", "*1e3")
    elif "M" in s:
        s = s.replace("M", "*1e6")
    elif "G" in s:
        s = s.replace("G", "*1e9")
    elif "T" in s:
        s = s.replace("T", "*1e12")
    z = flt(eval(s))
    if z <= 0:
        Error(f"Impedance {s!r} must be > 0")
    return flt(eval(s))
def T(R):
    'Return color string for resistance R'
    if R >= 1e9:
        return t.G
    elif R >= 1e6:
        return t.M
    elif R >= 1e3:
        return t.k
    elif R >= 1:
        return t.o
    else:
        return t.m
def Results():
    # Get problem's input
    L, Zin, Zout = d["dB"], d["Zin"], d["Zout"]
    Zratio = Zin/Zout
    # Double check input
    Assert(L >= 0)
    Assert(Zin > 0)
    Assert(Zout > 0)
    Assert(Zratio >= 1)
    # Get k, the attenuation ratio
    if d["-a"]:
        k = 1/L   # -a was used to make it a ratio directly
    else:
        # Equations from http://www.rfcafe.com/references/electrical/attenuators.htm
        # His Z1 is Zin here, Z2 is Zout
        k = 10**(L/10)
    kmin = 2*Zratio - 1 + 2*sqrt(Zratio*(Zratio - 1))
    if k < kmin:
        Error("Attenuation is too low for the given impedances")
    # Convenience constants
    a = k + 1
    b = 2*sqrt(k*Zin*Zout)
    c = k - 1
    if 1:  # tee
        R1tee = (a*Zin - b)/c
        R2tee = (a*Zout - b)/c
        R3tee = b/c
    if 1:  # pi
        R1pi = c*Zin*sqrt(Zout)/(a*sqrt(Zout) - 2*sqrt(k*Zin))
        R2pi = c*Zout*sqrt(Zin)/(a*sqrt(Zin) - 2*sqrt(k*Zout))
        R3pi = c/2*sqrt(Zin*Zout/k)
    columns = 60
    s = "Tee and pi attenuators"
    print(f"{t.purl}{s:^{columns}s}")
    t.print(f"{'-'*len(s):^{columns}s}")
    print(schematic)
    n, u, v = 20, " "*12, t.n
    da, o = "-"*n, "Ω"
    print(dedent(f'''
         Attenuation = {L} dB ({1/k} reduction)
         Zin         = {Zin.engsi}{o}
         Zout        = {Zout.engsi}{o}
    
                 {"pi":^{n}s}{u}{"tee":^{n}s}
                 {da:^{n}s}{u}{da:^{n}s}
         R1      {T(R1pi)}{R1pi.engsi + o:^{n}s}{v}{u}{T(R1tee)}{R1tee.engsi + o:^{n}s}{v}
         R2      {T(R2pi)}{R2pi.engsi + o:^{n}s}{v}{u}{T(R2tee)}{R2tee.engsi + o:^{n}s}{v}
         R3      {T(R3pi)}{R3pi.engsi + o:^{n}s}{v}{u}{T(R3tee)}{R3tee.engsi + o:^{n}s}{v}
    '''))
    # Show color coding
    print("Resistances are color coded:")
    s = (f"{T(1e9)}>= 1 G{o}{t.n}, {T(1e6)}>= 1 M{o}{t.n}, {T(1e3)}>= 1 k{o}{t.n}, "
         f"{T(1)} >= 1 {o}{t.n}, {T(0.001)} < 1 {o}{t.n}")
    print(s)
if __name__ == "__main__":
    d = {}
    ParseCommandLine(d)
    Results()
