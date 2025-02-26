"""
TODO

    Put the following lines in file 'a':
        1   colors
        2   cove
        3   dist
        4   obsolete
    fcut.py -r a 2:-2
    It doesn't work as expected.

    Instead, change the design to use frange.Sequence to interpret the
    line number ranges and change to 0-based indexing.

Extract specified lines from a file
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Extract specified lines from a file
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import pathlib
    import sys
    from pdb import set_trace as xx
    from pprint import pprint as pp
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
    debug = False
    # State variables
    number_lines = False


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] file n:m [n1:m2 ...]
      Prints specified 1-based line number ranges (inclusive) of a file.
        n        Print line n
        n:m      Print lines n through m
        n:       Print from line n to end of file
         :m      Print from line 1 to line m
         :       Print all lines of the file
      If n is negative, it means to count from the last line of the file
      backwards.  You can also use 0, which is the same as 1.
    Options:
        -c      Output the complement of the specified lines
    Examples:
        fcut file 10:-10
            Chop off the first and last 10 lines of the file.
        fcut file :10 -10:
            or
        fcut -r file 10:-10
            Prints the first 10 and last 10 lines of the file.
        fcut -n file :
            Number all the lines of the file
    """)
    )
    exit(status)


def GetLinesFromFile(file):
    assert ii(file, P)
    s = open(file).read()
    if s and s[-1] == "\n":
        s = s[:-1]
    return s.split("\n")


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def ParseCommandLine(d):
    d["-c"] = False  # Complement of set of numbers on command line
    d["-d"] = False  # Turn on debug printing
    if len(sys.argv) < 2:
        Usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cdh")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("cd"):
            d[o] = not d[o]
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    if len(args) < 2:
        Usage()
    if d["-d"]:
        global debug
        debug = True
    return args


def ProcessLineSpecs(line_specs, numlines):
    """Return a list of pairs of integers that reflect the region of
    line numbers of the file that the user asked for (the user's numbers
    are 1-based line numbers).  Return line number specs that are
    1-based.  numlines is the number of lines in the file that were read
    in plus one.
    """
    specs = []
    for spec in line_specs:
        if spec.count(":") > 1:
            Error(f"Line ranges can only have zero or one ':' characters")
        if spec == ":":
            low, high = 1, numlines
        else:
            s = spec.split(":")
            if len(s) == 1 or s[0] == "" or s[1] == "":
                if spec[-1] == ":":  # If it ends in ':'
                    low, high = int(s[0]), numlines
                elif spec[0] == ":":  # If it begins with ':'
                    low, high = 1, int(s[1])
                else:  # Didn't contain ':'
                    low = high = int(s[0])
            else:
                low, high = int(s[0]), int(s[1])
                if low > high:
                    low, high = high, low
        if low < 0:
            if not (1 <= abs(low) <= numlines):
                msg = f"(must be -1 to {-numlines})"
                Error(f"Low spec in '{spec}' is bad {msg}")
            low = numlines + low + 1
        if high < 0:
            if not (1 <= abs(high) <= numlines):
                msg = f"(must be -1 to {-numlines})"
                Error(f"High spec in '{spec}' is bad {msg}")
            high = numlines + high + 1
        if low > high:
            low, high = high, low
        # Clamp values
        low = max(1, low)
        high = min(numlines, high)
        specs.append((low, high))  # Note these are 1-based numbers
    if debug:
        print("+ specs =", specs)
    # Convert the specs to a set of numbers
    nums = []
    for start, stop in specs:
        nums.extend(range(start, stop + 1))  # + 1 makes it inclusive
    nums = set(nums)
    if d["-c"]:
        nums = set(range(1, numlines + 1)) - nums
    if debug:
        if d["-c"]:
            print('+ Complement taken because d["-c"] is True')
        print("+ Line numbers in specs =", " ".join([str(i) for i in nums]))
        print(f"+ Line numbers go from 1 to {numlines}")
    # nums is the set of line numbers to return
    return nums


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    file = args[0]
    line_specs = args[1:]
    # Get all the lines from the file.  Add a blank line so we can used
    # 1-based indexing.
    lines = [""] + GetLinesFromFile(P(file))
    if lines[1:]:
        n = len(lines)
        nums = ProcessLineSpecs(line_specs, n - 1)
        for i in nums:
            print(lines[i])
