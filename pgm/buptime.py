'''
Print the elapsed time.  A file name is given on the command line
and this script monitors when this file disappears from the file system,
then prints out the time.  The use case is my backup tool, which this
script's timing allows me to see how long the backup took.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print the elapsed time to see how long a backup takes
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from time import time, sleep, asctime
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from timer import Stopwatch
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        t.dbg = t("lill")
        g.sw = None
        g.name = sys.argv[0]
        t.msg = t("ornl")
        t.timeout = t("redl")
if 1:   # Utility
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.n}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] filename
          Start a timer and monitor when the filename disappears from the
          file system.  Print out the elapsed time.
        Options:
            -d      Turn on debug printing
            -i n    Interval in seconds to check for file [{d["-i"]} s]
            -k n    Terminate when this time is reached
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Debug printing
        d["-i"] = float(1)  # Check interval in s
        d["-k"] = 24*3600   # Terminate after this time
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "di:k:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
            elif o in ("-i", "-k"):
                try:
                    d[o] = float(a)
                    if d[o] <= 0:
                        raise ValueError()
                except ValueError:
                    msg = "-i option's argument must be > 0"
                    Error(msg)
        if d["-d"]:
            g.dbg = True
        return args[0]
if 1:   # Core functionality
    def Create(file):
        'Create the sentinel file and put the starting time in it'
        with open(file, "w") as fp:
            fp.write(f"Start time {time()} s\n")
    def Monitor(file):
        '''Periodically check that the sentinel file still exists.  When it
        is no longer present, print out the elapsed time.
        '''
        assert file.exists()
        timeout = False
        while True:
            Dbg(f"Starting sleep at {g.sw()} s")
            sleep(d["-i"])
            Dbg(f"Sleep over at {g.sw()} s")
            if not file.exists():
                Dbg(f"Sentinel file no longer exists at {g.sw()} s")
                break
            if g.sw() > d["-k"]:
                timeout = True
                Dbg(f"Timeout at {g.sw()} s")
                break
        if timeout:
            print(f"{t.timeout}{g.name} timed out after {d['-k']} s")
            print(f"  Clock time = {asctime()}")
            t.print(f"  Stopwatch time = {g.sw()} s")
        else:
            # Print the elapsed time
            et = g.sw()
            t.print(f"{t.msg}Elapsed time = {et} s = {et/60} minutes = {et/3600} hours")

if __name__ == "__main__":
    d = {}      # Options dictionary
    filename = ParseCommandLine(d)
    file = P(filename)
    Create(file)
    g.sw = Stopwatch()
    Monitor(file)


