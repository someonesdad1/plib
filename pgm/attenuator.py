'''
Script to design tee and pi attenuators.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2011, 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Design tee and pi attenuators
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import os
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from f import flt, sqrt
if 1:   # Global variables
    debug = 0   # Turns on debug printing
    nl = "\n"
    schematic = '''
           Pi                                    Tee

    o--+---R3----+--o                    o---R1---+---R2---o
       |         |                                |
       R1        R2                               R3
       |         |                                |
    o--+---------+--o       Ground       o--------+--------o
    '''[1:]
    manual1 = dedent(f'''
    Usage:  {sys.argv[0]} dB Z [Zout]
      Prints the design of tee and pi attenuators for a given dB loss.  Z is
      the input and output impedance.  If you just give Z, then the input and
      output impedance are the same.  The circuits are:

    ''')
    manual2 = dedent(f'''
            Zin >= Zout                           Zin >= Zout
    Options
      -d n      Set the output to n digits (default is 3)
    ''')
def Dbg(msg, no_newline=0):
    if debug:
        print(msg, file=sys.stderr, end="")
        if not no_newline:
            print()
def Usage(status=1):
    print(manual1)
    print(schematic)
    print(manual2)
    exit(status)
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def ParseCommandLine(d):
    x = flt(0)
    d["digits"] = 3
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
            d["digits"] = x.n = n
        if opt[0] == "-h":
            Usage(0)
    if len(args) < 2 or len(args) > 3:
        Usage()
    else:
        d["dB"] = float(args[0])
        if d["dB"] <= 0:
            Error("dB must be > 0")
        d["Zin"] = GetZ(args[1])
        if len(args) == 3:
            d["Zout"] = GetZ(args[2])
        else:
            d["Zout"] = d["Zin"]
    if d["Zout"] > d["Zin"]:
        Error("Zin must be >= Zout")
    x.low = 0.001
    x.high = 1e6
def GetZ(s):
    'Get impedance in ohms; allow use of common SI prefixes as suffixes'
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
    return flt(eval(s))
def Results():
    L, Zin, Zout = flt(d["dB"]), flt(d["Zin"]), flt(d["Zout"])
    # Equations from
    # http://www.rfcafe.com/references/electrical/attenuators.htm
    k, r = flt(10**(L/10)), flt(Zin/Zout)
    kmin = flt(2*r - 1 + 2*sqrt(r*(r - 1)))
    if k < kmin:
        Error("Attenuation is too low for the given impedances")
    a, b, c = k + 1, flt(2*sqrt(k*Zin*Zout)), k - 1
    # tee
    R1tee, R2tee, R3tee = flt((a*Zin - b)/c), flt((a*Zout - b)/c), flt(b/c)
    # pi
    R1pi, R2pi, R3pi = (flt(c*Zin*sqrt(Zout)/(a*sqrt(Zout) - 2*sqrt(k*Zin))),
                        flt(c*Zout*sqrt(Zin)/(a*sqrt(Zin) - 2*sqrt(k*Zout))),
                        flt(c/2*sqrt(Zin*Zout/k)))
    cols = int(os.environ.get("COLUMNS", 80)) - 15
    s = "Tee and pi attenuators"
    print(f"{s:^{cols}s}")
    print(f"{'-'*len(s):^{cols}s}")
    print(schematic)
    n, t = 18, " "*12
    da, o = "-"*n, " Ω"
    print(dedent(f'''
         Results given to {r.n} figures
         Attenuation = {L} dB
         Ratio       = {k}
         Zin         = {Zin}{o}
         Zout        = {Zout}{o}
                       {'pi':^{n}s}{t}{'tee':^{n}s}
                       {da:^{n}s}{t}{da:^{n}s}
         R1            {str(R1pi) + o:^{n}s}{t}{str(R1tee) + o:^{n}s}
         R2            {str(R2pi) + o:^{n}s}{t}{str(R2tee) + o:^{n}s}
         R3            {str(R3pi) + o:^{n}s}{t}{str(R3tee) + o:^{n}s}
    '''))
if __name__ == "__main__":
    d = {}
    ParseCommandLine(d)
    Results()
