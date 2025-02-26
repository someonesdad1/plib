"""
Prints combinations of gauge blocks that will sum to a desired size

    This is a brute-force solution of the subset sum problem.

    26 Dec 2014:  I checked my 'user' gauge block set's blocks that were 1 inch and under with a
    Starrett #216 micrometer that I got new in July of 1980.  Here are the deviations in 0.0001
    inch units from the nominal size:
        5/64    +2
        0.1004  +1
        0.1006  +1
        0.1008  +1
        0.104   +1
        0.107   +1
        0.108   +1
        0.112   +1
        0.116   -1
        0.117   -1
        0.118   -1
        0.119   +1
        0.121   +1
        0.126   -1
        0.131   -1
        0.140   -1
        0.145   -1
        0.147   -1
        0.350   -2
        0.450   -1
        0.550   -1
        0.800   -2
        0.850   +1
        0.900   -3
        0.950   -2
        1.000   -1
    These measurements are more likely to be the micrometer's inaccuracy rather than the gauge
    blocks' inaccuracies.  But they do give a measure of confidence in the consistency of the gauge
    blocks.
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2012 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Find gauge blocks to make a dimension
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import sys
        import getopt
        from itertools import combinations
        from math import *
    if 1:  # Custom imports
        from lwtest import Assert
        from wrap import dedent
        from f import flt
        from color import t
        from columnize import Columnize
        from gauge_sizes import gauges
        from u import u, ParseUnit
    if 1:  # Global variables
        # The following dictionary holds the gauge block sets.  You can add or delete sets as you
        # see fit.  The structure should be apparent if you want to add a new set.  Note the values
        # are integers; this helps make the summing of sizes fast and exact because there is no
        # roundoff error.
        gauge_block_sets = {
            # Value is (units, resolution, block_sizes_sequence)
            "user": (
                "inch",
                "0.0001",
                (  # 64 blocks
                    # This gauge block set is a used Starrett set I bought in 2005 and had
                    # some missing blocks.
                    250,
                    350,
                    490,
                    500,
                    1000,
                    1003,
                    1004,
                    1005,
                    1006,
                    1007,
                    1008,
                    1009,
                    1040,
                    1050,
                    1060,
                    1070,
                    1080,
                    1090,
                    1110,
                    1120,
                    1140,
                    1160,
                    1170,
                    1180,
                    1190,
                    1210,
                    1220,
                    1230,
                    1250,
                    1260,
                    1270,
                    1290,
                    1300,
                    1310,
                    1320,
                    1330,
                    1340,
                    1350,
                    1370,
                    1380,
                    1390,
                    1400,
                    1420,
                    1430,
                    1440,
                    1450,
                    1460,
                    1470,
                    1500,
                    2500,
                    3500,
                    4500,
                    5500,
                    6000,
                    6500,
                    7000,
                    7500,
                    8000,
                    8500,
                    9000,
                    9500,
                    20000,
                    30000,
                    40000,
                ),
            ),
            "metric": (
                "mm  ",
                "0.001",
                (  # 86 blocks
                    1001,
                    1002,
                    1003,
                    1004,
                    1005,
                    1006,
                    1007,
                    1008,
                    1009,
                    1010,
                    1020,
                    1030,
                    1040,
                    1050,
                    1060,
                    1070,
                    1080,
                    1090,
                    1100,
                    1110,
                    1120,
                    1130,
                    1140,
                    1150,
                    1160,
                    1170,
                    1180,
                    1190,
                    1200,
                    1210,
                    1220,
                    1230,
                    1240,
                    1250,
                    1260,
                    1270,
                    1280,
                    1290,
                    1300,
                    1310,
                    1320,
                    1330,
                    1340,
                    1350,
                    1360,
                    1370,
                    1380,
                    1390,
                    1400,
                    1410,
                    1420,
                    1430,
                    1440,
                    1450,
                    1460,
                    1470,
                    1480,
                    1490,
                    1000,
                    1500,
                    2000,
                    2500,
                    3000,
                    3500,
                    4000,
                    4500,
                    5000,
                    5500,
                    6000,
                    6500,
                    7000,
                    7500,
                    8000,
                    8500,
                    9000,
                    9500,
                    10000,
                    20000,
                    30000,
                    40000,
                    50000,
                    60000,
                    70000,
                    80000,
                    90000,
                    100000,
                ),
            ),
            "inch36": (
                "inch",
                "0.0001",
                (  # 36 blocks
                    500,
                    1001,
                    1002,
                    1003,
                    1004,
                    1005,
                    1006,
                    1007,
                    1008,
                    1009,
                    1010,
                    1020,
                    1030,
                    1040,
                    1050,
                    1060,
                    1070,
                    1080,
                    1090,
                    1100,
                    1200,
                    1300,
                    1400,
                    1500,
                    1600,
                    1700,
                    1800,
                    1900,
                    1000,
                    2000,
                    3000,
                    4000,
                    5000,
                    10000,
                    20000,
                    40000,
                ),
            ),
            "inch81": (
                "inch",
                "0.0001",
                (  # 81 blocks
                    500,
                    1001,
                    1002,
                    1003,
                    1004,
                    1005,
                    1006,
                    1007,
                    1008,
                    1009,
                    1010,
                    1020,
                    1030,
                    1040,
                    1050,
                    1060,
                    1070,
                    1080,
                    1090,
                    1100,
                    1110,
                    1120,
                    1130,
                    1140,
                    1150,
                    1160,
                    1170,
                    1180,
                    1190,
                    1200,
                    1210,
                    1220,
                    1230,
                    1240,
                    1250,
                    1260,
                    1270,
                    1280,
                    1290,
                    1300,
                    1310,
                    1320,
                    1330,
                    1340,
                    1350,
                    1360,
                    1370,
                    1380,
                    1390,
                    1400,
                    1410,
                    1420,
                    1430,
                    1440,
                    1450,
                    1460,
                    1470,
                    1480,
                    1490,
                    1000,
                    1500,
                    2000,
                    2500,
                    3000,
                    3500,
                    4000,
                    4500,
                    5000,
                    5500,
                    6000,
                    6500,
                    7000,
                    7500,
                    8000,
                    8500,
                    9000,
                    9500,
                    10000,
                    20000,
                    30000,
                    40000,
                ),
            ),
            "space": (
                "inch",
                "0.0005",
                [
                    # This is a "Space Blocks" set I bought in the early 1970's.  I
                    # remember paying around $70 for it and the same sets are
                    # available today for around the same price.  They're cylinders
                    # of steel finished to the stamped length and they can be
                    # clamped together with set screws because there is a tapped
                    # longitudinal hole through each piece.
                    500,
                    625,
                    600,
                    700,
                    800,
                    900,
                    1000,
                    1010,
                    1020,
                    1030,
                    1040,
                    1050,
                    1060,
                    1070,
                    1080,
                    1090,
                    1100,
                    1200,
                    1250,
                    1300,
                    1400,
                    1500,
                    1600,
                    1700,
                    1800,
                    1900,
                    2000,
                    3000,
                    4000,
                    5000,
                    6000,
                    7000,
                    8000,
                    9000,
                    10000,
                    10000,
                ],
            ),
        }
        # Dictionary used to get the format string needed to print out the
        # sizes.
        formats = {
            "0.001": "%.3f",
            "0.0001": "%.4f",
            "0.0005": "%.4f",
        }
        # Check to make sure we don't have a new resolution to handle
        for name in gauge_block_sets:
            unit, resolution, blocks = gauge_block_sets[name]
            assert resolution in formats
if 1:  # Utility

    def Manpage():
        print(
            dedent(
                f"""
 
        This script determines the gauge blocks necessary to get a desired dimensions.  The
        solution method is to search all the combinations of blocks.  This is a brute-force
        solution of the subset-sum problem.  However, it's a practical method when you want to find
        only 4 or 5 gauge block solutions.
 
        The progenitor use case of this script is a purchase I made in 2005 of a used Starrett
        gauge block set.  This was originally a nice 81 block set, but it obviously saw a goodly
        amount of use.  When I got the set, there were missing blocks and other brands substituted
        for some of the Starrett blocks.  The whole set was $50 delivered, probably many tens of
        times less than the set cost new.  The need for the script appeared because of the missing
        blocks -- this was a task that was too labor intensive to do manually.  A python brute
        force search solves the problem to find a practical solution, most of the time using
        only 4 blocks.
            
            In Mar 2024 on my 10 year old computer using python 3.11.5, the search times as a
            function of the number of blocks allowed were (
  
                Blocks       Time, s
                   4            0.2
                   5            0.9
                   6            8.3
                   7            74 
 
            This set has 80 blocks, so the combinatorial problem is 80 choose n.  The numbers, in
            millions, are 
                                    Ratio      Estimated time in s
                C(80, 4) = 1.6      1               0.2
                C(80, 5) = 24       4.5             0.9
                C(80, 6) = 300      138             28
                C(80, 7) = 3180     1990            400
 
        The "space block" set is something I bought in the early 1970's for around $70.  You can
        buy what appear to be nearly identical sets today for $60 to $90.  These are 1 inch diameter
        cylinders that are held together with set screws and will provide stacks giving desired
        sizes to uncertainties probably within a few tenths of a mil.  These will work well for
        most home shop tasks.  It is rare for home shop stuff to need the accuracy of the Starrett
        gauge blocks.
 
        """.rstrip()
            )
        )
        exit(0)

    def Usage(d, status=1):
        name, dsn, maxnum = sys.argv[0], d["-n"], d["-k"]
        tol = d["-f"]
        print(
            dedent(f"""
        Usage:  {name} [options] size1 [size2...]
          Prints out the gauge blocks to use to make up the indicated sizes.  Note the sizes will be
          rounded to the nearest unit of resolution of the gauge block set.  The '{dsn}' gauge block
          set is used by default.
         
          There are quite a few different gauge block sets in the world.  If you need to use a
          different set than what's provided in the script, it's easy to add a new set to the
          gauge_block_sets dictionary at the beginning of the script.
         
          You can use python expressions for the sizes; the math module's symbols are in scope.  For
          example, a gauge block stack for a length of 25/32 of an inch could be gotten by the size
          "3/4 + 1/32", assuming the gauge block dimensions are in inches.
        Options:
          -a        Show all combinations that make up the desired size, not just the first
                    combination found.
          -f pct    Tolerance percentage for -g/-G searches.  Defaults to {tol}%.
          -g dia    Display common gauge sizes for dia in inches.  Gauge sizes are number & letter
                    drills, AWG, and USS sheet steel.
          -G dia    Same as -g, but all gauge sizes are shown
          -h        Print a manpage
          -k num    Set the maximum subset size of blocks to use in the search.  The default is {maxnum}.
                    Making this number too large can result in long run times.
          -n set    Choose which gauge block set to use
          -t        Print out a table of the sizes of each gauge block set
          -T        For the user blocks, print out the dimensions up to 10 inches that cannot be gotten
                    with {maxnum} blocks.
        """)
        )
        print("Allowed gauge block set names and characteristics:")
        s = []
        for name in sorted(gauge_block_sets):
            unit, resolution, blocks = gauge_block_sets[name]
            s.append(f"  {name:10s} {resolution:6s} {unit} ({len(blocks)} blocks)")
        print("\n".join(s))
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Show all combinations, not just the first
        d["-f"] = 1  # Tolerance in % for -g/-G lookups
        d["-g"] = False  # Look up a gauge size (limited set)
        d["-G"] = False  # Look up all gauge sizes
        d["-k"] = 4  # Maximum subset size in search
        d["-n"] = "user"  # Name of default gauge block set
        d["-T"] = False  # Analyze user set for unreachable dimensions
        d["num_blocks"] = (1, 5)  # Min and max block combinations to search for
        if len(sys.argv) < 2:
            Usage(d)
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "af:gGk:n:tT")
        except getopt.error as str:
            print(str)
            sys.exit(1)
        for o, a in optlist:
            if o[1] in "agG":
                d[o] = not d[o]
            elif o == "-f":
                d["-f"] = int(a)
                if d["-f"] <= 0:
                    raise ValueError("-f option must be > 0")
            elif o == "-k":
                d["-k"] = int(a)
                if d["-k"] < 1:
                    raise ValueError("Bad subset size")
            elif o == "-n":
                d["-n"] = a
                if d["-n"] not in gauge_block_sets:
                    sys.stderr.write("Unrecognized gauge block set\n")
                    exit(1)
            elif o == "-t":
                d["-t"] = True
                PrintTable()
                exit(0)
            elif o == "-T":
                d["-T"] = True
                AnalyzeUser(d)
                exit(0)
        if not args:
            Usage(d)
        return args


if 1:  # Core functionality

    def PrintTable():
        """Print nicely-formatted tables of each type of block set."""
        for name, (unit, resolution, seq) in gauge_block_sets.items():
            s, f = [], float(resolution)
            print("{0} ({1})".format(name, "um" if unit == "mm" else "0.0001 inches"))
            fmt = formats[resolution] + "  "
            seq.sort()
            for i in seq:
                s.append(str(i))
            for i in Columnize(s):
                print(i)
        # Next, compare the 81-block and user sets
        set_81 = set(gauge_block_sets["inch81"][2])
        set_user = set(gauge_block_sets["user"][2])
        print("\nBlocks in 81-block set missing from 'user' set:")
        missing = list(set_81 - set_user)
        missing.sort()
        for i in Columnize(missing):
            print(i)
        print("Blocks in 'user' set not in 81-block set:")
        added = list(set_user - set_81)
        added.sort()
        for i in Columnize(added):
            print(i)

    def GetIntegerSize(size, d):
        """Convert the size number (a string in inches or mm) to an integer
        size to search for.
        """
        # string, string, list of integer sizes
        unit, resolution, blocks = gauge_block_sets[d["-n"]]
        x, T = abs(float(eval(size))), abs(float(resolution))
        # Using resolution as a template, round the size to an integer
        # number of template units.
        return int(x / T + 0.5)

    def PrintResults(integer_size, size, combination, d):
        """integer_size is the actual size searched for; size is the
        original string the user passed on the command line.
        """
        # string, string, list of integer sizes
        unit, resolution, blocks = gauge_block_sets[d["-n"]]
        fmt = formats[resolution]
        sz = abs(float(eval(size)))
        print(fmt % sz, ": ", sep="", end="")
        for i in combination:
            print(fmt % (float(i) * float(resolution)), " ", end="")
        print()

    def GetBlocks(size_str, d):
        size = GetIntegerSize(size_str, d)
        set_of_blocks = gauge_block_sets[d["-n"]][2]
        if size > sum(set_of_blocks):
            print("No solution for size %s" % size)
            return
        for num_blocks in range(1, d["-k"] + 1):
            for i in combinations(set_of_blocks, num_blocks):
                if sum(i) == size:
                    if not d["-T"]:
                        PrintResults(size, size_str, i, d)
                    if not d["-a"]:
                        return i
        return None

    def AnalyzeUser(d):
        """For dimensions less than 10 inches, determine which dimensions can't
        be gotten using the indicated (-k option) number of blocks.
        """
        ofp = open("user.blocks.impossible", "w")
        max_blocks = d["-k"]
        if 0:
            # Units are 0.0001 inches
            min_size, max_size = 1001, 100000
            print(
                dedent("""
            0.0001 inch dimensions that cannot be gotten with user block set:
            (Maximum number of blocks used is {max_blocks}).
            """)
            )
            print(msg)
            ofp.write(msg + "\n")
            for i, sz in enumerate(range(min_size, max_size)):
                size = f"  {sz / 10000:.4f}"
                seq = GetBlocks(size, d)
                if seq is None:
                    print(size)
                    ofp.write(size + "\n")
        if 1:
            # Units are 0.001 inches
            min_size, max_size = 100, 10000
            print(
                dedent("""
            0.001 inch dimensions that cannot be gotten with user block set:
            (Maximum number of blocks used is {max_blocks}).""")
            )
            print(msg)
            ofp.write(msg + "\n")
            for i, sz in enumerate(range(min_size, max_size)):
                size = f"{sz / 1000:.3f}"
                seq = GetBlocks(size, d)
                if seq is None:
                    print(size)
                    ofp.write(size + "\n")

    def GetSize(size):
        """size is a string and will normally be a decimal number in inches.
        However, an optional length unit can be appended (space separator
        optional).  The size in inches is returned.
        """
        t, unit = ParseUnit(size)
        t = float(t)
        if unit:
            if u.dim("inches") != u.dim(unit):
                print("'{}' is not a length unit".format(unit))
                exit(1)
            t *= u(unit) / u("inches")
        return t

    def GaugeSizes(sizes, d, all=False):
        """Display gauge sizes that are within the tolerance percentage (from
        d["-f"]) of the given size.
        """
        GAUGES = (
            list(sorted(gauges.keys()))
            if all
            else [
                "US Number drill sizes",
                "US Letter drill sizes",
                "AWG",
                "US Standard steel sheet",
            ]
        )
        tolerance = d["-f"]
        print("Printed items are within {}% of indicated size\n".format(tolerance))
        for Size in sizes:
            size = GetSize(Size)  # Convert to float in inches
            print("Size =", Size, " = {:.4f} inches".format(size))
            s = []
            for gauge in GAUGES:
                g = gauges[gauge]
                for sz in g:
                    sz_inches = g[sz]
                    tol = 100 * (sz_inches - size) / size
                    if abs(tol) <= tolerance:
                        s.append((tol, sz, sz_inches, gauge))
            if s:
                # Sort by first item, which is tolerance in %
                def f(x):
                    return x[0]

                for tol, sz, sz_inches, gauge in sorted(s, key=f):
                    print(
                        "  {:2s}   {:.4f}   {:6.1f}%   {}".format(
                            str(sz), sz_inches, tol, gauge
                        )
                    )
            else:
                print("  No matches")


if 1:  # Find sizes that cannot be made

    def PartialStarrettSet(dia_min, dia_max, klo=4, khi=6):
        """Print out the sizes that cannot be made with the indicated number of blocks.  dia_min
        and dia_max are integers in units of 0.0001 inches.  klo and khi are the k values to search
        with (k = number of blocks in set)
        """
        blocks = gauge_block_sets["user"][2]
        Assert(len(blocks) == 64)
        if 0:
            print(blocks)
        N = dia_max - dia_min + 1
        count = 0
        for dia in range(dia_min, dia_max + 1):
            count += 1
            found = False
            for k in range(klo, khi + 1):
                for i in combinations(blocks, k):
                    if sum(i) == dia:
                        found = True
                        break
                if found:
                    break
            if not found:
                x = float(dia / 1e4)
                # print(f"{t('ornl')}{x:.4f}{t.n}", end=" ")
                print(f"{x:.4f} {sw()} seconds", file=fd)
            # if count and count % 1000 == 0:
            #    pct = int(100*count/N)
            #    print(f"{t('redl')}{pct}%{t.n}", file=sys.stderr)
        # print()


if 0:
    d, D = 4000, 100000
    from timer import Stopwatch

    with open("starrett.64.impossible_4_to_6", "w") as fd:
        sw = Stopwatch()
        print("k = 4 to 6 impossible sizes from $pp/gauge.py", file=fd)
        PartialStarrettSet(d, D, klo=4, khi=6)
    print(f"Ended at {sw()} seconds")
    exit()
    """Results of running this code:

    k = 4 to 6 impossible sizes from $pp/gauge.py.  Took 1.7 days of calculation, 9033 sizes cannot be
    made out of 0.4 to 10 inches in steps of 0.1 mils, 96e3 sizes; this is 9.4%.  About 50% of them are
    above 9 inches, 1% are below 6 inches.

    2.6491 2.6492 2.6531 2.6532 2.6541 2.6542 2.7491 2.7492 2.7531 2.7532 2.7541 2.7542 2.8491 2.8492
    2.8531 2.8532 2.8541 2.8542 

    3.6491 3.6492 3.6531 3.6532 3.6541 3.6542 3.7491 3.7492 3.7531 3.7532
    3.7541 3.7542 3.8491 3.8492 3.8531 3.8532 3.8541 3.8542 

    4.6491 4.6492 4.6531 4.6532 4.6541 4.6542
    4.7491 4.7492 4.7531 4.7532 4.7541 4.7542 4.8491 4.8492 4.8531 4.8532 4.8541 4.8542

    5.4991 5.4992
    5.5031 5.5032 5.5041 5.5042 5.5111 5.5112 5.5141 5.5142 5.5161 5.5162 5.5211 5.5212 5.5251 5.5252
    5.5291 5.5292 5.5371 5.5372 5.5421 5.5422 5.5491 5.5492 5.5531 5.5532 5.5541 5.5542 5.5611 5.5612
    5.5641 5.5642 5.5661 5.5662 5.5711 5.5712 5.5751 5.5752 5.5791 5.5792 5.5871 5.5872 5.5921 5.5922
    5.5991 5.5992 5.6031 5.6032 5.6041 5.6042 5.6111 5.6112 5.6141 5.6142 5.6161 5.6162 5.6211 5.6212
    5.6251 5.6252 5.6291 5.6292 5.6371 5.6372 5.6421 5.6422 5.6491 5.6492 5.6531 5.6532 5.6541 5.6542
    5.6611 5.6612 5.6641 5.6642 5.6661 5.6662 5.6711 5.6712 5.6751 5.6752 5.6791 5.6792 5.6871 5.6872
    5.6921 5.6922 5.6991 5.6992 5.7031 5.7032 5.7041 5.7042 5.7111 5.7112 5.7141 5.7142 5.7161 5.7162
    5.7211 5.7212 5.7251 5.7252 5.7291 5.7292 5.7371 5.7372 5.7421 5.7422 5.7491 5.7492 5.7531 5.7532
    5.7541 5.7542 5.7611 5.7612 5.7641 5.7642 5.7661 5.7662 5.7711 5.7712 5.7751 5.7752 5.7791 5.7792
    5.7871 5.7872 5.7921 5.7922 5.7991 5.7992 5.8031 5.8032 5.8041 5.8042 5.8111 5.8112 5.8141 5.8142
    5.8161 5.8162 5.8211 5.8212 5.8251 5.8252 5.8291 5.8292 5.8371 5.8372 5.8421 5.8422 5.8491 5.8492
    5.8531 5.8532 5.8541 5.8542 5.8611 5.8612 5.8641 5.8642 5.8661 5.8662 5.8711 5.8712 5.8751 5.8752
    5.8791 5.8792 5.8871 5.8872 5.8921 5.8922 5.8991 5.8992 5.9031 5.9032 5.9041 5.9042 5.9111 5.9112
    5.9141 5.9142 5.9161 5.9162 5.9211 5.9212 5.9251 5.9252 5.9291 5.9292 5.9371 5.9372 5.9421 5.9422
    5.9491 5.9492 5.9531 5.9532 5.9541 5.9542 5.9611 5.9612 5.9641 5.9642 5.9661 5.9662 5.9711 5.9712
    5.9751 5.9752 5.9791 5.9792 5.9871 5.9872 5.9921 5.9922 5.9991 5.9992 

    6.0031 6.0032 6.0041 6.0042
    6.0111 6.0112 6.0141 6.0142 6.0161 6.0162 6.0211 6.0212 6.0251 6.0252 6.0291 6.0292 6.0371 6.0372
    6.0421 6.0422 6.0491 6.0492 6.0531 6.0532 6.0541 6.0542 6.0611 6.0612 6.0641 6.0642 6.0661 6.0662
    6.0711 6.0712 6.0751 6.0752 6.0791 6.0792 6.0871 6.0872 6.0921 6.0922 6.0991 6.0992 6.1031 6.1032
    6.1041 6.1042 6.1111 6.1112 6.1141 6.1142 6.1161 6.1162 6.1211 6.1212 6.1251 6.1252 6.1291 6.1292
    6.1371 6.1372 6.1421 6.1422 6.1491 6.1492 6.1531 6.1532 6.1541 6.1542 6.1611 6.1612 6.1641 6.1642
    6.1661 6.1662 6.1711 6.1712 6.1751 6.1752 6.1791 6.1792 6.1871 6.1872 6.1921 6.1922 6.1991 6.1992
    6.2031 6.2032 6.2041 6.2042 6.2111 6.2112 6.2141 6.2142 6.2161 6.2162 6.2211 6.2212 6.2251 6.2252
    6.2291 6.2292 6.2371 6.2372 6.2421 6.2422 6.2491 6.2492 6.2531 6.2532 6.2541 6.2542 6.2641 6.2642
    6.2661 6.2662 6.2711 6.2712 6.2791 6.2792 6.2871 6.2872 6.2921 6.2922 6.2991 6.2992 6.3031 6.3032
    6.3041 6.3042 6.3111 6.3112 6.3141 6.3142 6.3161 6.3162 6.3211 6.3212 6.3251 6.3252 6.3291 6.3292
    6.3991 6.3992 6.4031 6.4032 6.4041 6.4042 6.4991 6.4992 6.5021 6.5022 6.5031 6.5032 6.5041 6.5042
    6.5051 6.5052 6.5061 6.5062 6.5071 6.5072 6.5081 6.5082 6.5091 6.5092 6.5101 6.5102 6.5111 6.5112
    6.5121 6.5122 6.5131 6.5132 6.5141 6.5142 6.5151 6.5152 6.5161 6.5162 6.5171 6.5172 6.5181 6.5182
    6.5191 6.5192 6.5201 6.5202 6.5211 6.5212 6.5221 6.5222 6.5231 6.5232 6.5241 6.5242 6.5251 6.5252
    6.5261 6.5262 6.5271 6.5272 6.5281 6.5282 6.5291 6.5292 6.5301 6.5302 6.5311 6.5312 6.5321 6.5322
    6.5331 6.5332 6.5341 6.5342 6.5351 6.5352 6.5361 6.5362 6.5371 6.5372 6.5381 6.5382 6.5391 6.5392
    6.5401 6.5402 6.5411 6.5412 6.5421 6.5422 6.5431 6.5432 6.5441 6.5442 6.5451 6.5452 6.5461 6.5462
    6.5471 6.5472 6.5481 6.5482 6.5483 6.5484 6.5485 6.5486 6.5487 6.5488 6.5489 6.5491 6.5492 6.5501
    6.5502 6.5525 6.5526 6.5527 6.5528 6.5529 6.5531 6.5532 6.5533 6.5534 6.5535 6.5536 6.5537 6.5538
    6.5539 6.5541 6.5542 6.5611 6.5612 6.5641 6.5642 6.5661 6.5662 6.5711 6.5712 6.5751 6.5752 6.5791
    6.5792 6.5871 6.5872 6.5921 6.5922 6.5991 6.5992 6.6021 6.6022 6.6031 6.6032 6.6041 6.6042 6.6051
    6.6052 6.6061 6.6062 6.6071 6.6072 6.6081 6.6082 6.6091 6.6092 6.6101 6.6102 6.6111 6.6112 6.6121
    6.6122 6.6131 6.6132 6.6141 6.6142 6.6151 6.6152 6.6161 6.6162 6.6171 6.6172 6.6181 6.6182 6.6191
    6.6192 6.6201 6.6202 6.6211 6.6212 6.6221 6.6222 6.6231 6.6232 6.6241 6.6242 6.6251 6.6252 6.6261
    6.6262 6.6271 6.6272 6.6281 6.6282 6.6291 6.6292 6.6301 6.6302 6.6311 6.6312 6.6321 6.6322 6.6331
    6.6332 6.6341 6.6342 6.6351 6.6352 6.6361 6.6362 6.6371 6.6372 6.6381 6.6382 6.6391 6.6392 6.6401
    6.6402 6.6411 6.6412 6.6421 6.6422 6.6431 6.6432 6.6441 6.6442 6.6451 6.6452 6.6461 6.6462 6.6471
    6.6472 6.6481 6.6482 6.6483 6.6484 6.6485 6.6486 6.6487 6.6488 6.6489 6.6491 6.6492 6.6501 6.6502
    6.6525 6.6526 6.6527 6.6528 6.6529 6.6531 6.6532 6.6533 6.6534 6.6535 6.6536 6.6537 6.6538 6.6539
    6.6541 6.6542 6.6611 6.6612 6.6641 6.6642 6.6661 6.6662 6.6711 6.6712 6.6751 6.6752 6.6791 6.6792
    6.6871 6.6872 6.6921 6.6922 6.6991 6.6992 6.7021 6.7022 6.7031 6.7032 6.7041 6.7042 6.7051 6.7052
    6.7061 6.7062 6.7071 6.7072 6.7081 6.7082 6.7091 6.7092 6.7101 6.7102 6.7111 6.7112 6.7121 6.7122
    6.7131 6.7132 6.7141 6.7142 6.7151 6.7152 6.7161 6.7162 6.7171 6.7172 6.7181 6.7182 6.7191 6.7192
    6.7201 6.7202 6.7211 6.7212 6.7221 6.7222 6.7231 6.7232 6.7241 6.7242 6.7251 6.7252 6.7261 6.7262
    6.7271 6.7272 6.7281 6.7282 6.7291 6.7292 6.7301 6.7302 6.7311 6.7312 6.7321 6.7322 6.7331 6.7332
    6.7341 6.7342 6.7351 6.7352 6.7361 6.7362 6.7371 6.7372 6.7381 6.7382 6.7391 6.7392 6.7401 6.7402
    6.7411 6.7412 6.7421 6.7422 6.7431 6.7432 6.7441 6.7442 6.7451 6.7452 6.7461 6.7462 6.7471 6.7472
    6.7481 6.7482 6.7483 6.7484 6.7485 6.7486 6.7487 6.7488 6.7489 6.7491 6.7492 6.7501 6.7502 6.7525
    6.7526 6.7527 6.7528 6.7529 6.7531 6.7532 6.7533 6.7534 6.7535 6.7536 6.7537 6.7538 6.7539 6.7541
    6.7542 6.7611 6.7612 6.7641 6.7642 6.7661 6.7662 6.7711 6.7712 6.7751 6.7752 6.7791 6.7792 6.7871
    6.7872 6.7921 6.7922 6.7991 6.7992 6.8021 6.8022 6.8031 6.8032 6.8041 6.8042 6.8051 6.8052 6.8061
    6.8062 6.8071 6.8072 6.8081 6.8082 6.8091 6.8092 6.8101 6.8102 6.8111 6.8112 6.8121 6.8122 6.8131
    6.8132 6.8141 6.8142 6.8151 6.8152 6.8161 6.8162 6.8171 6.8172 6.8181 6.8182 6.8191 6.8192 6.8201
    6.8202 6.8211 6.8212 6.8221 6.8222 6.8231 6.8232 6.8241 6.8242 6.8251 6.8252 6.8271 6.8272 6.8281
    6.8282 6.8291 6.8292 6.8301 6.8302 6.8311 6.8312 6.8321 6.8322 6.8331 6.8332 6.8341 6.8342 6.8351
    6.8352 6.8371 6.8372 6.8381 6.8382 6.8391 6.8392 6.8401 6.8402 6.8411 6.8412 6.8421 6.8422 6.8431
    6.8432 6.8441 6.8442 6.8451 6.8452 6.8461 6.8462 6.8471 6.8472 6.8481 6.8482 6.8491 6.8492 6.8531
    6.8532 6.8541 6.8542 6.8611 6.8612 6.8641 6.8642 6.8661 6.8662 6.8711 6.8712 6.8751 6.8752 6.8791
    6.8792 6.8871 6.8872 6.8921 6.8922 6.8991 6.8992 6.9031 6.9032 6.9041 6.9042 6.9111 6.9112 6.9141
    6.9142 6.9161 6.9162 6.9211 6.9212 6.9251 6.9252 6.9291 6.9292 6.9371 6.9372 6.9421 6.9422 6.9491
    6.9492 6.9531 6.9532 6.9541 6.9542 6.9611 6.9612 6.9641 6.9642 6.9661 6.9662 6.9711 6.9712 6.9751
    6.9752 6.9791 6.9792 6.9871 6.9872 6.9921 6.9922 6.9991 6.9992

    7.0031 7.0032 7.0041 7.0042 7.0111
    7.0112 7.0141 7.0142 7.0161 7.0162 7.0211 7.0212 7.0251 7.0252 7.0291 7.0292 7.0371 7.0372 7.0421
    7.0422 7.0491 7.0492 7.0531 7.0532 7.0541 7.0542 7.0611 7.0612 7.0641 7.0642 7.0661 7.0662 7.0711
    7.0712 7.0751 7.0752 7.0791 7.0792 7.0871 7.0872 7.0921 7.0922 7.0991 7.0992 7.1031 7.1032 7.1041
    7.1042 7.1111 7.1112 7.1141 7.1142 7.1161 7.1162 7.1211 7.1212 7.1251 7.1252 7.1291 7.1292 7.1371
    7.1372 7.1421 7.1422 7.1491 7.1492 7.1531 7.1532 7.1541 7.1542 7.1611 7.1612 7.1641 7.1642 7.1661
    7.1662 7.1711 7.1712 7.1751 7.1752 7.1791 7.1792 7.1871 7.1872 7.1921 7.1922 7.1991 7.1992 7.2031
    7.2032 7.2041 7.2042 7.2111 7.2112 7.2141 7.2142 7.2161 7.2162 7.2211 7.2212 7.2251 7.2252 7.2291
    7.2292 7.2371 7.2372 7.2421 7.2422 7.2491 7.2492 7.2531 7.2532 7.2541 7.2542 7.2641 7.2642 7.2661
    7.2662 7.2711 7.2712 7.2791 7.2792 7.2871 7.2872 7.2921 7.2922 7.2991 7.2992 7.3031 7.3032 7.3041
    7.3042 7.3111 7.3112 7.3141 7.3142 7.3161 7.3162 7.3211 7.3212 7.3251 7.3252 7.3291 7.3292 7.3991
    7.3992 7.4031 7.4032 7.4041 7.4042 7.4991 7.4992 7.5021 7.5022 7.5031 7.5032 7.5041 7.5042 7.5051
    7.5052 7.5061 7.5062 7.5071 7.5072 7.5081 7.5082 7.5091 7.5092 7.5101 7.5102 7.5111 7.5112 7.5121
    7.5122 7.5131 7.5132 7.5141 7.5142 7.5151 7.5152 7.5161 7.5162 7.5171 7.5172 7.5181 7.5182 7.5191
    7.5192 7.5201 7.5202 7.5211 7.5212 7.5221 7.5222 7.5231 7.5232 7.5241 7.5242 7.5251 7.5252 7.5261
    7.5262 7.5271 7.5272 7.5281 7.5282 7.5291 7.5292 7.5301 7.5302 7.5311 7.5312 7.5321 7.5322 7.5331
    7.5332 7.5341 7.5342 7.5351 7.5352 7.5361 7.5362 7.5371 7.5372 7.5381 7.5382 7.5391 7.5392 7.5401
    7.5402 7.5411 7.5412 7.5421 7.5422 7.5431 7.5432 7.5441 7.5442 7.5451 7.5452 7.5461 7.5462 7.5471
    7.5472 7.5481 7.5482 7.5483 7.5484 7.5485 7.5486 7.5487 7.5488 7.5489 7.5491 7.5492 7.5501 7.5502
    7.5525 7.5526 7.5527 7.5528 7.5529 7.5531 7.5532 7.5533 7.5534 7.5535 7.5536 7.5537 7.5538 7.5539
    7.5541 7.5542 7.5611 7.5612 7.5641 7.5642 7.5661 7.5662 7.5711 7.5712 7.5751 7.5752 7.5791 7.5792
    7.5871 7.5872 7.5921 7.5922 7.5991 7.5992 7.6021 7.6022 7.6031 7.6032 7.6041 7.6042 7.6051 7.6052
    7.6061 7.6062 7.6071 7.6072 7.6081 7.6082 7.6091 7.6092 7.6101 7.6102 7.6111 7.6112 7.6121 7.6122
    7.6131 7.6132 7.6141 7.6142 7.6151 7.6152 7.6161 7.6162 7.6171 7.6172 7.6181 7.6182 7.6191 7.6192
    7.6201 7.6202 7.6211 7.6212 7.6221 7.6222 7.6231 7.6232 7.6241 7.6242 7.6251 7.6252 7.6261 7.6262
    7.6271 7.6272 7.6281 7.6282 7.6291 7.6292 7.6301 7.6302 7.6311 7.6312 7.6321 7.6322 7.6331 7.6332
    7.6341 7.6342 7.6351 7.6352 7.6361 7.6362 7.6371 7.6372 7.6381 7.6382 7.6391 7.6392 7.6401 7.6402
    7.6411 7.6412 7.6421 7.6422 7.6431 7.6432 7.6441 7.6442 7.6451 7.6452 7.6461 7.6462 7.6471 7.6472
    7.6481 7.6482 7.6483 7.6484 7.6485 7.6486 7.6487 7.6488 7.6489 7.6491 7.6492 7.6501 7.6502 7.6525
    7.6526 7.6527 7.6528 7.6529 7.6531 7.6532 7.6533 7.6534 7.6535 7.6536 7.6537 7.6538 7.6539 7.6541
    7.6542 7.6611 7.6612 7.6641 7.6642 7.6661 7.6662 7.6711 7.6712 7.6751 7.6752 7.6791 7.6792 7.6871
    7.6872 7.6921 7.6922 7.6991 7.6992 7.7021 7.7022 7.7031 7.7032 7.7041 7.7042 7.7051 7.7052 7.7061
    7.7062 7.7071 7.7072 7.7081 7.7082 7.7091 7.7092 7.7101 7.7102 7.7111 7.7112 7.7121 7.7122 7.7131
    7.7132 7.7141 7.7142 7.7151 7.7152 7.7161 7.7162 7.7171 7.7172 7.7181 7.7182 7.7191 7.7192 7.7201
    7.7202 7.7211 7.7212 7.7221 7.7222 7.7231 7.7232 7.7241 7.7242 7.7251 7.7252 7.7261 7.7262 7.7271
    7.7272 7.7281 7.7282 7.7291 7.7292 7.7301 7.7302 7.7311 7.7312 7.7321 7.7322 7.7331 7.7332 7.7341
    7.7342 7.7351 7.7352 7.7361 7.7362 7.7371 7.7372 7.7381 7.7382 7.7391 7.7392 7.7401 7.7402 7.7411
    7.7412 7.7421 7.7422 7.7431 7.7432 7.7441 7.7442 7.7451 7.7452 7.7461 7.7462 7.7471 7.7472 7.7481
    7.7482 7.7483 7.7484 7.7485 7.7486 7.7487 7.7488 7.7489 7.7491 7.7492 7.7501 7.7502 7.7525 7.7526
    7.7527 7.7528 7.7529 7.7531 7.7532 7.7533 7.7534 7.7535 7.7536 7.7537 7.7538 7.7539 7.7541 7.7542
    7.7611 7.7612 7.7641 7.7642 7.7661 7.7662 7.7711 7.7712 7.7751 7.7752 7.7791 7.7792 7.7871 7.7872
    7.7921 7.7922 7.7991 7.7992 7.8021 7.8022 7.8031 7.8032 7.8041 7.8042 7.8051 7.8052 7.8061 7.8062
    7.8071 7.8072 7.8081 7.8082 7.8091 7.8092 7.8101 7.8102 7.8111 7.8112 7.8121 7.8122 7.8131 7.8132
    7.8141 7.8142 7.8151 7.8152 7.8161 7.8162 7.8171 7.8172 7.8181 7.8182 7.8191 7.8192 7.8201 7.8202
    7.8211 7.8212 7.8221 7.8222 7.8231 7.8232 7.8241 7.8242 7.8251 7.8252 7.8271 7.8272 7.8281 7.8282
    7.8291 7.8292 7.8301 7.8302 7.8311 7.8312 7.8321 7.8322 7.8331 7.8332 7.8341 7.8342 7.8351 7.8352
    7.8371 7.8372 7.8381 7.8382 7.8391 7.8392 7.8401 7.8402 7.8411 7.8412 7.8421 7.8422 7.8431 7.8432
    7.8441 7.8442 7.8451 7.8452 7.8461 7.8462 7.8471 7.8472 7.8481 7.8482 7.8491 7.8492 7.8531 7.8532
    7.8541 7.8542 7.8611 7.8612 7.8641 7.8642 7.8661 7.8662 7.8711 7.8712 7.8751 7.8752 7.8791 7.8792
    7.8871 7.8872 7.8921 7.8922 7.8991 7.8992 7.9031 7.9032 7.9041 7.9042 7.9111 7.9112 7.9141 7.9142
    7.9161 7.9162 7.9211 7.9212 7.9251 7.9252 7.9291 7.9292 7.9371 7.9372 7.9421 7.9422 7.9491 7.9492
    7.9531 7.9532 7.9541 7.9542 7.9611 7.9612 7.9641 7.9642 7.9661 7.9662 7.9711 7.9712 7.9751 7.9752
    7.9791 7.9792 7.9871 7.9872 7.9921 7.9922 7.9991 7.9992

    8.0031 8.0032 8.0041 8.0042 8.0111 8.0112
    8.0141 8.0142 8.0161 8.0162 8.0211 8.0212 8.0251 8.0252 8.0291 8.0292 8.0371 8.0372 8.0421 8.0422
    8.0491 8.0492 8.0531 8.0532 8.0541 8.0542 8.0611 8.0612 8.0641 8.0642 8.0661 8.0662 8.0711 8.0712
    8.0751 8.0752 8.0791 8.0792 8.0871 8.0872 8.0921 8.0922 8.0991 8.0992 8.1031 8.1032 8.1041 8.1042
    8.1111 8.1112 8.1141 8.1142 8.1161 8.1162 8.1211 8.1212 8.1251 8.1252 8.1291 8.1292 8.1371 8.1372
    8.1421 8.1422 8.1491 8.1492 8.1531 8.1532 8.1541 8.1542 8.1611 8.1612 8.1641 8.1642 8.1661 8.1662
    8.1711 8.1712 8.1751 8.1752 8.1791 8.1792 8.1871 8.1872 8.1921 8.1922 8.1991 8.1992 8.2031 8.2032
    8.2041 8.2042 8.2111 8.2112 8.2141 8.2142 8.2161 8.2162 8.2211 8.2212 8.2251 8.2252 8.2291 8.2292
    8.2371 8.2372 8.2421 8.2422 8.2491 8.2492 8.2501 8.2502 8.2531 8.2532 8.2541 8.2542 8.2611 8.2612
    8.2641 8.2642 8.2661 8.2662 8.2711 8.2712 8.2751 8.2752 8.2791 8.2792 8.2871 8.2872 8.2921 8.2922
    8.2991 8.2992 8.3001 8.3002 8.3021 8.3022 8.3031 8.3032 8.3041 8.3042 8.3051 8.3052 8.3061 8.3062
    8.3071 8.3072 8.3081 8.3082 8.3091 8.3092 8.3101 8.3102 8.3111 8.3112 8.3121 8.3122 8.3131 8.3132
    8.3141 8.3142 8.3151 8.3152 8.3161 8.3162 8.3171 8.3172 8.3181 8.3182 8.3191 8.3192 8.3201 8.3202
    8.3211 8.3212 8.3221 8.3222 8.3231 8.3232 8.3241 8.3242 8.3251 8.3252 8.3261 8.3262 8.3271 8.3272
    8.3281 8.3282 8.3291 8.3292 8.3301 8.3302 8.3311 8.3312 8.3321 8.3322 8.3331 8.3332 8.3341 8.3342
    8.3351 8.3352 8.3361 8.3362 8.3371 8.3372 8.3381 8.3382 8.3391 8.3392 8.3401 8.3402 8.3411 8.3412
    8.3421 8.3422 8.3431 8.3432 8.3441 8.3442 8.3451 8.3452 8.3461 8.3462 8.3471 8.3472 8.3481 8.3482
    8.3483 8.3484 8.3485 8.3486 8.3487 8.3488 8.3489 8.3491 8.3492 8.3501 8.3502 8.3518 8.3519 8.3521
    8.3522 8.3523 8.3524 8.3525 8.3526 8.3527 8.3528 8.3529 8.3531 8.3532 8.3533 8.3534 8.3535 8.3536
    8.3537 8.3538 8.3539 8.3541 8.3542 8.3551 8.3552 8.3561 8.3562 8.3571 8.3572 8.3581 8.3582 8.3591
    8.3592 8.3601 8.3602 8.3603 8.3604 8.3605 8.3606 8.3607 8.3608 8.3609 8.3611 8.3612 8.3621 8.3622
    8.3631 8.3632 8.3633 8.3634 8.3635 8.3636 8.3637 8.3638 8.3639 8.3641 8.3642 8.3651 8.3652 8.3653
    8.3654 8.3655 8.3656 8.3657 8.3658 8.3659 8.3661 8.3662 8.3671 8.3672 8.3681 8.3682 8.3691 8.3692
    8.3701 8.3702 8.3703 8.3704 8.3705 8.3706 8.3707 8.3708 8.3709 8.3711 8.3712 8.3721 8.3722 8.3731
    8.3732 8.3741 8.3742 8.3743 8.3744 8.3745 8.3746 8.3747 8.3748 8.3749 8.3751 8.3752 8.3761 8.3762
    8.3771 8.3772 8.3781 8.3782 8.3783 8.3784 8.3785 8.3786 8.3787 8.3788 8.3789 8.3791 8.3792 8.3801
    8.3802 8.3811 8.3812 8.3821 8.3822 8.3831 8.3832 8.3841 8.3842 8.3851 8.3852 8.3861 8.3862 8.3863
    8.3864 8.3865 8.3866 8.3867 8.3868 8.3869 8.3871 8.3872 8.3881 8.3882 8.3891 8.3892 8.3901 8.3902
    8.3911 8.3912 8.3913 8.3914 8.3915 8.3916 8.3917 8.3918 8.3919 8.3921 8.3922 8.3931 8.3932 8.3941
    8.3942 8.3951 8.3952 8.3961 8.3962 8.3971 8.3972 8.3981 8.3982 8.3983 8.3984 8.3985 8.3986 8.3987
    8.3988 8.3989 8.3991 8.3992 8.4001 8.4002 8.4018 8.4019 8.4021 8.4022 8.4023 8.4024 8.4025 8.4026
    8.4027 8.4028 8.4029 8.4031 8.4032 8.4033 8.4034 8.4035 8.4036 8.4037 8.4038 8.4039 8.4041 8.4042
    8.4051 8.4052 8.4061 8.4062 8.4071 8.4072 8.4081 8.4082 8.4091 8.4092 8.4101 8.4102 8.4103 8.4104
    8.4105 8.4106 8.4107 8.4108 8.4109 8.4111 8.4112 8.4121 8.4122 8.4131 8.4132 8.4133 8.4134 8.4135
    8.4136 8.4137 8.4138 8.4139 8.4141 8.4142 8.4151 8.4152 8.4153 8.4154 8.4155 8.4156 8.4157 8.4158
    8.4159 8.4161 8.4162 8.4171 8.4172 8.4181 8.4182 8.4191 8.4192 8.4201 8.4202 8.4203 8.4204 8.4205
    8.4206 8.4207 8.4208 8.4209 8.4211 8.4212 8.4221 8.4222 8.4231 8.4232 8.4241 8.4242 8.4243 8.4244
    8.4245 8.4246 8.4247 8.4248 8.4249 8.4251 8.4252 8.4261 8.4262 8.4271 8.4272 8.4281 8.4282 8.4283
    8.4284 8.4285 8.4286 8.4287 8.4288 8.4289 8.4291 8.4292 8.4301 8.4302 8.4311 8.4312 8.4321 8.4322
    8.4331 8.4332 8.4341 8.4342 8.4351 8.4352 8.4361 8.4362 8.4363 8.4364 8.4365 8.4366 8.4367 8.4368
    8.4369 8.4371 8.4372 8.4381 8.4382 8.4391 8.4392 8.4401 8.4402 8.4411 8.4412 8.4413 8.4414 8.4415
    8.4416 8.4417 8.4418 8.4419 8.4421 8.4422 8.4431 8.4432 8.4441 8.4442 8.4451 8.4452 8.4461 8.4462
    8.4471 8.4472 8.4481 8.4482 8.4483 8.4484 8.4485 8.4486 8.4487 8.4488 8.4489 8.4491 8.4492 8.4501
    8.4502 8.4518 8.4519 8.4521 8.4522 8.4523 8.4524 8.4525 8.4526 8.4527 8.4528 8.4529 8.4531 8.4532
    8.4533 8.4534 8.4535 8.4536 8.4537 8.4538 8.4539 8.4541 8.4542 8.4551 8.4552 8.4561 8.4562 8.4571
    8.4572 8.4581 8.4582 8.4591 8.4592 8.4601 8.4602 8.4603 8.4604 8.4605 8.4606 8.4607 8.4608 8.4609
    8.4611 8.4612 8.4621 8.4622 8.4631 8.4632 8.4633 8.4634 8.4635 8.4636 8.4637 8.4638 8.4639 8.4641
    8.4642 8.4651 8.4652 8.4653 8.4654 8.4655 8.4656 8.4657 8.4658 8.4659 8.4661 8.4662 8.4671 8.4672
    8.4681 8.4682 8.4691 8.4692 8.4701 8.4702 8.4703 8.4704 8.4705 8.4706 8.4707 8.4708 8.4709 8.4711
    8.4712 8.4721 8.4722 8.4731 8.4732 8.4741 8.4742 8.4743 8.4744 8.4745 8.4746 8.4747 8.4748 8.4749
    8.4751 8.4752 8.4761 8.4762 8.4771 8.4772 8.4781 8.4782 8.4783 8.4784 8.4785 8.4786 8.4787 8.4788
    8.4789 8.4791 8.4792 8.4801 8.4802 8.4811 8.4812 8.4821 8.4822 8.4831 8.4832 8.4841 8.4842 8.4851
    8.4852 8.4861 8.4862 8.4863 8.4864 8.4865 8.4866 8.4867 8.4868 8.4869 8.4871 8.4872 8.4881 8.4882
    8.4891 8.4892 8.4901 8.4902 8.4911 8.4912 8.4913 8.4914 8.4915 8.4916 8.4917 8.4918 8.4919 8.4921
    8.4922 8.4931 8.4932 8.4941 8.4942 8.4951 8.4952 8.4961 8.4962 8.4971 8.4972 8.4981 8.4982 8.4983
    8.4984 8.4985 8.4986 8.4987 8.4988 8.4989 8.4991 8.4992 8.5001 8.5002 8.5018 8.5019 8.5021 8.5022
    8.5023 8.5024 8.5025 8.5026 8.5027 8.5028 8.5029 8.5031 8.5032 8.5033 8.5034 8.5035 8.5036 8.5037
    8.5038 8.5039 8.5041 8.5042 8.5051 8.5052 8.5061 8.5062 8.5071 8.5072 8.5081 8.5082 8.5091 8.5092
    8.5101 8.5102 8.5103 8.5104 8.5105 8.5106 8.5107 8.5108 8.5109 8.5111 8.5112 8.5121 8.5122 8.5131
    8.5132 8.5133 8.5134 8.5135 8.5136 8.5137 8.5138 8.5139 8.5141 8.5142 8.5151 8.5152 8.5153 8.5154
    8.5155 8.5156 8.5157 8.5158 8.5159 8.5161 8.5162 8.5171 8.5172 8.5181 8.5182 8.5191 8.5192 8.5201
    8.5202 8.5203 8.5204 8.5205 8.5206 8.5207 8.5208 8.5209 8.5211 8.5212 8.5221 8.5222 8.5231 8.5232
    8.5241 8.5242 8.5243 8.5244 8.5245 8.5246 8.5247 8.5248 8.5249 8.5251 8.5252 8.5261 8.5262 8.5271
    8.5272 8.5281 8.5282 8.5283 8.5284 8.5285 8.5286 8.5287 8.5288 8.5289 8.5291 8.5292 8.5301 8.5302
    8.5311 8.5312 8.5321 8.5322 8.5331 8.5332 8.5341 8.5342 8.5351 8.5352 8.5361 8.5362 8.5363 8.5364
    8.5365 8.5366 8.5367 8.5368 8.5369 8.5371 8.5372 8.5381 8.5382 8.5391 8.5392 8.5401 8.5402 8.5411
    8.5412 8.5413 8.5414 8.5415 8.5416 8.5417 8.5418 8.5419 8.5421 8.5422 8.5431 8.5432 8.5441 8.5442
    8.5451 8.5452 8.5461 8.5462 8.5471 8.5472 8.5481 8.5482 8.5483 8.5484 8.5485 8.5486 8.5487 8.5488
    8.5489 8.5491 8.5492 8.5501 8.5502 8.5518 8.5519 8.5521 8.5522 8.5523 8.5524 8.5525 8.5526 8.5527
    8.5528 8.5529 8.5531 8.5532 8.5533 8.5534 8.5535 8.5536 8.5537 8.5538 8.5539 8.5541 8.5542 8.5551
    8.5552 8.5561 8.5562 8.5571 8.5572 8.5581 8.5582 8.5591 8.5592 8.5601 8.5602 8.5603 8.5604 8.5605
    8.5606 8.5607 8.5608 8.5609 8.5611 8.5612 8.5621 8.5622 8.5631 8.5632 8.5633 8.5634 8.5635 8.5636
    8.5637 8.5638 8.5639 8.5641 8.5642 8.5651 8.5652 8.5653 8.5654 8.5655 8.5656 8.5657 8.5658 8.5659
    8.5661 8.5662 8.5671 8.5672 8.5681 8.5682 8.5691 8.5692 8.5701 8.5702 8.5703 8.5704 8.5705 8.5706
    8.5707 8.5708 8.5709 8.5711 8.5712 8.5721 8.5722 8.5731 8.5732 8.5741 8.5742 8.5743 8.5744 8.5745
    8.5746 8.5747 8.5748 8.5749 8.5751 8.5752 8.5761 8.5762 8.5771 8.5772 8.5781 8.5782 8.5783 8.5784
    8.5785 8.5786 8.5787 8.5788 8.5789 8.5791 8.5792 8.5801 8.5802 8.5811 8.5812 8.5821 8.5822 8.5831
    8.5832 8.5841 8.5842 8.5851 8.5852 8.5861 8.5862 8.5863 8.5864 8.5865 8.5866 8.5867 8.5868 8.5869
    8.5871 8.5872 8.5881 8.5882 8.5891 8.5892 8.5901 8.5902 8.5911 8.5912 8.5913 8.5914 8.5915 8.5916
    8.5917 8.5918 8.5919 8.5921 8.5922 8.5931 8.5932 8.5941 8.5942 8.5951 8.5952 8.5961 8.5962 8.5971
    8.5972 8.5981 8.5982 8.5983 8.5984 8.5985 8.5986 8.5987 8.5988 8.5989 8.5991 8.5992 8.6001 8.6002
    8.6018 8.6019 8.6021 8.6022 8.6023 8.6024 8.6025 8.6026 8.6027 8.6028 8.6029 8.6031 8.6032 8.6033
    8.6034 8.6035 8.6036 8.6037 8.6038 8.6039 8.6041 8.6042 8.6051 8.6052 8.6061 8.6062 8.6071 8.6072
    8.6081 8.6082 8.6091 8.6092 8.6101 8.6102 8.6103 8.6104 8.6105 8.6106 8.6107 8.6108 8.6109 8.6111
    8.6112 8.6121 8.6122 8.6131 8.6132 8.6133 8.6134 8.6135 8.6136 8.6137 8.6138 8.6139 8.6141 8.6142
    8.6151 8.6152 8.6153 8.6154 8.6155 8.6156 8.6157 8.6158 8.6159 8.6161 8.6162 8.6171 8.6172 8.6181
    8.6182 8.6191 8.6192 8.6201 8.6202 8.6203 8.6204 8.6205 8.6206 8.6207 8.6208 8.6209 8.6211 8.6212
    8.6221 8.6222 8.6231 8.6232 8.6241 8.6242 8.6243 8.6244 8.6245 8.6246 8.6247 8.6248 8.6249 8.6251
    8.6252 8.6261 8.6262 8.6271 8.6272 8.6281 8.6282 8.6283 8.6284 8.6285 8.6286 8.6287 8.6288 8.6289
    8.6291 8.6292 8.6301 8.6302 8.6311 8.6312 8.6321 8.6322 8.6331 8.6332 8.6341 8.6342 8.6351 8.6352
    8.6361 8.6362 8.6363 8.6364 8.6365 8.6366 8.6367 8.6368 8.6369 8.6371 8.6372 8.6381 8.6382 8.6391
    8.6392 8.6401 8.6402 8.6411 8.6412 8.6413 8.6414 8.6415 8.6416 8.6417 8.6418 8.6419 8.6421 8.6422
    8.6431 8.6432 8.6441 8.6442 8.6451 8.6452 8.6461 8.6462 8.6471 8.6472 8.6481 8.6482 8.6483 8.6484
    8.6485 8.6486 8.6487 8.6488 8.6489 8.6491 8.6492 8.6501 8.6502 8.6518 8.6519 8.6521 8.6522 8.6523
    8.6524 8.6525 8.6526 8.6527 8.6528 8.6529 8.6531 8.6532 8.6533 8.6534 8.6535 8.6536 8.6537 8.6538
    8.6539 8.6541 8.6542 8.6551 8.6552 8.6561 8.6562 8.6571 8.6572 8.6581 8.6582 8.6591 8.6592 8.6601
    8.6602 8.6603 8.6604 8.6605 8.6606 8.6607 8.6608 8.6609 8.6611 8.6612 8.6621 8.6622 8.6631 8.6632
    8.6633 8.6634 8.6635 8.6636 8.6637 8.6638 8.6639 8.6641 8.6642 8.6651 8.6652 8.6653 8.6654 8.6655
    8.6656 8.6657 8.6658 8.6659 8.6661 8.6662 8.6671 8.6672 8.6681 8.6682 8.6691 8.6692 8.6701 8.6702
    8.6703 8.6704 8.6705 8.6706 8.6707 8.6708 8.6709 8.6711 8.6712 8.6721 8.6722 8.6731 8.6732 8.6741
    8.6742 8.6743 8.6744 8.6745 8.6746 8.6747 8.6748 8.6749 8.6751 8.6752 8.6761 8.6762 8.6771 8.6772
    8.6781 8.6782 8.6783 8.6784 8.6785 8.6786 8.6787 8.6788 8.6789 8.6791 8.6792 8.6801 8.6802 8.6811
    8.6812 8.6821 8.6822 8.6831 8.6832 8.6841 8.6842 8.6851 8.6852 8.6861 8.6862 8.6863 8.6864 8.6865
    8.6866 8.6867 8.6868 8.6869 8.6871 8.6872 8.6881 8.6882 8.6891 8.6892 8.6901 8.6902 8.6911 8.6912
    8.6913 8.6914 8.6915 8.6916 8.6917 8.6918 8.6919 8.6921 8.6922 8.6931 8.6932 8.6941 8.6942 8.6951
    8.6952 8.6961 8.6962 8.6971 8.6972 8.6981 8.6982 8.6983 8.6984 8.6985 8.6986 8.6987 8.6988 8.6989
    8.6991 8.6992 8.7001 8.7002 8.7018 8.7019 8.7021 8.7022 8.7023 8.7024 8.7025 8.7026 8.7027 8.7028
    8.7029 8.7031 8.7032 8.7033 8.7034 8.7035 8.7036 8.7037 8.7038 8.7039 8.7041 8.7042 8.7051 8.7052
    8.7061 8.7062 8.7071 8.7072 8.7081 8.7082 8.7091 8.7092 8.7101 8.7102 8.7103 8.7104 8.7105 8.7106
    8.7107 8.7108 8.7109 8.7111 8.7112 8.7121 8.7122 8.7131 8.7132 8.7133 8.7134 8.7135 8.7136 8.7137
    8.7138 8.7139 8.7141 8.7142 8.7151 8.7152 8.7153 8.7154 8.7155 8.7156 8.7157 8.7158 8.7159 8.7161
    8.7162 8.7171 8.7172 8.7181 8.7182 8.7191 8.7192 8.7201 8.7202 8.7203 8.7204 8.7205 8.7206 8.7207
    8.7208 8.7209 8.7211 8.7212 8.7221 8.7222 8.7231 8.7232 8.7241 8.7242 8.7243 8.7244 8.7245 8.7246
    8.7247 8.7248 8.7249 8.7251 8.7252 8.7261 8.7262 8.7271 8.7272 8.7281 8.7282 8.7283 8.7284 8.7285
    8.7286 8.7287 8.7288 8.7289 8.7291 8.7292 8.7301 8.7302 8.7311 8.7312 8.7321 8.7322 8.7331 8.7332
    8.7341 8.7342 8.7351 8.7352 8.7361 8.7362 8.7363 8.7364 8.7365 8.7366 8.7367 8.7368 8.7369 8.7371
    8.7372 8.7381 8.7382 8.7391 8.7392 8.7401 8.7402 8.7411 8.7412 8.7413 8.7414 8.7415 8.7416 8.7417
    8.7418 8.7419 8.7421 8.7422 8.7431 8.7432 8.7441 8.7442 8.7451 8.7452 8.7461 8.7462 8.7471 8.7472
    8.7481 8.7482 8.7483 8.7484 8.7485 8.7486 8.7487 8.7488 8.7489 8.7491 8.7492 8.7501 8.7502 8.7518
    8.7519 8.7521 8.7522 8.7523 8.7524 8.7525 8.7526 8.7527 8.7528 8.7529 8.7531 8.7532 8.7533 8.7534
    8.7535 8.7536 8.7537 8.7538 8.7539 8.7541 8.7542 8.7551 8.7552 8.7561 8.7562 8.7571 8.7572 8.7581
    8.7582 8.7591 8.7592 8.7601 8.7602 8.7603 8.7604 8.7605 8.7606 8.7607 8.7608 8.7609 8.7611 8.7612
    8.7621 8.7622 8.7631 8.7632 8.7633 8.7634 8.7635 8.7636 8.7637 8.7638 8.7639 8.7641 8.7642 8.7651
    8.7652 8.7653 8.7654 8.7655 8.7656 8.7657 8.7658 8.7659 8.7661 8.7662 8.7671 8.7672 8.7681 8.7682
    8.7691 8.7692 8.7701 8.7702 8.7703 8.7704 8.7705 8.7706 8.7707 8.7708 8.7709 8.7711 8.7712 8.7721
    8.7722 8.7731 8.7732 8.7741 8.7742 8.7743 8.7744 8.7745 8.7746 8.7747 8.7748 8.7749 8.7751 8.7752
    8.7761 8.7762 8.7771 8.7772 8.7781 8.7782 8.7783 8.7784 8.7785 8.7786 8.7787 8.7788 8.7789 8.7791
    8.7792 8.7801 8.7802 8.7811 8.7812 8.7821 8.7822 8.7831 8.7832 8.7841 8.7842 8.7851 8.7852 8.7861
    8.7862 8.7863 8.7864 8.7865 8.7866 8.7867 8.7868 8.7869 8.7871 8.7872 8.7881 8.7882 8.7891 8.7892
    8.7901 8.7902 8.7911 8.7912 8.7913 8.7914 8.7915 8.7916 8.7917 8.7918 8.7919 8.7921 8.7922 8.7931
    8.7932 8.7941 8.7942 8.7951 8.7952 8.7961 8.7962 8.7971 8.7972 8.7981 8.7982 8.7983 8.7984 8.7985
    8.7986 8.7987 8.7988 8.7989 8.7991 8.7992 8.8001 8.8002 8.8018 8.8019 8.8021 8.8022 8.8023 8.8024
    8.8025 8.8026 8.8027 8.8028 8.8029 8.8031 8.8032 8.8033 8.8034 8.8035 8.8036 8.8037 8.8038 8.8039
    8.8041 8.8042 8.8051 8.8052 8.8061 8.8062 8.8071 8.8072 8.8081 8.8082 8.8091 8.8092 8.8101 8.8102
    8.8103 8.8104 8.8105 8.8106 8.8107 8.8108 8.8109 8.8111 8.8112 8.8121 8.8122 8.8131 8.8132 8.8133
    8.8134 8.8135 8.8136 8.8137 8.8138 8.8139 8.8141 8.8142 8.8151 8.8152 8.8153 8.8154 8.8155 8.8156
    8.8157 8.8158 8.8159 8.8161 8.8162 8.8171 8.8172 8.8181 8.8182 8.8191 8.8192 8.8201 8.8202 8.8203
    8.8204 8.8205 8.8206 8.8207 8.8208 8.8209 8.8211 8.8212 8.8221 8.8222 8.8231 8.8232 8.8241 8.8242
    8.8243 8.8244 8.8245 8.8246 8.8247 8.8248 8.8249 8.8251 8.8252 8.8261 8.8262 8.8271 8.8272 8.8281
    8.8282 8.8283 8.8284 8.8285 8.8286 8.8287 8.8288 8.8289 8.8291 8.8292 8.8301 8.8302 8.8311 8.8312
    8.8321 8.8322 8.8331 8.8332 8.8341 8.8342 8.8351 8.8352 8.8361 8.8362 8.8363 8.8364 8.8365 8.8366
    8.8367 8.8368 8.8369 8.8371 8.8372 8.8381 8.8382 8.8391 8.8392 8.8401 8.8402 8.8411 8.8412 8.8413
    8.8414 8.8415 8.8416 8.8417 8.8418 8.8419 8.8421 8.8422 8.8431 8.8432 8.8441 8.8442 8.8451 8.8452
    8.8461 8.8462 8.8471 8.8472 8.8481 8.8482 8.8483 8.8484 8.8485 8.8486 8.8487 8.8488 8.8489 8.8491
    8.8492 8.8501 8.8502 8.8518 8.8519 8.8521 8.8522 8.8523 8.8524 8.8525 8.8526 8.8527 8.8528 8.8529
    8.8531 8.8532 8.8533 8.8534 8.8535 8.8536 8.8537 8.8538 8.8539 8.8541 8.8542 8.8551 8.8552 8.8561
    8.8562 8.8571 8.8572 8.8581 8.8582 8.8591 8.8592 8.8601 8.8602 8.8603 8.8604 8.8605 8.8606 8.8607
    8.8608 8.8609 8.8611 8.8612 8.8621 8.8622 8.8631 8.8632 8.8633 8.8634 8.8635 8.8636 8.8637 8.8638
    8.8639 8.8641 8.8642 8.8651 8.8652 8.8653 8.8654 8.8655 8.8656 8.8657 8.8658 8.8659 8.8661 8.8662
    8.8671 8.8672 8.8681 8.8682 8.8691 8.8692 8.8701 8.8702 8.8703 8.8704 8.8705 8.8706 8.8707 8.8708
    8.8709 8.8711 8.8712 8.8721 8.8722 8.8731 8.8732 8.8741 8.8742 8.8743 8.8744 8.8745 8.8746 8.8747
    8.8748 8.8749 8.8751 8.8752 8.8761 8.8762 8.8771 8.8772 8.8781 8.8782 8.8783 8.8784 8.8785 8.8786
    8.8787 8.8788 8.8789 8.8791 8.8792 8.8801 8.8802 8.8811 8.8812 8.8821 8.8822 8.8831 8.8832 8.8841
    8.8842 8.8851 8.8852 8.8861 8.8862 8.8863 8.8864 8.8865 8.8866 8.8867 8.8868 8.8869 8.8871 8.8872
    8.8881 8.8882 8.8891 8.8892 8.8901 8.8902 8.8911 8.8912 8.8913 8.8914 8.8915 8.8916 8.8917 8.8918
    8.8919 8.8921 8.8922 8.8931 8.8932 8.8941 8.8942 8.8951 8.8952 8.8961 8.8962 8.8971 8.8972 8.8981
    8.8982 8.8983 8.8984 8.8985 8.8986 8.8987 8.8988 8.8989 8.8991 8.8992 8.9001 8.9002 8.9018 8.9019
    8.9021 8.9022 8.9023 8.9024 8.9025 8.9026 8.9027 8.9028 8.9029 8.9031 8.9032 8.9033 8.9034 8.9035
    8.9036 8.9037 8.9038 8.9039 8.9041 8.9042 8.9051 8.9052 8.9061 8.9062 8.9071 8.9072 8.9081 8.9082
    8.9091 8.9092 8.9101 8.9102 8.9103 8.9104 8.9105 8.9106 8.9107 8.9108 8.9109 8.9111 8.9112 8.9121
    8.9122 8.9131 8.9132 8.9133 8.9134 8.9135 8.9136 8.9137 8.9138 8.9139 8.9141 8.9142 8.9151 8.9152
    8.9153 8.9154 8.9155 8.9156 8.9157 8.9158 8.9159 8.9161 8.9162 8.9171 8.9172 8.9181 8.9182 8.9191
    8.9192 8.9201 8.9202 8.9203 8.9204 8.9205 8.9206 8.9207 8.9208 8.9209 8.9211 8.9212 8.9221 8.9222
    8.9231 8.9232 8.9241 8.9242 8.9243 8.9244 8.9245 8.9246 8.9247 8.9248 8.9249 8.9251 8.9252 8.9261
    8.9262 8.9271 8.9272 8.9281 8.9282 8.9283 8.9284 8.9285 8.9286 8.9287 8.9288 8.9289 8.9291 8.9292
    8.9301 8.9302 8.9311 8.9312 8.9321 8.9322 8.9331 8.9332 8.9341 8.9342 8.9351 8.9352 8.9361 8.9362
    8.9363 8.9364 8.9365 8.9366 8.9367 8.9368 8.9369 8.9371 8.9372 8.9381 8.9382 8.9391 8.9392 8.9401
    8.9402 8.9411 8.9412 8.9413 8.9414 8.9415 8.9416 8.9417 8.9418 8.9419 8.9421 8.9422 8.9431 8.9432
    8.9441 8.9442 8.9451 8.9452 8.9461 8.9462 8.9471 8.9472 8.9481 8.9482 8.9483 8.9484 8.9485 8.9486
    8.9487 8.9488 8.9489 8.9491 8.9492 8.9501 8.9502 8.9518 8.9519 8.9521 8.9522 8.9523 8.9524 8.9525
    8.9526 8.9527 8.9528 8.9529 8.9531 8.9532 8.9533 8.9534 8.9535 8.9536 8.9537 8.9538 8.9539 8.9541
    8.9542 8.9551 8.9552 8.9561 8.9562 8.9571 8.9572 8.9581 8.9582 8.9591 8.9592 8.9601 8.9602 8.9603
    8.9604 8.9605 8.9606 8.9607 8.9608 8.9609 8.9611 8.9612 8.9621 8.9622 8.9631 8.9632 8.9633 8.9634
    8.9635 8.9636 8.9637 8.9638 8.9639 8.9641 8.9642 8.9651 8.9652 8.9653 8.9654 8.9655 8.9656 8.9657
    8.9658 8.9659 8.9661 8.9662 8.9671 8.9672 8.9681 8.9682 8.9691 8.9692 8.9701 8.9702 8.9703 8.9704
    8.9705 8.9706 8.9707 8.9708 8.9709 8.9711 8.9712 8.9721 8.9722 8.9731 8.9732 8.9741 8.9742 8.9743
    8.9744 8.9745 8.9746 8.9747 8.9748 8.9749 8.9751 8.9752 8.9761 8.9762 8.9771 8.9772 8.9781 8.9782
    8.9783 8.9784 8.9785 8.9786 8.9787 8.9788 8.9789 8.9791 8.9792 8.9801 8.9802 8.9811 8.9812 8.9821
    8.9822 8.9831 8.9832 8.9841 8.9842 8.9851 8.9852 8.9861 8.9862 8.9863 8.9864 8.9865 8.9866 8.9867
    8.9868 8.9869 8.9871 8.9872 8.9881 8.9882 8.9891 8.9892 8.9901 8.9902 8.9911 8.9912 8.9913 8.9914
    8.9915 8.9916 8.9917 8.9918 8.9919 8.9921 8.9922 8.9931 8.9932 8.9941 8.9942 8.9951 8.9952 8.9961
    8.9962 8.9971 8.9972 8.9981 8.9982 8.9983 8.9984 8.9985 8.9986 8.9987 8.9988 8.9989 8.9991 8.9992

    9.0001 9.0002 9.0018 9.0019 9.0021 9.0022 9.0023 9.0024 9.0025 9.0026 9.0027 9.0028 9.0029 9.0031
    9.0032 9.0033 9.0034 9.0035 9.0036 9.0037 9.0038 9.0039 9.0041 9.0042 9.0051 9.0052 9.0061 9.0062
    9.0071 9.0072 9.0081 9.0082 9.0091 9.0092 9.0101 9.0102 9.0103 9.0104 9.0105 9.0106 9.0107 9.0108
    9.0109 9.0111 9.0112 9.0121 9.0122 9.0131 9.0132 9.0133 9.0134 9.0135 9.0136 9.0137 9.0138 9.0139
    9.0141 9.0142 9.0151 9.0152 9.0153 9.0154 9.0155 9.0156 9.0157 9.0158 9.0159 9.0161 9.0162 9.0171
    9.0172 9.0181 9.0182 9.0191 9.0192 9.0201 9.0202 9.0203 9.0204 9.0205 9.0206 9.0207 9.0208 9.0209
    9.0211 9.0212 9.0221 9.0222 9.0231 9.0232 9.0241 9.0242 9.0243 9.0244 9.0245 9.0246 9.0247 9.0248
    9.0249 9.0251 9.0252 9.0261 9.0262 9.0271 9.0272 9.0281 9.0282 9.0283 9.0284 9.0285 9.0286 9.0287
    9.0288 9.0289 9.0291 9.0292 9.0301 9.0302 9.0311 9.0312 9.0321 9.0322 9.0331 9.0332 9.0341 9.0342
    9.0351 9.0352 9.0361 9.0362 9.0363 9.0364 9.0365 9.0366 9.0367 9.0368 9.0369 9.0371 9.0372 9.0381
    9.0382 9.0391 9.0392 9.0401 9.0402 9.0411 9.0412 9.0413 9.0414 9.0415 9.0416 9.0417 9.0418 9.0419
    9.0421 9.0422 9.0431 9.0432 9.0441 9.0442 9.0451 9.0452 9.0461 9.0462 9.0471 9.0472 9.0481 9.0482
    9.0483 9.0484 9.0485 9.0486 9.0487 9.0488 9.0489 9.0491 9.0492 9.0493 9.0494 9.0495 9.0496 9.0497
    9.0498 9.0499 9.0501 9.0502 9.0518 9.0519 9.0521 9.0522 9.0523 9.0524 9.0525 9.0526 9.0527 9.0528
    9.0529 9.0531 9.0532 9.0533 9.0534 9.0535 9.0536 9.0537 9.0538 9.0539 9.0541 9.0542 9.0551 9.0552
    9.0561 9.0562 9.0571 9.0572 9.0581 9.0582 9.0591 9.0592 9.0601 9.0602 9.0603 9.0604 9.0605 9.0606
    9.0607 9.0608 9.0609 9.0611 9.0612 9.0621 9.0622 9.0631 9.0632 9.0633 9.0634 9.0635 9.0636 9.0637
    9.0638 9.0639 9.0641 9.0642 9.0651 9.0652 9.0653 9.0654 9.0655 9.0656 9.0657 9.0658 9.0659 9.0661
    9.0662 9.0671 9.0672 9.0681 9.0682 9.0691 9.0692 9.0701 9.0702 9.0703 9.0704 9.0705 9.0706 9.0707
    9.0708 9.0709 9.0711 9.0712 9.0721 9.0722 9.0731 9.0732 9.0741 9.0742 9.0743 9.0744 9.0745 9.0746
    9.0747 9.0748 9.0749 9.0751 9.0752 9.0761 9.0762 9.0771 9.0772 9.0781 9.0782 9.0783 9.0784 9.0785
    9.0786 9.0787 9.0788 9.0789 9.0791 9.0792 9.0801 9.0802 9.0811 9.0812 9.0821 9.0822 9.0831 9.0832
    9.0841 9.0842 9.0851 9.0852 9.0861 9.0862 9.0863 9.0864 9.0865 9.0866 9.0867 9.0868 9.0869 9.0871
    9.0872 9.0881 9.0882 9.0891 9.0892 9.0901 9.0902 9.0911 9.0912 9.0913 9.0914 9.0915 9.0916 9.0917
    9.0918 9.0919 9.0921 9.0922 9.0931 9.0932 9.0941 9.0942 9.0951 9.0952 9.0961 9.0962 9.0971 9.0972
    9.0981 9.0982 9.0983 9.0984 9.0985 9.0986 9.0987 9.0988 9.0989 9.0991 9.0992 9.0993 9.0994 9.0995
    9.0996 9.0997 9.0998 9.0999 9.1001 9.1002 9.1011 9.1012 9.1013 9.1014 9.1015 9.1016 9.1017 9.1018
    9.1019 9.1021 9.1022 9.1023 9.1024 9.1025 9.1026 9.1027 9.1028 9.1029 9.1031 9.1032 9.1033 9.1034
    9.1035 9.1036 9.1037 9.1038 9.1039 9.1041 9.1042 9.1043 9.1044 9.1045 9.1046 9.1047 9.1048 9.1049
    9.1051 9.1052 9.1053 9.1054 9.1055 9.1056 9.1057 9.1058 9.1059 9.1061 9.1062 9.1063 9.1064 9.1065
    9.1066 9.1067 9.1068 9.1069 9.1071 9.1072 9.1073 9.1074 9.1075 9.1076 9.1077 9.1078 9.1079 9.1081
    9.1082 9.1083 9.1084 9.1085 9.1086 9.1087 9.1088 9.1089 9.1091 9.1092 9.1093 9.1094 9.1095 9.1096
    9.1097 9.1098 9.1099 9.1101 9.1102 9.1103 9.1104 9.1105 9.1106 9.1107 9.1108 9.1109 9.1111 9.1112
    9.1113 9.1114 9.1115 9.1116 9.1117 9.1118 9.1119 9.1121 9.1122 9.1123 9.1124 9.1125 9.1126 9.1127
    9.1128 9.1129 9.1131 9.1132 9.1133 9.1134 9.1135 9.1136 9.1137 9.1138 9.1139 9.1141 9.1142 9.1143
    9.1144 9.1145 9.1146 9.1147 9.1148 9.1149 9.1151 9.1152 9.1153 9.1154 9.1155 9.1156 9.1157 9.1158
    9.1159 9.1161 9.1162 9.1163 9.1164 9.1165 9.1166 9.1167 9.1168 9.1169 9.1171 9.1172 9.1173 9.1174
    9.1175 9.1176 9.1177 9.1178 9.1179 9.1181 9.1182 9.1183 9.1184 9.1185 9.1186 9.1187 9.1188 9.1189
    9.1191 9.1192 9.1193 9.1194 9.1195 9.1196 9.1197 9.1198 9.1199 9.1201 9.1202 9.1203 9.1204 9.1205
    9.1206 9.1207 9.1208 9.1209 9.1211 9.1212 9.1213 9.1214 9.1215 9.1216 9.1217 9.1218 9.1219 9.1221
    9.1222 9.1223 9.1224 9.1225 9.1226 9.1227 9.1228 9.1229 9.1231 9.1232 9.1233 9.1234 9.1235 9.1236
    9.1237 9.1238 9.1239 9.1241 9.1242 9.1243 9.1244 9.1245 9.1246 9.1247 9.1248 9.1249 9.1251 9.1252
    9.1261 9.1262 9.1263 9.1264 9.1265 9.1266 9.1267 9.1268 9.1269 9.1271 9.1272 9.1273 9.1274 9.1275
    9.1276 9.1277 9.1278 9.1279 9.1281 9.1282 9.1283 9.1284 9.1285 9.1286 9.1287 9.1288 9.1289 9.1291
    9.1292 9.1293 9.1294 9.1295 9.1296 9.1297 9.1298 9.1299 9.1301 9.1302 9.1303 9.1304 9.1305 9.1306
    9.1307 9.1308 9.1309 9.1311 9.1312 9.1313 9.1314 9.1315 9.1316 9.1317 9.1318 9.1319 9.1321 9.1322
    9.1323 9.1324 9.1325 9.1326 9.1327 9.1328 9.1329 9.1331 9.1332 9.1333 9.1334 9.1335 9.1336 9.1337
    9.1338 9.1339 9.1341 9.1342 9.1343 9.1344 9.1345 9.1346 9.1347 9.1348 9.1349 9.1351 9.1352 9.1361
    9.1362 9.1363 9.1364 9.1365 9.1366 9.1367 9.1368 9.1369 9.1371 9.1372 9.1373 9.1374 9.1375 9.1376
    9.1377 9.1378 9.1379 9.1381 9.1382 9.1383 9.1384 9.1385 9.1386 9.1387 9.1388 9.1389 9.1391 9.1392
    9.1393 9.1394 9.1395 9.1396 9.1397 9.1398 9.1399 9.1401 9.1402 9.1403 9.1404 9.1405 9.1406 9.1407
    9.1408 9.1409 9.1411 9.1412 9.1413 9.1414 9.1415 9.1416 9.1417 9.1418 9.1419 9.1421 9.1422 9.1423
    9.1424 9.1425 9.1426 9.1427 9.1428 9.1429 9.1431 9.1432 9.1433 9.1434 9.1435 9.1436 9.1437 9.1438
    9.1439 9.1441 9.1442 9.1443 9.1444 9.1445 9.1446 9.1447 9.1448 9.1449 9.1451 9.1452 9.1453 9.1454
    9.1455 9.1456 9.1457 9.1458 9.1459 9.1461 9.1462 9.1463 9.1464 9.1465 9.1466 9.1467 9.1468 9.1469
    9.1471 9.1472 9.1473 9.1474 9.1475 9.1476 9.1477 9.1478 9.1479 9.1481 9.1482 9.1483 9.1484 9.1485
    9.1486 9.1487 9.1488 9.1489 9.1491 9.1492 9.1501 9.1502 9.1511 9.1512 9.1513 9.1514 9.1515 9.1516
    9.1517 9.1518 9.1519 9.1521 9.1522 9.1523 9.1524 9.1525 9.1526 9.1527 9.1528 9.1529 9.1531 9.1532
    9.1533 9.1534 9.1535 9.1536 9.1537 9.1538 9.1539 9.1541 9.1542 9.1543 9.1544 9.1545 9.1546 9.1547
    9.1548 9.1549 9.1551 9.1552 9.1553 9.1554 9.1555 9.1556 9.1557 9.1558 9.1559 9.1561 9.1562 9.1563
    9.1564 9.1565 9.1566 9.1567 9.1568 9.1569 9.1571 9.1572 9.1573 9.1574 9.1575 9.1576 9.1577 9.1578
    9.1579 9.1581 9.1582 9.1583 9.1584 9.1585 9.1586 9.1587 9.1588 9.1589 9.1591 9.1592 9.1593 9.1594
    9.1595 9.1596 9.1597 9.1598 9.1599 9.1601 9.1602 9.1611 9.1612 9.1613 9.1614 9.1615 9.1616 9.1617
    9.1618 9.1619 9.1621 9.1622 9.1623 9.1624 9.1625 9.1626 9.1627 9.1628 9.1629 9.1631 9.1632 9.1633
    9.1634 9.1635 9.1636 9.1637 9.1638 9.1639 9.1641 9.1642 9.1643 9.1644 9.1645 9.1646 9.1647 9.1648
    9.1649 9.1651 9.1652 9.1653 9.1654 9.1655 9.1656 9.1657 9.1658 9.1659 9.1661 9.1662 9.1663 9.1664
    9.1665 9.1666 9.1667 9.1668 9.1669 9.1671 9.1672 9.1673 9.1674 9.1675 9.1676 9.1677 9.1678 9.1679
    9.1681 9.1682 9.1683 9.1684 9.1685 9.1686 9.1687 9.1688 9.1689 9.1691 9.1692 9.1693 9.1694 9.1695
    9.1696 9.1697 9.1698 9.1699 9.1701 9.1702 9.1703 9.1704 9.1705 9.1706 9.1707 9.1708 9.1709 9.1711
    9.1712 9.1713 9.1714 9.1715 9.1716 9.1717 9.1718 9.1719 9.1721 9.1722 9.1723 9.1724 9.1725 9.1726
    9.1727 9.1728 9.1729 9.1731 9.1732 9.1733 9.1734 9.1735 9.1736 9.1737 9.1738 9.1739 9.1741 9.1742
    9.1751 9.1752 9.1761 9.1762 9.1763 9.1764 9.1765 9.1766 9.1767 9.1768 9.1769 9.1771 9.1772 9.1773
    9.1774 9.1775 9.1776 9.1777 9.1778 9.1779 9.1781 9.1782 9.1783 9.1784 9.1785 9.1786 9.1787 9.1788
    9.1789 9.1791 9.1792 9.1793 9.1794 9.1795 9.1796 9.1797 9.1798 9.1799 9.1801 9.1802 9.1803 9.1804
    9.1805 9.1806 9.1807 9.1808 9.1809 9.1811 9.1812 9.1813 9.1814 9.1815 9.1816 9.1817 9.1818 9.1819
    9.1821 9.1822 9.1823 9.1824 9.1825 9.1826 9.1827 9.1828 9.1829 9.1831 9.1832 9.1833 9.1834 9.1835
    9.1836 9.1837 9.1838 9.1839 9.1841 9.1842 9.1851 9.1852 9.1861 9.1862 9.1863 9.1864 9.1865 9.1866
    9.1867 9.1868 9.1869 9.1871 9.1872 9.1873 9.1874 9.1875 9.1876 9.1877 9.1878 9.1879 9.1881 9.1882
    9.1883 9.1884 9.1885 9.1886 9.1887 9.1888 9.1889 9.1891 9.1892 9.1893 9.1894 9.1895 9.1896 9.1897
    9.1898 9.1899 9.1901 9.1902 9.1903 9.1904 9.1905 9.1906 9.1907 9.1908 9.1909 9.1911 9.1912 9.1913
    9.1914 9.1915 9.1916 9.1917 9.1918 9.1919 9.1921 9.1922 9.1923 9.1924 9.1925 9.1926 9.1927 9.1928
    9.1929 9.1931 9.1932 9.1933 9.1934 9.1935 9.1936 9.1937 9.1938 9.1939 9.1941 9.1942 9.1943 9.1944
    9.1945 9.1946 9.1947 9.1948 9.1949 9.1951 9.1952 9.1953 9.1954 9.1955 9.1956 9.1957 9.1958 9.1959
    9.1961 9.1962 9.1963 9.1964 9.1965 9.1966 9.1967 9.1968 9.1969 9.1971 9.1972 9.1973 9.1974 9.1975
    9.1976 9.1977 9.1978 9.1979 9.1981 9.1982 9.1983 9.1984 9.1985 9.1986 9.1987 9.1988 9.1989 9.1991
    9.1992 9.2001 9.2002 9.2018 9.2019 9.2021 9.2022 9.2023 9.2024 9.2025 9.2026 9.2027 9.2028 9.2029
    9.2031 9.2032 9.2033 9.2034 9.2035 9.2036 9.2037 9.2038 9.2039 9.2041 9.2042 9.2051 9.2052 9.2061
    9.2062 9.2071 9.2072 9.2081 9.2082 9.2091 9.2092 9.2101 9.2102 9.2103 9.2104 9.2105 9.2106 9.2107
    9.2108 9.2109 9.2111 9.2112 9.2121 9.2122 9.2131 9.2132 9.2133 9.2134 9.2135 9.2136 9.2137 9.2138
    9.2139 9.2141 9.2142 9.2151 9.2152 9.2153 9.2154 9.2155 9.2156 9.2157 9.2158 9.2159 9.2161 9.2162
    9.2171 9.2172 9.2181 9.2182 9.2191 9.2192 9.2201 9.2202 9.2203 9.2204 9.2205 9.2206 9.2207 9.2208
    9.2209 9.2211 9.2212 9.2221 9.2222 9.2231 9.2232 9.2241 9.2242 9.2243 9.2244 9.2245 9.2246 9.2247
    9.2248 9.2249 9.2251 9.2252 9.2271 9.2272 9.2281 9.2282 9.2283 9.2284 9.2285 9.2286 9.2287 9.2288
    9.2289 9.2291 9.2292 9.2301 9.2302 9.2311 9.2312 9.2321 9.2322 9.2331 9.2332 9.2341 9.2342 9.2351
    9.2352 9.2371 9.2372 9.2381 9.2382 9.2391 9.2392 9.2401 9.2402 9.2411 9.2412 9.2421 9.2422 9.2431
    9.2432 9.2441 9.2442 9.2451 9.2452 9.2461 9.2462 9.2471 9.2472 9.2481 9.2482 9.2491 9.2492 9.2521
    9.2522 9.2531 9.2532 9.2541 9.2542 9.2551 9.2552 9.2561 9.2562 9.2571 9.2572 9.2581 9.2582 9.2591
    9.2592 9.2601 9.2602 9.2611 9.2612 9.2621 9.2622 9.2631 9.2632 9.2641 9.2642 9.2651 9.2652 9.2661
    9.2662 9.2671 9.2672 9.2681 9.2682 9.2691 9.2692 9.2701 9.2702 9.2711 9.2712 9.2721 9.2722 9.2731
    9.2732 9.2741 9.2742 9.2751 9.2752 9.2761 9.2762 9.2771 9.2772 9.2781 9.2782 9.2791 9.2792 9.2801
    9.2802 9.2811 9.2812 9.2821 9.2822 9.2831 9.2832 9.2841 9.2842 9.2851 9.2852 9.2861 9.2862 9.2871
    9.2872 9.2881 9.2882 9.2891 9.2892 9.2901 9.2902 9.2911 9.2912 9.2921 9.2922 9.2931 9.2932 9.2941
    9.2942 9.2951 9.2952 9.2961 9.2962 9.2971 9.2972 9.2981 9.2982 9.2983 9.2984 9.2985 9.2986 9.2987
    9.2988 9.2989 9.2991 9.2992 9.3001 9.3002 9.3025 9.3026 9.3027 9.3028 9.3029 9.3031 9.3032 9.3033
    9.3034 9.3035 9.3036 9.3037 9.3038 9.3039 9.3041 9.3042 9.3111 9.3112 9.3141 9.3142 9.3161 9.3162
    9.3211 9.3212 9.3251 9.3252 9.3291 9.3292 9.3371 9.3372 9.3421 9.3422 9.3491 9.3492 9.3501 9.3502
    9.3521 9.3522 9.3531 9.3532 9.3541 9.3542 9.3551 9.3552 9.3561 9.3562 9.3571 9.3572 9.3581 9.3582
    9.3591 9.3592 9.3601 9.3602 9.3611 9.3612 9.3621 9.3622 9.3631 9.3632 9.3641 9.3642 9.3651 9.3652
    9.3661 9.3662 9.3671 9.3672 9.3681 9.3682 9.3691 9.3692 9.3701 9.3702 9.3711 9.3712 9.3721 9.3722
    9.3731 9.3732 9.3741 9.3742 9.3751 9.3752 9.3761 9.3762 9.3771 9.3772 9.3781 9.3782 9.3791 9.3792
    9.3801 9.3802 9.3811 9.3812 9.3821 9.3822 9.3831 9.3832 9.3841 9.3842 9.3851 9.3852 9.3861 9.3862
    9.3871 9.3872 9.3881 9.3882 9.3891 9.3892 9.3901 9.3902 9.3911 9.3912 9.3921 9.3922 9.3931 9.3932
    9.3941 9.3942 9.3951 9.3952 9.3961 9.3962 9.3971 9.3972 9.3981 9.3982 9.3983 9.3984 9.3985 9.3986
    9.3987 9.3988 9.3989 9.3991 9.3992 9.4001 9.4002 9.4011 9.4012 9.4013 9.4014 9.4015 9.4016 9.4017
    9.4018 9.4019 9.4021 9.4022 9.4023 9.4024 9.4025 9.4026 9.4027 9.4028 9.4029 9.4031 9.4032 9.4033
    9.4034 9.4035 9.4036 9.4037 9.4038 9.4039 9.4041 9.4042 9.4043 9.4044 9.4045 9.4046 9.4047 9.4048
    9.4049 9.4051 9.4052 9.4053 9.4054 9.4055 9.4056 9.4057 9.4058 9.4059 9.4061 9.4062 9.4063 9.4064
    9.4065 9.4066 9.4067 9.4068 9.4069 9.4071 9.4072 9.4073 9.4074 9.4075 9.4076 9.4077 9.4078 9.4079
    9.4081 9.4082 9.4083 9.4084 9.4085 9.4086 9.4087 9.4088 9.4089 9.4091 9.4092 9.4093 9.4094 9.4095
    9.4096 9.4097 9.4098 9.4099 9.4101 9.4102 9.4103 9.4104 9.4105 9.4106 9.4107 9.4108 9.4109 9.4111
    9.4112 9.4113 9.4114 9.4115 9.4116 9.4117 9.4118 9.4119 9.4121 9.4122 9.4123 9.4124 9.4125 9.4126
    9.4127 9.4128 9.4129 9.4131 9.4132 9.4133 9.4134 9.4135 9.4136 9.4137 9.4138 9.4139 9.4141 9.4142
    9.4143 9.4144 9.4145 9.4146 9.4147 9.4148 9.4149 9.4151 9.4152 9.4153 9.4154 9.4155 9.4156 9.4157
    9.4158 9.4159 9.4161 9.4162 9.4163 9.4164 9.4165 9.4166 9.4167 9.4168 9.4169 9.4171 9.4172 9.4173
    9.4174 9.4175 9.4176 9.4177 9.4178 9.4179 9.4181 9.4182 9.4183 9.4184 9.4185 9.4186 9.4187 9.4188
    9.4189 9.4191 9.4192 9.4193 9.4194 9.4195 9.4196 9.4197 9.4198 9.4199 9.4201 9.4202 9.4203 9.4204
    9.4205 9.4206 9.4207 9.4208 9.4209 9.4211 9.4212 9.4213 9.4214 9.4215 9.4216 9.4217 9.4218 9.4219
    9.4221 9.4222 9.4223 9.4224 9.4225 9.4226 9.4227 9.4228 9.4229 9.4231 9.4232 9.4233 9.4234 9.4235
    9.4236 9.4237 9.4238 9.4239 9.4241 9.4242 9.4243 9.4244 9.4245 9.4246 9.4247 9.4248 9.4249 9.4251
    9.4252 9.4253 9.4254 9.4255 9.4256 9.4257 9.4258 9.4259 9.4261 9.4262 9.4263 9.4264 9.4265 9.4266
    9.4267 9.4268 9.4269 9.4271 9.4272 9.4273 9.4274 9.4275 9.4276 9.4277 9.4278 9.4279 9.4281 9.4282
    9.4283 9.4284 9.4285 9.4286 9.4287 9.4288 9.4289 9.4291 9.4292 9.4293 9.4294 9.4295 9.4296 9.4297
    9.4298 9.4299 9.4301 9.4302 9.4303 9.4304 9.4305 9.4306 9.4307 9.4308 9.4309 9.4311 9.4312 9.4313
    9.4314 9.4315 9.4316 9.4317 9.4318 9.4319 9.4321 9.4322 9.4323 9.4324 9.4325 9.4326 9.4327 9.4328
    9.4329 9.4331 9.4332 9.4333 9.4334 9.4335 9.4336 9.4337 9.4338 9.4339 9.4341 9.4342 9.4343 9.4344
    9.4345 9.4346 9.4347 9.4348 9.4349 9.4351 9.4352 9.4353 9.4354 9.4355 9.4356 9.4357 9.4358 9.4359
    9.4361 9.4362 9.4363 9.4364 9.4365 9.4366 9.4367 9.4368 9.4369 9.4371 9.4372 9.4373 9.4374 9.4375
    9.4376 9.4377 9.4378 9.4379 9.4381 9.4382 9.4383 9.4384 9.4385 9.4386 9.4387 9.4388 9.4389 9.4391
    9.4392 9.4393 9.4394 9.4395 9.4396 9.4397 9.4398 9.4399 9.4401 9.4402 9.4403 9.4404 9.4405 9.4406
    9.4407 9.4408 9.4409 9.4411 9.4412 9.4413 9.4414 9.4415 9.4416 9.4417 9.4418 9.4419 9.4421 9.4422
    9.4423 9.4424 9.4425 9.4426 9.4427 9.4428 9.4429 9.4431 9.4432 9.4433 9.4434 9.4435 9.4436 9.4437
    9.4438 9.4439 9.4441 9.4442 9.4443 9.4444 9.4445 9.4446 9.4447 9.4448 9.4449 9.4451 9.4452 9.4453
    9.4454 9.4455 9.4456 9.4457 9.4458 9.4459 9.4461 9.4462 9.4463 9.4464 9.4465 9.4466 9.4467 9.4468
    9.4469 9.4471 9.4472 9.4473 9.4474 9.4475 9.4476 9.4477 9.4478 9.4479 9.4480 9.4481 9.4482 9.4483
    9.4484 9.4485 9.4486 9.4487 9.4488 9.4489 9.4491 9.4492 9.4493 9.4494 9.4495 9.4496 9.4497 9.4498
    9.4499 9.4501 9.4502 9.4518 9.4519 9.4520 9.4521 9.4522 9.4523 9.4524 9.4525 9.4526 9.4527 9.4528
    9.4529 9.4530 9.4531 9.4532 9.4533 9.4534 9.4535 9.4536 9.4537 9.4538 9.4539 9.4541 9.4542 9.4551
    9.4552 9.4561 9.4562 9.4571 9.4572 9.4581 9.4582 9.4591 9.4592 9.4601 9.4602 9.4603 9.4604 9.4605
    9.4606 9.4607 9.4608 9.4609 9.4611 9.4612 9.4621 9.4622 9.4631 9.4632 9.4633 9.4634 9.4635 9.4636
    9.4637 9.4638 9.4639 9.4641 9.4642 9.4651 9.4652 9.4653 9.4654 9.4655 9.4656 9.4657 9.4658 9.4659
    9.4661 9.4662 9.4671 9.4672 9.4681 9.4682 9.4691 9.4692 9.4701 9.4702 9.4703 9.4704 9.4705 9.4706
    9.4707 9.4708 9.4709 9.4711 9.4712 9.4721 9.4722 9.4731 9.4732 9.4741 9.4742 9.4743 9.4744 9.4745
    9.4746 9.4747 9.4748 9.4749 9.4751 9.4752 9.4761 9.4762 9.4771 9.4772 9.4781 9.4782 9.4783 9.4784
    9.4785 9.4786 9.4787 9.4788 9.4789 9.4791 9.4792 9.4801 9.4802 9.4811 9.4812 9.4821 9.4822 9.4831
    9.4832 9.4841 9.4842 9.4851 9.4852 9.4861 9.4862 9.4863 9.4864 9.4865 9.4866 9.4867 9.4868 9.4869
    9.4871 9.4872 9.4881 9.4882 9.4891 9.4892 9.4901 9.4902 9.4911 9.4912 9.4913 9.4914 9.4915 9.4916
    9.4917 9.4918 9.4919 9.4921 9.4922 9.4931 9.4932 9.4941 9.4942 9.4951 9.4952 9.4961 9.4962 9.4971
    9.4972 9.4981 9.4982 9.4983 9.4984 9.4985 9.4986 9.4987 9.4988 9.4989 9.4991 9.4992 9.5001 9.5002
    9.5011 9.5012 9.5013 9.5014 9.5015 9.5016 9.5017 9.5018 9.5019 9.5021 9.5022 9.5023 9.5024 9.5025
    9.5026 9.5027 9.5028 9.5029 9.5031 9.5032 9.5033 9.5034 9.5035 9.5036 9.5037 9.5038 9.5039 9.5041
    9.5042 9.5043 9.5044 9.5045 9.5046 9.5047 9.5048 9.5049 9.5051 9.5052 9.5053 9.5054 9.5055 9.5056
    9.5057 9.5058 9.5059 9.5061 9.5062 9.5063 9.5064 9.5065 9.5066 9.5067 9.5068 9.5069 9.5071 9.5072
    9.5073 9.5074 9.5075 9.5076 9.5077 9.5078 9.5079 9.5081 9.5082 9.5083 9.5084 9.5085 9.5086 9.5087
    9.5088 9.5089 9.5091 9.5092 9.5093 9.5094 9.5095 9.5096 9.5097 9.5098 9.5099 9.5101 9.5102 9.5103
    9.5104 9.5105 9.5106 9.5107 9.5108 9.5109 9.5111 9.5112 9.5113 9.5114 9.5115 9.5116 9.5117 9.5118
    9.5119 9.5121 9.5122 9.5123 9.5124 9.5125 9.5126 9.5127 9.5128 9.5129 9.5131 9.5132 9.5133 9.5134
    9.5135 9.5136 9.5137 9.5138 9.5139 9.5141 9.5142 9.5143 9.5144 9.5145 9.5146 9.5147 9.5148 9.5149
    9.5151 9.5152 9.5153 9.5154 9.5155 9.5156 9.5157 9.5158 9.5159 9.5161 9.5162 9.5163 9.5164 9.5165
    9.5166 9.5167 9.5168 9.5169 9.5171 9.5172 9.5173 9.5174 9.5175 9.5176 9.5177 9.5178 9.5179 9.5181
    9.5182 9.5183 9.5184 9.5185 9.5186 9.5187 9.5188 9.5189 9.5191 9.5192 9.5193 9.5194 9.5195 9.5196
    9.5197 9.5198 9.5199 9.5201 9.5202 9.5203 9.5204 9.5205 9.5206 9.5207 9.5208 9.5209 9.5211 9.5212
    9.5213 9.5214 9.5215 9.5216 9.5217 9.5218 9.5219 9.5221 9.5222 9.5223 9.5224 9.5225 9.5226 9.5227
    9.5228 9.5229 9.5231 9.5232 9.5233 9.5234 9.5235 9.5236 9.5237 9.5238 9.5239 9.5241 9.5242 9.5243
    9.5244 9.5245 9.5246 9.5247 9.5248 9.5249 9.5251 9.5252 9.5253 9.5254 9.5255 9.5256 9.5257 9.5258
    9.5259 9.5261 9.5262 9.5263 9.5264 9.5265 9.5266 9.5267 9.5268 9.5269 9.5271 9.5272 9.5273 9.5274
    9.5275 9.5276 9.5277 9.5278 9.5279 9.5281 9.5282 9.5283 9.5284 9.5285 9.5286 9.5287 9.5288 9.5289
    9.5291 9.5292 9.5293 9.5294 9.5295 9.5296 9.5297 9.5298 9.5299 9.5301 9.5302 9.5303 9.5304 9.5305
    9.5306 9.5307 9.5308 9.5309 9.5311 9.5312 9.5313 9.5314 9.5315 9.5316 9.5317 9.5318 9.5319 9.5321
    9.5322 9.5323 9.5324 9.5325 9.5326 9.5327 9.5328 9.5329 9.5331 9.5332 9.5333 9.5334 9.5335 9.5336
    9.5337 9.5338 9.5339 9.5341 9.5342 9.5343 9.5344 9.5345 9.5346 9.5347 9.5348 9.5349 9.5351 9.5352
    9.5353 9.5354 9.5355 9.5356 9.5357 9.5358 9.5359 9.5361 9.5362 9.5363 9.5364 9.5365 9.5366 9.5367
    9.5368 9.5369 9.5371 9.5372 9.5373 9.5374 9.5375 9.5376 9.5377 9.5378 9.5379 9.5381 9.5382 9.5383
    9.5384 9.5385 9.5386 9.5387 9.5388 9.5389 9.5391 9.5392 9.5393 9.5394 9.5395 9.5396 9.5397 9.5398
    9.5399 9.5401 9.5402 9.5403 9.5404 9.5405 9.5406 9.5407 9.5408 9.5409 9.5411 9.5412 9.5413 9.5414
    9.5415 9.5416 9.5417 9.5418 9.5419 9.5421 9.5422 9.5423 9.5424 9.5425 9.5426 9.5427 9.5428 9.5429
    9.5431 9.5432 9.5433 9.5434 9.5435 9.5436 9.5437 9.5438 9.5439 9.5441 9.5442 9.5443 9.5444 9.5445
    9.5446 9.5447 9.5448 9.5449 9.5451 9.5452 9.5453 9.5454 9.5455 9.5456 9.5457 9.5458 9.5459 9.5461
    9.5462 9.5463 9.5464 9.5465 9.5466 9.5467 9.5468 9.5469 9.5471 9.5472 9.5473 9.5474 9.5475 9.5476
    9.5477 9.5478 9.5479 9.5480 9.5481 9.5482 9.5483 9.5484 9.5485 9.5486 9.5487 9.5488 9.5489 9.5491
    9.5492 9.5493 9.5494 9.5495 9.5496 9.5497 9.5498 9.5499 9.5501 9.5502 9.5518 9.5519 9.5520 9.5521
    9.5522 9.5523 9.5524 9.5525 9.5526 9.5527 9.5528 9.5529 9.5530 9.5531 9.5532 9.5533 9.5534 9.5535
    9.5536 9.5537 9.5538 9.5539 9.5541 9.5542 9.5551 9.5552 9.5561 9.5562 9.5571 9.5572 9.5581 9.5582
    9.5591 9.5592 9.5601 9.5602 9.5603 9.5604 9.5605 9.5606 9.5607 9.5608 9.5609 9.5611 9.5612 9.5621
    9.5622 9.5631 9.5632 9.5633 9.5634 9.5635 9.5636 9.5637 9.5638 9.5639 9.5641 9.5642 9.5651 9.5652
    9.5653 9.5654 9.5655 9.5656 9.5657 9.5658 9.5659 9.5661 9.5662 9.5671 9.5672 9.5681 9.5682 9.5691
    9.5692 9.5701 9.5702 9.5703 9.5704 9.5705 9.5706 9.5707 9.5708 9.5709 9.5711 9.5712 9.5721 9.5722
    9.5731 9.5732 9.5741 9.5742 9.5743 9.5744 9.5745 9.5746 9.5747 9.5748 9.5749 9.5751 9.5752 9.5761
    9.5762 9.5771 9.5772 9.5781 9.5782 9.5783 9.5784 9.5785 9.5786 9.5787 9.5788 9.5789 9.5791 9.5792
    9.5801 9.5802 9.5811 9.5812 9.5821 9.5822 9.5831 9.5832 9.5841 9.5842 9.5851 9.5852 9.5861 9.5862
    9.5863 9.5864 9.5865 9.5866 9.5867 9.5868 9.5869 9.5871 9.5872 9.5881 9.5882 9.5891 9.5892 9.5901
    9.5902 9.5911 9.5912 9.5913 9.5914 9.5915 9.5916 9.5917 9.5918 9.5919 9.5921 9.5922 9.5931 9.5932
    9.5941 9.5942 9.5951 9.5952 9.5961 9.5962 9.5971 9.5972 9.5981 9.5982 9.5983 9.5984 9.5985 9.5986
    9.5987 9.5988 9.5989 9.5991 9.5992 9.6001 9.6002 9.6011 9.6012 9.6013 9.6014 9.6015 9.6016 9.6017
    9.6018 9.6019 9.6021 9.6022 9.6023 9.6024 9.6025 9.6026 9.6027 9.6028 9.6029 9.6031 9.6032 9.6033
    9.6034 9.6035 9.6036 9.6037 9.6038 9.6039 9.6041 9.6042 9.6043 9.6044 9.6045 9.6046 9.6047 9.6048
    9.6049 9.6051 9.6052 9.6053 9.6054 9.6055 9.6056 9.6057 9.6058 9.6059 9.6061 9.6062 9.6063 9.6064
    9.6065 9.6066 9.6067 9.6068 9.6069 9.6071 9.6072 9.6073 9.6074 9.6075 9.6076 9.6077 9.6078 9.6079
    9.6081 9.6082 9.6083 9.6084 9.6085 9.6086 9.6087 9.6088 9.6089 9.6091 9.6092 9.6093 9.6094 9.6095
    9.6096 9.6097 9.6098 9.6099 9.6101 9.6102 9.6103 9.6104 9.6105 9.6106 9.6107 9.6108 9.6109 9.6111
    9.6112 9.6113 9.6114 9.6115 9.6116 9.6117 9.6118 9.6119 9.6121 9.6122 9.6123 9.6124 9.6125 9.6126
    9.6127 9.6128 9.6129 9.6131 9.6132 9.6133 9.6134 9.6135 9.6136 9.6137 9.6138 9.6139 9.6141 9.6142
    9.6143 9.6144 9.6145 9.6146 9.6147 9.6148 9.6149 9.6151 9.6152 9.6153 9.6154 9.6155 9.6156 9.6157
    9.6158 9.6159 9.6161 9.6162 9.6163 9.6164 9.6165 9.6166 9.6167 9.6168 9.6169 9.6171 9.6172 9.6173
    9.6174 9.6175 9.6176 9.6177 9.6178 9.6179 9.6181 9.6182 9.6183 9.6184 9.6185 9.6186 9.6187 9.6188
    9.6189 9.6191 9.6192 9.6193 9.6194 9.6195 9.6196 9.6197 9.6198 9.6199 9.6201 9.6202 9.6203 9.6204
    9.6205 9.6206 9.6207 9.6208 9.6209 9.6211 9.6212 9.6213 9.6214 9.6215 9.6216 9.6217 9.6218 9.6219
    9.6221 9.6222 9.6223 9.6224 9.6225 9.6226 9.6227 9.6228 9.6229 9.6231 9.6232 9.6233 9.6234 9.6235
    9.6236 9.6237 9.6238 9.6239 9.6241 9.6242 9.6243 9.6244 9.6245 9.6246 9.6247 9.6248 9.6249 9.6251
    9.6252 9.6253 9.6254 9.6255 9.6256 9.6257 9.6258 9.6259 9.6261 9.6262 9.6263 9.6264 9.6265 9.6266
    9.6267 9.6268 9.6269 9.6271 9.6272 9.6273 9.6274 9.6275 9.6276 9.6277 9.6278 9.6279 9.6281 9.6282
    9.6283 9.6284 9.6285 9.6286 9.6287 9.6288 9.6289 9.6291 9.6292 9.6293 9.6294 9.6295 9.6296 9.6297
    9.6298 9.6299 9.6301 9.6302 9.6303 9.6304 9.6305 9.6306 9.6307 9.6308 9.6309 9.6311 9.6312 9.6313
    9.6314 9.6315 9.6316 9.6317 9.6318 9.6319 9.6321 9.6322 9.6323 9.6324 9.6325 9.6326 9.6327 9.6328
    9.6329 9.6331 9.6332 9.6333 9.6334 9.6335 9.6336 9.6337 9.6338 9.6339 9.6341 9.6342 9.6343 9.6344
    9.6345 9.6346 9.6347 9.6348 9.6349 9.6351 9.6352 9.6353 9.6354 9.6355 9.6356 9.6357 9.6358 9.6359
    9.6361 9.6362 9.6363 9.6364 9.6365 9.6366 9.6367 9.6368 9.6369 9.6371 9.6372 9.6373 9.6374 9.6375
    9.6376 9.6377 9.6378 9.6379 9.6381 9.6382 9.6383 9.6384 9.6385 9.6386 9.6387 9.6388 9.6389 9.6391
    9.6392 9.6393 9.6394 9.6395 9.6396 9.6397 9.6398 9.6399 9.6401 9.6402 9.6403 9.6404 9.6405 9.6406
    9.6407 9.6408 9.6409 9.6411 9.6412 9.6413 9.6414 9.6415 9.6416 9.6417 9.6418 9.6419 9.6421 9.6422
    9.6423 9.6424 9.6425 9.6426 9.6427 9.6428 9.6429 9.6431 9.6432 9.6433 9.6434 9.6435 9.6436 9.6437
    9.6438 9.6439 9.6441 9.6442 9.6443 9.6444 9.6445 9.6446 9.6447 9.6448 9.6449 9.6451 9.6452 9.6453
    9.6454 9.6455 9.6456 9.6457 9.6458 9.6459 9.6461 9.6462 9.6463 9.6464 9.6465 9.6466 9.6467 9.6468
    9.6469 9.6471 9.6472 9.6473 9.6474 9.6475 9.6476 9.6477 9.6478 9.6479 9.6480 9.6481 9.6482 9.6483
    9.6484 9.6485 9.6486 9.6487 9.6488 9.6489 9.6491 9.6492 9.6493 9.6494 9.6495 9.6496 9.6497 9.6498
    9.6499 9.6501 9.6502 9.6518 9.6519 9.6520 9.6521 9.6522 9.6523 9.6524 9.6525 9.6526 9.6527 9.6528
    9.6529 9.6530 9.6531 9.6532 9.6533 9.6534 9.6535 9.6536 9.6537 9.6538 9.6539 9.6541 9.6542 9.6551
    9.6552 9.6561 9.6562 9.6571 9.6572 9.6581 9.6582 9.6591 9.6592 9.6601 9.6602 9.6603 9.6604 9.6605
    9.6606 9.6607 9.6608 9.6609 9.6611 9.6612 9.6621 9.6622 9.6631 9.6632 9.6633 9.6634 9.6635 9.6636
    9.6637 9.6638 9.6639 9.6641 9.6642 9.6651 9.6652 9.6653 9.6654 9.6655 9.6656 9.6657 9.6658 9.6659
    9.6661 9.6662 9.6671 9.6672 9.6681 9.6682 9.6691 9.6692 9.6701 9.6702 9.6703 9.6704 9.6705 9.6706
    9.6707 9.6708 9.6709 9.6711 9.6712 9.6721 9.6722 9.6731 9.6732 9.6741 9.6742 9.6743 9.6744 9.6745
    9.6746 9.6747 9.6748 9.6749 9.6751 9.6752 9.6761 9.6762 9.6771 9.6772 9.6781 9.6782 9.6783 9.6784
    9.6785 9.6786 9.6787 9.6788 9.6789 9.6791 9.6792 9.6801 9.6802 9.6811 9.6812 9.6821 9.6822 9.6831
    9.6832 9.6841 9.6842 9.6851 9.6852 9.6861 9.6862 9.6863 9.6864 9.6865 9.6866 9.6867 9.6868 9.6869
    9.6871 9.6872 9.6881 9.6882 9.6891 9.6892 9.6901 9.6902 9.6911 9.6912 9.6913 9.6914 9.6915 9.6916
    9.6917 9.6918 9.6919 9.6921 9.6922 9.6931 9.6932 9.6941 9.6942 9.6951 9.6952 9.6961 9.6962 9.6971
    9.6972 9.6981 9.6982 9.6983 9.6984 9.6985 9.6986 9.6987 9.6988 9.6989 9.6991 9.6992 9.7001 9.7002
    9.7011 9.7012 9.7013 9.7014 9.7015 9.7016 9.7017 9.7018 9.7019 9.7021 9.7022 9.7023 9.7024 9.7025
    9.7026 9.7027 9.7028 9.7029 9.7031 9.7032 9.7033 9.7034 9.7035 9.7036 9.7037 9.7038 9.7039 9.7041
    9.7042 9.7043 9.7044 9.7045 9.7046 9.7047 9.7048 9.7049 9.7051 9.7052 9.7053 9.7054 9.7055 9.7056
    9.7057 9.7058 9.7059 9.7061 9.7062 9.7063 9.7064 9.7065 9.7066 9.7067 9.7068 9.7069 9.7071 9.7072
    9.7073 9.7074 9.7075 9.7076 9.7077 9.7078 9.7079 9.7081 9.7082 9.7083 9.7084 9.7085 9.7086 9.7087
    9.7088 9.7089 9.7091 9.7092 9.7093 9.7094 9.7095 9.7096 9.7097 9.7098 9.7099 9.7101 9.7102 9.7103
    9.7104 9.7105 9.7106 9.7107 9.7108 9.7109 9.7111 9.7112 9.7113 9.7114 9.7115 9.7116 9.7117 9.7118
    9.7119 9.7121 9.7122 9.7123 9.7124 9.7125 9.7126 9.7127 9.7128 9.7129 9.7131 9.7132 9.7133 9.7134
    9.7135 9.7136 9.7137 9.7138 9.7139 9.7141 9.7142 9.7143 9.7144 9.7145 9.7146 9.7147 9.7148 9.7149
    9.7151 9.7152 9.7153 9.7154 9.7155 9.7156 9.7157 9.7158 9.7159 9.7161 9.7162 9.7163 9.7164 9.7165
    9.7166 9.7167 9.7168 9.7169 9.7171 9.7172 9.7173 9.7174 9.7175 9.7176 9.7177 9.7178 9.7179 9.7181
    9.7182 9.7183 9.7184 9.7185 9.7186 9.7187 9.7188 9.7189 9.7191 9.7192 9.7193 9.7194 9.7195 9.7196
    9.7197 9.7198 9.7199 9.7201 9.7202 9.7203 9.7204 9.7205 9.7206 9.7207 9.7208 9.7209 9.7211 9.7212
    9.7213 9.7214 9.7215 9.7216 9.7217 9.7218 9.7219 9.7221 9.7222 9.7223 9.7224 9.7225 9.7226 9.7227
    9.7228 9.7229 9.7231 9.7232 9.7233 9.7234 9.7235 9.7236 9.7237 9.7238 9.7239 9.7241 9.7242 9.7243
    9.7244 9.7245 9.7246 9.7247 9.7248 9.7249 9.7251 9.7252 9.7261 9.7262 9.7263 9.7264 9.7265 9.7266
    9.7267 9.7268 9.7269 9.7271 9.7272 9.7273 9.7274 9.7275 9.7276 9.7277 9.7278 9.7279 9.7281 9.7282
    9.7283 9.7284 9.7285 9.7286 9.7287 9.7288 9.7289 9.7291 9.7292 9.7293 9.7294 9.7295 9.7296 9.7297
    9.7298 9.7299 9.7301 9.7302 9.7303 9.7304 9.7305 9.7306 9.7307 9.7308 9.7309 9.7311 9.7312 9.7313
    9.7314 9.7315 9.7316 9.7317 9.7318 9.7319 9.7321 9.7322 9.7323 9.7324 9.7325 9.7326 9.7327 9.7328
    9.7329 9.7331 9.7332 9.7333 9.7334 9.7335 9.7336 9.7337 9.7338 9.7339 9.7341 9.7342 9.7343 9.7344
    9.7345 9.7346 9.7347 9.7348 9.7349 9.7351 9.7352 9.7361 9.7362 9.7363 9.7364 9.7365 9.7366 9.7367
    9.7368 9.7369 9.7371 9.7372 9.7373 9.7374 9.7375 9.7376 9.7377 9.7378 9.7379 9.7381 9.7382 9.7383
    9.7384 9.7385 9.7386 9.7387 9.7388 9.7389 9.7391 9.7392 9.7393 9.7394 9.7395 9.7396 9.7397 9.7398
    9.7399 9.7401 9.7402 9.7403 9.7404 9.7405 9.7406 9.7407 9.7408 9.7409 9.7411 9.7412 9.7413 9.7414
    9.7415 9.7416 9.7417 9.7418 9.7419 9.7421 9.7422 9.7423 9.7424 9.7425 9.7426 9.7427 9.7428 9.7429
    9.7431 9.7432 9.7433 9.7434 9.7435 9.7436 9.7437 9.7438 9.7439 9.7441 9.7442 9.7443 9.7444 9.7445
    9.7446 9.7447 9.7448 9.7449 9.7451 9.7452 9.7453 9.7454 9.7455 9.7456 9.7457 9.7458 9.7459 9.7461
    9.7462 9.7463 9.7464 9.7465 9.7466 9.7467 9.7468 9.7469 9.7471 9.7472 9.7473 9.7474 9.7475 9.7476
    9.7477 9.7478 9.7479 9.7481 9.7482 9.7483 9.7484 9.7485 9.7486 9.7487 9.7488 9.7489 9.7491 9.7492
    9.7501 9.7502 9.7518 9.7519 9.7521 9.7522 9.7523 9.7524 9.7525 9.7526 9.7527 9.7528 9.7529 9.7531
    9.7532 9.7533 9.7534 9.7535 9.7536 9.7537 9.7538 9.7539 9.7541 9.7542 9.7551 9.7552 9.7561 9.7562
    9.7571 9.7572 9.7581 9.7582 9.7591 9.7592 9.7601 9.7602 9.7603 9.7604 9.7605 9.7606 9.7607 9.7608
    9.7609 9.7611 9.7612 9.7621 9.7622 9.7631 9.7632 9.7633 9.7634 9.7635 9.7636 9.7637 9.7638 9.7639
    9.7641 9.7642 9.7651 9.7652 9.7653 9.7654 9.7655 9.7656 9.7657 9.7658 9.7659 9.7661 9.7662 9.7671
    9.7672 9.7681 9.7682 9.7691 9.7692 9.7701 9.7702 9.7703 9.7704 9.7705 9.7706 9.7707 9.7708 9.7709
    9.7711 9.7712 9.7721 9.7722 9.7731 9.7732 9.7741 9.7742 9.7743 9.7744 9.7745 9.7746 9.7747 9.7748
    9.7749 9.7751 9.7752 9.7761 9.7762 9.7771 9.7772 9.7781 9.7782 9.7783 9.7784 9.7785 9.7786 9.7787
    9.7788 9.7789 9.7791 9.7792 9.7801 9.7802 9.7811 9.7812 9.7821 9.7822 9.7831 9.7832 9.7841 9.7842
    9.7851 9.7852 9.7861 9.7862 9.7863 9.7864 9.7865 9.7866 9.7867 9.7868 9.7869 9.7871 9.7872 9.7881
    9.7882 9.7891 9.7892 9.7901 9.7902 9.7911 9.7912 9.7913 9.7914 9.7915 9.7916 9.7917 9.7918 9.7919
    9.7921 9.7922 9.7931 9.7932 9.7941 9.7942 9.7951 9.7952 9.7961 9.7962 9.7971 9.7972 9.7981 9.7982
    9.7983 9.7984 9.7985 9.7986 9.7987 9.7988 9.7989 9.7991 9.7992 9.8001 9.8002 9.8018 9.8019 9.8021
    9.8022 9.8023 9.8024 9.8025 9.8026 9.8027 9.8028 9.8029 9.8031 9.8032 9.8033 9.8034 9.8035 9.8036
    9.8037 9.8038 9.8039 9.8041 9.8042 9.8051 9.8052 9.8061 9.8062 9.8071 9.8072 9.8081 9.8082 9.8091
    9.8092 9.8101 9.8102 9.8103 9.8104 9.8105 9.8106 9.8107 9.8108 9.8109 9.8111 9.8112 9.8121 9.8122
    9.8131 9.8132 9.8133 9.8134 9.8135 9.8136 9.8137 9.8138 9.8139 9.8141 9.8142 9.8151 9.8152 9.8153
    9.8154 9.8155 9.8156 9.8157 9.8158 9.8159 9.8161 9.8162 9.8171 9.8172 9.8181 9.8182 9.8191 9.8192
    9.8201 9.8202 9.8203 9.8204 9.8205 9.8206 9.8207 9.8208 9.8209 9.8211 9.8212 9.8221 9.8222 9.8231
    9.8232 9.8241 9.8242 9.8243 9.8244 9.8245 9.8246 9.8247 9.8248 9.8249 9.8251 9.8252 9.8261 9.8262
    9.8271 9.8272 9.8281 9.8282 9.8283 9.8284 9.8285 9.8286 9.8287 9.8288 9.8289 9.8291 9.8292 9.8301
    9.8302 9.8311 9.8312 9.8321 9.8322 9.8331 9.8332 9.8341 9.8342 9.8351 9.8352 9.8361 9.8362 9.8363
    9.8364 9.8365 9.8366 9.8367 9.8368 9.8369 9.8371 9.8372 9.8381 9.8382 9.8391 9.8392 9.8401 9.8402
    9.8411 9.8412 9.8413 9.8414 9.8415 9.8416 9.8417 9.8418 9.8419 9.8421 9.8422 9.8431 9.8432 9.8441
    9.8442 9.8451 9.8452 9.8461 9.8462 9.8471 9.8472 9.8481 9.8482 9.8483 9.8484 9.8485 9.8486 9.8487
    9.8488 9.8489 9.8491 9.8492 9.8501 9.8502 9.8518 9.8519 9.8521 9.8522 9.8523 9.8524 9.8525 9.8526
    9.8527 9.8528 9.8529 9.8531 9.8532 9.8533 9.8534 9.8535 9.8536 9.8537 9.8538 9.8539 9.8541 9.8542
    9.8551 9.8552 9.8561 9.8562 9.8571 9.8572 9.8581 9.8582 9.8591 9.8592 9.8601 9.8602 9.8603 9.8604
    9.8605 9.8606 9.8607 9.8608 9.8609 9.8611 9.8612 9.8621 9.8622 9.8631 9.8632 9.8633 9.8634 9.8635
    9.8636 9.8637 9.8638 9.8639 9.8641 9.8642 9.8651 9.8652 9.8653 9.8654 9.8655 9.8656 9.8657 9.8658
    9.8659 9.8661 9.8662 9.8671 9.8672 9.8681 9.8682 9.8691 9.8692 9.8701 9.8702 9.8703 9.8704 9.8705
    9.8706 9.8707 9.8708 9.8709 9.8711 9.8712 9.8721 9.8722 9.8731 9.8732 9.8741 9.8742 9.8743 9.8744
    9.8745 9.8746 9.8747 9.8748 9.8749 9.8751 9.8752 9.8761 9.8762 9.8771 9.8772 9.8781 9.8782 9.8783
    9.8784 9.8785 9.8786 9.8787 9.8788 9.8789 9.8791 9.8792 9.8801 9.8802 9.8811 9.8812 9.8821 9.8822
    9.8831 9.8832 9.8841 9.8842 9.8851 9.8852 9.8861 9.8862 9.8863 9.8864 9.8865 9.8866 9.8867 9.8868
    9.8869 9.8871 9.8872 9.8881 9.8882 9.8891 9.8892 9.8901 9.8902 9.8911 9.8912 9.8913 9.8914 9.8915
    9.8916 9.8917 9.8918 9.8919 9.8921 9.8922 9.8931 9.8932 9.8941 9.8942 9.8951 9.8952 9.8961 9.8962
    9.8971 9.8972 9.8981 9.8982 9.8983 9.8984 9.8985 9.8986 9.8987 9.8988 9.8989 9.8991 9.8992 9.9001
    9.9002 9.9018 9.9019 9.9021 9.9022 9.9023 9.9024 9.9025 9.9026 9.9027 9.9028 9.9029 9.9031 9.9032
    9.9033 9.9034 9.9035 9.9036 9.9037 9.9038 9.9039 9.9041 9.9042 9.9051 9.9052 9.9061 9.9062 9.9071
    9.9072 9.9081 9.9082 9.9091 9.9092 9.9101 9.9102 9.9103 9.9104 9.9105 9.9106 9.9107 9.9108 9.9109
    9.9111 9.9112 9.9121 9.9122 9.9131 9.9132 9.9133 9.9134 9.9135 9.9136 9.9137 9.9138 9.9139 9.9141
    9.9142 9.9151 9.9152 9.9153 9.9154 9.9155 9.9156 9.9157 9.9158 9.9159 9.9161 9.9162 9.9171 9.9172
    9.9181 9.9182 9.9191 9.9192 9.9201 9.9202 9.9203 9.9204 9.9205 9.9206 9.9207 9.9208 9.9209 9.9211
    9.9212 9.9221 9.9222 9.9231 9.9232 9.9241 9.9242 9.9243 9.9244 9.9245 9.9246 9.9247 9.9248 9.9249
    9.9251 9.9252 9.9261 9.9262 9.9271 9.9272 9.9281 9.9282 9.9283 9.9284 9.9285 9.9286 9.9287 9.9288
    9.9289 9.9291 9.9292 9.9301 9.9302 9.9311 9.9312 9.9321 9.9322 9.9331 9.9332 9.9341 9.9342 9.9351
    9.9352 9.9361 9.9362 9.9363 9.9364 9.9365 9.9366 9.9367 9.9368 9.9369 9.9371 9.9372 9.9381 9.9382
    9.9391 9.9392 9.9401 9.9402 9.9411 9.9412 9.9413 9.9414 9.9415 9.9416 9.9417 9.9418 9.9419 9.9421
    9.9422 9.9431 9.9432 9.9441 9.9442 9.9451 9.9452 9.9461 9.9462 9.9471 9.9472 9.9481 9.9482 9.9483
    9.9484 9.9485 9.9486 9.9487 9.9488 9.9489 9.9491 9.9492 9.9501 9.9502 9.9518 9.9519 9.9521 9.9522
    9.9523 9.9524 9.9525 9.9526 9.9527 9.9528 9.9529 9.9531 9.9532 9.9533 9.9534 9.9535 9.9536 9.9537
    9.9538 9.9539 9.9541 9.9542 9.9551 9.9552 9.9561 9.9562 9.9571 9.9572 9.9581 9.9582 9.9591 9.9592
    9.9601 9.9602 9.9603 9.9604 9.9605 9.9606 9.9607 9.9608 9.9609 9.9611 9.9612 9.9621 9.9622 9.9631
    9.9632 9.9633 9.9634 9.9635 9.9636 9.9637 9.9638 9.9639 9.9641 9.9642 9.9651 9.9652 9.9653 9.9654
    9.9655 9.9656 9.9657 9.9658 9.9659 9.9661 9.9662 9.9671 9.9672 9.9681 9.9682 9.9691 9.9692 9.9701
    9.9702 9.9703 9.9704 9.9705 9.9706 9.9707 9.9708 9.9709 9.9711 9.9712 9.9721 9.9722 9.9731 9.9732
    9.9741 9.9742 9.9743 9.9744 9.9745 9.9746 9.9747 9.9748 9.9749 9.9751 9.9752 9.9761 9.9762 9.9771
    9.9772 9.9781 9.9782 9.9783 9.9784 9.9785 9.9786 9.9787 9.9788 9.9789 9.9791 9.9792 9.9801 9.9802
    9.9811 9.9812 9.9821 9.9822 9.9831 9.9832 9.9841 9.9842 9.9851 9.9852 9.9861 9.9862 9.9863 9.9864
    9.9865 9.9866 9.9867 9.9868 9.9869 9.9871 9.9872 9.9881 9.9882 9.9891 9.9892 9.9901 9.9902 9.9911
    9.9912 9.9913 9.9914 9.9915 9.9916 9.9917 9.9918 9.9919 9.9921 9.9922 9.9931 9.9932 9.9941 9.9942
    9.9951 9.9952 9.9961 9.9962 9.9971 9.9972 9.9981 9.9982 9.9983 9.9984 9.9985 9.9986 9.9987 9.9988
    9.9989 9.9991 9.9992
    """

if __name__ == "__main__":
    d = {}
    sizes = ParseCommandLine(d)
    if d["-G"]:
        GaugeSizes(sizes, d, all=True)
    elif d["-g"]:
        GaugeSizes(sizes, d, all=False)
    else:
        for size in sizes:
            GetBlocks(size, d)
