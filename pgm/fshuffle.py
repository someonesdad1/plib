"""
Randomly shuffle the lines of a file
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
    # Randomly shuffle the lines of a file
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    import random
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] file1 [file2...]
      Randomly shuffle the lines of the files and print them to stdout.
      Use '-' to read from stdin.
    Options:
        -s sd   Seed the random number generator for repeatable shuffling
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-s"] = None  # Seed for random number generator
    try:
        optlist, files = getopt.getopt(sys.argv[1:], "s:")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        exit(1)
    for o, a in optlist:
        if o == "-s":
            d["-s"] = a
    if not files:
        Usage(d)
    return files


def GetLines(files, d):
    # Note lines will have newlines
    lines = []
    for file in files:
        s = sys.stdin.readlines() if file == "-" else open(file).readlines()
        lines.extend(s)
    return lines


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    if d["-s"] is not None:
        random.seed(d["-s"])
    lines = GetLines(files, d)
    random.shuffle(lines)
    for line in lines:
        print(line, end="")
