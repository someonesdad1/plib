'''
Run a script when it changes
    
    This script helps development of a script by letting you edit the
    script in one window and see the change in the output when you save the
    script.  Run the script with the -h option to see some examples.

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
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        g.dbg = True
        g.sep = "-"     # Separator character
        g.count = 0     # Count number of times script is run
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
        t.hdr = t("wht", "#001146")
        t.pid = t("redl")
        t.cmdline = t("purl")
        g.L, g.C = GetScreen()
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
    def Manpage():
        print(dedent(f'''

        This script is handy when developing scripts.  I use it most of the
        time for developing python scripts, but it should work for many
        development tasks, as long as you're on a UNIX-type system like
        cygwin, Linux, or Mac.  Here's how I use this script:

            I use a portrait monitor to run my editor.  I normally run this
            with 100 to 130 lines so I can see a goodly amount of code in a
            window.  In the landscape monitor I have two side-by-side
            terminals with 100 columns and 53 lines to run the script and
            have another shell window for miscellaneous task.  I run the
            script under development with mkpy.py.  When I change the
            script being developed and save it, it is run in the other
            window.  The core feature is that I don't have to move my mouse
            cursor to the other window and execute a command.

        '''))
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] "command string"
          Monitor the mtime of the indicated script and when it changes, run
          the script with the arguments.  The command line will be run in a
          shell.  Note the -f option is required.
        Example
          python {sys.argv[0]} -f myfile "ls | awk -f myfile"
            The ls command will execute and its results will be processed
            by awk using myfile for its commands.  When myfile changes, 
            a separator with the elapsed time from starting will be printed
            and the new myscript will be run with the interpreter.
        Options
            -c      Clear the screen before the python script is run
            -f s    Script file to monitor for mtime changes
            -h      Print a manpage
            -o      Run the script only once
            -v      Verbose mode:  show count and clock time
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Clear the screen when script runs
        d["-f"] = ""        # Script to monitor mtime
        d["-o"] = False     # Run once
        d["-v"] = False     # Verbose mode
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chf:ov") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cov"):
                d[o] = not d[o]
            elif o == "-f":
                d[o] = a
            elif o == "-h":
                Usage(status=0)
        GetColors()
        if not args:
            Usage()
        if not d["-f"]:
            Error(f"-f option for the file to monitor for mtime changes required")
        d["-f"] = P(d["-f"])
        if not d["-f"].exists():
            Error(f"File {d['-f']!r} doesn't exist")
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
    def Run(cmdline, start_time):
        runtime = time.time() - start_time
        if runtime < 60:
            s = f"{runtime:.1f} seconds"
        elif runtime < 3600:
            s = f"{runtime/60:.2f} minutes"
        elif runtime < 24*3600:
            s = f"{runtime/3600:.3f} hours"
        else:
            s = f"{runtime/(24*3600):.3f} days"
        # Print separator
        if not d["-c"]:
            sep = f"{s} since starting"
            # Put the date nearer to the left side
            lsep = len(sep) + 2     # Separator + 2 spaces
            left = g.C//5
            right = g.C - left - lsep
            t.print(f"{t.hdr}{g.sep*left} {sep} {g.sep*right}")
            # If verbose, print clock time
            if d["-v"]:
                t.print(f"{t.cmdline}cmdline = {cmdline!r}")
                Date()
                print()
        subprocess.run(cmdline, shell=True)
    def ExecuteScript(cmdline):
        '''The cmdline is the single string the user typed on the command
        line.  It can contain '$p' for python or '$a' for gawk.  The first
        token must be the interpreter to use and the second token must be
        the name of the script.  The script will be run when its
        modification time changes.
        '''
        f = cmdline.split()
        if len(f) < 2:
            Error("The string on the command line must contain 2 or more tokens")
        script = d["-f"]
        if d["-v"]:
            print(f"Command = {cmdline!r}")
        mtime = script.stat().st_mtime
        start_time = time.time()
        if not d["-v"]:
            t.print(f"{t.cmdline}cmdline = {cmdline!r}")
        t.print(f"{t.pid}PID of mkpy.py = {os.getpid()}")
        Run(cmdline, start_time)
        if d["-o"]:
            return
        while True:
            stat = script.stat()
            new_mtime = stat.st_mtime
            if new_mtime > mtime:
                Clear()
                Run(cmdline, start_time)
                mtime = new_mtime
            # The delay below is important, as lack of one will cause an
            # apparent race condition where the stat() call fails.  The
            # failure occurs (by binary search) for sleep times less than
            # around 100 ms or so.  Half a second seems reasonable.
            time.sleep(0.5)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    cmdline = ' '.join(args)
    ExecuteScript(cmdline)
