'''
Design of a hammer
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
    # Calculate mass of a cylindrical hammer head
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from f import flt, pi
if 1:   # Global variables
    specific_gravity = []
    for line in '''
        Aluminum       : 2.7
        Ash            : 0.68
        Babbitt        : 7.28
        Brass          : 8.6
        Bronze         : 8.2
        Cast iron      : 7.87
        Cherry         : 0.6
        Copper         : 8.96
        Douglas fir    : 0.51
        Lead           : 11.4
        Oak            : 0.75
        Pine           : 0.42
        Polyethylene   : 0.95
        Steel          : 7.86
        Sugar maple    : 0.68
        Zinc           : 7.13'''.split("\n"):
        if not line.strip():
            continue
        name, value = [i.strip() for i in line.split(":")]
        rho = flt(1000*float(value), units="kg/m3")
        specific_gravity.append((name, rho))
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] diameter length
      Print out mass in lb and kg of a hammer head of the given diameter and
      length in inches for various materials.
    Options:
        -m      Use mm for dimensions
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-b"] = False
    d["-l"] = False
    d["-m"] = False
    d["-s"] = False
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "bhlms")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-b", "-l", "-m", "-s"):
            d[o] = not d[o]
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    if len(args) != 2:
        Usage(d)
    return args
def PrintMass(D, L):
    'D = diameter in m, L = length in m'
    D.rtz = True
    A = area = D**2*pi/4
    V = volume = area*L
    print(dedent('''
    Mass of hammer
    --------------
    '''))
    print(f"  Diameter = {D.to('inch')} = {D.to('mm')}")
    print(f"  Length   = {L.to('inch')} = {L.to('mm')}")
    print(f"  Volume   = {V.to('inch3')} = {V.to('liter')}")
    print(dedent(f'''
    
      Material        rho       lbm          kg
    --------------   -----     -----       -------'''))
    n = 12
    for name, rho in specific_gravity:
        m = V*rho
        lb = flt(m.to("lb").val)
        kg = flt(m.to("kg").val)
        spgr = flt(rho.to("g/mL").val)
        print(f"{name:<14s}   {spgr!s:^6s} {lb!s:^{n}s} {kg!s:^{n}s}")
    print(f"rho is specific gravity in g/mL")
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    D, L = [flt(i, "inches") for i in args]
    if d["-m"]:
        D, L = [flt(i, "mm") for i in args]
    PrintMass(D, L)
