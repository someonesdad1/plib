"""
Get a thickness with the Starrett #467 thickness gauge
    Find the leaves of the Starrett #467 thickness gauge to get a desired
    thickness.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Get a thickness with the Starrett #467 thickness gauge
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import bisect
    import sys
    import os
    import getopt
    from itertools import combinations
    from collections import defaultdict
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from f import flt
    from color import C
if 1:  # Global variables

    class g:
        pass

    g.i = C.lyel  # Used to flag an inexact metric conversion
    g.n = C.norm
    # The leaves are the following thicknesses in units of 0.1 mils:
    leaves = (15, 20, 30, 40, 60, 80, 100, 200, 300, 400, 750, 1000, 2000)


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] [size1 [size2 ...]]
      Print the leaves to use to get desired thicknesses from the Starrett
      model 467 thickness gauge.  Each size is in inches.
    Options:
      -a    Show all combinations
      -M    Use units of mils
      -m    Get thicknesses in mm (results will be approximate)
      -t    Print table of how to get all sizes 
      -v    Show the dimensions that can't be made
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-a"] = False  # Show all combinations
    d["-t"] = False  # Print table
    d["-M"] = False  # Use units of mils
    d["-m"] = False  # Use units of mm
    d["-v"] = False  # Print dimensions that can't be made
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "aMmtv")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for o, a in optlist:
        if o[1] in "aMmtv":
            d[o] = not d[o]
    if d["-v"]:
        CannotBeMade()
        exit(0)
    if not args and not d["-t"]:
        Usage()
    return args


def GetCombinations():
    """Generate all possible combinations of gauges and return as a
    dict with key size_in_tenths.  Each value of the dict is a list
    of the tuples of leaves that make up that size:
        [
            (gauges1, ...),
            (gauges2, ...),
            ...
        ]
    """
    results = defaultdict(list)
    assert leaves
    for num_comb in range(1, 14):
        for comb in combinations(leaves, num_comb):
            size = sum(comb)
            results[size].append(comb)
    return results


def CannotBeMade():
    not_in = []
    for i in range(15, 5001, 5):
        if i not in size_dict:
            not_in.append(i)
    not_in = list(sorted(not_in))
    print("The following dimensions in inches cannot be made:")
    flt(0).rtz = True
    for i in not_in:
        print(f"  {flt(i / 1e4)}")
    exit(0)


def Dec(size, end_space=0):
    """Convert size to a decimal string with no leading zero.
    Remove the trailing zero if necessary.  Assumes size is an
    integer between 15 and 5000.  If end_space is true, append a
    space character if the zero is removed.
    """
    assert 15 <= size <= 5000
    if d["-M"]:
        # Use mils
        if 0:
            x = flt(size) / 10
            with x:
                x.n = 5
                x.rtz = x.rtdp = True
                return str(x)
        else:
            s = str(round(float(size) / 10, 1))
            while s[-1] == "0":
                s = s[:-1]
            if s[-1] == ".":
                s = s[:-1]
            return s
    else:
        s = f"{size:04d}"
        if s[-1] == "0":
            s = s[:-1]
            if end_space:
                s += " "
        return "." + s


def PrintMetric(mm, size_dict):
    "Find the closest set of leaves to the size in mm"
    assert isinstance(mm, str)
    sizes = list(sorted(size_dict))
    tenths = int(1e4 * float(mm) / 25.4 + 0.5)
    # First check endpoints
    if tenths == sizes[0]:
        size = tenths
    elif tenths == sizes[-1]:
        size = tenths
    else:
        # Find the closest entry by bisection
        index = bisect.bisect_left(sizes, tenths)
        size = sizes[index]
        if size < sizes[0] or size > sizes[-1]:
            return  # No match
    # Now size contains the entry to print
    entry = size_dict[size]
    exact = True if size == tenths else False
    if d["-M"]:
        dim = round(1000 * float(mm) / 25.4, 1)
        units = "mils"
    else:
        dim = round(float(mm) / 25.4, 4)
        units = "inches"
    print(f"Size = {mm} mm = {dim} {units}:", end="  ")
    if not exact:
        p = flt(100 * (tenths - size) / size)
        mils = round((tenths - size) / 10, 1)
        dir = "low" if p < 0 else "high"
        with p:
            p.n = 2
            print(f"{g.i} ({dir} by {p}% = {mils} mils){g.n}")
    else:
        print()
    if d["-a"]:
        # Show all combinations for this value
        for leaves in entry:
            s = []
            for i in leaves:
                s.append(Dec(i))
            u = ", ".join(s)
            print(f"        {u}")
    else:
        # Find the shortest set of leaves
        shortest = []
        for leaves in entry:
            shortest.append((len(leaves), leaves))
        shortest = sorted(shortest)[0]
        s = []
        for i in shortest[1]:
            s.append(Dec(i))
        u = ", ".join(s)
        print(f"        {u}")


def PrintResults(tenths, size_dict):
    """tenths contains the integer size in 0.1 mils desired.  Find this
    integer in size_dict and print the combinations of leaves that make it
    up.  If not present, just return.

    If -m is used, then the size is in mm, so find the closest size.
    """
    assert isinstance(tenths, int)
    if tenths not in size_dict:
        return
    entry = size_dict[tenths]
    t = Dec(tenths, end_space=1) + ":"
    if d["-a"]:
        print(t)
        for leaves in entry:
            s = []
            for i in leaves:
                s.append(Dec(i))
            u = ", ".join(s)
            print(f"        {u}")
    else:
        # Find the shortest set of leaves
        shortest = []
        for leaves in entry:
            shortest.append((len(leaves), leaves))
        shortest = sorted(shortest)[0]
        s = []
        for i in shortest[1]:
            s.append(Dec(i))
        u = ", ".join(s)
        print(f"{t:6s}  {u}")


if __name__ == "__main__":
    d = {}  # Options dictionary
    size_dict = GetCombinations()
    sizes = ParseCommandLine(d)
    if d["-t"]:
        for size in sorted(size_dict):
            PrintResults(size, size_dict)
    else:
        for size in sizes:
            if d["-m"]:
                PrintMetric(size, size_dict)
            else:
                tenths = int(1e4 * size + 0.5)
                PrintResults(tenths, size_dict)
