'''
Calculate characteristics of a dividing head

See PIM Feb 1991, "The Mathematics of a Dividing Head", pg 17

The fundamental characteristic of the dividing head is the gear ratio R.
If you want N divisions, then you'll need to make R/N turns of the worm
gear shaft to get 1/N of a circle of movement.  Here, assume R and N are
both integers.

    Example:  suppose R = 40 and we want N = 24 divisions.  Then 1/24th of
    a revolution is gotten by a turn of 40/24 or 1-16/24 of a turn.  This
    is the fraction 1-2/3 in lowest terms.  We can perform this operation
    if we have a dividing plate with 3 equally-spaced holes in it.

The number of holes needed for N turns is thus Fraction(R % N, N).denominator.

This lets us construct a table of N versus number of holes in a plate for a
given ratio R.

'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
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
    if 1:   # Standard imports
        from collections import defaultdict
        from fraction import Fraction
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from columnize import Columnize
        from primes import IsPrime
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] Nmax [hmax]
          For a dividing head with a ratio R, construct a table showing the
          number of holes needed to get all the divisions from 2 to Nmax.
          hmax is the maximum number of holes allowed in a plate.  If you
          provide hmax, some divisions will not be possible.  R, N, and
          hmax must be integers.
        Options:
            -h      Print a manpage
            -r R    Set ratio [{d['-r']}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Describe this option
        d["-d"] = 3         # Number of significant digits
        d["-r"] = 40        # Default ratio
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:hr:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = f"{o} option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
            elif o == "-r":
                try:
                    d[o] = int(a)
                    if not (d[o] >= 2):
                        raise ValueError()
                except ValueError:
                    msg = f"{o} option's argument must be an integer > 1"
                    Error(msg)
        if len(args) not in (1, 2):
            Usage(status=1)
        return args
if 1:   # Core functionality
    def OrganizeResults(results):
        '''results is a dict of Nmax for keys and di[n] is the number of holes in a
        dividing plate to get Nmax for the give ratio.  List things by number
        of holes and the values of Nmax that can be gotten with that number of
        holes.
        '''
        mydict = defaultdict(list)
        for n in results:
            holes = results[n]
            mydict[holes].append(n)
        # Find the mydict entries that are prime numbers and only have one
        # entry, that of their number.
        p = []
        for n in mydict:
            if n == 1:
                continue
            if IsPrime(n) and len(mydict[n]) == 1:
                p.append(n)
        # Remove these from the dict
        for n in p:
            del mydict[n]
        # If hmax is given, remove numbers > hmax
        too_many, o = [], []
        if hmax:
            o = set(range(hmax + 1, Nmax))
            for n in o:
                if n in mydict:
                    del mydict[n]
                    too_many.append(n)
        # Print report
        w, s = 4, " "*4
        cmd = ' '.join(sys.argv[1:])
        print(f"Dividing head calculations (args = {cmd!r})")
        print(f"{ratio:{w}d}{s}Worm gear ratio")
        print(f"{Nmax:{w}d}{s}Max divisions to generate")
        if hmax:
            print(f"{hmax:{w}d}{s}Max holes in plates")
        print(f"\nHoles  Divisions")
        o = []
        for i in sorted(mydict):
            s = ' '.join(str(j) for j in mydict[i])
            o.append(f"{i:2d}:  {s}")
        for i in Columnize(o):
            print(i)
        # Plates for single prime numbers
        print(f"Plates for single prime numbers:")
        for i in Columnize([str(j) for j in sorted(p)], indent=" "*4):
            print(i)
        # Plates removed
        if hmax:
            print(f"Plates removed because they were > hmax = {hmax}:")
            for i in Columnize([str(j) for j in sorted(too_many)], indent=" "*4):
                print(i)
        CoalesceHoles(mydict)
    def CoalesceHoles(mydict):
        '''Reduce the set to a minimum number of hole circles needed.

        Here's the results for arguments of 100 50:

            Dividing head calculations
              40    Worm gear ratio
             100    Max divisions to generate
              50    Max holes in plates
            
            Holes  Divisions
             1:  40                   11:  11 22 44 55 88       29:  29 58
             2:  16 20 80             12:  96                   31:  31 62
             3:  3 6 12 15 24 30 60   13:  13 26 52 65          33:  33 66
             4:  10 32                15:  75                   37:  37 74
             5:  8 25 50 100          17:  17 34 68 85          39:  39 78
             6:  48                   19:  19 38 76 95          41:  41 82
             7:  7 14 28 35 56 70     20:  2                    43:  43 86
             8:  5 64                 21:  21 42 84             47:  47 94
             9:  9 18 36 45 72 90     23:  23 46 92             49:  49 98
            10:  4                    27:  27 54
            Plates for single prime numbers:
                53 59 61 67 71 73 79 83 89 97
            Plates removed because they were > hmax:
                51 57 63 69 77 81 87 91 93 99

        Here's how this would be analyzed.  Integer factors:
            10: 2 5
            12: 2 2 3
            14: 2 7
            15: 3 5
            16: 2 2 2 2
            18: 2 3 3
            20: 2 2 5
            21: 3 7
            22: 2 11
            24: 2 2 2 3
            25: 5 5
            26: 2 13
            27: 3 3 3
            28: 2 2 7
            30: 2 3 5
            32: 2 2 2 2 2
            33: 3 11
            34: 2 17
            35: 5 7
            36: 2 2 3 3
            38: 2 19
            39: 3 13
            40: 2 2 2 5
            42: 2 3 7
            44: 2 2 11
            45: 3 3 5
            46: 2 23
            48: 2 2 2 2 3
            49: 7 7
            50: 2 5 5

        First get the even number of holes:
            2 4 6 8 10 12 20 
        The factors are
            2: 2
            4: 2 2
            6: 2 3
            8: 2 2 2
            10: 2 5
            12: 2 2 3
            20: 2 2 5
        
        The factors in the list are 2, 3, 5
        '''

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    ratio = d["-r"]
    Nmax = int(args[0])
    hmax = None if len(args) == 1 else int(args[1])
    results = {}
    for n in range(2, Nmax + 1):
        if ratio % n:
            results[n] = Fraction(ratio % n, n).denominator
        else:
            results[n] = ratio // n
    if 1:
        OrganizeResults(results)
    else:
        o, p = [], []
        print("N:h where N is desired divisions and h is number of holes")
        for n in results:
            o.append(f"{n:3d}:{results[n]:3d}")
        for i in Columnize(o, col_width=10):
            print(i)
