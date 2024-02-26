'''
Print out dimensions of various machine tapers.
'''
 
# Copyright (C) 2020 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Academic Free License version 3.0.
# See http://opensource.org/licenses/AFL-3.0.
#
 
if 1:   # Imports & globals
    import getopt
    import os
    import sys
    from fractions import Fraction
    from math import atan, pi
 
    # Debugging stuff
    from pdb import set_trace as xx
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d, status=1):
    name = sys.argv[0]
    s = '''
Usage:  {name} [options] 
  Print out dimensions in inches of various machine tapers.  Morse and Jacobs
  tapers are printed by default; use -a to include Jarno and B&S.

Options:
  -a    Print all tapers.
  -m    Print dimensions in mm.
'''[1:-1]
    print(s.format(**locals()))
    exit(status)

def ParseCommandLine():
    d = opt
    d["-a"] = False
    d["-m"] = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ahm")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("am"):
            d[o] = not d[o]
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    return args

def MorseTapers():
    data = (
        # Ref:  MH, 19th ed., pg 1679.
        # tpf = taper in inches per foot
        # A = large diameter at end of socket
        # H = hole depth
        #      tpf       A      H
        (0, 0.62460, 0.3561, 2 + Fraction(1/32)),
        (1, 0.59858, 0.475 , 2 + Fraction(5/32)),
        (2, 0.59941, 0.700 , 2 + Fraction(39/64)),
        (3, 0.60235, 0.938 , 3 + Fraction(1/4)),
        (4, 0.62326, 1.231 , 4 + Fraction(1/8)),
        (5, 0.63151, 1.748 , 5 + Fraction(1/4)),
        (6, 0.62565, 2.494 , 7 + Fraction(21/64)),
        (7, 0.62400, 3.270 , 10 + Fraction(5/64)),
    )
    if opt["-m"]:
        print(f'''
Morse Tapers (dimensions in mm)
           Large   Small             Slope    Included
    Num     Dia     Dia   Length    (D-d)/L   Angle, °
    ---   ------  ------  ------    -------   --------
'''[1:-1])
        f = lambda x: x*25.4
        for i in data:
            MT, tpf, D, H = i
            X = 1/32 if MT == 0 else 1/16
            L = H - X
            d = D - tpf*L/12
            angle = 2*atan((D - d)/(2*L))*180/pi
            slope = (D - d)/L
            print(f"     {MT}    "
                f"{f(D):>6.2f} "
                f"{f(d):>7.2f} "
                f"{f(L):>7.1f} "
                f"{slope:>10.5f} "
                f"{angle:>9.3f} "
            )
    else:
        print(f'''
Morse Tapers (dimensions in inches)
           Large   Small             Taper    Included
    Num     Dia     Dia   Length    per ft.   Angle, °
    ---   ------  ------  ------    -------   --------
'''[1:-1])
        for i in data:
            MT, tpf, D, H = i
            X = 1/32 if MT == 0 else 1/16
            L = H - X
            d = D - tpf*L/12
            angle = 2*atan((D - d)/(2*L))*180/pi
            print(f"     {MT}    "
                f"{D:>6.4f} "
                f"{d:>7.4f} "
                f"{L:>7.2f} "
                f"{tpf:>10.5f} "
                f"{angle:>9.3f} "
            )

def Jarno():
    'See MH, 19th ed., pg 1683'
    def Get(n):
        assert(2 <= n <= 20)
        D, d, L = n/8, n/10, n/2
        return D, d, L
    if opt["-m"]:
        print(f'''
Jarno Tapers (dimensions in mm)
           Large   Small             Slope    Included
    Num     Dia     Dia   Length    (D-d)/L   Angle, °
    ---   ------  ------  ------    -------   --------
'''[1:-1])
        f = lambda x: x*25.4
        for n in range(2, 21):
            D, d, L = Get(n)
            angle = 2*atan((D - d)/(2*L))*180/pi
            slope = (D - d)/L
            print(f"    {n:2d}    "
                f"{f(D):>6.2f} "
                f"{f(d):>7.2f} "
                f"{f(L):>7.1f} "
                f"{slope:>10.5f} "
                f"{angle:>9.3f} "
            )
    else:
        print(f'''
Jarno Tapers (dimensions in inches)
           Large   Small             Taper    Included
    Num     Dia     Dia   Length    per ft.   Angle, °
    ---   ------  ------  ------    -------   --------
'''[1:-1])
        for n in range(2, 21):
            D, d, L = Get(n)
            tpf = (D - d)/(L/12)
            angle = 2*atan((D - d)/(2*L))*180/pi
            print(f"    {n:>2d}    "
                f"{D:>6.4f} "
                f"{d:>7.4f} "
                f"{L:>7.2f} "
                f"{tpf:>10.5f} "
                f"{angle:>9.3f} "
            )

def BS():
    'Reference MH, 19th ed., pg 1682'
    data = (
        #No. tpf(inch), d, L]
        (1 , 0.50200, 0.20000, Fraction(15/16)),
        (2 , 0.50200, 0.25000, 1 + Fraction(3/16)),
        (3 , 0.50200, 0.31250, 1 + Fraction(1/2)),
        (4 , 0.50240, 0.35000, 1 + Fraction(11/16)),
        (5 , 0.50160, 0.45000, 2 + Fraction(1/8)),
        (6 , 0.50329, 0.50000, 2 + Fraction(3/8)),
        (7 , 0.50147, 0.60000, 2 + Fraction(7/8)),
        (8 , 0.50100, 0.75000, 3 + Fraction(9/16)),
        (9 , 0.50085, 0.90010, 4 + Fraction(1/4)),
        (10, 0.51612, 1.04465, 5),
        (11, 0.50100, 1.24995, 5 + Fraction(15/16)),
        (12, 0.49973, 1.50010, 7 + Fraction(1/8)),
        (13, 0.50020, 1.75005, 7 + Fraction(3/4)),
        (14, 0.50000, 2.00000, 8 + Fraction(1/4)),
        (15, 0.50000, 2.25000, 8 + Fraction(3/4)),
        (16, 0.50000, 2.50000, 9 + Fraction(1/4)),
        (17, 0.50000, 2.75000, 9 + Fraction(3/4)),
        (18, 0.50000, 3.00000, 10 + Fraction(1/4)),
    )
    if opt["-m"]:
        print(f'''
Brown & Sharpe Tapers (dimensions in mm)
           Large   Small             Slope    Included
    Num     Dia     Dia   Length    (D-d)/L   Angle, °
    ---   ------  ------  ------    -------   --------
'''[1:-1])
        f = lambda x: x*25.4
        for i in data:
            n, tpf, d, L = i
            L = float(L)
            tpi = tpf/12
            D = d + L*tpi
            angle = 2*atan((D - d)/(2*L))*180/pi
            slope = (D - d)/L
            print(f"    {n:2d}    "
                f"{f(D):>6.2f} "
                f"{f(d):>7.2f} "
                f"{f(L):>7.1f} "
                f"{slope:>10.5f} "
                f"{angle:>9.3f} "
            )
    else:
        print(f'''
Brown & Sharpe Tapers (dimensions in inches)
           Large   Small             Taper    Included
    Num     Dia     Dia   Length    per ft.   Angle, °
    ---   ------  ------  ------    -------   --------
'''[1:-1])
        for i in data:
            n, tpf, d, L = i
            L = float(L)
            tpi = tpf/12
            D = d + L*tpi
            angle = 2*atan((D - d)/(2*L))*180/pi
            print(f"    {n:>2d}    "
                f"{D:>6.4f} "
                f"{d:>7.4f} "
                f"{L:>7.2f} "
                f"{tpf:>10.5f} "
                f"{angle:>9.3f} "
            )

def JacobsTapers():
    'Reference MH, 19th ed, p 1690'
    data = (
        #No    D       d        L
        (0 , 0.2500, 0.22844, 0.43750),
        (1 , 0.3840, 0.33341, 0.65625),
        (2 , 0.5590, 0.48764, 0.87500),
        (3 , 0.8110, 0.74610, 1.21875),
        (4 , 1.1240, 1.03720, 1.65630),
        (5 , 1.4130, 1.31610, 1.87500),
        (6 , 0.6760, 0.62410, 1.00000),
        (33, 0.6240, 0.56050, 1.00000),
    )
    if opt["-m"]:
        print(f'''
Jacobs Tapers (dimensions in mm)
           Large   Small             Slope    Included
    Num     Dia     Dia   Length    (D-d)/L   Angle, °
    ---   ------  ------  ------    -------   --------
'''[1:-1])
        f = lambda x: x*25.4
        for i in data:
            n, D, d, L = i
            angle = 2*atan((D - d)/(2*L))*180/pi
            slope = (D - d)/L
            print(f"    {n:2d}    "
                f"{f(D):>6.2f} "
                f"{f(d):>7.2f} "
                f"{f(L):>7.1f} "
                f"{slope:>10.5f} "
                f"{angle:>9.3f} "
            )
    else:
        print(f'''
Jacobs Tapers (dimensions in inches)
           Large   Small             Taper    Included
    Num     Dia     Dia   Length    per ft.   Angle, °
    ---   ------  ------  ------    -------   --------
'''[1:-1])
        for i in data:
            n, D, d, L = i
            tpf = (D - d)/(L/12)
            angle = 2*atan((D - d)/(2*L))*180/pi
            print(f"    {n:>2d}    "
                f"{D:>6.4f} "
                f"{d:>7.4f} "
                f"{L:>7.2f} "
                f"{tpf:>10.5f} "
                f"{angle:>9.3f} "
            )

if __name__ == "__main__":
    opt = {}      # Options dictionary
    ParseCommandLine()
    if opt["-a"]:
        Jarno()
        print()
        BS()
        print()
    JacobsTapers()
    print()
    MorseTapers()
