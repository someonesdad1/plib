'''
Prints out tables of dB stuff.

dBm definitions
    dBm(R Ω) = 20*log(V/sqrt(R/1000))
    V = sqrt(R/1000)*10**(dBm/20)
    R = V**2*10**(-dBm/10 + 3)

Converting between different dBm voltage measures:
    dBm(R Ω) = dBm(S Ω) + C where C = 10*log(S/R)
        dBm(50) = dBm(600) + 10.8
        dBm(75) = dBm(600) + 9.0
        dBm(50) = dBm(75) + 1.8
    0 dBm(600) is 0.7746 V = sqrt(600/1000)
    0 dBm(50) is 0.2236 V = sqrt(50/1000)
    0 dBm(75) is 0.2739 V = sqrt(75/1000)

'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Prints out tables of dB stuff
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    from math import sqrt, log10 as log
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from sig import sig
if 1:   # Global variables
    sig.low = 1e-4
    W = int(os.environ["COLUMNS"]) - 1
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options]
      Print dB stuff.
    
    Options:
        -d  Print only distortion information
        -h  Print a manpage
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-d"] = False     # Print distortion data only
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dh")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("d"):
            d[o] = not d[o]
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    return args
def Distortion():
    print(f"{'Distortion in dBc converted to %':^{W}s}")
    out = ["dBc   %"]
    for dBc in range(101):
        pct = 100*10**(-dBc/20)
        out.append(f"{dBc:3d}  {sig(pct)}")
    for i in Columnize(out):
        print(i)
def dBV_dBm600():
    print(f"{'dBV to dBm(600)':^{W}s}")
    out = ["dBV  dBm(600)"]
    for dBV in range(101):
        dBm = 20*log(10**(dBV/20)/sqrt(600/1000))
        out.append(f"{dBV:3d}  {dBm:4.1f}")
    for i in Columnize(out):
        print(i)
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-d"]:
        Distortion()
        exit()
    Distortion()
    print()
    dBV_dBm600()
