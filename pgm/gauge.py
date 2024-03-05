'''
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
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2012 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Find gauge blocks to make a dimension
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import sys
        import getopt
        from itertools import combinations
        from math import *
    if 1:   # Custom imports
        from lwtest import Assert
        from wrap import dedent
        from f import flt
        from color import t
        from columnize import Columnize
        from gauge_sizes import gauges
        from u import u, ParseUnit
    if 1:   # Global variables
        # The following dictionary holds the gauge block sets.  You can add or delete sets as you
        # see fit.  The structure should be apparent if you want to add a new set.  Note the values
        # are integers; this helps make the summing of sizes fast and exact because there is no
        # roundoff error.
        gauge_block_sets = {
            # Value is (units, resolution, block_sizes_sequence)
            "user": ("inch", "0.0001", (    # 64 blocks
                # This gauge block set is a used Starrett set I bought in 2005 and had
                # some missing blocks.
                250, 350, 490, 500, 1000, 1003, 1004, 1005, 1006, 1007,
                1008, 1009, 1040, 1050, 1060, 1070, 1080, 1090, 1110, 1120,
                1140, 1160, 1170, 1180, 1190, 1210, 1220, 1230, 1250, 1260,
                1270, 1290, 1300, 1310, 1320, 1330, 1340, 1350, 1370, 1380,
                1390, 1400, 1420, 1430, 1440, 1450, 1460, 1470, 1500, 2500,
                3500, 4500, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000,
                9500, 20000, 30000, 40000)
            ),
            "metric": ("mm  ", "0.001", (   # 86 blocks
                1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010,
                1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110,
                1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210,
                1220, 1230, 1240, 1250, 1260, 1270, 1280, 1290, 1300, 1310,
                1320, 1330, 1340, 1350, 1360, 1370, 1380, 1390, 1400, 1410,
                1420, 1430, 1440, 1450, 1460, 1470, 1480, 1490, 1000, 1500,
                2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500,
                7000, 7500, 8000, 8500, 9000, 9500, 10000, 20000, 30000,
                40000, 50000, 60000, 70000, 80000, 90000, 100000)
            ),
            "inch36": ("inch", "0.0001", (  # 36 blocks
                500, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009,
                1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100,
                1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 1000, 2000,
                3000, 4000, 5000, 10000, 20000, 40000)
            ),
            "inch81": ("inch", "0.0001", (  # 81 blocks
                500, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009,
                1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100,
                1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200,
                1210, 1220, 1230, 1240, 1250, 1260, 1270, 1280, 1290, 1300,
                1310, 1320, 1330, 1340, 1350, 1360, 1370, 1380, 1390, 1400,
                1410, 1420, 1430, 1440, 1450, 1460, 1470, 1480, 1490, 1000,
                1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000,
                6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 20000, 30000,
                40000)
            ),
            "space": ("inch", "0.0005", [
                # This is a "Space Blocks" set I bought in the early 1970's.  I
                # remember paying around $70 for it and the same sets are
                # available today for around the same price.  They're cylinders
                # of steel finished to the stamped length and they can be
                # clamped together with set screws because there is a tapped
                # longitudinal hole through each piece.
                500, 625, 600, 700, 800, 900, 1000, 1010, 1020, 1030, 1040,
                1050, 1060, 1070, 1080, 1090, 1100, 1200, 1250, 1300, 1400,
                1500, 1600, 1700, 1800, 1900, 2000, 3000, 4000, 5000, 6000,
                7000, 8000, 9000, 10000, 10000]
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
        print(dedent(f'''
 
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
 
        '''.rstrip()))
        exit(0)
    def Usage(d, status=1):
        name, dsn, maxnum = sys.argv[0], d["-n"], d["-k"]
        tol = d["-f"]
        print(dedent(f'''
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
        '''))
        print("Allowed gauge block set names and characteristics:")
        s = []
        for name in sorted(gauge_block_sets):
            unit, resolution, blocks = gauge_block_sets[name]
            s.append(f"  {name:10s} {resolution:6s} {unit} ({len(blocks)} blocks)")
        print('\n'.join(s))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all combinations, not just the first
        d["-f"] = 1         # Tolerance in % for -g/-G lookups 
        d["-g"] = False     # Look up a gauge size (limited set)
        d["-G"] = False     # Look up all gauge sizes
        d["-k"] = 4         # Maximum subset size in search
        d["-n"] = "user"    # Name of default gauge block set
        d["-T"] = False     # Analyze user set for unreachable dimensions
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
        '''Print nicely-formatted tables of each type of block set.
        '''
        for name, (unit, resolution, seq) in gauge_block_sets.items():
            s, f = [], float(resolution)
            print("{0} ({1})".format(name, "um" if unit == "mm"
                  else "0.0001 inches"))
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
        '''Convert the size number (a string in inches or mm) to an integer
        size to search for.
        '''
        # string, string, list of integer sizes
        unit, resolution, blocks = gauge_block_sets[d["-n"]]
        x, T = abs(float(eval(size))), abs(float(resolution))
        # Using resolution as a template, round the size to an integer
        # number of template units.
        return int(x/T + 0.5)
    def PrintResults(integer_size, size, combination, d):
        '''integer_size is the actual size searched for; size is the
        original string the user passed on the command line.
        '''
        # string, string, list of integer sizes
        unit, resolution, blocks = gauge_block_sets[d["-n"]]
        fmt = formats[resolution]
        sz = abs(float(eval(size)))
        print(fmt % sz, ": ", sep="", end="")
        for i in combination:
            print(fmt % (float(i)*float(resolution)), " ", end="")
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
        '''For dimensions less than 10 inches, determine which dimensions can't
        be gotten using the indicated (-k option) number of blocks.
        '''
        ofp = open("user.blocks.impossible", "w")
        max_blocks = d["-k"]
        if 0:
            # Units are 0.0001 inches
            min_size, max_size = 1001, 100000
            print(dedent('''
            0.0001 inch dimensions that cannot be gotten with user block set:
            (Maximum number of blocks used is {max_blocks}).
            '''))
            print(msg)
            ofp.write(msg + "\n")
            for i, sz in enumerate(range(min_size, max_size)):
                size = f"  {sz/10000:.4f}"
                seq = GetBlocks(size, d)
                if seq is None:
                    print(size)
                    ofp.write(size + "\n")
        if 1:
            # Units are 0.001 inches
            min_size, max_size = 100, 10000
            print(dedent('''
            0.001 inch dimensions that cannot be gotten with user block set:
            (Maximum number of blocks used is {max_blocks}).'''))
            print(msg)
            ofp.write(msg + "\n")
            for i, sz in enumerate(range(min_size, max_size)):
                size = f"{sz/1000:.3f}"
                seq = GetBlocks(size, d)
                if seq is None:
                    print(size)
                    ofp.write(size + "\n")
    def GetSize(size):
        '''size is a string and will normally be a decimal number in inches.
        However, an optional length unit can be appended (space separator
        optional).  The size in inches is returned.
        '''
        t, unit = ParseUnit(size)
        t = float(t)
        if unit:
            if u.dim("inches") != u.dim(unit):
                print("'{}' is not a length unit".format(unit))
                exit(1)
            t *= u(unit)/u("inches")
        return t
    def GaugeSizes(sizes, d, all=False):
        '''Display gauge sizes that are within the tolerance percentage (from
        d["-f"]) of the given size.
        '''
        GAUGES = list(sorted(gauges.keys())) if all else [
            "US Number drill sizes",
            "US Letter drill sizes",
            "AWG",
            "US Standard steel sheet",
        ]
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
                    tol = 100*(sz_inches - size)/size
                    if abs(tol) <= tolerance:
                        s.append((tol, sz, sz_inches, gauge))
            if s:
                # Sort by first item, which is tolerance in %
                def f(x):
                    return x[0]
                for tol, sz, sz_inches, gauge in sorted(s, key=f):
                    print("  {:2s}   {:.4f}   {:6.1f}%   {}".format(str(sz),
                                sz_inches, tol, gauge))
            else:
                print("  No matches")
if 1:   # Find sizes that cannot be made
    def PartialStarrettSet(dia_min, dia_max, klo=4, khi=6):
        '''Print out the sizes that cannot be made with the indicated number of blocks.  dia_min
        and dia_max are integers in units of 0.0001 inches.  klo and khi are the k values to search
        with (k = number of blocks in set)
        '''
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
                x = float(dia/1e4)
                #print(f"{t('ornl')}{x:.4f}{t.n}", end=" ")
                print(f"{x:.4f} {sw()} seconds", file=fd)
            #if count and count % 1000 == 0:
            #    pct = int(100*count/N)
            #    print(f"{t('redl')}{pct}%{t.n}", file=sys.stderr)
        #print()

if 1:
    d, D = 4000, 100000
    from timer import Stopwatch
    with open("starrett.64.impossible_4_to_6", "w") as fd:
        sw = Stopwatch()
        print("k = 4 to 6 impossible sizes from $pp/gauge.py", file=fd)
        PartialStarrettSet(d, D, klo=4, khi=6)
    print(f"Ended at {sw()} seconds")
    exit()

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
