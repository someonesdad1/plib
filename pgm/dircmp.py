"""
Compare two directories
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Compare two directories
    # ∞what∞#
    # ∞test∞# #∞test∞#
    # Standard imports
    import filecmp
    import getopt
    import os
    from pathlib import Path as P
    import sys
    from pdb import set_trace as xx

    # Custom imports
    from columnize import Columnize
    from wrap import wrap, dedent
    from color import Color, TRM as t

    # Global variables
    ii = isinstance

    class g:
        pass

    g.dir1 = None
    g.dir2 = None
    t.first = t("grnl")
    t.second = t("yell")
    t.differ = t("redl")
    t.same = t("sky")
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] dir1 dir2
          Compare the files in two directories.
        Options:
            -r      Recursive compare
            -s      Show files that are the same
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-r"] = False
        d["-s"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hrs", ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("rs"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug

                debug.SetDebugger()
        return args


if 1:  # Core functionality

    def GetFiles(directory):
        dir = P(directory)
        if not dir.exists():
            Error(f"{directory!r} doesn't exist")
        files = dir.glob("**/*") if d["-r"] else dir.glob("*")
        return set(i.relative_to(dir) for i in files if i.is_file())

    def OnlyIn(name, color, files1, files2):
        r = files1 - files2
        if r:
            print(f"{color}Files only in {name}:")
            for i in Columnize(sorted(r), indent="  "):
                print(i)
            t.out()

    def Report():
        OnlyIn(g.dir1, t.first, g.files1, g.files2)
        OnlyIn(g.dir2, t.second, g.files2, g.files1)
        common = g.files1 & g.files2
        match, mismatch, errors = filecmp.cmpfiles(
            g.dir1, g.dir2, common, shallow=False
        )
        if mismatch:
            print(f"{t.differ}Files that differ:")
            for i in Columnize(sorted(mismatch), indent="  "):
                print(i)
            t.out()
        if d["-s"] and match:
            print(f"{t.same}Files that are the same:")
            for i in Columnize(sorted(match), indent="  "):
                print(i)
            t.out()


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if len(args) != 2:
        Usage()
    g.dir1, g.dir2 = args
    g.files1, g.files2 = GetFiles(g.dir1), GetFiles(g.dir2)
    Report()
