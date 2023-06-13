'''
Print out lead-acid battery voltage as function of temperature
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Print out lead-acid battery voltage as function of temperature
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} temp [c_or_f]
      Print out a table of the voltage of a lead-acid battery at
      temperature temp, which must be an integer divisible by 10.
      Use c for °C and f for degrees °F.  Allow half a day for
      the battery to reach equilibrium after charging.
    '''))
    exit(status)
def ParseCommandLine(d):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-h", "--help"):
            Usage(d, status=0)
    if not args:
        Usage(d)
    return args
def C(T_degF):
    return 5/9*(T_degF - 32)
def V(pct_chg, T_degC):
    '''I cannot attribute this formula for lead-acid battery voltage as a
    function of % of charge and electrolyte temperature, as I found it many
    years ago and didn't write down the source.
    '''
    return (pct_chg/100 + 15.5151)/1.3065 + (T_degC - 26.7)/231.7
if __name__ == "__main__":
    d = {}      # Options dictionary
    flt(0).n = 4
    args = ParseCommandLine(d)
    T = int(args[0])
    if T % 10 != 0:
        print("temp must be divisible by 10")
        exit(1)
    degC = True
    if len(args) == 2:
        degC = True if args[1] == "c" else False
    w = int(os.environ.get("COLUMNS", 80)) - 1 
    print(f"{'Lead-Acid Battery Voltage':^{w}s}")
    n = 6
    print(f"{T} °{'C' if degC else 'F'}")
    print(" %  ", end="")
    for i in range(10):
        print(f"{T + i:^{n}d} ", end="")
    print()
    print("--- ", end="")
    for i in range(10):
        print(f"{'-'*n:^{n}s} ", end="")
    print()
    for pct in range(0, 101, 10):
        print(f"{pct:3d}", end=" ")
        for T_offset in range(10):
            T0 = T + T_offset
            if not degC:
                T0 = C(T0)  # Change F to C
            v = V(pct, T0)
            print(f"{v:{n}.3f}", end=" ")
        print()
    print()
