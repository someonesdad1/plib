"""

ToDo
    - Operators
        - d h:  Calculate number of holes to move with h hole plate to get
          d degrees of rotation
        - t h:  Print a table of all the numbers of divisions that can be
          gotten with dividing plates with holes from 1 to h.
        - m d:  Print how to get d divisions with the Master dividing head
          and which h to use on the plate.
        - h h:  Number of divisions that can be gotten with a plate with h
          holes.

Calculate characteristics of a dividing head

See PIM Feb 1991, "The Mathematics of a Dividing Head", pg 17

The fundamental characteristics of the dividing head are
    R       Gear ratio, number of turns required to make output shaft
            rotate once.
    H       Number of equally-spaced holes in dividing plate.

If you want N divisions on something, then you'll need to make R/N turns of
the worm gear shaft to get 1/N of a circle of movement.  Here, assume R and
N are both integers.

    Example:  suppose R = 40 and we want N = 24 divisions.  Then 1/24th of
    a revolution is gotten by a turn of 40/24 or 1-16/24 of a turn.  This
    is the fraction 1-2/3 in lowest terms.  We can perform this operation
    if we have a dividing plate with 3 equally-spaced holes in it - or any
    number of holes that's a multiple of 3..

The number of holes needed for N turns is thus Fraction(R % N, N).denominator.

This lets us construct a table of N versus number of holes in a plate for a
given ratio R.



---------------------------------------------------------------------------
Relatively common divisions needed

2 4 8   Square, octagon
5       Pentagon
6       Hexagon
---------------------------------------------------------------------------

B&S dividing heads came with three plates:
    1:  15 16 17 18 19 20
    2:  21 23 27 29 31 33
    3:  37 39 41 43 47 49

Assuming a 40:1 gear ratio, these give the divisions

15: 75 150
16: 128
17: 17 34 68 85 136 170
18: 144
19: 19 38 76 95 152 190
20: 2
21: 21 42 84 105 168
23: 23 46 92 115 184
27: 27 54 108 135
29: 29 58 116 145
31: 31 62 124 155
33: 33 66 132 165
37: 37 74 148 185
39: 39 78 156 195
41: 41 82 164
43: 43 86 172
47: 47 94 188
49: 49 98 196

"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Calculate characteristics of a dividing head
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import defaultdict, deque
        from fraction import Fraction
        import getopt
        import os
        from pprint import pprint as pp
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from f import flt
        from wrap import wrap, dedent
        from color import t
        from columnize import Columnize
        from primes import IsPrime, AllFactors
    if 1:  # Global variables
        W = int(os.environ.get("COLUMNS", "80")) - 1
        dbg = True
        dbg = False
if 1:  # Manpage

    def Manpage():
        print(
            dedent(f"""

        A dividing head is a spindle that is rotated by a worm gear and
        worm wheel.  A handle turns the worm gear and a dividing plate with
        equally-spaced holes is rigidly attached to the worm gear.  The
        worm gear takes R full turns to rotate the spindle once and the
        plate has H holes in it.

        With H holes, the circle is divided up into R*H divisions.  This
        setup lets you evenly divide something into X divisions where
        X is any integer factor of R*H.

        Example:  with a 40:1 worm gear ratio and a plate with 16 holes,
        we get 40*16 = 640 divisions.  The smallest movement of the spindle is 
        1/640 or 0.001563 of a rotation or 0.5625°.  The factors of 640 are

            2 4 5 8 10 16 20 32 40 64 80 128 160 320

        and it's clear that we can get any of these divisions by 

        holes on the worm gear allows an integer number of rotations by
        using an indexing pin in the plate.  The usual operation is to
        accurately rotate the spindle by a known angle.  See [1].

        Suppose the worm gear ratio is R and the number of evenly-spaced
        holes in the dividing plate is H.  Both R and H are assumed to be
        integers > 0.  For example, a common worm ratio is 40, which means
        the worm gear must revolve 40 times to cause the worm wheel to
        rotate once.

        Suppose we have a specific ratio R and number of holes in the
        dividing plate H.  The plate allows a minimum worm gear rotation of
        1/H of a full rotation and the gear reduction means this results in
        a rotation of 1/(H*R) of a circle.  Thus, H holes with the
        reduction of R means the circle is divided into H*R locations
        around a circle.

        The behavior is gotten with fractional arithmetic. 


        References:
            [1] https://en.wikipedia.org/wiki/Indexing_head
            [2] Projects in Metal, Feb 1991, "The Mathematics of a Dividing
                Head", pg 17.

        """)
        )
        exit(0)


if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] operator operator_arguments
          d   N [h]
            Construct table showing number of holes to get divisions 
            from 2 to N.  If h is given, limit holes to h.
          m
            Show details on Master dividing head.
          a h
            Show angle data for number of holes from 2 to h.
        Options:
            -h      Print a manpage
            -m      Print characteristics of Master dividing head
            -r R    Set worm gear ratio [{d["-r"]}]
            -t      Show table of divisions wanted and holes needed
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-d"] = 4  # Number of significant digits
        d["-r"] = 40  # Default worm gear ratio
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hr:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
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
        if not dbg and not args:
            Usage()
        x = flt(0)
        x.N = d["-d"]
        x.rtz = True
        return list(args)


if 1:  # Master dividing head

    def MasterDividingHead():
        """Print out the division capabilities of the Master dividing head.

        This is a smaller Master dividing head for lathes that belonged
        to HPR.  It has an expanding collet to fit a spindle tube and,
        once secured to the lathe, can divide spindle rotation into desired
        numbers.

        The worm gear is 40:1 and the dividing plate has 21, 23, 27, 29,
        31, and 33 holes.
        """
        print(
            dedent(f"""
        Master dividing head for lathe (belonged to HPR)
            40:1 worm with 21 23 27 29 31 33 holes in plate

        Number of divisions achievable:
                  1  2   4   5   8  10  20
                 -------------------------
            21:  21 42  84 105 168 210 420
            23:  23 46  92 115 184 230 460
            27:  27 54 108 135 216 270
            29:  29 58 116 145 232 290
            31:  31 62 124 155 248 310
            33:  33 66 132 165 264 330

        This script gives the 
        """)
        )


if 0:  # Core functionality

    def OrganizeResults(results):
        """results is a dict of Nmax for keys and di[n] is the number of holes in a
        dividing plate to get Nmax for the give ratio.  List things by number
        of holes and the values of Nmax that can be gotten with that number of
        holes.
        """
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
        w, s = 4, " " * 4
        cmd = " ".join(sys.argv[1:])
        print(f"Dividing head calculations (args = {cmd!r})")
        print(f"{ratio:{w}d}{s}Worm gear ratio")
        print(f"{Nmax:{w}d}{s}Max divisions to generate")
        if hmax:
            print(f"{hmax:{w}d}{s}Max holes in plates")
        print(f"\nHoles  Divisions")
        o = []
        for i in sorted(mydict):
            s = " ".join(str(j) for j in mydict[i])
            o.append(f"{i:2d}:  {s}")
        for i in Columnize(o):
            print(i)
        # Plates for single prime numbers
        print(f"Plates for single prime numbers:")
        for i in Columnize([str(j) for j in sorted(p)], indent=" " * 4):
            print(i)
        # Plates removed
        if hmax:
            print(f"Plates removed because they were > hmax = {hmax}:")
            for i in Columnize([str(j) for j in sorted(too_many)], indent=" " * 4):
                print(i)
        CoalesceHoles(mydict)

    def CoalesceHoles(mydict):
        """Reduce the set to a minimum number of hole circles needed.

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
        """

    def HoleTable(*args):
        if not args:
            Error("Need N, the maximum number of divisions wanted")
        Nmax = int(args[0])
        ratio = d["-r"]
        # Get the results
        results = {}
        for n in range(2, Nmax + 1):
            if ratio % n:
                results[n] = Fraction(ratio % n, n).denominator
            else:
                results[n] = ratio // n
        # Organize into report
        o, p = [], []
        print("N:h where N is desired divisions and h is number of holes")
        for n in results:
            o.append(f"{n:3d}:{results[n]:3d}")
        for i in Columnize(o, col_width=10):
            print(i)

    def AngleData(*args):
        if not args:
            Error("Need h, the maximum number of holes")
        Hmax = int(args[0])
        ratio = d["-r"]
        print(
            f"Angle steps for number of holes in division plate, worm ratio is {d['-r']}\n"
        )
        print(f"Holes Steps   1000/Steps   °/step")
        print(f"----- -----   ----------   ------")
        for h in range(1, Hmax + 1):
            n = ratio * h
            recip = flt(1000 / n)
            step_deg = 360 * recip / 1000
            s = " ".join(str(i) for i in AllFactors(n))
            print(f"{h:4d} {n:5d}      {recip!s:8s}   {step_deg!s:6s}    {s}")

    def VernierPlates(*args):
        pass


if 1:  # Core functionality

    def Degrees(*args):
        pass

    def Master(*args):
        pass

    def DivisionsWithPlates(*args):
        """If only one argument is present, print out the divisions that
        can be gotten with all plates with holes from 1 to that value.
        Otherwise, just print the divisions for the given plates.
        """
        discrete = False
        try:
            if len(args) > 1:
                discrete = True
                H = [int(i) for i in args]
                if any(i < 1 for i in H):
                    Error("Arguments must be integers > 0")
            else:
                H = range(1, int(args[0]) + 1)
        except ValueError:
            Error("For op == d, the argument must be an integer > 0")
        ratio = d["-r"]
        # Construct dictionary div with key = number of divisions and where the
        # value is the number of holes that let this number of divisions be
        # gotten.
        div = defaultdict(list)
        for h in H:
            for factor in AllFactors(ratio * h):
                div[factor].append(h)
        # Make sure for each item in dict that number of holes is only
        # given once
        for i in div:
            div[i] = list(sorted(set(div[i])))
        # Print report
        print(f"Number of divisions realizable (ratio = {ratio})")
        if discrete:
            print(f"  Holes:  {' '.join(args)}\n")
        print(f"Divisions    Number of holes to use ")
        print(f"---------   ------------------------")
        indent = " " * 12
        for n in sorted(div):
            dq = deque(str(j) for j in div[n])
            line = f"{n:^9d}   "
            o = []
            # Format things to get proper indenting
            while dq:
                item = dq.popleft()
                if len(line + " " + item) >= W:
                    print(line)
                    line = indent + " " + item
                else:
                    line += " " + item
            if line:
                print(line)
        print("\nList of divisions available:")
        o = sorted([f"{i:4d}" for i in div], key=int)
        for i in Columnize(o, indent=" " * 4, col_width=8):
            print(i)


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if dbg:
        op, args = "t", ["50"]
        # Master dividing head's possibilities
        op, args = "t", "21 23 27 29 31 33".split()
    else:
        op = args.pop(0)
    if dbg:
        if op == "t":  # Table of divisions gotten with plates up to h
            DivisionsWithPlates(*args)
        elif op == "h":  # What divisions a plate with h holes can give
            Plate(*args)
        elif op == "d":  # How to get specific degrees of rotation
            Degrees(*args)
        elif op == "m":  # How to get divisions with Master dividing head
            Master(*args)
        else:
            Error(f"{op!r} not recognized")
    else:
        if op == "d":
            HoleTable(*args)
        elif op == "m":
            MasterDividingHead()
        elif op == "a":
            AngleData(*args)
        elif op == "a":
            VernierPlates(*args)
        else:
            Error(f"{op!r} not recognized")
