"""
Show file names in directory that are too long for a 2 column display in
80 columns.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Show file names that are too long
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] [dir1 [dir2...]]
      Show files in the indicated directories whose names are too long for
      an n-column display in an 80-column window.  Defaults to current
      directory and n = 2 columns.
    Options:
        -c n    Show names that are too long for n columns.  n defaults to 2.
        -w      Use current screen width instead of 80 columns
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-c"] = 2
    d["-w"] = False
    try:
        opts, dirs = getopt.getopt(sys.argv[1:], "c:hw")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("w"):
            d["-width"] = int(os.environ["COLUMNS"]) // 2
        elif o == "-c":
            d[o] = int(a)
            if d[o] < 1:
                Error("-c option must be 2 or larger")
        elif o in ("-h", "--help"):
            Usage(status=0)
    if d["-w"]:
        d["width"] = int(os.environ["COLUMNS"]) // d["-c"]
    else:
        d["width"] = 80 // d["-c"]
    if not dirs:
        Usage()
    return dirs


def Report(dir, d):
    pl, w = pathlib.Path(dir), d["width"]
    files = []
    for file in pl.glob("*"):
        s = str(file)
        if len(s) > w:
            files.append((s, len(s) - w))
    if files:
        print(pl.resolve())
        for i, excess in files:
            print(f"  {i} [+{excess}]")


if __name__ == "__main__":
    d = {}  # Options dictionary
    dirs = ParseCommandLine(d)
    for dir in dirs:
        Report(dir, d)
