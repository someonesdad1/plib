'''
Given a voltage divider total resistance and ratio, print out the closest
divider that can be made with on-hand resistors.
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
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    from collections import namedtuple
    from itertools import combinations
if 1:   # Custom imports
    from wrap import dedent
    from resistors import Resistors, GetClosest
    from sig import sig
    from u import ParseUnit, SI_prefixes
    from fpformat import FPFormat
if 1:   # Global variables
    number_limit_default = 20
    fp = FPFormat(num_digits=3)
    fp.trailing_decimal_point(False)
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    n = number_limit_default
    print(dedent(f'''
    Usage:  {name} [options] R ratio [n]
      For the indicated total resistance R and desired ratio, print out the
      resistors to use from the on-hand set that give the closest fit.  You can
      specify n matches to print; it defaults to {n}.  Set n to 0 to show all
      possible dividers from the on-hand set of resistors.
    
    {name} -2 R V0 V1 V2
      Given a potiometer of resistance R, calculate the two resistors needed to
      let the pot adjust between V1 and V2 when the two resistors and the pot
      are in series with the pot in the middle and V0 across the three
      resistances.
    
    Options
      -2        Solve the problem 2 problem
      -t res    Set the minimum ratio of Rtotal/Rdesired to keep
      -T res    Set the maximum ratio of Rtotal/Rdesired to keep
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-2"] = False
    d["-t"] = None
    d["-T"] = None
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "2t:T:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-t", "-T"):
            d[o] = GetR(a)
        elif o in ("-2",):
            Problem2(args, d)
            exit(0)
    if len(args) not in (2, 3):
        Usage(d)
    if len(args) == 2:
        args.append(number_limit_default)
    sig.digits = 3
    sig.rtz = True
    return args
def Combinations(R):
    '''Get the combinations of the paired resistors, then add in each
    resistor paired with itself.
    '''
    a = list(combinations(Resistors(), 2))
    return a + [(i, i) for i in R]
def GetR(s):
    '''s is a string that can have a cuddled SI prefix.
    '''
    val, prefix = ParseUnit(s)
    val = float(val)
    if prefix:
        val *= float(SI_prefixes[prefix])
    return val
def Pct(p):
    '''Return float p as a string.  If it's < 10, return it to two
    significant figures; otherwise, make it an integer.
    '''
    if p < 0.01:
        return "0"
    elif p < 10:
        return sig(p, 2)
    return str(int(p))
def GetMatches(candidates, delta):
    matches = []
    for c in candidates:
        if c.dr <= delta and c.dratio <= delta:
            matches.append(c)
    return matches
def Include(dr, d):
    '''If dr satisfies the -t and -T options, return True; otherwise return
    False.
    '''
    if d["-t"] is not None and d["-T"] is not None:
        return d["-t"] <= dr <= d["-T"]
    if d["-t"] is not None:
        return dr >= d["-t"]
    if d["-T"] is not None:
        return dr <= d["-T"]
    return True  # Keep everything if no limits set
def Show_dr(dr):
    dR = sig(dr)
    if not dR:
        return " .0"
    elif str(dR)[0] == "0":
        return " " + str(dR)[1:]
    return str(dR)
def FindResistors(Rtotal, desired_ratio, number_limit, d):
    eng = fp.engsic
    matches = []
    C = namedtuple("Candidate", "dr dratio ratio rtotal R1 R2")
    resistor_set = Resistors()
    comb = Combinations(Resistors())
    n = len(resistor_set)
    N = len(comb)
    f = lambda x, y:  round(abs(x/y - 1), 4)
    for R1, R2 in comb:
        rtotal = R1 + R2
        ratio = R1/rtotal
        dr, dratio = rtotal/Rtotal, f(ratio, desired_ratio)
        if Include(dr, d):
            matches.append(C(dratio, dr, ratio, rtotal, R1, R2))
        ratio = R2/rtotal
        dratio = f(ratio, desired_ratio)
        if Include(dr, d):
            matches.append(C(dratio, dr, ratio, rtotal, R2, R1))
    matches = list(sorted(matches))
    if number_limit:
        matches = matches[:number_limit]
    print("Rtotal = {}, ratio = {}".format(eng(Rtotal), sig(desired_ratio)))
    print(dedent(f'''
    {n} resistors in on-hand set
    {N} pairwise combinations examined
    Scores:
        - Ratio score closest to zero is best
        - Rtotal score nearest 1 is best
     
        Scores             Actual
    Ratio    Rtotal    Ratio   Rtotal      R1       R2
    ---------------    --------------    ------   ------'''))
    for candidate in matches:
        drat, dr, ratio, rtotal, R1, R2 = candidate
        print("{:^6s}   {:6s}    {:8s} {:8s} {:^8s} {:^8s}".format(
            Pct(100*drat), Show_dr(dr), sig(ratio, 3), eng(rtotal),
            eng(R1), eng(R2)))
def Problem2(args, d):
    E = fp.engsi
    if len(args) != 4:
        Error("Need 4 arguments (R, V, V1, V2) for -2 option")
    R, V, V1, V2 = args
    V, V1, V2 = [float(i) for i in (V, V1, V2)]
    if not (V > V1 > V2 > 0):
        Error("Voltages on command line must be strictly decreasing and > 0")
    R = GetR(R)
    R1 = R*(V - V1)/(V1 - V2)
    R2 = R*V2/(V1 - V2)
    try:
        R1c = GetClosest(R1)
        R2c = GetClosest(R2)
    except ValueError as e:
        print(str(e))
        exit(1)
    i = V/(R + R1 + R2)
    # Print report
    i, R, V, V1, V2 = [E(i) for i in (i, R, V, V1, V2)]
    R1, R2, R1c, R2c = [E(i) for i in (R1, R2, R1c, R2c)]
    print(dedent(r'''
                         ◯ Vout
                         |
                         ↓
    Ground  ◯--\/\/\---\/\/\---\/\/\---◯ V 
                 R2      R       R1
    
    Two resistors R1 and R2 with pot between them.  Pot adjustment gives V1
    across R1 and V2 across R2 and the pot adjusts Vout continuously between
    them.
        V  = {V}V
        V1 = {V1}V
        V2 = {V2}V
        R1 = {R1}Ω (closest is {R1c}Ω)
        R2 = {R2}Ω (closest is {R2c}Ω)
        i = {i}A
    ''').format(**locals()))
if __name__ == "__main__":
    d = {}      # Options dictionary
    R, ratio, number_limit = ParseCommandLine(d)
    R = GetR(R)
    ratio = eval(ratio)
    FindResistors(R, ratio, int(number_limit), d)
