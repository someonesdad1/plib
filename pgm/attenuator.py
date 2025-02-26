"""
Script to design tee and pi attenuators.

    https://www.rfcafe.com/references/electrical/attenuators.htm has formulas for attenuators.

"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2011, 2021 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Design tee and pi attenuators
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    import os
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from lwtest import Assert
    from f import flt, sqrt
if 1:  # Global variables
    debug = 0  # Turns on debug printing
    nl = "\n"
    schematic = """
           Pi                                    Tee

    o--+---R3----+--o                    o---R1---+---R2---o
       |         |                                |
       R1        R2                               R3
       |         |                                |
    o--+---------+--o       Ground       o--------+--------o
    """[1:]


def Dbg(msg, no_newline=0):
    if debug:
        print(msg, file=sys.stderr, end="")
        if not no_newline:
            print()


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} dB Zin [Zout]
      Prints the design of tee and pi attenuators for a given voltage attenuation in dB.  Zin is
      the input impedance and Zout is the output impedance.  If you just give Zin, then the input
      and output impedance are the same.  The circuits are:
    
      Example:  
        Make an adapter from a 10 MΩ voltmeter input to a 1 MΩ scope probe.  Use units of MΩ.
        Make it a 20 dB attenuator.  Arguments = '20 10 1'.  The results for the tee attenuator
        (most practical of my on-hand resistors) are R1 = 9.56 MΩ, R2 = 381 kΩ, R3 = 639 kΩ.  This
        result was checked against the calculator at
        https://www.rfcafe.com/references/electrical/attenuators.htm.
    """)
    )
    print(schematic)
    print(
        dedent(f"""
            Zin >= Zout                           Zin >= Zout
    Options
      -d n      Print n digits in the report [{d["-d"]}]
    """)
    )
    exit(status)


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def ParseCommandLine(d):
    x = flt(0)
    d["-d"] = 3
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "d:h")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-d":
            try:
                n = int(opt[1])
            except ValueError:
                Error("'%s' isn't a valid integer" % opt[1])
            if n < 1 or n > 15:
                Error("Number of digits must be between 1 and 15")
            d["-d"] = x.N = n
        if opt[0] == "-h":
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
    x.low = 0.001  # Use sci below this value
    x.high = 1e6  # Use sci above this value


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


def Results():
    # Get input parameters
    L, Zin, Zout = d["dB"], d["Zin"], d["Zout"]
    zratio = Zin / Zout
    # Double check input
    Assert(L >= 0)
    Assert(Zin > 0)
    Assert(Zout > 0)
    # Equations from http://www.rfcafe.com/references/electrical/attenuators.htm
    k = 10 ** (L / 10)
    kmin = 2 * zratio - 1 + 2 * sqrt(zratio * (zratio - 1))
    if k < kmin:
        Error("Attenuation is too low for the given impedances")
    # Convenience constants
    a = k + 1
    b = 2 * sqrt(k * Zin * Zout)
    c = k - 1
    if 1:  # tee
        R1tee = (a * Zin - b) / c
        R2tee = (a * Zout - b) / c
        R3tee = b / c
    if 1:  # pi
        R1pi = c * Zin * sqrt(Zout) / (a * sqrt(Zout) - 2 * sqrt(k * Zin))
        R2pi = c * Zout * sqrt(Zin) / (a * sqrt(Zin) - 2 * sqrt(k * Zout))
        R3pi = c / 2 * sqrt(Zin * Zout / k)
    if 0:
        columns = int(os.environ.get("COLUMNS", 80))
    else:
        columns = 60  # Just use a fixed number, as that's simplest
    s = "Tee and pi attenuators"
    print(f"{s:^{columns}s}")
    print(f"{'-' * len(s):^{columns}s}")
    print(schematic)
    n, t = 20, " " * 12
    da, o = "-" * n, "Ω"
    print(
        dedent(f"""
         Results given to {zratio.N} figures
         Attenuation = {L} dB (ratio = {k})
         Zin         = {Zin.engsi}{o}
         Zout        = {Zout.engsi}{o}
    
                 {"pi":^{n}s}{t}{"tee":^{n}s}
                 {da:^{n}s}{t}{da:^{n}s}
         R1      {R1pi.engsi + o:^{n}s}{t}{R1tee.engsi + o:^{n}s}
         R2      {R2pi.engsi + o:^{n}s}{t}{R2tee.engsi + o:^{n}s}
         R3      {R3pi.engsi + o:^{n}s}{t}{R3tee.engsi + o:^{n}s}
    """)
    )


if __name__ == "__main__":
    d = {}
    ParseCommandLine(d)
    Results()
