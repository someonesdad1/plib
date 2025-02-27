"""
Loads a CPU with n busy/wait tasks
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Script to load a CPU with processes that do nothing
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from multiprocessing import Process, Lock
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
        import time
    if 1:  # Custom imports
        import timer
        from f import flt
        from color import t
        from lwtest import Assert
        from u import u, ParseUnit
        from dpprint import PP

        pp = PP()  # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl  # wsl is True when running under WSL Linux
        # from columnize import Columnize
    if 1:  # Global variables

        class G:
            # Storage for global variables as attributes
            pass

        g = G()
        g.dbg = False
        ii = isinstance
if 1:  # Utility

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def GetColors():
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")

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
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] n [busy_time]
          Starts n processes that are busy-wait loops doing no work.  busy_time is a float between
          0 and 100, representing the percentage of a 1 second interval that each process is busy
          and consumes all of its core's resources.  It defaults to 100, meaning each process
          consumes 100% of a core's processing time.
        Options:
            -d      Turn on debugging
            -t t    Lifetime:  causes the processes to die in a time of t [{d["-t"]}].
                    Use time units that are in /plib/u.py (defaults to s).
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-d"] = False  # Turn on debugging
        d["-t"] = "15 min"  # Die after this time
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dt:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dz"):
                d[o] = not d[o]
            elif o == "-t":  # Die after this time
                d[o] = a
            elif o == "-h":
                Usage(status=0)
        g.dbg = True if d["-d"] else False
        GetColors()
        Dbg(f"Command line:  {' '.join(sys.argv)!r}")
        g.W, g.L = GetScreen()
        if 1:  # Get our lifetime in s
            num, unit = ParseUnit(d["-t"])
            g.lifetime = float(num) * u(unit)
            if g.lifetime < 0:
                Error(f"-t option's value must be >= 0")
        # Process the args by setting g.n and g.busy_fraction
        g.n = int(args[0])
        g.busy_fraction = flt(1)
        if g.n <= 0:
            Usage()
        if len(args) == 2:
            g.busy_fraction = flt(args[1]) / 100
        if not 0 <= g.busy_fraction <= 1:
            Error("busy_time must be a float on [0, 1]")


if 1:  # Core functionality

    def Child(number, lifetime, busy_time):
        """Start a child process that runs for lifetime seconds, then exits.  busy_time is a float on
        [0, 1] that is how long to run in seconds.  1 - busy_time is the time that the child
        process should sleep.  number is an integer identifying the child.
        """
        assert 0 <= busy_time <= 1
        runtime_s = busy_time
        sleeptime_s = 1 - busy_time
        # Note:  Stopwatch is a class instance that returns a flt (type of float in f.py) that is
        # the time in seconds since it was instantiated when its __call__ method is called.
        sw = timer.Stopwatch()
        try:
            while sw() < lifetime:
                t = sw()  # Current elapsed time
                while sw() - t < runtime_s:
                    pass  # Busy loop for runtime_s
                time.sleep(sleeptime_s)  # Sleep for sleeptime_s
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    d = {}  # Options dictionary
    ParseCommandLine(d)
    # g.n has number of children to launch
    # g.busy_fraction is fraction of 1 second to run
    # g.die is time in s to die
    Dbg(f"  Number of children   {g.n}")
    Dbg(f"  Busy fraction        {g.busy_fraction}")
    Dbg(f"  Lifetime             {g.lifetime} s")
    # Main processing:  start g.n children
    g.sw = timer.Stopwatch()
    g.children = []
    Dbg(f"Starting child processes")
    for number in range(g.n):
        p = Process(target=Child, args=(number, g.lifetime, g.busy_fraction))
        Dbg(f"  Child {number} created")
        p.start()
        g.children.append(p)
        print(f"Child {number} started (pid = {p.pid})")
    # Wait for each child to terminate
    plural = "es" if g.n > 1 else ""
    Dbg(f"Waiting for child process{plural} to finish")
    try:
        for child in g.children:
            child.join()
    except KeyboardInterrupt:
        pass
    print(f"{sys.argv[0]} finished after {g.sw()} s")
