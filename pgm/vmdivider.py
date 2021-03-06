'''
TODO

    * Include the -2 problem solving of a pot with two resistors in the
      obsolete/divider.py script.

    * Since the equations are available, allow an uncertainty analysis to
      be done on the voltage ratios using the calculated resistors and an
      assumed tolerance %.  The uncertainty of the resistors will be
      assumed to be triangular and the uncertainty will be 1/sqrt(6) times
      the percentage half-width.
      
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
    # Solve a voltage divider problem to help design a divider for e.g. a
    # voltmeter.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from resistors import Resistors, GetClosest
    from fpformat import FPFormat
    from f import *
    from color import C
    import u
if 1:   # Global variables
    class g: pass
    g.exact = C.lcyn
    g.ser = C.yel
    g.par = C.grn
    g.dev = C.lmag
    g.err = C.lred
    g.norm = C.norm
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] R ratio1 ratio2 [ratio3 ...]
      Design a voltage divider for the input of a voltmeter.  R is the
      total divider resistance in ohms.  The ratios must be floating point
      numbers on the open interval (0, 1).  Expressions are allowed.  My
      on-hand resistor set is used by default (change to your set if
      needed).  R can contain a cuddled SI prefix and the units are assumed
      to be ohms.
    Problem 2
        {sys.argv[0]} -2 R V V1 V2
      The -2 option allows you to solve for the case of using a pot of
      value R to adjust a voltage between V1 and V2 with a supply voltage
      of V.  The script solves for the two resistors on either side of the
      pot.
    Options:
        -2      Solve problem 2
        -E e    Use an EIA resistor set
        -h      Print a manpage (more detailed documentation)
    '''))
    print(s)
    exit(status)
def Manpage():
    print(dedent(f'''
    The schematic is

        o-------+-----------o  ρ0
                |
                R1
                |
        o-------+-----------o  ρ1
                |
                R2
                |
        o-------+-----------o  ρ2
                |
            ...
                |
        o-------+-----------o  ρ(n - 1)
                |
                Rn
                |
                +-----------o  ρn
                |
            GND
    
    The equations are
    
        R = total resistance = sum{{i=1}}{{n}}Ri
    
        R1 = R*(1 - ρ1)
        Ri = R*(ρ(i-1) - ρi), i = 2, 3, ..., n-1
        Rn = R*ρ(n-1)

    If we define ρ0 = 1 and ρn = 0, we have the solution

        Ri = R*(ρ(i-1) - ρi) where i = 1, 2, ..., n

    The inverse equations are

        ρ1 = 1 - R1/R
        ρi = ρ(i-1) - Ri/R
        ρ(n-1) = Rn/R

    Algorithm
        * Solve for the needed resistances.
        * For each resistance, get the two resistors (parallel or series)
          that best give the needed resistance.
        * Calculate the actual ratios and total resistance.
        * Report the information.

    EIA resistor set
      To use an EIA set of resistors, use the -E option with an argument of
      the form
            'n e1 e2 ...'
      where n is an integer 6, 12, 24, 48, or 96 and e1, e2, ... are
      integers that give the power of ten for each decade of resistors (the
      numbers can be separated by spaces or commas).  For example, '6 -1 0
      1 2 3 4 5 6' would represent the set of six EIA resistance values E6
      (1, 1.5, 2.2, 3.3, 4.7, and 6.8) with multiplers of 1e-1, 1e0, 1e1,
      ..., 1e6.  The result would be a set of 48 different resistor values.

    Example
        I have an analog meter from an old HP instrument that has 0-1 and
        0-3 scales.  It requires 1 mA for full scale deflection, which is
        also 250 mV due to the meter's resistance (these are very nice
        meters made by Weston that were used in the HP 400H VTVM in the
        1950's).

        I would like to use this meter to make an analog voltmeter that
        measures DC voltages with full-scale ranges of 0.1, 0.3, 1, 3, 10,
        30, 100, and 300 V.  I want the input resistance to be 10 MΩ.  The
        voltage divider ratios need to be such that the input voltage is
        divided down to 100 mV (I'll use an op amp to get the required 250
        mV).  The ratios needed are thus 0.1 divided by the range, or 1,
        1/3, 1/10, 1/30, 1/100, 1/300, 1/1000, and 1/3000.  We ignore the 1
        and use the following command line (note the use of expressions):

        {sys.argv[0]} 10M 1/3 1/10 1/30 1/100 1/300 1/1000 1/3000

        The result is
            Voltage divider command line:
            '10M 1/3 1/10 1/30 1/100 1/300 1/1000 1/3000'
            Total resistance = 10 MΩ
            Desired ratios
                    0.3333
                    0.1
                    0.0333
                    0.01
                    0.0033
                    0.001
                    0.0003
            Resistors needed
                    6.667 MΩ
                    2.333 MΩ
                    666.7 kΩ
                    233.3 kΩ
                    66.67 kΩ
                    23.33 kΩ
                    6.667 kΩ
                    3.333 kΩ
            Using the on-hand resistor set (% is deviation from needed)
                    6.674 MΩ        [0;33;40m674 kΩ + 6 MΩ [1;35;40m0.11%[0;37;40m
                    2.333 MΩ        [0;32;40m4 MΩ || 5.6 MΩ[0;37;40m
                    666.7 kΩ        [0;32;40m1.2 MΩ || 1.5 MΩ[0;37;40m
                    233.3 kΩ        [0;33;40m13.3 kΩ + 220 kΩ [1;35;40m-0.014%[0;37;40m
                    66.72 kΩ        [0;32;40m67 kΩ || 16 MΩ [1;35;40m0.081%[0;37;40m
                    23.33 kΩ        [0;33;40m1.33 kΩ + 22 kΩ [1;35;40m-0.014%[0;37;40m
                    6.667 kΩ        [0;32;40m10 kΩ || 20 kΩ[0;37;40m
                    3.333 kΩ        [0;32;40m5 kΩ || 10 kΩ[0;37;40m
            Actual ratios (% is deviation from goal)
                    0.3331         [1;35;40m-0.073%[0;37;40m
                    0.0999         [1;35;40m-0.072%[0;37;40m
                    0.0333         [1;35;40m-0.068%[0;37;40m
                    0.01           [1;35;40m-0.023%[0;37;40m
                    0.0033         [1;35;40m-0.083%[0;37;40m
                    0.001          [1;35;40m-0.073%[0;37;40m
                    0.0003         [1;35;40m-0.073%[0;37;40m

    '''))
    ColorCoding()
    print(dedent(f'''

    Problem 2
        The -2 option solves the following problem:

                                ◯ Vout
                                |
                                V
            Ground  ◯--\/\/\---\/\/\---\/\/\---◯ V 
                        R1      R       R2

        Two resistors R1 and R2 have a pot of resistance R between them.
        When V is applied across the pot and two resistors, the pot
        adjustment allows you to have voltages between V1 and V2 at the
        Vout terminal.  The script prints out 1) the resistances needed and
        2) the current that will pass through the pot and resistors when
        the Vout terminal is open.

    '''.rstrip()))
    exit(0)
def ColorCoding():
    print(dedent(f'''
        The color coding in the report is:
            {g.dev}Deviation in % from goal{g.norm}
            {g.err}Needed resistor is not available{g.norm}
            {g.exact}Deviation is zero to about 6 figures{g.norm}
            {g.ser}Resistors are in series {g.norm}
            {g.par}Resistors are in parallel {g.norm}
    ''', n=4))
def ParseCommandLine():
    d["-2"] = False     # Solve problem 2
    d["-d"] = 4         # Number of significant digits
    d["-E"] = None      # EIA set specifier
    d["command_line"] = ' '.join(sys.argv[1:])
    try:
        opts, args = getopt.getopt(sys.argv[1:], "2d:Eh")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("2a"):
            d[o] = not d[o]
        elif o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = ("-d option's argument must be an integer between "
                       "1 and 15")
                Error(msg)
        elif o in ("-h", "--help"):
            Manpage()
    if len(args) < 2:
        Usage(d)
    d["fp"] = FPFormat()
    d["fp"].digits(d["-d"])
    d["fp"].trailing_decimal_point(False)
    d["ohm"] = "Ω"
    x = flt(0)
    x.n = 2     # Used for percent deviations
    x.rtz = True
    return args
def ProcessArguments(args):
    if 1:  # Get the total resistance
        r = args.pop(0)
        x, unit = u.ParseUnit(r)
        if unit and unit not in u.SI_prefixes:
            Error(f"Non-SI suffix on total resistance '{r}'")
        factor = u.u(unit + "m")
        try:
            R = eval(x)
        except Exception:
            Error(f"'{x}' isn't a proper form for a number expression")
        R *= factor     # Multiply by SI prefix
        d["R"] = R
    if 1:  # Expand the arguments into ratios
        ratios = []
        for arg in args:
            try:
                x = eval(arg)
                ratios.append(x)
            except Exception:
                Error(f"'{arg}' isn't a proper form for a number expression")
        if not ratios:
            Error(f"Need at least one ratio")
        # The ratios must be sorted in descending order
        ratios = list(reversed(sorted(ratios)))
        # None of the ratios can be equal and all must be > 0 and < 1
        if not all([i > 0 for i in ratios]):
            Error("All ratios must be > 0")
        if not all([i < 1 for i in ratios]):
            Error("All ratios must be < 1")
        if len(set(ratios)) != len(ratios):
            Error("All ratios must be different")
        # Make the first element unity
        ratios.insert(0, 1)
        d["ratios"] = ratios
def GetEIA():
    '''Return (n, pow0, pow1, ...) where n is the EIA series and pow0,
    etc. are the powers of 10.
    '''
    s = d["-E"]
    s = s.replace(",", " ")
    f = [int(i) for i in s.split()]
    n = f.pop(0)
    assert n in set((6, 12, 24, 48, 96))
    f.insert(n, 0)
    return f
def GetResistors():
    if d["-E"]:
        f = GetEIA()
        d["resistors"] = Resistors(EIA=f[0], powers_of_10=f[1:])
    else:
        d["resistors"] = Resistors()  # On-hand set
def Fix(x):
    'Format with fpformat.fix and remove trailing zeros'
    fp = d["fp"]
    s = fp.fix(x)
    while s and s[-1] == "0":
        s = s[:-1]
    return s
def Fmt(R):
    '''Format a resistance R.  Use engsi format, but remove trailing zeros
    and remove the decimal point if possible.
    '''
    fp = d["fp"].engsi
    t = fp(R) + d["ohm"]
    s, u = t.split()
    while s and s[-1] == "0":
        s = s[:-1]
    if s and s[-1] == ".":
        s = s[:-1]
    return ' '.join([s, u])
def SolveSystem():
    fp = d["fp"]
    F = Fmt
    Rtotal, ratios = d["R"], d["ratios"]
    n = len(ratios)
    ind, k = " "*8, 12
    R = [0]*n
    # Calculate resistances
    for i in range(1, len(ratios)):
        R[i] = Rtotal*(ratios[i - 1] - ratios[i])
    # Get rid of initial 0
    R.pop(0)
    # Get last resistance
    R.append(Rtotal - sum(R))
    # Format values
    Rs = [F(i) for i in R]
    # Print results
    print(f"Voltage divider command line:\n  '{d['command_line']}'")
    print(f"  Total resistance = {F(Rtotal)}")
    print(f"  Desired ratios")
    for r in ratios[1:]:
        print(f"{ind}{Fix(r)}")
    print(f"  Resistors needed")
    for r in Rs:
        print(f"{ind}{r}")
    # Get the closest resistors to what we need
    Rclosest = []
    try:
        for r in R:
            Rclosest.append(GetClosest(r, resistors=d["resistors"],
                                    series=True, parallel=True))
    except Exception:
        print(f"{g.err}The needed resistor {F(r)} is not in the resistor set{g.norm}")
        exit(1)
    t = f"EIA{GetEIA()[0]}" if d["-E"] else "on-hand"
    print(f"  Using the {t} resistor set (% is deviation from needed)")
    Rtotal_actual = 0
    Ractual = []
    nearly_exact = 1e-6
    for i, r in enumerate(Rclosest):
        if isinstance(r, list):
            R1, R2, rdiff, typ = r
            if typ == "series":
                Rt = R1 + R2
                dev = flt((Rt - R[i])/R[i])
                if abs(dev) < nearly_exact:
                    Re = f"{g.ser}{F(R1)} + {F(R2)}{g.norm}"
                else:
                    Re = f"{g.ser}{F(R1)} + {F(R2)} {g.dev}{100*dev}%{g.norm}"
            else:
                Rt = 1/(1/R1 + 1/R2)
                dev = flt((Rt - R[i])/R[i])
                if abs(dev) < nearly_exact:
                    Re = f"{g.par}{F(R1)} || {F(R2)}{g.norm}"
                else:
                    Re = f"{g.par}{F(R1)} || {F(R2)} {g.dev}{100*dev}%{g.norm}"
            Rtotal_actual += Rt
            Ractual.append(Rt)
            print(f"{ind}{F(Rt):{k}s}    {Re}")
        else:
            Rtotal_actual += r
            Ractual.append(r)
            print(f"{ind}{F(r):{k}s}")
    print(f"  Actual ratios (% is deviation from goal)")
    ρactual = []
    for i in range(len(Ractual)):
        if not i:
            ρactual.append(1 - Ractual[i]/Rtotal_actual)
        else:
            ρactual.append(ρactual[i - 1] - Ractual[i]/Rtotal_actual)
    for i, ratio in enumerate(ρactual[:-1]):
        goal = ratios[i + 1]
        dev = flt((ratio - goal)/goal)
        if abs(dev) < nearly_exact:
            print(f"{g.exact}{ind}{Fix(ratio):{k}s}{C.norm}")
        else:
            with dev:
                dev.n = 2
                print(f"{ind}{Fix(ratio):{k}s}   {g.dev}{100*dev}%{g.norm}")
def GetR(s):
    's is a string that can have a cuddled SI prefix'
    val, prefix = u.ParseUnit(s)
    val = flt(val)
    if prefix:
        val *= flt(u.SI_prefixes[prefix])
    return val
def Problem2(args):
    E = d["fp"].engsi
    if len(args) != 4:
        Error("Need 4 arguments (R, V, V1, V2) for -2 option")
    R, V, V1, V2 = args
    V, V1, V2 = [flt(i) for i in (V, V1, V2)]
    if V1 < V2:
        V1, V2 = V2, V1
    if not (V > V1 > 0):
        Error(f"V ({V}) must be greater than {max((V1, V2))}")
    if V1 <= 0 or V2 <= 0:
        Error("V1 and V2 must be greater than 0")
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
    i, V, V1, V2 = [E(i) for i in (i, V, V1, V2)]
    R, R1, R2, R1c, R2c = [Fmt(i) for i in (R, R1, R2, R1c, R2c)]
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
        R1 = {R1} (closest is {R1c})
        R2 = {R2} (closest is {R2c})
        i = {i}A
    ''').format(**locals()))
    exit(0)
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine()
    if d["-2"]:
        Problem2(args)
    ProcessArguments(args)
    GetResistors()
    SolveSystem()
