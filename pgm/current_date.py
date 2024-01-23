'''
Show current date/time
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Show current date/time
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from pathlib import Path as P
        from pprint import pprint as pp
        import getopt
        import os
        import re
        import subprocess
        import sys
        import time
    if 1:   # Custom imports
        from color import t
        from u import u
        from get import GetLines
        from wrap import dedent
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        t.dbg = t("lill")
        t.day = t("lav")

        ii = isinstance
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    g.W, g.L = GetScreen()
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stderr   # Debug printing to stderr by default
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        The time units are those allowed by the /plib/u.py script.  Run
        'python /plib/u.py time' to see the supported time units:

        '''))
        cmd = [sys.executable, "/plib/u.py", "Time"]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode:
            Error("Running u.py got an error")
        print(r.stdout.decode())
        print(dedent(f'''
         See?
        '''))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [offset [unit]]
          Show the current date/time on one line.  If offset is given, it
          shows the date/time with the current offset from now.  Allowed
          units for offset are s, min, hr, day, wk, mo, yr.
        Example
          1.  '{sys.argv[0]} -3 wk' shows the time/date 3 weeks ago.
          2.  Let x be the value in s printed out by the command.  
              '{sys.argv[0]} -x s' should show the date of the epoch,
              1 Jan 1970.
        Options
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Describe this option
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-h":
                Manpage()
        return args
if 1:   # Core functionality
    def PrintDateTime(*args):
        pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
