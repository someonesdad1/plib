'''
Show sizes of on-hand o-rings
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Show sizes of on-hand o-rings
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    from fractions import Fraction
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from get import GetFraction
    from fraction import FormatFraction
    from f import flt
    from color import C
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    # O-ring data
    # 1.23 is inches, 1/8 is fractional inches, M1.3 is mm
    #   ID
    #   OD
    #   Cross section
    #   Material (N = nitrile, V = viton)
    #   ; Name/number (optional)
    data = '''
    # Red box
        1/8     1/4     1/16    ;F-01 Red box
        3/16    1/4     1/16    ;F-02 Red box
        1/4     3/8     1/16    ;F-03 Red box
        5/16    7/16    1/16    ;F-04 Red box
        3/8     1/2     1/16    ;F-05 Red box
        1/2     5/8     1/16    ;F-06 Red box
        3/8     9/16    3/32    ;F-07 Red box
        7/16    5/8     3/32    ;F-08 Red box
        1/2     11/16   3/32    ;F-09 Red box
        9/16    3/4     3/32    ;F-10 Red box
        5/8     13/16   3/32    ;F-11 Red box
        11/16   7/8     3/32    ;F-12 Red box
        3/4     15/16   3/32    ;F-13 Red box
        13/16   1       3/32    ;F-14 Red box
        7/8     1-1/16  3/32    ;F-15 Red box
        3/4     1       1/8     ;F-16 Red box

        15/16   1-1/16  1/8     ;F-17 Red box
        7/8     1-1/8   1/8     ;F-18 Red box
        15/16   1-3/16  1/8     ;F-19 Red box
        1       1-1/4   1/8     ;F-20 Red box
        1-1/16  1-5/16  1/8     ;F-21 Red box
        1-1/8   1-3/8   1/8     ;F-22 Red box
        1-3/16  1-7/16  1/8     ;F-23 Red box
        1-1/4   1-1/2   1/8     ;F-24 Red box
        1-5/16  1-9/16  1/8     ;F-25 Red box
        1-3/8   1-5/8   1/8     ;F-26 Red box
        1-7/16  1-11/16 1/8     ;F-27 Red box
        1-1/2   1-3/4   1/8     ;F-28 Red box
        1-5/8   1-7/8   1/8     ;F-29 Red box
        1-3/4   2       1/8     ;F-30 Red box
        1-7/8   2-1/8   1/8     ;F-31 Red box
        2       2-1/4   1/8     ;F-32 Red box

    # Plumber's Pak
        3/8     9/16    3/32    ;Plumber's Pak 2-110
        5/16    7/16    1/16    ;Plumber's Pak 2-011
        1/4     3/8     1/16    ;Plumber's Pak 2-010
        9/16    3/4     3/32    ;Plumber's Pak 2-113
        1/2     11/16   3/32    ;Plumber's Pak 2-112
        7/16    5/8     3/32    ;Plumber's Pak 2-111
        3/4     15/16   3/32    ;Plumber's Pak 2-116
        11/16   7/8     3/32    ;Plumber's Pak 2-115
        5/8     13/16   3/32    ;Plumber's Pak 2-114
        7/8     1-1/8   1/8     ;Plumber's Pak 2-210
        13/16   1-1/16  1/8     ;Plumber's Pak 2-211
        3/4     1       1/8     ;Plumber's Pak 2-212
    '''
class Size(object):
    def __init__(self, s):
        'self.value will be size in inches'
        s = s.strip()
        self.metric = False
        self.fraction = False
        if "/" in s:
            self.value = GetFraction(s)
            self.fraction = True
        elif s[0].lower() == "m":
            self.value = flt(s[1:])/25.4
            self.metric = True
        else:
            self.value = flt(s)
    @property
    def inches(self):   
        return self.value
    @property
    def mm(self):   
        return self.value*25.4
    def __repr__(self):
        return str(self)
    def __str__(self):
        x = self.value
        if self.fraction:
            return FormatFraction(x) + f" {flt(x):.3f}"
        elif self.metric:
            if int(x) == x:
                return "M" + str(int(x))
            else:
                return "M" + str(x)
        else:
            if int(x) == x:
                return str(int(x))
            else:
                return str(x)
    def __lt__(self, other):
        return self.value < other.value
def GetData():
    orings = []
    for line in data.split("\n"):
        line = line.strip()
        if not line or line[0] == "#":
            continue
        other, name = line.split(";")
        s = other.split()
        id = Size(s[0])
        od = Size(s[1])
        thickness = Size(s[2])
        orings.append((id, od, thickness, name))
    return list(sorted(orings))
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [dia1 [dia2 ...]]
      Show on-hand o-rings that are closest to the indicated diameter(s) in 
      inches.
    Options:
      -m      Use mm for diameters
      -r      Reverse sort
      -s x    Sort table by x (i = inside, o = outside, t = thickness)
      -t      Show table of all the o-rings
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-m"] = False
    d["-r"] = False
    d["-s"] = "i"
    d["-t"] = False
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "mrs:t")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("mrt"):
            d[o] = not d[o]
        elif o == "-s":
            if a not in list("iot"):
                Error("-s option must be i, o, or t")
            d[o] = a
    if d["-t"]:
        ShowTable()
        exit(0)
    return args
def ShowTable():
    k = 0
    if d["-s"] == "o":
        k = 1
    elif d["-s"] == "t":
        k = 2
    orings = GetData()
    f = lambda x: x[k]
    orings = sorted(orings, key=f, reverse=d["-r"])
    i = "Inside Diameter"
    o = "Outside Diameter"
    t = "  Thickness  "
    m = 7
    n = " "*m + "Name" + " "*m
    h = "-"
    sep = " "*3
    if d["-m"]:
        print("Table of o-ring sizes (dimensions in mm)")
    else:
        print("Table of o-ring sizes (dimensions in inches, M means metric size in mm)")
    print(dedent(f'''
    {i}{sep}{o}{sep}{t}{sep}{n}
    {h*len(i)}{sep}{h*len(o)}{sep}{h*len(t)}{sep}{h*len(n)}
    '''))
    for id, od, thickness, name in orings:
        if d["-m"]:
            print(f"{str(id.mm()):^{len(i)}s}{sep}{str(od.mm()):^{len(o)}s}{sep}"
                f"{str(thickness.mm()):^{len(t)}s}{sep}{name}")
        else:
            print(f"{str(id):^{len(i)}s}{sep}{str(od):^{len(o)}s}{sep}"
                f"{str(thickness):^{len(t)}s}{sep}{name}")
def ShowMatches(dia):
    def KeepSmallest(seq):
        'Return a list containing only the smallest first items of seq'
        seq = sorted(seq)
        keep = [seq[0]]
        smallest = seq[0][0]
        n = 1
        while len(seq) > n - 1 and seq[n][0] == smallest:
            keep.append(seq[n])
            n += 1
        return keep
    def Show(item):
        absdiff, diff, oring = item
        id, od, t, name = oring
        if not diff:    # Exact matches are in color
            print(f"{C.lgrn}    ID = {id}, OD = {od}, T = {t}, {name}{C.norm}")
        else:
            print(f"    diff = {diff}  ID = {id}, OD = {od}, T = {t}, {name}")
    if "/" in dia:
        D = flt(GetFraction(dia))
        is_fraction = True
    else:
        D = flt(dia)
        is_fraction = False
    if d["-m"]:
        D /= 25.4
    ID, OD, T = [], [], []
    # Compute the difference for each from the target value and sort to
    # find the closest.
    for item in orings:
        id, od, thickness, name = item
        i, o, t = id.inches - D, od.inches - D, thickness.inches - D
        ID.append((abs(i), i, item))
        OD.append((abs(o), o, item) )
        T.append((abs(t), t, item))
    ID = KeepSmallest(ID)
    OD = KeepSmallest(OD)
    u = f"{'mm' if d['-m'] else 'inches'}"
    print("Diameters in inches")
    print(f"Search value = {dia} {u}", end=" ")
    if d["-m"]:
        print(f"= {flt(dia)/25.4:.3f} inches")
    else:
        print()
    print(f"  Closest ID match(es):")
    for item in ID:
        Show(item)
    print(f"  Closest OD match(es):")
    for item in OD:
        Show(item)
    if 0:   # Don't show thicknesses (maybe later)
        print(f"  Closest thickness match(es):")
        for item in T:
            Show(item)
if __name__ == "__main__":
    d = {}      # Options dictionary
    diameters = ParseCommandLine(d)
    orings = GetData()
    for dia in diameters:
        ShowMatches(dia)
