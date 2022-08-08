'''
Select from on-hand resistors to make a voltage divider or a given
resistance value from a pair of resistors in series or parallel
 
    Change the on_hand global variable to reflect the resistors you have.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Select from on-hand resistors to make a voltage divider or a given
    # resistance value from a pair of resistors in series or parallel
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    from math import *
    from itertools import combinations
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from sig import sig
    from fpformat import FPFormat
    from columnize import Columnize
    from color import C, fg, normal, yellow as highlight, lred, lgreen
    from u import u, ParseUnit, SI_prefixes
if 1:   # Global variables
    fp = FPFormat()
    fp.trailing_dp = False
    # On-hand resistor values.  Change these entries to match what you have.
    on_hand = dedent('''

    0.025 0.18 0.2 0.27 0.33           1 2.2 4.6 8.3

    10.1 12 14.7 15 17.8 22 27 28.4 30 31.6 33 35 38.4 46.3 50 55.5 61.8 67
    75 78 81

    100 110 115 121 150 162 170 178 196 215 220 237 268 270 287 316 330 349
    388 465 500 513 546 563 617 680 750 808 822 980

    1k 1.1k 1.18k 1.21k 1.33k 1.47k 1.5k 1.62k 1.78k 1.96k 2.16k 2.2k 2.37k
    2.61k 2.72k 3k 3.16k 3.3k 3.47k 3.82k 4.64k 5k 5.53k 6.8k 6.84k 8k 8.3k
    9.09k

    10k 11.8k 12.1k 13.3k 15k 16.2k 17.8k 18k 19.5k 20k 22k 26.2k 33k 39k
    42.4k 46k 51k 55k 67k 75k 82k

    100k 120k 147k 162k 170k 180k 220k 263k 330k 390k 422k 460k 464k 560k
    674k 820k

    1M 1.2M 1.5M 1.7M 1.9M 2.2M 2.4M 2.6M 2.8M 3.2M 4M 4.8M 5.6M 6M 8.7M
    10M 16M 23.5M
    ''')
    # The following array is used to define what decades of E-series
    # resistors are included.
    powers_of_10 = (-1, 0, 1, 2, 3, 4, 5, 6, 7)
    # EIA recommended resistor values.  From
    # http://www.radio-electronics.com/info/data/resistor/resistor_standard_values.php
    EIA = {
        6: (1.0, 1.5, 2.2, 3.3, 4.7, 6.8),
        12: (1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2),
        24: (1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
            3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1),
        48: (1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54,
            1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49,
            2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65, 3.83, 4.02,
            4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49,
            6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53),
        96: (1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24,
            1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58,
            1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00,
            2.05, 2.10, 2.16, 2.21, 2.36, 2.32, 2.37, 2.43, 2.49, 2.55,
            2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24,
            3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12,
            4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.91, 5.11, 5.23,
            5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65,
            6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45,
            8.66, 8.87, 9.09, 9.31, 9.59, 9.76),
    }

    # These are the SI prefixes likely to be used
    prefixes = {
        "n": -9,
        "u": -6,
        "m": -3,
        "k": 3,
        "M": 6,
        "G": 9,
        "T": 12,
    }
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    pmin = "%.1g" % (10**min(powers_of_10))
    pmax = "%.1g" % (10**(max(powers_of_10) + 1))
    num_entries = d["-n"]
    digits = d["-d"]
    print(dedent(f'''
    Usage:  {name} [options] action [parameters]
    
    Actions:
      bcd
          Using available resistors, produce resistances of values 1, 2, 4, and
          8 in each decade.  This allows you to build a resistance box from BCD
          type switches.
      D[ivider] R1 R2 R3 ...
          Prints out the total resistance and divider ratios of a string of
          resistors used as e.g. a front-end to a voltmeter.
      d[ivider] ratio
          Finds the pairs of resistors that yield the given ratio within the
          desired tolerance (defaults to 1%; use -t to change).
      dd[ivider] total_resistance ratio1 ratio2 [ratio3...]
          Designs a voltage divider that has the indicated total resistance in
          ohms and n ratios.  You'll get a list of n+1 resistors that will make
          the divider.
      r[esistor] resistance
          Finds pairs of resistors that will yield the desired resistance by
          using the pairs in series or parallel.  The default search tolerance
          is 1%; use the -t option to change.
      R[esistor] resistance
          Finds a set of resistors that sums to as close as possible to the
          desired resistance value.  You'd then connect these in series.
      q[uotient] ratio
          Finds pairs of resistors that have the given ratio.
      l[ist]
          List on-hand and EIA resistor values.
      p[airs] file target {{s|p}}
          For the (probably measured) resistance values in file, one value per
          line and a line separating the two groups, calculate the combinations
          of either serial (s) or parallel (p) resistance values.  The output
          will be presented as a % deviation from the target value for all the
          combinations.
    Options:
      -c f   Specifies a set of on-hand resistors to use instead of the
             internally defined ones.  The file f consists of
             whitespace-separated values of the forms 22.3, 22.3k, 22.3M,
             or 22.3G.  You can use the usual floating point exponential
             notation instead such as 22.3e0, 22.3e3, etc.
      -d n   Specify n significant digits in the output [{digits}]
      -e n   Specify EIA series to use (n from 6, 12, 24, 48, 96)
      -n n   Limit output to n entries [{num_entries}]
      -p     Only show parallel combinations.
      -r t:p (For voltage divider calculations only) Specifies the total
             resistance t of the divider and the tolerance percentage p on
             this value.  Only resistor pairs that have this total
             resistance within the specified tolerance will be printed.
      -s     Only show series combinations
      -t p   Changes the % tolerance p for searching.  For the voltage divider
             search, gives the ratio tolerance.  For the resistor pair
             search, the total resistances within the tolerance of the
             desired value will be printed.
    Color code:
        0   Black       3   Orange      6   Blue        9   White
        1   Brown       4   Yellow      7   Violet      Gold 0.1
        2   Red         5   Green       8   Gray        Silver 0.01
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-c"] = None      # Configuration file
    d["-d"] = 4         # Significant figures
    d["-e"] = None      # Which EIA series to use
    d["-n"] = 30        # How many to show if get lots from search
    d["-p"] = False     # Only show parallel
    d["-r"] = None      # Specify total divider resistance
    d["-s"] = False     # Only show series
    d["-t"] = 0.01      # Tolerance
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "c:d:e:n:pr:st:")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-c":
            d["-c"] = opt[1]
        if opt[0] == "-d":
            d["-d"] = int(opt[1])
            if d["-d"] < 1 or d["-d"] > 15:
                print("Bad argument for -d option")
                exit(1)
        if opt[0] == "-e":
            d["-e"] = int(opt[1])
            if d["-e"] not in (6, 12, 24, 48, 96):
                Error("-e option's value must be 6, 12, 24, 48, or 96")
        if opt[0] == "-n":
            try:
                d["-n"] = int(opt[1])
                if d["-n"] < 1:
                    raise Exception()
            except Exception:
                Error("-n option must be integer > 0")
        if opt[0] == "-p":
            d["-p"] = True
        if opt[0] == "-r":
            s = opt[1]
            if ":" in s:
                f = s.split(":")
                if len(f) != 2:
                    Error("Bad form for option -r")
                # d["-r"] is (total_resistance, tolerance)
                d["-r"] = (float(f[0]), float(f[1])/100)
                if d["-r"][1] <= 0:
                    Error("-r:  percent tolerance must be > 0")
            else:
                Error("-r option must contain a ':' character")
        if opt[0] == "-s":
            d["-s"] = True
        if opt[0] == "-t":
            d["-t"] = float(opt[1])/100
            if d["-t"] <= 0:
                Error("-t:  percent tolerance must be > 0")
    if not args:
        Usage(d)
    if args[0][:2] == "dd":
        cmd = "dd"
    else:
        cmd = args[0][0]
    if cmd not in ("b", "d", "D", "dd", "l", "p", "q", "r", "R"):
        Error("Command '%s' not recognized" % args[0])
    if cmd in ("d", "q", "r", "R"):
        if len(args) != 2:
            Usage(d)
    elif cmd in ("dd",):
        if len(args) < 3:
            Usage(d)
    elif cmd in ("l",):
        if len(args) != 1:
            Usage(d)
    args[0] = cmd
    return args
def ConvertString(s):
    '''s will be a number possibly followed by an SI prefix.  Return it as
    a float.
    '''
    msg = f"'{s}' is an unrecognized resistance value"
    f = ParseUnit(s)
    factor = 1
    if not f:
        Error(msg)
    m, unit = f
    if unit:
        if unit not in SI_prefixes:
            Error(msg)
        factor = float(SI_prefixes[unit])
    try:
        return float(m)*factor
    except Exception:
        Error(msg)
def GetResistors(d):
    R, p = [], {"m": 1e-3, "k": 1e3, "M": 1e6, "G": 1e9, "T": 1e12}
    if d["-e"] is not None:
        # Use EIA resistors
        for p in powers_of_10:
            for i in EIA[d["-e"]]:
                R.append(i*10**p)
    else:
        # Use on-hand resistors
        if d["-c"] is not None:
            global on_hand
            on_hand = open(d["-c"]).read()
        for line in on_hand.split("\n"):
            line = line.strip()
            if not line or line[0] == "#":
                continue
            for i in line.split():
                R.append(ConvertString(i))
    d["R"] = R
def Div(d, ratio, R1, R2):
    '''If the divider ratio of R1 and R2 (R1 on top) is within the desired
    tolerance of ratio, then include it in the set d["divider"].
    '''
    s, t = R1 + R2, d["-t"]
    if d["-r"] is not None:
        R, Rt = d["-r"]
        if not ((1 - Rt)*R <= s <= (1 + Rt)*R):
            return
    rat1, rat2 = R1/s, R2/s
    if (1 - t)*ratio <= rat1 <= (1 + t)*ratio:
        d["divider"].add((rat1, R1, R2))
    elif (1 - t)*ratio <= rat2 <= (1 + t)*ratio:
        d["divider"].add((rat2, R2, R1))
def Divider(d, ratio):
    d["divider"] = set()
    # First check using equal resistors
    for R in d["R"]:
        Div(d, float(ratio), R, R)
    for R1, R2 in combinations(d["R"], 2):
        Div(d, float(ratio), R1, R2)
    # Print report
    div = list(d["divider"])
    if not div:
        print("No divider can be made")
        return
    div.sort()
    print("Voltage divider with ratio = ", ratio, ", tolerance = ",
          sig(d["-t"]*100, 2), "%", sep="")
    print()
    print("% dev from")
    print("desired ratio       R1           R2      Total Res.")
    print("-------------   ----------   ----------  ----------")
    for rat, r1, r2 in div:
        dev = 100*((rat - float(ratio))/float(ratio))
        pct = sig(dev)
        if dev >= 0:
            pct = " " + pct
        R1, R2, R = fp.engsi(r1), fp.engsi(r2), fp.engsi(r1 + r2)
        if not dev:
            fg(highlight)
        print("   {0:10}   {1:^10}   {2:^10}   {3:^10}".format(pct, R1, R2, R))
        normal()
def Resistance(d, resistance, report=False):
    '''Print the report of the choices to get the desired resistance if
    report is True.  If report is False, return 
    '''
    d["resistances"] = set()
    # First see if we have an exact match
    if resistance in d["R"]:
        d["resistances"].add((resistance, "e", resistance, 0))
    else:
        # First check using equal resistors
        for R in d["R"]:
            Res(d, resistance, R, R)
        for R1, R2 in combinations(d["R"], 2):
            Res(d, resistance, R1, R2)
    res = list(d["resistances"])
    if not res:
        if report:
            print("No resistor combinations that meet tolerance")
            return
        else:
            return []
    # Check if we have too many entries; if so, whittle down the list to
    # the closest N.
    clipped = False
    if len(res) > d["-n"]:
        # Sort by absolute value of tolerance
        def tol(tgt, val):
            return abs(val - tgt)/val
        r = [(tol(resistance, i[0]), i) for i in res]   # Decorate with abs val
        r.sort()
        res = [i[1] for i in r[:d["-n"]]]
        clipped = True
    if report:
        # Print report
        res.sort()
        print("Desired resistance = ", d["desired"], " = ", sig(d["res"]) +
              ", tolerance = ", sig(d["-t"]*100, 2), "%", sep="")
        if clipped:
            print("Closest %d matches shown" % d["-n"])
        print()
        print("% dev from")
        print("desired res.        R1           R2      Connection")
        print("-------------   ----------   ----------  ----------")
        for val, c, r1, r2 in res:
            dev = 100*((val - resistance)/resistance)
            pct = sig(dev, 2)
            if dev >= 0:
                pct = " " + pct
            R1, R2 = fp.engsi(r1), fp.engsi(r2)
            conn = {"s": "series", "p": "parallel", "e": "exact"}[c]
            if (d["-p"] and c == "s") or (d["-s"] and c == "p"):
                continue
            if not dev:
                fg(highlight)
            if c == "e":
                print("   {0:10}   {1:^10}                {2}".format(pct,
                      R1, conn))
            else:
                print("   {0:10}   {1:^10}   {2:^10}   {3}".format(pct,
                      R1, R2, conn))
            normal()
    else:
        return res
def Res(d, R, R1, R2):
    '''See if R1 and R2 sum to R within the desired tolerance; if so,
    include it in the set d["resistances"].
    '''
    t = d["-t"]
    ser = R1 + R2
    if (1 - t)*R <= ser <= (1 + t)*R:
        d["resistances"].add((ser, "s", R1, R2))
    par = 1/(1/R1 + 1/R2)
    if (1 - t)*R <= par <= (1 + t)*R:
        d["resistances"].add((par, "p", R1, R2))
def Quotient(d, ratio):
    if ratio == 1:
        print("Quotient cannot be 1")
        exit(1)
    d["resistances"], t, Ratio = set(), d["-t"], float(ratio)
    for R1, R2 in combinations(d["R"], 2):
        q1 = R1/R2
        q2 = 1/q1
        if (1 - t)*Ratio <= q1 <= (1 + t)*Ratio:
            d["resistances"].add((q1, R1, R2))
        elif (1 - t)*Ratio <= q2 <= (1 + t)*Ratio:
            d["resistances"].add((q2, R2, R1))
    # Print report
    res = list(d["resistances"])
    if not res:
        print("No resistor combinations that meet tolerance")
        return
    res.sort()
    print("Desired ratio = ", ratio, ", tolerance = ",
          sig(d["-t"]*100, 2), "%", sep="")
    print()
    print("% dev from")
    print("desired ratio       R1           R2")
    print("-------------   ----------   ----------")
    for val, r1, r2 in res:
        dev = 100*((val - Ratio)/Ratio)
        pct = sig(dev, 2)
        if dev >= 0:
            pct = " " + pct
        R1, R2 = fp.engsi(r1), fp.engsi(r2)
        if not dev:
            fg(highlight)
        print("   {0:10}   {1:^10}   {2:^10}".format(pct, R1, R2))
        normal()
def List(d):
    # EIA
    print("EIA resistance series:")
    sig.rtz = True
    for n in (6, 12, 24, 48, 96):
        print("E%d:" % n)
        digits = 2 if n < 48 else 3
        s = []
        for num in EIA[n]:
            s.append(sig(num, digits))
        for i in Columnize(s, horiz=True):
            print(" ", i)
    if 0:
        print(dedent(f'''
        Allen-Bradley 1.6 kW pot:
          Resistance:  0.35 to 17.5 ohms
          Current:  250 A max
          At line voltages:  120 VAC ==> 6.8 to 250 A, 240 VAC ==> 13.7 to 250 A
          10 A at 120 V requires 12 ohms, 15 A requires 8 ohms'''))
    print("-"*70)
    print(C.lmag, end="")
    print("On-hand resistors:")
    print(on_hand)
    print(C.norm, end="")
def Pairs(args, d):
    if len(args) != 4:
        Usage(d)
    parallel = True if args[3] == "p" else False
    target_value = float(args[2])
    if target_value <= 0:
        Error("Target value must be > 0")
    # Read file data
    lines = [i.strip() for i in open(args[1]).readlines()]
    # Check that we have only one blank line and an equal number of
    # resistance values on either side of it.
    r1, r2, first = [], [], True
    for line in lines:
        if not line:
            first = False
            continue
        if first:
            r1.append(float(line))
        else:
            r2.append(float(line))
    if not r1 or not r2:
        Error("Missing blank line in resistor file '%s'" % args[1])
    if len(r1) != len(r2):
        Error("Two resistor sets don't have equal number in resistor file '%s'"
              % args[1])
    # Calculate the set of resultant resistances
    results = []
    for i in r1:
        for j in r2:
            if parallel:
                r = 1/(1/i + 1/j)
            else:
                r = i + j
            pct_dev = 100*(r - target_value)/target_value
            pct_dev = 0 if abs(pct_dev) < 1e-10 else pct_dev
            results.append([pct_dev, r, i, j])
    results.sort()
    model, file = "parallel" if parallel else "series", args[1]
    print(dedent(f'''
    Model = {model}
    File  = {file}
    
    % dev from
    mean value      Resistance          R1               R2
    ----------      ----------      -------------   -------------
    '''))
    sig.digits = d["-d"]
    for i in results:
        r, r1, r2 = i[1:]
        print("%9s%%      " % sig(i[0], 2), nl=False)
        print("%-10s      " % sig(r), nl=False)
        print("%-10s      " % sig(r1), nl=False)
        print("%-10s" % sig(r2))
def GetValue(args):
    '''Convert a number and optional SI prefix on the command line to a
    floating point equivalent.  Note the string with the optional trailing
    suffix removed can be an expression.
    '''
    s, factor = ''.join(args).replace(" ", ""), 1
    if s[-1] in prefixes:
        factor = 10**prefixes[s[-1]]
        s = s[:-1]
    try:
        return float(eval(s))*factor
    except Exception:
        print("'%s' isn't recognized as a resistance value" % ' '.join(args))
        exit(1)
def Series(d, res):
    '''Find a set of resistors that sum to the desired value but remain
    less than or equal to it.
    '''
    resistors = d["R"]
    resistors.sort()
    resistors = list(reversed(resistors))
    used = []
    while resistors and sum(used) <= res:
        if resistors[0] + sum(used) <= res:
            used.append(resistors[0])
        else:
            del resistors[0]
    print("Sum =", fp.engsi(sum(used)))
    print("  Resistor     % of total")
    r = 0
    for i in used:
        r += i
        print("  %-10s" % fp.engsi(i), " ", sig(100*r/res, 6))
def Interpret(s):
    '''Given a string such as '10k', convert it to a floating point value
    in ohms.  Note that the string with the suffix removed can be a valid
    python expression.
    '''
    factor = 1
    s = s.strip()
    if s[-1] in prefixes:
        factor = 10**prefixes[s[-1]]
        s = s[:-1]
    return float(eval(s))*factor
def DividerRatios(d, res):
    r = [Interpret(i) for i in res]
    R = sum(r)
    print("String of voltage dividers:")
    print("  Resistors given:")
    for i in res:
        print("    ", i)
    print("  Total resistance =", fp.engsi(R))
    print("  Divider ratios:")
    for i in range(1, len(r)):
        D = sum(r[i:])/R
        print("  %2d  " % i, sig(D, 4))
def DDivider(args, d):
    '''The arguments are:
        total_resistance_ohms ratio1 ratio2 ...
                              -----------------
                                    n ratios
    Return the n+1 resistors that make up this divider.
 
    The equations are

        R_n = R*rho_{n-1}
        R_i = R*(rho_{i-1} - rho_i), i = 2, 3, ..., n-1
        R_1 = R*(1 - rho_1)

    Note that it's easier to augment the array of ratios with 0 at the
    beginning and 1 at the end; then we can use the indexed formula

        R_i = R*(rho_{i-1} - rho_i), i = 1, 2, 3, ..., n

    to get the n resistances.
    '''
    R = Interpret(args[1])
    if R <= 0:
        Error("Total resistance must be > 0")
    try:
        rho = [float(i) for i in args[2:]]
    except Exception:
        Error("Couldn't get ratios:\n  '%s'" % str(args[1:]))
    if len(rho) < 2:
        Error("Need at least two ratios")
    if min(rho) <= 0:
        Error("Ratios must all be > 0")
    if max(rho) >= 1:
        Error("Ratios must all be < 1")
    rho.sort()
    rho = list(reversed(rho))
    rho = [1] + rho + [0]   # Augment for indexing ease
    n = len(rho)
    print("Resistors                   Ratio")
    print("--------------------        ----------")
    for i in range(1, n):
        Rx = R*(rho[i-1] - rho[i])
        if i == n - 1:
            print("  R%d = %-20s" % (i, fp.engsi(Rx)))
        else:
            print("  R%d = %-20s %s" % (i, fp.engsi(Rx), rho[i]))
    print("Total resistance =", fp.engsi(R))
def sdev(r1, r2):
    '''Return the standard deviation of the two values.
    '''
    mean = (r1 + r2)/2
    return (r1 - mean)**2 + (r2 - mean)**2
def Best(R, res):
    '''Return the best selection of resistor R from the list res.
    '''
    # Get exact matches
    exact = []
    for r in res:
        if r[0] == R:
            exact.append(r)
    if exact:
        # Use the match where the two resistors are closest
        closest = []
        for i in exact:
            closest.append([sdev(i[2], i[3]), i])
        closest = sorted(closest)
        return closest[0][1]
    else:
        # Use the match with the lowest deviation
        lowest = (1e308,)
        for r in res:
            if r[0] < lowest[0]:
                lowest = r
        match = lowest
    return match
def Int(x):
    return int(x) if x == int(x) else x
def BCD(args, d):
    '''Print the series/parallel combinations of on-hand resistors to
    construct the needed 1, 2, 4, 8 values in each decade.  This allows
    construction of a resistance box from suitable BCD (binary-coded
    decimal) switches.
 
    Note that the typical BCD switch connects the common to the appropriate
    1-2-4-8 terminal and there's no easy way to make a resistance box from
    such a thing, although a capacitor box is possible.
    '''
    onhand = d["R"]
    rmin, rmax = min(onhand), max(onhand)
    from pprint import pprint as pp
    for decade in range(0, 7):
        for r in (1, 2, 4, 8):
            R = r*10**decade
            print("{:10d}:".format(R), end="  ")
            if R in onhand:
                fg(lgreen)
                print("Exact")
                normal()
            else:
                res = Resistance(d, R, report=False)
                if res:
                    choice = Best(R, res)
                    p = "+" if choice[1] == "s" else "||"
                    r1, r2 = Int(choice[2]), Int(choice[3])
                    pct = (choice[0] - R)/R*100
                    pct = "[{}%]".format(sig(pct, 2)) if pct else ""
                    print(r1, p, r2, pct)
                else:
                    fg(lred)
                    print("No match")
                    normal()
    exit(0)
if __name__ == "__main__":
    d = {}   # Options dictionary
    args = ParseCommandLine(d)
    sig.digits = d["-d"]
    GetResistors(d)
    if args[0] == "b":
        BCD(args, d)
    elif args[0] == "dd":
        DDivider(args, d)
    elif args[0] == "d":
        ratio = args[1]
        if float(ratio) <= 0:
            Error("Divider ratio must be > 0")
        Divider(d, ratio)
    elif args[0] == "D":
        res = args[1:]
        if len(res) < 2:
            Error("Need at least two resistances")
        DividerRatios(d, res)
    elif args[0] == "l":
        List(d)
    elif args[0] == "p":
        Pairs(args, d)
    elif args[0] == "q":
        ratio = args[1]
        if float(ratio) <= 0:
            Error("Quotient ratio must be > 0")
        Quotient(d, ratio)
    elif args[0] == "R":
        d["desired"] = ' '.join(args[1:])
        res = d["res"] = GetValue(args[1:])
        if res <= 0:
            Error("Desired resistance must be > 0")
        Series(d, res)
    elif args[0] == "r":
        d["desired"] = ' '.join(args[1:])
        res = d["res"] = GetValue(args[1:])
        if res <= 0:
            Error("Desired resistance must be > 0")
        Resistance(d, res, report=True)
# vim: wm=5
