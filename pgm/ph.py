"""
Provide filter pip help
    'pip help cmd' gives help on the command, then annoyingly includes a
    long page of general options.  This script filters out the General
    Options.
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Pip help filter
    ##∞what∞#
    ##∞test∞# #∞test∞#
    # Standard imports
    import getopt
    import os
    from pathlib import Path as P
    import sys
    import subprocess
    from pdb import set_trace as xx

    # Custom imports
    from wrap import wrap, dedent
    from color import Color, TRM as t

    # Global variables
    ii = isinstance
    W = int(os.environ.get("COLUMNS", "80")) - 1
    L = int(os.environ.get("LINES", "50"))
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        nm = sys.argv[0]
        print(
            dedent(f"""
        Usage:  {nm} cmd
          Print out pip's help on a command, filtering out the general
          options.  Example:  '{nm} install' gives help information on the
          install command.
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, cmds = getopt.getopt(sys.argv[1:], "ah", ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug

                debug.SetDebugger()
        assert ii(cmds, list)
        return cmds


if 1:  # Core functionality

    def ExecuteCommand(arg):
        cmd = ["/usr/local/bin/pip", "help"]
        cmd.extend(arg)
        r = subprocess.run(cmd, capture_output=True, text=True)
        s = r.stdout
        loc = s.find("General Options:\n")
        print(s[:loc].strip())


if __name__ == "__main__":
    d = {}  # Options dictionary
    cmd = ParseCommandLine(d)
    ExecuteCommand(cmd)
