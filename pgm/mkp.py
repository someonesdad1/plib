'''
Run a python script when it changes
    
    At startup the screen is cleared.  Then the script's mtime is stored
    and when it changes, the script is run with the given parameters.
    Each time the script is run, a separator string in color is printed
    with the current date/time.
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
        # <programming> Run a python script when it changes
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
        import time
    if 1:   # Custom imports
        from color import t
        from get import GetLines
        from wrap import dedent
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from wsl import wsl     # wsl is True when running under WSL Linux
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        g.dbg = True
        ii = isinstance
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
        t.hdr = t("grnl")
        # Separator for subsequent invocations
        g.L, g.C = GetScreen()
        g.sep = "-"*g.C
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stdout
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] python_script [arguments]
          Monitor the mtime of the python_script and when it changes, run
          the script with the arguments, notating the run with a separator
          and the current date/time.
        Options:
            -h      Print a manpage
            -c      Clear the screen before the python script is run
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Clear the screen when script runs
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ch") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("c"):
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
                Usage(status=0)
        GetColors()
        if not args:
            Usage()
        return args
if 1:   # Core functionality
    def Date():
        cmd = P("/plib/pgm/current_date.py")
        assert cmd.exists(), f"{str(cmd)!r} doesn't exist"
        cmd = [P("/plib/pgm/current_date.py"), "0"]
        subprocess.run(cmd)
    def Clear():
        if not d["-c"]:
            return
        subprocess.run("clear", shell=True)
    def Run(arguments, start_time):
        cmd = [sys.executable] + list(arguments)
        #cmd = sys.executable + " " + ' '.join(arguments)
        # Print separator and date
        t.print(f"{t.hdr}{g.sep}")
        print(f"{t('purl')}cmd = {cmd!r}")
        Date()
        runtime = time.time() - start_time
        if runtime < 60:
            s = f"{runtime/60:.2f} seconds"
        elif runtime < 3600:
            s = f"{runtime/60:.2f} minutes"
        elif runtime < 24*3600:
            s = f"{runtime/3600:.3f} hours"
        else:
            s = f"{runtime/(24*3600):.3f} days"
        t.print(f"{t.hdr}Run time = {s}")
        print()
        #subprocess.run(cmd, shell=True, env=os.environ)
        subprocess.run(cmd)
    def ExecuteScript(arguments):
        '''arguments will be deque of [python_script, optional_arguments].
        Run the python script with the indicated arguments (list of
        strings) whenever its mtime changes.
        '''
        # Get the name of the python script to run
        file = arguments[0]
        script = P(file)
        if not script.exists():
            Error(f"Python script {script.resolve()!r} doesn't exist")
        else:
            print(f"Script is '{script.resolve()}'")
        Dbg(f"{script!r}")
        mtime = script.stat().st_mtime
        start_time = time.time()
        Run(arguments, start_time)
        while True:
            stat = script.stat()
            new_mtime = stat.st_mtime
            if new_mtime > mtime:
                Clear()
                Run(arguments, start_time)
                mtime = new_mtime
            # The delay below is important, as lack of one will cause an
            # apparent race condition where the stat() call fails.  The
            # failure occurs (by binary search) for sleep times less than
            # around 100 ms or so.  Half a second seems reasonable.
            time.sleep(0.5)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    ExecuteScript(deque(args))
