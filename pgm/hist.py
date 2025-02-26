"""
Categorize output of bash history command (this script analyzes stdin)
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Summarize bash history
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
    from collections import defaultdict
if 1:  # Custom imports
    from columnize import Columnize
    from wrap import wrap, dedent, indent, Wrap
    from globalcontainer import Global, Variable, Constant

    if 0:
        import debug

        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
    G = Global()
    G.ro = Constant()
    G.rw = Variable()
if 1:  # Utility

    def eprint(*p, **kw):
        "Print to stderr"
        print(*p, **kw, file=sys.stderr)

    def Error(msg, status=1):
        eprint(msg)
        exit(status)

    def Usage(d, status=1):
        name = sys.argv[0]
        print(
            dedent(f"""
    Usage:  {name} [options] [file]
      Summarizes the output of the bash history command.  Reads stdin if
      file is '-'.

    Options:
        -h      Print a manpage
    """)
        )
        exit(status)

    def ParseCommandLine(d):
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o in ("-h", "--help"):
                Usage(d, status=0)
        if len(args) > 1:
            Error("Put only one file on command line")
        return args[0]


if 1:  # Core functionality

    def Classify(lines):
        rd = defaultdict(int)
        global total
        for line in lines:
            total += 1
            f = line.split()
            if len(f) < 3:
                continue
            f.pop(0)
            f.pop(0)
            cmd = f.pop(0)
            if cmd[0] == "#" or ";" in cmd:
                continue
            rd[cmd] += 1
        return rd

    def Report(rd, n=100):
        items = list(reversed(sorted([(int(j), i) for i, j in rd.items()])))
        out = []
        m = max([len(cmd) for count, cmd in items[:n]])
        for count, cmd in items[:n]:
            out.append(f"{cmd:{m}s} {count:6d}")
        print("Most heavily-used commands in shell history:")
        for line in Columnize(out):
            print(line)
        print("Total commands in history =", total)


if __name__ == "__main__":
    d = {}  # Options dictionary
    total = 0
    file = ParseCommandLine(d)
    stream = sys.stdin if file == "-" else open(file)
    lines = stream.read().split("\n")
    report_dict = Classify(lines)
    Report(report_dict)
