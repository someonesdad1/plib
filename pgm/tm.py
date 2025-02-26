"""
Clock time in seconds since epoch
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
    # Times in seconds since epoch
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import time
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
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
        Usage:  {name} [options] [offset_seconds]
          Print the current time in seconds less any given offset.
        Options:
          -h      Print a manpage
    """)
        )
        exit(status)

    def ParseCommandLine(d):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o in ("-h", "--help"):
                Usage(d, status=0)
        return float(args[0]) if args else 0.0


if __name__ == "__main__":
    d = {}  # Options dictionary
    offset = ParseCommandLine(d)
    print(f"{time.time() - offset}")
