if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Extract lines from files
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    P = pathlib.Path


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {name} [options] file1 [file2...]
      Read stdin for a list of 1-based numbers that indicate which lines
      to extract from one or more text files.  The numbers must be
      white-space-separated integers (floating point numbers will be
      converted to integers).  Repeated integers will cause repeated
      output lines.  The lines will be printed in the order the integers
      are given.  The text file(s) are given on the command line.
    Options:
        -f f    Read numbers from file f
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-f"] = None
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:h")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-f",):
            d["-f"] = p = P(a)
            if not p.exists():
                Error(f"'{a}' doesn't exist")
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    return args


def ProcessFile(file, ln):
    "For file, print line numbers in sequence ln"
    try:
        lines = [i.rstrip("\n") for i in open(file).readlines()]
        if not lines:
            return 0
    except Exception:
        print(f"Couldn't read '{file}'")
        return 1
    for i in ln:
        print(lines[i])
    return 0


def GetLineNumbers():
    if d["-f"] is not None:
        ln = [int(i) - 1 for i in open(d["-f"]).read().split()]
    else:
        ln = [int(i) - 1 for i in sys.stdin.read().split()]
    return ln


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    return_status, ln = 0, GetLineNumbers()
    for file in files:
        return_status += ProcessFile(file, ln)
    exit(return_status)
